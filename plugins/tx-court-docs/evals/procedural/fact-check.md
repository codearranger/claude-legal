# tx-fact-check — verifying Texas citations

## Prompt

Before I file my Texas brief, can you check my citations? I cited a
Texas Supreme Court case and a court-of-appeals case, and I want the
formats right.

## Expected triggers

- `tx-fact-check`

## Acceptance criteria

### Reporter + court conventions

- [ ] Confirms Texas cases are cited to the **South Western Reporter**
      (S.W.3d / S.W.2d) because Texas abolished its official Texas
      Reports
- [ ] For a **Supreme Court of Texas** case, uses the `(Tex. [year])`
      court-and-year parenthetical
- [ ] For a **court of appeals** case, requires the **district** in the
      parenthetical (e.g., `(Tex. App.—Dallas [year], ...)`) **and** the
      **petition-history parenthetical** (`pet. denied` / `pet. ref'd` /
      `no pet.` etc.) — flags that omitting the writ/petition history is
      a defect

### Two courts of last resort

- [ ] Demonstrates awareness that Texas has **two courts of last
      resort** — the Supreme Court of Texas (civil) and the Court of
      Criminal Appeals (criminal) — and applies the civil one for a
      civil brief

### Verification posture

- [ ] Checks citation **form** against
      `../tx-law-references/references/citation-format.md`, and routes
      verification of whether a case **exists / is good law** to
      case-law research (CourtListener / Legal Data Hunter) rather than
      vouching for a holding from memory

## Common failure modes

- Cites to "Tex." reporter or invents a Texas Reports citation
- Omits the court-of-appeals district or the petition-history
  parenthetical
- Treats the Court of Criminal Appeals as the civil court of last resort
