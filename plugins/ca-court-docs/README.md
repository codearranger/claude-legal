# ca-court-docs

Draft and format documents for California Superior Courts.

## What it does

- Applies **California Rules of Court 2.100-2.119** formatting to pleadings and papers (US Letter, 1″ margins on all sides, 12-point Courier/Times New Roman/Arial, 1.5 or double spacing, line numbering in the left margin, black ink only on white paper, footer with title-of-paper + page number, two-hole punch)
- Builds CRC 2.111 **pleading captions** with attorney/pro per info in the upper-left within 2.5″ and the case caption block on the right (court, county, case number, document title, hearing date / time / department)
- Scaffolds common document types: **declarations** (CCP § 2015.5 with date AND place of execution), **motions + memoranda of points and authorities** (CRC 3.1113 — max 15 pages, TOC + TOA if over 10), **Notices of Motion** (CCP § 1010, separate from the memo), and **proposed orders** (CRC 3.1312 — "[PROPOSED]" title prefix, 5-court-day service rule)
- Handles **exhibit attachment** per CRC 3.1110(f) (lettered exhibits, bookmarked PDFs for 25+ pages, authentication via declaration)
- Covers **Los Angeles Superior Court (LASC)** specifics — Stanley Mosk Courthouse + district courthouses (Spring Street, Norwalk, Pomona, Van Nuys, Pasadena, Long Beach, Compton), Court Reservation System (CRS), Local Rule 3.31 tentative-ruling regime, Odyssey eFileCA portal
- Covers **San Francisco Superior Court (SFSC)** specifics — Civic Center Courthouse at 400 McAllister, Department 302 law-and-motion calendar, SFSC Local Rules, File and ServeXpress portal
- Covers a **most-populous-counties roll-up** — Orange, San Diego, Riverside, San Bernardino, Santa Clara, Alameda, Sacramento, Contra Costa, Fresno, Kern — courthouse addresses, e-filing vendors (Tyler / One Legal / various), per-county tentative-ruling and case-management practices
- Supports **pro per ("In Pro Per")** workflows using the pro-se drafting framework adapted for California (no bar number; self-represented signature block; CCP § 2015.5 declaration form)
- Guides the **first 30 days** after service — CCP § 412.20(a)(3) 30-day answer window; meet-and-confer requirements for demurrer (CCP § 430.41) and motion to strike (CCP § 435.5); demurrer triage under CCP § 430.10; anti-SLAPP analysis under CCP § 425.16 (60-day window); cross-complaints under CCP §§ 426.10-426.50
- Provides matter-neutral **discovery procedure** under the Civil Discovery Act (CCP §§ 2016.010-2036.050) — RFPs, RFAs, depositions, the 35-special-interrogatory cap under CCP § 2030.030(a), the 45-day jurisdictional motion-to-compel-further deadline under CCP §§ 2030.300(c) / 2031.310(c) / 2033.290(c), separate-statement requirement under CRC 3.1345, mandatory sanctions under CCP § 2023.030
- Guides **hearing preparation** under California's distinctive **tentative-ruling regime** (CRC 3.1308 + per-court local rules) — judge posts tentative day before; contesting party calls by 4:30 p.m.; oral argument 5-10 minutes per side; remote appearances via LACourtConnect (LASC) / Zoom / Microsoft Teams depending on court
- Covers **post-judgment** procedure — CCP § 473 relief (mandatory attorney-affidavit-of-fault vs. discretionary, 6-month deadline), CCP § 663 motion to vacate, CCP §§ 683-708 enforcement (10-year judgment life, judgment liens, writ of execution, wage garnishment under § 706, debtor exam under § 708.110), CCP § 704 exemptions (AB 1885 homestead $300K-$600K, motor vehicle, deposit account, retirement)
- Provides canonical **online-sources** catalog (courts.ca.gov, leginfo.legislature.ca.gov, dfpi.ca.gov, lacourt.org, sfsuperiorcourt.org) and a **fact-check** skill that runs citation, internal-consistency, packet, and sworn-vs.-argued passes before filing, using **California Style Manual** citation conventions (year-before-volume `(2001) 25 Cal.4th 826`, comma-plus-§ `Code Civ. Proc., § 437c`, CRC 8.1115 unpublished-opinion rule)
- Ships a **subject-matter bundle for consumer-debt defense** — FDCPA (15 U.S.C. § 1692 et seq.), Regulation F (12 C.F.R. Part 1006), the **Rosenthal Fair Debt Collection Practices Act** (Cal. Civ. Code §§ 1788-1788.33 — reaches first-party AND third-party collectors; § 1788.17 FDCPA incorporation; $100-$1,000 statutory damages; one-way attorney's fees), the **Fair Debt Buying Practices Act** (Cal. Civ. Code §§ 1788.50-1788.66 — heightened pleading + documentation for debt buyers under § 1788.58), the **California Debt Collection Licensing Act** (Cal. Fin. Code §§ 100000-100027 — DFPI licensure since Jan 2022, affirmative defense for non-licensure), the **Unfair Competition Law** (Cal. Bus. & Prof. Code §§ 17200-17210 — 4-year SOL, "unlawful" prong borrows Rosenthal / FDCPA / CDCLA violations), the **CLRA** (Cal. Civ. Code §§ 1750-1784), chain-of-title doctrine under Cal. Comm. Code Art. 9, debt-specific key cases (*Komarova*, *Davidson v. Seterus*, *Best Service Co. v. Pickett*, *Riverisland Cold Storage*, *Trope v. Katz*, *Aguilar v. Atlantic Richfield*), RFP / interrogatory / RFA banks targeting debt-buyer deficiencies, meet-and-confer templates, and six synthetic example filings (answer, declaration, motion to compel, M&C, proposed order, certificate of service)

## Architecture

The plugin is organized into two layers:

1. **Matter-neutral procedural skills** — these apply to any California civil case regardless of subject matter (CCP civil rules, CEC evidence rules, fees-and-costs, local rules, citation format per the California Style Manual, online sources, discovery procedure, first-30-days response, hearings, filing packets, post-judgment, fact-check, deadlines, pro per, statewide format, LASC, SFSC, county-courts roll-up).
2. **Subject-matter bundles** — self-contained skills supplying the substantive law, fact patterns, request banks, case catalog, and example filings for one subject matter. The procedural skills delegate subject-matter-specific questions to these bundles.

Currently shipping one subject-matter bundle: `ca-consumer-debt`. The architecture leaves clean slots for future bundles (landlord-tenant under the Cal. Civ. Code § 1940 framework, family law under the Family Code, personal injury, employment under the Lab. Code, etc.).

## Components

All functionality is exposed as **skills**. There are no slash commands — the agent matches each skill's description against what the user says and invokes it automatically.

### Matter-neutral reference skills

| Skill | Purpose |
|-------|---------|
| `ca-statewide-format` | CRC 2.100-2.119 formatting rules, caption structure (CRC 2.111), signature blocks, exhibit handling (CRC 3.1110(f)), the four document templates |
| `ca-lasc` | Los Angeles Superior Court specifics — Stanley Mosk Courthouse + district courthouses, CRS reservation system, Local Rule 3.31 tentatives, e-filing via Odyssey eFileCA |
| `ca-sfsc` | San Francisco Superior Court specifics — Civic Center Courthouse, Department 302 law-and-motion, e-filing via File and ServeXpress |
| `ca-county-courts` | Most-populous counties' Superior Courts (Orange, San Diego, Riverside, San Bernardino, Santa Clara, Alameda, Sacramento, Contra Costa, Fresno, Kern), with addresses, e-filing systems, local-rule pointers |
| `ca-pro-se` | pro-se drafting framework adapted for California — fact-front-loaded, written to the judge; "In Pro Per" signature; service protocols under CCP §§ 412.10-417.40, § 1010.6 |
| `ca-law-references` | Civil rules (CCP), Evidence Code (CEC), fees and costs (CCP §§ 1032-1033.5, § 1717, § 1021.5, § 998), local rules (LASC, SFSC, OCSC, other counties), citation format per the California Style Manual, canonical online sources, general-civil key cases (*Aguilar*, *Howell*, *Reid v. Google*, *Riverisland*) |
| `ca-discovery` | Matter-neutral discovery framework under the Civil Discovery Act — RFPs, interrogatories (35-special cap), RFAs, depositions, meet-and-confer, motion to compel further (45-day jurisdictional deadline), separate statement (CRC 3.1345), sanctions (CCP § 2023.030) |
| `ca-hearings` | Tentative-ruling regime (CRC 3.1308), oral argument structure, remote appearances (LACourtConnect, Zoom, Teams), courtroom etiquette, hearing-day checklist |
| `ca-post-judgment` | CCP § 473 motion to vacate (mandatory + discretionary), CCP § 706 garnishment response (25%/30x federal-minimum-wage CCPA limit), CCP § 704 exemptions, CCP § 708.110 debtor exam, CCP § 724 satisfaction of judgment |

### Matter-neutral workflow skills

| Skill | Triggers on | Does |
|-------|-------------|------|
| `ca-first-30-days` | "I was just served", "answer deadline", "demurrer triage" | From-service-through-response workflow — CCP § 412.20(a)(3) 30-day deadline math, demurrer vs. answer vs. anti-SLAPP triage, meet-and-confer requirements (CCP § 430.41 / § 435.5), affirmative defenses checklist, compulsory cross-complaint analysis |
| `ca-draft-motion` | "draft a motion", "motion to compel / strike / demurrer / SJ" | Scaffolds a motion + Notice of Motion + Memorandum of P&A (pro-se drafting framework adapted for CA), Separate Statement for compel-further / SJ motions, Declaration under CCP § 2015.5 |
| `ca-draft-declaration` | "draft a declaration", "declaration in support" | Scaffolds a declaration with numbered paragraphs, CCP § 2015.5 penalty-of-perjury attestation (with date AND place of execution), exhibit references |
| `ca-draft-note` | "Notice of Motion", "draft my motion notice" | Scaffolds the Notice of Motion under CCP § 1010 (separate document from the memo, with date / time / department / nature / grounds / supporting papers) |
| `ca-draft-order` | "proposed order", "order granting" | Scaffolds a `[PROPOSED]` order with recitals, specific operative language, CRC 3.1312 5-court-day service compliance |
| `ca-quality-check` | "QC this", "is this CRC 2.100 compliant", "review before I file" | Two-pass format + content check; motion-type-specific checklists; separate-statement enforcement (CRC 3.1345) |
| `ca-fact-check` | "fact check this", "verify citations", "cite-check" | Four-pass verification — citation verification (California Style Manual), CRC 8.1115 unpublished-opinion check, internal consistency, packet consistency. Never silently rewrites |
| `ca-deadlines` | "when is my answer due", "compute the deadline" | Computes court- and calendar-day deadlines with Govt. Code § 6700 holidays (including day-after-Thanksgiving, Cesar Chavez Day, Lincoln's Birthday); response, discovery (the 45-day rule), motion-notice (16/9/5 court days under § 1005(b)), SJ (75 days under § 437c), appeal (60 days under CRC 8.104), and post-judgment windows |
| `ca-schedule-hearing` | "reserve a hearing date" | Drafts the LASC Court Reservation System workflow, SFSC online reservation, or per-county equivalent — computes earliest viable hearing date from the CCP § 1005(b) 16-court-day notice + service-method extensions |
| `ca-file-packet` | "assemble the packet", "I'm ready to file" | Verifies components (Notice of Motion + Memo + Separate Statement + Declaration + Proposed Order + POS), caption consistency, service deadlines; e-filing instructions for the specific court (Odyssey eFileCA / File and ServeXpress / One Legal); CRC 3.1113 page-limit enforcement |
| `ca-submit-order` | "submit the order", "the judge granted — prepare the order" | Strips `[PROPOSED]`, applies bench modifications, prepares the transmittal per CRC 3.1312, computes the 5-court-day service and objection windows, tracks Notice of Entry of Order under CRC 8.104 |

### Subject-matter bundles

| Bundle | Covers |
|--------|--------|
| `ca-consumer-debt` | Debt-buyer and original-creditor collection cases — FDCPA (15 U.S.C. § 1692 et seq.), Regulation F (12 C.F.R. Part 1006), the Rosenthal Act (Cal. Civ. Code §§ 1788-1788.33 with *Komarova* / *Davidson v. Seterus* first-party reach), the FDBPA (Cal. Civ. Code §§ 1788.50-1788.66 with § 1788.58 heightened pleading), the CDCLA (Cal. Fin. Code §§ 100000-100027 DFPI licensure), the UCL (Cal. Bus. & Prof. Code §§ 17200-17210 with 4-year SOL and three-prong test), the CLRA (Cal. Civ. Code §§ 1750-1784), California statutes of limitations as applied to consumer debt (CCP § 337 written contract / 4 years; CCP § 360 revival; CCP § 361 borrowing; Cal. Comm. Code § 2725 / § 3118), UCC Article 9 chain-of-title doctrine (Cal. Comm. Code §§ 9101-9809 with § 9404 assignee defenses and § 9406 notification), five recurring debt-buyer fact patterns, debt-specific key cases (*Komarova v. National Credit Acceptance*, *Davidson v. Seterus*, *Best Service Co. v. Pickett*, *Riverisland Cold Storage*, *Trope v. Katz*, *Aguilar v. Atlantic Richfield*), RFPs / interrogatories (35-special bank) / RFAs / meet-and-confer templates targeting debt-buyer deficiencies, and synthetic example filings (answer, motion to compel, declaration, proposed order, meet-and-confer letter, certificate of service) |

## Composition examples

- A typical debt-buyer defense flow: `ca-first-30-days` composes with `ca-consumer-debt` for subject-matter triage, then with `ca-draft-motion` / `ca-draft-declaration` / `ca-draft-note` / `ca-draft-order` for the filings, `ca-law-references` for civil and evidence rules and fee authorities, `ca-pro-se` for voice and the pro-se drafting framework, `ca-statewide-format` for CRC 2.100-2.119 compliance, `ca-lasc` or `ca-sfsc` for venue specifics, `ca-fact-check` before filing, and `ca-file-packet` for assembly.
- A general civil answer flow without subject-matter specifics: `ca-first-30-days` runs with just the procedural layer — `ca-law-references`, `ca-draft-*`, `ca-fact-check`, `ca-file-packet`.

## Installing

From a marketplace that includes this plugin:

```
/plugin install ca-court-docs
```

## Required tools

The plugin assumes access to standard Claude file tools: Read, Write, Edit, Bash. For `.docx` generation it expects `node` + the `docx` npm package, and for format validation a Python 3 interpreter. The `format-check.py` script validates CRC 2.100-2.119 compliance on `.docx` files; the `case-calendar.py` script computes deadlines under CCP §§ 12, 12a, 12c with the Govt. Code § 6700 holiday calendar.

## California-specific procedural quirks the plugin surfaces

- **Tentative-ruling regime** (CRC 3.1308) — judge posts tentative day before; contesting party must call by 4:30 p.m. day before, or tentative becomes the order without oral argument. This is virtually universal in California civil law-and-motion practice.
- **35-special-interrogatory cap** (CCP § 2030.030(a)) — only 35 specially prepared interrogatories without a CCP § 2030.040 declaration of necessity; form interrogatories (DISC-001, DISC-002) have no cap.
- **45-day jurisdictional deadline** on motion to compel further responses (CCP §§ 2030.300(c), 2031.310(c), 2033.290(c)) — missing this deadline forfeits the right entirely. May be extended only by written agreement.
- **Court-day notice periods** for motion practice (CCP § 1005(b)) — 16 court days notice, 9 court days opposition, 5 court days reply. Not calendar days. Different from federal Fed. R. Civ. P. 6 conventions.
- **75-day SJ notice** (CCP § 437c(a)(2)) — significantly longer than FRCP 56's effective ~14-21 days. Separate statement is mandatory.
- **Mandatory meet-and-confer** for demurrer (CCP § 430.41) and motion to strike (CCP § 435.5) — at least 5 days before the responsive-pleading deadline.
- **Rosenthal Act first-party reach** (Cal. Civ. Code § 1788.2(c) plus *Komarova* / *Davidson v. Seterus*) — unlike federal FDCPA, Rosenthal covers original creditors collecting their own debts.
- **CDCLA licensure** (Cal. Fin. Code § 100002, effective Jan 1, 2022) — debt collectors AND debt buyers must hold a DFPI license; non-licensure is an affirmative defense and a UCL "unlawful" predicate.
- **FDBPA heightened pleading** (Cal. Civ. Code § 1788.58) — debt-buyer complaints must allege charge-off balance, date of last payment, original creditor, account number, chain of title, and ALL post-charge-off purchasers; missing allegations are grounds for demurrer.
- **CCP § 2015.5 declaration** requires both date AND **place of execution** — many out-of-state and federal practitioners omit the place requirement.
- **California Style Manual** citation format — year before volume `(2001) 25 Cal.4th 826`, comma + § for statutes `Code Civ. Proc., § 437c`. NOT Bluebook.
- **CRC 8.1115** — unpublished California Court of Appeal opinions are GENERALLY NOT CITABLE in California courts (narrow exceptions for collateral estoppel / res judicata / law of the case).
- **AB 1885 homestead** (Cal. Civ. Code § 704.730, amended 2021) — homestead exemption is now $300,000–$600,000 (depending on county median home price), a substantial increase from the pre-2021 $75K-$175K range.

## Not legal advice

This plugin is a drafting aid. Review all output carefully against current court rules and local practice before filing. The author is not an attorney and nothing in this plugin constitutes legal advice.

## License

MIT.
