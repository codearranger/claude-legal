# wa-family-law — Child support calculation

## Prompt

I'm in a Washington dissolution. We have two kids (ages 6 and
9). My net monthly income is $4,200; my spouse's is $7,800.
The kids will live primarily with me. How is child support
calculated?

## Expected triggers

- `wa-family-law`
- `wa-family-court`

## Acceptance criteria

- [ ] Identifies Washington's income-shares model under RCW
      26.18 + 26.19
- [ ] References the **Washington Economic Table** at RCW
      26.19.020
- [ ] Walks combined-net-income calculation:
      $4,200 + $7,800 = $12,000
- [ ] **Checks the combined-income against the current Economic
      Table cap** (read from
      `wa-law-references/references/wa-rcw-debt/RCW-26_19.md`)
      — does NOT hard-code the cap figure
- [ ] References mandatory child-support worksheets (WSCSS)
- [ ] Each parent's pro rata share derived from the prompt:
      $4,200 / $12,000 = 35%; $7,800 / $12,000 = 65%
- [ ] References RCW 26.19.071 net-income definition (gross
      MINUS tax, FICA, mandatory pension, mandatory union,
      court-ordered support)
- [ ] Notes adjustments: health insurance, daycare,
      extraordinary medical (RCW 26.19.080)
- [ ] Notes potential residential-schedule deviation if
      shared residential time

## Common failure modes

- Hard-coding a specific cap figure rather than reading from
  the references corpus
- Forgetting the mandatory worksheet
- Using gross income (should be net)
- Mixing in another state's framework (e.g., percentage-of-payor
  model or 93-overnight rule)
