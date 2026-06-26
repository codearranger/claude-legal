# ga-cobb — Cobb County caption + PeachCourt e-filing + Cobb standing orders

## Prompt

I have a civil debt case to file in Cobb County, Georgia. What goes in
the caption, how do I e-file it, and is there anything Cobb-specific I
should know?

## Expected triggers

- `ga-cobb`
- `ga-statewide-format`
- `ga-file-packet`

## Acceptance criteria

### Caption (Cobb specifics)

- [ ] Confirms the caption follows the O.C.G.A. § 9-11-10 layout and
      names the correct court line — for a debt action, the **STATE COURT
      OF COBB COUNTY / STATE OF GEORGIA** (debt-collection suits are filed
      in State Court, not Superior Court; cross-reference
      `ga-state-court`); for a Superior-court matter, **SUPERIOR COURT OF
      COBB COUNTY / STATE OF GEORGIA**
- [ ] Uses **"Civil Action File No."** as the file-number label
- [ ] Notes the **Cobb Judicial Circuit** is a single-county circuit and
      reads the current judge/division-assignment practice from the skill
      references rather than asserting a specific judge or division

### PeachCourt e-filing

- [ ] Identifies **PeachCourt** as Cobb County's e-filing platform (Cobb
      uses PeachCourt, **not** Odyssey eFileGA) and notes civil e-filing
      in Cobb Superior Court is mandatory — reads the current effective
      date / scope from the references rather than asserting it from memory
- [ ] Notes PeachCourt auto-generates the case-initiation documents
      (case initiation form, disclosure, summons, sheriff's entry of
      service) and, in domestic cases, auto-attaches the domestic standing
      order

### Cobb-specific practice

- [ ] Notes Cobb has **no business court** (no MABCD enrollment) and that
      magistrate civil matters are subject to the § 15-10-2(5) cap — reads
      the current cap from the corpus rather than asserting a dollar figure
- [ ] Reads any Cobb standing-order or chambers conventions from the
      `ga-cobb` skill references rather than inventing local rules

## Common failure modes

- Writes the court as a generic "Cobb County Court" instead of the
  precise "STATE COURT OF COBB COUNTY / STATE OF GEORGIA" (or Superior)
- Routes Cobb filings to Odyssey eFileGA instead of PeachCourt
- Files a routine debt suit in Superior Court instead of State Court
- Uses "Case No." instead of "Civil Action File No."
