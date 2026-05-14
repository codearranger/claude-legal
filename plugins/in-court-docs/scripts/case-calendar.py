#!/usr/bin/env python3
"""
case-calendar.py — Compute Indiana court deadlines.

Supports calendar-day and court-day counting with Indiana state
holidays (IC 1-1-9-1) excluded for court-day mode and applied as
end-of-period rollover days under Ind. Trial R. 6(A).

Indiana-specific quirks encoded here:

  - Good Friday is an Indiana state holiday under IC 1-1-9-1
    (most states do not observe it as a judicial holiday)
  - Primary Election Day (1st Tuesday after 1st Monday in May,
    even years) is a state holiday
  - General Election Day (1st Tuesday after 1st Monday in
    November, even years) is a state holiday
  - Day after Thanksgiving is observed by Governor's proclamation
    most years
  - Indiana abolished T.R. 6(E) in 2009 — no extra mail days
    (unlike federal FRCP 6(d) and Oregon ORCP 10 C)

Usage:
    case-calendar.py --from YYYY-MM-DD --days N --mode [calendar|court]
    case-calendar.py --from YYYY-MM-DD --rule RULE_KEY
    case-calendar.py --rules

Examples:
    # Answer due — 20 calendar days from service 2025-04-15
    case-calendar.py --from 2025-04-15 --days 20 --mode calendar

    # SOL on credit card account — 6 years from last activity
    case-calendar.py --from 2019-03-15 --rule sol-open-account

    # Apply a named rule
    case-calendar.py --from 2025-04-15 --rule answer-due

    # List known rules
    case-calendar.py --rules
"""

import argparse
import datetime
import sys
from typing import Optional


# Indiana legal holidays (IC 1-1-9-1)
# Holidays falling on Saturday are observed on Friday; Sunday -> Monday
# (Indiana practice tracks the federal observed-day rule).
FIXED_HOLIDAYS = [
    (1, 1),    # New Year's Day
    (2, 12),   # Lincoln's Birthday (observed; courts often open)
    (7, 4),    # Independence Day
    (11, 11),  # Veterans Day
    (12, 25),  # Christmas Day
]

# Week-based holidays (n-th weekday of month)
WEEK_HOLIDAYS = [
    # (month, weekday [0=Mon], ordinal [1=first, -1=last])
    (1, 0, 3),   # MLK — 3rd Monday of January
    (2, 0, 3),   # Washington's Birthday — 3rd Monday of February
    (5, 0, -1),  # Memorial Day — last Monday of May
    (9, 0, 1),   # Labor Day — 1st Monday of September
    (10, 0, 2),  # Columbus Day — 2nd Monday of October
    (11, 3, 4),  # Thanksgiving — 4th Thursday of November
]


def _easter_date(year: int) -> datetime.date:
    """Compute Easter Sunday for a given year (Meeus/Jones/Butcher
    Gregorian algorithm). Good Friday is the preceding Friday."""
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
    L = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * L) // 451
    month = (h + L - 7 * m + 114) // 31
    day = ((h + L - 7 * m + 114) % 31) + 1
    return datetime.date(year, month, day)


def _good_friday(year: int) -> datetime.date:
    """Good Friday is the Friday before Easter Sunday."""
    return _easter_date(year) - datetime.timedelta(days=2)


def _election_day(year: int, month: int) -> Optional[datetime.date]:
    """
    Indiana Election Days (IC 1-1-9-1):
      - Primary: 1st Tuesday after 1st Monday in May, even years
      - General: 1st Tuesday after 1st Monday in November, even
        years
    """
    if year % 2 != 0:
        return None
    # Find 1st Monday of month
    first = datetime.date(year, month, 1)
    offset_mon = (0 - first.weekday()) % 7
    first_monday = first + datetime.timedelta(days=offset_mon)
    # Tuesday after 1st Monday
    return first_monday + datetime.timedelta(days=1)


# Named rules: (days, mode, description, authority)
RULES = {
    # Initial response
    "answer-due": (
        20, "calendar",
        "Answer due after service (T.R. 6(C))",
        "Ind. Trial R. 6(C)",
    ),
    "answer-due-extension": (
        50, "calendar",
        "Answer + 30-day extension by stipulation (T.R. 6(B))",
        "Ind. Trial R. 6(B), (C)",
    ),
    "appearance-due": (
        20, "calendar",
        "Appearance form due with first responsive filing",
        "Ind. Trial R. 3.1",
    ),

    # Discovery
    "interrogatory-response": (
        30, "calendar",
        "Interrogatory response due (T.R. 33(C))",
        "Ind. Trial R. 33(C)",
    ),
    "rfp-response": (
        30, "calendar",
        "RFP response due (T.R. 34(B))",
        "Ind. Trial R. 34(B)",
    ),
    "rfa-response": (
        30, "calendar",
        "RFA response due (T.R. 36(A)); failure deems admitted",
        "Ind. Trial R. 36(A)",
    ),
    "deposition-notice": (
        10, "calendar",
        "Deposition notice — minimum 10 days (T.R. 30(B)(1))",
        "Ind. Trial R. 30(B)(1)",
    ),
    "subpoena-non-party-notice": (
        5, "calendar",
        "Subpoena notice to parties before service on non-party (T.R. 45(B)(1))",
        "Ind. Trial R. 45(B)(1)",
    ),

    # Summary judgment (T.R. 56)
    "summary-judgment-response": (
        30, "calendar",
        "SJ response due (30 days after service) (T.R. 56(C))",
        "Ind. Trial R. 56(C)",
    ),
    "summary-judgment-reply-marion-cpc": (
        15, "calendar",
        "SJ reply (Marion CPC default; varies by courtroom)",
        "Marion CPC § IV; Ind. Trial R. 56(C)",
    ),

    # Motion practice
    "motion-response-typical": (
        15, "calendar",
        "Motion response (typical Marion CPC / local rule)",
        "Marion CPC § II; Ind. Trial R. 7",
    ),
    "motion-reply-typical": (
        7, "calendar",
        "Motion reply (typical local-rule convention)",
        "Marion CPC § II",
    ),
    "continuance-motion": (
        7, "calendar",
        "Motion to continue — file at least 7 days before setting",
        "Ind. Trial R. 53.5; LR49-TR53.5",
    ),

    # Post-judgment
    "motion-to-correct-error": (
        30, "calendar",
        "T.R. 59 Motion to Correct Error (jurisdictional)",
        "Ind. Trial R. 59(C)",
    ),
    "tr-59-deemed-denied": (
        45, "calendar",
        "T.R. 59 motion deemed denied if no ruling within 45 days",
        "Ind. Trial R. 59(B)",
    ),
    "tr-60-b-1-3-deadline": (
        365, "calendar",
        "T.R. 60(B)(1)-(3) motion — outer 1-year deadline",
        "Ind. Trial R. 60(B)",
    ),
    "notice-of-appeal-no-tr59": (
        30, "calendar",
        "Notice of Appeal — 30 days from final judgment (no T.R. 59 filed)",
        "Ind. App. R. 9(A)(1)",
    ),
    "notice-of-appeal-with-tr59": (
        30, "calendar",
        "Notice of Appeal — 30 days from T.R. 59 ruling (or deemed denial)",
        "Ind. App. R. 9(A)(1); Ind. Trial R. 59(B)",
    ),
    "garnishee-answer": (
        20, "calendar",
        "Garnishee Defendant Answer due (Garnishee Summons)",
        "Ind. Trial R. 4; T.R. 69",
    ),
    "judgment-life": (
        7305, "calendar",  # 20 years (approx; 20 * 365.25)
        "Judgment lifespan (20 years, renewable)",
        "IC 34-55-1-2",
    ),
    "judgment-lien-real-property": (
        3653, "calendar",  # 10 years
        "Judgment lien on real property expires (renewable)",
        "IC 34-55-9-2",
    ),

    # Statutes of limitation (defenses)
    "sol-open-account": (
        2191, "calendar",  # 6 years (approx; 6 * 365.25)
        "SOL — open account / account stated / credit card (6 years)",
        "IC 34-11-2-7",
    ),
    "sol-written-contract-money": (
        2191, "calendar",
        "SOL — written contract for money signed by party charged (6 years)",
        "IC 34-11-2-11",
    ),
    "sol-written-contract-property": (
        3653, "calendar",  # 10 years
        "SOL — written contract NOT for money (property) (10 years)",
        "IC 34-11-2-9",
    ),
    "sol-promissory-note": (
        2191, "calendar",
        "SOL — promissory note (6 years)",
        "IC 34-11-2-13",
    ),
    "sol-personal-injury": (
        730, "calendar",  # 2 years
        "SOL — personal injury (2 years)",
        "IC 34-11-2-4",
    ),
    "sol-fraud-discovery": (
        2191, "calendar",
        "SOL — fraud (6 years from discovery)",
        "IC 34-11-2-7",
    ),
    "sol-foreign-judgment": (
        3653, "calendar",
        "SOL — foreign judgment registration (10 years)",
        "IC 34-11-2-10",
    ),

    # Consumer-protection SOLs
    "sol-dcsa-discovery": (
        730, "calendar",
        "SOL — Indiana DCSA (2 years from discovery)",
        "IC 24-5-0.5-5(b)",
    ),
    "sol-fdcpa": (
        365, "calendar",
        "SOL — federal FDCPA (1 year from violation)",
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
    "sol-iuccc": (
        365, "calendar",
        "SOL — Indiana UCCC civil liability (1 year)",
        "IC 24-4.5-5-201(2)",
    ),

    # FDCPA / Reg F windows
    "fdcpa-validation-period": (
        30, "calendar",
        "Consumer's window to dispute debt (FDCPA validation)",
        "15 U.S.C. § 1692g; 12 C.F.R. § 1006.34",
    ),
    "dcsa-cure-period": (
        30, "calendar",
        "DCSA pre-suit cure period — 30 days from written demand",
        "IC 24-5-0.5-5(a)",
    ),
    "small-claims-trial-de-novo": (
        60, "calendar",
        "Trial de novo from small-claims judgment (Marion / Lake)",
        "IC 33-29-2-13 / IC 33-34-9-1",
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


def in_holidays(year: int) -> set:
    """Return set of Indiana state legal holidays for a year (IC 1-1-9-1)."""
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

    # Indiana-specific: Good Friday
    holidays.add(_good_friday(year))

    # Indiana-specific: Election Days (even years only)
    primary = _election_day(year, 5)
    if primary:
        holidays.add(primary)
    general = _election_day(year, 11)
    if general:
        holidays.add(general)

    # Day after Thanksgiving — observed most years by Governor's
    # proclamation. We include it by default; remove if a given
    # year's proclamation excludes it.
    thanksgiving = _nth_weekday(year, 11, 3, 4)
    holidays.add(thanksgiving + datetime.timedelta(days=1))

    return holidays


def is_court_day(d: datetime.date) -> bool:
    """True if d is a court day (not a weekend or Indiana legal holiday)."""
    if d.weekday() >= 5:   # Saturday or Sunday
        return False
    if d in in_holidays(d.year):
        return False
    return True


def add_calendar_days(start: datetime.date, n: int) -> datetime.date:
    """Add calendar days. Apply T.R. 6(A) end-of-period rule:
    if the final day falls on weekend or Indiana legal holiday,
    extend to next non-holiday business day."""
    end = start + datetime.timedelta(days=n)
    if n != 0:
        step = 1 if n > 0 else -1
        while not is_court_day(end):
            end += datetime.timedelta(days=step)
    return end


def add_court_days(start: datetime.date, n: int) -> datetime.date:
    """Count n court days forward (if n>0) or backward (if n<0).
    Used for periods of less than 7 days under T.R. 6(A) where
    intermediate weekends and holidays are excluded."""
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
    print("Known Indiana deadline rules:")
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
        description="Compute Indiana court deadlines (T.R. 6(A) time computation with IC 1-1-9-1 holidays)"
    )
    parser.add_argument("--from", dest="from_date", help="Triggering date (YYYY-MM-DD)")
    parser.add_argument("--days", type=int, help="Number of days (negative = before)")
    parser.add_argument(
        "--mode",
        choices=["calendar", "court"],
        default="calendar",
        help="Calendar days (default) or court days (for periods <7 days under T.R. 6(A))",
    )
    parser.add_argument("--rule", help="Named rule (see --rules)")
    parser.add_argument("--rules", action="store_true", help="List known Indiana deadline rules")
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
