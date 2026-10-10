#!/usr/bin/env python3
"""
case-calendar.py — Compute Michigan court deadlines.

Supports calendar-day and court-day counting with Michigan legal
holidays (MCL 435.101) excluded for court-day mode. Time computation
follows MCR 1.108 (exclude the first day, include the last; if the
last day is a Saturday, Sunday, or legal holiday, roll forward to the
next business day) with the MCR 2.107(C) mail add-on baked into the
mail-service named rules.

Usage:
    case-calendar.py --from YYYY-MM-DD --days N --mode [calendar|court]
    case-calendar.py --from YYYY-MM-DD --rule RULE_KEY
    case-calendar.py --rules

Examples:
    # Answer due — 21 calendar days from personal service 2025-04-15
    case-calendar.py --from 2025-04-15 --days 21 --mode calendar

    # SOL on contract — 6 years from last activity 2019-03-15
    case-calendar.py --from 2019-03-15 --rule sol-written-contract

    # Apply a named rule
    case-calendar.py --from 2025-04-15 --rule answer-due-personal

    # List known rules
    case-calendar.py --rules
"""

import argparse
import datetime
import sys
from typing import Optional


# Michigan legal holidays (MCL 435.101)
# Holidays falling on Saturday are observed on Friday; Sunday -> Monday
# (standard "observed-day" shifting).
#
# NOTE: Michigan IS distinctive in recognizing Lincoln's Birthday
# (February 12) as a legal holiday under MCL 435.101 — most states do
# not. Columbus Day (2nd Monday of October) is also enumerated.
FIXED_HOLIDAYS = [
    (1, 1),    # New Year's Day
    (2, 12),   # Lincoln's Birthday (Michigan-distinctive)
    (6, 19),   # Juneteenth
    (7, 4),    # Independence Day
    (11, 11),  # Veterans Day
    (12, 25),  # Christmas Day
]

# Week-based holidays (n-th weekday of month)
WEEK_HOLIDAYS = [
    # (month, weekday [0=Mon], ordinal [1=first, -1=last])
    (1, 0, 3),   # MLK — 3rd Monday of January
    (2, 0, 3),   # Washington's Birthday / Presidents' Day — 3rd Monday of February
    (5, 0, -1),  # Memorial Day — last Monday of May
    (9, 0, 1),   # Labor Day — 1st Monday of September
    (10, 0, 2),  # Columbus Day — 2nd Monday of October (enumerated in MCL 435.101)
    (11, 3, 4),  # Thanksgiving — 4th Thursday of November
]


# Named rules: (days, mode, description, authority)
RULES = {
    # Initial response
    "answer-due-personal": (
        21, "calendar",
        "Answer due after personal service in Michigan",
        "MCR 2.108(A)(1)",
    ),
    "answer-due-mail-or-out-of-state": (
        28, "calendar",
        "Answer due after service by mail or on an out-of-state party "
        "(includes the MCR 2.107(C) mail add-on)",
        "MCR 2.108(A)(2); MCR 2.107(C)",
    ),

    # Motion practice
    "motion-for-reconsideration": (
        21, "calendar",
        "Motion for reconsideration after entry of order/judgment",
        "MCR 2.119(F)",
    ),

    # Appeals
    "claim-of-appeal": (
        21, "calendar",
        "Claim of appeal of right to the Court of Appeals",
        "MCR 7.204(A)",
    ),

    # Statutes of limitation (defenses)
    "sol-written-contract": (
        2191, "calendar",  # 6 years (approx; account for leap years as ~365.25)
        "SOL — contract (6 years)",
        "MCL 600.5807",
    ),
    "sol-injury": (
        1096, "calendar",  # 3 years (approx; 3*365 + 1 leap)
        "SOL — personal injury / injury to person or property (3 years)",
        "MCL 600.5805",
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


def mi_holidays(year: int) -> set:
    """Return set of Michigan legal holidays for a year (MCL 435.101)."""
    holidays = set()

    for m, d in FIXED_HOLIDAYS:
        date = datetime.date(year, m, d)
        # Observed-day shift (Saturday → Friday; Sunday → Monday)
        if date.weekday() == 5:   # Saturday → Friday
            date -= datetime.timedelta(days=1)
        elif date.weekday() == 6:  # Sunday → Monday
            date += datetime.timedelta(days=1)
        holidays.add(date)

    for m, wd, n in WEEK_HOLIDAYS:
        holidays.add(_nth_weekday(year, m, wd, n))

    # Michigan courts observe the Friday after Thanksgiving as a court
    # holiday. (It is not separately enumerated in MCL 435.101, but it
    # is a court-administrative holiday in Michigan practice.)
    thanksgiving = _nth_weekday(year, 11, 3, 4)
    holidays.add(thanksgiving + datetime.timedelta(days=1))

    return holidays


def is_court_day(d: datetime.date) -> bool:
    """True if d is a court day (not a weekend or Michigan legal holiday)."""
    if d.weekday() >= 5:   # Saturday or Sunday
        return False
    if d in mi_holidays(d.year):
        return False
    return True


def add_calendar_days(start: datetime.date, n: int) -> datetime.date:
    """Add calendar days. Apply MCR 1.108 end-of-period rule:
    exclude the first day and include the last; if the final day falls on
    a Saturday, Sunday, or legal holiday, roll forward to the next
    business day."""
    end = start + datetime.timedelta(days=n)
    if n != 0:
        # MCR 1.108: if last day is weekend or holiday, roll forward to
        # the next business day (forward computation).
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
    print("Michigan named deadline rules (MCR 1.108 / MCL 435.101):")
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
        description="Compute Michigan court deadlines (MCR 1.108 / MCL 435.101)"
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
