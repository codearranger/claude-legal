# ga-draft-order — Proposed order with separated findings and ordering clause

## Prompt

My motion to compel discovery in the State Court of Cobb County was
granted. The judge asked me to prepare a proposed order. What does a
Georgia proposed order look like, and how do I get it to the judge?

## Expected triggers

- `ga-draft-order`
- `ga-statewide-format`
- `ga-submit-order`

## Acceptance criteria

### Structure of a Georgia proposed order

- [ ] Separates the order into the standard parts:
      - **Recitals** ("This matter came before the Court on …")
      - **Findings** (numbered, keyed to the record — read the current
        Georgia practice from the `ga-draft-order` skill references)
      - **Ordering clause** ("IT IS HEREBY ORDERED that …") — grants
        exactly the relief requested in the motion; no broader or
        narrower relief
      - **Signature and date lines** for the judge of the State Court of
        Cobb County
- [ ] Carries the full Georgia caption and document title
      (cross-reference `ga-statewide-format`) naming the court and
      "Civil Action File No."

### Submission to the court

- [ ] Describes how a proposed order is transmitted to chambers in
      Georgia — typically uploaded through the county e-filing system
      (PeachCourt for Cobb) and/or emailed to the judicial assistant in
      an editable format — reads the per-court transmittal practice from
      the `ga-submit-order` skill references rather than asserting a
      universal rule
- [ ] Notes copying all parties on the transmittal and referencing the
      case number and the motion being ruled on

### Consent / agreed-form orders

- [ ] Notes the **consent order** path: if both parties approve the
      language, the order or cover transmittal states it is submitted
      "by consent" / "approved as to form," which often speeds entry

## Common failure modes

- Embeds the proposed order inside the motion brief instead of a separate
  document
- Grants relief broader than what the underlying motion requested
- Invents a chambers email address instead of reading per-court practice
  from the references
- Mislabels the case number (uses a generic "Case No." instead of the
  Georgia "Civil Action File No.")
