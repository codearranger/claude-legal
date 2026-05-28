# Evals — Skill Regression Tests (California)

This folder contains prompt-based regression tests for each
skill in the `ca-court-docs` plugin. The prompts are
**natural-language user requests** that should trigger the
corresponding skill(s) and produce output that meets the
acceptance criteria listed alongside each prompt.

## How to run an eval

1. Load the plugin in a fresh Claude Code session
2. Paste the **prompt** into the chat
3. Check the output against the **expected triggers** and
   **acceptance criteria**
4. Record pass/fail and any divergence

Evals are **not automated** — they are designed to be run by
a human reviewer who is checking whether a skill edit caused
regression.

## Folder layout

- `procedural/` — evals for matter-neutral civil-procedure
  skills (`ca-law-references`, `ca-discovery`, `ca-deadlines`,
  `ca-first-30-days`, `ca-hearings`, `ca-file-packet`,
  `ca-post-judgment`, `ca-fact-check`)
- `drafting/` — evals for drafting skills (`ca-draft-motion`,
  `ca-draft-declaration`, `ca-draft-order`, `ca-draft-note`)
- `formatting/` — evals for format / local-rule skills
  (`ca-statewide-format`, `ca-lasc`, `ca-sfsc`,
  `ca-county-courts`, `ca-pro-se`, `ca-quality-check`)
- `subject-matter/` — evals for subject-matter bundles
  (`ca-consumer-debt`)
- `integration/` — evals that exercise multiple skills in
  combination (end-to-end filing packets)

## Writing new evals

Each eval file is Markdown with this structure:

```markdown
# [Skill name] — [short eval name]

## Prompt
[The user message that should trigger the skill]

## Expected triggers
- [Which skill(s) should fire]

## Acceptance criteria
- [Specific content that must appear]
- [Specific citations or rules that must be correct]
- [Format or structural requirements]

## Common failure modes
- [What regression looks like]
```

Keep prompts realistic — the way a pro se litigant would
actually ask. Avoid leading the skill by naming the rule
explicitly unless the test is *specifically* about whether
the skill can look up a named rule.

## California-specific test focuses

Several California procedural distinctions deserve coverage:

- **Tentative-ruling regime** (CRC 3.1308) — many courts post
  tentatives the day before; affects hearing strategy.
- **35-interrogatory cap** (CCP § 2030.030(a)) — specials capped
  at 35 without § 2030.040 declaration; form interrogs uncapped.
- **45-day motion-to-compel-further deadline** (CCP §§ 2030.300(c),
  2031.310(c), 2033.290(c)) — jurisdictional; missing it forfeits
  the right entirely.
- **Court-day notice periods** (CCP § 1005(b)) — California uses
  court days, not calendar, for motion notice / opposition / reply.
- **Rosenthal Act first-party reach** (Cal. Civ. Code § 1788.2(c))
  — unlike federal FDCPA, Rosenthal covers original creditors too.
- **CDCLA licensure** (Cal. Fin. Code § 100001) — debt collectors
  and buyers must be DFPI-licensed as of January 2022; non-licensure
  is an affirmative defense.

## Cross-references

- `or-court-docs/evals/` — the parallel OR evals (same framework)
- `wa-court-docs/evals/` — the parallel WA evals
