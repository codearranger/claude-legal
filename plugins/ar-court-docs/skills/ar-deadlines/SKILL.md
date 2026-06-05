---
name: ar-deadlines
description: >
  Use when the user asks about timing or deadlines in an Arkansas civil
  case. Triggers include "when is my answer due in Arkansas", "Ark. R.
  Civ. P. 6 time computation", "Rule 6(d) mail rule", "3 days for
  mailing Arkansas", "deadline in Arkansas circuit court", "Arkansas
  court holidays", "Ark. Code Ann. § 1-5-101 holidays", "is Christmas
  Eve a court holiday in Arkansas", "Daisy Gatson Bates Day", "Arkansas
  statute of limitations", "SOL on a contract in Arkansas", "how long
  to appeal District Court de novo", "summary judgment response time
  Arkansas". Computes calendar-day deadlines under Ark. R. Civ. P. 6,
  applies the Rule 6(d) 3-day mail add-on, rolls forward off Saturdays
  / Sundays / Ark. Code Ann. § 1-5-101 legal holidays (including the
  distinctive Daisy Gatson Bates Day and Christmas Eve), and maps named
  rules (answer-due, district-court de novo appeal, summary-judgment
  response, statutes of limitations) to days plus authority.
version: 0.1.0
---

# Arkansas Case Deadlines

> **NOT LEGAL ADVICE.** This skill computes deadlines. Independently
> verify in the cited rule or statute, confirm the venue's local rules
> and any standing order, and treat no computed date as final without
> checking.

Use this skill to compute deadlines under **Ark. R. Civ. P. 6** (time
computation), the Arkansas legal-holiday list (**Ark. Code Ann.
§ 1-5-101**), and the named rules across the Ark. R. Civ. P. and the
Arkansas Code.

## Ark. R. Civ. P. 6(a) — time computation

To count a period stated in the Ark. R. Civ. P. or in an Arkansas
statute:

1. **Exclude** the day of the act or event that starts the period
   (e.g., the service date).
2. **Include** the last day of the period, **unless** it is a
   **Saturday, a Sunday, or a legal holiday** — in which case the
   period runs to the **end of the next day** that is not one of those.

### Ark. R. Civ. P. 6(d) — the 3-day mail add-on

When a party has a right or duty to act within a prescribed period
**after service of a notice or other paper**, and service was made **by
mail**, **3 days** are added to the prescribed period. Apply Rule 6(d)
**after** the underlying count. Confirm whether the venue treats
**electronic service** (under Administrative Order No. 21 / e-filing)
the same way — registered e-filers generally consent to e-service, and
the add-on treatment for e-service should be verified.

> Frame every day count below as the **current** rule. Confirm the
> number against the verbatim rule text in `ar-law-references` before
> treating any computed date as final — day counts are exactly the kind
> of value that drifts and must stay pointer-only here.

## Arkansas legal holidays — Ark. Code Ann. § 1-5-101

| Holiday | Date rule |
|---|---|
| New Year's Day | January 1 (fixed) |
| Dr. Martin Luther King Jr.'s Birthday | 3rd Monday in January |
| **George Washington's Birthday and Daisy Gatson Bates Day** | 3rd Monday in February (**combined** — distinctive) |
| Memorial Day | Last Monday in May |
| Independence Day | July 4 (fixed) |
| Labor Day | 1st Monday in September |
| Veterans Day | November 11 (fixed) |
| Thanksgiving Day | 4th Thursday in November |
| **Christmas Eve** | December 24 (fixed) — Arkansas state holiday (**distinctive**) |
| Christmas Day | December 25 (fixed) |

> **Two Arkansas specifics to flag.** Arkansas combines **George
> Washington's Birthday with Daisy Gatson Bates Day** on the **3rd
> Monday in February**, and observes **Christmas Eve (December 24)** as
> a state holiday. Both count for the Rule 6(a) roll-forward.

> ⚠ **The "employee's birthday" floating holiday is NOT a court-closure
> date.** Section 1-5-101 lets a state employee take a personal
> birthday holiday, but courts are **open** — do **not** encode it as a
> deadline-rolling holiday.

> ⚠ **Arkansas does NOT currently observe Columbus Day or Juneteenth as
> a § 1-5-101 holiday for these purposes, and Good Friday is NOT a state
> holiday.** Verify against the current statute when refreshing.

> **Substitution / weekend roll.** A holiday falling on **Saturday** is
> observed the **preceding Friday**; a holiday falling on **Sunday** is
> observed the **succeeding Monday**.

## Named rules — quick reference

Run `python3 scripts/case-calendar.py --rules` for the full list, and
`python3 scripts/case-calendar.py --from YYYY-MM-DD --rule <key>` for a
specific computation. The most commonly invoked:

| Rule key | What it is | Authority |
|---|---|---|
| `answer-due` | Answer due after service of summons & complaint | Ark. R. Civ. P. 12 |
| `answer-due-nonresident` | Longer answer window for out-of-state / nonresident defendants | Ark. R. Civ. P. 12 |
| `service-period` | Rule 4 period to serve the summons & complaint | Ark. R. Civ. P. 4 |
| `summary-judgment-response` | Response to a Rule 56 motion | Ark. R. Civ. P. 56 |
| `discovery-response` | Response to interrogatories / RFPs / RFAs | Ark. R. Civ. P. 33 / 34 / 36 |
| `mail-add-on` | Add-on for service by mail | Ark. R. Civ. P. 6(d) |
| `rule-60a-window` | Window for broad Rule 60(a) relief to vacate/modify | Ark. R. Civ. P. 60(a) |
| `district-court-appeal` | De novo appeal from District Court to Circuit Court | Ark. District Court Rules / Ark. R. Civ. P. |
| `sol-written-contract` | Written contract SOL | Ark. Code Ann. § 16-56-111 |
| `sol-oral-open-account` | Oral contract / open account SOL | Ark. Code Ann. § 16-56-105 |
| `sol-personal-injury` | Personal injury / general tort SOL | Ark. Code Ann. § 16-56-105 |
| `sol-med-mal` | Medical malpractice SOL | Ark. Code Ann. § 16-114-203 |
| `sol-wrongful-death` | Wrongful death SOL | Ark. Code Ann. § 16-62-102 |
| `judgment-life` | Judgment enforceable life | Ark. Code Ann. § 16-65-501 / § 16-56-114 |
| `fdcpa-validation` | Consumer's debt-validation window | 15 U.S.C. § 1692g |
| `fdcpa-sol` | FDCPA private-action SOL | 15 U.S.C. § 1692k(d) |

> The exact **day counts and year counts are deliberately not printed
> in this table** — they are the kind of value that drifts with
> amendments. The script encodes the current numbers and the holiday
> roll-forward; the authoritative numbers live in `ar-law-references`.
> Always confirm an unusual number against the cited rule. Statutory
> periods stated in **years** (SOLs, the judgment life) are computed on
> the calendar anniversary date, not as a fixed day-count.

## Two short / distinctive windows to watch

- **Rule 60(a) 90-day window** — Arkansas lets a court broadly modify
  or vacate a judgment **within 90 days** of entry; after that only the
  narrower Rule 60(c) grounds apply. Calendar the 90-day line the
  moment judgment enters. See `ar-post-judgment`.
- **District Court de novo appeal** — appeal from District Court to
  Circuit Court for trial de novo runs on a **short** window from
  entry; miss it and the judgment stands. Confirm the current count in
  `ar-law-references`. See `ar-district-courts` and `ar-post-judgment`.

## Statutes of limitations — primary Arkansas claims (Ark. Code Ann. Title 16)

| Claim | Authority | Notes |
|---|---|---|
| Written contract | Ark. Code Ann. § 16-56-111 | Most signed credit-card agreements |
| Oral contract / open account | Ark. Code Ann. § 16-56-105 | Open-account theory; shorter than written |
| Personal injury / general tort / negligence | Ark. Code Ann. § 16-56-105 | |
| Property damage / fraud | Ark. Code Ann. § 16-56-105 | Fraud subject to a discovery rule |
| Medical malpractice | Ark. Code Ann. § 16-114-203 | Shorter; see `ar-personal-injury` |
| Wrongful death | Ark. Code Ann. § 16-62-102 | Statutory beneficiaries |
| Judgments (enforceable life / revivable) | Ark. Code Ann. § 16-65-501 / § 16-56-114 | Scire facias revival |
| FDCPA | 15 U.S.C. § 1692k(d) | Applies in Arkansas courts |

SOL accrual, tolling, and any revival by part-payment or written
acknowledgment are **fact-dependent** — verify against current law for
the specific claim. For credit-card debt, whether the written-contract
or open-account period applies turns on whether a signed agreement
exists — see `ar-consumer-debt`.

## Examples

### "When is my answer due if I was served personally in Little Rock on Friday, March 14, 2025?"

```
$ python3 scripts/case-calendar.py --from 2025-03-14 --rule answer-due
Answer due (Ark. R. Civ. P. 12)
  From: Friday, March 14, 2025
  Calendar days after service; rolled forward off any
  Sat/Sun/§ 1-5-101 holiday (incl. Daisy Gatson Bates Day,
  Christmas Eve)
  Authority: Ark. R. Civ. P. 12
```

### "I was served by mail — how does that change it?"

Add the **Rule 6(d) 3-day mail add-on** after the underlying count, then
roll forward off any Saturday/Sunday/§ 1-5-101 holiday.

## How `ar-deadlines` composes with the scripts

The body above is the reference; the arithmetic lives in
`scripts/case-calendar.py`, which:

- Encodes the Ark. Code Ann. § 1-5-101 holidays (including the combined
  **Washington's Birthday / Daisy Gatson Bates Day** and **Christmas
  Eve**, and **excluding** Columbus Day, Juneteenth, Good Friday, and
  the floating employee birthday)
- Computes the holiday set for any year and the weekend/holiday
  roll-forward rule
- Applies the Ark. R. Civ. P. 6(d) 3-day mail add-on
- Maps named rule keys to `(days, description, authority)`

Use `scripts/case-calendar.py --rules` for the canonical list and
`scripts/case-calendar.py --from YYYY-MM-DD --rule <key>` for a specific
computation.

## Composition

- For format: `ar-statewide-format`
- For the substantive rule text: `ar-law-references`
- For first-response timing: `ar-first-30-days`
- For discovery timing: `ar-discovery`
- For post-judgment timing (Rule 59 / 60, the de novo appeal):
  `ar-post-judgment`
- For matter-specific deadlines: `ar-family-law`, `ar-consumer-debt`,
  `ar-personal-injury`

## References

- `ar-law-references` hosts the Ark. R. Civ. P. 6 text (with the 6(d)
  mail rule), the Ark. Code Ann. § 1-5-101 holiday statute with
  year-by-year computed dates, the SOL chart by claim type with
  authority, and the full named-rules list with current day counts.
