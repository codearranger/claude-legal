# wa-family-law — Dissolution waiting period + community property

## Prompt

My spouse and I are filing for divorce in King County. We were
married 12 years, own a house jointly, and I inherited some
stock from my mother during the marriage. How does Washington
divide property, and when can we get a final decree?

## Expected triggers

- `wa-family-law`
- `wa-family-court`
- `wa-kcsc`

## Acceptance criteria

- [ ] Identifies **90-day mandatory waiting period** between
      filing and final decree under RCW 26.09.030
- [ ] Identifies Washington as a **community-property state**
      under RCW 26.16 (NOT equitable distribution)
- [ ] Explains community property = property acquired during
      marriage with community labor / income
- [ ] Explains separate property = pre-marital + gifts +
      inheritance (the inherited stock = separate)
- [ ] Explains RCW 26.09.080 "just and equitable" division
      considering nature/extent of community AND separate
      property
- [ ] Notes that under RCW 26.09.080 the court CAN award
      separate property to the non-owning spouse to achieve
      just-and-equitable result (key distinction from common-
      law / equitable-distribution states)
- [ ] Notes commingling risk — if separate stock was sold and
      proceeds mixed with community funds, may lose separate
      character

## Common failure modes

- Calling WA an "equitable distribution" state
- Treating inheritance as automatically community property
- Missing the 90-day waiting period
- Stating separate property is "off-limits" (it's not)
