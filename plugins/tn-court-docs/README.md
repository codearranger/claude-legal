# tn-court-docs — Tennessee

Draft and format pleadings, declarations, motions, and proposed orders for Tennessee trial courts.

> **NOT LEGAL ADVICE.** Output is a drafting aid; verify every rule, deadline, and citation against current law before filing.

## What it covers

Tennessee has **no single statewide page/margin/font rule** — form of pleadings is governed by Tenn. R. Civ. P. 10 (caption + numbered paragraphs + exhibits) and Rule 11 (signature with the BPR number); page limits/typography come from each court's **local rules** (indexed on the AOC "Local Rules of Practice" page at tncourts.gov).

Covers Tennessee's three trial-court layers — **Circuit Court** (law), **Chancery Court** (equity), and the limited-jurisdiction **General Sessions Court** (the dominant consumer-debt and eviction forum: $25,000 civil cap under § 16-15-501, unlimited detainer jurisdiction, suit by civil warrant, 10-day de novo appeal to Circuit under § 27-5-108). Dedicated venue skills for the four largest counties (Davidson / Shelby / Knox / Hamilton) plus a `tn-general-sessions` skill, a county-courts roll-up, and split family-forum skills (`tn-family-court` for Circuit/Chancery divorce + `tn-juvenile-court` for Title 37 paternity / dependency / TPR).

**Four subject-matter bundles:** `tn-consumer-debt` (FDCPA, Reg F, **TCPA** at § 47-18-101 with the *Pursell* rule that it generally does not reach debt collection, the **Tennessee Collection Service Act** at Title 62 ch. 20, the 2024 § 20-6-104 debt-buyer rule, chain of title, 6-year SOL at § 28-3-109), `tn-family-law` (Title 36 — equitable distribution § 36-4-121, 60/90-day waiting period § 36-4-103, income-shares CS § 36-5-101, four alimony types § 36-5-121, parenting plans § 36-6-401 + 2018 relocation § 36-6-108), `tn-landlord-tenant` (URLTA § 66-28-101 in counties over 75,000, non-URLTA § 66-7-101, 14-day notice § 66-28-505, detainer warrants § 29-18-101), `tn-personal-injury` (*McIntyre v. Balentine* modified comparative fault / 49% bar, 1-year SOL § 28-3-104, GTLA caps § 29-20-101, HCLA pre-suit notice + certificate of good faith § 29-26-121/-122).

**29 SKILL.md files.** Distinctives flagged: the *Rye* *Celotex*-style summary-judgment standard; Tenn. R. Civ. P. 6.01/6.05 deadline arithmetic with § 15-1-101 holidays (incl. Good Friday + Columbus Day); county-by-county e-filing.

## Reference corpora

Under `skills/tn-law-references/references/` (each corpus dir has its own README): `tn-statutes-debt/` (verbatim Tenn. Code Ann.; the statutory **text is public domain** — LexisNexis copyrights only the *annotations* — and is mirrored from Justia), `court-rules/`, plus the shared federal symlinks.

## Refresh

`scripts/pull_tn_statutes.py` (curl_cffi; stubs on 403) · `scripts/pull_tn_court_rules.py`. Plugin scripts: `format-check.py` · `case-calendar.py`.

---
Part of the [claude-legal](../../README.md) marketplace. Skills are indexed in [CLAUDE.md](../../CLAUDE.md).
