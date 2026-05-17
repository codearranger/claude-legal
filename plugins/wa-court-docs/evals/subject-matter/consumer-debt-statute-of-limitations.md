# wa-consumer-debt — Statute of limitations on credit-card debt

## Prompt

I was sued in Washington on a credit-card account. My last
payment was about 5 years ago. The complaint attaches monthly
statements but no signed cardholder agreement. What's my SOL
defense?

## Expected triggers

- `wa-consumer-debt`
- `wa-first-30-days`
- `wa-law-references`

## Acceptance criteria

- [ ] Identifies the SOL framework at **RCW 4.16** (see
      `wa-law-references/references/wa-rcw-debt/RCW-4_16.md`
      for current day counts)
- [ ] Distinguishes written-contract SOL (longer) vs.
      oral / account-stated SOL (shorter) — chooses based on
      whether plaintiff produces the signed cardholder agreement
- [ ] Notes that without the signed agreement, the shorter SOL
      may apply (depending on jurisdiction and case law —
      *Discover Bank v. Bridges*)
- [ ] Computes the time from last-payment date against the
      applicable current SOL (per chapter file) to flag whether
      facially time-barred
- [ ] Notes acknowledgment / partial-payment revival risk
- [ ] Notes affirmative-defense pleading requirement (must be
      pleaded in answer)
- [ ] References FDCPA / Regulation F prohibition on collecting
      time-barred debt as the parallel federal counterclaim

## Common failure modes

- Hard-coding a "6 years" / "3 years" figure rather than
  reading current values from the chapter file
- Treating monthly statements alone as sufficient to invoke the
  longer SOL
- Missing the affirmative-defense pleading requirement
- Missing the FDCPA parallel
