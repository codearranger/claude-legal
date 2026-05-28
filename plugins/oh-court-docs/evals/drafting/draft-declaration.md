# oh-draft-declaration — Affidavit scaffold (Ohio uses affidavits)

## Prompt

I need a declaration / affidavit to support my motion to
compel in my Ohio Common Pleas case. I'm Jane Doe, pro se,
in Cuyahoga County case CV-25-987654.

## Expected triggers

- `oh-draft-declaration`
- `oh-statewide-format`
- `oh-pro-se`

## Acceptance criteria

### Structure (Ohio AFFIDAVIT, not federal-style declaration)

- [ ] Title: `AFFIDAVIT OF JANE DOE IN SUPPORT OF
      [MOTION]` — Ohio uses **affidavit**, not
      "declaration under penalty of perjury"
- [ ] "STATE OF OHIO, COUNTY OF CUYAHOGA, SS:" header
- [ ] Opening: "Jane Doe, being first duly sworn upon her
      oath, deposes and says:"
- [ ] Numbered paragraphs
- [ ] Signature block with notary jurat: "Sworn to before
      me and subscribed in my presence this ___ day of ___,
      20__"
- [ ] Notary signature + commission line
- [ ] "FURTHER AFFIANT SAYETH NAUGHT" or equivalent
      closing

### Citations

- [ ] References **R.C. 2319.04** as the Ohio statute
      authorizing affidavits
- [ ] If supporting summary judgment, references **Civ. R.
      56(C) / (E)** affidavit standard

## Common failure modes

- Using federal "I declare under penalty of perjury under
  the laws of the United States, 28 U.S.C. § 1746"
  language — that is NOT Ohio practice
- Omitting the notary jurat (Ohio affidavits MUST be
  notarized)
- Calling it a "declaration" without notarization
- Missing personal-knowledge basis in opening paragraph
