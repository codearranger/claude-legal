# ga-file-packet — County e-filing assembly (PeachCourt / Odyssey eFileGA) + fee waiver

## Prompt

I've finished drafting my answer and a supporting affidavit in a Georgia
State Court case. I need to file them. Walk me through assembling the
packet, e-filing it, and what to do if I can't afford the filing fee.

## Expected triggers

- `ga-file-packet`
- `ga-statewide-format`
- `ga-pro-se`

## Acceptance criteria

### County e-filing platform

- [ ] Identifies the correct platform by county — **PeachCourt** for Cobb
      (and Gwinnett-area Superior), **Odyssey eFileGA** for Fulton and
      Gwinnett State/Superior — and notes civil e-filing is mandatory
      statewide (SB 407) — reads the current per-county platform map from
      the references rather than asserting it from memory
- [ ] Notes each document (answer, affidavit, proposed order) is filed as
      a **separate** attachment with the correct document type, not merged
      into one PDF

### Packet preflight

- [ ] Runs a format check before upload: Georgia caption with the correct
      court/county line and **"Civil Action File No."**, marketplace
      baseline layout, certificate of service under O.C.G.A. § 9-11-5, and
      a signature block matching the filer's status
- [ ] Confirms any **proposed order** is a separate document
      (cross-reference `ga-draft-order`)

### Filing fees and fee waiver

- [ ] Reads the current filing-fee schedule from the references corpus
      rather than asserting dollar figures from memory
- [ ] Routes an indigent filer to the **O.C.G.A. § 9-15-2 / § 9-11-3
      poverty affidavit** (affidavit of indigence) and notes the clerk or
      opposing party may contest it, triggering a hearing — cross-reference
      `ga-pro-se`

## Common failure modes

- Routes a Cobb filing to Odyssey eFileGA (Cobb uses PeachCourt)
- Tells the filer to merge all documents into one PDF
- Asserts filing-fee dollar amounts from memory
- Ignores the poverty-affidavit fee-waiver path
