# in-court-docs — Indiana

Draft and format pleadings, declarations, motions, and proposed orders for Indiana trial courts.

> **NOT LEGAL ADVICE.** Output is a drafting aid; verify every rule, deadline, and citation against current law before filing.

## What it covers

Applies **Ind. Trial R. 5(E)** formatting (Indiana lacks a single consolidated format rule; requirements live across T.R. 5(E), T.R. 11, and county local rules); covers Marion Superior Court (Indianapolis — statewide's highest civil-case-volume court) and Lake Superior Court (Crown Point, with Hammond and East Chicago branches), plus the populous-counties roll-up (Allen, Hamilton, St. Joseph, Vanderburgh, Elkhart, Tippecanoe, Porter, Madison, Bartholomew). Pro se under the *Goossens v. Goossens* same-standard rule.

**Two subject-matter bundles:**
- `in-consumer-debt` — FDCPA / Reg F / **IUCCC** (IC 24-4.5) / **DCSA** (IC 24-5-0.5, Indiana's UDAP analog) / chain-of-title under Indiana UCC Article 9 (IC 26-1-9.1) / debt SOLs (IC 34-11-2).
- `in-family-law` — paternity (**IC 31-14**, the JP case-type backbone for non-marital children); dissolution (IC 31-15, equitable distribution); child support (IC 31-16 + Indiana Child Support Guidelines); custody/parenting time (IC 31-17 + Parenting Time Guidelines); adoption (IC 31-19); UCCJEA (IC 31-21); DCS/CHINS/TPR/delinquency (IC 31-25/30/32/34/35/37); protection orders (IC 34-26-5).

A dedicated `in-family-court` venue skill covers Indiana's family-law topology (no separate Family Court trial court; large counties run a Juvenile Division; smaller counties like Bartholomew consolidate JP/DC/DR in the Circuit Court).

**Procedural quirks worth flagging:** (1) summary judgment under T.R. 56 follows ***Jarboe v. Landmark*** — the movant must affirmatively negate an element (rejected federal *Celotex* burden-shifting); (2) **T.R. 59 motion to correct error** is a required appeal prerequisite for some issues; (3) Indiana requires no collection-agency licensing (defense leans on chain-of-title + FDCPA + DCSA). Statewide Odyssey e-filing since 2017. **23 SKILL.md files.** Follows the thin-skill architecture.

## Reference corpora

Under `skills/in-law-references/references/` (each corpus dir has its own README): `in-statutes-debt/`, `court-rules/`, plus the shared federal symlinks.

## Refresh

`scripts/pull_indiana_statutes.py` (api.iga.in.gov; stubs without `IGA_API_KEY`) · `scripts/pull_indiana_rules.py`. Plugin scripts: `format-check.py` · `case-calendar.py`.

---
Part of the [claude-legal](../../README.md) marketplace. Skills are indexed in [CLAUDE.md](../../CLAUDE.md).
