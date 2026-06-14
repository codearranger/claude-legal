# co-file-packet — CCEFS e-filing assembly + JDF 205/206 fee waiver

## Prompt

I've finished drafting my motion and supporting declaration
in Colorado District Court. I need to file them through the
Colorado e-filing system. Walk me through assembling the
packet, picking the right document codes, and what to do
if I can't afford the filing fee.

## Expected triggers

- `co-file-packet`
- `co-statewide-format`
- `co-pro-se`

## Acceptance criteria

### CCEFS upload workflow

- [ ] Identifies **CCEFS** (Colorado Courts E-Filing
      System) as the statewide mandatory e-filing
      platform for represented parties — reads the
      current document-type / document-code selection
      step from the skill references rather than
      inventing codes from memory
- [ ] Notes that each document in the packet (motion,
      declaration, proposed order) is filed as a
      **separate attachment** with its own document
      code, not concatenated into one PDF

### Document packet preflight

- [ ] Runs a format check before upload: two-block
      caption present, COURT USE ONLY box, correct
      font/margin/spacing, line numbering, certificate
      of service attached
- [ ] Confirms the **proposed order** is a separate
      document (cross-reference `co-draft-order`) and
      carries the correct document code

### Filing fees + fee waiver

- [ ] Identifies the correct filing-fee schedule for
      the action type under **C.R.S. art. 32 of title
      13** — reads the current fee amounts from the
      references corpus rather than asserting dollar
      figures from memory
- [ ] Routes the indigent filer to **JDF 205 (Motion
      to File Without Payment of Fees)** and
      **JDF 206 (Order re: Motion to File Without
      Payment of Fees)** and notes the income-
      eligibility standard — reads current thresholds
      from the corpus

### Pro-se filing path

- [ ] Notes the **CCEFS Pro Se** track for
      self-represented litigants and, where CCEFS is
      not yet available, the paper-filing alternative
      — cross-references `co-pro-se`

## Common failure modes

- Asserts specific CCEFS document codes from memory
- Tells the filer to combine all documents into one
  PDF instead of filing them separately
- States filing-fee dollar amounts from memory
- Ignores the JDF 205/206 fee-waiver path
