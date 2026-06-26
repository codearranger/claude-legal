# ga-court-docs — Georgia

Draft and format pleadings, declarations, motions, and proposed orders for Georgia courts.

> **NOT LEGAL ADVICE.** Output is a drafting aid; verify every rule, deadline, and citation against current law before filing.

## What it covers

Applies **O.C.G.A. § 9-11-10 + Uniform Superior Court Rules** formatting; covers Fulton County Superior Court, Cobb County Superior Court, and a county-courts roll-up. Architected as matter-neutral civil-procedure skills (Georgia Civil Practice Act (O.C.G.A. Title 9, Ch. 11) civil rules, Georgia Evidence Code (O.C.G.A. Title 24) evidence rules, fees and costs, local rules, citation per the Georgia appellate citation (Bluebook-based), discovery, first-30-days, hearings, filing, post-judgment, fact-check, deadlines, drafting scaffolders) plus subject-matter bundles (starting with `ga-consumer-debt`).

<!-- TODO: expand coverage — venues, subject bundles, statute / court-rule corpus sizes, SKILL.md count, and any procedural quirks worth flagging. -->

## Reference corpora

Under `skills/ga-law-references/references/` (each corpus dir has its own README): `ga-statutes-debt/`, `court-rules/`, plus the shared `federal-debt-laws/` / `federal-bankruptcy/` / `ucc-model/` symlinks into `claude-legal-federal-laws`.

## Refresh

Plugin scripts: `format-check.py` (O.C.G.A. § 9-11-10 + Uniform Superior Court Rules) · `case-calendar.py`.

---
Part of the [claude-legal](../../README.md) marketplace. Skills are indexed in [CLAUDE.md](../../CLAUDE.md).
