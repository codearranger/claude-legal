# tx-statewide-format — Texas district-court petition format

## Prompt

What are the formatting rules for an original petition I'm filing in a
Texas district court? Caption, fonts, line numbering, footer — and
what has to be in the petition itself.

## Expected triggers

- `tx-statewide-format`

## Acceptance criteria

### Caption and pleading form

- [ ] Produces a Texas district-court caption: court name with the
      county (e.g., "IN THE __ JUDICIAL DISTRICT COURT OF __ COUNTY,
      TEXAS"), styled cause with **Plaintiff v. Defendant**, a cause-
      number line, and the document title
- [ ] States pleadings follow **TRCP 45** (plain statement, no
      technical forms) and **TRCP 47** form, with numbered allegations

### Rule 47(c) statement of relief (Texas quirk)

- [ ] Requires the petition to include the **TRCP 47(c) statement of
      the range of relief sought** (the damages-range tier), and notes
      that failure to plead the 47(c) range can bar a default judgment
      — reading the current tier thresholds from
      `../tx-law-references/references/civil-rules.md` /
      `tx-statutes-debt/` rather than hard-coding them

### Marketplace layout conventions

- [ ] Applies **line-numbered pleading paper by default**, with the
      docx `LineNumberRestartFormat.NEW_PAGE` recipe and the warning
      not to set `start` explicitly
- [ ] Includes the **footer** convention (document title left,
      `Page X of Y` via PAGE/NUMPAGES fields)

### Signature

- [ ] Provides a TRCP 57 signature block (and notes a pro-se filer
      signs without a State Bar of Texas bar number)

### Tooling

- [ ] Points to `scripts/format-check.py` to validate a generated
      `.docx`

## Common failure modes

- Omits the Rule 47(c) relief-range statement
- Hard-codes the 47(c) tier dollar figures instead of deferring to the
  corpus
- Forgets line numbering or the `Page X of Y` footer
- Uses "Complaint" instead of "Original Petition"
