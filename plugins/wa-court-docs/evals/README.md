# Evals — Skill Regression Tests

This folder contains prompt-based regression tests for each skill in the
`wa-court-docs` plugin. The prompts are **natural-language user requests**
that should trigger the corresponding skill(s) and produce output that
meets the acceptance criteria listed alongside each prompt.

## How to run an eval

1. Load the plugin in a fresh Claude Code session
2. Paste the **prompt** into the chat
3. Check the output against the **expected triggers** and **acceptance
   criteria**
4. Record pass/fail and any divergence

Evals are **not automated** — they are designed to be run by a human
reviewer who is checking whether a skill edit caused regression.

## Folder layout

- `procedural/` — evals for matter-neutral civil-procedure skills
  (`wa-law-references`, `wa-discovery`, `wa-deadlines`, `wa-first-30-days`,
  `wa-hearings`, `wa-file-packet`, `wa-post-judgment`, `wa-fact-check`)
- `drafting/` — evals for drafting skills (`wa-draft-motion`,
  `wa-draft-declaration`, `wa-draft-order`, `wa-draft-note`)
- `formatting/` — evals for format / local-rule skills
  (`wa-statewide-format`, `wa-kcdc`, `wa-pro-se`, `wa-quality-check`)
- `subject-matter/` — evals for subject-matter bundles
  (`wa-consumer-debt`)
- `integration/` — evals that exercise multiple skills in combination
  (end-to-end filing packets)

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

Keep prompts realistic — the way a pro se litigant would actually ask.
Avoid leading the skill by naming the rule explicitly unless the test is
*specifically* about whether the skill can look up a named rule.

## Notes

- These evals do **not** exercise file writing or external fetches —
  they test skill *triggering* and the *substantive content* of the
  response
- For fact-check evals, the reviewer must manually verify that cited
  rule numbers, RCW sections, and case names match the sources listed
  in `wa-law-references/references/online-sources.md`
- When a skill is edited, at minimum run the eval in its own folder
  plus any integration evals that touch that skill
