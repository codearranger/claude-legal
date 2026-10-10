# wa-first-30-days — Answer deadline and counterclaims

## Prompt
I was just served with a summons and complaint in King County District
Court on April 1, 2026. What's the deadline to answer and what should I
include?

## Expected triggers
- `wa-first-30-days`
- `wa-law-references` (civil-rules.md — CRLJ 4, 8, 12, 13)

## Acceptance criteria
- Identifies **20-day answer deadline** for civil cases (verifying
  against the governing statute)
- Cites **CRLJ 8** (answer form), **CRLJ 12** (defenses),
  **CRLJ 13** (counterclaims)
- Notes the CR 12(b) enumerated defenses that should be preserved in
  the answer (PJ, SMJ, venue, service defects, failure to state a
  claim)
- Mentions **affirmative defenses** (CRLJ 8(c)) must be pled or waived
  (e.g., statute of limitations, payment, release, accord and
  satisfaction)
- Notes **counterclaims** — compulsory (same transaction) vs.
  permissive
- For subject-matter-specific defenses (FDCPA, CPA counterclaims for
  debt cases), points to the subject-matter bundle
  (`wa-consumer-debt/SKILL.md`)
- Correctly computes deadline: April 1 + 20 days = April 21, 2026

## Common failure modes
- Stating a federal 21-day deadline
- Missing affirmative-defense waiver warning
- Missing the distinction between compulsory and permissive
  counterclaims
- Leaking subject-matter-specific counterclaim content into the
  matter-neutral response
