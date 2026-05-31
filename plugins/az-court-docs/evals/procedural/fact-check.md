# az-fact-check — Verify an A.R.S./rule cite + an Arizona case + the correct rule set for the forum

## Prompt

I drafted a motion for my Arizona case and I want to make sure all
my citations are real and correct before I file. I cited a couple
of statutes, a Ariz. R. Civ. P. rule, and an Arizona court case I
found online. My case is a debt collection matter in Justice Court.

## Expected triggers

- `az-fact-check`
- `az-law-references`

## Acceptance criteria

### Statute / rule verification

- [ ] Verifies each **A.R.S. §** citation against `az-statutes-debt/`
      and each rule citation against `court-rules/` — confirms the
      section/rule exists and that the cited proposition matches the
      text, rather than accepting the cite at face value
- [ ] Flags any citation that cannot be verified against the corpus
      as unverified (does not assert it is correct from memory)

### Case verification

- [ ] Verifies the Arizona case against `key-cases.md` and/or a
      structured source in `legal-data-apis.md` (e.g., CourtListener
      Arizona courts) — confirms name, citation, and that it stands
      for the asserted proposition; flags it if it cannot be verified

### Forum / rule-set check

- [ ] Confirms the document uses the **correct rule set for the
      forum** — for a Justice Court debt matter, the **Justice Court
      Rules of Civil Procedure (JCRCP)**, NOT the ARCP and NOT the
      ARFLP — and flags a mismatched rule citation as a defect (read
      the scope of each set from the corpus)

### Honest sourcing

- [ ] Treats every cite as unverified until checked against the
      corpus / a structured source; cites by number

## Common failure modes

- Accepts a fabricated or misremembered A.R.S. section or case as
  correct without checking the corpus
- Fails to catch ARCP citations in a Justice Court (JCRCP) matter
- Asserts a case holding from memory instead of verifying it
