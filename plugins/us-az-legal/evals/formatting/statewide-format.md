# az-statewide-format — Ariz. R. Civ. P. 10 caption, signature, and line numbering

## Prompt

I'm self-represented in Arizona and about to file my first
document in Superior Court. What does the top of the page need to
look like — the caption, the line numbering, the signature at the
bottom? I want it to be accepted, not bounced for format.

## Expected triggers

- `az-statewide-format`
- `az-pro-se`

## Acceptance criteria

### Caption

- [ ] Describes the **Ariz. R. Civ. P. 10** caption: court
      identification, party names with designations, case number,
      and document title — read the exact layout from
      `az-statewide-format` / the references corpus rather than
      asserting margins/fonts from memory
- [ ] Notes the **line-numbered pleading paper** convention (numbered
      lines down the left margin) used in Arizona civil filings

### Signature and verification

- [ ] States the signature requirements — for a represented party
      the attorney's State Bar of Arizona number; for a
      self-represented party no bar number (cross-reference
      `az-pro-se`) — read the current rule from the corpus
- [ ] Notes where a certificate of service belongs and ties it to
      **Ariz. R. Civ. P. 5**

### Honest sourcing

- [ ] Reads page-layout specifics (margins, font, spacing, line
      numbering) from the references corpus rather than asserting
      fixed numbers from memory
- [ ] Cites Arizona authority by rule number (Ariz. R. Civ. P. 10,
      Rule 5) rather than generic "court rules"

## Common failure modes

- Asserts margin/font/spacing numbers from memory instead of the
  corpus
- Omits the line-numbering convention
- Adds a bar number to a self-represented signature block
