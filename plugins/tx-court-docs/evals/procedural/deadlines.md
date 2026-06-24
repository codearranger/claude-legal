# tx-deadlines — Monday-rule answer + JP answer + SOL

## Prompt

I was served with a citation and original petition in a Texas district
court case on **April 15, 2025**. When is my answer due, and how do I
count it? Also — if it had been filed in a justice court instead, when
would the answer be due?

## Expected triggers

- `tx-deadlines`
- `tx-first-30-days`

## Acceptance criteria

### District-court answer (the Monday rule — Texas quirk)

- [ ] States the answer is due under **TRCP 99** by **10:00 a.m. on the
      Monday next after the expiration of twenty days after the date of
      service** — and explicitly flags this is NOT a flat 20-day count
- [ ] Computes it from the user's April 15, 2025 service date: 20 days
      after service is May 5, 2025; the answer is therefore due
      **Monday, May 12, 2025 at 10:00 a.m.** (the Monday next after
      that 20-day expiration) — and the deterministic arithmetic is
      shown
- [ ] Offers `scripts/case-calendar.py --from 2025-04-15 --rule
      answer-due` (the special Monday-rule key)

### Justice-court answer

- [ ] States the justice-court answer is due by the **end of the 14th
      day after service of citation** (TRCP 502.5), and offers
      `--rule answer-due-justice`

### Time computation + holidays

- [ ] Applies **TRCP 4** computation (exclude the day of service,
      include the last day; roll forward off a Saturday/Sunday/legal
      holiday) and the **TRCP 21a +3 days** for service by mail/email
      where relevant
- [ ] Uses **Tex. Gov't Code § 662.003** holidays if a deadline lands
      on one, treating Juneteenth and the Friday after Thanksgiving as
      court-closed and the state partial-staffing days (Confederate
      Heroes Day, Texas Independence Day, San Jacinto Day, LBJ Day) as
      NOT court-closed

### SOL anchor

- [ ] Identifies the **4-year** limitations period for a debt/contract
      claim (CPRC § 16.004), confirming the period against the corpus

## Common failure modes

- Treats the district answer as due a flat 20 days after service
- Forgets to roll the 20-day expiration forward to the next Monday at
  10:00 a.m.
- Excludes Juneteenth incorrectly, or excludes a partial-staffing day
  as court-closed
