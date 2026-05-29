# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

The `claude-legal` **marketplace** — a Claude Code / Cowork marketplace of court-document plugins organized one plugin per state, plus two shared federal reference plugins (a debt/consumer-finance corpus + a nationwide FCRA consumer credit-report-rights skills layer, and an immigration-law corpus). It ships **ten plugins total — eight state plugins + two shared federal reference plugins**:

- **`claude-legal-immigration-laws`** — Shared, venue-independent reference plugin for U.S. immigration law (the federal counterpart to `claude-legal-federal-laws`, built for immigration practice). **Sources/reference plugin — references-only, no skills yet (like the federal plugin pre-v0.3.0).** Snapshots the canonical **rules** verbatim as Markdown via three pullers: the **INA** (`scripts/pull_ina.py` — 8 U.S.C. Chapter 12 from uscode.house.gov USLM XML, one file per subchapter I–V, with an INA-section ↔ 8 U.S.C.-section crosswalk in the corpus README), the immigration **regulations** (`scripts/pull_immigration_cfr.py` — curated 8 CFR DHS chapter I + EOIR chapter V (8 CFR 1001–1337, the immigration courts + Board of Immigration Appeals) + State Department 22 CFR visa/passport/exchange parts, from the eCFR versioner API), and the **Foreign Affairs Manual** (`scripts/pull_fam.py` — canonical-URL pointer stubs, because fam.state.gov serves an incomplete TLS certificate chain that the sandbox's TLS-inspecting egress proxy can't verify → HTTP 503; this is an egress/cert-chain issue, *not* destination bot-gating, so `curl_cffi` TLS-impersonation does not help — verbatim mirroring requires an egress that completes the chain; `_file_is_stub` guard preserves any later-mirrored verbatim text). **Case law is wired on-demand, not snapshotted** (immigration case law is too large/fast-moving to mirror): `references/legal-data-apis.md` + `references/online-sources.md` index the federal **circuit courts** (petitions for review of removal orders under INA § 242 / 8 U.S.C. § 1252, via CourtListener REST + the connected CourtListener MCP, with per-circuit `court` ids), the **Board of Immigration Appeals** precedent decisions (I&N Dec., via the EOIR Virtual Law Library), and the USCIS **Administrative Appeals Office (AAO)** decisions (website/PDF — no JSON API). Marketplace metadata bumped to 0.24.0 when this plugin was added.
- **`claude-legal-federal-laws`** — Shared plugin holding the canonical copy of federal U.S. debt-collection and consumer-finance law (FDCPA, FCRA, TILA, ECOA, Reg B/F/V/Z) and the model Uniform Commercial Code (Articles 1, 2, 3, 9). Every state plugin below declares this as a dependency and symlinks into its `references/` tree, so federal content lives in one place rather than being copy-pasted per state. **Was data-only through v0.3.0; as of v0.4.0 it also ships a nationwide, venue-independent consumer credit-report-rights skills layer** (5 skills) built on the FCRA: `consumer-report-ordering` (order all Big-3 + specialty CRA reports; free-report entitlements under § 1681j; private right of action for non-delivery), `consumer-credit-disputes` (lawful direct-to-CRA disputes under § 1681i via e-OSCAR/certified mail; the 4-business-day identity-theft block under § 1681c-2 with wet-ink affidavits; post-dispute multi-regulator escalation to defeat the bona fide error defense), `consumer-report-accuracy` (PII hygiene; the Date of First Delinquency clock + debt-buyer re-aging; the "disputed by consumer" scoring-exclusion flag), `consumer-harm-documentation` (communication logs with state-varying call-recording-consent caveats; damages ledgers including "firm books" postage/time tracking; harm-declaration scaffolds), and `consumer-credit-monitoring` (generating adverse-action proof; § 1681i(d) re-notification of everyone who pulled the report; fixed-date annual review of Big-3 + specialty reports; post-breach checklists). These are matter-neutral, state-independent self-help skills that produce documents (not advice) and compose with the per-state `*-consumer-debt` and `*-pro-se` skills. Because every state plugin depends on this plugin, the consumer skills are available anywhere any state plugin is installed.
- **`wa-court-docs`** — Washington State (GR 14 formatting; **30 SKILL.md files**; **6 venue skills** — King County District (`wa-kcdc`), King County Superior (`wa-kcsc`), Pierce County / Tacoma (`wa-pierce`), Snohomish County / Everett (`wa-snohomish`), Spokane County (`wa-spokane`), Superior Court Family Law Department (`wa-family-court`) — plus a long-tail roll-up (`wa-county-courts`); **six subject-matter bundles** — `wa-consumer-debt` (FDCPA + Reg F + RCW 19.16 + Washington CPA + chain of title), `wa-family-law` (Washington's community-property regime + RCW Title 26 dissolution / parenting / child support framework + the 2022 consolidated RCW 7.105 civil-protection-order regime + RCW 26.26A UPA parentage), `wa-landlord-tenant` (RCW 59.18 RLTA + the 2019 SB 5600 mandatory-form pay-or-vacate reform + the 2021 SB 5160 just-cause framework + HB 1815 statewide tenant Right to Counsel + ERP), `wa-personal-injury` (RCW 4.22 pure comparative fault + several-liability post-1986 Reform Act + WPLA at RCW 7.72 + medical malpractice at RCW 7.70 + RCW 4.92 / 4.96 Notice of Tort Claim), `wa-employment` (Minimum Wage Act + WLAD at RCW 49.60 + PFML under RCW Title 50A + Paid Sick Leave + non-compete reform at RCW 49.62 + L&I exclusive remedy under RCW 51), and `wa-commercial-disputes` (Washington CPA at RCW 19.86 with the *Hangman Ridge* 5-element test + WBCA at RCW 23B + WA LLC Act at RCW 25.15 + UCC at RCW 62A + MAR under RCW 7.06)). **WA pioneers the "thin-skill" architecture**: SKILL.md bodies describe procedural frameworks and point at the references corpus for current statutory text, dollar thresholds, day counts, and section subsections rather than embedding them — so the quarterly RCW puller can update canonical law without requiring SKILL.md edits.
- **`or-court-docs`** — Oregon (UTCR 2.010 formatting, Multnomah + Washington County Circuit Court + populous-counties roll-up, ORS 697 / UTPA consumer-debt bundle).
- **`ca-court-docs`** — California (CRC 2.100-2.119 formatting, LASC + SFSC + populous-counties roll-up, Rosenthal Act / FDBPA / CDCLA consumer-debt bundle). All 21 SKILL.md files authored with CA-specific substance; reference corpora include the shared `federal-debt-laws/` + `ucc-model/` content via the `claude-legal-federal-laws` dependency, the CA-specific `ca-statutes-debt/` (Rosenthal Act, FDBPA, CDCLA, UCL, CLRA, CCP procedural sections, Cal. Comm. Code UCC enactments), and the CA `court-rules/` corpus (CRC Titles 2/3/5/7/8, Cal. Evid. Code, LASC + SFSC + OCSC local rules).
- **`co-court-docs`** — Colorado (C.R.C.P. 10 + Chief Justice Directive 11-01 formatting with the two-block caption + case-number/division/courtroom box, Denver District Court / 2nd JD + Arapahoe County District Court / 18th JD + populous-counties roll-up, CFDCPA / CCPA / UCCC consumer-debt bundle, **plus a Colorado-specific family-law bundle** — `co-family-law` — covering UDMA dissolution / annulment, child support under C.R.S. § 14-10-115 with the 93-overnight rule, parental responsibilities under C.R.S. § 14-10-124, maintenance under C.R.S. § 14-10-114, and common-law marriage under *People v. Lucero* / *Hogsett & Neale*). Colorado was the **first state plugin to ship with two subject-matter bundles in its initial release** — consumer-debt and family-law — for a total of **22 SKILL.md files**.
- **`in-court-docs`** — Indiana (Indiana Trial Rule 5(E) format, Marion Superior Court / Indianapolis + Lake Superior Court / Crown Point + populous-counties roll-up including Bartholomew Circuit Court, IUCCC / DCSA consumer-debt bundle leaning on chain-of-title + FDCPA since Indiana has no collection-agency licensing regime; **plus an in-family-court venue skill + in-family-law subject bundle** covering paternity at IC 31-14 — the **JP case-type backbone** for non-marital children — dissolution at IC 31-15 under Indiana's **equitable-distribution** regime, child support at IC 31-16 with the Indiana Child Support Guidelines court rule, custody and parenting time at IC 31-17 with the Indiana Parenting Time Guidelines court rule, adoption at IC 31-19, UCCJEA at IC 31-21, DCS / CHINS / TPR / delinquency at IC 31-25 / 30 / 32 / 34 / 35 / 37, and protection orders at IC 34-26-5. Family-court topology: Indiana has no separate Family Court trial court; large counties (Marion, Lake, Allen, Hamilton, St. Joseph, Vanderburgh) have a dedicated Juvenile Division; smaller counties like Bartholomew consolidate JP / DC / DR jurisdiction in the Circuit Court. 23 SKILL.md files total). Architected with the *Jarboe v. Landmark* summary-judgment standard and the unique T.R. 59 motion-to-correct-error procedure flagged prominently. Follows the thin-skill architecture — chapter pointers + procedural frameworks, with current statutory text + thresholds + day counts living in the references corpus.
- **`ny-court-docs`** — New York (22 NYCRR § 202.5 paper format + 22 NYCRR § 202.5-b NYSCEF e-filing format with the New York caption and "-against-" party separator; broadest civil-court venue coverage in the marketplace — **five flagship Supreme Court venues each as its own skill** — New York County / 1st JD / Manhattan with the $500k-threshold Commercial Division, Kings County / 2nd JD / Brooklyn with the CPLR 3408 foreclosure conference part, Bronx County / 12th JD, Nassau County / 10th JD / Mineola with a $200k-threshold Commercial Division, Queens County / 11th JD / Jamaica — **plus two dedicated Long Island District Court skills** (`ny-nassau-dc` and `ny-suffolk-dc`) covering the Uniform District Court Act / 22 NYCRR Part 212 forum (civil jurisdiction up to $15,000, L&T summary proceedings under RPAPL Article 7, the primary pro-se debt-defense forum on Long Island) that doesn't exist anywhere else in the state — plus dedicated venue skills for the rest of NY's fragmented civil-court system — `ny-nyc-civil-court` (Civil Court Act $50k cap, 5 borough branches, the highest-volume consumer-debt forum in the country with 22 NYCRR § 208.6-a default-scrutiny), `ny-nyc-housing-court` (Housing Part of NYC Civil Court — RPAPL Article 7 summary proceedings + Local Law 136 universal Right to Counsel + ERAP stays), `ny-city-courts` (~60 upstate City Courts under UCCA / 22 NYCRR Part 210, $15k cap), `ny-justice-courts` (~1,250 Town & Village Justice Courts under UJCA / 22 NYCRR Part 214, $3k cap), `ny-family-court` (FCA: custody, support, family-offense, PINS, abuse/neglect) — plus a long-tail Supreme Court roll-up (`ny-county-courts`) for Suffolk / Westchester / Erie / Monroe / Onondaga / Richmond / Rockland / Albany / Orange / Dutchess / Saratoga / Oneida Supreme Court Civil Term; **five subject-matter bundles**: `ny-consumer-debt` (FDCPA / Reg F / 2022 CCFA / GBL § 600 / GBL § 349 / CPLR 4544 / UCC Article 9 chain of title), `ny-landlord-tenant` (RPAPL Article 7 / 2019 HSTPA / 2024 Good Cause / RPL § 235-b / Local Law 136 / ERAP), `ny-personal-injury` (CPLR Article 14-A pure comparative fault, no-fault § 5102(d), Labor Law § 240(1) scaffold law, GML § 50-e Notice of Claim, CPLR 214-a medical malpractice, CVA / ASA revival windows), `ny-employment` (NYS HRL, NYC HRL with mandatory attorney's fees, Labor Law § 191/198/740, WARN Act, CROWN Act, 2018 Sexual Harassment Act), `ny-commercial-disputes` (22 NYCRR § 202.70 Commercial Division, CPLR 3016(b) fraud particularity, BCL § 1104-a judicial dissolution, GOL §§ 5-1401/5-1402 NY-as-destination-forum, Faithless Servant Doctrine)). New York ships with **35 SKILL.md files** — the largest state plugin to date — because of the five flagship Supreme Court skills, the two dedicated Long Island District Court skills, the two NYC Civil/Housing Court skills, the upstate City + Justice Court roll-ups, the Family Court skill, and **five subject-matter bundles** (consumer-debt + landlord-tenant + personal-injury + employment + commercial-disputes).

- **`oh-court-docs`** — Ohio (Ohio Civ. R. 10 + per-court local rules; eight flagship Court of Common Pleas venues each as its own skill — Cuyahoga (Cleveland), Franklin (Columbus), Hamilton (Cincinnati), Summit (Akron), Montgomery (Dayton), Lucas (Toledo), Stark (Canton), Butler (Hamilton, OH) — plus a county-courts roll-up for the other 80 counties, a dedicated `oh-municipal-courts` skill (R.C. Chapter 1901, $15,000 civil cap + $6,000 small-claims), and `oh-family-court` covering both the Domestic Relations Division (divorce + married-parent custody/support under R.C. Chapter 3105 + 3109) and the Juvenile Division (unmarried-parent custody + child-support enforcement + abuse/neglect under R.C. Chapter 2151). Two baseline subject bundles: `oh-consumer-debt` (FDCPA + Reg F + Ohio Consumer Sales Practices Act under R.C. Chapter 1345 with R.C. 1345.09 treble damages + mandatory attorney's fees + R.C. 2305.06 six-year written-contract SOL + chain of title under Ohio UCC Article 9 at R.C. Chapter 1309; **no Ohio collection-agency licensing regime** — debt-buyer cases lean on chain-of-title + FDCPA); `oh-family-law` (R.C. Chapter 3105 divorce + equitable distribution at R.C. 3105.171 (NOT community property) + R.C. Chapter 3119 income-shares child-support guidelines with $300,000 combined-income cap + R.C. 3105.18 spousal support + R.C. Chapter 3127 UCCJEA + R.C. Chapter 3115 UIFSA). 30 SKILL.md files. Ohio public-domain citation `YYYY-Ohio-NNNN` mandatory in appellate cases since 2002.

- **`tn-court-docs`** — Tennessee. Tennessee has **no single statewide page/margin/font rule** — form of pleadings is governed by Tenn. R. Civ. P. 10 (caption + numbered paragraphs + exhibits) and Rule 11 (signature with the attorney's Board of Professional Responsibility number), and page limits/typography come from each court's **local rules** (indexed at the AOC "Local Rules of Practice" page, tncourts.gov; canonical per-county pointers for Davidson/Shelby/Knox/Hamilton + General Sessions + Juvenile live at `tn-law-references/references/court-rules/Tenn-Local-Rules-Practice.md`). Covers Tennessee's three trial-court layers — **Circuit Court** (law), **Chancery Court** (equity, with the Tennessee-distinctive Clerk & Master and Chancellor titles), and the limited-jurisdiction **General Sessions Court**, the dominant consumer-debt and eviction forum ($25,000 civil cap under Tenn. Code Ann. § 16-15-501, unlimited detainer jurisdiction, informal procedure with no formal discovery as of right, suit commenced by a **civil warrant**, and a **10-day de novo appeal to Circuit Court** under § 27-5-108). Ships dedicated venue skills for the four largest counties — Davidson (Nashville, 20th JD, Metro consolidated government, eFileTN/Odyssey Chancery), Shelby (Memphis, 30th JD, eFlex), Knox (Knoxville, 6th JD), Hamilton (Chattanooga, 11th JD) — plus a `tn-general-sessions` skill, a county-courts roll-up, and **split family-forum skills** (`tn-family-court` for Circuit/Chancery divorce + `tn-juvenile-court` for Title 37 paternity / dependency / TPR). **Six subject-matter bundles**: `tn-consumer-debt` (FDCPA + Reg F + the **Tennessee Consumer Protection Act** at § 47-18-101 with the *Pursell v. First American National Bank*, 937 S.W.2d 838 (Tenn. 1996) rule that the TCPA generally does not reach the act of collecting a debt + the **Tennessee Collection Service Act** licensing regime at Title 62 ch. 20 + the **2024 § 20-6-104 debt-buyer pre-default-judgment documentation requirement** + chain of title under Tennessee UCC Article 9 + the 6-year written-contract SOL at § 28-3-109 / 4-year goods SOL at § 47-2-725); `tn-family-law` (Title 36 — **equitable distribution** at § 36-4-121 (NOT community property) + the 60/90-day irreconcilable-differences waiting period at § 36-4-103 + **income-shares** child support at § 36-5-101 with Tenn. Comp. R. & Regs. ch. 1240-02-04 + the **four Tennessee alimony types** at § 36-5-121 + permanent parenting plans at § 36-6-401 with the 2018 relocation framework at § 36-6-108 + UCCJEA at § 36-6-201 + UIFSA at § 36-5-2001); `tn-landlord-tenant` (the **URLTA** at § 66-28-101 applicable in counties over 75,000 population + non-URLTA counties at § 66-7-101 + the 14-day nonpayment notice at § 66-28-505 + detainer-warrant practice at § 29-18-101 with the 10-day de novo appeal + the **CARES Act § 4024(c) 30-day notice overlay** for federally-subsidized properties confirmed by *Schiminger v. Cooperage Project, LLC* (Tenn. App. 2024) + the **self-help eviction prohibition** at § 66-28-504 with 3-months-or-3x-actual-damages remedy + the § 66-28-514 **retaliation presumption** within 1 year of protected activity + security-deposit forfeiture under § 66-28-301(g)); `tn-personal-injury` (*McIntyre v. Balentine*, 833 S.W.2d 52 (Tenn. 1992) **modified comparative fault** with the 49% bar + **several liability** post-*McIntyre* for non-intentional torts + the 1-year tort SOL at § 28-3-104 + the **Governmental Tort Liability Act** at § 29-20-101 with $300k/$700k caps under § 29-20-403, shortened ~12-month SOL under § 29-20-305, **bench trial under § 29-20-307**, and the immunity-removal-category framework + the **Health Care Liability Act** 60-day pre-suit notice + certificate of good faith at § 29-26-121/-122 with the contiguous-state expert rule under § 29-26-115 and the 3-year statute of repose under § 29-26-116 not extended by pre-suit notice + the **2011 tort-reform damages caps** at § 29-39-102 (non-economic $750k/$1M catastrophic) and § 29-39-104 (punitive greater of $500k or 2x compensatory) upheld in *McClay v. Airport Management Services, LLC*, 596 S.W.3d 686 (Tenn. 2020) + the **TPLA 10-year statute of repose** at § 29-28-103 + wrongful death at § 20-5-106 with *Jordan v. Baptist Three Rivers Hospital*, 984 S.W.2d 593 (Tenn. 1999) emotional damages + the **dual-regime dog-bite statute** at § 44-8-413 + UM/UIM service under § 56-7-1206); `tn-employment` (**Tennessee Human Rights Act** at § 4-21-101 with **8+ employee** coverage threshold under § 4-21-102(5) and **1-year judicial SOL** at § 4-21-311 with mandatory attorney's fees and 180-day administrative window to THRC at § 4-21-302 + **Tennessee Disability Act** at § 8-50-103 + the **Tennessee Public Protection Act** whistleblower regime at § 50-1-304 with the strict "**sole reason**" element confirmed in *Williams v. City of Burns*, 465 S.W.3d 96 (Tenn. 2015) + the **Wage Regulation Act** at § 50-2-101 (no state minimum wage — FLSA $7.25 applies; final-wage timing at § 50-2-103 within 21 days; willful-nonpayment liquidated damages) + Tennessee's **right-to-work** statute at § 50-1-201 constitutionalized by the Nov. 2022 Tenn. Const. art. XI § 21 amendment + common-law non-compete enforceability under *Murfreesboro Medical Clinic v. Udom*, 166 S.W.3d 674 (Tenn. 2005) + the **workers'-compensation** exclusive-remedy regime at § 50-6-101 with the **post-7/1/14 forum split** to the **Court of Workers' Compensation Claims (CWCC)** under § 50-6-237 — Chancery retains jurisdiction for pre-7/1/14 injuries); and `tn-commercial-disputes` (the **Chancery Court** as Tennessee's principal commercial-equity forum + the **Davidson Business Court** program in the 20th JD + the **TCPA *Pursell* B2B exclusion** that defeats most business-to-business deceptive-act claims + the **Tennessee Uniform Trade Secrets Act (TUTSA)** at § 47-25-1701 with reasonable-royalty fallback and exemplary-damages-up-to-2x-compensatory + the **Uniform Voidable Transactions Act** (formerly TUFTA) at § 66-3-301 + the **Tennessee Revised LLC Act** at § 48-249-101 + the **Tennessee Business Corporation Act** at § 48-11-101 with the 1998 demand-required-no-futility reform for derivative actions + **Rule 9.02 fraud-with-particularity** pleading + business torts (tortious interference, civil conspiracy, conversion) + the **Tennessee Uniform Arbitration Act** at § 29-5-301 with FAA preemption practice + the **Tennessee Securities Act** at § 48-1-101). The *Rye v. Women's Care Center of Memphis*, 477 S.W.3d 235 (Tenn. 2015) *Celotex*-style summary-judgment standard is flagged in the motion skills; the case-calendar script encodes the § 15-1-101 holidays (Tennessee observes **Good Friday** and **Columbus Day**). **31 SKILL.md files**.

All eight state plugins are architected identically: matter-neutral civil-procedure skills plus subject-matter bundles (consumer-debt + family-law in each state, with additional subject bundles where the state's civil practice justifies them). The structure leaves clean slots for plugins covering additional states.

Output is documents, not advice; everything is bracketed by a "not legal advice" disclaimer that downstream skills repeat.

> **NOT LEGAL ADVICE.** Generated content is a drafting aid; verify against current rules and case law before filing.

## Big-picture architecture

Three layers, three things to know:

1. **Marketplace → Plugin → Skill.** Two manifests (`.claude-plugin/marketplace.json` at repo root, `plugins/<plugin>/.claude-plugin/plugin.json` per plugin) plus per-skill `SKILL.md` files. The runtime loads skills by their **directory name**; the `name:` field in `SKILL.md` frontmatter must match the directory exactly or the skill won't load. The linter enforces this.

2. **Skills only — no slash commands.** Every workflow is a skill auto-invoked from natural-language triggers in its `description:` frontmatter. When adding a workflow, write it as a skill; do not add a slash command.

3. **Matter-neutral procedural skills + subject-matter bundles.** The procedural skills (statewide-format, discovery, hearings, fact-check, deadlines, draft-* skills, etc.) know nothing about a specific area of law. Subject-matter bundles (`wa-consumer-debt`, `or-consumer-debt`; landlord-tenant / family / PI are the future slots) plug into them via composition. Don't bake subject-matter law into procedural skills.

**County coverage is skills inside the state plugin, not separate plugins.** One plugin per state; within it, a high-volume court can get its own skill (`wa-kcdc` for King County District Court, `wa-kcsc` for King County Superior Court, `or-multcc` for Multnomah Circuit, `or-wccc` for Washington County Circuit), and the long tail of counties is carried as a single roll-up skill plus reference data (`wa-county-courts`, `or-county-courts`). Name court skills `<state>-<court>` (e.g., `wa-kcdc`, `or-multcc`) or use the state-level roll-up. Don't create a plugin or a skill per county — that doesn't scale to 3,000+ U.S. counties; add detail to the roll-up's reference files on demand.

## Skills index — Federal consumer credit-report rights (`claude-legal-federal-laws`, 5 skills)

State-independent, matter-neutral FCRA self-help skills. All cite the in-plugin
`references/federal-debt-laws/FCRA.md` via the relative path `../../references/federal-debt-laws/FCRA.md`
(no symlink — this is the home plugin). Each produces documents (not advice) and opens with the
`NOT LEGAL ADVICE` disclaimer.

| Skill | Role |
|---|---|
| `consumer-report-ordering` | Order all Big-3 + nationwide specialty CRA reports (CLUE, ChexSystems, MIB, NCTUE, tenant-screening, etc.); free-report entitlements (annual, post-adverse-action under § 1681j(b), data-breach / identity-theft / public-assistance / unemployment triggers); private right of action for non-delivery under §§ 1681n/1681o |
| `consumer-credit-disputes` | Lawful direct-to-CRA dispute under § 1681i (e-OSCAR / certified mail) — NOT a regulator complaint; 30-day (45 FACTA) clock; the 4-business-day identity-theft block under § 1681c-2 / trafficking § 1681c-3 with wet-ink (non-eSigned) affidavits; restart-if-not-lawful; credit-repair caution; post-dispute multi-regulator escalation to defeat the bona fide error defense |
| `consumer-report-accuracy` | PII hygiene (strip stale addresses/phones; request furnisher contact info when active reporting blocks removal); Date of First Delinquency as the ~7-year reporting + SOL clock (§ 1681c) and debt-buyer re-aging; the "disputed by consumer" scoring-exclusion flag; weekly-pull monitoring + sticky-note evidence organization |
| `consumer-harm-documentation` | Communication logs (with state-varying one-party/all-party call-recording-consent caveat); refusals-to-record + hang-ups as bad-faith evidence; harm taxonomy (interest, denials, insurance, jobs, eviction, time/postage via "firm books"); written cost breakdowns from creditors; emotional/physiological harm via providers + wearables; harm-declaration scaffold |
| `consumer-credit-monitoring` | Apply for credit in the last 3–6 months to generate adverse-action proof; § 1681i(d) re-notification to everyone who received the report (6-month / 2-year employment window); soft/hard inquiry monitoring; fixed-date (birthday) annual review of Big-3 + specialty reports; post-data-breach checklists |

## Skills index — Washington (`wa-court-docs`, 30 skills)

| Skill | Role |
|---|---|
| `wa-statewide-format` | GR 14 + statewide drafting conventions |
| `wa-kcdc` | King County District Court (East/Redmond, South/Burien, West/Seattle) |
| `wa-kcsc` | King County Superior Court (Seattle / Kent — MRJC); LCR 82 case assignment, LCR 4 case schedule, LCR 7 motions + working copies |
| `wa-pierce` | Pierce County Superior Court (Tacoma); PCLR; MAR; LINX e-filing |
| `wa-snohomish` | Snohomish County Superior Court (Everett); SCLR; MAR |
| `wa-spokane` | Spokane County Superior Court; SLR; MAR; Division III Court of Appeals seat |
| `wa-family-court` | Superior Court Family Law Department venue mechanics; AOC mandatory forms under GR 31; family-law commissioners; mandatory parenting seminars; GAL under RCW 26.12.175 |
| `wa-county-courts` | Other most-populous counties' district/superior courts (Clark, Thurston, Kitsap, Yakima, Whatcom, Benton) |
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
| `wa-consumer-debt` | Subject bundle: FDCPA, Reg F, RCW 19.16, Washington CPA, chain of title |
| `wa-family-law` | Subject bundle: RCW 26.09 dissolution + RCW 26.16 community-property regime + RCW 26.18/26.19 income-shares child support with the Washington Economic Table + RCW 26.26A Uniform Parentage Act + RCW 7.105 consolidated civil-protection orders |
| `wa-landlord-tenant` | Subject bundle: RCW 59.18 RLTA + SB 5160 just-cause framework + HB 1815 statewide tenant Right to Counsel + ERP + warranty of habitability + retaliation |
| `wa-personal-injury` | Subject bundle: RCW 4.22 pure comparative fault + 1986 several-liability Reform Act + WPLA at RCW 7.72 + medical malpractice under RCW 7.70 with 8-year statute of repose + RCW 4.92/4.96 Notice of Tort Claim |
| `wa-employment` | Subject bundle: Minimum Wage Act + WLAD at RCW 49.60 with no damages cap + 8+ employee coverage + Paid Sick Leave + PFML under RCW 50A + non-compete reform under RCW 49.62 + L&I exclusive remedy under RCW 51 |
| `wa-commercial-disputes` | Subject bundle: Washington CPA at RCW 19.86 with *Hangman Ridge* 5-element test + treble damages + WBCA at RCW 23B + LLC Act at RCW 25.15 + UCC at RCW 62A + MAR under RCW 7.06 |

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
| `or-consumer-debt` | Subject bundle: FDCPA, Reg F, **ORS 697 collection-agency registration**, **Oregon UTPA (ORS 646.605)**, chain of title, 5 fact-pattern triage, RFP/RFA banks |

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
| `ca-consumer-debt` | Subject bundle: FDCPA, Reg F, **California Rosenthal Act (Cal. Civ. Code §§ 1788 et seq.)**, **California Debt Collection Licensing Act (Fin. Code § 100000 et seq.)**, chain of title, fact-pattern triage, RFP/RFA banks |

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

## Skills index — New York (`ny-court-docs`, 35 skills)

| Skill | Role |
|---|---|
| `ny-statewide-format` | 22 NYCRR § 202.5 paper format + § 202.5-b NYSCEF format; the NY caption with "-against-" separator and Index Number; verified-vs-unverified pleadings (CPLR 3020); Tanbook (New York Law Reports Style Manual) citation |
| `ny-nyco` | New York County Supreme Court (1st JD, Manhattan); 60/80/111 Centre Street; IAS Part routing; $500k-threshold Commercial Division (22 NYCRR § 202.70) |
| `ny-kings` | Kings County Supreme Court (2nd JD, Brooklyn); 360 Adams Street; high-volume CPLR 3408 foreclosure settlement conferences; $150k Commercial Division |
| `ny-bronx` | Bronx County Supreme Court (12th JD); 851 Grand Concourse; high-volume Personal Injury Part; DCM pilot |
| `ny-nassau` | Nassau County Supreme Court (10th JD, Mineola); 100 Supreme Court Drive; $200k Commercial Division; Matrimonial Center; active MAP/ADR |
| `ny-queens` | Queens County Supreme Court (11th JD, Jamaica); 88-11 Sutphin Boulevard; $150k Commercial Division; multilingual Pro Se Office |
| `ny-county-courts` | Supreme Court Civil Term roll-up for Suffolk/Westchester/Erie/Monroe/Onondaga/Richmond/Rockland/Albany/Orange/Dutchess/Saratoga/Oneida; non-Supreme civil-court layers each have their own dedicated skill |
| `ny-nyc-civil-court` | Civil Court of the City of New York (Civil Court Act, $50k cap, 5 borough branches; the highest-volume consumer-debt forum in the country; UCMS / CCEF e-filing; 22 NYCRR Part 208 with § 208.6-a default-scrutiny) |
| `ny-nyc-housing-court` | NYC Housing Court (Housing Part of Civil Court; RPAPL Article 7 summary proceedings; Local Law 136 universal Right to Counsel; ERAP automatic stay; rent regulation overlays) |
| `ny-nassau-dc` | Nassau County District Court (UDCA + 22 NYCRR Part 212); 99 Main Street, Hempstead; six geographic districts; Civil / L&T / Small Claims / Commercial Claims Parts; $15,000 civil jurisdiction; CCFA enforcement |
| `ny-suffolk-dc` | Suffolk County District Court (UDCA + 22 NYCRR Part 212); Cohalan Court Complex, Central Islip; covers only the five western towns + Brookhaven (eastern towns route to Town Justice Courts); $15,000 civil jurisdiction; CCFA enforcement |
| `ny-city-courts` | Upstate City Courts under UCCA + 22 NYCRR Part 210; ~60 cities, $15,000 civil cap; Buffalo / Rochester / Syracuse / Albany / Yonkers / White Plains and others; opt-in Good Cause Eviction tracking; Housing Parts in larger cities |
| `ny-justice-courts` | Town & Village Justice Courts under UJCA + 22 NYCRR Part 214; ~1,250 courts statewide; $3,000 civil + small-claims cap; lay-judge dynamics; the only civil forum for eastern Suffolk County matters under $3k |
| `ny-family-court` | NY Family Court under the FCA + 22 NYCRR Part 205; CSSA child support at FCA § 413 (17/25/29/31/35% with $183k 2024 cap); Article 6 custody under *Eschbach* best-interests; Article 8 family-offense Orders of Protection; Article 10 abuse and neglect with ACS / DSS; Support Magistrate + 35-day FCA § 439(e) objection clock |
| `ny-pro-se` | Pro-se drafting framework adapted for NY; post-2023 CPLR 2106 universal-affirmation form ending the notary bottleneck; "Self-Represented" signature block; CLARO clinics + NYC right-to-counsel under Local Law 136 of 2017 |
| `ny-law-references` | CPLR (Articles 1-89), Guide to NY Evidence + CPLR Article 45 codified evidence, 22 NYCRR (Parts 202/208/210/212), Tanbook citation, fees under CPLR Arts 81-89, local rules — **canonical reference corpora live here** |
| `ny-discovery` | CPLR Article 31 disclosure with the broadest "material and necessary" scope in the U.S. (CPLR 3101(a) / *Allen v. Crowell-Collier*); CPLR 3120 Notice for D&I (RFPs); CPLR 3130/3133(b) 25-interrogatory cap; CPLR 3123 Notice to Admit; CPLR 3106-3119 EBT (depositions); 22 NYCRR § 202.20-f good-faith conferral (2021); CPLR 3124 motion to compel |
| `ny-hearings` | Microsoft Teams remote default; submitted-vs-argued motion distinction; IAS Part oral argument; courtroom etiquette |
| `ny-post-judgment` | CPLR 5015(a)(1)-(5) motion-to-vacate with the 1-year clock; CPLR Article 52 enforcement (5222 restraining notice, 5231 income execution, 5232 levy, 5225/5227 turnover, 5224 information subpoena); CPLR 5222-a Exempt Income Protection Act with $3,090 floor and EJ-FOC-1 exemption form; CPLR 5205/5206 exemptions; CPLR 5020 satisfaction; CPLR 211(b) 20-year SOL on money judgments (the longest in the U.S.) |
| `ny-first-30-days` | CPLR 3012 answer deadlines (20 in-state / 30 out-of-state, substituted, mail); substituted-service "complete 10 days after filing affidavit" rule; CPLR 3211(a)(1)-(11) pre-answer motion-to-dismiss grounds with the (e) consolidation rule; CPLR 3018 affirmative defenses; CPLR 3019 permissive counterclaims |
| `ny-fact-check` | Four-pass framework (citation verification, internal consistency, packet consistency, sworn-vs-argued consistency); Tanbook conventions; CCFA effective-date check |
| `ny-deadlines` | CPLR 2103 service add-ons (5-day mail, 1-day overnight); CPLR 2103-a (2022) email service; NY Gen. Constr. Law § 24 holidays including Lincoln's Birthday (Feb 12) and annual Election Day; § 25-a Saturday/Sunday rules; CPLR 2103(c) forward-roll; named-rule catalog |
| `ny-draft-motion` / `-declaration` / `-note` / `-order` | Scaffolders; 22 NYCRR § 202.8-b 25-page memo / 15-page reply limits; CPLR 2214 Notice of Motion with 8-day minimum service; CPLR 2214(d) Order to Show Cause; CPLR 2106 affirmation (post-2023 universal) vs. CPLR 2309 affidavit; 22 NYCRR § 202.48 settle-order with 60-day clock |
| `ny-quality-check` | Two-pass format + content QC; 22 NYCRR § 202.5(e) redaction; NYSCEF document-type selection check |
| `ny-schedule-hearing` | IAS-Part chambers-email and self-scheduling per Justice's Part Rules; OSC ex parte protocol |
| `ny-file-packet` | NYSCEF / UCMS (NYC Civil Court CCEF) / per-court e-filing assembly; 22 NYCRR § 202.5(e) redaction; document-type selection; bookmarks; service mode |
| `ny-submit-order` | 22 NYCRR § 202.48 settle-order procedure with the jurisdictional 60-day clock under *Funk v. Barry*; counter-order; chambers transmittal letter; post-signature Notice of Entry |
| `ny-consumer-debt` | Subject bundle: FDCPA, Reg F, **2022 Consumer Credit Fairness Act** (CPLR 213(a) 3-year SOL on consumer credit, CPLR 3015(e) heightened pleading, 22 NYCRR § 202.27-a heightened default-judgment evidence, CPLR 308(six) additional notice), **N.Y. GBL § 600 et seq.** collection-agency licensing (NYC + certain counties), **N.Y. GBL §§ 349 / 350** deceptive acts and false advertising, **CPLR 4544** small-print contracts, chain of title under N.Y. UCC Article 9 with CPLR 4518 business-records foundation as construed by *Bank of NY Mellon v. Gordon*, 171 AD3d 197 (2d Dept 2019); 5-pattern fact-pattern triage |
| `ny-landlord-tenant` | Subject bundle: RPAPL Article 7 summary proceedings (§ 711(2) nonpayment with 14-day demand; § 711(1) holdover with RPL § 226-c 30/60/90-day scaled notice); **2019 HSTPA** (1-month security-deposit cap at GOL § 7-108(1-a), late-fee cap at RPL § 238-a, bilateral fees at RPL § 234, 6-year overcharge lookback); **2024 Good Cause Eviction Law** at RPL Article 6-A; rent regulation regimes (Rent Stabilization for pre-1974 NYC 6+-unit; Rent Control; Loft Law); RPL § 235-b implied warranty of habitability; NYC right-to-counsel at NYC Admin Code § 26-1301 (Local Law 136 of 2017); ERAP automatic stay |
| `ny-personal-injury` | Subject bundle: CPLR Article 14-A pure comparative fault + Article 16 several-liability cap for non-economic damages; **Insurance Law § 5102(d)** no-fault "serious injury" threshold + Article 51 PIP; **Labor Law § 240(1)** absolute scaffold-law liability + § 241(6) Industrial Code (12 NYCRR Part 23); **GML § 50-e** 90-day Notice of Claim against state actors; CPLR 214-a 30-month medical-malpractice SOL with continuous-treatment toll; CPLR 214-c discovery-rule toxic-tort SOL; **EPTL § 5-4.1** wrongful death (2-year); **Child Victims Act** (CPLR 214-g) + **Adult Survivors Act** (CPLR 214-j) revival windows; Bill of Particulars practice |
| `ny-employment` | Subject bundle: **NYS HRL** (NY Exec Law § 296, all-size employer post-2019 reforms, "petty slights" harassment standard); **NYC HRL** (NYC Admin Code § 8-107, *Williams v. NYC Housing Authority* construed-broadly rule, caregiver + salary-history + stalking-victim protections; mandatory attorney's fees under § 8-502(g)); Labor Law § 191 frequency-of-pay (*Vega* late-payment liquidated damages); § 198 wage theft with 6-year SOL + 100/200% liquidated damages; **Labor Law § 740 whistleblower** (post-2022 expansion); NYS WARN Act (50+ employees, 90-day notice); 2018 Sexual Harassment Act; CROWN Act |
| `ny-commercial-disputes` | Subject bundle: **22 NYCRR § 202.70 Commercial Division** rules (Appendix A — 25-page memos, proportionality in discovery, designated counsel, accelerated adjudication; county-by-county threshold $50k-$500k); **CPLR 3016(b)** fraud particularity; CPLR 213(2) 6-year contract SOL + 213(8) 6/2-year fraud discovery rule; **BCL § 720** derivative actions + **BCL § 1104-a** judicial dissolution with § 1118 buyout election; LLC Law § 702 dissolution; **Faithless Servant Doctrine** (*Phansalkar*); **GOL §§ 5-1401 / 5-1402** NY-as-destination-forum (\$250k / \$1M thresholds); CPLR 5004 9% pre-judgment interest |

New York ships with **35 SKILL.md files** — by far the largest state plugin in the marketplace — reflecting NY's unusually fragmented civil-court system. The plugin covers:

- **Statewide procedural skills**: `ny-statewide-format`, `ny-discovery`, `ny-deadlines`, `ny-first-30-days`, `ny-hearings`, `ny-post-judgment`, `ny-fact-check`, `ny-quality-check`, `ny-schedule-hearing`, `ny-file-packet`, `ny-submit-order`, plus the four `ny-draft-*` scaffolders and the `ny-pro-se` framework + `ny-law-references` corpus host
- **Five flagship Supreme Court skills**: `ny-nyco`, `ny-kings`, `ny-bronx`, `ny-nassau`, `ny-queens`
- **One Supreme Court roll-up**: `ny-county-courts` (Suffolk / Westchester / Erie / Monroe / Onondaga / Richmond / Rockland / Albany / Orange / Dutchess / Saratoga / Oneida)
- **Two Long Island District Court skills**: `ny-nassau-dc`, `ny-suffolk-dc` (UDCA / 22 NYCRR Part 212)
- **Two dedicated NYC Civil Court skills**: `ny-nyc-civil-court` (Civil Court Act $50k cap, 5 boroughs; the highest-volume consumer-debt forum in the country) and `ny-nyc-housing-court` (RPAPL Article 7 summary proceedings; Local Law 136 Right to Counsel; ERAP)
- **Upstate City Courts roll-up**: `ny-city-courts` (~60 cities under UCCA / 22 NYCRR Part 210, $15k cap)
- **Justice Courts roll-up**: `ny-justice-courts` (~1,250 Town and Village courts under UJCA / 22 NYCRR Part 214, $3k cap)
- **Family Court skill**: `ny-family-court` (FCA Articles 3-10; CSSA; Support Magistrates; Article 8 family-offense Orders of Protection; the only NY trial-court venue with right-to-assigned-counsel as a general rule)
- **Five subject-matter bundles**: `ny-consumer-debt`, `ny-landlord-tenant`, `ny-personal-injury`, `ny-employment`, `ny-commercial-disputes`

## Skills index — Tennessee (`tn-court-docs`, 31 skills)

| Skill | Role |
|---|---|
| `tn-statewide-format` | Canonical layout home — Tenn. R. Civ. P. 10 caption + numbered paragraphs + exhibits, Rule 11 signature (BPR # / Pro Se), Rule 5 certificate of service, line-numbered pleading paper + footer (default ON), citation per Tenn. Sup. Ct. R. 4; **no statewide page/margin/font rule** — typography defers to local rules |
| `tn-davidson` | Davidson County (Nashville) — 20th JD; Metro consolidated government; Circuit / Chancery (Clerk & Master) / General Sessions / Juvenile; eFileTN/Odyssey Chancery e-filing |
| `tn-shelby` | Shelby County (Memphis) — 30th JD; Circuit / Chancery; eFlex e-filing |
| `tn-knox` | Knox County (Knoxville) — 6th JD; Circuit / Chancery (incl. child-support magistrate practice) / General Sessions / Juvenile |
| `tn-hamilton` | Hamilton County (Chattanooga) — 11th JD; Circuit / Chancery / General Sessions / Juvenile |
| `tn-general-sessions` | Limited-jurisdiction high-volume forum — $25,000 cap (§ 16-15-501), unlimited detainer jurisdiction, civil-warrant model, no formal discovery as of right, 10-day de novo appeal to Circuit (§ 27-5-108); the dominant consumer-debt + eviction forum |
| `tn-county-courts` | Roll-up for the other populous counties (Rutherford, Williamson, Montgomery, Sumner, Wilson, Sevier, Washington, Madison, Bradley, etc.); confirm JD + local rules via the AOC index |
| `tn-pro-se` | Pro-se drafting framework; BPR-number-omitted signature; Rule 4/5 service; Circuit-Chancery vs. General Sessions forum guidance |
| `tn-law-references` | Civil rules, evidence (803(6)/902), fees (incl. § 20-12-119(c)), citation, local-rules index, online sources — **canonical reference corpus host** (`court-rules/`, `tn-statutes-debt/`, federal symlinks) |
| `tn-discovery` | Tenn. R. Civ. P. 26–37; **no statewide interrogatory cap** (local rules may cap); 30/45-day responses; General Sessions has no formal discovery; meet-and-confer + motion to compel |
| `tn-hearings` | Oral argument, motion-day / docket-call dynamics (esp. General Sessions), remote-appearance practice (local-rule-dependent), etiquette |
| `tn-post-judgment` | Rule 59 (30-day, non-extendable) + Rule 60.02; execution/garnishment + Title 26 exemptions; satisfaction; 10-day General Sessions de novo appeal |
| `tn-first-30-days` | 30-day answer (Rule 12.01; 15 days after a Rule 12 denial); 12.02(6) + the conversion-to-Rule-56 trap; § 20-12-119(c) fee-shifting; affirmative defenses; Rule 13 counterclaims |
| `tn-fact-check` | Citation verification (Tenn. Code Ann., Tenn. R. Civ. P./Evid., S.W.3d; Tenn. Sup. Ct. R. 4), internal/packet/sworn-vs-argued consistency |
| `tn-deadlines` | Rule 6.01 computation + Rule 6.05 3-day mail add-on; § 15-1-101 holidays (Good Friday, Columbus Day, Juneteenth in; day-after-Thanksgiving out); named-rule catalog |
| `tn-draft-motion` / `-declaration` / `-note` / `-order` | Scaffolders; the *Rye* summary-judgment standard + Rule 56.04 timing live in `-motion`; `-declaration` defaults to a notarized affidavit; `-note` is the **Notice of Hearing** |
| `tn-quality-check` | Pre-filing two-pass format + content QC (Tenn. R. Civ. P. 10/11 caption + signature; WARN where typography is a local-rule matter) |
| `tn-schedule-hearing` | Coordinate-then-notice vs. General Sessions return-date; Notice of Hearing template; per-flagship-county routing |
| `tn-file-packet` | Assemble + file; **county-by-county e-filing** (eFileTN/Odyssey, eFlex, Tybera/TnCIS, or paper; statewide appellate AOC portal); preflight scripts |
| `tn-submit-order` | Post-hearing proposed-order transmittal; prevailing party prepares + circulates for "approved as to form" |
| `tn-family-court` | Divorce venue — both Circuit and Chancery have jurisdiction; filing mechanics, parenting-plan requirement, mediation; routes unmarried-parent matters to Juvenile Court |
| `tn-juvenile-court` | Title 37 venue — parentage / legitimation, unmarried-parent custody & support, dependency & neglect (§ 37-1-101), TPR, delinquency; magistrate-rehearing-then-appeal structure |
| `tn-consumer-debt` | Subject bundle: FDCPA, Reg F, TCPA (§ 47-18-101; *Pursell* — generally does not reach debt collection), Tennessee Collection Service Act (Title 62 ch. 20), the 2024 § 20-6-104 debt-buyer rule, chain of title, SOLs (§ 28-3-109 / § 47-2-725), sworn-account (§ 24-5-107); General Sessions forum + de novo-appeal-for-discovery strategy |
| `tn-family-law` | Subject bundle: Title 36 — equitable distribution (§ 36-4-121), grounds (§ 36-4-101) + 60/90-day ID waiting period (§ 36-4-103), income-shares child support (§ 36-5-101 / ch. 1240-02-04), four alimony types (§ 36-5-121), permanent parenting plans (§ 36-6-401) + best interest (§ 36-6-106) + 2018 relocation (§ 36-6-108), UCCJEA / UIFSA, orders of protection (§ 36-3-601); no Tennessee common-law marriage |
| `tn-landlord-tenant` | Subject bundle: URLTA (§ 66-28-101, counties over 75,000) + non-URLTA general law (§ 66-7-101), 14-day nonpayment notice (§ 66-28-505), CARES Act 30-day notice overlay for federally-subsidized properties (*Schiminger* 2024), detainer warrants (§ 29-18-101) in General Sessions with 10-day de novo appeal + possession bond (§ 29-18-130), self-help eviction prohibition (§ 66-28-504) with 3-mo/3x damages, retaliation presumption (§ 66-28-514), security-deposit forfeiture (§ 66-28-301(g)) |
| `tn-personal-injury` | Subject bundle: *McIntyre v. Balentine* modified comparative fault (49% bar) + several liability, SOL catalog (§ 28-3-104 / § 28-3-105), GTLA ($300k/$700k caps; § 29-20-101) + immunity removal + bench trial (§ 29-20-307) + shortened ~12-month SOL (§ 29-20-305), HCLA 60-day pre-suit notice (§ 29-26-121) + certificate of good faith (§ 29-26-122) + contiguous-state expert (§ 29-26-115) + 3-yr statute of repose (§ 29-26-116), 2011 tort-reform caps (§ 29-39-102 non-economic $750k/$1M catastrophic; § 29-39-104 punitive greater of $500k/2x) upheld in *McClay* (2020), TPLA 10-year statute of repose (§ 29-28-103), wrongful death (§ 20-5-106) with *Jordan* emotional damages, UM/UIM (§ 56-7-1206) |
| `tn-employment` | Subject bundle: THRA (§ 4-21-101; 8+ employee; 1-year judicial SOL § 4-21-311; mandatory atty fees; THRC 180-day window § 4-21-302) + TDA (§ 8-50-103) + TPPA whistleblower (§ 50-1-304) with the "sole reason" element confirmed in *Williams v. City of Burns* (2015) + Wage Regulation Act (§ 50-2-101; no state minimum wage — FLSA $7.25; final wages within 21 days § 50-2-103) + Tennessee right-to-work (§ 50-1-201) constitutionalized Nov. 2022 (Tenn. Const. art. XI § 21) + common-law non-compete under *Murfreesboro Medical Clinic v. Udom* (2005) + workers' comp exclusive remedy (§ 50-6-101) with post-7/1/14 forum split to the Court of Workers' Compensation Claims (§ 50-6-237) |
| `tn-commercial-disputes` | Subject bundle: Chancery as commercial-equity forum + Davidson Business Court (20th JD) + TCPA *Pursell* B2B exclusion + TUTSA trade secrets (§ 47-25-1701) with exemplary-up-to-2x + UVTA fraudulent transfer (§ 66-3-301, formerly TUFTA) + Tennessee Revised LLC Act (§ 48-249-101) + Tennessee Business Corporation Act (§ 48-11-101) with the 1998 demand-required reform + Rule 9.02 fraud-with-particularity + business torts + Tennessee Uniform Arbitration Act (§ 29-5-301) with FAA preemption + Tennessee Securities Act (§ 48-1-101) |

## Reference corpora — Washington (`wa-law-references/references/`)

Verbatim text pulled from official sources, organized by domain:

- **`court-rules/`** — 1,233 WA court rules across 35 sets (CR, CRLJ, ER, GR, RAP, etc.) extracted from courts.wa.gov PDFs.
- **`federal-debt-laws/`** *(symlink)* — points into `claude-legal-federal-laws/references/federal-debt-laws/`. **20 sources**: FDCPA, FCRA, TILA, ECOA, EFTA, CCPA-Garnishment (15 U.S.C. §§ 1671-1677), **RESPA (12 U.S.C. §§ 2601-2617), SCRA (50 U.S.C. ch 50), FHA (42 U.S.C. ch 45 subch I), FTC Telemarketing Sales Rule (16 C.F.R. Part 310)**, plus CFPB Reg B / E / F / M / N / P / V / X / Z / DD from `uscode.house.gov` USLM XML and the eCFR Versioner API.
- **`federal-bankruptcy/`** *(symlink)* — points into `claude-legal-federal-laws/references/federal-bankruptcy/`. **8 chapters** of Title 11 U.S.C.: Chapter 1 (General), 3 (Case Administration), 5 (Creditors / Debtor / Estate), 7 (Liquidation), 11 (Reorganization), 12 (Family Farmer / Fisherman), 13 (Adjustment of Debts), 15 (Cross-Border).
- **`ucc-model/`** *(symlink)* — points into `claude-legal-federal-laws/references/ucc-model/`. Model UCC Articles 1, 2, 3, 9 (Cornell LII).
- **`wa-rcw-debt/`** — **3,255 sections across 92 RCW chapters** covering full civil practice (procedure, evidence, special proceedings, family law, family-law parentage under the 2019 UPA enactment at RCW 26.26A, the 2022 consolidated civil-protection-order regime at RCW 7.105, dependency / TPR at RCW 13.34, landlord-tenant under RCW 59.18 / 59.12 / 59.20, real property, business regulation, admin law, UCC at RCW 62A, public-records, vulnerable-adults, **medical malpractice at RCW 7.70**, **product liability under WPLA at RCW 7.72**, **WLAD at RCW 49.60**, **non-compete reform at RCW 49.62**, **L&I exclusive remedy at RCW 51.04**, and the **WBCA at RCW 23B.06 / 23B.08 / 23B.13 / 23B.14**) from `app.leg.wa.gov`. Directory name retained for path stability; scope is no longer "debt-only" despite the slug. The previously curated entries for RCW 26.10 (repealed and integrated into the RCW 26.09 third-party custody framework, Laws of 2020 ch 312), RCW 26.50 (DV Prevention — superseded by the consolidated RCW 7.105 civil-protection-order regime in 2022), and RCW 49.78 (repealed when the comprehensive RCW Title 50A PFML regime took effect in 2019) are no longer pulled because the legislature redirects those URLs to disposition tables rather than chapter text — the curated CHAPTERS list reflects that, and the puller now refuses to write empty stubs (emits a WARNING with the dispositioned URL detected) so future repeals surface loudly.
- **`legal-data-apis.md`** — agent-facing index of the structured APIs above.
- **`online-sources.md`** — canonical human-facing URLs for the same sources.

## Reference corpora — Oregon (`or-law-references/references/`)

Mirrors the WA corpora structure:

- **`court-rules/`** — Oregon court rules (ORCP, UTCR, OEC, ORAP, ORPC, Multnomah SLR, Washington Co SLR) pulled by `scripts/pull_oregon_rules.py` from oregonlegislature.gov (ORCP + OEC as Microsoft Word "filtered HTML" exports), the OJD SharePoint asset library (UTCR + ORAP + the two SLRs — list-name + highest-Id selection), and osbar.org (ORPC PDF). Seven MD files / ~2.4 MB.
- **`federal-debt-laws/`** *(symlink)* — points into `claude-legal-federal-laws/references/federal-debt-laws/`.
- **`federal-bankruptcy/`** *(symlink)* — points into `claude-legal-federal-laws/references/federal-bankruptcy/`.
- **`ucc-model/`** *(symlink)* — points into `claude-legal-federal-laws/references/ucc-model/`.
- **`or-ors-debt/`** — **35 ORS chapters / ~5.6 MB** covering full civil practice. Pulled by `scripts/pull_oregon_ors.py` from `oregonlegislature.gov/bills_laws/ors/ors{NNN}.html`. The original debt-focused set (ORS 12, 14, 18, 19, 20, 21, 36, 40, 71-79, 82, 90, 105, 174, 187, 646, 697) plus chapters 32 (Injunctions, repealed-stub), 33 (Contempt), 41 (Evidence framework), 79A (UCC Article 9 — renumbered from 79 in 2025), 86 (Mortgages and trust deeds), 87 (Liens), 88 (Foreclosure), 100 (Condominiums), 107 (Dissolution / family law), 109 (Parent and child), 116 (Probate procedure), 124 (Vulnerable persons), 165 (Forgery / theft / fraud), 192 (Public records and meetings), 657 (Unemployment insurance), 659A (Employment discrimination). Directory name retained for path stability.
- **`legal-data-apis.md`** — Oregon-flavored agent-facing API index (oregonlegislature.gov, CourtListener Oregon courts, etc.).
- **`online-sources.md`** — canonical URLs for Oregon law.

OR pull scripts:

- **`scripts/pull_oregon_ors.py`** — fetches ORS chapter pages by zero-padded slug (e.g. `ors012.html`, `ors079A.html`), parses the Word-filtered HTML with a stdlib `html.parser` walker that emits one Markdown paragraph per `<p>` and promotes `<b>NN.NNN ...</b>` runs to `## NN.NNN Title` section headings. Handles alphabetic suffixes (`79A`, `659A`) and the fully-repealed Chapter 32 (bare `<b>32.010</b>` shape with the `[Repealed by ...]` body in an unbolded run). Includes jittered-exponential-backoff retries and atomic tmp-rename writes; bumps `_manifest.json` to version 0.3.0 on a successful full pull.
- **`scripts/pull_oregon_rules.py`** — pulls the seven OR court-rule canonical sources. HTML sources (ORCP, OEC) go through the same paragraph walker; PDF sources (UTCR, ORAP, ORPC, Multnomah-SLR, Washington-SLR) go through `pdftotext -layout`. UTCR/ORAP/SLR PDF URLs are discovered at run time via the courts.oregon.gov SharePoint REST API (`/_api/web/lists/getbytitle('LIST')/items?$expand=File&$orderby=Id desc`) and the highest-Id matching item wins. Bumps `_manifest.json` to version 0.2.0 on success.

Both wired into the quarterly `refresh-references` workflow under `target=or`. Each corpus dir has its own `README.md` with citation tables and a "re-pull" command.

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

- **`court-rules/`** — Colorado court rules. **72 Chief Justice Directives (CJDs)** including the foundational **CJD 11-01 Statewide Electronic Filing Standards** (effective Jan 1, 2026) are auto-pulled verbatim from `coloradojudicial.gov` by `scripts/pull_co_court_rules.py`. The rule sets themselves — **C.R.C.P., CRE, C.A.R., Colorado Rules of Professional Conduct** — are published commercially by West (Colorado Court Rules) and LexisNexis under copyright, with no free Colorado-government mirror, so the corpus carries pointer stubs for those sets and the streamlined Chapter 18 county-court / Chapter 25 small-claims rules. Total corpus: ~1.3 MB across 78 MD files.
- **`federal-debt-laws/`** *(symlink)* — points into `claude-legal-federal-laws/references/federal-debt-laws/`.
- **`federal-bankruptcy/`** *(symlink)* — points into `claude-legal-federal-laws/references/federal-bankruptcy/`.
- **`ucc-model/`** *(symlink)* — points into `claude-legal-federal-laws/references/ucc-model/`.
- **`co-statutes-debt/`** — **14 articles / ~2.0 MB** of verbatim C.R.S. content fetched by `scripts/pull_co_statutes.py` from the official Colorado General Assembly C.R.S. PDFs at `content.leg.colorado.gov`. Articles: 4-9 (UCC Article 9), 5-1 (UCCC general), 5-16 (CFDCPA), 6-1 (CCPA — 643 KB), 13-22 (Mediation / ADR), 13-50 (Judgments — joint rights), 13-52 (Judgment enforcement), 13-54 (Exemptions), 13-54.5 (Garnishment), 13-80 (Limitations), 13-90 (Witnesses), 14-10 (UDMA — 362 KB; the chapter `co-family-law` already cited), 14-13 (UCCJEA), 24-4 (State APA).

CO pull scripts:

- **`scripts/pull_co_statutes.py`** — fetches C.R.S. title PDFs from `content.leg.colorado.gov`, runs `pdftotext -layout`, slices by `ARTICLE N` headers, and emits one MD file per article with `## § NN-N-NNN. Title` section headings. Includes `http_get_bytes()` retry helper (3 retries with exponential backoff) and atomic tmp-rename writes. Wired into the quarterly `refresh-references` workflow under `target=co`.
- **`scripts/pull_co_court_rules.py`** — walks the paginated CJD index at `https://www.coloradojudicial.gov/supreme-court/chief-justice-directives`, downloads each PDF, converts via `pdftotext -layout`, dedupes page-header noise, and emits one MD file per CJD (`CJD-NN-NN.md`). For the four paywalled rule sets (C.R.C.P., CRE, C.A.R., Colo. RPC) plus the C.R.C.P. county-court / small-claims subsets, the script writes pointer-stub MDs (idempotent — existing hand-authored files are preserved unless `--overwrite-stubs` is passed). Mirrors `pull_co_statutes.py`'s atomic-write / ThreadPoolExecutor pattern. Wired into the quarterly `refresh-references` workflow under `target=co`.

## Reference corpora — New York (`ny-law-references/references/`)

Mirrors the WA/OR/CA/CO corpora structure:

- **`court-rules/`** — New York court rules. The principal sources are the **22 NYCRR Uniform Rules** (Part 202 Supreme/County, Part 208 NYC Civil Court, Part 210 City Courts, Part 212 District Courts, Part 214 Court of Claims, plus Part 130 sanctions and Part 1200 Rules of Professional Conduct), the Commercial Division Rules at § 202.70, and the New York Law Reports Style Manual (Tanbook). All 22 NYCRR rules are published by the Office of Court Administration at `www.nycourts.gov/rules/trialcourts/` — a Cloudflare-protected host. The puller writes verbatim Markdown when the upstream is reachable and **pointer stubs** (canonical URL + scope description) when the upstream returns a Cloudflare interstitial; mirrors `pull_co_court_rules.py`'s "publish what we can verify + honest stubs for the rest" discipline.
- **`federal-debt-laws/`** *(symlink)* — points into `claude-legal-federal-laws/references/federal-debt-laws/`.
- **`federal-bankruptcy/`** *(symlink)* — points into `claude-legal-federal-laws/references/federal-bankruptcy/`.
- **`ucc-model/`** *(symlink)* — points into `claude-legal-federal-laws/references/ucc-model/`.
- **`ny-statutes-debt/`** — **36 NY consolidated-laws targets / ~2.9 MB verbatim** across **CPLR** (15 articles: 1, 2, 3, 21, 22, 23, 30, 31, 32, 40 Trial, 45 Evidence, 50, 51, 52, 53), **General Obligations Law** (Article 5 contracts incl. statute of frauds + interest rates; Article 17 revival of debts), **General Business Law** (Article 22-A §§ 349-350 deceptive acts; Article 29-H §§ 600-606 NY mini-FDCPA), **RPAPL** (Articles 7 + 13 — summary proceedings + foreclosure), **Real Property Law** (Article 6-A Good Cause Eviction; Article 7 Landlord and Tenant), **N.Y. UCC** (Articles 2, 3, 9 — the NY enactment), **Domestic Relations Law** (Article 9 Annulment; Article 10 Divorce; Article 13 Matrimonial), **Family Court Act** (Article 4 Child Support; Article 5-B UIFSA — the actual home of UIFSA in NY), **Estates Powers and Trusts Law** (Article 5 Family Rights), **General Construction Law** (full law — public holidays + time computation; § 19/24/25/25-a), and **Banking Law** (Article 12-D Licensed Mortgage Bankers; Article 12-E Licensed Mortgage Loan Originators; Article 14-A Student Loan Servicers). The directory name retains the original slug for path stability; scope covers the full NY civil-practice surface.

NY pull scripts:

- **`scripts/pull_ny_court_rules.py`** — fetches **15 verbatim Parts** of 22 NYCRR (Parts 100 / 104 / 125 / 130 / 202 / 205 / 206 / 207 / 208 / 210 / 212 / 214 / 216 / 220 / 221 — Supreme + Family + Court of Claims + Surrogate's + NYC Civil + upstate City + District + Justice Courts + Commercial Division at § 202.70 inside Part 202 + Judicial Conduct + Records Retention + Engagement of Counsel + Costs and Sanctions + Sealing + Jury + Depositions) + **5 pointer stubs** for content with no free authoritative HTML source (Part 1200 Rules of Professional Conduct, Tanbook PDF, NYC Civil Court Directives, Nassau / Suffolk DC local rules). Because the upstream host (`www.nycourts.gov`) sits behind Cloudflare with bot-fight mode that fingerprints both IP reputation and TLS handshake, the puller uses **curl_cffi** with Chrome TLS impersonation and accepts an optional Cloudflare-Warp HTTP proxy via the **`NY_RULES_PROXY`** env var. The proxy is **developer-local** (LAN-only) — GitHub Actions runners can't reach it; the quarterly CI workflow runs without the proxy, so its NY-rules step typically just bumps the `Fetched:` date without changing content. The `_file_is_stub` regression check keeps committed verbatim content in place even when a stub-only re-run happens. The canonical way to refresh the corpus is for an operator to run the puller locally with their `NY_RULES_PROXY` set and commit the diff.
- **`scripts/pull_ny_statutes.py`** — fetches NY consolidated-laws articles from the **NY State Senate Open Legislation API** at `legislation.nysenate.gov/api/3/laws/<lawId>/<locationId>`. The API requires a registered key; set `NYSENATE_API_KEY` (env var) or the workflow secret of the same name to enable the verbatim path. Without the key the puller writes well-formed pointer stubs (mirrors `pull_indiana_statutes.py`'s conditional-API pattern). Both scripts emit `_manifest.json` with version + last_pulled.

Plugin-internal scripts (`format-check.py` and `case-calendar.py`) ship adapted for NY: 22 NYCRR § 202.5 + § 202.5-b format check and CPLR 2103 deadline arithmetic with NY Gen. Constr. Law § 24 holidays.

## Reference corpora — Tennessee (`tn-law-references/references/`)

Mirrors the structure of the other state plugins:

- **`court-rules/`** — **4 statewide rule sets / ~2.7 MB / 473 rule sub-pages verbatim** plus an expanded per-county canonical-URL directory for local rules. Pulled by `scripts/pull_tn_court_rules.py` from the Tennessee AOC at `tncourts.gov`. Files: `Tenn-Rules-Civil-Procedure.md` (TRCP, 288 sub-pages), `Tenn-Rules-Evidence.md` (TRE, 65 sub-pages), `Tenn-Rules-Appellate-Procedure.md` (TRAP, 55 sub-pages), `Tenn-Supreme-Court-Rules.md` (TSCR including Tenn. Sup. Ct. R. 4 on citation, 65 sub-pages), and `Tenn-Local-Rules-Practice.md` — an authored canonical-URL directory indexing local-rules entry points for Davidson (Courts of Record + General Sessions Civil + Probate + Juvenile), Shelby (Rules of the Court + Chancery + Circuit + AOC mirrors), Knox (6th JD Uniform Local Rules + Chancery + Circuit + General Sessions + Child Support Magistrate), and Hamilton (11th JD Local Rules of Civil Practice — county PDF + AOC 2-1-2024 mirror + Chancery rules-and-fees page) plus the AOC JD-map + clerks-list pointer for the other 91 counties.
- **`federal-debt-laws/`** *(symlink)* — points into `claude-legal-federal-laws/references/federal-debt-laws/`.
- **`federal-bankruptcy/`** *(symlink)* — points into `claude-legal-federal-laws/references/federal-bankruptcy/`.
- **`ucc-model/`** *(symlink)* — points into `claude-legal-federal-laws/references/ucc-model/`.
- **`tn-statutes-debt/`** — **25 chapters of the Tenn. Code Ann. verbatim (~2.6 MB / 1,496 sections)** covering the civil-practice + consumer-debt + family-law + landlord-tenant + tort + commercial surface (Titles 15, 16, 20, 24, 26, 27, 28, 29, 36, 37, 47, 62, 66). Pulled by `scripts/pull_tn_statutes.py` from the Justia mirror at `law.justia.com/codes/tennessee/`. The Tennessee Code is published officially by LexisNexis under copyright (the free hottopics mirror is a JS container, not flat HTML); Justia/FindLaw are the structured free mirrors. Both sit behind **Cloudflare bot-fight mode** that fingerprints the TLS handshake — stdlib urllib gets a 403 even from a residential IP. **As of `_manifest.json` v0.2.0** the puller uses **`curl_cffi` with Chrome TLS impersonation** and walks **Chapter → Part → Section** for chapters subdivided into Parts; run from a residential or VPN-routed IP, it produces verbatim Markdown for all 25 chapters. Falls back to **well-formed pointer stubs** carrying the canonical Justia + LexisNexis URLs when fetch fails. The `_file_is_stub` regression guard preserves any verbatim content already committed. Directory name retains the legacy `debt` slug for path stability.

TN pull scripts:

- **`scripts/pull_tn_court_rules.py`** — fetches the Tennessee AOC's Drupal HTML for each statewide rule set, walks the landing page to discover per-rule sub-page URLs by path prefix, and extracts the rule body from `<div class="field--name-field-rules-rule-content">` on each sub-page. Aggregates one MD file per rule set with the rule number/title as H2 headings. Atomic writes (`.md.tmp` + rename), jittered-exponential-backoff retries, and a `_file_is_stub` regression guard. Bumps `_manifest.json` on success.
- **`scripts/pull_tn_statutes.py`** — fetches the Justia mirror's chapter index per target, walks per-section links (or **Chapter → Part → Section** when subdivided), and extracts section bodies from the `<div id="codes-content">` container. Uses **`curl_cffi` with Chrome TLS impersonation** to defeat Cloudflare bot-fight TLS fingerprinting; falls back to stdlib urllib when curl_cffi is unavailable. On 403 or when more than half the section pages come back empty, falls back to a clean pointer stub with the canonical Justia URL + the LexisNexis URL + a one-line scope description. Honors `--stubs-only` for environments that want to force the stub shape.

Both wired into the quarterly `refresh-references` workflow under `target=tn`.

Plugin-internal scripts ship adapted for Tennessee on day one: `format-check.py` checks the marketplace common-practice defaults against the Tenn. R. Civ. P. 10.01 caption (WARN where typography is a local-rule matter, since Tennessee has no statewide format rule), and `case-calendar.py` does Tenn. R. Civ. P. 6.01/6.05 deadline arithmetic with the Tenn. Code Ann. § 15-1-101 holidays — including a Gregorian-computus **Good Friday** and **Columbus Day** — and a named-rule catalog (answer-due, general-sessions-appeal, summary-judgment-service, the SOLs, the HCLA pre-suit notice, the divorce waiting periods, etc.).

## Reference corpora — Immigration (`claude-legal-immigration-laws/references/`)

A federal, venue-independent corpus structured around the two-layer split immigration practice actually uses — **rules snapshotted verbatim, case law indexed for on-demand lookup**. Unlike the state plugins this plugin has no `<state>-law-references` skill host; the corpora live directly under `plugins/claude-legal-immigration-laws/references/`.

- **`immigration-statutes/`** — the **Immigration and Nationality Act (INA)** = **8 U.S.C. Chapter 12**, verbatim, one Markdown file per subchapter (I General Provisions, II Immigration, III Nationality and Naturalization, IV Refugee Assistance, V Alien Terrorist Removal Procedures; ~1.6 MB, with Subchapter II the bulk). Pulled by `scripts/pull_ina.py` from uscode.house.gov USLM XML. The `README.md` carries the **INA-section ↔ 8 U.S.C.-section crosswalk** practitioners cite by (INA § 212 = 8 U.S.C. § 1182, INA § 240 = 8 U.S.C. § 1229a, INA § 245 = 8 U.S.C. § 1255, etc.) because the offset is not constant across the Act.
- **`immigration-regulations/`** — curated **8 CFR** (DHS/USCIS/CBP/ICE chapter I parts + the DOJ/EOIR chapter V parts at 8 CFR 1001/1003/1208/1240 — the immigration courts and the **Board of Immigration Appeals**) and **22 CFR** State-Department visa/passport/exchange parts (40/41/42/51/53/62), verbatim, one file per Part. Pulled by `scripts/pull_immigration_cfr.py` from the eCFR versioner API. Many subjects appear twice (DHS vs. EOIR, e.g. asylum at 8 CFR 208 vs. 1208) — cite the version that governs the forum. The list is curated to the most-cited parts; extend by adding a row to `CFR_PARTS`.
- **`foreign-affairs-manual/`** — the **FAM** (9 FAM Visas incl. 9 FAM 302 ineligibilities + 9 FAM 402 NIV classifications; 8 FAM Nationality; 7 FAM Consular Affairs). Ships as **canonical-URL pointer stubs** because fam.state.gov is JavaScript-rendered + serves an incomplete TLS certificate chain (omits the issuing intermediate) that the sandbox's TLS-inspecting egress proxy can't verify (it doesn't AIA-chase) → HTTP 503. **Unlike** the NY-rules / TN-statutes Cloudflare TLS-fingerprint gates, this is an egress/cert-chain failure, not destination bot-gating, so `curl_cffi` Chrome impersonation does **not** unblock it (verified: the proxy, not the client, fails verification). `scripts/pull_fam.py` writes verbatim when the egress can complete the chain and stubs otherwise; the `_file_is_stub` guard preserves committed verbatim text. FAM is agency guidance — persuasive, not binding — so cites are always paired with the controlling INA / CFR provision.
- **`legal-data-apis.md`** — agent-facing index for the **on-demand case-law layer**: CourtListener (REST v4 + the connected CourtListener MCP) for the **federal circuits** with per-circuit `court` ids (note: immigration appeals reach an Article III court as a **petition for review of a BIA final order** under INA § 242 / 8 U.S.C. § 1252, filed directly in the circuit — no district-court merits layer; district courts appear for habeas, naturalization, and mandamus/APA delay); the EOIR Virtual Law Library for **BIA precedent** (I&N Dec.); and the USCIS site for **AAO** decisions (no JSON API — website/PDF). Also records the statute/reg refresh endpoints (note the **zero-padded** `usc08` filename quirk that the federal puller's two-digit titles never hit).
- **`online-sources.md`** — canonical human-facing URLs for all of the above plus the Visa Bulletin, USCIS/EOIR forms, and policy manuals.

Versioning: routine corpus refreshes bump nothing skill-level (there are no skills); track currency via each corpus's `_manifest.json` (`last_pulled`, `release_point` / `as_of`, `mode`). Adding/removing a corpus dir or changing which sources are covered is a `plugin.json` version bump.

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

# Refresh reference corpora — Oregon
python3 scripts/pull_oregon_rules.py \
  --out plugins/or-court-docs/skills/or-law-references/references/court-rules
python3 scripts/pull_oregon_ors.py --workers 4 \
  --out plugins/or-court-docs/skills/or-law-references/references/or-ors-debt

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

# Refresh reference corpora — New York
python3 scripts/pull_ny_court_rules.py --workers 4 \
  --out plugins/ny-court-docs/skills/ny-law-references/references/court-rules
# With NYSENATE_API_KEY set, this pulls verbatim CPLR / GOB / GBS / RPAPL / UCC / DRL / EPT / GCN / BNK content:
NYSENATE_API_KEY=<key> python3 scripts/pull_ny_statutes.py --workers 4 \
  --out plugins/ny-court-docs/skills/ny-law-references/references/ny-statutes-debt
# Without the key, the puller writes pointer stubs (use --stubs-only to force):
python3 scripts/pull_ny_statutes.py --workers 4 --stubs-only

# New York scripts
python3 plugins/ny-court-docs/scripts/format-check.py <file>   # 22 NYCRR § 202.5 + § 202.5-b compliance
python3 plugins/ny-court-docs/scripts/case-calendar.py ...     # CPLR 2103 deadline arithmetic with NY Gen. Constr. Law § 24 holidays
python3 plugins/ny-court-docs/scripts/case-calendar.py --rules # List New York named deadline rules

# Refresh reference corpora — Tennessee
python3 scripts/pull_tn_court_rules.py --workers 2 \
  --out plugins/tn-court-docs/skills/tn-law-references/references/court-rules
# Without Justia reachable, this writes well-formed pointer stubs:
python3 scripts/pull_tn_statutes.py --workers 4 \
  --out plugins/tn-court-docs/skills/tn-law-references/references/tn-statutes-debt
# Or force stubs explicitly:
python3 scripts/pull_tn_statutes.py --workers 4 --stubs-only

# Tennessee scripts
python3 plugins/tn-court-docs/scripts/format-check.py <file>   # Tenn. R. Civ. P. 10/11 + local-rule common-practice check
python3 plugins/tn-court-docs/scripts/case-calendar.py ...     # Tenn. R. Civ. P. 6.01/6.05 deadline arithmetic with Tenn. Code Ann. § 15-1-101 holidays (incl. Good Friday + Columbus Day)
python3 plugins/tn-court-docs/scripts/case-calendar.py --rules # List Tennessee named deadline rules

# Refresh reference corpora — Immigration (shared plugin; no --out needed, defaults are wired)
python3 scripts/pull_ina.py                 # INA = 8 U.S.C. Chapter 12 → immigration-statutes/
python3 scripts/pull_immigration_cfr.py     # curated 8 CFR + 22 CFR → immigration-regulations/
python3 scripts/pull_fam.py                 # FAM pointer stubs (verbatim when fam.state.gov reachable) → foreign-affairs-manual/
python3 scripts/pull_fam.py --stubs-only    # force stub shape (skip the network fetch)
# Refresh just one piece:
python3 scripts/pull_ina.py --only schII                       # just INA Subchapter II
python3 scripts/pull_immigration_cfr.py --only 8CFR-1003-eoir-bia  # just the EOIR/BIA part
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
plugins/claude-legal-federal-laws/  # SHARED federal-law plugin; depended on by every state plugin
  .claude-plugin/plugin.json        # version 0.4.0
  references/federal-debt-laws/     # FDCPA, FCRA, TILA, ECOA, Reg B/F/V/Z — canonical source
  references/ucc-model/             # Model UCC Articles 1, 2, 3, 9 — canonical source
  skills/consumer-report-ordering/SKILL.md      # FCRA consumer credit-report-rights skills layer (v0.4.0+)
  skills/consumer-credit-disputes/SKILL.md
  skills/consumer-report-accuracy/SKILL.md
  skills/consumer-harm-documentation/SKILL.md
  skills/consumer-credit-monitoring/SKILL.md
plugins/claude-legal-immigration-laws/  # SHARED immigration-law reference plugin (references-only; no skills yet)
  .claude-plugin/plugin.json        # version 0.1.0
  references/immigration-statutes/      # INA = 8 U.S.C. Chapter 12, one file per subchapter (+ INA↔8 USC crosswalk in README)
  references/immigration-regulations/   # curated 8 CFR (DHS ch I + EOIR ch V) + 22 CFR visa/passport parts
  references/foreign-affairs-manual/    # FAM pointer stubs (fam.state.gov cert-chain 503s the TLS-inspecting egress proxy); verbatim when egress completes the chain
  references/legal-data-apis.md         # on-demand case-law index: circuits (CourtListener), BIA (EOIR), AAO (USCIS)
  references/online-sources.md          # canonical human-facing URLs
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
  scripts/format-check.py           # C.R.C.P. 10 + CJD 11-01 compliance
  scripts/case-calendar.py          # C.R.C.P. 6 deadline arithmetic with C.R.S. § 24-11-101 holidays
  evals/                            # five eval categories (drafting/formatting/procedural/subject-matter/integration); empty dirs + stub README
plugins/ny-court-docs/              # 35 skills (statewide-format + 5 flagship Supreme Court venues + 2 dedicated Long Island District Courts + 2 NYC Civil/Housing Court skills + upstate City Courts + Justice Courts + Family Court + Supreme Court roll-up + 13 standard procedural + 5 subject bundles: consumer-debt + landlord-tenant + personal-injury + employment + commercial-disputes)
  .claude-plugin/plugin.json        # plugin manifest (version: 0.3.0)
  skills/<skill>/SKILL.md           # 35 SKILL.md files with substantive New York content
  skills/ny-law-references/references/{court-rules,federal-debt-laws,federal-bankruptcy,ucc-model,ny-statutes-debt}/README.md
  scripts/format-check.py           # 22 NYCRR § 202.5 + § 202.5-b compliance
  scripts/case-calendar.py          # CPLR 2103 deadline arithmetic with NY Gen. Constr. Law § 24 holidays (including Lincoln's Birthday + Election Day)
  evals/                            # five eval categories with 21 authored evals (drafting/formatting/procedural/subject-matter/integration)
plugins/tn-court-docs/              # 31 skills (statewide-format + 4 flagship county venues — Davidson/Shelby/Knox/Hamilton — + General Sessions + county-courts roll-up + split family-court/juvenile-court + 14 standard procedural + 6 subject bundles: consumer-debt + family-law + landlord-tenant + personal-injury + employment + commercial-disputes); declares dependencies: [claude-legal-federal-laws]
  .claude-plugin/plugin.json        # plugin manifest (version: 0.2.0)
  skills/<skill>/SKILL.md           # 31 SKILL.md files with substantive Tennessee content
  skills/tn-law-references/references/{court-rules,tn-statutes-debt}/  # rules verbatim (~2.7MB); statutes verbatim (~2.6MB / 1,496 sections via curl_cffi Chrome impersonation + Chapter→Part→Section walker); local-rules canonical-URL directory for Davidson/Shelby/Knox/Hamilton + General Sessions + Juvenile
  skills/tn-law-references/references/{federal-debt-laws,federal-bankruptcy,ucc-model}  # symlinks into the shared plugin
  scripts/format-check.py           # Tenn. R. Civ. P. 10/11 + local-rule common-practice check
  scripts/case-calendar.py          # Tenn. R. Civ. P. 6.01/6.05 deadline arithmetic with Tenn. Code Ann. § 15-1-101 holidays (incl. Good Friday + Columbus Day)
  evals/                            # five eval categories with 22 authored evals; TN-distinctive coverage incl. *Rye* SJ standard, Rule 12.02(6)→Rule 56 conversion + § 20-12-119(c) fee-shifting, General Sessions 10-day de novo appeal, HCLA pre-suit notice + cert of good faith, GTLA caps, 2011 tort-reform caps + *McClay*, § 20-6-104 debt-buyer default-judgment rule, Chancery vs. Circuit caption, THRA, *Pursell* B2B exclusion
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
  pull_co_court_rules.py            # coloradojudicial.gov CJD PDFs → co court-rules/ (+ paywalled-rule stubs)
  pull_oregon_rules.py              # oregonlegislature.gov + OJD SharePoint + osbar.org → or court-rules/
  pull_oregon_ors.py                # oregonlegislature.gov → or-ors-debt/
  pull_indiana_rules.py             # rules.incourts.gov + in.gov/courts/files PDFs → in court-rules/
  pull_indiana_statutes.py          # api.iga.in.gov (key-gated) → in-statutes-debt/ (stubs without key)
  pull_ny_court_rules.py            # nycourts.gov/rules/trialcourts/ (Cloudflare-gated) → ny court-rules/ (stubs on CF interstitial)
  pull_ny_statutes.py               # legislation.nysenate.gov/api/3/laws/ (key-gated) → ny-statutes-debt/ (stubs without NYSENATE_API_KEY)
  pull_ohio_court_rules.py          # supremecourt.ohio.gov PDFs → oh court-rules/
  pull_ohio_statutes.py             # codes.ohio.gov HTML → oh-statutes-debt/
  pull_tn_court_rules.py            # tncourts.gov per-rule HTML sub-pages → tn court-rules/
  pull_tn_statutes.py               # law.justia.com/codes/tennessee/ (IP-blocked from many egress) → tn-statutes-debt/ (stubs on 403)
  pull_ina.py                       # uscode.house.gov USLM XML (Title 8 ch 12, zero-padded usc08) → immigration-statutes/
  pull_immigration_cfr.py           # ecfr.gov versioner API (curated 8 CFR + 22 CFR) → immigration-regulations/
  pull_fam.py                       # fam.state.gov (incomplete cert chain → TLS-inspecting egress proxy 503; not bot-gating, curl_cffi can't fix) → foreign-affairs-manual/ (pointer stubs; verbatim when egress completes the chain)
```
