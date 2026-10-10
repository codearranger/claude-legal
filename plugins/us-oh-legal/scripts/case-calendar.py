#!/usr/bin/env python3
"""
case-calendar.py — Compute Ohio court deadlines.

Supports calendar-day and court-day counting with Ohio state
legal holidays (R.C. 1.14 + R.C. 1.45 time computation)
excluded for court-day mode.

Usage:
    case-calendar.py --from YYYY-MM-DD --days N --mode [calendar|court]
    case-calendar.py --from YYYY-MM-DD --rule RULE_KEY
    case-calendar.py --rules

Examples:
    # Answer due — 28 days from service (Civ. R. 12(A)(1))
    case-calendar.py --from 2025-04-15 --rule answer-due

    # SOL on written contract — 6 years (R.C. 2305.06)
    case-calendar.py --from 2019-04-15 --rule sol-written-contract

    # SOL on Ohio CSPA claim — 2 years (R.C. 1345.10)
    case-calendar.py --from 2023-04-15 --rule sol-cspa

    # List known rules
    case-calendar.py --rules
"""

from __future__ import annotations

import argparse
import datetime
import sys
from typing import Optional


# Ohio legal holidays under R.C. 1.14.
# R.C. 1.45: when a deadline falls on Saturday, Sunday, or
# a legal holiday, it rolls forward to the next business day.
FIXED_HOLIDAYS = [
    (1, 1),    # New Year's Day
    (6, 19),   # Juneteenth (added 2024)
    (7, 4),    # Independence Day
    (11, 11),  # Veterans Day
    (12, 25),  # Christmas Day
]

# Week-based holidays (n-th weekday of month).
# Ohio still observes Columbus Day under R.C. 1.14 (unlike
# CO's Frances Xavier Cabrini Day replacement).
WEEK_HOLIDAYS = [
    # (month, weekday[0=Mon], ordinal[1=first, -1=last])
    (1, 0, 3),   # MLK — 3rd Monday of January
    (2, 0, 3),   # Washington's Birthday — 3rd Monday of Feb
    (5, 0, -1),  # Memorial Day — last Monday of May
    (9, 0, 1),   # Labor Day — 1st Monday of September
    (10, 0, 2),  # Columbus Day — 2nd Monday of October
    (11, 3, 4),  # Thanksgiving — 4th Thursday of November
]


def _nth_weekday(year: int, month: int, weekday: int,
                  n: int) -> datetime.date:
    """Return the date of the n-th weekday of month/year.
    n=1 means first; n=-1 means last."""
    if n > 0:
        d = datetime.date(year, month, 1)
        offset = (weekday - d.weekday()) % 7
        return d + datetime.timedelta(
            days=offset + (n - 1) * 7
        )
    # n=-1: walk back from end of month
    next_month = month + 1
    next_year = year
    if next_month > 12:
        next_month = 1
        next_year += 1
    last = datetime.date(next_year, next_month, 1) - \
        datetime.timedelta(days=1)
    offset = (last.weekday() - weekday) % 7
    return last - datetime.timedelta(days=offset)


def get_holidays(year: int) -> set[datetime.date]:
    """Return the set of Ohio legal holidays for a year."""
    out: set[datetime.date] = set()
    for month, day in FIXED_HOLIDAYS:
        try:
            d = datetime.date(year, month, day)
        except ValueError:
            continue
        out.add(d)
        # R.C. 1.45 weekend roll: holiday on Saturday is
        # observed Friday; on Sunday observed Monday.
        if d.weekday() == 5:  # Saturday
            out.add(d - datetime.timedelta(days=1))
        elif d.weekday() == 6:  # Sunday
            out.add(d + datetime.timedelta(days=1))
    for month, weekday, ordinal in WEEK_HOLIDAYS:
        out.add(_nth_weekday(year, month, weekday, ordinal))
    return out


def is_court_day(d: datetime.date) -> bool:
    """True if d is a court day (not weekend or legal holiday)."""
    if d.weekday() >= 5:
        return False
    if d in get_holidays(d.year):
        return False
    return True


def roll_forward(d: datetime.date) -> datetime.date:
    """Roll forward to next court day if d is weekend/holiday
    (Ohio Civ. R. 6(A) + R.C. 1.45)."""
    while not is_court_day(d):
        d = d + datetime.timedelta(days=1)
    return d


def add_calendar_days(start: datetime.date,
                       n: int) -> datetime.date:
    """Add n calendar days; roll forward final day if it
    falls on weekend or legal holiday (Civ. R. 6(A))."""
    return roll_forward(start + datetime.timedelta(days=n))


def add_court_days(start: datetime.date,
                    n: int) -> datetime.date:
    """Add n court days (skipping weekends + Ohio legal
    holidays)."""
    d = start
    added = 0
    while added < n:
        d = d + datetime.timedelta(days=1)
        if is_court_day(d):
            added += 1
    return d


# Named-rule catalog. Each entry maps to:
#   (mode, days, description, authority)
RULES = {
    "answer-due": (
        "calendar", 28,
        "Answer to complaint (Civ. R. 12(A)(1))",
        "Ohio Civ. R. 12(A)(1)",
    ),
    "answer-reply-due": (
        "calendar", 28,
        "Reply to counterclaim / answer to cross-claim",
        "Ohio Civ. R. 12(A)(2)",
    ),
    "motion-response-civ": (
        "calendar", 14,
        "Response to motion (typical local-rule default; "
        "verify per-court)",
        "Ohio Civ. R. 6(C)(1) (where adopted by local rule)",
    ),
    "msj-notice": (
        "calendar", 14,
        "Summary judgment 14-day minimum notice",
        "Ohio Civ. R. 56(C)",
    ),
    "magistrate-objection": (
        "calendar", 14,
        "Written objection to magistrate's decision",
        "Ohio Civ. R. 53(D)(3)(b)(i)",
    ),
    "motion-to-correct-error": (
        "calendar", 28,
        "Motion to vacate / for new trial (Civ. R. 59 / 60)",
        "Ohio Civ. R. 59 / 60",
    ),
    "appeal-notice": (
        "calendar", 30,
        "Notice of appeal to court of appeals",
        "Ohio App. R. 4(A)",
    ),
    "sol-written-contract": (
        "calendar", 365 * 6,
        "SOL — written contract (6 years)",
        "R.C. 2305.06",
    ),
    "sol-oral-contract": (
        "calendar", 365 * 4,
        "SOL — oral / implied contract (4 years)",
        "R.C. 2305.07",
    ),
    "sol-conversion-fraud": (
        "calendar", 365 * 4,
        "SOL — conversion / fraud (4 years)",
        "R.C. 2305.09",
    ),
    "sol-personal-injury": (
        "calendar", 365 * 2,
        "SOL — personal injury (2 years)",
        "R.C. 2305.10",
    ),
    "sol-libel-slander": (
        "calendar", 365 * 1,
        "SOL — libel / slander (1 year)",
        "R.C. 2305.11",
    ),
    "sol-cspa": (
        "calendar", 365 * 2,
        "SOL — Ohio Consumer Sales Practices Act (2 years)",
        "R.C. 1345.10",
    ),
    "sol-judgment-enforcement": (
        "calendar", 365 * 5,
        "SOL — judgment enforcement (5 years; renewable)",
        "R.C. 2329.07",
    ),
    "fed-30day-notice": (
        "calendar", 3,
        "Forcible Entry and Detainer — 3-day notice to "
        "leave the premises",
        "R.C. 1923.04",
    ),
    "divorce-residency-state": (
        "calendar", 180,
        "Ohio divorce residency — 6 months in state before "
        "filing",
        "R.C. 3105.03",
    ),
    "divorce-residency-county": (
        "calendar", 90,
        "Ohio divorce residency — 90 days in county before "
        "filing",
        "R.C. 3105.03",
    ),
    "dissolution-waiting": (
        "calendar", 30,
        "Dissolution — 30-day minimum before hearing after "
        "filing petition",
        "R.C. 3105.64",
    ),
}


def list_rules() -> None:
    print("Ohio named-deadline rules:")
    for key, (mode, days, desc, authority) in sorted(RULES.items()):
        print(f"  {key:35s}  {days:>5} {mode:>8}  "
              f"{desc}  ({authority})")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--from", dest="start", type=str,
                    help="Start date YYYY-MM-DD")
    ap.add_argument("--days", type=int)
    ap.add_argument("--mode", choices=["calendar", "court"],
                    default="calendar")
    ap.add_argument("--rule", type=str,
                    help="Named-rule key (see --rules)")
    ap.add_argument("--rules", action="store_true",
                    help="List the named-rule catalog")
    args = ap.parse_args()

    if args.rules:
        list_rules()
        return 0

    if not args.start:
        print("--from is required", file=sys.stderr)
        return 2
    try:
        start = datetime.date.fromisoformat(args.start)
    except ValueError:
        print(f"Bad date: {args.start}", file=sys.stderr)
        return 2

    if args.rule:
        if args.rule not in RULES:
            print(f"Unknown rule: {args.rule}",
                  file=sys.stderr)
            print("  use --rules to list known rules")
            return 2
        mode, days, desc, authority = RULES[args.rule]
    else:
        if args.days is None:
            print("Either --rule or --days is required",
                  file=sys.stderr)
            return 2
        mode, days = args.mode, args.days
        desc = f"{days} {mode}-day period"
        authority = "(user-supplied)"

    if mode == "calendar":
        result = add_calendar_days(start, days)
    else:
        result = add_court_days(start, days)

    print(f"From {start} + {days} {mode} days = {result}")
    print(f"  Rule:     {desc}")
    print(f"  Authority: {authority}")
    print(f"  Result is a {result.strftime('%A')}")
    if not is_court_day(result):
        print("  (NOTE: result is NOT a court day; "
              "consider rolling)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
