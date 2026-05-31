# az-family-law — Community-property division + legal decision-making

## Prompt

I'm getting divorced in Arizona. We have a house, two cars, and
some retirement accounts, plus a credit card in my name only. We
also have two kids. How does Arizona split property, am I on the
hook for that credit card, and how does the court decide custody?

## Expected triggers

- `az-family-law`
- `az-family-court`

## Acceptance criteria

### Community-property characterization and division

- [ ] Identifies Arizona as a **community-property** state and frames
      the property/debt analysis under **A.R.S. § 25-211** (property
      acquired during marriage is community property) and
      **A.R.S. § 25-318** (division of community property and debts
      on dissolution) — reads the current text/standard from
      `az-statutes-debt/` rather than asserting it
- [ ] Notes the **equitable (not necessarily equal) but generally
      substantially equal** division standard the court applies, and
      that debt incurred during marriage is generally community debt
      regardless of whose name is on it — read the rule from the
      corpus
- [ ] Distinguishes **separate property** (pre-marital, gift,
      inheritance) under the governing A.R.S. section read from the
      corpus

### Legal decision-making and parenting time

- [ ] Uses Arizona's **legal decision-making** terminology (not
      "custody") and frames the **best-interests** analysis under
      **A.R.S. § 25-403** — reads the statutory best-interests factors
      from the corpus rather than listing them from memory
- [ ] Notes parenting time and child support are determined under
      the related A.R.S. provisions / Arizona Child Support
      Guidelines (read the governing sections from the corpus)

### Forum / procedure

- [ ] Notes the matter proceeds under the **Arizona Rules of Family
      Law Procedure (ARFLP)**, not the ARCP (cross-reference
      `az-family-court`)

## Common failure modes

- Treats Arizona as an equitable-distribution (non-community-
  property) state
- Uses "custody" instead of legal decision-making, or lists the
  § 25-403 factors from memory
- Asserts the § 25-211 / § 25-318 standards from memory
- Applies the ARCP instead of the ARFLP to the dissolution
