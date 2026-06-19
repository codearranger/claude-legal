#!/usr/bin/env python3
"""
case-calendar.py — Compute Idaho court deadlines.

Supports calendar-day and court-day counting with Idaho legal
holidays (Idaho Code § 73-108) excluded for court-day mode, and the
I.R.C.P. 2.2 time-computation rule (exclude the first day, count every
intervening day including weekends and holidays, include the last day;
if the last day is a Saturday, Sunday, or legal holiday, the period
runs to the next day that is not).

Idaho quirk: time computation lives in **I.R.C.P. 2.2**, NOT Rule 6.
I.R.C.P. 6 is "[Reserved]" in Idaho. Any deadline arithmetic must
point at Rule 2.2. When a period runs from service and service was by
mail, I.R.C.P. 2.2 adds 3 days.

Usage:
    case-calendar.py --from YYYY-MM-DD --days N --mode [calendar|court]
    case-calendar.py --from YYYY-MM-DD --rule RULE_KEY
    case-calendar.py --rules

Examples:
    # Answer due — 21 calendar days from service 2025-04-15
    case-calendar.py --from 2025-04-15 --days 21 --mode calendar

    # SOL on written contract — 5 years from last activity 2019-03-15
    case-calendar.py --from 2019-03-15 --rule sol-written-contract

    # Apply a named rule
    case-calendar.py --from 2025-04-15 --rule answer-due

    # List known rules
    case-calendar.py --rules
"""

import argparse
import datetime
import sys
from typing import Optional


# Idaho legal holidays (Idaho Code § 73-108).
# Observed-day shift (§ 73-108): a holiday that falls on Saturday is
# observed the preceding Friday; a holiday other than Sunday that falls
# on Sunday is observed the following Monday.
#
# NOTE: Idaho's § 73-108 does NOT include Juneteenth as a state legal
# holiday. Idaho DOES observe Columbus Day (2nd Monday of October). The
# January observance is "Martin Luther King, Jr.-Idaho Human Rights Day."
FIXED_HOLIDAYS = [
    (1, 1),    # New Year's Day
    (7, 4),    # Independence Day
    (11, 11),  # Veterans Day
    (12, 25),  # Christmas
]

# Week-based holidays (n-th weekday of month)
WEEK_HOLIDAYS = [
    # (month, weekday [0=Mon], ordinal [1=first, -1=last])
    (1, 0, 3),   # Martin Luther King, Jr.-Idaho Human Rights Day — 3rd Mon Jan
    (2, 0, 3),   # Washington's Birthday — 3rd Mon Feb
    (5, 0, -1),  # Memorial Day — last Mon May
    (9, 0, 1),   # Labor Day — 1st Mon Sep
    (10, 0, 2),  # Columbus Day — 2nd Mon Oct
    (11, 3, 4),  # Thanksgiving Day — 4th Thu Nov
]


# Named rules: (days, mode, description, authority)
RULES = {
    # Initial response
    "answer-due": (
        21, "calendar",
        "Answer due after service of summons and complaint (21 days)",
        "I.R.C.P. 12(a)(1)(A)",
    ),
    "response-amended": (
        14, "calendar",
        "Response to an amended pleading (14 days)",
        "I.R.C.P. 15(a)(3)",
    ),
    "summons-service": (
        182, "calendar",
        "Deadline to serve the summons and complaint after filing (182 days)",
        "I.R.C.P. 4(b)(2)",
    ),

    # Discovery (30-day response window; I.R.C.P. 33/34/36)
    "interrogatory-response": (
        30, "calendar",
        "Interrogatory response due (30 days); cap of 40 interrogatories",
        "I.R.C.P. 33(a)(1), 33(b)(2)",
    ),
    "rfp-response": (
        30, "calendar",
        "Request-for-production response due (30 days)",
        "I.R.C.P. 34(b)(2)",
    ),
    "rfa-response": (
        30, "calendar",
        "Request-for-admission response due (30 days); failure deems admitted",
        "I.R.C.P. 36(a)(3)",
    ),

    # Summary judgment (I.R.C.P. 56) — counted BACKWARD from the hearing
    "sj-motion-before-hearing": (
        -28, "calendar",
        "SJ motion + brief served at least 28 days before the hearing",
        "I.R.C.P. 56(b)",
    ),
    "sj-response-before-hearing": (
        -14, "calendar",
        "SJ answering brief served at least 14 days before the hearing",
        "I.R.C.P. 56(b)",
    ),

    # Motion practice (notice of hearing)
    "motion-notice": (
        14, "calendar",
        "Written motion + notice served at least 14 days before the hearing",
        "I.R.C.P. 7(b)(3)",
    ),

    # Post-judgment
    "new-trial-motion": (
        14, "calendar",
        "Motion for new trial / to alter or amend judgment (14 days)",
        "I.R.C.P. 59(b), 59(e)",
    ),
    "reconsideration": (
        14, "calendar",
        "Motion for reconsideration of a final judgment (14 days)",
        "I.R.C.P. 11.2(b)",
    ),
    "relief-judgment-outer": (
        180, "calendar",
        "Rule 60(b)(1)-(3) — outer 6-month deadline",
        "I.R.C.P. 60(c)(1)",
    ),
    "memorandum-costs": (
        14, "calendar",
        "Memorandum of costs after judgment (14 days)",
        "I.R.C.P. 54(d)",
    ),
    "appeal": (
        42, "calendar",
        "Notice of Appeal to the Idaho Supreme Court (42 days)",
        "I.A.R. 14(a)",
    ),

    # Statutes of limitation (defenses)
    "sol-written-contract": (
        1826, "calendar",  # 5 years (~365.25/yr)
        "SOL — written contract / instrument in writing (5 years)",
        "Idaho Code § 5-216",
    ),
    "sol-oral-contract": (
        1461, "calendar",  # 4 years
        "SOL — oral / unwritten contract (4 years)",
        "Idaho Code § 5-217",
    ),
    "sol-open-account": (
        1461, "calendar",  # 4 years (§ 5-217; accrual under § 5-222)
        "SOL — open account / account not in writing (4 years)",
        "Idaho Code § 5-217; accrual § 5-222",
    ),
    "sol-personal-injury": (
        730, "calendar",  # 2 years
        "SOL — personal injury (2 years)",
        "Idaho Code § 5-219",
    ),
    "sol-fraud-discovery": (
        1096, "calendar",  # 3 years
        "SOL — fraud (3 years from discovery)",
        "Idaho Code § 5-218(4)",
    ),
    "sol-judgment": (
        4018, "calendar",  # 11 years
        "SOL — action upon a judgment (11 years)",
        "Idaho Code § 5-215",
    ),

    # Consumer-protection / federal SOLs
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

    # FDCPA / Reg F validation window
    "fdcpa-validation-period": (
        30, "calendar",
        "Consumer's window to dispute the debt (FDCPA validation)",
        "15 U.S.C. § 1692g; 12 CFR § 1006.34",
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


def id_holidays(year: int) -> set:
    """Return set of Idaho legal holidays for a year (Idaho Code § 73-108)."""
    holidays = set()

    for m, d in FIXED_HOLIDAYS:
        date = datetime.date(year, m, d)
        # Observed-day shift per § 73-108
        if date.weekday() == 5:    # Saturday → preceding Friday
            date -= datetime.timedelta(days=1)
        elif date.weekday() == 6:  # Sunday → following Monday
            date += datetime.timedelta(days=1)
        holidays.add(date)

    for m, wd, n in WEEK_HOLIDAYS:
        holidays.add(_nth_weekday(year, m, wd, n))

    # § 73-108 does NOT include Juneteenth or the day after Thanksgiving
    # as Idaho state legal holidays.
    return holidays


def is_court_day(d: datetime.date) -> bool:
    """True if d is a court day (not a weekend or Idaho legal holiday)."""
    if d.weekday() >= 5:   # Saturday or Sunday
        return False
    if d in id_holidays(d.year):
        return False
    return True


def add_calendar_days(start: datetime.date, n: int) -> datetime.date:
    """Add calendar days. Apply the I.R.C.P. 2.2 end-of-period rule:
    exclude the first day, include the last; if the final day falls on a
    Saturday, Sunday, or legal holiday, roll to the next day that is
    not."""
    end = start + datetime.timedelta(days=n)
    if n != 0:
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
    print("Known rules (Idaho):")
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
        description="Compute Idaho court deadlines (I.R.C.P. 2.2 / Idaho Code § 73-108)"
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
