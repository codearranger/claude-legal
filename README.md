# claude-legal

A Claude Code / Cowork marketplace of plugins for preparing U.S. court documents, organized one plugin per state.

## What's in here

Five plugins today — four state plugins plus one shared data-only plugin they all depend on:

- **`claude-legal-federal-laws`** — Shared, data-only plugin. Holds the canonical copy of federal U.S. debt-collection and consumer-finance law (FDCPA, FCRA, TILA, ECOA, Reg B/F/V/Z) and the model Uniform Commercial Code (Articles 1, 2, 3, 9). Every state plugin below declares it as a `dependencies:` entry in `plugin.json` and reaches it via in-tree symlinks; the Claude Code marketplace runtime auto-installs the dependency and dereferences the symlinks at install time, so each installed state plugin still has federal content locally available.
- **`wa-court-docs`** — Washington State. Drafts and formats pleadings, declarations, motions, notes for motion docket, and proposed orders for Washington courts. Applies GR 14 formatting; covers King County District Court (all three divisions — East/Redmond, South/Burien, West/Seattle), King County Superior Court (Seattle / Kent — MRJC), and the most-populous counties' roll-up (Pierce, Snohomish, Spokane, Clark, Thurston, Kitsap, Yakima, Whatcom, Benton). Supports pro se workflows. The `wa-consumer-debt` subject-matter bundle covers FDCPA / Reg F / WA CPA debt-defense.
- **`or-court-docs`** — Oregon. Drafts and formats pleadings, declarations, motions, notices of hearing, and proposed orders for Oregon circuit courts. Applies UTCR 2.010 formatting; covers Multnomah County Circuit Court (Portland / Central Courthouse), Washington County Circuit Court (Hillsboro), and the most-populous counties' roll-up (Clackamas, Lane, Marion, Jackson, Deschutes, Linn, Benton, Yamhill, Polk, Douglas). Supports pro se workflows. The `or-consumer-debt` subject-matter bundle covers FDCPA / Reg F / Oregon UTPA (ORS 646.605) / ORS 697 Collection Agency Registration / chain-of-title doctrine.
- **`ca-court-docs`** — California. Drafts and formats pleadings, declarations, motions, notices of motion, and proposed orders for California superior courts. Applies California Rules of Court 2.100-2.119 formatting; covers Los Angeles Superior Court (LASC — Stanley Mosk Courthouse + the LASC district courthouses), San Francisco Superior Court (SFSC — Civic Center Courthouse, Dept. 302 law-and-motion), and the most-populous-counties roll-up (Orange, San Diego, Riverside, San Bernardino, Santa Clara, Alameda, Sacramento, Contra Costa, Fresno, Kern). Supports pro se ("In Pro Per") workflows. The `ca-consumer-debt` subject-matter bundle covers FDCPA / Reg F / Rosenthal Fair Debt Collection Practices Act (Cal. Civ. Code §§ 1788 et seq.) / Fair Debt Buying Practices Act (Cal. Civ. Code §§ 1788.50 et seq.) / California Debt Collection Licensing Act (Cal. Fin. Code §§ 100000 et seq., 2022) / chain-of-title doctrine under Cal. Comm. Code Art. 9.
- **`co-court-docs`** — Colorado. Drafts and formats pleadings, declarations, motions, notices, and proposed orders for Colorado courts. Applies C.R.C.P. 10 + Chief Justice Directive 11-01 formatting (uniform 1-inch margins, 12-point font, double-spaced, the two-block Colorado caption with the case-number / division / courtroom box); covers Denver District Court (2nd Judicial District — Lindsey-Flanigan Courthouse), Arapahoe County District Court (18th Judicial District — Centennial / Aurora / Littleton), and the most-populous-counties roll-up (Jefferson, El Paso, Adams, Boulder, Larimer, Douglas, Weld, Pueblo, Mesa, Broomfield). Supports pro se / "Self-Represented" workflows including the CCEFS Pro Se portal and the Colorado Judicial Branch JDF (Judicial Department Forms) catalog. **Two subject-matter bundles** ship in the initial release: (1) `co-consumer-debt` covers FDCPA / Reg F / Colorado Fair Debt Collection Practices Act (C.R.S. art. 16 of title 5, recodified from Title 12 in 2022) / Colorado Consumer Protection Act (C.R.S. art. 1 of title 6 with treble damages and mandatory fees) / Colorado UCCC / collection-agency licensure under the AG's Collection Agency Board / chain-of-title doctrine under Colorado UCC Article 9; (2) `co-family-law` covers the Uniform Dissolution of Marriage Act (C.R.S. art. 10 of title 14), the 91-day residency and 91-day waiting-period requirements, dissolution / legal separation / declaration of invalidity (annulment) under C.R.S. § 14-10-111, allocation of parental responsibilities (C.R.S. § 14-10-124 — Colorado replaced "custody" terminology in 1998), the income-shares child-support guideline (C.R.S. § 14-10-115 with the 93-overnight rule), maintenance (C.R.S. § 14-10-114), common-law marriage under *People v. Lucero* as modernized by *In re Marriage of Hogsett & Neale*, and the C.R.C.P. 16.2 mandatory financial-disclosure regime with the Sworn Financial Statement (JDF 1111). Colorado is the first state plugin to ship with two subject-matter bundles at the initial release for a total of **22 SKILL.md files** (vs. 21 in WA / OR / CA).

All four state plugins are architected the same way: matter-neutral civil-procedure skills (statewide format, civil rules, evidence rules, fees and costs, local rules, citation format, online sources, discovery, first-30-days response, hearings, filing packets, post-judgment, fact-checking, deadlines) plus subject-matter bundles that plug into the procedural skills. They share federal/UCC reference content via the `claude-legal-federal-laws` dependency rather than copying it into each plugin.

The marketplace is organized one plugin per state; more state plugins can be added under `plugins/` as it grows.

## Install

Add this marketplace to Claude Code or Cowork, then install the plugins:

```
/plugin marketplace add https://github.com/codearranger/claude-legal
/plugin install wa-court-docs@claude-legal
/plugin install or-court-docs@claude-legal
/plugin install ca-court-docs@claude-legal
/plugin install co-court-docs@claude-legal
```

Each state plugin declares `claude-legal-federal-laws` as a `dependencies:` entry, so the marketplace runtime installs the shared plugin automatically — no need to install it explicitly.

## Repo layout

```
claude-legal/
├── .claude-plugin/
│   └── marketplace.json              # Marketplace manifest
├── plugins/
│   ├── claude-legal-federal-laws/    # SHARED data-only plugin (depended on by every state plugin)
│   │   ├── .claude-plugin/plugin.json
│   │   ├── README.md
│   │   └── references/
│   │       ├── federal-debt-laws/    # FDCPA, FCRA, TILA, ECOA, Reg B/F/V/Z (canonical)
│   │       └── ucc-model/            # Model UCC Articles 1, 2, 3, 9 (canonical)
│   ├── wa-court-docs/                # Washington State plugin (21 skills)
│   │   ├── .claude-plugin/plugin.json
│   │   ├── skills/                   # GR 14, KCDC, KCSC, county roll-up, etc.
│   │   ├── scripts/                  # format-check.py (GR 14), case-calendar.py (CR 6)
│   │   └── evals/
│   └── or-court-docs/                # Oregon plugin (21 skills)
│       ├── .claude-plugin/plugin.json
│       ├── skills/                   # UTCR 2.010, or-multcc, or-wccc, or-county-courts, or-consumer-debt, etc.
│       │   ├── or-statewide-format/  # UTCR 2.010 + statewide drafting
│       │   ├── or-multcc/            # Multnomah Circuit Court (Portland)
│       │   ├── or-wccc/              # Washington Co Circuit Court (Hillsboro)
│       │   ├── or-county-courts/     # Clackamas, Lane, Marion, Jackson, Deschutes, etc.
│       │   ├── or-pro-se/            # pro-se drafting framework adapted for Oregon
│       │   ├── or-law-references/    # ORCP, OEC, ORS, citation format, local SLRs
│       │   ├── or-discovery/         # RFPs, RFAs, depositions, ORCP 46 (no interrogatories!)
│       │   ├── or-hearings/          # Oral argument, WebEx, etiquette
│       │   ├── or-post-judgment/     # ORCP 71, ORS 18.600+ garnishment, exemptions
│       │   ├── or-first-30-days/     # Answer, ORCP 21 motions, counterclaims
│       │   ├── or-fact-check/        # Citation verification (Oregon Style Manual)
│       │   ├── or-deadlines/         # ORCP 10 + ORS 187.010 holidays
│       │   ├── or-draft-motion/      # Scaffold motion + memorandum
│       │   ├── or-draft-declaration/ # Scaffold declaration with exhibits
│       │   ├── or-draft-note/        # Scaffold Notice of Hearing
│       │   ├── or-draft-order/       # Scaffold proposed order
│       │   ├── or-quality-check/     # UTCR 2.010 format + content QC
│       │   ├── or-schedule-hearing/  # JA / Civil Division date-request email
│       │   ├── or-file-packet/       # Assemble packet for File and Serve
│       │   ├── or-submit-order/      # Post-hearing signed-order transmittal
│       │   └── or-consumer-debt/     # FDCPA, Reg F, ORS 697, UTPA, chain of title
│       ├── scripts/
│       │   ├── format-check.py       # UTCR 2.010 compliance checker
│       │   └── case-calendar.py      # ORCP 10 deadline arithmetic + ORS 187 holidays
│       └── evals/                    # Drafting, formatting, procedural, subject-matter, integration evals
│   └── ca-court-docs/                # California plugin (21 skills)
│       ├── .claude-plugin/plugin.json
│       ├── skills/                   # ca-statewide-format (CRC 2.100-2.119), ca-lasc, ca-sfsc, ca-county-courts, ca-consumer-debt (Rosenthal/FDBPA/CDCLA), etc.
│       │   ├── ca-statewide-format/  # CRC 2.100-2.119 + statewide drafting
│       │   ├── ca-lasc/              # Los Angeles Superior Court
│       │   ├── ca-sfsc/              # San Francisco Superior Court (Dept. 302)
│       │   ├── ca-county-courts/     # Orange, San Diego, Riverside, Santa Clara, etc.
│       │   ├── ca-pro-se/            # pro-se drafting framework adapted for California ("In Pro Per")
│       │   ├── ca-law-references/    # CCP, CEC, CRC, citation format (California Style Manual), local rules
│       │   ├── ca-discovery/         # CCP §§ 2016+ (Civil Discovery Act); 35-rog cap; 45-day jurisdictional motion-to-compel-further
│       │   ├── ca-hearings/          # Tentative-ruling regime (CRC 3.1308); LACourtConnect
│       │   ├── ca-post-judgment/     # CCP § 473 relief, CCP § 706 garnishment, CCP § 704 exemptions
│       │   ├── ca-first-30-days/     # Demurrer (CCP § 430.10), motion to strike, anti-SLAPP (CCP § 425.16)
│       │   ├── ca-fact-check/        # Citation verification (California Style Manual); CRC 8.1115 unpublished-opinion rule
│       │   ├── ca-deadlines/         # CCP § 12, § 12a, § 12c + Govt. Code § 6700 holidays
│       │   ├── ca-draft-motion/      # Notice of Motion + Memorandum of P&A; separate-statement requirements
│       │   ├── ca-draft-declaration/ # CCP § 2015.5 declarations (with place of execution)
│       │   ├── ca-draft-note/        # Notice of Motion under CCP § 1010
│       │   ├── ca-draft-order/       # [PROPOSED] order conventions
│       │   ├── ca-quality-check/     # CRC 2.100-2.119 format + content QC
│       │   ├── ca-schedule-hearing/  # LASC Court Reservation System / SFSC Dept. 302 reservation
│       │   ├── ca-file-packet/       # Odyssey eFileCA / File and ServeXpress; CCP § 1005(b) timing
│       │   ├── ca-submit-order/      # CRC 3.1312 5-court-day proposed-order rule
│       │   └── ca-consumer-debt/     # FDCPA, Reg F, Rosenthal Act, FDBPA, CDCLA, UCL, chain of title
│       ├── scripts/
│       │   ├── format-check.py       # CRC 2.100-2.119 compliance checker
│       │   └── case-calendar.py      # CCP § 12 deadline arithmetic + Govt. Code § 6700 holidays
│       └── evals/                    # Drafting, formatting, procedural, subject-matter, integration evals
│   └── co-court-docs/                # Colorado plugin (22 skills — 21 standard + co-family-law)
│       ├── .claude-plugin/plugin.json
│       ├── skills/                   # C.R.C.P. 10 + CJD 11-01 statewide format; Denver + Arapahoe + county roll-up
│       │   ├── co-statewide-format/  # C.R.C.P. 10 + CJD 11-01; two-block Colorado caption
│       │   ├── co-denver/            # Denver District Court (2nd JD — Lindsey-Flanigan)
│       │   ├── co-arapahoe/          # Arapahoe County District Court (18th JD — Centennial)
│       │   ├── co-county-courts/     # Jefferson, El Paso, Adams, Boulder, Larimer, Douglas, etc.
│       │   ├── co-pro-se/            # pro-se drafting framework; "Self-Represented"; CCEFS Pro Se; JDF forms
│       │   ├── co-law-references/    # C.R.C.P., CRE, citation format, fees, local rules, CJDs
│       │   ├── co-discovery/         # C.R.C.P. 26-37 (interrogatories under Rule 33 ARE available, 25-cap); county-court Rule 311
│       │   ├── co-hearings/          # Webex statewide; tentative-ruling regime; chambers practice standards
│       │   ├── co-post-judgment/     # C.R.C.P. 59/60(b); C.R.S. § 13-54.5 garnishment; SB22-086 exemptions ($250k homestead)
│       │   ├── co-first-30-days/     # 21-day answer (C.R.C.P. 12(a)(1)); Warne v. Hall plausibility standard
│       │   ├── co-fact-check/        # Citation verification; Colorado neutral-citation (post-2012 cases)
│       │   ├── co-deadlines/         # C.R.C.P. 6 + C.R.S. § 24-11-101 holidays (incl. Frances Xavier Cabrini Day, Juneteenth)
│       │   ├── co-draft-motion/      # C.R.C.P. 121 § 1-15 motion + memorandum; 15/10-page limits
│       │   ├── co-draft-declaration/ # C.R.S. § 13-27-104 declaration (no notary required)
│       │   ├── co-draft-note/        # Notice of Hearing / Substitution / Address Change / Dismissal
│       │   ├── co-draft-order/       # Proposed order with separate findings + ordering clause; Word-copy chambers protocol
│       │   ├── co-quality-check/     # CJD 11-01 format + pro-se drafting framework content QC
│       │   ├── co-schedule-hearing/  # Chambers / JA email templates per JD
│       │   ├── co-file-packet/       # CCEFS workflow; document codes; fee schedule; JDF 205/206 waiver
│       │   ├── co-submit-order/      # Post-hearing transmittal; Word-format chambers copy; agreed-form orders
│       │   ├── co-consumer-debt/     # FDCPA, Reg F, CFDCPA, CCPA, UCCC, collection-agency licensure, chain of title, 6-year SOL
│       │   └── co-family-law/        # UDMA (C.R.S. art. 10 of title 14); dissolution / annulment / legal separation; C.R.C.P. 16.2; § 14-10-115 child support; § 14-10-124 parental responsibilities; § 14-10-114 maintenance
│       ├── scripts/
│       │   ├── format-check.py       # C.R.C.P. 10 + CJD 11-01 compliance checker
│       │   └── case-calendar.py      # C.R.C.P. 6 deadline arithmetic + C.R.S. § 24-11-101 holidays
│       └── evals/                    # Drafting, formatting, procedural, subject-matter, integration evals
├── scripts/                          # Shared marketplace scripts
│   ├── lint-skills.py                # Frontmatter + name/dir-match linter
│   ├── hooks/pre-commit              # Symlink target for git hook
│   ├── pull_court_rules.py           # courts.wa.gov → wa court rules
│   ├── pull_wa_rcw.py                # app.leg.wa.gov → wa RCW chapters
│   ├── pull_ca_court_rules.py        # courts.ca.gov → ca court rules
│   ├── pull_ca_statutes.py           # leginfo.legislature.ca.gov → ca statute chapters
│   ├── pull_federal_debt_laws.py     # Federal law (shared content; FDCPA, FCRA, TILA, ECOA, Reg F/V/Z/B)
│   └── pull_ucc.py                   # Model UCC (shared content; Articles 1, 2, 3, 9)
├── LICENSE
└── README.md
```

## Key differences across states

The plugins are intentionally parallel, but they encode the genuine procedural differences between the jurisdictions. A few worth highlighting:

| Concept | Washington | Oregon | California | Colorado |
|---------|------------|--------|------------|----------|
| Format rule | GR 14 | UTCR 2.010 | CRC 2.100-2.119 | C.R.C.P. 10 + CJD 11-01 |
| Page 1 top margin | 3 inches | 2 inches | 1 inch | 1 inch (uniform) |
| Civil rules | CR (superior) + CRLJ (district) | ORCP (unified — no district court) | CCP (Code of Civil Procedure) | C.R.C.P. (district) + Chapter 18 county-court rules |
| Evidence rules | ER (court rule) | OEC (statutory at ORS Ch. 40) | CEC (statutory at Cal. Evid. Code) | CRE (court rule) |
| Answer due | 20 days | 30 days | 30 days | **21 days** (in-state); 35 (out-of-state) |
| Failure to state | CR 12(b)(6) / CRLJ 12(b)(6) | ORCP 21 A(8) | CCP § 430.10(e) (general demurrer) | C.R.C.P. 12(b)(5) (Twombly/Iqbal post-*Warne v. Hall*) |
| Discovery — interrogatories | CR 33 (available) | **Not available** without court order | CCP § 2030.030 (form + special; **35-question cap on specials w/o declaration**) | C.R.C.P. 33 (available; 25-cap) |
| Discovery — RFPs | CR 34 | ORCP 43 | CCP § 2031.010 | C.R.C.P. 34 |
| Discovery — RFAs | CR 36 | ORCP 45 | CCP § 2033.010 | C.R.C.P. 36 |
| Motion to compel | CR 37 / CRLJ 37 | ORCP 46 A | CCP § 2031.310 / § 2030.300 / § 2033.290 | C.R.C.P. 37(a) |
| Motion practice timing | CR 6(d) | UTCR 5.030 + SLRs | CCP § 1005 (16 court days notice) | C.R.C.P. 121 § 1-15: 21-day response / 7-day reply / 15-page limit |
| Mandatory conferral | varies | varies | meet-and-confer per discovery rules | C.R.C.P. 121 § 1-15(8) for all non-dispositive motions |
| Summary judgment | CR 56 | ORCP 47 | CCP § 437c (longer notice period than FRCP 56) | C.R.C.P. 56; >= 91 days before trial |
| Vacate judgment | CR 60 | ORCP 71 | CCP § 473 / § 663 | C.R.C.P. 60(b); 182-day outer for (b)(1)-(3) |
| Time computation | CR 6 | ORCP 10 | CCP §§ 12, 12a, 12c | C.R.C.P. 6 + C.R.S. § 24-11-101 holidays |
| Statute citation | RCW 19.16.260 (no §) | ORS 697.015 (no §) | Cal. Civ. Code § 1788.13 (with §) | C.R.S. § 13-80-103.5 (with §) |
| Case citation | Wn.2d, Wn. App., P.3d (periods) | Or, Or App, P3d (no periods) | Cal., Cal. App. (per California Style Manual) | `[YEAR] CO [###]` / `[YEAR] COA [###]` (post-2012 neutral citation + parallel P.3d) |
| Parties separator | "vs." | "v." | "v." | "v." |
| Exhibit labels | Letters (A, B, C) | Numbers (1, 2, 3) | Letters (A, B, C) — or numbers; varies | Letters (A, B, C) |
| Consumer-protection statute | RCW 19.86 (CPA) | ORS 646.605 (UTPA) | Cal. Civ. Code §§ 1788 et seq. (Rosenthal Act) + Bus. & Prof. Code §§ 17200 (UCL) | C.R.S. art. 1 of title 6 (CCPA; 3x damages + fees) |
| State debt-collection statute | RCW 19.16 | ORS 697 | Cal. Fin. Code §§ 100000 et seq. (CDCLA, 2022); Cal. Civ. Code § 1788 (Rosenthal) | C.R.S. art. 16 of title 5 (CFDCPA — recodified from Title 12 in 2022) |
| Collection-agency licensure | RCW 19.16 (Washington Collection Agency Act) | ORS 697 | CDCLA (Cal. Fin. Code §§ 100000 et seq.) | C.R.S. § 5-16-115 (AG's Collection Agency Board) |
| Credit-card SOL | 6 years (written) / 3 years (open account) | 6 years (written) | 4 years (written contract under CCP § 337) | **6 years** under C.R.S. § 13-80-103.5(1)(a) (*Hassler*, 2012 CO 24) |
| eFiling system | KCDC/KCSC portals + statewide eFile | OJD File and Serve (Tyler; statewide) | Per-county (varies; LASC, SFSC e-file via Tyler / ImageSoft / vendor mix) | CCEFS — statewide (Colorado Courts E-Filing System) |
| Family-law framework | RCW Title 26 (divorce, etc.) — not yet bundled | ORS Chapter 107 — not yet bundled | Fam. Code (divorce, custody, support) — not yet bundled | **UDMA (C.R.S. art. 10 of title 14) — bundled in `co-family-law` (Colorado is the first state with a family-law subject bundle in its initial release)** |
| Custody terminology | "Parenting plan" / RCW 26.09 | "Custody" / "parenting time" (ORS 107) | "Custody" / "visitation" / Fam. Code | "**Parental responsibilities**" (decision-making + parenting time) — Colorado replaced "custody" in 1998 |

These differences are captured throughout the skill bodies and reference files — porting templates across states requires more than search-and-replace.

## Disclaimer

Not legal advice. These plugins provide drafting assistance only. Review all generated content and confirm compliance with current court rules and local practice before filing.

## License

MIT. See [LICENSE](LICENSE).
