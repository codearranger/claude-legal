# id-statewide-format — I.R.C.P. 2 form of documents

## Prompt

What are the formatting rules for a document I'm filing in an Idaho
District Court? Paper, font, margins, spacing — and where does the
rule live?

## Expected triggers

- `id-statewide-format`

## Acceptance criteria

### Correct rule sourcing

- [ ] States that Idaho's statewide format spec lives in **I.R.C.P. 2**
      (form of documents / caption), with **I.R.C.P. 10** governing the
      form of pleadings (numbered paragraphs) and **I.R.C.P. 11** the
      signature — does NOT attribute the format spec to Rule 10 alone
- [ ] Reads the specific margin / font / spacing figures from the
      court-rules corpus rather than reciting them as memorized
      constants, while it may summarize: letter paper, a minimum font
      size, double or one-and-one-half spacing, larger top/side
      margins than bottom, title of court set down from the top of
      page 1, and the document title at the foot of each page

### Marketplace layout conventions

- [ ] Applies **line-numbered pleading paper by default**, with the
      docx `LineNumberRestartFormat.NEW_PAGE` recipe and the warning
      not to set `start` explicitly
- [ ] Includes the **footer** convention (document title left,
      `Page X of Y` via PAGE/NUMPAGES fields)
- [ ] Handles the page-1 top margin (title of court set down from the
      top) via a two-section layout or a leading-spacing paragraph,
      setting line numbering on both sections if two are used

### Tooling

- [ ] Points to `scripts/format-check.py` to validate a generated
      `.docx` against the I.R.C.P. 2 baseline

## Common failure modes

- Says the format rule is "Rule 10" and omits Rule 2
- Hard-codes margin/font numbers without deferring to the corpus
- Forgets line numbering or the Page X of Y footer
