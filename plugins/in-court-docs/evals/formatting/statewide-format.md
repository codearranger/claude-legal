# in-statewide-format — Trial Rule 5(E) format + T.R. 10(A) caption

## Prompt

I'm filing my first motion in an Indiana court. I'm not
represented by a lawyer. What does the top of the page need
to look like — the court name, the parties, the cause number,
the margins, the font, and the signature at the bottom? I
want the clerk to accept it, not bounce it.

## Expected triggers

- `in-statewide-format`
- `in-pro-se`

## Acceptance criteria

### Caption — T.R. 10(A)

- [ ] Produces the correct Indiana caption structure:
      STATE OF INDIANA / court name line / county line,
      then parties stacked on the left with the `)` chain
      down the right, cause number in the right column —
      reads the exact layout from `in-statewide-format`
      rather than asserting it from memory
- [ ] Uses **"v."** (not "vs.") between parties — Indiana
      citation convention
- [ ] Correctly formats the cause number: two-digit county
      code + D/C + court number + YYMM + case-type code +
      sequence (e.g., `49D01-2503-PL-001234`) — explains
      the encoding rather than inventing a number

### Page format — T.R. 5(E)

- [ ] States the T.R. 5(E) requirements: 8½ × 11 white
      paper, one side only; reads current margin and font
      specs from the corpus rather than asserting fixed
      numbers from memory
- [ ] Notes the **2-inch top margin on page 1** (to clear
      the Odyssey e-filing clerk stamp / banner) and
      1-inch margins elsewhere
- [ ] Notes the **12-pt minimum serif font** and
      double-spaced body text requirements

### Paragraph numbering — T.R. 10(B)

- [ ] States that T.R. 10(B) requires **numbered
      paragraphs** for all averments of claim or defense;
      notes this is distinct from line-numbered pleading
      paper (which is a marketplace convention, not an
      Indiana rule requirement)

### Signature — T.R. 11(A) pro se block

- [ ] Produces the correct pro se signature block: party
      name + "Pro Se" designation, address, telephone,
      email — **no Attorney Number** (that would be
      required only for counsel)
- [ ] Notes T.R. 11(B) verification ("I affirm, under the
      penalties for perjury…") when the document is a
      verified pleading or declaration

### Certificate of Service — T.R. 5(B)

- [ ] States that every filing other than the initial
      complaint must include a **Certificate of Service**
      at the end; notes that Odyssey auto-serves
      registered counsel but the certificate should still
      appear in the document body

## Common failure modes

- Asserts specific margin/font numbers from memory instead
  of the corpus
- Uses "vs." instead of "v."
- Adds an Attorney Number to a pro se signature block
- Confuses numbered paragraphs (T.R. 10(B)) with the
  optional left-margin line-numbering convention
- Omits the Certificate of Service from a responsive
  filing
