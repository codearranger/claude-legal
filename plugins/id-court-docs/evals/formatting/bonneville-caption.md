# id-bonneville — Bonneville County District Court caption + venue

## Prompt

I need to file a civil complaint in Bonneville County, Idaho (Idaho
Falls). Build me the caption and tell me what court and judicial
district this is, and how I file it.

## Expected triggers

- `id-bonneville`
- `id-statewide-format`

## Acceptance criteria

### Venue identification

- [ ] Identifies the court as the **District Court of the Seventh
      Judicial District, in and for Bonneville County**, sitting in
      Idaho Falls
- [ ] Correctly states that Bonneville County is in the **Seventh
      Judicial District** (not another district)
- [ ] Notes the Magistrate Division vs. District Court split for civil
      cases and routes by amount in controversy — reading the current
      jurisdictional dollar line from the corpus rather than asserting
      it from memory

### Caption form (I.R.C.P. 2)

- [ ] Builds a caption with the **title of the court**, the **party
      title** (Plaintiff v. Defendant), the **case number** slot, and
      the **document title**, per I.R.C.P. 2
- [ ] Places the attorney/party identification block above the title
      of the court, left of center; for a self-represented filer,
      omits the Idaho State Bar number
- [ ] Defers exact margin/font/placement figures to
      `id-statewide-format` / the court-rules corpus rather than
      inventing numbers

### Filing mechanics

- [ ] Describes filing through **iCourt** (Odyssey *File & Serve*)
      under the I.R.E.F.S., noting e-filing is mandatory for attorneys
      and optional for self-represented filers

## Common failure modes

- Puts Bonneville County in the wrong judicial district
- Invents a margin/font figure instead of deferring to the corpus
- Uses Petitioner/Respondent for an ordinary civil complaint
- Omits the iCourt / I.R.E.F.S. filing path
