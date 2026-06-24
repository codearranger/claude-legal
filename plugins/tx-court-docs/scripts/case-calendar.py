#!/usr/bin/env python3
"""
case-calendar.py — Compute Texas court deadlines.

Supports calendar-day and court-day counting with Texas legal holidays
(Tex. Gov't Code § 662.003) excluded for court-day mode, and the
Tex. R. Civ. P. 4 time-computation rule (exclude the day of the event,
count every intervening day including weekends and holidays, include the
last day; if the last day is a Saturday, Sunday, or legal holiday, the
period runs to the next day that is not).

Texas quirk — the "Monday rule" answer deadline: in a district or
constitutional/statutory county court, a defendant's answer is due "by
10:00 a.m. on the Monday next after the expiration of twenty days after
the date of service" (Tex. R. Civ. P. 99(b)). That is NOT a flat 20-day
count; the special rule `answer-due` computes it. In a justice court the
answer is due by the end of the 14th day after service of citation
(Tex. R. Civ. P. 502.5) — use `answer-due-justice`.

When a period runs from service and service was by mail / commercial
delivery (and, where applicable, fax or email), Tex. R. Civ. P. 21a adds
days — confirm the current add-on against the court-rules corpus.

Usage:
    case-calendar.py --from YYYY-MM-DD --days N --mode [calendar|court]
    case-calendar.py --from YYYY-MM-DD --rule RULE_KEY
    case-calendar.py --rules

Examples:
    # District-court answer — Monday rule from service 2025-04-15
    case-calendar.py --from 2025-04-15 --rule answer-due

    # SOL on debt / written contract — 4 years from last activity 2021-03-15
    case-calendar.py --from 2021-03-15 --rule sol-debt

    # Discovery response — 30 days from service 2025-04-15
    case-calendar.py --from 2025-04-15 --rule rfp-response

    # List known rules
    case-calendar.py --rules
"""

import argparse
import datetime
import sys
from typing import Optional


# Texas legal holidays the courts observe (Tex. Gov't Code § 662.003(a),
# the "national holidays," which are the court-closed days). The state-only
# "partial-staffing" holidays in § 662.003(b) — Confederate Heroes Day
# (Jan 19), Texas Independence Day (Mar 2), San Jacinto Day (Apr 21), and
# Lyndon B. Johnson Day (Aug 27) — generally do NOT close the courts and are
# intentionally excluded here.
#
# Observed-day shift: a holiday that falls on Saturday is observed the
# preceding Friday; a holiday that falls on Sunday is observed the following
# Monday (the common clerk practice for court-closure purposes).
FIXED_HOLIDAYS = [
    (1, 1),    # New Year's Day
    (6, 19),   # Juneteenth (Emancipation Day in Texas) — also a national holiday
    (7, 4),    # Independence Day
    (11, 11),  # Veterans Day
    (12, 25),  # Christmas Day
]

# Week-based holidays (n-th weekday of month)
WEEK_HOLIDAYS = [
    # (month, weekday [0=Mon], ordinal [1=first, -1=last])
    (1, 0, 3),   # Martin Luther King, Jr. Day — 3rd Mon Jan
    (2, 0, 3),   # Presidents' Day / Washington's Birthday — 3rd Mon Feb
    (5, 0, -1),  # Memorial Day — last Mon May
    (9, 0, 1),   # Labor Day — 1st Mon Sep
    (11, 3, 4),  # Thanksgiving Day — 4th Thu Nov
    # Friday after Thanksgiving is handled in tx_holidays() (Thu + 1).
]


# Named rules: (days, mode, description, authority)
# NOTE on drift: day counts here are framework anchors. Statutes of
# limitation and notice periods can change; confirm against the
# tx-statutes-debt / court-rules corpora before relying on a figure.
RULES = {
    # Initial response (see also the special `answer-due` Monday rule below)
    "answer-due": (
        0, "special-monday",
        "District/county-court answer — 10:00 a.m. on the Monday next after "
        "20 days from service (the Texas 'Monday rule')",
        "Tex. R. Civ. P. 99(b)",
    ),
    "answer-due-justice": (
        14, "calendar",
        "Justice-court answer — by the end of the 14th day after service of "
        "citation",
        "Tex. R. Civ. P. 502.5",
    ),

    # Discovery (30-day response window)
    "interrogatory-response": (
        30, "calendar",
        "Interrogatory response due (30 days); cap of 25 (excluding those "
        "identifying persons with knowledge)",
        "Tex. R. Civ. P. 197.2(a), 197.1",
    ),
    "rfp-response": (
        30, "calendar",
        "Request-for-production response due (30 days; 50 days if served with "
        "or before the answer is due — confirm)",
        "Tex. R. Civ. P. 196.2",
    ),
    "rfa-response": (
        30, "calendar",
        "Request-for-admission response due (30 days); failure deems admitted",
        "Tex. R. Civ. P. 198.2",
    ),

    # Summary judgment (Tex. R. Civ. P. 166a) — counted BACKWARD from hearing
    "sj-motion-before-hearing": (
        -21, "calendar",
        "Summary-judgment motion served & filed at least 21 days before the "
        "hearing or submission",
        "Tex. R. Civ. P. 166a(c)",
    ),
    "sj-response-before-hearing": (
        -7, "calendar",
        "Summary-judgment response due not later than 7 days before the "
        "hearing (absent leave)",
        "Tex. R. Civ. P. 166a(c)",
    ),

    # Pleadings / motions
    "rule-91a-motion": (
        60, "calendar",
        "Rule 91a motion to dismiss filed within 60 days after the first "
        "pleading containing the challenged cause of action",
        "Tex. R. Civ. P. 91a.3",
    ),

    # Post-judgment (plenary power; Tex. R. Civ. P. 329b)
    "motion-new-trial": (
        30, "calendar",
        "Motion for new trial / to modify, correct, or reform the judgment "
        "(within 30 days after the judgment is signed)",
        "Tex. R. Civ. P. 329b(a), (g)",
    ),
    "plenary-power": (
        30, "calendar",
        "Trial court's plenary power (30 days after signing, absent a timely "
        "post-judgment motion that extends it)",
        "Tex. R. Civ. P. 329b(d)",
    ),
    "appeal": (
        30, "calendar",
        "Notice of appeal to the Court of Appeals (30 days after the judgment "
        "is signed; 90 days if a timely MNT / request for findings is filed)",
        "Tex. R. App. P. 26.1",
    ),
    "appeal-with-mnt": (
        90, "calendar",
        "Notice of appeal when a timely motion for new trial, motion to "
        "modify, or request for findings was filed (90 days)",
        "Tex. R. App. P. 26.1(a)",
    ),
    "restricted-appeal": (
        180, "calendar",
        "Restricted appeal (6 months after the judgment is signed)",
        "Tex. R. App. P. 26.1(c), 30",
    ),
    "findings-request": (
        20, "calendar",
        "Request for findings of fact and conclusions of law (20 days after "
        "the judgment is signed)",
        "Tex. R. Civ. P. 296",
    ),

    # Justice-court appeals
    "eviction-appeal": (
        5, "calendar",
        "Appeal of a justice-court eviction judgment to county court "
        "(5 days after the judgment is signed)",
        "Tex. R. Civ. P. 510.9",
    ),
    "jp-appeal": (
        21, "calendar",
        "Appeal of a (non-eviction) justice-court judgment to county court "
        "(21 days after the judgment is signed)",
        "Tex. R. Civ. P. 506.1",
    ),

    # Statutes of limitation (defenses) — Tex. Civ. Prac. & Rem. Code
    "sol-debt": (
        1461, "calendar",  # 4 years
        "SOL — debt / breach of contract / open or stated account (4 years)",
        "Tex. Civ. Prac. & Rem. Code § 16.004; residual § 16.051",
    ),
    "sol-personal-injury": (
        730, "calendar",  # 2 years
        "SOL — personal injury / most torts (2 years)",
        "Tex. Civ. Prac. & Rem. Code § 16.003",
    ),
    "sol-fraud": (
        1461, "calendar",  # 4 years
        "SOL — fraud / breach of fiduciary duty (4 years)",
        "Tex. Civ. Prac. & Rem. Code § 16.004",
    ),
    "sol-dtpa": (
        730, "calendar",  # 2 years
        "SOL — DTPA (2 years from when the deceptive act occurred or was or "
        "should have been discovered)",
        "Tex. Bus. & Com. Code § 17.565",
    ),
    "sol-judgment-dormancy": (
        3653, "calendar",  # 10 years
        "Judgment dormancy — a judgment becomes dormant if no writ of "
        "execution issues within 10 years (revival by scire facias)",
        "Tex. Civ. Prac. & Rem. Code § 34.001; revival § 31.006",
    ),

    # DTPA pre-suit notice
    "dtpa-presuit-notice": (
        60, "calendar",
        "DTPA pre-suit written notice — at least 60 days before filing suit",
        "Tex. Bus. & Com. Code § 17.505(a)",
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


def tx_holidays(year: int) -> set:
    """Return set of Texas court-observed legal holidays for a year
    (Tex. Gov't Code § 662.003(a))."""
    holidays = set()

    for m, d in FIXED_HOLIDAYS:
        date = datetime.date(year, m, d)
        # Observed-day shift for court-closure purposes.
        if date.weekday() == 5:    # Saturday → preceding Friday
            date -= datetime.timedelta(days=1)
        elif date.weekday() == 6:  # Sunday → following Monday
            date += datetime.timedelta(days=1)
        holidays.add(date)

    for m, wd, n in WEEK_HOLIDAYS:
        holidays.add(_nth_weekday(year, m, wd, n))

    # Friday after Thanksgiving (state holiday; courts customarily closed).
    thanksgiving = _nth_weekday(year, 11, 3, 4)
    holidays.add(thanksgiving + datetime.timedelta(days=1))

    return holidays


def is_court_day(d: datetime.date) -> bool:
    """True if d is a court day (not a weekend or Texas legal holiday)."""
    if d.weekday() >= 5:   # Saturday or Sunday
        return False
    if d in tx_holidays(d.year):
        return False
    return True


def add_calendar_days(start: datetime.date, n: int) -> datetime.date:
    """Add calendar days. Apply the Tex. R. Civ. P. 4 end-of-period rule:
    exclude the first day, include the last; if the final day falls on a
    Saturday, Sunday, or legal holiday, roll to the next day that is not."""
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


def texas_monday_rule(service: datetime.date) -> datetime.date:
    """Tex. R. Civ. P. 99(b): the answer is due by 10:00 a.m. on the Monday
    next after the expiration of twenty days after the date of service.

    Compute 20 days after service, then advance to the following Monday. If
    the 20-day mark is itself a Monday, the rule still points to the NEXT
    Monday (the Monday *next after* the expiration of the 20 days)."""
    twentieth = service + datetime.timedelta(days=20)
    # Days until the next Monday (strictly after the 20-day mark).
    # weekday(): Monday == 0.
    days_ahead = (0 - twentieth.weekday()) % 7
    if days_ahead == 0:
        days_ahead = 7
    monday = twentieth + datetime.timedelta(days=days_ahead)
    # If that Monday is a legal holiday, the clerk's office is closed; the
    # period runs to the next day that is not a Saturday, Sunday, or holiday.
    while not is_court_day(monday):
        monday += datetime.timedelta(days=1)
    return monday


def compute_deadline(start: datetime.date, days: int, mode: str) -> datetime.date:
    if mode == "special-monday":
        return texas_monday_rule(start)
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
    header = f"Deadline: {deadline.strftime('%A, %B %d, %Y')}"
    if mode == "special-monday":
        header += " (answer due by 10:00 a.m.)"
    if description:
        header = f"{description}\n{header}"
    lines = [header]
    lines.append(f"  From: {start.strftime('%A, %B %d, %Y')}")
    if mode == "special-monday":
        lines.append("  Rule: Monday next after 20 days from service (Tex. R. Civ. P. 99(b))")
    else:
        direction = "after" if days >= 0 else "before"
        n = abs(days)
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
    print("Known rules (Texas):")
    print()
    for key, (days, mode, desc, auth) in sorted(RULES.items()):
        if mode == "special-monday":
            direction = "special (Monday rule)"
            mode_label = ""
        else:
            direction = "" if days == 0 else (f"+{days}" if days > 0 else f"{days}")
            mode_label = mode
        print(f"  {key}")
        print(f"    {desc}")
        print(f"    {direction} {mode_label} days".rstrip())
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
        description="Compute Texas court deadlines (Tex. R. Civ. P. 4 / Tex. Gov't Code § 662.003)"
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
