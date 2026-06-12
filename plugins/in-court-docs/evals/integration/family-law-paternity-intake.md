# Integration — Paternity + custody + child support intake (JP case, Lake County)

## Prompt

I'm the father of a 2-year-old. The mother and I were never
married and we've separated. She lives in Gary, I live in
Hammond — both in Lake County. I want to establish my
legal rights, get a custody order, and figure out what
child support will look like. I can't afford a lawyer
right now. Walk me through the whole process.

## Expected triggers

- `in-family-law`
- `in-family-court`
- `in-lake`
- `in-pro-se`
- `in-statewide-format`
- `in-deadlines`

## Acceptance criteria

### Forum and case type (in-lake + in-family-court)

- [ ] Identifies the case type as a **JP (paternity)**
      case under **IC 31-14** in the **Lake Superior
      Court Juvenile Division** or the Lake Circuit
      Court — reads the Lake County topology from
      `in-lake` / `in-family-court` rather than asserting
      specific division assignments from memory
- [ ] Notes Lake County's cause-number format
      (`45D0x-YYMM-JP-NNNNNN`) from `in-lake`

### Paternity establishment (in-family-law)

- [ ] Explains the two paths: (1) **paternity affidavit**
      executed at the hospital or through the State
      Department of Health, or (2) **judicial action**
      under IC 31-14 via a verified petition
- [ ] Notes that if a paternity affidavit was already
      signed at the hospital, paternity may already be
      legally established — explains the short rescission
      window (reads the rescission period from the corpus
      rather than asserting it from memory)
- [ ] If no affidavit, describes filing the verified
      petition and the genetic-testing process under
      IC 31-14-6 (threshold creates a rebuttable
      presumption — reads the threshold from the corpus)

### Custody and parenting time — IC 31-17

- [ ] States the best-interests framework under
      IC 31-17-2-8 and the rebuttable presumption
      historically favoring the biological mother for
      a non-marital child — notes the presumption is
      rebuttable on best-interests factors
- [ ] Notes the **Indiana Parenting Time Guidelines**
      as the default residential-time schedule; default
      schedules vary by age cohort (infant / toddler /
      school-age / adolescent)

### Child support — Indiana Child Support Guidelines

- [ ] States that child support is calculated under the
      **Indiana Child Support Guidelines** (an Indiana
      Supreme Court rule) using the income-shares model
      — identifies Worksheet A (sole custody) as the
      applicable worksheet
- [ ] Lists the calculation inputs: each parent's weekly
      gross income, guideline deductions to weekly
      adjusted gross income, combined income → look up
      basic obligation on the schedule → pro rata share
- [ ] Notes the combined-income cap above which the
      court has discretion (reads the current cap from
      the corpus rather than asserting it from memory)

### Pro se mechanics (in-pro-se + in-statewide-format)

- [ ] Identifies the fee-waiver option under IC 33-37-3-2
      for an income-qualifying petitioner
- [ ] Notes the T.R. 11(B) verification requirement on
      the IC 31-14 petition; pro se signature block
      (no Attorney Number)
- [ ] Notes the Odyssey optional e-filing path for
      self-represented litigants; if paper, service of
      the petition and summons under T.R. 4

## Common failure modes

- Directs the father to file a dissolution case (not
  applicable — the parents were never married; the
  case type is JP, not DR)
- Asserts a specific paternity-affidavit rescission
  period, genetic-testing threshold, or combined-income
  cap from memory without verifying against the corpus
- States Indiana Parenting Time Guidelines schedules
  as fixed day counts from memory
- Omits the fee waiver option for a self-represented
  litigant who cannot afford costs
