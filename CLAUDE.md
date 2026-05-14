# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

The `claude-legal` **marketplace** — a Claude Code / Cowork marketplace of court-document plugins organized one plugin per state, plus a shared data-only plugin for federal law. It ships **five** plugins:

- **`claude-legal-federal-laws`** — Shared, data-only plugin holding the canonical copy of federal U.S. debt-collection and consumer-finance law (FDCPA, FCRA, TILA, ECOA, Reg B/F/V/Z) and the model Uniform Commercial Code (Articles 1, 2, 3, 9). No skills. Every state plugin below declares this as a dependency and symlinks into its `references/` tree, so federal content lives in one place rather than being copy-pasted per state.
- **`wa-court-docs`** — Washington State (GR 14 formatting, King County District + Superior + populous-counties roll-up, RCW 19.16 / WA CPA consumer-debt bundle).
- **`or-court-docs`** — Oregon (UTCR 2.010 formatting, Multnomah + Washington County Circuit Court + populous-counties roll-up, ORS 697 / UTPA consumer-debt bundle).
- **`ca-court-docs`** — California (CRC 2.100-2.119 formatting, LASC + SFSC + populous-counties roll-up, Rosenthal Act / FDBPA / CDCLA consumer-debt bundle). All 21 SKILL.md files authored with CA-specific substance; reference corpora include the shared `federal-debt-laws/` + `ucc-model/` content via the `claude-legal-federal-laws` dependency, the CA-specific `ca-statutes-debt/` (Rosenthal Act, FDBPA, CDCLA, UCL, CLRA, CCP procedural sections, Cal. Comm. Code UCC enactments), and the CA `court-rules/` corpus (CRC Titles 2/3/5/7/8, Cal. Evid. Code, LASC + SFSC + OCSC local rules).
- **`co-court-docs`** — Colorado (C.R.C.P. 10 + Chief Justice Directive 11-01 formatting with the two-block caption + case-number/division/courtroom box, Denver District Court / 2nd JD + Arapahoe County District Court / 18th JD + populous-counties roll-up, CFDCPA / CCPA / UCCC consumer-debt bundle, **plus a Colorado-specific family-law bundle** — `co-family-law` — covering UDMA dissolution / annulment, child support under C.R.S. § 14-10-115 with the 93-overnight rule, parental responsibilities under C.R.S. § 14-10-124, maintenance under C.R.S. § 14-10-114, and common-law marriage under *People v. Lucero* / *Hogsett & Neale*). Colorado is the **first state plugin to ship with two subject-matter bundles in its initial release** — consumer-debt and family-law — for a total of **22 SKILL.md files**.

All four state plugins are architected identically: matter-neutral civil-procedure skills plus subject-matter bundles (starting with consumer-debt defense in each state). The structure leaves clean slots for plugins covering additional states.

Output is documents, not advice; everything is bracketed by a "not legal advice" disclaimer that downstream skills repeat.

> **NOT LEGAL ADVICE.** Generated content is a drafting aid; verify against current rules and case law before filing.

## Big-picture architecture

Three layers, three things to know:

1. **Marketplace → Plugin → Skill.** Two manifests (`.claude-plugin/marketplace.json` at repo root, `plugins/<plugin>/.claude-plugin/plugin.json` per plugin) plus per-skill `SKILL.md` files. The runtime loads skills by their **directory name**; the `name:` field in `SKILL.md` frontmatter must match the directory exactly or the skill won't load. The linter enforces this.

2. **Skills only — no slash commands.** Every workflow is a skill auto-invoked from natural-language triggers in its `description:` frontmatter. When adding a workflow, write it as a skill; do not add a slash command.

3. **Matter-neutral procedural skills + subject-matter bundles.** The procedural skills (statewide-format, discovery, hearings, fact-check, deadlines, draft-* skills, etc.) know nothing about a specific area of law. Subject-matter bundles (`wa-consumer-debt`, `or-consumer-debt`; landlord-tenant / family / PI are the future slots) plug into them via composition. Don't bake subject-matter law into procedural skills.

**County coverage is skills inside the state plugin, not separate plugins.** One plugin per state; within it, a high-volume court can get its own skill (`wa-kcdc` for King County District Court, `wa-kcsc` for King County Superior Court, `or-multcc` for Multnomah Circuit, `or-wccc` for Washington County Circuit), and the long tail of counties is carried as a single roll-up skill plus reference data (`wa-county-courts`, `or-county-courts`). Name court skills `<state>-<court>` (e.g., `wa-kcdc`, `or-multcc`) or use the state-level roll-up. Don't create a plugin or a skill per county — that doesn't scale to 3,000+ U.S. counties; add detail to the roll-up's reference files on demand.

## Skills index — Washington (`wa-court-docs`, 21 skills)

| Skill | Role |
|---|---|
| `wa-statewide-format` | GR 14 + statewide drafting conventions |
| `wa-kcdc` | King County District Court (East/Redmond, South/Burien, West/Seattle) |
| `wa-kcsc` | King County Superior Court (Seattle / Kent — MRJC); LCR 82 case assignment, LCR 4 case schedule, LCR 7 motions + working copies |
| `wa-county-courts` | Other most-populous counties' district/superior courts (Pierce, Snohomish, Spokane, Clark, Thurston, Kitsap, Yakima, Whatcom, Benton) |
| `wa-pro-se` | Pro se workflows; pro-se drafting framework; service |
| `wa-law-references` | Civil rules, evidence, citation format, fees, local rules — **canonical reference corpora live here** |
| `wa-discovery` | RFPs, interrogatories, RFAs, meet-and-confer, motion to compel |
| `wa-hearings` | Oral argument, Zoom, courtroom etiquette |
| `wa-post-judgment` | CR 60, garnishment, exemptions, supplemental proceedings |
| `wa-first-30-days` | Answer, defenses, counterclaims |
| `wa-fact-check` | Citation verification, quote-to-source checking |
| `wa-deadlines` | CR/CRLJ 6 with RCW 1.16.050 holidays |
| `wa-draft-motion` / `-declaration` / `-note` / `-order` | Scaffolders |
| `wa-quality-check` | Pre-filing format + content QC |
| `wa-schedule-hearing` | KCDC CivilMGT date-request email |
| `wa-file-packet` | Assemble + preflight a packet |
| `wa-submit-order` | Post-hearing signed-order transmittal |
| `wa-consumer-debt` | Subject bundle: FDCPA, Reg F, RCW 19.16, CPA, chain of title |

## Skills index — Oregon (`or-court-docs`, 21 skills)

| Skill | Role |
|---|---|
| `or-statewide-format` | UTCR 2.010 + statewide drafting conventions (UTCR 2.100 caption, UTCR 2.110 title, UTCR 2.120 redaction) |
| `or-multcc` | Multnomah County Circuit Court (Portland / Central Courthouse); JA-based scheduling; SLR 5.025 / 5.045 / 5.100 |
| `or-wccc` | Washington County Circuit Court (Hillsboro); Civil Division scheduling; SLR 5.045 simultaneous-Notice rule, 15-page working-copy threshold |
| `or-county-courts` | Other most-populous Oregon counties (Clackamas, Lane, Marion, Jackson, Deschutes, Linn, Benton, Yamhill, Polk, Douglas); 36-county directory |
| `or-pro-se` | Pro se workflows; pro-se drafting framework adapted for Oregon; signature block omits OSB#; service under ORCP 9 |
| `or-law-references` | ORCP civil rules, OEC evidence rules, ORS 20 fees, Oregon Style Manual citation format, local SLRs — **canonical reference corpora live here** |
| `or-discovery` | RFPs, RFAs, depositions, meet-and-confer (SLR 5.045/5.046), motion to compel under ORCP 46 A. **Key Oregon distinction: no written interrogatories under ORCP without court order.** |
| `or-hearings` | Oral argument, WebEx, courtroom etiquette, hearing-day checklist |
| `or-post-judgment` | ORCP 71 vacation, ORS 18.600+ garnishment, ORS 18.345-385 exemptions, ORS 18.265+ debtor exam, ORS 18.235 satisfaction |
| `or-first-30-days` | Answer, ORCP 21 motion-to-dismiss triage, affirmative defenses, counterclaims |
| `or-fact-check` | Citation verification against canonical sources; Oregon Style Manual conventions |
| `or-deadlines` | ORCP 10 time computation with ORS 187.010 holidays (note: no day-after-Thanksgiving in Oregon) |
| `or-draft-motion` / `-declaration` / `-note` / `-order` | Scaffolders |
| `or-quality-check` | Pre-filing format + content QC (UTCR 2.010 + pro-se drafting framework) |
| `or-schedule-hearing` | JA date-request email (Multnomah) / Civil Division (Washington Co) / per-county routing |
| `or-file-packet` | Assemble + preflight a packet for OJD File and Serve |
| `or-submit-order` | Post-hearing signed-order transmittal; UTCR 5.100 3-court-day service |
| `or-consumer-debt` | Subject bundle: FDCPA, Reg F, **ORS 697 collection-agency registration**, **Oregon UTPA (ORS 646.605)**, chain of title, 5 fact-pattern triage, RFP/RFA banks, synthetic example filings |

## Skills index — California (`ca-court-docs`, 21 skills)

Mirrors the WA / OR 21-skill shape; substantive CA content authored across SKILL.md bodies and references.

| Skill | Role |
|---|---|
| `ca-statewide-format` | CRC 2.100-2.119 + statewide drafting conventions |
| `ca-lasc` | Los Angeles Superior Court (statewide's highest-volume civil court); LASC local rules + Court Reservation System |
| `ca-sfsc` | San Francisco Superior Court; SFSC local rules + Department 302 law-and-motion |
| `ca-county-courts` | Other most-populous California counties' superior courts (Orange, San Diego, Riverside, San Bernardino, Santa Clara, Alameda, Sacramento, Contra Costa, Fresno) |
| `ca-pro-se` | Pro se workflows; pro-se drafting framework adapted for California; service under CCP §§ 1010-1020 |
| `ca-law-references` | CCP civil rules, CEC evidence rules, Cal. Civ. Code, CRC, fees, local rules — **canonical reference corpora live here** |
| `ca-discovery` | RFPs (CCP § 2031), interrogatories (CCP §§ 2030.010 form/special — **35-question limit on specials w/o declaration**), RFAs (CCP § 2033), depositions, meet-and-confer, motion to compel under CCP § 2031.310 et seq. |
| `ca-hearings` | Oral argument, tentative-ruling regime (CRC 3.1308), remote appearances, courtroom etiquette |
| `ca-post-judgment` | CCP § 473 relief, CCP § 663 motion to vacate, EJ 195 etc. garnishment, CCP § 703 exemptions, debtor exam (CCP § 708.110), satisfaction (CCP § 724) |
| `ca-first-30-days` | Answer (30 days from service per CCP § 412.20(a)(3)), CCP § 430.10 demurrer triage, CCP § 435 motion to strike, affirmative defenses, cross-complaints |
| `ca-fact-check` | Citation verification against canonical sources; California Style Manual conventions |
| `ca-deadlines` | CCP § 12 / § 12a / § 12c time computation with state holidays (Govt. Code § 6700) |
| `ca-draft-motion` / `-declaration` / `-note` / `-order` | Scaffolders ("draft-note" maps to California's **Notice of Motion** under CCP § 1010) |
| `ca-quality-check` | Pre-filing format + content QC (CRC 2.100-2.119 + pro-se drafting framework) |
| `ca-schedule-hearing` | LASC Court Reservation System / SFSC Department 302 reservation / per-county routing |
| `ca-file-packet` | Assemble + preflight a packet for e-filing (mandatory in many CA courts) |
| `ca-submit-order` | Post-hearing signed-order transmittal under CRC 3.1312 (5-day proposed-order rule) |
| `ca-consumer-debt` | Subject bundle: FDCPA, Reg F, **California Rosenthal Act (Cal. Civ. Code §§ 1788 et seq.)**, **California Debt Collection Licensing Act (Fin. Code § 100000 et seq.)**, chain of title, fact-pattern triage, RFP/RFA banks, synthetic example filings |

## Skills index — Colorado (`co-court-docs`, 22 skills)

| Skill | Role |
|---|---|
| `co-statewide-format` | C.R.C.P. 10 + Chief Justice Directive 11-01; two-block Colorado caption with case-number / division / courtroom box |
| `co-denver` | Denver District Court (2nd Judicial District) — Lindsey-Flanigan Courthouse; CCEFS; chambers practice standards |
| `co-arapahoe` | Arapahoe County District Court (18th Judicial District) — Centennial / Aurora / Littleton; Word-format chambers-copy convention |
| `co-county-courts` | Roll-up: 1st (Jefferson), 4th (El Paso), 17th (Adams + Broomfield), 20th (Boulder), 8th (Larimer), 19th (Weld), 10th (Pueblo), 21st (Mesa), Douglas (currently 18th, future 23rd JD); county-court limited-jurisdiction practice under C.R.C.P. 301-411; small claims under C.R.C.P. 501-521 |
| `co-pro-se` | pro-se drafting framework; "Self-Represented" designation; CCEFS Pro Se; JDF forms catalog; Self-Help Center directory |
| `co-law-references` | C.R.C.P., CRE, fees and costs, citation format, local rules — **canonical reference corpora live here** |
| `co-discovery` | C.R.C.P. 26-37; 25-interrogatory presumptive cap; C.R.C.P. 121 § 1-15(8) and § 1-12 conferral; county-court C.R.C.P. 311 simplified discovery |
| `co-hearings` | Oral argument; Cisco Webex statewide protocol; tentative rulings; evidentiary-hearing prep |
| `co-post-judgment` | C.R.C.P. 59 / 60(b); C.R.S. § 13-54.5 garnishment regime; expanded SB22-086 exemptions including $250k homestead; C.R.C.P. 69 supplemental proceedings |
| `co-first-30-days` | 21-day answer under C.R.C.P. 12(a)(1); *Warne v. Hall* Twombly/Iqbal-equivalent pleading standard; affirmative defenses catalog; compulsory counterclaims |
| `co-fact-check` | Citation verification; Colorado neutral-citation format (post-2012 `[YEAR] CO [###]` / `[YEAR] COA [###]`); packet consistency; sworn-vs-argued alignment |
| `co-deadlines` | C.R.C.P. 6 with C.R.S. § 24-11-101 holidays (including Juneteenth added 2022 by SB22-228 and Frances Xavier Cabrini Day replacing Columbus Day in 2020 by H.B. 20-1031) |
| `co-draft-motion` / `-declaration` / `-note` / `-order` | Scaffolders; C.R.C.P. 121 § 1-15 page limits (15/15/10); C.R.S. § 13-27-104 declaration verification language |
| `co-quality-check` | Pre-filing format + content QC (CJD 11-01 + pro-se drafting framework) |
| `co-schedule-hearing` | Chambers-email / JA contact templates per JD; court issues Notice of Setting (parties do not self-schedule) |
| `co-file-packet` | CCEFS workflow; document codes; C.R.S. art. 32 of title 13 filing-fee schedule; JDF 205/206 fee waiver |
| `co-submit-order` | Post-hearing signed-order transmittal; Word-format chambers-copy email protocol; agreed-form orders |
| `co-consumer-debt` | Subject bundle: FDCPA, Reg F, **CFDCPA (C.R.S. art. 16 of title 5, recodified from Title 12 in 2022)**, **Colorado Consumer Protection Act (C.R.S. art. 1 of title 6) with treble damages + mandatory fees**, **Uniform Consumer Credit Code (C.R.S. art. 1-9 of title 5)**, Colorado collection-agency licensure under C.R.S. § 5-16-115, chain-of-title under Colorado UCC Article 9, 6-year SOL on liquidated debt under C.R.S. § 13-80-103.5(1)(a) (Hassler v. Account Brokers, 2012 CO 24) |
| `co-family-law` | Subject bundle: UDMA (C.R.S. art. 10 of title 14); 91-day residency + 91-day waiting period under § 14-10-106; dissolution / legal separation under § 14-10-106; declaration of invalidity (annulment) under § 14-10-111 with the narrow grounds catalog; C.R.C.P. 16.2 mandatory financial disclosures with Sworn Financial Statement (JDF 1111); allocation of parental responsibilities under § 14-10-124 with decision-making and parenting time; § 14-10-115 income-shares child-support guideline with the 93-overnight rule, JDF 1820 E worksheet, and imputation-of-income standard; maintenance under § 14-10-114 (2014 + 2024 reforms); modification under § 14-10-122 (10% threshold for child support); common-law marriage under *People v. Lucero* (1987) as modernized by *In re Marriage of Hogsett & Neale*, 2021 CO 1; UCCJEA at C.R.S. art. 13 of title 14 |

Colorado is the first state plugin to ship with **two** subject-matter bundles in its initial release (consumer-debt + family-law) and therefore has 22 skills rather than the 21-skill default.

## Reference corpora — Washington (`wa-law-references/references/`)

Verbatim text pulled from official sources, organized by domain:

- **`court-rules/`** — 1,233 WA court rules across 35 sets (CR, CRLJ, ER, GR, RAP, etc.) extracted from courts.wa.gov PDFs.
- **`federal-debt-laws/`** *(symlink)* — points into `claude-legal-federal-laws/references/federal-debt-laws/`. **20 sources**: FDCPA, FCRA, TILA, ECOA, EFTA, CCPA-Garnishment (15 U.S.C. §§ 1671-1677), **RESPA (12 U.S.C. §§ 2601-2617), SCRA (50 U.S.C. ch 50), FHA (42 U.S.C. ch 45 subch I), FTC Telemarketing Sales Rule (16 C.F.R. Part 310)**, plus CFPB Reg B / E / F / M / N / P / V / X / Z / DD from `uscode.house.gov` USLM XML and the eCFR Versioner API.
- **`federal-bankruptcy/`** *(symlink)* — points into `claude-legal-federal-laws/references/federal-bankruptcy/`. **8 chapters** of Title 11 U.S.C.: Chapter 1 (General), 3 (Case Administration), 5 (Creditors / Debtor / Estate), 7 (Liquidation), 11 (Reorganization), 12 (Family Farmer / Fisherman), 13 (Adjustment of Debts), 15 (Cross-Border).
- **`ucc-model/`** *(symlink)* — points into `claude-legal-federal-laws/references/ucc-model/`. Model UCC Articles 1, 2, 3, 9 (Cornell LII).
- **`wa-rcw-debt/`** — **1,547 sections across 75 RCW chapters** covering full civil practice (procedure, evidence, special proceedings, family law, landlord-tenant, real property, business regulation, admin law, UCC, public-records, vulnerable-adults) from `app.leg.wa.gov`. Directory name retained for path stability; scope is no longer "debt-only" despite the slug.
- **`legal-data-apis.md`** — agent-facing index of the structured APIs above.
- **`online-sources.md`** — canonical human-facing URLs for the same sources.

## Reference corpora — Oregon (`or-law-references/references/`)

Mirrors the WA corpora structure; populated by future pull scripts (initial PR ships scaffolding + READMEs + manifests):

- **`court-rules/`** — Oregon court rules (ORCP, UTCR, OEC, ORAP, Multnomah SLR, Washington Co SLR) from counciloncourtprocedures.org and courts.oregon.gov.
- **`federal-debt-laws/`** *(symlink)* — points into `claude-legal-federal-laws/references/federal-debt-laws/`.
- **`federal-bankruptcy/`** *(symlink)* — points into `claude-legal-federal-laws/references/federal-bankruptcy/`.
- **`ucc-model/`** *(symlink)* — points into `claude-legal-federal-laws/references/ucc-model/`.
- **`or-ors-debt/`** — **35 ORS chapters / ~5.6 MB** covering full civil practice. The original debt-focused set (ORS 12, 14, 18, 19, 20, 21, 36, 40, 71-79, 82, 90, 105, 174, 187, 646, 697) plus chapters 32 (Injunctions, repealed-stub), 33 (Contempt), 41 (Evidence framework), 79A (UCC Article 9 — renumbered from 79 in 2025), 86 (Mortgages and trust deeds), 87 (Liens), 88 (Foreclosure), 100 (Condominiums), 107 (Dissolution / family law), 109 (Parent and child), 116 (Probate procedure), 124 (Vulnerable persons), 165 (Forgery / theft / fraud), 192 (Public records and meetings), 657 (Unemployment insurance), 659A (Employment discrimination). Directory name retained for path stability.
- **`legal-data-apis.md`** — Oregon-flavored agent-facing API index (oregonlegislature.gov, CourtListener Oregon courts, etc.).
- **`online-sources.md`** — canonical URLs for Oregon law.

Each corpus dir has its own `README.md` with citation tables and a "re-pull" command. The `scripts/pull_*.py` are reusable across plugins; they are wired into the quarterly remote-agent routine (`trig_018yahbiUwS1uTUJSuDNrCqG`) which runs Jan/Apr/Jul/Oct 1 at 17:00 UTC and opens a single PR if anything changed.

## Reference corpora — California (`ca-law-references/references/`)

Mirrors the WA/OR corpora structure:

- **`court-rules/`** — California Rules of Court (CRC) **Titles 1, 2, 3, 4, 5, 7, 8, 9, 10** + the California Evidence Code summary + LASC / SFSC / OCSC / other-county local rules + California Rules of Professional Conduct. Titles 2/3/5/7/8 are hand-authored curated commentary (Overview + Division headings + key-rule summaries); Titles 1/4/9/10 are puller-verbatim full rule text from `pull_ca_court_rules.py` against `courts.ca.gov/cms/rules/index/<word>`. Re-pulling 2/3/5/7/8 would replace the curated commentary with verbatim text — gated by a `--only` flag for safety.
- **`federal-debt-laws/`** *(symlink)* — points into `claude-legal-federal-laws/references/federal-debt-laws/`.
- **`federal-bankruptcy/`** *(symlink)* — points into `claude-legal-federal-laws/references/federal-bankruptcy/`.
- **`ucc-model/`** *(symlink)* — points into `claude-legal-federal-laws/references/ucc-model/`.
- **`ca-statutes-debt/`** — **32 files / ~724 KB** covering CA statutory civil practice. Original debt-focused set (CCP SOL / service / pleadings / motions / discovery / relief / enforcement / exemptions; Civ. Code Rosenthal / FDBPA / CLRA / atty-fees; B&P UCL; Fin. Code CDCLA; Comm. Code UCC Articles 2/3/9 as enacted) plus 14 civil-practice expansion groups: CCP-Trial-New-JNOV (§§ 657-663a), CCP-Writs (§§ 1085-1097), CCP-Unlawful-Detainer (§§ 1159-1179), CCP-Arbitration (§§ 1280-1294.2), CivCode-Contracts (§§ 1549-1692), CivCode-Damages (§§ 3274-3359), CivCode-Song-Beverly (§§ 1790-1795.8), EvidCode-Key (relevance / hearsay / authentication / best evidence), FamCode-Dissolution / FamCode-Property / FamCode-Custody / FamCode-Support, ProbCode-Basics, LabCode-Wages.

CA pull scripts: `scripts/pull_ca_court_rules.py` fetches CRC Titles 1-10 from courts.ca.gov; `scripts/pull_ca_statutes.py` fetches the configured CCP / Civ. Code / B&P / Fin. Code / Comm. Code sections from leginfo.legislature.ca.gov. Both follow the same pattern as the WA pullers (`pull_court_rules.py`, `pull_wa_rcw.py`).

## Reference corpora — Colorado (`co-law-references/references/`)

Mirrors the WA/OR/CA corpora structure:

- **`court-rules/`** — Colorado court rules (C.R.C.P. with the streamlined Chapter 18 county-court rules and Chapter 25 small-claims rules, CRE, C.A.R., Colorado Rules of Professional Conduct, Chief Justice Directives including CJD 11-01) — to be populated by a future `pull_co_court_rules.py` against the Colorado Judicial Branch publication source.
- **`federal-debt-laws/`** *(symlink)* — points into `claude-legal-federal-laws/references/federal-debt-laws/`.
- **`federal-bankruptcy/`** *(symlink)* — points into `claude-legal-federal-laws/references/federal-bankruptcy/`.
- **`ucc-model/`** *(symlink)* — points into `claude-legal-federal-laws/references/ucc-model/`.
- **`co-statutes-debt/`** — **14 articles / ~2.0 MB** of verbatim C.R.S. content fetched by `scripts/pull_co_statutes.py` from the official Colorado General Assembly C.R.S. PDFs at `content.leg.colorado.gov`. Articles: 4-9 (UCC Article 9), 5-1 (UCCC general), 5-16 (CFDCPA), 6-1 (CCPA — 643 KB), 13-22 (Mediation / ADR), 13-50 (Judgments — joint rights), 13-52 (Judgment enforcement), 13-54 (Exemptions), 13-54.5 (Garnishment), 13-80 (Limitations), 13-90 (Witnesses), 14-10 (UDMA — 362 KB; the chapter `co-family-law` already cited), 14-13 (UCCJEA), 24-4 (State APA).

CO pull scripts:

- **`scripts/pull_co_statutes.py`** — fetches C.R.S. title PDFs from `content.leg.colorado.gov`, runs `pdftotext -layout`, slices by `ARTICLE N` headers, and emits one MD file per article with `## § NN-N-NNN. Title` section headings. Includes `http_get_bytes()` retry helper (3 retries with exponential backoff) and atomic tmp-rename writes. Wired into the quarterly `refresh-references` workflow under `target=co`.
- `scripts/pull_co_court_rules.py` — TODO; would fetch C.R.C.P., CRE, C.A.R., and CJDs from coloradojudicial.gov.

## Common commands

```bash
# Lint every SKILL.md in the marketplace (frontmatter + name/dir match)
python3 scripts/lint-skills.py

# Install the pre-commit hook (one-time, per checkout)
ln -sf ../../scripts/hooks/pre-commit .git/hooks/pre-commit

# Refresh reference corpora — Washington (need: python3.10+, poppler for court-rules)
brew install poppler   # one-time
python3 scripts/pull_court_rules.py --workers 12 \
  --manifest plugins/wa-court-docs/skills/wa-law-references/references/court-rules/_manifest.json
python3 scripts/pull_federal_debt_laws.py
python3 scripts/pull_ucc.py --workers 8
python3 scripts/pull_wa_rcw.py --workers 12

# Refresh reference corpora — Oregon (pull scripts to be added in a follow-up PR):
# python3 scripts/pull_oregon_rules.py --workers 12 \
#   --manifest plugins/or-court-docs/skills/or-law-references/references/court-rules/_manifest.json
# python3 scripts/pull_oregon_ors.py --workers 12 \
#   --manifest plugins/or-court-docs/skills/or-law-references/references/or-ors-debt/_manifest.json

# Plugin-internal helpers (used by certain skills)
python3 plugins/wa-court-docs/scripts/format-check.py <file>   # GR 14 compliance
python3 plugins/wa-court-docs/scripts/case-calendar.py ...     # CR 6 deadline arithmetic
python3 plugins/or-court-docs/scripts/format-check.py <file>   # UTCR 2.010 compliance
python3 plugins/or-court-docs/scripts/case-calendar.py ...     # ORCP 10 deadline arithmetic with ORS 187 holidays

# Refresh reference corpora — California
python3 scripts/pull_ca_court_rules.py --workers 8 \
  --out plugins/ca-court-docs/skills/ca-law-references/references/court-rules
python3 scripts/pull_ca_statutes.py --workers 8 \
  --out plugins/ca-court-docs/skills/ca-law-references/references/ca-statutes-debt

# California scripts
python3 plugins/ca-court-docs/scripts/format-check.py <file>   # CRC 2.100-2.119 compliance
python3 plugins/ca-court-docs/scripts/case-calendar.py ...     # CCP § 12 deadline arithmetic with Govt. Code § 6700 holidays

# Colorado scripts
python3 plugins/co-court-docs/scripts/format-check.py <file>   # C.R.C.P. 10 + CJD 11-01 compliance
python3 plugins/co-court-docs/scripts/case-calendar.py ...     # C.R.C.P. 6 deadline arithmetic with C.R.S. § 24-11-101 holidays
python3 plugins/co-court-docs/scripts/case-calendar.py --rules # List Colorado named deadline rules
```

The lint also runs in CI on every push/PR (`.github/workflows/lint-skills.yml`).

## Versioning — three levels

There are three independent version fields. Bump only what changed.

| File | Field | When to bump |
|---|---|---|
| `.claude-plugin/marketplace.json` | `metadata.version` | When the marketplace's plugin set, descriptions, or category data changes (e.g., adding a new plugin, materially rewriting an existing plugin's listing copy). |
| `plugins/<plugin>/.claude-plugin/plugin.json` | `version` | When **anything** in the plugin changes that a downstream installer might care about — new skill, removed skill, changed skill description triggers, new reference corpus, bumped plugin keywords. This is the version users will see installed. |
| `plugins/<plugin>/skills/<skill>/SKILL.md` | `version:` (frontmatter) | When that **specific** skill's content, body instructions, or trigger phrases change. Adding/removing files under that skill's `references/` counts. Editing CLAUDE.md does not. |

### Semver mapping for this repo

- **PATCH** (`0.1.0 → 0.1.1`): typo fix, clarification, link repair, doc-only edit, refresh of an existing reference file with no semantic change.
- **MINOR** (`0.1.0 → 0.2.0`): new section in a skill, new reference file, new procedural feature, additional triggers in a skill description (additive — old triggers still work).
- **MAJOR** (`0.x.y → 1.0.0`, then `1.x → 2.0`): breaking change to a skill's contract or trigger phrases, removal/rename of a skill, removal/relocation of a reference path that other skills cite.

The repo is pre-1.0 across the board; staying in `0.x` while shape is settling is intentional. Bumps so far have all been MINOR/PATCH.

### Procedure for a version bump

1. Edit the affected skill / plugin / reference content first.
2. Bump the **most-specific** version that changed:
   - Edited `SKILL.md` body or its `references/` → bump that skill's `version:`.
   - Added/removed a skill, or changed `plugin.json` description/keywords → also bump `plugin.json`'s `version`.
   - Added a new plugin or rewrote marketplace-level descriptions → also bump `marketplace.json`'s `metadata.version`.
3. Run `python3 scripts/lint-skills.py` — must pass.
4. Commit. The pre-commit hook re-runs the linter; CI re-runs it on push.

### Versioning gotchas

- The linter requires `version:` to be **present** in every `SKILL.md`. It does **not** validate semver format — that's on the author.
- **`name:` in `SKILL.md` must equal the containing directory name.** Renaming a skill = rename the dir, update `name:`, then grep the repo for old references (other skills cross-link by name).
- Adding a new skill: lint-clean it locally before commit. The runtime ignores skills that fail to parse, but CI will fail loudly.

## Reference-corpus refresh discipline

When a `pull_*.py` script runs and the corpus changes:

- The diff lives entirely under the relevant `<plugin>/skills/<state>-law-references/references/<corpus>/` directory.
- Bump the relevant `<state>-law-references` `SKILL.md` `version:` (PATCH for routine refresh, MINOR if a new corpus dir was added).
- Do **not** also bump `plugin.json` for a routine corpus refresh; reserve plugin-version bumps for things that change which skills exist.

The quarterly agent routine handles this automatically — it stages only the references dirs and opens a PR. When reviewing that PR, decide whether the bump is PATCH (routine refresh) or MINOR (e.g., new release point worth flagging) and edit the SKILL.md before merging.

## Cross-state architecture notes

When adding a new state plugin, the WA / OR pair establishes the pattern:

1. **Naming**: `<state>-court-docs` (e.g., `ca-court-docs`, `tx-court-docs`).
2. **Skill naming**: `<state>-<role>` for procedural skills (e.g., `ca-statewide-format`); `<state>-<court>` for court-specific skills (e.g., `ca-lasc` for Los Angeles Superior Court).
3. **Subject-matter bundles**: `<state>-<topic>` (e.g., `ca-consumer-debt`).
4. **Reference structure**: mirror the corpus directories (`court-rules/`, `federal-debt-laws/`, `ucc-model/`, `<state>-statutes-debt/`).
5. **Scripts**: `format-check.py` and `case-calendar.py` per plugin, parameterized to the state's format requirements and holidays.
6. **Federal law is shared content in a dedicated plugin**: the FDCPA/FCRA/TILA text, the Bankruptcy Code (Title 11 U.S.C.), and the model UCC live once in `plugins/claude-legal-federal-laws/references/`. Each state plugin's `references/federal-debt-laws/`, `references/federal-bankruptcy/`, and `references/ucc-model/` are **symlinks** into that shared plugin, and each state plugin's `plugin.json` declares `"dependencies": ["claude-legal-federal-laws"]`. The Claude Code marketplace runtime auto-installs the dependency and dereferences symlinks within a marketplace at install time (copying target content into the install cache), so each installed state plugin still has the federal content locally available. When adding a new state plugin, copy this dependency declaration + symlink pattern; do **not** copy the federal-debt-laws or federal-bankruptcy or ucc-model content directly.
7. **Procedural quirks should be flagged prominently** in the relevant skill descriptions: Oregon's no-interrogatories quirk is in `or-discovery`; California's CCP 437c summary judgment timing differs from FRCP, etc.

### Project skill for adding new states

A project-scoped skill lives at `.claude/skills/scaffold-state-plugin/`. When the user asks to add a new state plugin (California, Texas, Florida, New York, etc.), this skill is what the coding agent invokes. It contains:

- The 21-skill pattern derived from `wa-court-docs` and `or-court-docs`
- A scaffolder script (`scripts/scaffold-state.py`) that generates a lint-clean directory tree, plugin.json, copied scripts with TODO markers, and stubs for every SKILL.md
- A checklist for the manual content-authoring phase (`references/checklist.md`)
- A research protocol for gathering state-specific procedural rules (`references/state-research-protocol.md`)
- A cross-state quirks catalog so the agent knows which procedural distinctives to flag in the new plugin (`references/cross-state-quirks.md`)
- Skill templates for the highest-variance roles (`references/skill-templates/`)

The skill is **project-scoped** (in `.claude/skills/`), not a marketplace plugin — it is tooling for the coding agent maintaining the repo, not a deliverable for end users.

The scaffolder produces a lint-clean skeleton. The substantive law content for each SKILL.md and reference file must be researched and authored after scaffolding — do NOT search-and-replace from WA or OR.

## Repo layout (at a glance)

```
.claude-plugin/marketplace.json     # marketplace manifest (metadata.version)
.github/workflows/lint-skills.yml          # CI: runs lint on push/PR
.github/workflows/refresh-references.yml   # Quarterly cron + workflow_dispatch refresh
plugins/claude-legal-federal-laws/  # SHARED data-only plugin; depended on by every state plugin
  .claude-plugin/plugin.json        # version 0.1.0
  references/federal-debt-laws/     # FDCPA, FCRA, TILA, ECOA, Reg B/F/V/Z — canonical source
  references/ucc-model/             # Model UCC Articles 1, 2, 3, 9 — canonical source
plugins/wa-court-docs/
  .claude-plugin/plugin.json        # plugin manifest (version); declares dependencies: [claude-legal-federal-laws]
  skills/<skill>/SKILL.md           # one per skill (version: in frontmatter)
  skills/wa-law-references/references/
    federal-debt-laws -> ../../../../claude-legal-federal-laws/references/federal-debt-laws  (symlink)
    ucc-model         -> ../../../../claude-legal-federal-laws/references/ucc-model          (symlink)
    court-rules/, wa-rcw-debt/, etc.   # state-specific content stays in-plugin
  scripts/format-check.py           # GR 14 compliance
  scripts/case-calendar.py          # CR 6 deadline arithmetic
  evals/                            # drafting / formatting / procedural / subject-matter / integration
plugins/or-court-docs/              # same shape; declares dependencies: [claude-legal-federal-laws]
  .claude-plugin/plugin.json
  skills/<skill>/SKILL.md
  skills/or-law-references/references/
    federal-debt-laws -> ../../../../claude-legal-federal-laws/references/federal-debt-laws  (symlink)
    ucc-model         -> ../../../../claude-legal-federal-laws/references/ucc-model          (symlink)
    court-rules/, or-ors-debt/, etc.
  scripts/format-check.py           # UTCR 2.010 compliance
  scripts/case-calendar.py          # ORCP 10 deadline arithmetic with ORS 187 holidays
  evals/
plugins/ca-court-docs/              # scaffolded stubs (lint-clean; awaiting substantive content)
  .claude-plugin/plugin.json
  skills/<skill>/SKILL.md           # 21 stubs
  skills/ca-law-references/references/{court-rules,federal-debt-laws,ucc-model,ca-statutes-debt}/README.md
  scripts/format-check.py           # copied from or-court-docs; TODO-marked for CRC 2.100-2.119 adaptation
  scripts/case-calendar.py          # copied from or-court-docs; TODO-marked for CCP § 12 / Govt. Code § 6700
  evals/                            # empty drafting/formatting/procedural/subject-matter/integration dirs + stub README
plugins/co-court-docs/              # 22 skills (21 standard + co-family-law)
  .claude-plugin/plugin.json        # plugin manifest (version: 0.1.0)
  skills/<skill>/SKILL.md           # 22 SKILL.md files with substantive Colorado content
  skills/co-law-references/references/{court-rules,federal-debt-laws,ucc-model,co-statutes-debt}/README.md
  skills/co-family-law/references/examples/   # synthetic example filings dir
  scripts/format-check.py           # C.R.C.P. 10 + CJD 11-01 compliance
  scripts/case-calendar.py          # C.R.C.P. 6 deadline arithmetic with C.R.S. § 24-11-101 holidays
  evals/                            # five eval categories (drafting/formatting/procedural/subject-matter/integration); empty dirs + stub README
scripts/
  lint-skills.py                    # frontmatter + name/dir-match linter
  hooks/pre-commit                  # symlink target for .git/hooks/pre-commit
  pull_court_rules.py               # courts.wa.gov → wa court-rules/
  pull_federal_debt_laws.py         # uscode.house.gov + ecfr.gov → plugins/claude-legal-federal-laws/references/federal-debt-laws/
  pull_ucc.py                       # law.cornell.edu/ucc → plugins/claude-legal-federal-laws/references/ucc-model/
  pull_wa_rcw.py                    # app.leg.wa.gov → wa-rcw-debt/
  pull_ca_court_rules.py            # courts.ca.gov → ca court-rules/
  pull_ca_statutes.py               # leginfo.legislature.ca.gov → ca-statutes-debt/
  pull_co_statutes.py               # content.leg.colorado.gov C.R.S. PDFs → co-statutes-debt/
  # TODO: pull_oregon_rules.py       # counciloncourtprocedures.org + courts.oregon.gov → or court-rules/
  # TODO: pull_oregon_ors.py         # oregonlegislature.gov → or-ors-debt/  (OR ORS content currently maintained via ad-hoc agent fetches)
  # TODO: pull_co_court_rules.py     # coloradojudicial.gov → co court-rules/
```
