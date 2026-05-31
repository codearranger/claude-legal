#!/usr/bin/env python3
"""
case-calendar.py — Compute Arizona court deadlines.

Supports calendar-day and court-day counting with Arizona legal
holidays (A.R.S. § 1-301) excluded for court-day mode, and the
Ariz. R. Civ. P. 6(a) time-computation rule (exclude the first day,
include the last; roll forward off a Saturday, Sunday, or legal
holiday).

Usage:
    case-calendar.py --from YYYY-MM-DD --days N --mode [calendar|court] \
                     [--jurisdiction arizona|federal]
    case-calendar.py --from YYYY-MM-DD --rule RULE_KEY
    case-calendar.py --rules

Examples:
    # Answer due — 20 calendar days from in-state service 2025-04-15
    case-calendar.py --from 2025-04-15 --days 20 --mode calendar

    # SOL on written contract — 6 years from last activity 2019-03-15
    case-calendar.py --from 2019-03-15 --rule sol-written-contract

    # Apply a named rule
    case-calendar.py --from 2025-04-15 --rule answer-due-in-state

    # List known rules
    case-calendar.py --rules
"""

import argparse
import datetime
import sys
from typing import Optional


# Arizona legal holidays (A.R.S. § 1-301).
# Holidays falling on Saturday are observed on Friday; Sunday -> Monday
# (A.R.S. § 1-301(B)-(C)).
#
# NOTE: Arizona's § 1-301 does NOT include Juneteenth.
# Arizona combines Lincoln and Washington into a single observance,
# "Lincoln/Washington Presidents' Day" (3rd Monday of February) — there
# is NO separate Lincoln's Birthday. Likewise the January observance is
# "Martin Luther King Jr./Civil Rights Day."
FIXED_HOLIDAYS = [
    (1, 1),    # New Year's Day
    (7, 4),    # Independence Day
    (11, 11),  # Veterans' Day
    (12, 25),  # Christmas Day
]

# Week-based holidays (n-th weekday of month)
WEEK_HOLIDAYS = [
    # (month, weekday [0=Mon], ordinal [1=first, -1=last])
    (1, 0, 3),   # MLK Jr./Civil Rights Day — 3rd Monday of January
    (2, 0, 3),   # Lincoln/Washington Presidents' Day — 3rd Monday of February
    (5, 0, -1),  # Memorial Day — last Monday of May
    (9, 0, 1),   # Labor Day — 1st Monday of September
    (10, 0, 2),  # Columbus Day — 2nd Monday of October
    (11, 3, 4),  # Thanksgiving — 4th Thursday of November
]


# Named rules: (days, mode, description, authority)
RULES = {
    # Initial response
    "answer-due-in-state": (
        20, "calendar",
        "Answer due after service within Arizona (20 days)",
        "Ariz. R. Civ. P. 12(a)(1)(A)",
    ),
    "answer-due-out-of-state": (
        30, "calendar",
        "Answer due after service outside Arizona (30 days)",
        "Ariz. R. Civ. P. 12(a)(1)(B)",
    ),
    "answer-due-mail": (
        25, "calendar",
        "Answer due after in-state service by mail (20 + 5 mail days)",
        "Ariz. R. Civ. P. 12(a), 6(c)",
    ),
    "response-amended": (
        14, "calendar",
        "Response to amended complaint",
        "Ariz. R. Civ. P. 15(a)(3)",
    ),

    # Discovery
    "rfp-response": (
        40, "calendar",
        "RFP response due (40 days)",
        "Ariz. R. Civ. P. 34(b)(2)",
    ),
    "rfa-response": (
        40, "calendar",
        "RFA response due (40 days); failure deems admitted",
        "Ariz. R. Civ. P. 36(a)(3)",
    ),
    "interrogatory-response": (
        40, "calendar",
        "Interrogatory response due (40 days)",
        "Ariz. R. Civ. P. 33(b)(2)",
    ),
    "deposition-notice": (
        5, "calendar",
        "Reasonable written notice of deposition (5 days customary)",
        "Ariz. R. Civ. P. 30(b)(1)",
    ),

    # Summary judgment (Ariz. R. Civ. P. 56)
    "sj-response": (
        30, "calendar",
        "SJ response due (30 days after service of motion)",
        "Ariz. R. Civ. P. 56(c)(3)",
    ),
    "sj-reply": (
        15, "calendar",
        "SJ reply due (15 days after service of response)",
        "Ariz. R. Civ. P. 56(c)(3)",
    ),

    # Motion practice
    "response-motion": (
        10, "calendar",
        "Response to a non-dispositive motion (10 days)",
        "Ariz. R. Civ. P. 7.1(a)(3)",
    ),
    "reply-motion": (
        5, "calendar",
        "Reply on a non-dispositive motion (5 days)",
        "Ariz. R. Civ. P. 7.1(a)(3)",
    ),

    # Post-judgment
    "new-trial-motion": (
        15, "calendar",
        "Motion for new trial / to alter or amend judgment",
        "Ariz. R. Civ. P. 59(b), 59(d)",
    ),
    "relief-judgment-cap": (
        180, "calendar",
        "Rule 60(c)(1)-(3) — outer 6-month deadline",
        "Ariz. R. Civ. P. 60(c)",
    ),
    "appeal": (
        30, "calendar",
        "Notice of Appeal — superior court to Court of Appeals",
        "ARCAP 9(a)",
    ),
    "cost-bill": (
        10, "calendar",
        "Statement of costs after judgment",
        "A.R.S. § 12-332; Ariz. R. Civ. P. 54(f)",
    ),
    "fee-application": (
        20, "calendar",
        "Application for attorney fees after judgment",
        "Ariz. R. Civ. P. 54(g)(2)",
    ),

    # Arbitration (compulsory arbitration)
    "arbitration-appeal-de-novo": (
        20, "calendar",
        "Appeal from compulsory arbitration award (trial de novo)",
        "Ariz. R. Civ. P. 77(a)",
    ),

    # Statutes of limitation (defenses)
    "sol-written-contract": (
        2191, "calendar",  # 6 years (approx; ~365.25/yr)
        "SOL — written contract / debt (6 years)",
        "A.R.S. § 12-548",
    ),
    "sol-oral-contract": (
        1096, "calendar",  # 3 years
        "SOL — oral or unwritten contract (3 years)",
        "A.R.S. § 12-543",
    ),
    "sol-open-account": (
        1096, "calendar",  # 3 years
        "SOL — open or stated account (3 years)",
        "A.R.S. § 12-543, § 12-544",
    ),
    "sol-tort-personal-injury": (
        730, "calendar",  # 2 years
        "SOL — personal injury (2 years)",
        "A.R.S. § 12-542",
    ),
    "sol-fraud-discovery": (
        1096, "calendar",  # 3 years
        "SOL — fraud (3 years from discovery)",
        "A.R.S. § 12-543(3)",
    ),
    "sol-real-property": (
        3653, "calendar",  # 10 years
        "SOL — recovery of real property (10 years)",
        "A.R.S. § 12-526",
    ),

    # Consumer-protection / federal SOLs
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

    # FDCPA / Reg F window
    "fdcpa-validation-period": (
        30, "calendar",
        "Consumer's window to dispute debt (FDCPA validation)",
        "15 USC § 1692g; 12 CFR § 1006.34",
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
        # Last weekday
        if month == 12:
            next_month_first = datetime.date(year + 1, 1, 1)
        else:
            next_month_first = datetime.date(year, month + 1, 1)
        last_day = next_month_first - datetime.timedelta(days=1)
        offset = (last_day.weekday() - weekday) % 7
        return last_day - datetime.timedelta(days=offset)


def az_holidays(year: int) -> set:
    """Return set of Arizona legal holidays for a year (A.R.S. § 1-301)."""
    holidays = set()

    for m, d in FIXED_HOLIDAYS:
        date = datetime.date(year, m, d)
        # Observed-day shift per A.R.S. § 1-301(B)-(C)
        if date.weekday() == 5:   # Saturday → Friday
            date -= datetime.timedelta(days=1)
        elif date.weekday() == 6:  # Sunday → Monday
            date += datetime.timedelta(days=1)
        holidays.add(date)

    for m, wd, n in WEEK_HOLIDAYS:
        holidays.add(_nth_weekday(year, m, wd, n))

    # A.R.S. § 1-301 does NOT include Juneteenth, nor the day after
    # Thanksgiving, as a state legal holiday.
    return holidays


def is_court_day(d: datetime.date) -> bool:
    """True if d is a court day (not a weekend or Arizona legal holiday)."""
    if d.weekday() >= 5:   # Saturday or Sunday
        return False
    if d in az_holidays(d.year):
        return False
    return True


def add_calendar_days(start: datetime.date, n: int) -> datetime.date:
    """Add calendar days. Apply Ariz. R. Civ. P. 6(a) end-of-period rule:
    exclude the first day, include the last; if the final day falls on a
    Saturday, Sunday, or legal holiday, roll forward to the next court
    day."""
    end = start + datetime.timedelta(days=n)
    if n != 0:
        # Ariz. R. Civ. P. 6(a)(1)(C): if the last day is a Saturday,
        # Sunday, or legal holiday, the period runs to the next court day
        # (forward computation).
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
        description="Compute Arizona court deadlines (Ariz. R. Civ. P. 6 / A.R.S. § 1-301)"
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
