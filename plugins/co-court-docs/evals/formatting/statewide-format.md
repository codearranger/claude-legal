# co-statewide-format — C.R.C.P. 10 + CJD 11-01 two-block caption with COURT USE ONLY box

## Prompt

I'm filing a motion in Colorado District Court for the first
time. What does the top of the document need to look like —
the caption, the font, the margins, the two boxes I've seen
on Colorado court forms? I want it accepted, not bounced for
format.

## Expected triggers

- `co-statewide-format`
- `co-pro-se`

## Acceptance criteria

### The two-block Colorado caption

- [ ] Describes the **Colorado flexible caption**: a
      **left-hand block** (court identification, case name,
      case number, division, courtroom) and a **right-hand
      "COURT USE ONLY" block** (for the clerk's stamp) —
      read the current layout requirements from the
      `co-statewide-format` skill / CJD 11-01 references
      rather than asserting exact column widths from memory
- [ ] Notes the document **title** appears below the caption
      block, and is not embedded in the caption itself

### Typography and page layout

- [ ] States the **C.R.C.P. 10 + CJD 11-01** requirements:
      **1-inch margins** on all sides, **double-spaced** body
      text, **12-point** minimum font — read current figures
      from the references corpus rather than asserting them
      from memory
- [ ] Notes the **line-numbering** convention (numbered lines
      down the left margin) that is standard Colorado civil
      practice

### Signature block

- [ ] Identifies where the signature block goes; for a
      self-represented party, no Atty. Reg. # is required
      (cross-reference `co-pro-se`); for an attorney, the
      Colorado **Attorney Registration Number** must appear
- [ ] Notes that a **certificate of service** appears at the
      end of the document under C.R.C.P. 5

### Honest sourcing

- [ ] Reads page-layout specifics (margins, font size,
      spacing, line-numbering) from the references corpus;
      cites the controlling authority as **C.R.C.P. 10**
      and **CJD 11-01**, not generic "court rules"

## Common failure modes

- Asserts fixed margin/font/spacing numbers from memory
  without corpus support
- Describes a single-block caption (misses the COURT USE
  ONLY right-hand box)
- Adds an Attorney Reg. # to a self-represented signature
  block
- Omits the certificate of service requirement
