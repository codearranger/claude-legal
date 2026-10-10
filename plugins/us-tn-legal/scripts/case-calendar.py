#!/usr/bin/env python3
"""
case-calendar.py — Compute Tennessee court deadlines.

Supports calendar-day and court-day counting with Tennessee legal
holidays (T.C.A. § 15-1-101) excluded for court-day mode and the
Tenn. R. Civ. P. 6.01 rolling-forward rule applied when a deadline
falls on a Saturday, Sunday, or legal holiday.

Tennessee distinctives encoded here:
  - Good Friday IS a Tennessee legal holiday (a MOVABLE feast — the
    Friday before Easter, computed via the Gregorian computus).
  - Columbus Day (2nd Monday in October) IS a Tennessee legal holiday.
  - Juneteenth (June 19) is in the statutory list.
  - The day after Thanksgiving is NOT a § 15-1-101 holiday (it is only
    an administrative state-employee holiday) and is therefore not
    excluded from deadline arithmetic.
  - Substitution (§ 15-1-101): a holiday on Sunday is observed the
    following Monday; on Saturday, the preceding Friday.

Usage:
    case-calendar.py --from YYYY-MM-DD --days N --mode [calendar|court]
    case-calendar.py --from YYYY-MM-DD --rule RULE_KEY
    case-calendar.py --rules

Examples:
    # Answer due — 30 days from service 2025-01-15 (Tenn. R. Civ. P. 12.01)
    case-calendar.py --from 2025-01-15 --rule answer-due

    # Summary-judgment motion must be served >= 30 days before hearing
    case-calendar.py --from 2025-09-15 --days -30 --mode calendar

    # List known rules
    case-calendar.py --rules
"""

import argparse
import datetime
import sys
from typing import Optional


# Tennessee legal holidays with FIXED calendar dates (T.C.A. § 15-1-101).
# Holidays falling on Saturday are observed the preceding Friday;
# Sunday holidays are observed the following Monday.
FIXED_HOLIDAYS = [
    (1, 1),    # New Year's Day
    (6, 19),   # Juneteenth (in the § 15-1-101 list)
    (7, 4),    # Independence Day
    (11, 11),  # Veterans' Day
    (12, 25),  # Christmas Day
]

# Week-based holidays (n-th weekday of month).
# (month, weekday [0=Mon], ordinal [1=first, -1=last])
WEEK_HOLIDAYS = [
    (1, 0, 3),   # Martin Luther King, Jr. Day — 3rd Monday of January
    (2, 0, 3),   # Washington Day (Presidents' Day) — 3rd Monday of February
    (5, 0, -1),  # Memorial / Decoration Day — last Monday of May
    (9, 0, 1),   # Labor Day — 1st Monday of September
    (10, 0, 2),  # Columbus Day — 2nd Monday of October (TN observes it)
    (11, 3, 4),  # Thanksgiving Day — 4th Thursday of November
]

# NOTE: Tennessee does NOT list the day after Thanksgiving in
# § 15-1-101. It is an administrative state-employee holiday only and
# is therefore not excluded from Rule 6.01 deadline arithmetic here.


# Named rules: (days, mode, description, authority)
RULES = {
    # Answer / response window
    "answer-due": (
        30, "calendar",
        "Answer due (30 days after service of summons and complaint)",
        "Tenn. R. Civ. P. 12.01",
    ),
    "answer-after-rule12-denial": (
        15, "calendar",
        "Responsive pleading after notice of denial of a Rule 12 motion",
        "Tenn. R. Civ. P. 12.01",
    ),
    "reply-counterclaim": (
        30, "calendar",
        "Reply to a counterclaim / answer to a cross-claim",
        "Tenn. R. Civ. P. 12.01",
    ),
    # Discovery
    "discovery-response": (
        30, "calendar",
        "Response to interrogatories / RFP / RFA",
        "Tenn. R. Civ. P. 33.01; 34.02; 36.01",
    ),
    "discovery-response-defendant-preanswer": (
        45, "calendar",
        "Defendant's response to interrogatories served before answering",
        "Tenn. R. Civ. P. 33.01",
    ),
    "rfa-deemed-admitted": (
        30, "calendar",
        "RFA — silence = admission (add 3 mail days under Rule 6.05 if mailed)",
        "Tenn. R. Civ. P. 36.01; 6.05",
    ),
    "mail-service-addon": (
        3, "calendar",
        "Days added to a service-triggered period when served by mail",
        "Tenn. R. Civ. P. 6.05",
    ),
    # Motion practice
    "summary-judgment-service": (
        -30, "calendar",
        "SJ motion must be SERVED at least 30 days before the hearing",
        "Tenn. R. Civ. P. 56.04",
    ),
    "summary-judgment-response": (
        -5, "calendar",
        "Adverse party's SJ response served no later than 5 days before hearing",
        "Tenn. R. Civ. P. 56.04",
    ),
    # Post-judgment / appeals
    "motion-alter-amend": (
        30, "calendar",
        "Rule 59 post-trial motion (alter/amend, new trial) — NON-extendable",
        "Tenn. R. Civ. P. 59.04",
    ),
    "rule-60-one-year": (
        365, "calendar",
        "Rule 60.02(1)/(2) outer limit (~1 year)",
        "Tenn. R. Civ. P. 60.02",
    ),
    "general-sessions-appeal": (
        10, "calendar",
        "De novo appeal of a General Sessions civil judgment to Circuit Court",
        "T.C.A. § 27-5-108",
    ),
    "detainer-appeal": (
        10, "calendar",
        "De novo appeal of a detainer (eviction) judgment to Circuit Court",
        "T.C.A. § 27-5-108",
    ),
    # FDCPA / Reg F (federal)
    "fdcpa-validation": (
        30, "calendar",
        "Consumer's window to dispute debt after § 1692g notice",
        "15 U.S.C. § 1692g(a)(3)",
    ),
    "fdcpa-sol": (
        365, "calendar",
        "FDCPA private civil action statute of limitations (1 year)",
        "15 U.S.C. § 1692k(d)",
    ),
    # Tennessee SOLs (see references for accrual / case authority)
    "sol-contract": (
        2191, "calendar",  # ~6 years
        "SOL — written contract / open account incl. most credit-card debt (6 years)",
        "T.C.A. § 28-3-109",
    ),
    "sol-goods": (
        1461, "calendar",  # ~4 years
        "SOL — sale of goods under the UCC (4 years)",
        "T.C.A. § 47-2-725",
    ),
    "sol-tort": (
        365, "calendar",
        "SOL — personal injury / personal torts (1 year)",
        "T.C.A. § 28-3-104",
    ),
    "sol-property": (
        1096, "calendar",  # ~3 years
        "SOL — injury to real or personal property (3 years)",
        "T.C.A. § 28-3-105",
    ),
    "sol-tcpa": (
        365, "calendar",
        "SOL — Tennessee Consumer Protection Act (1 year from discovery; 5-year repose)",
        "T.C.A. § 47-18-110",
    ),
    # Landlord-tenant
    "urlta-nonpayment-notice": (
        14, "calendar",
        "URLTA nonpayment: lease terminates >= 14 days after receipt if unpaid",
        "T.C.A. § 66-28-505",
    ),
    # Health Care Liability Act
    "hcla-presuit-notice": (
        -60, "calendar",
        "HCLA pre-suit notice — at least 60 days before filing the complaint",
        "T.C.A. § 29-26-121",
    ),
    "hcla-sol-extension": (
        120, "calendar",
        "SOL/repose extension after compliant HCLA pre-suit notice",
        "T.C.A. § 29-26-121(c)",
    ),
    "gtla-sol": (
        365, "calendar",
        "Governmental Tort Liability Act SOL (~12 months — verify § 29-20-305)",
        "T.C.A. § 29-20-305",
    ),
    # Family law (Title 36)
    "divorce-waiting-no-children": (
        60, "calendar",
        "Irreconcilable-differences divorce: complaint on file 60 days (no minor child)",
        "T.C.A. § 36-4-103(a)",
    ),
    "divorce-waiting-children": (
        90, "calendar",
        "Irreconcilable-differences divorce: complaint on file 90 days (unmarried child under 18)",
        "T.C.A. § 36-4-103(a)",
    ),
    "relocation-notice": (
        60, "calendar",
        "Parental relocation notice — 60 days before move (out of state / >50 miles)",
        "T.C.A. § 36-6-108",
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


def _easter(year: int) -> datetime.date:
    """Gregorian Easter Sunday (Anonymous / Meeus computus)."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return datetime.date(year, month, day)


def good_friday(year: int) -> datetime.date:
    """Good Friday = the Friday before Easter Sunday (movable; a TN
    legal holiday under T.C.A. § 15-1-101)."""
    return _easter(year) - datetime.timedelta(days=2)


def tn_holidays(year: int) -> set:
    """Return the set of Tennessee state legal holidays for a year
    (T.C.A. § 15-1-101), including observed-day substitution for the
    fixed-date holidays."""
    holidays = set()

    for m, d in FIXED_HOLIDAYS:
        date = datetime.date(year, m, d)
        # Observed-day shift (§ 15-1-101)
        if date.weekday() == 5:    # Saturday → preceding Friday
            date -= datetime.timedelta(days=1)
        elif date.weekday() == 6:  # Sunday → following Monday
            date += datetime.timedelta(days=1)
        holidays.add(date)

    for m, wd, n in WEEK_HOLIDAYS:
        holidays.add(_nth_weekday(year, m, wd, n))

    holidays.add(good_friday(year))

    return holidays


def is_court_day(d: datetime.date) -> bool:
    """True if d is a court day (not a weekend or TN legal holiday)."""
    if d.weekday() >= 5:   # Saturday or Sunday
        return False
    if d in tn_holidays(d.year):
        return False
    return True


def roll_forward_rule(d: datetime.date) -> datetime.date:
    """Tenn. R. Civ. P. 6.01: when the last day of the period falls on
    a Saturday, Sunday, or legal holiday, the period runs until the end
    of the next day that is not one of those days."""
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
        # Rule 6.01 roll-forward applies to forward counts
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
        lines.append("  Status: TODAY")
    elif delta < 0:
        lines.append(f"  Status: {abs(delta)} day(s) ago (OVERDUE if not done)")
    else:
        lines.append(f"  Status: {delta} day(s) from today")
    return "\n".join(lines)


def list_rules():
    print("Known rules (Tennessee):")
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
        description="Compute Tennessee court deadlines (Tenn. R. Civ. P. 6.01 + T.C.A. § 15-1-101)"
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
