# wa-fact-check — Pre-filing citation verification

## Prompt
Before I file this motion, can you fact-check every rule, statute, and
case citation against canonical sources?

## Expected triggers
- `wa-fact-check`
- `wa-law-references` (online-sources.md)

## Acceptance criteria
- Identifies every citation in the document (rules, statutes, cases,
  regulations)
- Checks each against the canonical URL in
  `wa-law-references/references/online-sources.md` (or the bundle-side
  online-sources file for subject-matter citations)
- Uses **WebFetch only** — no curl, wget, Python requests, or other
  bypasses
- Reports any citation that:
  - Cannot be verified
  - Has been superseded or amended since the cited date
  - Is cited to the wrong reporter or wrong section
  - Has the wrong case name or year
- Produces a report with PASS / FAIL per citation and the source
  checked
- Flags cases that may have been overruled and need shepardizing

## Common failure modes
- Fabricating "verified" results without actually fetching
- Using non-canonical URLs (like casetext, justia without
  cross-verification)
- Using curl or alternative fetch methods
- Checking case name only, not the substantive holding
- Missing citations that are formatted unusually
