# Integration — end-to-end Idaho divorce intake

## Prompt

I want to file for divorce in Bonneville County, Idaho. We have two
kids. Where do I file, what rules apply, and what do I need to get
started?

## Expected triggers

- `id-family-court`
- `id-family-law`
- `id-bonneville`

## Acceptance criteria

### Forum and rules

- [ ] Routes the case to the **Magistrate Division of the District
      Court, Seventh Judicial District, Bonneville County** (Idaho
      Falls)
- [ ] States the proceeding is governed by the **Idaho Rules of Family
      Law Procedure (I.R.F.L.P.)**, a separate rule set from the
      I.R.C.P., and uses the I.R.F.L.P. 208 document form

### Substance

- [ ] Identifies divorce grounds (irreconcilable differences,
      **I.C. § 32-610**) and the **community-property** framework
      (**I.C. § 32-906**)
- [ ] Explains child support runs on the **Idaho Child Support
      Guidelines (I.R.F.L.P. 120)** income-shares model and custody on
      the best-interests standard (**I.C. § 32-717**) — without
      hard-coding guideline dollar figures (read from references)
- [ ] Flags the reconciliation/waiting mechanics without asserting a
      precise day count (verify current period)

### Getting started

- [ ] Points to Idaho self-help resources (Idaho Court Assistance
      Office / Odyssey "Guide & File") and the petition + mandatory
      financial disclosures
- [ ] Uses Petitioner/Respondent and an "In re the Marriage of"
      caption

## Common failure modes

- Applies the I.R.C.P. instead of the I.R.F.L.P.
- Treats Idaho as equitable-distribution
- Hard-codes a child-support number or an exact waiting period
