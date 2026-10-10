# Integration — end-to-end Texas debt-defense answer

## Prompt

A debt buyer sued me in a Smith County, Texas Justice Court (Precinct
1) on an old credit card — they're calling it a "sworn account." I was
served on **April 15, 2025**. I think the debt is too old and I don't
think they really own it. Walk me through defending this and draft my
answer.

## Expected triggers

- `tx-smith-county-jp`
- `tx-justice-courts`
- `tx-first-30-days`
- `tx-consumer-debt`
- `tx-deadlines`
- `tx-statewide-format`

## Acceptance criteria

### Deadline + venue

- [ ] Identifies the venue as a **Smith County Justice Court, Precinct
      1** and that justice-court procedure runs on **TRCP 500–510**,
      with the Rules of Civil Procedure / Evidence largely inapplicable
      except as Part V incorporates them (TRCP 500.3(e))
- [ ] States the justice-court answer is due by the **end of the 14th
      day after service** (TRCP 502.5) — i.e., **April 29, 2025** from
      the April 15 service date — and offers `case-calendar.py --from
      2025-04-15 --rule answer-due-justice`; if the matter were instead
      in district/county court, notes the **TRCP 99 Monday rule** would
      govern (May 12, 2025)

### Substance preserved in the answer

- [ ] Raises the **statute-of-limitations** defense (4-year, CPRC
      § 16.004) and the **no-revival** rule for time-barred consumer
      debt (Fin. Code § 392.307) — reading the figures from the corpus
- [ ] Includes a **verified denial of the sworn account** (TRCP 185 /
      93(10)) — recognizing that a bare general denial does not put a
      sworn account in issue — verified by a CPRC § 132.001 unsworn
      declaration since no notary is needed
- [ ] Raises the **standing / chain-of-title** challenge and the
      **§ 392.101 surety-bond** issue, and targets discovery at the
      chain-of-title documents (`tx-discovery`)
- [ ] Responds to each allegation; avoids admitting the debt or amount

### Form

- [ ] Applies the simplified JP pleading posture with the
      `tx-statewide-format` caption/footer and a **certificate of
      service**; **pro-se signature block with no bar number**
- [ ] Notes a **TRCP 145 Statement of Inability** is available if costs
      can't be paid, and that JP appeals are **de novo to county court**
      (TRCP 506)

## Common failure modes

- Uses the Monday rule (or a flat 20 days) for the justice-court answer
  instead of the 14-day TRCP 502.5 window
- Files a bare general denial against a sworn account (no verified
  denial)
- Imposes full district-court motion/evidence practice in JP court
- Recites the SOL / bond / § 392.307 figures from memory
