#!/usr/bin/env python3
"""
case-calendar.py — Compute Colorado court deadlines.

Supports calendar-day and court-day counting with Colorado legal
holidays (C.R.S. § 24-11-101) excluded for court-day mode and the
C.R.C.P. 6(a) rolling-forward rule applied when a deadline falls on
a Saturday, Sunday, or legal holiday.

Usage:
    case-calendar.py --from YYYY-MM-DD --days N --mode [calendar|court]
    case-calendar.py --from YYYY-MM-DD --rule RULE_KEY
    case-calendar.py --rules

Examples:
    # Answer due — 21 days from service 2025-01-15 (C.R.C.P. 12(a))
    case-calendar.py --from 2025-01-15 --rule answer-due

    # Reply to a C.R.C.P. 121 § 1-15 motion — 7 days after response
    case-calendar.py --from 2025-04-30 --days 7 --mode calendar

    # Motion-to-compel filed before SJ hearing
    case-calendar.py --from 2025-09-15 --days -91 --mode calendar

    # List known rules
    case-calendar.py --rules
"""

import argparse
import datetime
import sys
from typing import Optional


# Colorado legal holidays (C.R.S. § 24-11-101).
# Holidays falling on Saturday are observed on the preceding Friday;
# Sunday holidays are observed on the following Monday.
FIXED_HOLIDAYS = [
    (1, 1),   # New Year's Day
    (6, 19),  # Juneteenth (Colorado added in 2022; federal in 2021)
    (7, 4),   # Independence Day
    (11, 11), # Veterans Day
    (12, 25), # Christmas Day
]

# Week-based holidays (n-th weekday of month).
# (month, weekday [0=Mon], ordinal [1=first, -1=last])
WEEK_HOLIDAYS = [
    (1, 0, 3),   # MLK Day — 3rd Monday of January
    (2, 0, 3),   # Presidents' Day — 3rd Monday of February
    (5, 0, -1),  # Memorial Day — last Monday of May
    (9, 0, 1),   # Labor Day — 1st Monday of September
    (10, 0, 1),  # Frances Xavier Cabrini Day — 1st Monday of October
                 # (replaced Columbus Day per H.B. 20-1031, effective 2020)
    (11, 3, 4),  # Thanksgiving — 4th Thursday of November
]

# Note: Colorado does NOT observe the day after Thanksgiving as a state
# legal holiday (contrast Washington, which does). Some judicial
# districts administratively close on certain days but the
# C.R.S. § 24-11-101 list above controls deadline arithmetic under
# C.R.C.P. 6(a).


# Named rules: (days, mode, description, authority)
RULES = {
    # Answer / response window
    "answer-due": (
        21, "calendar",
        "Answer due (Colorado resident, in-state service)",
        "C.R.C.P. 12(a)(1)",
    ),
    "answer-due-out-of-state": (
        35, "calendar",
        "Answer due (out-of-state defendant, personally served)",
        "C.R.C.P. 12(a)(2)",
    ),
    "reply-counterclaim": (
        21, "calendar",
        "Reply to counterclaim", "C.R.C.P. 12(a)(3)",
    ),
    "response-to-amended": (
        14, "calendar",
        "Response to amended pleading", "C.R.C.P. 15(a)",
    ),
    # Discovery
    "discovery-response": (
        30, "calendar",
        "Response to interrogatories / RFP / RFA",
        "C.R.C.P. 33(a)(3); 34(b)(2); 36(a)",
    ),
    "rfa-deemed-admitted": (
        35, "calendar",
        "RFA — silence = admission (30 + 5 mail days if mailed)",
        "C.R.C.P. 36(a); 6(e)",
    ),
    "case-management-conference": (
        49, "calendar",
        "Initial case management conference (default)",
        "C.R.C.P. 16(b)",
    ),
    "proposed-case-mgmt-order": (
        7, "calendar",
        "Proposed Case Management Order (filed at least 7 days before CMC)",
        "C.R.C.P. 16(b)(2)",
    ),
    "rule-26-disclosures": (
        28, "calendar",
        "Rule 26(a)(1) initial disclosures (28 days after case at issue)",
        "C.R.C.P. 26(a)(1)",
    ),
    # Motion practice (C.R.C.P. 121 § 1-15)
    "121-response": (
        21, "calendar",
        "Response to motion under C.R.C.P. 121 § 1-15(1)(b)",
        "C.R.C.P. 121 § 1-15(1)(b)",
    ),
    "121-reply": (
        7, "calendar",
        "Reply on motion under C.R.C.P. 121 § 1-15(1)(d)",
        "C.R.C.P. 121 § 1-15(1)(d)",
    ),
    "summary-judgment-motion": (
        -91, "calendar",
        "Summary judgment motion filed before trial (91 days)",
        "C.R.C.P. 56(c)",
    ),
    # Post-judgment / appeals
    "motion-reconsideration": (
        14, "calendar",
        "C.R.C.P. 59 motion for new trial or amend findings",
        "C.R.C.P. 59(a)",
    ),
    "rule-60-b-1-3": (
        182, "calendar",
        "C.R.C.P. 60(b)(1)-(3) outer deadline (~6 months)",
        "C.R.C.P. 60(b)",
    ),
    "notice-of-appeal": (
        49, "calendar",
        "Notice of Appeal to Colorado Court of Appeals",
        "C.A.R. 4(a)",
    ),
    "satisfaction-of-judgment": (
        21, "calendar",
        "Creditor must file satisfaction after demand",
        "C.R.S. § 13-52-110",
    ),
    "garnishment-answer": (
        7, "calendar",
        "Garnishee's answer to writ of continuing garnishment",
        "C.R.S. § 13-54.5-106(2)",
    ),
    "exemption-claim": (
        14, "calendar",
        "Judgment debtor's written objection to garnishment",
        "C.R.S. § 13-54.5-108",
    ),
    # FDCPA / Reg F
    "fdcpa-validation": (
        30, "calendar",
        "Consumer's window to dispute debt after § 1692g notice",
        "15 U.S.C. § 1692g(a)(3)",
    ),
    "fdcpa-sol": (
        365, "calendar",
        "FDCPA private civil action statute of limitations",
        "15 U.S.C. § 1692k(d)",
    ),
    # Colorado SOLs (consumer debt — see references for case authority)
    "sol-contract": (
        2191, "calendar",  # ~6 years
        "SOL — liquidated debt / written instrument (6 years)",
        "C.R.S. § 13-80-103.5(1)(a)",
    ),
    "sol-tort": (
        730, "calendar",  # 2 years
        "SOL — tort and most general civil claims (2 years)",
        "C.R.S. § 13-80-102",
    ),
    "sol-ccpa": (
        1096, "calendar",  # 3 years
        "SOL — Colorado Consumer Protection Act (3 years)",
        "C.R.S. § 6-1-115",
    ),
    "sol-cfdcpa": (
        365, "calendar",
        "SOL — Colorado Fair Debt Collection Practices Act (1 year)",
        "C.R.S. § 5-16-113(4)",
    ),
    # Family law (Title 14)
    "udma-waiting-period": (
        91, "calendar",
        "UDMA mandatory 91-day waiting period before decree",
        "C.R.S. § 14-10-106(1)(a)(III)",
    ),
    "udma-residency": (
        91, "calendar",
        "UDMA jurisdictional residency before filing",
        "C.R.S. § 14-10-106(1)(a)(I)",
    ),
    "16-2-sfs": (
        42, "calendar",
        "Sworn Financial Statement due (42 days after case filed)",
        "C.R.C.P. 16.2(e)(2)",
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


def co_holidays(year: int) -> set:
    """Return set of Colorado state legal holidays for a year
    (C.R.S. § 24-11-101)."""
    holidays = set()

    for m, d in FIXED_HOLIDAYS:
        date = datetime.date(year, m, d)
        # Observed-day shift (C.R.S. § 24-11-101(2))
        if date.weekday() == 5:   # Saturday → preceding Friday
            date -= datetime.timedelta(days=1)
        elif date.weekday() == 6:  # Sunday → following Monday
            date += datetime.timedelta(days=1)
        holidays.add(date)

    for m, wd, n in WEEK_HOLIDAYS:
        holidays.add(_nth_weekday(year, m, wd, n))

    return holidays


def is_court_day(d: datetime.date) -> bool:
    """True if d is a court day (not a weekend or CO legal holiday)."""
    if d.weekday() >= 5:   # Saturday or Sunday
        return False
    if d in co_holidays(d.year):
        return False
    return True


def roll_forward_rule(d: datetime.date) -> datetime.date:
    """C.R.C.P. 6(a)(1)(C): When the last day of the period falls on
    a Saturday, Sunday, or legal holiday, the period extends to the
    end of the next day that is not one of those days."""
    while not is_court_day(d):
        d += datetime.timedelta(days=1)
    return d


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
        raw = add_calendar_days(start, days)
        # C.R.C.P. 6(a)(1)(C) roll-forward applies to forward counts
        if days >= 0:
            return roll_forward_rule(raw)
        return raw
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
    print("Known rules (Colorado):")
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
        description="Compute Colorado court deadlines (C.R.C.P. 6 + C.R.S. § 24-11-101)"
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
