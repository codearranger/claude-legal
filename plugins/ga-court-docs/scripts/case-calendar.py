#!/usr/bin/env python3
"""
case-calendar.py — Compute Georgia court deadlines.

Supports calendar-day and court-day counting with Georgia legal
holidays (O.C.G.A. § 1-4-1) excluded for court-day mode, and the
Georgia time-computation rules (O.C.G.A. § 1-3-1(d)(3), incorporated
into the Civil Practice Act by O.C.G.A. § 9-11-6(a)):

  - The first day is not counted; the last day is counted.
  - If the last day is a Saturday, Sunday, or § 1-4-1 legal holiday,
    the period runs through the next business day.
  - When the prescribed period is LESS THAN seven days, intermediate
    Saturdays, Sundays, and legal holidays are excluded from the count.

Usage:
    case-calendar.py --from YYYY-MM-DD --days N --mode [calendar|court]
    case-calendar.py --from YYYY-MM-DD --rule RULE_KEY
    case-calendar.py --rules

Examples:
    # Answer due — 30 days from service 2025-04-15
    case-calendar.py --from 2025-04-15 --rule answer-due

    # SOL on a credit-card debt — 6 years from default 2019-03-15
    case-calendar.py --from 2019-03-15 --rule sol-credit-card

    # List known rules
    case-calendar.py --rules

NOTE ON HOLIDAYS: Georgia sets exactly thirteen state-holiday days
each year by gubernatorial proclamation (O.C.G.A. § 1-4-1(b)). Ten of
them follow predictable federal-style rules and are computed here. The
remaining few FLOAT year to year and are NOT auto-computed:
  - Washington's Birthday is statutorily a February federal holiday but
    Georgia defers its OBSERVANCE to the year-end cluster (often Dec. 24).
  - The spring "State Holiday" (the date formerly published as
    Confederate Memorial Day, statutorily anchored near April 26).
  - In some years a second floating "State Holiday."
For court deadlines that land near late December or late April, verify
the court's actual closure against the per-year schedule at
georgia.gov / the AOC, because a floated holiday can push a rollover.
"""

import argparse
import datetime
import sys
from typing import Optional


# Georgia legal holidays with predictable dates (O.C.G.A. § 1-4-1,
# incorporating the federal holidays as of Jan. 1, 2022). Saturday
# observance shifts to Friday; Sunday to Monday (federal practice).
FIXED_HOLIDAYS = [
    (1, 1),    # New Year's Day
    (6, 19),   # Juneteenth (observed in Georgia)
    (7, 4),    # Independence Day
    (11, 11),  # Veterans Day
    (12, 25),  # Christmas Day
]

# Week-based holidays (n-th weekday of month)
WEEK_HOLIDAYS = [
    # (month, weekday [0=Mon], ordinal [1=first, -1=last])
    (1, 0, 3),   # MLK Jr.'s Birthday — 3rd Monday of January
    (5, 0, -1),  # Memorial Day — last Monday of May
    (9, 0, 1),   # Labor Day — 1st Monday of September
    (10, 0, 2),  # Columbus Day — 2nd Monday of October (observed)
    (11, 3, 4),  # Thanksgiving Day — 4th Thursday of November
]


# Named rules: (days, mode, description, authority)
# Day counts for multi-year statutes of limitation are approximate
# (≈365.25/yr); always confirm the exact calendar date and any tolling
# or revival (O.C.G.A. §§ 9-3-110, 9-3-112) before relying on an SOL.
RULES = {
    # --- Initial response (Civil Practice Act) ---
    "answer-due": (
        30, "calendar",
        "Answer due — 30 days after service of summons and complaint",
        "O.C.G.A. § 9-11-12(a)",
    ),
    "open-default-as-of-right": (
        15, "calendar",
        "Open default as a matter of right (pay costs) — 15 days after "
        "the case goes into default; run from the day after answer was due",
        "O.C.G.A. § 9-11-55(a)",
    ),
    "amended-pleading-response": (
        15, "calendar",
        "Response to an amended pleading (or within the original answer "
        "period, whichever is longer)",
        "O.C.G.A. § 9-11-15(a)",
    ),

    # --- Discovery (Civil Practice Act) ---
    "interrogatory-response": (
        30, "calendar",
        "Interrogatory answers due (30 days after service)",
        "O.C.G.A. § 9-11-33(a)",
    ),
    "interrogatory-response-with-summons": (
        45, "calendar",
        "Interrogatory answers due when served with the summons "
        "(defendant gets 45 days after service of summons)",
        "O.C.G.A. § 9-11-33(a)",
    ),
    "rfp-response": (
        30, "calendar",
        "Response to Request for Production due (30 days after service)",
        "O.C.G.A. § 9-11-34(b)",
    ),
    "rfp-response-with-summons": (
        45, "calendar",
        "RFP response due when served with the summons (45 days)",
        "O.C.G.A. § 9-11-34(b)",
    ),
    "rfa-response": (
        30, "calendar",
        "Response to Request for Admission due (30 days); unanswered "
        "matters are DEEMED ADMITTED",
        "O.C.G.A. § 9-11-36(a)",
    ),
    "rfa-response-with-summons": (
        45, "calendar",
        "RFA response due when served with the summons (45 days); "
        "unanswered matters are DEEMED ADMITTED",
        "O.C.G.A. § 9-11-36(a)",
    ),
    "discovery-period": (
        180, "calendar",
        "Default discovery period — 6 months from the filing of the "
        "answer (extendable by order/local rule)",
        "USCR 5",
    ),

    # --- Summary judgment + motion practice ---
    "sj-motion-before-hearing": (
        -30, "calendar",
        "Summary-judgment motion must be served at least 30 days before "
        "the hearing",
        "O.C.G.A. § 9-11-56(c)",
    ),
    "motion-response": (
        30, "calendar",
        "Response to a motion due (typical) — 30 days after service of "
        "the motion",
        "USCR 6.2",
    ),

    # --- Dispossessory (landlord-tenant) ---
    "dispossessory-answer": (
        7, "calendar",
        "Answer to a dispossessory (eviction) summons — 7 days from "
        "actual service",
        "O.C.G.A. § 44-7-51(b)",
    ),
    "dispossessory-writ": (
        7, "calendar",
        "Writ of possession effective 7 days after judgment for the "
        "landlord",
        "O.C.G.A. § 44-7-55(a)",
    ),

    # --- Post-judgment ---
    "motion-new-trial": (
        30, "calendar",
        "Motion for new trial — 30 days after entry of judgment",
        "O.C.G.A. § 5-5-40(a)",
    ),
    "motion-jnov": (
        30, "calendar",
        "Motion for judgment notwithstanding the verdict — 30 days "
        "after entry of judgment",
        "O.C.G.A. § 9-11-50(b)",
    ),
    "notice-of-appeal": (
        30, "calendar",
        "Notice of appeal — 30 days after entry of the appealable order "
        "or judgment",
        "O.C.G.A. § 5-6-38(a)",
    ),
    "set-aside-judgment": (
        1096, "calendar",  # 3 years
        "Motion to set aside (non-amendable defect / certain grounds) — "
        "within 3 years of judgment",
        "O.C.G.A. § 9-11-60(f)",
    ),
    "judgment-dormancy": (
        2557, "calendar",  # 7 years
        "Judgment becomes dormant 7 years after entry unless a writ of "
        "execution is issued and entered on the GED",
        "O.C.G.A. § 9-12-60",
    ),
    "revive-dormant-judgment": (
        1096, "calendar",  # 3 years
        "Revive a dormant judgment (scire facias / renewal) — within 3 "
        "years of dormancy",
        "O.C.G.A. § 9-12-61",
    ),

    # --- Garnishment (post-2016 chapter) ---
    "garnishment-claim": (
        20, "calendar",
        "Defendant's claim/challenge to garnishment — file promptly "
        "(before disbursement/distribution); ~20 days after the "
        "garnishee's answer is the practical window",
        "O.C.G.A. §§ 18-4-15, 18-4-93",
    ),

    # --- FBPA pre-suit demand ---
    "fbpa-demand": (
        -30, "calendar",
        "FBPA written demand for relief must be delivered at least 30 "
        "days BEFORE filing suit (statutory prerequisite; does not toll "
        "the SOL)",
        "O.C.G.A. § 10-1-399(b)",
    ),

    # --- Statutes of limitation (defenses) ---
    "sol-written-contract": (
        2191, "calendar",  # 6 years
        "SOL — simple written contract (6 years from due and payable)",
        "O.C.G.A. § 9-3-24",
    ),
    "sol-credit-card": (
        2191, "calendar",  # 6 years
        "SOL — credit-card debt on a written cardmember agreement "
        "(6 years; Hill v. American Express; Phoenix Recovery v. Mehta)",
        "O.C.G.A. § 9-3-24",
    ),
    "sol-open-account": (
        1461, "calendar",  # 4 years
        "SOL — open account / oral contract / implied promise (4 years); "
        "the better classification where no written agreement is produced",
        "O.C.G.A. § 9-3-25",
    ),
    "sol-contract-catchall": (
        1461, "calendar",  # 4 years
        "SOL — other contracts not otherwise provided for (4 years)",
        "O.C.G.A. § 9-3-26",
    ),
    "sol-personal-injury": (
        730, "calendar",  # 2 years
        "SOL — injuries to the person (2 years)",
        "O.C.G.A. § 9-3-33",
    ),
    "sol-defamation": (
        365, "calendar",  # 1 year
        "SOL — injury to reputation / defamation (1 year)",
        "O.C.G.A. § 9-3-33",
    ),
    "sol-realty": (
        1461, "calendar",  # 4 years
        "SOL — trespass upon or damage to realty (4 years)",
        "O.C.G.A. § 9-3-30",
    ),
    "sol-personalty": (
        1461, "calendar",  # 4 years
        "SOL — injury to / conversion / recovery of personalty (4 years)",
        "O.C.G.A. §§ 9-3-31, 9-3-32",
    ),
    "sol-fbpa": (
        730, "calendar",  # 2 years
        "SOL — Fair Business Practices Act (2 years)",
        "O.C.G.A. § 10-1-401",
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

    # --- FDCPA / Reg F window ---
    "fdcpa-validation-period": (
        30, "calendar",
        "Consumer's window to dispute the debt (FDCPA validation)",
        "15 U.S.C. § 1692g; 12 C.F.R. § 1006.34",
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


def ga_holidays(year: int) -> set:
    """Return the set of predictable Georgia legal holidays for a year
    (O.C.G.A. § 1-4-1). See the module docstring: the floating
    "State Holiday" days and the deferred Washington's Birthday
    observance are proclamation-driven and are NOT included here."""
    holidays = set()

    for m, d in FIXED_HOLIDAYS:
        date = datetime.date(year, m, d)
        if date.weekday() == 5:    # Saturday → Friday
            date -= datetime.timedelta(days=1)
        elif date.weekday() == 6:  # Sunday → Monday
            date += datetime.timedelta(days=1)
        holidays.add(date)

    for m, wd, n in WEEK_HOLIDAYS:
        holidays.add(_nth_weekday(year, m, wd, n))

    # Day after Thanksgiving — published as a "State Holiday" and a
    # routine court-closure day in Georgia.
    thanksgiving = _nth_weekday(year, 11, 3, 4)
    holidays.add(thanksgiving + datetime.timedelta(days=1))

    return holidays


def is_court_day(d: datetime.date) -> bool:
    """True if d is a court day (not a weekend or Georgia legal holiday)."""
    if d.weekday() >= 5:
        return False
    if d in ga_holidays(d.year):
        return False
    return True


def add_calendar_days(start: datetime.date, n: int) -> datetime.date:
    """Add calendar days under O.C.G.A. § 1-3-1(d)(3).

    For a period of 7 or more days: count calendar days, then if the
    last day is a weekend or holiday extend to the next business day.
    For a period of FEWER than 7 days: exclude intermediate weekends
    and holidays from the count (effectively count business days)."""
    if n == 0:
        return start
    if abs(n) < 7:
        # Sub-7-day periods exclude intermediate Sat/Sun/holidays.
        return add_court_days(start, n)
    end = start + datetime.timedelta(days=n)
    step = 1 if n > 0 else -1
    while not is_court_day(end):
        end += datetime.timedelta(days=step)
    return end


def add_court_days(start: datetime.date, n: int) -> datetime.date:
    """Count n court days forward (n>0) or backward (n<0)."""
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
        lines.append("  Status: TODAY")
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
    parser = argparse.ArgumentParser(description="Compute Georgia court deadlines")
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
