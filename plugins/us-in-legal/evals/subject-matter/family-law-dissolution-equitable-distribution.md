# in-family-law — Dissolution + equitable-distribution framework

## Prompt

I'm filing for divorce in Indiana. My spouse and I have
been married 12 years. We have one child (age 8). We own
a house jointly. I inherited some stock from my mother
during the marriage. How does Indiana divide property,
and what's the case-type code?

## Expected triggers

- `in-family-law`
- `in-family-court`

## Acceptance criteria

- [ ] Identifies the case type as **DC — Dissolution with
      Children** (would be **DN** if no minor children)
- [ ] Identifies Indiana as an **equitable-distribution**
      state under IC 31-15-7 — NOT community property
- [ ] Notes the **rebuttable presumption of equal
      division** under IC 31-15-7 (presumption rebutted
      by application of statutory factors)
- [ ] Identifies the divisible pool: Indiana includes
      **both marital AND non-marital property** in the
      pool (subject to characterization arguments under
      the contribution / acquisition factors)
- [ ] References the **rebuttal factors** at IC 31-15-7
      (contributions, economic circumstances, dissipation,
      conduct, tax consequences, earnings, etc.) — points
      at `in-law-references/references/in-statutes-debt/
      IC-31-15.md` for the current factor enumeration
      rather than embedding the list
- [ ] Applies framework to the inherited stock: inherited
      property received during marriage may be subject to
      the equitable-distribution analysis under the
      contribution / acquisition factors; the answer is
      fact-dependent (commingling, source-of-funds, how
      title was held). Avoids stating that inheritance is
      automatically excluded (which would be community-
      property-state reasoning)
- [ ] Walks dissolution procedural framework: verified
      petition, service under Trial Rule 4, mandatory
      waiting period (read current period from IC-31-15.md),
      mandatory financial disclosures, provisional orders,
      potential mediation per county local rule, final
      hearing → Decree
- [ ] References Indiana Child Support Guidelines (court
      rule) for support calculation given the minor child
- [ ] References Indiana Parenting Time Guidelines (court
      rule) for default parenting time

## Common failure modes

- Treating Indiana as community property
- Treating inheritance as automatically off-limits (that's
  community-property-state reasoning)
- Hard-coding the residency / waiting-period day count
- Using DR (Domestic Relations Miscellaneous) instead of
  DC for the initial dissolution filing
- Missing the rebuttable-equal-division presumption
- Skipping the divisible-pool-includes-non-marital-property
  doctrine
