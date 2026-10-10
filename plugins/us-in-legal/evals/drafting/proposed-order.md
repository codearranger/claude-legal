# in-draft-order — Indiana proposed order for judge signature

## Prompt

I just argued my motion to dismiss in Marion Superior Court
and the judge said "prepare an order." What does an Indiana
proposed order look like, what sections does it need, and
how do I get it to the judge?

## Expected triggers

- `in-draft-order`
- `in-marion`
- `in-submit-order`
- `in-statewide-format`

## Acceptance criteria

### Document form

- [ ] Identifies the document as a **proposed order**
      (the judge signs the proposed order to make it
      final) — separate from the motion itself
- [ ] Notes that Marion County practice requires a
      proposed order to accompany **every motion** at
      filing — not only at the argument stage (reads the
      Marion local rule from `in-marion` rather than
      asserting the specific rule number from memory)

### Caption

- [ ] Caption follows T.R. 10(A); document title clearly
      labeled: "ORDER GRANTING DEFENDANT'S MOTION TO
      DISMISS" (or the relevant title)
- [ ] Cause number, judge's name line (e.g., "HON.
      ________________, JUDGE"), and courtroom division
      included

### Body structure

- [ ] **Findings clause** (if needed): "The Court having
      considered…" or "The Court, having reviewed the
      motion, briefs, and arguments of counsel, and being
      duly advised in the premises…"
- [ ] **Ordering clause**: "IT IS THEREFORE ORDERED,
      ADJUDGED, AND DECREED that:" followed by numbered
      specific relief paragraphs
- [ ] Signature block: judge's signature line + date line
      (no party signature on the order itself)
- [ ] Separates findings from ordering clause clearly

### Transmittal — in-submit-order

- [ ] Describes how to transmit the proposed order to
      the judge: Marion practice is to upload the
      proposed order through **Odyssey** as a separate
      document type ("Proposed Order") after the hearing,
      or to email the judge's chambers per the assigned
      courtroom's practice — reads the Marion-specific
      transmittal protocol from `in-marion` / `in-submit-
      order` rather than asserting a fixed method

### Format

- [ ] T.R. 5(E) format; double-spaced; 12-pt serif;
      no party signature required — the judge signs

## Common failure modes

- Combines the order and the motion into a single document
- Omits the ordering clause or writes a vague ordering
  clause ("IT IS SO ORDERED")
- Adds a party signature block to the order
- Fails to flag that Marion practice requires proposed
  orders with every motion, not just after argument
- Asserts the specific Marion local rule citation from
  memory instead of the corpus
