#!/usr/bin/env python3
"""
case-calendar.py — Compute California court deadlines.

Supports calendar-day and court-day counting with California state
legal holidays (Cal. Govt. Code §§ 6700, 6701; Cal. Code Civ. Proc.
§ 135) excluded for court-day mode.

Time computation per CCP § 12 (exclude first day, include last;
extend if last day is a holiday) and CCP § 12a (any holiday observed
under Govt. Code § 6700 + judicial holidays).

Usage:
    case-calendar.py --from YYYY-MM-DD --days N --mode [calendar|court]
    case-calendar.py --from YYYY-MM-DD --rule RULE_KEY
    case-calendar.py --rules

Examples:
    # Answer due — 30 calendar days from service 2026-04-15
    case-calendar.py --from 2026-04-15 --days 30 --mode calendar

    # SOL on written contract — 4 years from breach 2022-03-15
    case-calendar.py --from 2022-03-15 --rule sol-written-contract

    # Apply a named rule
    case-calendar.py --from 2026-04-15 --rule answer-due

    # List known rules
    case-calendar.py --rules
"""

import argparse
import datetime
import sys
from typing import Optional


# California legal holidays (Cal. Govt. Code §§ 6700-6701).
#
# For "judicial holiday" purposes, CCP § 135 incorporates Govt. Code
# § 6700 plus any other day judges declare. NOTE: CCP § 135 has been
# amended several times — practitioners should confirm specific
# holidays for the year against the Judicial Council's annual calendar
# at courts.ca.gov.
#
# Holidays falling on Saturday are observed on Friday; Sunday is
# observed on Monday (Govt. Code § 6700(a) general rule for state
# holidays).
#
# NOTE: California DOES recognize the Friday after Thanksgiving as a
# state holiday (Govt. Code § 6700(a)(14)). Oregon does NOT.
FIXED_HOLIDAYS = [
    (1, 1),    # New Year's Day (Govt. Code § 6700(a)(1))
    (2, 12),   # Lincoln's Birthday (Govt. Code § 6700(a)(3); some
               # courts observe, others do not — included by default
               # because CCP § 135 incorporates Govt. Code § 6700)
    (3, 31),   # Cesar Chavez Day (Govt. Code § 6700(a)(13); judicial
               # holiday per Stats. 2014, ch. 310)
    (6, 19),   # Juneteenth (added by Stats. 2022, ch. 33)
    (7, 4),    # Independence Day (Govt. Code § 6700(a)(7))
    (11, 11),  # Veterans Day (Govt. Code § 6700(a)(11))
    (12, 25),  # Christmas Day (Govt. Code § 6700(a)(15))
]

# Week-based holidays (n-th weekday of month).
# CA has a heavier mid- to late-year week-holiday calendar than many
# states because of the day-after-Thanksgiving holiday.
WEEK_HOLIDAYS = [
    # (month, weekday [0=Mon], ordinal [1=first, -1=last])
    (1, 0, 3),   # MLK Day — 3rd Monday of January (Govt. Code § 6700(a)(2))
    (2, 0, 3),   # Presidents' Day — 3rd Monday of February (Govt. Code § 6700(a)(4))
    (5, 0, -1),  # Memorial Day — last Monday of May (Govt. Code § 6700(a)(6))
    (9, 0, 1),   # Labor Day — 1st Monday of September (Govt. Code § 6700(a)(9))
    (11, 3, 4),  # Thanksgiving — 4th Thursday of November (Govt. Code § 6700(a)(12))
]


# Named rules: (days, mode, description, authority).
#
# California's hallmark distinction from most states is the heavy use
# of "court days" rather than calendar days for motion practice (e.g.,
# CCP § 1005(b) sets motion notice at 16 court days, opposition at 9
# court days before hearing, reply at 5 court days before).
RULES = {
    # Initial response
    "answer-due": (
        30, "calendar",
        "Answer due after personal service in California",
        "Code Civ. Proc., § 412.20(a)(3)",
    ),
    "answer-due-norf": (
        30, "calendar",
        "Answer due after service by mail w/ NORF "
        "(time runs from completed service date, then 30 days)",
        "Code Civ. Proc., §§ 412.20(a)(3), 415.30",
    ),
    "demurrer-due": (
        30, "calendar",
        "Demurrer due (same as answer; CCP § 430.40 also permits at "
        "any time before answer)",
        "Code Civ. Proc., § 430.40",
    ),
    "meet-confer-demurrer": (
        -5, "calendar",
        "Meet-and-confer required at least 5 days before filing "
        "demurrer (CCP § 430.41)",
        "Code Civ. Proc., § 430.41(a)(2)",
    ),
    "meet-confer-strike": (
        -5, "calendar",
        "Meet-and-confer required at least 5 days before filing "
        "motion to strike (CCP § 435.5)",
        "Code Civ. Proc., § 435.5(a)(2)",
    ),
    "anti-slapp-window": (
        60, "calendar",
        "Anti-SLAPP motion must be filed within 60 days of service "
        "of complaint",
        "Code Civ. Proc., § 425.16(f)",
    ),

    # Discovery
    "rfp-response": (
        30, "calendar",
        "RFP response due (CCP § 2031.260) — 30 days from service "
        "of the request",
        "Code Civ. Proc., § 2031.260",
    ),
    "rog-response": (
        30, "calendar",
        "Interrogatory response due (CCP § 2030.260) — 30 days from "
        "service of the rogs",
        "Code Civ. Proc., § 2030.260",
    ),
    "rfa-response": (
        30, "calendar",
        "RFA response due (CCP § 2033.250) — 30 days from service; "
        "failure to respond may deem admissions under § 2033.280",
        "Code Civ. Proc., § 2033.250",
    ),
    "discovery-response-mail-add": (
        5, "calendar",
        "Mail extension for in-state mail service (add to 30-day "
        "response window)",
        "Code Civ. Proc., § 1013(a)",
    ),
    "motion-compel-further": (
        45, "calendar",
        "Motion to compel further responses — 45 days from service "
        "of the verified responses; JURISDICTIONAL deadline",
        "Code Civ. Proc., §§ 2030.300(c), 2031.310(c), 2033.290(c)",
    ),
    "deposition-notice-party": (
        10, "calendar",
        "Deposition notice — party (10 days; CCP § 2025.270)",
        "Code Civ. Proc., § 2025.270",
    ),
    "deposition-subpoena-nonparty": (
        20, "calendar",
        "Deposition subpoena for non-party records — 20 days for "
        "consumer notice (CCP § 1985.3) and 15 days for objection",
        "Code Civ. Proc., §§ 1985.3, 2020.410",
    ),
    "discovery-cutoff": (
        -30, "calendar",
        "Discovery cutoff — 30 days before trial date (motions to "
        "compel must be HEARD 15 days before trial; § 2024.020)",
        "Code Civ. Proc., § 2024.020(a)",
    ),
    "discovery-motion-cutoff": (
        -15, "calendar",
        "Discovery motions must be heard (not just filed) 15 days "
        "before trial",
        "Code Civ. Proc., § 2024.020(a)",
    ),

    # Motion practice — CCP § 1005(b)
    "motion-notice-min": (
        -16, "court",
        "Minimum notice period for motions: 16 court days before "
        "the hearing (CCP § 1005(b))",
        "Code Civ. Proc., § 1005(b)",
    ),
    "motion-notice-mail-add": (
        5, "calendar",
        "Extra time for in-state mail service of motion papers "
        "(add 5 calendar days; CCP § 1013(a))",
        "Code Civ. Proc., § 1013(a)",
    ),
    "motion-notice-eservice-add": (
        2, "court",
        "Extra time for electronic service of motion papers "
        "(add 2 court days; CCP § 1010.6(a)(3)(B))",
        "Code Civ. Proc., § 1010.6(a)(3)(B)",
    ),
    "motion-opposition": (
        -9, "court",
        "Opposition to motion due 9 court days before hearing",
        "Code Civ. Proc., § 1005(b)",
    ),
    "motion-reply": (
        -5, "court",
        "Reply to motion due 5 court days before hearing",
        "Code Civ. Proc., § 1005(b)",
    ),

    # Summary judgment / adjudication (CCP § 437c)
    "sj-notice-min": (
        -75, "calendar",
        "MSJ/MSA notice — 75 calendar days before hearing",
        "Code Civ. Proc., § 437c(a)(2)",
    ),
    "sj-opposition": (
        -14, "calendar",
        "Opposition to MSJ/MSA due 14 calendar days before hearing",
        "Code Civ. Proc., § 437c(b)(2)",
    ),
    "sj-reply": (
        -5, "calendar",
        "Reply to MSJ/MSA opposition due 5 calendar days before "
        "hearing",
        "Code Civ. Proc., § 437c(b)(4)",
    ),
    "sj-trial-cutoff": (
        -30, "calendar",
        "MSJ/MSA must be HEARD no later than 30 days before trial",
        "Code Civ. Proc., § 437c(a)(3)",
    ),

    # Case management (CRC 3.700-3.770)
    "cmc-statement-due": (
        -15, "calendar",
        "Case Management Conference Statement due 15 calendar days "
        "before CMC (CRC 3.725)",
        "Cal. Rules of Court, rule 3.725",
    ),

    # Post-judgment / relief
    "ccp-473-relief": (
        180, "calendar",
        "CCP § 473(b) relief from default/order — up to 6 months "
        "(approx. 180 calendar days)",
        "Code Civ. Proc., § 473(b)",
    ),
    "new-trial-motion": (
        15, "calendar",
        "Notice of intention to move for new trial — 15 days after "
        "service of notice of entry of judgment (or 180 days after "
        "filing of judgment, whichever first)",
        "Code Civ. Proc., § 659",
    ),
    "appeal-civil": (
        60, "calendar",
        "Notice of appeal — 60 days after notice of entry of "
        "judgment (or 180 days after entry; whichever first)",
        "Cal. Rules of Court, rule 8.104(a)",
    ),
    "memorandum-of-costs": (
        15, "calendar",
        "Memorandum of Costs (Form MC-010) — 15 days after notice "
        "of entry of judgment or service of judgment (CRC 3.1700(a))",
        "Cal. Rules of Court, rule 3.1700(a)",
    ),
    "motion-tax-costs": (
        15, "calendar",
        "Motion to tax costs — 15 days after service of Memorandum "
        "of Costs (CRC 3.1700(b))",
        "Cal. Rules of Court, rule 3.1700(b)",
    ),
    "judgment-life": (
        3653, "calendar",  # ~10 years (3652 calendar + leap)
        "Money judgment enforceability — 10 years; renewable for "
        "additional 10 years under CCP § 683.110",
        "Code Civ. Proc., §§ 683.020, 683.110",
    ),

    # Garnishment / exemptions
    "claim-of-exemption": (
        15, "calendar",
        "Claim of Exemption (Form EJ-160) — 15 days from service of "
        "Notice of Levy or Earnings Withholding Order",
        "Code Civ. Proc., § 703.520",
    ),

    # Proposed orders (CRC 3.1312)
    "proposed-order-serve": (
        5, "court",
        "Prevailing party must serve proposed order within 5 court "
        "days of ruling",
        "Cal. Rules of Court, rule 3.1312(a)",
    ),
    "proposed-order-object": (
        5, "court",
        "Opposing party has 5 court days to object to form of "
        "proposed order",
        "Cal. Rules of Court, rule 3.1312(a)",
    ),

    # Statutes of limitations (defenses)
    "sol-written-contract": (
        1461, "calendar",  # 4 years (3 * 365 + 366 leap)
        "SOL — written contract (4 years)",
        "Code Civ. Proc., § 337",
    ),
    "sol-oral-contract": (
        730, "calendar",
        "SOL — oral contract (2 years)",
        "Code Civ. Proc., § 339",
    ),
    "sol-open-book-account": (
        1461, "calendar",
        "SOL — open book account (4 years from last entry)",
        "Code Civ. Proc., § 337(a)",
    ),
    "sol-personal-injury": (
        730, "calendar",
        "SOL — personal injury (2 years)",
        "Code Civ. Proc., § 335.1",
    ),
    "sol-fraud": (
        1095, "calendar",
        "SOL — fraud (3 years; discovery rule per § 338(d))",
        "Code Civ. Proc., § 338(d)",
    ),
    "sol-statutory-liability": (
        1095, "calendar",
        "SOL — statutory liability where no other period specified "
        "(3 years)",
        "Code Civ. Proc., § 338(a)",
    ),
    "sol-real-property": (
        1826, "calendar",
        "SOL — recovery of real property (5 years)",
        "Code Civ. Proc., § 318",
    ),
    "sol-ucc-art-2": (
        1461, "calendar",
        "SOL — sale of goods (UCC Art. 2; 4 years from breach)",
        "Cal. Comm. Code, § 2725",
    ),
    "sol-ucc-art-3": (
        2191, "calendar",
        "SOL — negotiable instrument (UCC Art. 3; 6 years from due "
        "date)",
        "Cal. Comm. Code, § 3118",
    ),

    # Consumer-protection SOLs
    "sol-rosenthal": (
        365, "calendar",
        "SOL — Rosenthal Fair Debt Collection Practices Act (1 year "
        "from violation)",
        "Civ. Code, § 1788.30(f)",
    ),
    "sol-fdbpa": (
        365, "calendar",
        "SOL — Fair Debt Buying Practices Act (1 year from violation)",
        "Civ. Code, § 1788.62",
    ),
    "sol-ucl": (
        1461, "calendar",
        "SOL — Unfair Competition Law (4 years)",
        "Bus. & Prof. Code, § 17208",
    ),
    "sol-clra": (
        1095, "calendar",
        "SOL — Consumers Legal Remedies Act (3 years)",
        "Civ. Code, § 1783",
    ),
    "sol-fdcpa": (
        365, "calendar",
        "SOL — FDCPA (1 year from violation)",
        "15 U.S.C. § 1692k(d)",
    ),
    "sol-fcra-discovery": (
        730, "calendar",
        "SOL — FCRA (2 years from discovery; 5-year repose)",
        "15 U.S.C. § 1681p",
    ),
    "sol-tila": (
        365, "calendar",
        "SOL — TILA (1 year from violation)",
        "15 U.S.C. § 1640(e)",
    ),

    # FDCPA / Reg F window
    "fdcpa-validation-period": (
        30, "calendar",
        "Consumer's window to dispute debt (FDCPA validation)",
        "15 U.S.C. § 1692g; 12 C.F.R. § 1006.34",
    ),

    # CLRA pre-suit notice
    "clra-pre-suit-notice": (
        30, "calendar",
        "CLRA pre-suit notice — 30 days before damages claim filed",
        "Civ. Code, § 1782",
    ),

    # FDBPA pleading / chain-of-title window (no deadline per se,
    # but relevant timing rules under § 1788.58 et seq.)
}


def _nth_weekday(year: int, month: int, weekday: int, n: int) -> datetime.date:
    """Return date of nth (1..5) or last (-1) weekday in a month."""
    if n > 0:
        first = datetime.date(year, month, 1)
        offset = (weekday - first.weekday()) % 7
        day = 1 + offset + (n - 1) * 7
        return datetime.date(year, month, day)
    else:
        # Last weekday
        if month == 12:
            next_month_first = datetime.date(year + 1, 1, 1)
        else:
            next_month_first = datetime.date(year, month + 1, 1)
        last_day = next_month_first - datetime.timedelta(days=1)
        offset = (last_day.weekday() - weekday) % 7
        return last_day - datetime.timedelta(days=offset)


def _day_after_thanksgiving(year: int) -> datetime.date:
    """Return the Friday after Thanksgiving (4th Thursday of November)
    for a given year. CA recognizes this as a state holiday under
    Govt. Code § 6700(a)(14)."""
    thanksgiving = _nth_weekday(year, 11, 3, 4)  # 4th Thursday Nov
    return thanksgiving + datetime.timedelta(days=1)


def ca_holidays(year: int) -> set:
    """Return the set of California state legal holidays for a year.

    Sources:
      - Cal. Govt. Code §§ 6700, 6701 (state holidays)
      - Cal. Code Civ. Proc. § 135 (judicial holidays incorporate
        Govt. Code holidays)
      - Stats. 2022, ch. 33 (Juneteenth)
      - Stats. 2014, ch. 310 (Cesar Chavez Day judicial holiday)

    For "court day" purposes, the function returns the days CCP § 12a
    treats as non-court days. Some practical caveats:
      - Cesar Chavez Day (March 31) is observed by state agencies but
        treated as a judicial holiday only in years when courts
        choose to observe; default behavior is to include it.
      - Lincoln's Birthday (Feb 12) — many CA courts observe; included
        by default.
      - Individual Superior Courts may close on additional days;
        verify against the court's own calendar.
    """
    holidays = set()

    for m, d in FIXED_HOLIDAYS:
        date = datetime.date(year, m, d)
        # Observed-day shift (CCP § 10 / general practice):
        # Saturday → previous Friday; Sunday → next Monday.
        if date.weekday() == 5:   # Saturday → Friday
            date -= datetime.timedelta(days=1)
        elif date.weekday() == 6:  # Sunday → Monday
            date += datetime.timedelta(days=1)
        holidays.add(date)

    for m, wd, n in WEEK_HOLIDAYS:
        holidays.add(_nth_weekday(year, m, wd, n))

    # Day after Thanksgiving — Govt. Code § 6700(a)(14). California
    # observes this; Oregon (where the OR plugin was scaffolded from)
    # does not.
    holidays.add(_day_after_thanksgiving(year))

    return holidays


def is_court_day(d: datetime.date) -> bool:
    """True if d is a court day (not a weekend or CA legal holiday)."""
    if d.weekday() >= 5:   # Saturday or Sunday
        return False
    if d in ca_holidays(d.year):
        return False
    return True


def add_calendar_days(start: datetime.date, n: int) -> datetime.date:
    """Add calendar days. Apply CCP § 12 / § 12a end-of-period rule:
    if the final day falls on a weekend or holiday, extend to the next
    business day (only for forward computation)."""
    end = start + datetime.timedelta(days=n)
    if n != 0:
        step = 1 if n > 0 else -1
        while not is_court_day(end):
            end += datetime.timedelta(days=step)
    return end


def add_court_days(start: datetime.date, n: int) -> datetime.date:
    """Count n court days forward (if n>0) or backward (if n<0).

    CCP § 12c — "court day" means any day other than Saturday,
    Sunday, or a judicial holiday.
    """
    if n == 0:
        return start
    step = 1 if n > 0 else -1
    remaining = abs(n)
    current = start
    while remaining > 0:
        current += datetime.timedelta(days=step)
        if is_court_day(current):
            remaining -= 1
    return current


def compute_deadline(start: datetime.date, days: int, mode: str) -> datetime.date:
    if mode == "calendar":
        return add_calendar_days(start, days)
    elif mode == "court":
        return add_court_days(start, days)
    else:
        raise ValueError(f"Unknown mode: {mode}")


def format_result(
    start: datetime.date,
    days: int,
    mode: str,
    deadline: datetime.date,
    description: Optional[str] = None,
    authority: Optional[str] = None,
) -> str:
    direction = "after" if days >= 0 else "before"
    n = abs(days)
    header = f"Deadline: {deadline.strftime('%A, %B %d, %Y')}"
    if description:
        header = f"{description}\n{header}"
    lines = [header]
    lines.append(f"  From: {start.strftime('%A, %B %d, %Y')}")
    lines.append(f"  {n} {mode} day{'s' if n != 1 else ''} {direction}")
    if authority:
        lines.append(f"  Authority: {authority}")
    today = datetime.date.today()
    delta = (deadline - today).days
    if delta == 0:
        lines.append(f"  Status: TODAY")
    elif delta < 0:
        lines.append(f"  Status: {abs(delta)} day(s) ago (OVERDUE if not done)")
    else:
        lines.append(f"  Status: {delta} day(s) from today")
    return "\n".join(lines)


def list_rules():
    print("Known rules:")
    print()
    for key, (days, mode, desc, auth) in sorted(RULES.items()):
        direction = "" if days == 0 else (f"+{days}" if days > 0 else f"{days}")
        print(f"  {key}")
        print(f"    {desc}")
        print(f"    {direction} {mode} days")
        print(f"    {auth}")
        print()


def parse_date(s: str) -> datetime.date:
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        print(f"Error: date '{s}' is not in YYYY-MM-DD format", file=sys.stderr)
        sys.exit(2)


def main():
    parser = argparse.ArgumentParser(
        description="Compute California court deadlines"
    )
    parser.add_argument("--from", dest="from_date", help="Triggering date (YYYY-MM-DD)")
    parser.add_argument("--days", type=int, help="Number of days (negative = before)")
    parser.add_argument(
        "--mode",
        choices=["calendar", "court"],
        default="calendar",
        help="Calendar days (default) or court days",
    )
    parser.add_argument("--rule", help="Named rule (see --rules)")
    parser.add_argument("--rules", action="store_true", help="List known rules")
    args = parser.parse_args()

    if args.rules:
        list_rules()
        return 0

    if not args.from_date:
        parser.error("--from is required")

    start = parse_date(args.from_date)

    if args.rule:
        if args.rule not in RULES:
            print(f"Error: unknown rule '{args.rule}'. Run --rules to list.", file=sys.stderr)
            return 2
        days, mode, desc, auth = RULES[args.rule]
        deadline = compute_deadline(start, days, mode)
        print(format_result(start, days, mode, deadline, desc, auth))
        return 0

    if args.days is None:
        parser.error("Either --days or --rule is required")

    deadline = compute_deadline(start, args.days, args.mode)
    print(format_result(start, args.days, args.mode, deadline))
    return 0


if __name__ == "__main__":
    sys.exit(main())
