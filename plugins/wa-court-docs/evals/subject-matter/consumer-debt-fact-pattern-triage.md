# wa-consumer-debt — Fact-pattern triage

## Prompt

I just got sued in Washington by "Velocity Investments LLC."
The complaint says I owe $4,800 on a credit-card account
originally with Wells Fargo. The complaint attaches a
"Certificate of Indebtedness" and a generic "Bill of Sale" but
not the cardholder agreement. The last payment was about 5
years ago. What kind of case is this?

## Expected triggers

- `wa-consumer-debt`
- `wa-first-30-days`

## Acceptance criteria

- [ ] Recognizes this as a **debt-buyer** case (Velocity is a
      well-known debt buyer, not an original creditor)
- [ ] Matches against the recurring fact patterns in
      `wa-consumer-debt/references/fact-patterns.md`:
      pattern 1 (generic pool schedule), pattern 2 (missing
      statements), pattern 3 (no cardholder agreement),
      possibly pattern 5 (SOL trap given the 5-year lookback)
- [ ] Flags the **5-year-from-last-payment SOL question** —
      whether facially time-barred depends on whether the
      longer (written contract) or shorter (oral / account-
      stated) WA SOL applies; that turns on whether the
      cardholder agreement is in evidence
- [ ] Suggests answer + counterclaim posture: SOL defense (if
      plaintiff lacks cardholder agreement, shorter SOL likely
      applies); chain-of-title challenge; FDCPA counterclaim;
      WA CPA counterclaim
- [ ] Identifies first-wave discovery targets: complete chain;
      original cardholder agreement; all monthly statements;
      affidavit of debt's foundation
- [ ] Pulls current WA SOL day counts from
      `wa-law-references/references/wa-rcw-debt/RCW-4_16.md`
      rather than hard-coding

## Common failure modes

- Treating Velocity as an original creditor
- Hard-coding a specific WA SOL figure
- Missing the chain-of-title issue
- Skipping the FDCPA / WA CPA counterclaim posture
