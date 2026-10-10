# co-draft-order — Proposed order with separated findings and ordering clause

## Prompt

My motion to compel discovery in Colorado District Court
was granted. The judge asked me to prepare a proposed
order. What does a Colorado proposed order look like, and
how do I get it to chambers?

## Expected triggers

- `co-draft-order`
- `co-statewide-format`
- `co-submit-order`

## Acceptance criteria

### Structure of a Colorado proposed order

- [ ] Separates the order into the standard Colorado
      parts:
      - **Recitals** ("The Court, having considered…")
      - **Findings** (numbered, keyed to the record —
        read the current Colorado practice from the
        `co-draft-order` skill references)
      - **Ordering clause** ("IT IS HEREBY ORDERED
        that…") — grants exactly the relief requested
        in the motion; no broader or narrower relief
      - **Signature and date lines** for the judge
- [ ] Notes the order carries the full two-block
      Colorado caption and document title
      (cross-reference `co-statewide-format`); the
      COURT USE ONLY box is present but left blank

### Word format + chambers transmittal

- [ ] States that proposed orders in Colorado are
      typically sent to chambers as a **Word document**
      (not a PDF) so the judge can edit — reads the
      per-judicial-district chambers practice from the
      `co-submit-order` skill references rather than
      asserting a universal rule
- [ ] Describes the **chambers transmittal email**
      protocol — attaching the Word file, referencing
      the case number and motion, copying all parties
      — reading per-JD contact practice from the
      references

### Agreed-form orders

- [ ] Notes the **agreed-form order** path: if both
      parties approve the language, the transmittal
      cover email states "approved as to form" by
      all parties, which often speeds entry

## Common failure modes

- Embeds the proposed order inside the motion brief
  instead of filing it as a separate document
- Sends a PDF instead of a Word document to chambers
- Grants relief broader than what the underlying
  motion requested
- Invents a chambers email address instead of reading
  per-JD practice from the references
