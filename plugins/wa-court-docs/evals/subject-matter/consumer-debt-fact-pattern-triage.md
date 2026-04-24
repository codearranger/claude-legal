# wa-consumer-debt — Fact-pattern triage

## Prompt
Here's my situation: I was sued by [debt buyer name] on [date] in KCDC.
They claim I owe $X on a [credit card / medical / personal loan]
account that allegedly defaulted in [year]. They produced a redacted
bill of sale and no signed contract. I disputed by email when they
first contacted me in [year] and they stopped responding.

What defenses and counterclaims should I consider?

## Expected triggers
- `wa-consumer-debt` (SKILL.md — the triage workflow)

## Acceptance criteria
- Walks through a structured triage covering:
  - **Standing / chain of title** — can plaintiff prove assignment?
  - **Statute of limitations** — 6 (written) / 3 (unwritten); accrual;
    revival
  - **Evidence** — admissibility of records under ER 803(6) /
    ER 901 / ER 1002
  - **FDCPA violations** — § 1692e, § 1692g, § 1692f; Reg F
  - **CPA counterclaim** — Hangman Ridge 5 elements + 19.16.440 per se
  - **Collection Agency Act** — licensing violations (RCW 19.16.110
    licensing requirement)
  - **Answer + affirmative defenses** — must plead SOL, payment,
    accord and satisfaction, failure of consideration
- Notes that subject-matter bundle composes with matter-neutral
  procedural skills (`wa-discovery`, `wa-law-references`,
  `wa-first-30-days`)
- Does **not** give definitive legal advice — frames as "consider"

## Common failure modes
- Giving only one defense track (e.g., only SOL, missing chain of
  title)
- Missing licensing question under RCW 19.16.110
- Missing the duty to plead affirmative defenses
- Overpromising outcome
