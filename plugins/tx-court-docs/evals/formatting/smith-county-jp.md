# tx-smith-county-jp — Smith County Justice Court caption + posture

## Prompt

I'm filing in a Smith County, Texas Justice Court — it's a debt-claim
case in Precinct 1. How do I caption it and what's different about
filing in a JP court versus district court?

## Expected triggers

- `tx-smith-county-jp`
- `tx-justice-courts`
- `tx-statewide-format`

## Acceptance criteria

### Venue layering

- [ ] Recognizes `tx-smith-county-jp` **layers on** `tx-justice-courts`
      (the statewide TRCP 500–510 framework) and `tx-statewide-format`
- [ ] Captions for a **Smith County Justice Court, Precinct 1** (Justice
      of the Peace court), identifying the county seat as **Tyler** and
      confirming the current precinct/place layout against the corpus
      rather than asserting a fixed precinct count from memory

### Justice-court posture (the quirk)

- [ ] States that under **TRCP 500.3(e)** the other Rules of Civil
      Procedure and the **Rules of Evidence do NOT apply** in Justice
      Court except where Part V (Rules 500–510) specifically
      incorporates them
- [ ] Identifies a **debt-claim case** as governed by **TRCP 508** and
      that the JP court hears small/debt claims up to a statutory
      ceiling (reading the current ceiling from
      `../tx-law-references/references/tx-statutes-debt/` /
      `civil-rules.md`, not hard-coding it)
- [ ] Notes filing through **eFileTexas.gov** and that appeals from a
      JP court go **de novo to the county court** (TRCP 506) on an
      appeal bond, cash deposit, or Statement of Inability to Afford
      Payment

### Form

- [ ] Applies the simplified JP pleading posture (plain statement; no
      technical forms) rather than imposing full district-court motion
      practice

## Common failure modes

- Captions it as a district or county court
- Applies the full Rules of Evidence / Civil Procedure in JP court
- Hard-codes the current JP jurisdictional ceiling
- Says JP appeals go to a court of appeals instead of de novo to county
  court
