#!/usr/bin/env python3
"""
case-calendar.py — Compute Arkansas court deadlines.

Supports calendar-day and court-day counting with Arkansas state
holidays (Ark. Code Ann. § 1-5-101) excluded for court-day mode and
for the end-of-period roll under Ark. R. Civ. P. 6(a).

Usage:
    case-calendar.py --from YYYY-MM-DD --days N --mode [calendar|court]
    case-calendar.py --from YYYY-MM-DD --rule RULE_KEY
    case-calendar.py --rules

Examples:
    # Answer due — 30 calendar days from service 2025-04-15
    case-calendar.py --from 2025-04-15 --days 30 --mode calendar

    # SOL on written contract — 5 years from last activity 2019-03-15
    case-calendar.py --from 2019-03-15 --rule sol-written-contract

    # Apply a named rule
    case-calendar.py --from 2025-04-15 --rule answer-due

    # List known rules
    case-calendar.py --rules

NOT LEGAL ADVICE. This is a date-arithmetic aid. Verify every
deadline against the current Arkansas Rules of Civil Procedure, the
controlling statute, and the filing court's local rules. Ark. R.
Civ. P. 6(a) excludes the day of the triggering event and includes
the last day unless it is a Saturday, Sunday, or legal holiday, in
which case the period runs to the next day that is not one of those.
Ark. R. Civ. P. 6(d) adds 3 days when a party must act after service
of a paper made by mail.
"""

import argparse
import datetime
import sys
from typing import Optional


# Arkansas legal holidays (Ark. Code Ann. § 1-5-101).
# A holiday falling on Saturday is observed on the preceding Friday;
# a holiday falling on Sunday is observed on the succeeding Monday.
#
# Arkansas distinctives encoded below:
#   - Christmas Eve (Dec 24) is a state holiday.
#   - The third Monday in February is "George Washington's Birthday
#     and Daisy Gatson Bates Day."
# Arkansas does NOT observe Columbus Day, Juneteenth, or the day after
# Thanksgiving as § 1-5-101 holidays for these purposes, and Good
# Friday is not a state holiday. The "employee's birthday" floating
# holiday under § 1-5-101 is a personal day, not a court closure, and
# is intentionally NOT encoded here.
FIXED_HOLIDAYS = [
    (1, 1),    # New Year's Day
    (7, 4),    # Independence Day
    (11, 11),  # Veterans Day
    (12, 24),  # Christmas Eve
    (12, 25),  # Christmas Day
]

# Week-based holidays (n-th weekday of month)
WEEK_HOLIDAYS = [
    # (month, weekday [0=Mon], ordinal [1=first, -1=last])
    (1, 0, 3),   # Dr. Martin Luther King Jr.'s Birthday — 3rd Monday of January
    (2, 0, 3),   # Washington's Birthday & Daisy Gatson Bates Day — 3rd Monday of February
    (5, 0, -1),  # Memorial Day — last Monday of May
    (9, 0, 1),   # Labor Day — 1st Monday of September
    (11, 3, 4),  # Thanksgiving — 4th Thursday of November
]


# Named rules: (days, mode, description, authority)
# Day counts that may drift are documented here; verify against the
# current rule/statute text in the ar-law-references corpus.
RULES = {
    # Initial response
    "answer-due": (
        30, "calendar",
        "Answer due after service of summons and complaint",
        "Ark. R. Civ. P. 12(a)",
    ),
    "service-period": (
        120, "calendar",
        "Summons must be served within 120 days of filing the complaint",
        "Ark. R. Civ. P. 4(i)",
    ),
    "response-amended": (
        10, "calendar",
        "Response to an amended pleading (10 days, or remaining time if longer)",
        "Ark. R. Civ. P. 15(a)",
    ),

    # Discovery (Ark. R. Civ. P. 26-37)
    "interrogatory-response": (
        30, "calendar",
        "Answers/objections to interrogatories due",
        "Ark. R. Civ. P. 33(b)",
    ),
    "rfp-response": (
        30, "calendar",
        "Response to requests for production due",
        "Ark. R. Civ. P. 34(b)",
    ),
    "rfa-response": (
        30, "calendar",
        "Response to requests for admission due; unanswered matters deemed admitted",
        "Ark. R. Civ. P. 36(a)",
    ),
    "discovery-response-with-summons": (
        45, "calendar",
        "Discovery served with the summons/complaint: defendant's response not due before 45 days after service",
        "Ark. R. Civ. P. 33(b), 34(b), 36(a)",
    ),

    # Summary judgment (Ark. R. Civ. P. 56)
    "sj-response": (
        21, "calendar",
        "Response to a motion for summary judgment (21 days after service)",
        "Ark. R. Civ. P. 56(c)",
    ),

    # Post-judgment
    "new-trial-motion": (
        10, "calendar",
        "Motion for new trial / to amend judgment (not later than 10 days after entry)",
        "Ark. R. Civ. P. 59(b)",
    ),
    "rule-60a-window": (
        90, "calendar",
        "Rule 60(a) window: court may modify or vacate to correct error within 90 days of filing the judgment",
        "Ark. R. Civ. P. 60(a)",
    ),
    "notice-of-appeal": (
        30, "calendar",
        "Notice of appeal from circuit court to the appellate courts",
        "Ark. R. App. P.-Civ. 4(a)",
    ),
    "district-court-appeal": (
        30, "calendar",
        "Appeal from District Court to Circuit Court (de novo) by filing the record",
        "Ark. Dist. Ct. R. 9",
    ),
    "judgment-life": (
        3653, "calendar",  # ~10 years
        "Judgment lifespan (10 years; revivable by scire facias)",
        "Ark. Code Ann. § 16-65-501; § 16-56-114",
    ),

    # Statutes of limitation (defenses)
    "sol-written-contract": (
        1826, "calendar",  # ~5 years
        "SOL — written contract (5 years)",
        "Ark. Code Ann. § 16-56-111",
    ),
    "sol-oral-open-account": (
        1096, "calendar",  # ~3 years
        "SOL — oral contract / open account (3 years)",
        "Ark. Code Ann. § 16-56-105",
    ),
    "sol-tort": (
        1096, "calendar",  # ~3 years
        "SOL — personal injury / general tort (3 years)",
        "Ark. Code Ann. § 16-56-105",
    ),
    "sol-property-damage": (
        1096, "calendar",
        "SOL — injury to property (3 years)",
        "Ark. Code Ann. § 16-56-105",
    ),
    "sol-fraud-discovery": (
        1096, "calendar",
        "SOL — fraud (3 years; discovery rule may toll accrual)",
        "Ark. Code Ann. § 16-56-105",
    ),
    "sol-medical-malpractice": (
        730, "calendar",  # 2 years
        "SOL — medical malpractice (2 years)",
        "Ark. Code Ann. § 16-114-203",
    ),
    "sol-wrongful-death": (
        1096, "calendar",
        "SOL — wrongful death (3 years)",
        "Ark. Code Ann. § 16-62-102",
    ),
    "sol-acra": (
        365, "calendar",
        "SOL — Arkansas Civil Rights Act employment claim (1 year)",
        "Ark. Code Ann. § 16-123-107(c)",
    ),

    # Consumer-protection SOLs (federal overlay)
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
    "fdcpa-validation-period": (
        30, "calendar",
        "Consumer's window to dispute debt (FDCPA validation)",
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
        # Last weekday
        if month == 12:
            next_month_first = datetime.date(year + 1, 1, 1)
        else:
            next_month_first = datetime.date(year, month + 1, 1)
        last_day = next_month_first - datetime.timedelta(days=1)
        offset = (last_day.weekday() - weekday) % 7
        return last_day - datetime.timedelta(days=offset)


def ar_holidays(year: int) -> set:
    """Return set of Arkansas state legal holidays for a year
    (Ark. Code Ann. § 1-5-101), with observed-day shifts."""
    holidays = set()

    for m, d in FIXED_HOLIDAYS:
        date = datetime.date(year, m, d)
        # Observed-day shift: Saturday -> preceding Friday;
        # Sunday -> succeeding Monday.
        if date.weekday() == 5:    # Saturday → Friday
            date -= datetime.timedelta(days=1)
        elif date.weekday() == 6:  # Sunday → Monday
            date += datetime.timedelta(days=1)
        holidays.add(date)

    for m, wd, n in WEEK_HOLIDAYS:
        holidays.add(_nth_weekday(year, m, wd, n))

    return holidays


def is_court_day(d: datetime.date) -> bool:
    """True if d is a court day (not a weekend or Arkansas legal holiday)."""
    if d.weekday() >= 5:   # Saturday or Sunday
        return False
    if d in ar_holidays(d.year):
        return False
    return True


def add_calendar_days(start: datetime.date, n: int) -> datetime.date:
    """Add calendar days, then apply the Ark. R. Civ. P. 6(a)
    end-of-period rule: if the last day is a Saturday, Sunday, or legal
    holiday, the period runs to the next day that is none of those."""
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
    print("Known Arkansas rules:")
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
        description="Compute Arkansas court deadlines (Ark. R. Civ. P. 6; § 1-5-101 holidays)"
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
