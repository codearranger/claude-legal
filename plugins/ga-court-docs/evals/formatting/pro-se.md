# ga-pro-se — Self-represented party workflows, forms, and fee waivers

## Prompt

I can't afford a lawyer and want to represent myself in a Georgia civil
case. How do I sign and file documents, do I need official forms, and
what if I can't afford the filing fee?

## Expected triggers

- `ga-pro-se`
- `ga-statewide-format`
- `ga-file-packet`

## Acceptance criteria

### Self-represented designation and signature

- [ ] Explains the **"Pro Se" / Self-Represented** signature block (name,
      address, phone, email; **no Georgia Bar No.**) and that the litigant
      signs in their own name under O.C.G.A. § 9-11-11
- [ ] Notes the **same § 9-11-10 caption and USCR practice** apply to
      self-represented filings as to attorney filings; no relaxed format
      standard

### Forms and e-filing

- [ ] Identifies the Georgia forms sources — GSCCCA / Council of Superior
      Court Judges forms and county clerk packets (e.g., GSCCCA SC-15 /
      SC-16 for family-violence protective orders) — and reads the catalog
      scope from the skill references rather than asserting which specific
      form is mandatory from memory
- [ ] Notes the county-dependent e-filing platform (**PeachCourt** for
      Cobb/Gwinnett-area Superior; **Odyssey eFileGA** for Fulton and
      Gwinnett State/Superior) and that self-represented filers may use
      the e-filing portal or, where allowed, paper (cross-reference
      `ga-file-packet`)

### Fee waivers (in forma pauperis)

- [ ] Identifies the **O.C.G.A. § 9-15-2 / § 9-11-3** poverty affidavit
      (affidavit of indigence / in forma pauperis) as the Georgia
      fee-waiver path and reads the current filing-without-fees procedure
      from the references rather than asserting income thresholds from
      memory
- [ ] Notes the opposing party or clerk may **contest** the indigence
      affidavit, triggering a hearing

### Self-help resources

- [ ] Routes the litigant to courthouse self-help / law-library resources
      and georgiacourts.gov, reading the per-county locations from the
      references rather than inventing room numbers or URLs

## Common failure modes

- Adds a Georgia Bar No. to a self-represented signature block
- Tells the filer a relaxed format standard applies to pro se documents
- Asserts a fee-waiver income threshold as a fixed number from memory
- Routes a Cobb filing to Odyssey eFileGA instead of PeachCourt
