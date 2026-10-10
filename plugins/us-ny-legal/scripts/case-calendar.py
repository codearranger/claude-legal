#!/usr/bin/env python3
"""
case-calendar.py — Compute New York court deadlines.

Supports calendar-day and court-day counting with New York state
holidays (NY Gen. Constr. Law § 24 + § 25-a) excluded for court-
day mode.

Usage:
    case-calendar.py --from YYYY-MM-DD --days N --mode [calendar|court]
    case-calendar.py --from YYYY-MM-DD --rule RULE_KEY
    case-calendar.py --rules

Examples:
    # Answer due — 20 calendar days from personal service 2025-04-15
    case-calendar.py --from 2025-04-15 --days 20 --mode calendar

    # SOL on consumer-credit (post-CCFA) — 3 years from default
    case-calendar.py --from 2022-04-15 --rule sol-consumer-credit-ccfa

    # Notice of Motion service period — 8 days minimum (+5 mail)
    case-calendar.py --from 2025-04-15 --rule notice-of-motion-mail

    # List known rules
    case-calendar.py --rules
"""

import argparse
import datetime
import sys
from typing import Optional


# New York legal holidays (NY Gen. Constr. Law § 24)
# § 25-a: if a holiday falls on Saturday, the Friday before is the
# legal holiday for "public business"; if on Sunday, the Monday
# after.
# CPLR 2103(c) and CPLR 2103-a use a slightly different rule —
# forward-roll to next business day when computing a CPLR deadline
# falling on a weekend/holiday.
FIXED_HOLIDAYS = [
    (1, 1),    # New Year's Day
    (2, 12),   # Lincoln's Birthday — NY-distinctive
    (6, 19),   # Juneteenth — added 2020/2024
    (7, 4),    # Independence Day
    (11, 11),  # Veterans Day
    (12, 25),  # Christmas Day
]

# Week-based holidays (n-th weekday of month)
WEEK_HOLIDAYS = [
    # (month, weekday [0=Mon], ordinal [1=first, -1=last])
    (1, 0, 3),   # MLK — 3rd Monday of January
    (2, 0, 3),   # Presidents' Day — 3rd Monday of February
    (5, 0, -1),  # Memorial Day — last Monday of May
    (9, 0, 1),   # Labor Day — 1st Monday of September
    (10, 0, 2),  # Columbus Day / Indigenous Peoples' Day — 2nd Monday of October
    (11, 3, 4),  # Thanksgiving — 4th Thursday of November
]


def _election_day(year: int) -> datetime.date:
    """Election Day: Tuesday after the first Monday in November.
    Annual NY court holiday (NY Gen. Constr. Law § 24)."""
    nov1 = datetime.date(year, 11, 1)
    first_monday = nov1 + datetime.timedelta(days=(7 - nov1.weekday()) % 7)
    return first_monday + datetime.timedelta(days=1)


# Named rules: (days, mode, description, authority)
RULES = {
    # Initial response — CPLR 3012
    "answer-personal": (
        20, "calendar",
        "Answer due after personal service in-state (CPLR 308(1))",
        "CPLR 3012(a), 3012(c)",
    ),
    "answer-substituted": (
        30, "calendar",
        "Answer due after substituted service (CPLR 308(2) — service complete 10 days after filing affidavit)",
        "CPLR 3012(c), CPLR 308(2)",
    ),
    "answer-nail-and-mail": (
        30, "calendar",
        "Answer due after nail-and-mail service (CPLR 308(4))",
        "CPLR 3012(c), CPLR 308(4)",
    ),
    "answer-out-of-state": (
        30, "calendar",
        "Answer due after personal service out-of-state",
        "CPLR 3012(c)",
    ),
    "answer-secretary-of-state": (
        30, "calendar",
        "Answer due after service on Secretary of State for corporation",
        "CPLR 3012(c), CPLR 311",
    ),

    # Service of process
    "service-of-summons": (
        120, "calendar",
        "Service of summons + complaint must be completed within 120 days of filing",
        "CPLR 306-b",
    ),

    # Motion practice — CPLR 2214
    "notice-of-motion": (
        8, "calendar",
        "Minimum service period before motion return date (CPLR 2214(b))",
        "CPLR 2214(b)",
    ),
    "notice-of-motion-mail": (
        13, "calendar",
        "Minimum service period before motion return date when serving by mail (8 + 5 mail rule)",
        "CPLR 2214(b), 2103(b)(2)",
    ),
    "cross-motion": (
        7, "calendar",
        "Cross-motion must be served at least 7 days before return date",
        "CPLR 2215",
    ),
    "opposition-papers": (
        7, "calendar",
        "Default: opposition papers must be served at least 7 days before return date (varies per Part Rules)",
        "CPLR 2214(b)",
    ),

    # Discovery — CPLR Article 31
    "rfp-response": (
        20, "calendar",
        "Notice for Discovery and Inspection (RFPs) response due",
        "CPLR 3120(2)",
    ),
    "interrogatory-response": (
        20, "calendar",
        "Interrogatory response due (CPLR 3133(a))",
        "CPLR 3133(a)",
    ),
    "notice-to-admit-response": (
        20, "calendar",
        "Notice to Admit response due (non-response = deemed admitted)",
        "CPLR 3123(a)",
    ),
    "deposition-notice": (
        20, "calendar",
        "Deposition (EBT) notice — minimum 20 days",
        "CPLR 3107",
    ),
    "bill-of-particulars": (
        30, "calendar",
        "Bill of Particulars demand response",
        "CPLR 3042(a)",
    ),

    # Preliminary Conference / Note of Issue
    "preliminary-conference": (
        45, "calendar",
        "Preliminary Conference within 45 days of RJI",
        "22 NYCRR § 202.12",
    ),

    # Post-judgment — CPLR 5015 et seq.
    "motion-vacate-default": (
        365, "calendar",
        "CPLR 5015(a)(1) excusable default — 1-year clock from notice of entry",
        "CPLR 5015(a)(1)",
    ),
    "motion-vacate-jurisdiction": (
        0, "calendar",
        "CPLR 5015(a)(4) lack of jurisdiction — NO time limit",
        "CPLR 5015(a)(4)",
    ),
    "motion-reargument": (
        30, "calendar",
        "Motion for reargument — 30 days from notice of entry",
        "CPLR 2221(d)",
    ),
    "notice-of-appeal-ad": (
        30, "calendar",
        "Notice of Appeal to Appellate Division — 30 days from notice of entry",
        "CPLR 5513(a)",
    ),
    "settle-order-deadline": (
        60, "calendar",
        "22 NYCRR § 202.48 — proposed order must be submitted within 60 days; missing forfeits the right (*Funk v. Barry*)",
        "22 NYCRR § 202.48",
    ),
    "satisfaction-demand-response": (
        20, "calendar",
        "Creditor must file satisfaction within 20 days of debtor's written demand",
        "CPLR 5020(c)",
    ),
    "restraining-notice-duration": (
        365, "calendar",
        "Restraining Notice on debtor or garnishee — effective for 1 year",
        "CPLR 5222(b)",
    ),
    "information-subpoena-response": (
        7, "calendar",
        "Information subpoena response window",
        "CPLR 5224",
    ),

    # Judgment lifespan
    "judgment-life-20-year": (
        7305, "calendar",  # 20 years (approx)
        "Money judgment enforceable for 20 years (the longest in the U.S.)",
        "CPLR 211(b)",
    ),

    # Statutes of limitation — CPLR Article 2
    "sol-consumer-credit-ccfa": (
        1096, "calendar",  # 3 years (approx)
        "SOL — consumer-credit transaction (post-CCFA, 2022): 3 years",
        "CPLR 213(a) (post-CCFA, L 2021, ch 593)",
    ),
    "sol-written-contract": (
        2192, "calendar",  # 6 years
        "SOL — general contract (6 years)",
        "CPLR 213(2)",
    ),
    "sol-account-stated": (
        2192, "calendar",
        "SOL — account stated (6 years)",
        "CPLR 213(2)",
    ),
    "sol-personal-injury": (
        1096, "calendar",  # 3 years
        "SOL — personal injury (3 years)",
        "CPLR 214(5)",
    ),
    "sol-defamation": (
        365, "calendar",
        "SOL — defamation (1 year)",
        "CPLR 215(3)",
    ),
    "sol-fraud-discovery": (
        2192, "calendar",
        "SOL — fraud (6 years from accrual / 2 years from discovery)",
        "CPLR 213(8)",
    ),
    "sol-real-property": (
        7305, "calendar",
        "SOL — recovery of real property (10 years)",
        "CPLR 212",
    ),
    "sol-foreclosure": (
        2192, "calendar",
        "SOL — mortgage foreclosure (6 years; FAPA L 2022, ch 821 — no unilateral revival of acceleration)",
        "CPLR 213(4)",
    ),

    # Consumer-protection SOLs
    "sol-gbl-349": (
        1096, "calendar",
        "SOL — GBL § 349 (3 years)",
        "CPLR 214(2)",
    ),
    "sol-fdcpa": (
        365, "calendar",
        "SOL — FDCPA (1 year from violation)",
        "15 USC § 1692k(d)",
    ),
    "sol-fcra-discovery": (
        730, "calendar",
        "SOL — FCRA (2 years from discovery; 5-year repose)",
        "15 USC § 1681p",
    ),
    "sol-tila": (
        365, "calendar",
        "SOL — TILA (1 year from violation)",
        "15 USC § 1640(e)",
    ),

    # FDCPA / Reg F
    "fdcpa-validation-period": (
        30, "calendar",
        "Consumer's window to dispute debt (FDCPA validation)",
        "15 USC § 1692g; 12 CFR § 1006.34",
    ),

    # Landlord-tenant — RPAPL
    "rpapl-demand-nonpayment": (
        14, "calendar",
        "14-day written demand for rent (predicate to nonpayment proceeding)",
        "RPL § 711(2) (post-HSTPA)",
    ),
    "rpl-226-c-under-1yr": (
        30, "calendar",
        "Notice to vacate — tenant resident less than 1 year",
        "RPL § 226-c(2)(a)",
    ),
    "rpl-226-c-1-to-2yr": (
        60, "calendar",
        "Notice to vacate — tenant resident 1 to 2 years",
        "RPL § 226-c(2)(b)",
    ),
    "rpl-226-c-over-2yr": (
        90, "calendar",
        "Notice to vacate — tenant resident more than 2 years",
        "RPL § 226-c(2)(c)",
    ),
    "answer-summary-proceeding": (
        10, "calendar",
        "Answer in summary proceeding (RPAPL § 743) — typically 7-10 days depending on service",
        "RPAPL § 743",
    ),
}


def _nth_weekday(year: int, month: int, weekday: int, n: int) -> datetime.date:
    """Return date of nth (1..5) or last (-1) weekday in a month."""
    if n > 0:
        first = datetime.date(year, month, 1)
        offset = (weekday - first.weekday()) % 7
        day = 1 + offset + (n - 1) * 7
        return datetime.date(year, month, day)
    else:
        if month == 12:
            next_month_first = datetime.date(year + 1, 1, 1)
        else:
            next_month_first = datetime.date(year, month + 1, 1)
        last_day = next_month_first - datetime.timedelta(days=1)
        offset = (last_day.weekday() - weekday) % 7
        return last_day - datetime.timedelta(days=offset)


def ny_holidays(year: int) -> set:
    """Return set of New York state legal holidays for a year
    (NY Gen. Constr. Law § 24)."""
    holidays = set()

    for m, d in FIXED_HOLIDAYS:
        date = datetime.date(year, m, d)
        # Observed-day shift per NY Gen. Constr. Law § 25-a
        if date.weekday() == 5:   # Saturday → Friday
            date -= datetime.timedelta(days=1)
        elif date.weekday() == 6:  # Sunday → Monday
            date += datetime.timedelta(days=1)
        holidays.add(date)

    for m, wd, n in WEEK_HOLIDAYS:
        holidays.add(_nth_weekday(year, m, wd, n))

    # Election Day — annual in NY
    holidays.add(_election_day(year))

    return holidays


def is_court_day(d: datetime.date) -> bool:
    """True if d is a court day (not a weekend or NY legal holiday)."""
    if d.weekday() >= 5:   # Saturday or Sunday
        return False
    if d in ny_holidays(d.year):
        return False
    return True


def add_calendar_days(start: datetime.date, n: int) -> datetime.date:
    """Add calendar days. Apply CPLR 2103(c) end-of-period rule:
    if the final day falls on weekend or holiday, extend to next
    business day (forward-roll for deadlines)."""
    end = start + datetime.timedelta(days=n)
    if n != 0:
        step = 1 if n > 0 else -1
        while not is_court_day(end):
            end += datetime.timedelta(days=step)
    return end


def add_court_days(start: datetime.date, n: int) -> datetime.date:
    """Count n court days forward (if n>0) or backward (if n<0)."""
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
        description="Compute New York court deadlines"
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
