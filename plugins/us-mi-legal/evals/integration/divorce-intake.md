# Integration — Divorce intake in the Family Division

## Prompt

I want to file for divorce in Michigan. We have two minor kids
and we've lived in the state for years. I can't afford a lawyer
so I'm doing this myself. Where do I file, what's the process
and timeline, and how do I make sure my paperwork is formatted
right and on time?

## Expected triggers

- `mi-family-court`
- `mi-family-law`
- `mi-pro-se`
- `mi-statewide-format`
- `mi-deadlines`

## Acceptance criteria

### Forum and filing (mi-family-court)

- [ ] Identifies the **Family Division of the Circuit Court** as
      the forum for divorce and that the matter is commenced by a
      **complaint for divorce**
- [ ] Notes the **residency / venue requirements** for filing —
      cite the controlling statute (MCL 552.9) and **read the
      current residency-period requirements from the references
      corpus** rather than asserting them from memory
- [ ] Points to the relevant **SCAO family-law forms** (read the
      current catalog/pointers from the corpus rather than
      asserting form numbers)

### Substance (mi-family-law)

- [ ] States Michigan is a **no-fault** divorce state and reads
      the statutory grounds language from the corpus
- [ ] Flags the issues the case must address: **property
      division** (equitable distribution), **child custody**
      under the **MCL 722.23 best-interest factors**, **parenting
      time**, and **child support** under the Michigan Child
      Support Formula — reading specifics (factors, formula
      pointers) from the corpus rather than asserting them

### Timeline (mi-deadlines)

- [ ] Identifies the **statutory waiting period** before a
      divorce judgment may enter (longer where there are minor
      children) — cite the controlling statute (MCL 552.9f) and
      **read the current waiting periods from the corpus** rather
      than asserting the day/month counts from memory
- [ ] Applies **MCR 1.108** time computation and the Michigan
      legal-holiday roll-forward to any computed deadlines

### Pro se + formatting (mi-pro-se / mi-statewide-format)

- [ ] Self-represented signature block (no P-number); MCR 1.109(E)
- [ ] Caption / format per **MCR 1.109 / MCR 2.113**; flags
      **MCR 1.109(D)(9)** PII handling for documents containing
      children's identifiers and financial information

## Common failure modes

- Files in the wrong court (treats divorce as a general civil
  matter rather than the Family Division)
- Asserts residency periods or the divorce waiting period from
  memory instead of reading MCL 552.9 / 552.9f from the corpus
- Recites or invents the MCL 722.23 best-interest factors rather
  than reading them from the corpus
- Misses the SCAO family-law forms or the MCR 1.109(D)(9) PII
  handling for child/financial data
