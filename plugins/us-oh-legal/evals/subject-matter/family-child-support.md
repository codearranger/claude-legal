# oh-family-law — Child support calculation

## Prompt

I'm in an Ohio Common Pleas divorce. We have one child
(8 years old, lives primarily with me). My income is
$45,000; my spouse's income is $85,000. How is child
support calculated?

## Expected triggers

- `oh-family-law`
- `oh-family-court`

## Acceptance criteria

- [ ] Identifies Ohio as an **income-shares** state under
      **R.C. Chapter 3119**
- [ ] References the **R.C. 3119.022 worksheet**
- [ ] Walks combined-gross-income calculation:
      $45k + $85k = $130k
- [ ] Notes **$300,000 combined-income cap** at R.C.
      3119.04 (here, well below cap)
- [ ] References R.C. 3119.021 basic support schedule
- [ ] Notes health-insurance / childcare adjustments
      (R.C. 3119.30, R.C. 3119.302)
- [ ] Notes **parenting-time deviation** under R.C.
      3119.231 if extended parenting time
- [ ] Notes **CSEA** administrative review every 36
      months under R.C. 3119.60-79

## Common failure modes

- Applying percentage-of-payor model (Texas / WI)
- Applying community-property concept (Ohio is equitable
  distribution, but that's a property concept, not a
  support concept)
- Missing the $300k cap
- Missing CSEA administrative path
