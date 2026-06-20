# id-court-docs — Idaho

Draft and format pleadings, declarations, motions, notices of hearing, and proposed orders for Idaho's District Courts and their Magistrate Divisions.

> **NOT LEGAL ADVICE.** Output is a drafting aid; verify every rule, deadline, and citation against current law before filing.

## What it covers

Applies the **I.R.C.P. 2 / 10** form-of-documents rules (Idaho's statewide pleading-format spec lives in **I.R.C.P. 2** — letter paper, ≥ 11-point font, double or 1½ spacing, ≥ 1.2″ top/side and ≥ 1″ bottom margins, title of court ≥ 3″ from the top of page 1, document title at the foot of each page; **I.R.C.P. 10** governs the form of pleadings and numbered paragraphs; **I.R.C.P. 11** the signature and the Idaho State Bar number). Documents file through **iCourt** (Tyler Odyssey *File & Serve*) under the **I.R.E.F.S.** — mandatory for attorneys, optional for self-represented filers.

Idaho's trial court is the unified **District Court**, organized into **seven judicial districts**, each with a **Magistrate Division** (small claims and general civil up to $5,000, eviction, probate, and all family-law matters). Venue skills:

- **`id-ada`** — Ada County District Court, **Fourth Judicial District** (Boise) — the state's most populous venue.
- **`id-bonneville`** — Bonneville County District Court, **Seventh Judicial District** (Idaho Falls).
- **`id-county-courts`** — a statewide roll-up of all seven judicial districts and their county rosters.

Architected as matter-neutral civil-procedure skills — statewide format, discovery (Idaho **allows interrogatories**, capped at 40 including subparts under I.R.C.P. 33), hearings, first-30-days, post-judgment, deadlines, fact-check, filing, and drafting scaffolders (motion, declaration, notice of hearing, proposed order) — plus two subject-matter bundles:

- **`id-consumer-debt`** — FDCPA / Regulation F overlay, the **Idaho Consumer Protection Act** (I.C. § 48-601 et seq.), the **Idaho Collection Agency Act** (I.C. § 26-2222 et seq. — debt-buyer licensing under § 26-2223 administered by the Idaho Department of Finance), the **Idaho Credit Code** (I.C. Title 28 ch. 41-46), statute-of-limitations defenses, chain of title, and the I.R.E. 803(6) / 902(11) debt-buyer evidence foundation.
- **`id-family-law`** + **`id-family-court`** — the separate **Idaho Rules of Family Law Procedure (I.R.F.L.P.)** heard in the Magistrate Division, **community-property** distribution (I.C. § 32-906), the income-shares **Idaho Child Support Guidelines** (I.R.F.L.P. 120), custody best-interests (I.C. § 32-717), and the UCCJEA.

**23 skills total** (21-skill civil-practice core + the two family skills).

### Procedural quirks worth flagging

- **Time computation lives in I.R.C.P. 2.2, not Rule 6** — I.R.C.P. 6 is *[Reserved]* in Idaho. `case-calendar.py` anchors on Rule 2.2 (3-day add-on for service by mail).
- **The format spec lives in I.R.C.P. 2**, not Rule 10 — Rule 10 cross-references it.
- **Idaho allows written interrogatories** (40 including discrete subparts, I.R.C.P. 33(a)(1)).
- **Idaho Code § 73-108 holidays**: no Juneteenth as a state holiday; Columbus Day is observed; the January holiday is *Martin Luther King, Jr.-Idaho Human Rights Day*.
- **Community property** state; a **separate family-law procedure rule set** (I.R.F.L.P.).

## Reference corpora

Under `skills/id-law-references/references/` (each corpus dir has its own README):

- `court-rules/` — **verbatim** I.R.C.P., I.R.E., I.R.F.L.P., and I.A.R. rule text (53 rules across 4 files) fetched by `scripts/pull_idaho_rules.py` from the isc.idaho.gov per-rule print views. (I.R.E.F.S. e-filing mechanics are summarized in the skills rather than snapshotted.)
- `id-statutes-debt/` — **verbatim** Idaho Code text (8 topic files / ~44 sections) for the chapters most relevant to civil + family practice (Title 5 limitations, Title 11 exemptions/garnishment, Title 12 fees, Title 28 credit code + UCC Article 9, Title 32 family law, Title 55 homestead, Title 73 holidays, and the consumer-protection / collection-agency chapters), fetched by `scripts/pull_idaho_statutes.py` from legislature.idaho.gov.
- `federal-debt-laws/`, `federal-bankruptcy/`, `ucc-model/` — **symlinks** into the shared `claude-legal-federal-laws` plugin (declared as a dependency; dereferenced at install time).

## Scripts

- `scripts/format-check.py` — validates a generated `.docx` against the I.R.C.P. 2 baseline (letter paper, ≥ 11-pt font, ≥ 1.2″/1″ margins, 1.5×+ spacing, black ink, footer pagination).
- `scripts/case-calendar.py` — I.R.C.P. 2.2 deadline arithmetic with Idaho Code § 73-108 holidays and named rules (answer-due, discovery responses, summary-judgment windows, appeal, statutes of limitation). Run `case-calendar.py --rules` to list them.

## Dependencies

- `claude-legal-federal-laws` — shared federal / UCC / Bankruptcy corpora (symlinked into `references/`).
- `document-skills` (from the `anthropic-agent-skills` marketplace) — DOCX / PDF / PPTX / XLSX output.

---
Part of the [claude-legal](../../README.md) marketplace. Skills are indexed in [CLAUDE.md](../../CLAUDE.md).
