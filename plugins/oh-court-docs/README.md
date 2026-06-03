# oh-court-docs — Ohio

Draft and format pleadings, declarations, motions, and proposed orders for Ohio courts.

> **NOT LEGAL ADVICE.** Output is a drafting aid; verify every rule, deadline, and citation against current law before filing.

## What it covers

Applies **Ohio Civ. R. 10 + per-court local rules** (Ohio has no statewide pleading-format rule). Covers **eight flagship Court of Common Pleas venues each as its own skill** — Cuyahoga (Cleveland), Franklin (Columbus), Hamilton (Cincinnati), Summit (Akron), Montgomery (Dayton), Lucas (Toledo), Stark (Canton), Butler (Hamilton, OH) — plus a county-courts roll-up for the other 80 counties, a dedicated `oh-municipal-courts` skill (R.C. Chapter 1901; $15,000 civil cap; $6,000 small-claims division; the primary pro-se consumer-debt forum), and `oh-family-court` (the Domestic Relations Division + the Juvenile Division under R.C. Chapter 2151).

**Two subject-matter bundles:**
- `oh-consumer-debt` — FDCPA + Reg F + **Ohio Consumer Sales Practices Act** (R.C. Chapter 1345; R.C. 1345.09 treble damages + mandatory fees); chain of title under Ohio UCC Article 9 (R.C. Chapter 1309); R.C. 2305.06 six-year written-contract SOL; no Ohio collection-agency licensing regime.
- `oh-family-law` — R.C. Chapter 3105 divorce + equitable distribution at R.C. 3105.171 (NOT community property); R.C. Chapter 3109 custody/parenting/support; R.C. Chapter 3119 income-shares CS guidelines ($300k combined-income cap); R.C. 3105.18 spousal support; R.C. Chapter 3127 UCCJEA; R.C. Chapter 3115 UIFSA.

**30 SKILL.md files.** Ohio quirks worth flagging: public-domain citation `YYYY-Ohio-NNNN` (mandatory in appellate cases since 2002); Columbus Day legal holiday (R.C. 1.14); 28-day answer; Civ. R. 53 magistrates with a 14-day objection clock; Civ. R. 41(A) one-dismissal rule.

## Reference corpora

Under `skills/oh-law-references/references/` (each corpus dir has its own README): `oh-statutes-debt/`, `court-rules/`, plus the shared federal symlinks.

## Refresh

`scripts/pull_ohio_statutes.py` · `scripts/pull_ohio_court_rules.py`. Plugin scripts: `format-check.py` · `case-calendar.py`.

---
Part of the [claude-legal](../../README.md) marketplace. Skills are indexed in [CLAUDE.md](../../CLAUDE.md).
