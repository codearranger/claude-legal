# Evals — Skill Regression Tests (Idaho)

Prompt-based regression tests for the `id-court-docs` plugin, across
five categories.

> **NOT LEGAL ADVICE.** These evals exercise drafting and procedural
> scaffolding, not legal advice.

## Folder layout

- `drafting/` — drafting-skill evals (motion, affidavit/declaration, notice of hearing, proposed order)
- `formatting/` — format and venue-caption evals (statewide format, Bonneville caption, pro se, quality check)
- `procedural/` — matter-neutral civil-procedure evals (deadlines, discovery, fact-check, file-packet, first-30-days, law-references)
- `subject-matter/` — subject-bundle evals (debt-buyer chain of title, time-barred debt, collection-agency licensing, community-property division)
- `integration/` — end-to-end multi-skill evals (debt-defense answer, divorce intake)

## Thin-skill acceptance criteria

User-stated hypothetical facts in eval prompts are fine. Acceptance
criteria must NOT hard-code drift-prone current-law values (exemption
amounts, homestead figures, child-support numbers). Where a figure
matters, the criterion requires the agent to **read the current value
from the references corpus** (`../id-law-references/references/`),
not recite it from memory.

## Idaho-specific things these evals guard

- **Time computation lives in I.R.C.P. 2.2, not Rule 6** (Rule 6 is reserved).
- **The format spec lives in I.R.C.P. 2**, not Rule 10.
- **Idaho allows interrogatories** (40 including subparts, I.R.C.P. 33).
- **Magistrate Division vs. District Court** civil split (the $5,000 line — read the current figure from the corpus).
- **Separate I.R.F.L.P.** family rules; **community property**.
- **Idaho Code § 73-108 holidays** (no state Juneteenth; Columbus Day observed).
