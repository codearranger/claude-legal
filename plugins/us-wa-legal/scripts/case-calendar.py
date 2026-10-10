#!/usr/bin/env python3
"""
case-calendar.py — Compute Washington court deadlines.

Supports calendar-day and court-day counting with Washington state
holidays excluded for court-day mode.

Usage:
    case-calendar.py --from YYYY-MM-DD --days N --mode [calendar|court] \
                     [--jurisdiction washington|federal]
    case-calendar.py --from YYYY-MM-DD --rule RULE_KEY
    case-calendar.py --rules

Examples:
    # Answer due — 20 calendar days from service 2025-01-15
    case-calendar.py --from 2025-01-15 --days 20 --mode calendar

    # Reply due — 5 court days before hearing
    case-calendar.py --from 2025-04-30 --days -5 --mode court

    # Apply a named rule
    case-calendar.py --from 2025-01-15 --rule answer-due

    # List known rules
    case-calendar.py --rules
"""

import argparse
import datetime
import sys
from typing import Optional


# Washington legal holidays (RCW 1.16.050)
# Holidays falling on Saturday are observed on Friday; Sunday -> Monday.
FIXED_HOLIDAYS = [
    (1, 1),   # New Year's Day
    (7, 4),   # Independence Day
    (11, 11), # Veterans Day
    (12, 25), # Christmas Day
    (6, 19),  # Juneteenth
]

# Week-based holidays (n-th weekday of month)
WEEK_HOLIDAYS = [
    # (month, weekday [0=Mon], ordinal [1=first, -1=last])
    (1, 0, 3),   # MLK — 3rd Monday of January
    (2, 0, 3),   # Presidents' Day — 3rd Monday of February
    (5, 0, -1),  # Memorial Day — last Monday of May
    (9, 0, 1),   # Labor Day — 1st Monday of September
    (11, 3, 4),  # Thanksgiving — 4th Thursday of November
    # Native American Heritage Day — day after Thanksgiving —
    # is a WA state legal holiday per RCW 1.16.050. It is Thanksgiving + 1
    # and is added dynamically in wa_holidays() below rather than here
    # because the "day after" isn't a weekday ordinal.
]


# Named rules: (days, mode, description, authority)
RULES = {
    "answer-due": (
        20, "calendar",
        "Answer due (WA resident)", "CR 12(a)(1)"
    ),
    "answer-due-nonresident": (
        60, "calendar",
        "Answer due (non-resident)", "CR 12(a)(1)"
    ),
    "reply-counterclaim": (
        20, "calendar",
        "Reply to counterclaim", "CR 12(a)(3)"
    ),
    "response-to-amended": (
        14, "calendar",
        "Response to amended complaint", "CR 15(a)"
    ),
    "discovery-response": (
        30, "calendar",
        "Discovery response", "CR 33/34/36"
    ),
    "discovery-response-mailed": (
        33, "calendar",
        "Discovery response + 3 mail days", "CR 6(e)"
    ),
    "rfa-deemed-admitted": (
        30, "calendar",
        "RFA — silence = admission", "CR 36(a)"
    ),
    "motion-reconsideration": (
        10, "calendar",
        "Motion for reconsideration", "CR 59(b)"
    ),
    "cr60-b1-3": (
        365, "calendar",
        "CR 60(b)(1)-(3) outer deadline", "CR 60(b)"
    ),
    "appeal-superior": (
        30, "calendar",
        "Notice of Appeal to Court of Appeals", "RAP 5.2"
    ),
    "appeal-district": (
        30, "calendar",
        "Notice of Appeal under RALJ", "RALJ 2.5"
    ),
    "garnishee-answer": (
        20, "calendar",
        "Garnishee's answer", "RCW 6.27.190"
    ),
    "exemption-claim": (
        21, "calendar",
        "Exemption Claim Form (mailing rule)", "RCW 6.27"
    ),
    "fdcpa-dispute": (
        30, "calendar",
        "Consumer's window to dispute debt", "15 U.S.C. § 1692g"
    ),
    "fdcpa-sol": (
        365, "calendar",
        "FDCPA civil statute of limitations", "15 U.S.C. § 1692k(d)"
    ),
    "satisfaction-of-judgment": (
        60, "calendar",
        "Creditor must file satisfaction", "RCW 4.56.100"
    ),
    "sj-filed-before-hearing": (
        -28, "calendar",
        "Summary judgment motion filed before hearing", "CR 56(c)"
    ),
    "response-motion-superior": (
        -11, "court",
        "Response to motion (superior court)", "CR 6(d)"
    ),
    "reply-motion-superior": (
        -5, "court",
        "Reply on motion (superior court)", "CR 6(d)"
    ),
    "response-motion-district": (
        -3, "court",
        "Response to motion (district court)", "CRLJ 6(d)"
    ),
    "note-for-motion": (
        -9, "court",
        "Note for motion docket (minimum lead time)", "CR 6(d)"
    ),
    "sol-written-contract": (
        2191, "calendar",   # 6 years (rough; leap years may vary)
        "SOL — written contract (6 years)", "RCW 4.16.040"
    ),
    "sol-oral-contract": (
        1096, "calendar",   # 3 years
        "SOL — oral contract (3 years)", "RCW 4.16.080(3)"
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


def wa_holidays(year: int) -> set:
    """Return set of Washington state legal holidays for a year."""
    holidays = set()

    for m, d in FIXED_HOLIDAYS:
        date = datetime.date(year, m, d)
        # Observed-day shift
        if date.weekday() == 5:   # Saturday → Friday
            date -= datetime.timedelta(days=1)
        elif date.weekday() == 6:  # Sunday → Monday
            date += datetime.timedelta(days=1)
        holidays.add(date)

    for m, wd, n in WEEK_HOLIDAYS:
        holidays.add(_nth_weekday(year, m, wd, n))

    # Native American Heritage Day — Friday after Thanksgiving
    # (RCW 1.16.050). Add it as Thanksgiving + 1 day.
    thanksgiving = _nth_weekday(year, 11, 3, 4)
    holidays.add(thanksgiving + datetime.timedelta(days=1))

    return holidays


def is_court_day(d: datetime.date) -> bool:
    """True if d is a court day (not a weekend or WA holiday)."""
    if d.weekday() >= 5:   # Saturday or Sunday
        return False
    if d in wa_holidays(d.year):
        return False
    return True


def add_calendar_days(start: datetime.date, n: int) -> datetime.date:
    return start + datetime.timedelta(days=n)


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
        description="Compute Washington court deadlines"
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
