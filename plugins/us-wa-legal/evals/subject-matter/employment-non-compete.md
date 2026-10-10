# wa-employment — Non-compete enforceability under RCW 49.62

## Prompt

My Washington employer wants me to sign a 2-year non-compete
preventing me from working anywhere in the U.S. for any
competitor. I make $80,000 a year. Is it enforceable?

## Expected triggers

- `wa-employment`

## Acceptance criteria

- [ ] Identifies **RCW 49.62** non-compete reform (effective 2020)
- [ ] Identifies the salary-threshold rule: non-compete VOID below
      a COL-adjusted statutory threshold; the threshold is reset
      annually under RCW 49.62.020
- [ ] **Reads the current threshold from
      `wa-law-references/references/wa-rcw-debt/RCW-49_62.md`**
      (or notes the L&I-published current figure) — does NOT
      hard-code a dollar figure
- [ ] Compares the $80k salary in the prompt against the **current**
      threshold and reaches the correct conclusion
- [ ] Even if above threshold:
      - Maximum duration presumed reasonable (current period in
        chapter file)
      - Must be disclosed at offer OR supported by independent
        consideration
      - Layoff-trigger automatic invalidation if employee receives
        less than base salary in severance
- [ ] Notes damages for attempted enforcement (current multiplier
      and fee-shifting in chapter file)
- [ ] Notes restrictions on non-solicitation / anti-moonlighting
      also covered

## Common failure modes

- Treating non-competes as generally enforceable in WA
- Hard-coding a year-specific threshold rather than checking the
  references corpus
- Missing the damages-for-attempted-enforcement provision
- Confusing with restrictive covenants other than non-competes
