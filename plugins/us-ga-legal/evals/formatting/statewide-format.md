# ga-statewide-format — O.C.G.A. § 9-11-10 caption + USCR practice + marketplace baseline

## Prompt

I'm filing a motion in a Georgia court for the first time. What does the
top of the document need to look like — the caption, the court name, the
case number, the font and margins? I want it accepted, not bounced.

## Expected triggers

- `ga-statewide-format`
- `ga-pro-se`

## Acceptance criteria

### The Georgia caption (O.C.G.A. § 9-11-10)

- [ ] Describes the **O.C.G.A. § 9-11-10(a)** caption requirements — the
      name of the **court** and **county**, the **title of the action**
      (parties), the **file number**, and the designation under
      § 9-11-7(a) — and reads the current layout from the
      `ga-statewide-format` skill references rather than asserting a fixed
      box layout from memory
- [ ] Uses **"Civil Action File No."** as the Georgia file-number label
      (not a generic "Case No.")
- [ ] Uses the correct party designations: **Plaintiff / Defendant** for
      civil actions; **Petitioner / Respondent** for divorce/family
      matters
- [ ] Notes the document **title** appears below the caption

### Typography and page layout (marketplace baseline)

- [ ] Notes that Georgia has **no single statewide pleading-paper rule**;
      practice flows from O.C.G.A. § 9-11-10/11 plus the Uniform Superior
      Court Rules (and the parallel State / Magistrate court rules)
- [ ] Applies the marketplace format baseline — US Letter, 1-inch
      margins, 12-point serif or Arial, double-spaced body, footer with
      title and page number — reading current figures from the references
      corpus rather than asserting them from memory

### Signature block

- [ ] For a self-represented party, the block shows name/address/phone/
      email and **"Pro Se"** with **no Georgia Bar No.** (cross-reference
      `ga-pro-se`); an attorney block carries the **Georgia Bar No.**
- [ ] Notes a **certificate of service** appears at the foot under
      O.C.G.A. § 9-11-5

## Common failure modes

- Asserts a single statewide pleading-paper rule for Georgia (there is
  none)
- Uses a generic "Case No." instead of "Civil Action File No."
- Adds a Georgia Bar No. to a self-represented signature block
- Asserts fixed margin/font numbers from memory without corpus support
