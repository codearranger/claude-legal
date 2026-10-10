# tn-statewide-format — Chancery vs. Circuit caption variation

## Prompt

I'm filing a divorce complaint in Davidson County, Tennessee.
The Chancellor is hearing the case. How should the caption read?
How is that different from a Circuit Court caption in the same
county?

## Expected triggers

- `tn-statewide-format`
- `tn-davidson`
- `tn-family-court` (or `tn-family-law`)

## Acceptance criteria

### Court identifier line

- [ ] For **Chancery**: identifies the standard form as
      **"IN THE CHANCERY COURT FOR DAVIDSON COUNTY, TENNESSEE"**
      (or **"IN THE CHANCERY COURT OF DAVIDSON COUNTY,
      TENNESSEE"** — some clerks use "of"; both are acceptable
      but should match local conventions)
- [ ] For **Circuit**: identifies the corresponding line as
      **"IN THE CIRCUIT COURT FOR DAVIDSON COUNTY, TENNESSEE"**
- [ ] Notes that some divisions add the city tag ("AT
      NASHVILLE", "AT CHATTANOOGA") below the county/state line
- [ ] (Bonus) Cites the **20th Judicial District** designation,
      which some courts include below the court identifier

### Clerk identification

- [ ] Identifies the **Chancery clerk as the "Clerk & Master"**
      — a Tennessee-distinctive title for the Chancery clerk
      (a vestige of the older Master in Chancery role)
- [ ] Identifies the **Circuit clerk as the "Circuit Court
      Clerk"**
- [ ] Notes that pleadings filed in Chancery are filed with the
      Clerk & Master; pleadings in Circuit are filed with the
      Circuit Court Clerk

### Judicial title

- [ ] States that the **Chancery judge is the "Chancellor"** —
      another Tennessee-distinctive convention
- [ ] States that the **Circuit judge is the "Judge"** (or
      "Circuit Judge")
- [ ] Notes the addressing convention: "Chancellor [Last Name]"
      in Chancery; "Judge [Last Name]" in Circuit

### Caption mechanics

- [ ] Identifies the **Tenn. R. Civ. P. 10.01** core caption
      requirements: name of court, parties, file number,
      designation of the pleading
- [ ] Recognizes that the **right-side parenthetical column**
      (with closing parens for each line) is standard Tennessee
      style for both Chancery and Circuit
- [ ] Notes the docket-number space: typically left blank for
      first filing, filled in by the clerk on receipt

### Substantive jurisdiction distinction (bonus)

- [ ] Notes that **both** Chancery and Circuit have subject-
      matter jurisdiction over divorce in Tennessee (under
      Tenn. Code Ann. § 36-4-104), so the caption choice is a
      filing-strategy decision, not a jurisdictional necessity
- [ ] Notes Chancery is the **equity forum**, often preferred
      where injunctive relief / specific performance / equitable
      remedies are sought

## Common failure modes

- Writes "IN THE COURT OF CHANCERY" (incorrect — Tennessee uses
  "Chancery Court")
- Calls the Chancery clerk simply "Clerk" instead of "Clerk &
  Master"
- Calls the Chancellor "Judge" (close but not the convention)
- Mixes the two (e.g., addresses a Chancellor as Judge or vice
  versa)
- Asserts Circuit lacks subject-matter jurisdiction over divorce
  (false — both forums have concurrent jurisdiction)
- Treats the caption as identical between the two forums
- Omits the right-side parenthetical column
