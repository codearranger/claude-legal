# co-court-docs — Colorado

Draft and format pleadings, declarations, motions, and proposed orders for Colorado district and county courts.

> **NOT LEGAL ADVICE.** Output is a drafting aid; verify every rule, deadline, and citation against current law before filing.

## What it covers

Applies **C.R.C.P. 10 + Chief Justice Directive 11-01** formatting (two-block caption with case-number / division / courtroom box); covers Denver District Court (2nd JD — Lindsey-Flanigan Courthouse), Arapahoe County District Court (18th JD — Centennial / Aurora / Littleton), and the most-populous-counties roll-up (Jefferson, El Paso, Adams, Boulder, Larimer, Douglas, Weld, Pueblo, Mesa, Broomfield).

**Two subject-matter bundles** ship in the initial release:
- `co-consumer-debt` — FDCPA, Reg F, CFDCPA, CCPA, UCCC, chain-of-title, 6-year SOL on liquidated debt.
- `co-family-law` — UDMA (dissolution, parental responsibilities, § 14-10-115 income-shares child support with the 93-overnight rule, maintenance, common-law marriage under *Hogsett & Neale*).

Colorado was the first state with two bundles at initial release. **22 SKILL.md files.**

Statute corpus: 14 articles / 2.0 MB (UCC, UCCC, CFDCPA, CCPA, mediation, judgments, exemptions, garnishment, limitations, UDMA, UCCJEA, APA). Court-rules corpus: **80 files** — 72 verbatim Chief Justice Directives (CJDs) including the Jan-2026 statewide eFiling standards, plus pointer stubs for C.R.C.P. / CRE / C.A.R. / Colo. RPC. Those rule sets are **public-domain edicts of the Colorado Supreme Court** (only the West/Lexis *annotated compilations* are copyrighted), but Colorado publishes no free structured copy of the bare rule text — see the court-rules corpus README.

## Reference corpora

Under `skills/co-law-references/references/` (each corpus dir has its own README): `co-statutes-debt/`, `court-rules/`, plus the shared federal symlinks.

## Refresh

`scripts/pull_co_statutes.py` · `scripts/pull_co_court_rules.py`. Plugin scripts: `format-check.py` (C.R.C.P. 10 + CJD 11-01) · `case-calendar.py` (C.R.C.P. 6 + C.R.S. § 24-11-101 holidays).

---
Part of the [claude-legal](../../README.md) marketplace. Skills are indexed in [CLAUDE.md](../../CLAUDE.md).
