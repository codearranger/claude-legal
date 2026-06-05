# Ark. Code Ann. Title 1, Chapter 5 — Holidays and Observances

> **CURATED SUMMARY — NOT VERBATIM STATUTORY TEXT.** This is a structured,
> citation-rich digest for drafting use. The official section text (public
> domain) is at https://law.justia.com/codes/arkansas/title-1/ (walk to
> Chapter 5). A future run of `scripts/pull_arkansas_statutes.py` will
> supersede this file with verbatim text.
>
> **NOT LEGAL ADVICE.** Verify every section against the current Ark. Code
> Ann. before filing.

## Scope

Title 1 ("General Provisions"), Chapter 5 designates Arkansas's official
state holidays and memorial/observance days. For litigation it matters
chiefly because **Ark. R. Civ. P. 6(a) excludes legal holidays** from
deadline computation when a period ends on one, rolling the deadline to the
next non-holiday, non-weekend day. The `case-calendar.py` deadline-arithmetic
helper encodes the § 1-5-101 closure holidays.

## Key sections

- **§ 1-5-101 — Legal/state holidays.** Enumerates the days observed as
  official Arkansas state holidays. The set (verify against current text)
  comprises:
  1. New Year's Day — January 1
  2. Dr. Martin Luther King Jr.'s Birthday — third Monday in January (made a
     standalone holiday after the legislature separated it from the former
     Robert E. Lee combination)
  3. **George Washington's Birthday and Daisy Gatson Bates Day** — third
     Monday in February. **DISTINCTIVE:** Arkansas pairs Washington's Birthday
     with **Daisy Gatson Bates Day**, honoring the civil-rights leader, on the
     same third-Monday-of-February observance.
  4. Memorial Day — last Monday in May
  5. Independence Day — July 4
  6. Labor Day — first Monday in September
  7. Veterans Day — November 11
  8. Thanksgiving Day — fourth Thursday in November
  9. **Christmas Eve — December 24.** **DISTINCTIVE:** Arkansas observes
     December 24 as a state holiday in its own right.
  10. Christmas Day — December 25
  11. **An employee's birthday — a floating personal holiday.** State
      employees may take their own birthday as a holiday. This is a personal
      day, **NOT a fixed statewide court-closure date** — courts remain open,
      so it should **not** be encoded as a deadline-rolling holiday in
      calendar math.

- **§ 1-5-102 — Memorial / commemorative days and observances.** Designates
  additional commemorative days that are observed but are generally **not**
  court-closure holidays (and so do not roll civil deadlines). Confirm the
  current catalog against the statute before relying on any single day.

## Weekend-observance rule

When a fixed-date § 1-5-101 holiday falls on a weekend, the observed closure
typically shifts: a **Saturday** holiday is observed the **preceding Friday**,
and a **Sunday** holiday is observed the **succeeding Monday** (verify against
current administrative practice). For Ark. R. Civ. P. 6(a) deadline
computation, treat the **observed** closure day as the holiday.

## Not on the Arkansas § 1-5-101 list (verify when refreshing)

Arkansas does **not** currently carry **Columbus Day** or **Juneteenth** as a
§ 1-5-101 state-closure holiday for deadline purposes, and **Good Friday** is
not a state holiday. Confirm against the current statute on each refresh, as
the holiday catalog is amended from time to time by act of the General
Assembly.

## Drafting / deadline note

For court-deadline computation under Ark. R. Civ. P. 6(a), exclude the
fixed-date and floating-Monday § 1-5-101 holidays above (and observed
weekend shifts), but **exclude the floating employee birthday** from
deadline math because it is not a uniform court closure.
