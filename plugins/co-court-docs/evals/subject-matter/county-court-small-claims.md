# co-county-courts — County court + C.R.C.P. 311 simplified procedure + small claims

## Prompt

Someone is suing me for about $3,500 in a Colorado county
court, not a district court. I've never dealt with county
court before. How is it different from district court, what
rules apply, and is there a small-claims option for this
kind of dispute?

## Expected triggers

- `co-county-courts`
- `co-first-30-days`
- `co-statewide-format`

## Acceptance criteria

### Jurisdictional split

- [ ] States the **county court vs. district court**
      split: county court handles civil claims up to the
      statutory limit — reads the **current
      jurisdictional threshold** from the references
      corpus rather than asserting a dollar figure from
      memory; confirms that $3,500 falls within county
      court jurisdiction

### C.R.C.P. 311 simplified procedure

- [ ] Identifies **C.R.C.P. 301–411** (county-court
      civil rules) as the governing procedure —
      specifically noting the **simplified discovery**
      under C.R.C.P. 311 (no C.R.C.P. 26(a)(1) initial
      disclosures, more limited discovery than district
      court) — reads the current scope from the corpus
- [ ] Notes that C.R.C.P. 10 + CJD 11-01 format
      requirements still apply in county court

### Small claims (C.R.C.P. 501–521)

- [ ] Identifies the **small-claims** track under
      **C.R.C.P. 501–521** for claims at or below the
      small-claims jurisdictional limit — reads the
      **current dollar cap** from the references corpus
      rather than asserting a number from memory
- [ ] Notes the key small-claims features: informal
      procedure, no attorneys without court permission,
      limited discovery, judge decides based on
      informal hearing — reads current specifics from
      the corpus

### Caption and format

- [ ] Confirms the same Colorado two-block caption
      applies in county court, including the COURT USE
      ONLY box (cross-reference `co-statewide-format`)
- [ ] Notes the court name line: "County Court,
      [County] County, State of Colorado" (not
      "District Court")

## Common failure modes

- States the county court jurisdictional cap as a
  fixed number from memory instead of the corpus
- States the small-claims cap as a fixed number
  from memory instead of the corpus
- Applies full C.R.C.P. 26-37 discovery to a county
  court case instead of the C.R.C.P. 311 simplified
  regime
- Writes "District Court" in the caption instead of
  "County Court"
