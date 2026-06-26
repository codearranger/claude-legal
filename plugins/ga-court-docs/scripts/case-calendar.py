# TODO: Adapt this script for Georgia.
# Update format-rule references, holidays, and named rules for Georgia.

#!/usr/bin/env python3
"""
case-calendar.py — Compute Oregon court deadlines.

Supports calendar-day and court-day counting with Oregon state
holidays (ORS 187.010) excluded for court-day mode.

Usage:
    case-calendar.py --from YYYY-MM-DD --days N --mode [calendar|court] \
                     [--jurisdiction oregon|federal]
    case-calendar.py --from YYYY-MM-DD --rule RULE_KEY
    case-calendar.py --rules

Examples:
    # Answer due — 30 calendar days from service 2025-04-15
    case-calendar.py --from 2025-04-15 --days 30 --mode calendar

    # SOL on contract — 6 years from last activity 2019-03-15
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


# Oregon legal holidays (ORS 187.010)
# Holidays falling on Saturday are observed on Friday; Sunday -> Monday
# (ORS 187.020).
#
# NOTE: Oregon does NOT recognize the Friday after Thanksgiving as a
# statewide legal holiday (Washington does).
FIXED_HOLIDAYS = [
    (1, 1),    # New Year's Day
    (6, 19),   # Juneteenth
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
    (11, 3, 4),  # Thanksgiving — 4th Thursday of November
]


# Named rules: (days, mode, description, authority)
RULES = {
    # Initial response
    "answer-due": (
        30, "calendar",
        "Answer due after personal service in Oregon",
        "ORCP 7 C(2)",
    ),
    "answer-due-mail": (
        33, "calendar",
        "Answer due after service by mail (+3 mail days)",
        "ORCP 7 C(2), 10 C",
    ),
    "return-of-service": (
        63, "calendar",
        "Return of Service must be filed within 63 days of service",
        "ORCP 7 D(3)",
    ),
    "response-amended": (
        14, "calendar",
        "Response to amended complaint",
        "ORCP 23 A (typical)",
    ),

    # Discovery
    "rfp-response": (
        30, "calendar",
        "RFP response due (ORCP 43 B)",
        "ORCP 43 B",
    ),
    "rfp-response-with-summons": (
        45, "calendar",
        "RFP response due (served with summons; ORCP 43 B)",
        "ORCP 43 B",
    ),
    "rfa-response": (
        30, "calendar",
        "RFA response due (ORCP 45 B); failure deems admitted",
        "ORCP 45 B",
    ),
    "rfa-response-with-summons": (
        45, "calendar",
        "RFA response due (served with summons; ORCP 45 B)",
        "ORCP 45 B",
    ),
    "deposition-notice-party": (
        5, "calendar",
        "Deposition notice — party (5 days)",
        "ORCP 39 B",
    ),
    "deposition-notice-nonparty": (
        7, "calendar",
        "Deposition notice — non-party (7 days; subpoena required)",
        "ORCP 39 B, 55",
    ),

    # Summary judgment (ORCP 47 C)
    "sj-motion": (
        -60, "calendar",
        "SJ motion filed before trial (at least 60 days before)",
        "ORCP 47 C",
    ),
    "sj-response": (
        20, "calendar",
        "SJ response due (20 days after service)",
        "ORCP 47 C",
    ),
    "sj-reply": (
        5, "calendar",
        "SJ reply due (5 days after service of response)",
        "ORCP 47 C",
    ),
    "sj-hearing": (
        11, "calendar",
        "SJ hearing must be at least 11 days after reply filing",
        "ORCP 47 C",
    ),

    # Motion practice
    "response-motion-typical": (
        14, "calendar",
        "Motion response (typical Oregon local SLR)",
        "Local SLR; ORCP 36, 46",
    ),
    "reply-motion-typical": (
        7, "calendar",
        "Motion reply (typical Oregon local SLR)",
        "Local SLR",
    ),

    # Post-judgment
    "vacation-cap": (
        365, "calendar",
        "ORCP 71 B(1)-(3) — outer 1-year deadline",
        "ORCP 71 B",
    ),
    "appeal-circuit": (
        30, "calendar",
        "Notice of Appeal — circuit to Court of Appeals",
        "ORS 19.255, ORAP 5.30",
    ),
    "amend-judgment": (
        10, "calendar",
        "Motion to amend judgment",
        "ORCP 64",
    ),
    "garnishment-challenge": (
        30, "calendar",
        "Challenge to Writ of Garnishment — exemption claim",
        "ORS 18.700+",
    ),
    "judgment-life": (
        3653, "calendar",  # 10 years (approx; 3652 + 1 leap)
        "Judgment lifespan (10 years, renewable)",
        "ORS 18.182",
    ),
    "fee-statement-orcp-68": (
        14, "calendar",
        "Statement of Attorney Fees and Costs (ORCP 68 C(2))",
        "ORCP 68 C(2)",
    ),
    "cost-bill": (
        14, "calendar",
        "Cost bill under ORCP 68",
        "ORCP 68 C",
    ),

    # Arbitration
    "arbitration-trial-de-novo": (
        20, "calendar",
        "Trial de novo request from arbitration award",
        "ORS 36.425",
    ),

    # Statutes of limitation (defenses)
    "sol-written-contract": (
        2191, "calendar",  # 6 years (approx; account for leap years as ~365.25)
        "SOL — written contract (6 years)",
        "ORS 12.080(1)",
    ),
    "sol-open-account": (
        2191, "calendar",
        "SOL — open account (6 years)",
        "ORS 12.080(2)-(4)",
    ),
    "sol-statutory-liability": (
        2191, "calendar",
        "SOL — statutory liability (6 years; UTPA repose; ORS 697)",
        "ORS 12.080(2)",
    ),
    "sol-tort-personal-injury": (
        730, "calendar",  # 2 years
        "SOL — personal injury (2 years)",
        "ORS 12.110",
    ),
    "sol-fraud-discovery": (
        730, "calendar",
        "SOL — fraud (2 years from discovery; 10-year repose)",
        "ORS 12.110(1)",
    ),
    "sol-real-property": (
        3653, "calendar",
        "SOL — real property (10 years)",
        "ORS 12.040",
    ),

    # Consumer-protection SOLs
    "sol-utpa-discovery": (
        365, "calendar",
        "SOL — UTPA from discovery (1 year; 6-year repose)",
        "ORS 646.638(6)",
    ),
    "sol-utpa-repose": (
        2191, "calendar",
        "SOL — UTPA outer repose (6 years from violation)",
        "ORS 646.638(6)",
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


def or_holidays(year: int) -> set:
    """Return set of Oregon state legal holidays for a year (ORS 187.010)."""
    holidays = set()

    for m, d in FIXED_HOLIDAYS:
        date = datetime.date(year, m, d)
        # Observed-day shift per ORS 187.020
        if date.weekday() == 5:   # Saturday → Friday
            date -= datetime.timedelta(days=1)
        elif date.weekday() == 6:  # Sunday → Monday
            date += datetime.timedelta(days=1)
        holidays.add(date)

    for m, wd, n in WEEK_HOLIDAYS:
        holidays.add(_nth_weekday(year, m, wd, n))

    # Oregon does NOT recognize the day after Thanksgiving as a
    # statewide legal holiday (unlike Washington's Native American
    # Heritage Day under RCW 1.16.050).
    return holidays


def is_court_day(d: datetime.date) -> bool:
    """True if d is a court day (not a weekend or Oregon legal holiday)."""
    if d.weekday() >= 5:   # Saturday or Sunday
        return False
    if d in or_holidays(d.year):
        return False
    return True


def add_calendar_days(start: datetime.date, n: int) -> datetime.date:
    """Add calendar days. Apply ORCP 10 A end-of-period rule:
    if the final day falls on weekend or holiday, extend to next business
    day."""
    end = start + datetime.timedelta(days=n)
    if n != 0:
        # ORCP 10 A: if last day is weekend or holiday, extend to next
        # business day (only for forward computation).
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
        description="Compute Oregon court deadlines"
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
