# oh-fact-check — Citation verification

## Prompt

Please fact-check this proposed cite for an Ohio appellate
brief: "Smith v. Jones, 2024-Ohio-1234, ¶ 12 (8th Dist.)."
What does the citation system require, and is this well-
formed?

## Expected triggers

- `oh-fact-check`
- `oh-law-references`

## Acceptance criteria

- [ ] Recognizes the format as Ohio's public-domain
      citation: `YYYY-Ohio-NNNN`
- [ ] Notes this format is **mandatory** in Ohio appellate
      cases since 2002
- [ ] Walks the four-pass framework: facial validity,
      Westlaw / public-domain verification, pin cite to ¶,
      court / district verification
- [ ] Notes the **¶** symbol with paragraph number is the
      preferred Ohio pin cite (rather than page number)
- [ ] Notes "(8th Dist.)" indicates the 8th District Court
      of Appeals (Cuyahoga County)

## Common failure modes

- Treating the citation as a West-only cite (no public-
  domain awareness)
- Wrong pin-cite convention
- Missing the 2002 effective-date note
