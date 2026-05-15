# claude-legal

A Claude Code / Cowork marketplace of plugins for preparing U.S. court documents, organized one plugin per state plus a shared plugin for federal law.

## What's in here

**Seven plugins** today — six state plugins plus one shared data-only plugin they all depend on:

- **`claude-legal-federal-laws`** — Shared, data-only plugin. Holds the canonical copy of federal consumer-finance law (FDCPA, FCRA, TILA, ECOA, EFTA, CCPA-Garnishment + Reg B/E/F/M/N/P/V/X/Z/DD), real-estate / consumer-protection adjuncts (RESPA, SCRA, Fair Housing Act, FTC Telemarketing Sales Rule), the Bankruptcy Code (Title 11 U.S.C. chapters 1, 3, 5, 7, 11, 12, 13, 15), and the model Uniform Commercial Code (Articles 1, 2, 3, 9). Every state plugin below declares it as a `dependencies:` entry in `plugin.json` and reaches it via in-tree symlinks; the Claude Code marketplace runtime auto-installs the dependency and dereferences the symlinks at install time, so each installed state plugin still has the federal content locally available.

- **`wa-court-docs`** — **Washington State.** Drafts and formats pleadings, declarations, motions, notes for motion docket, and proposed orders for Washington courts. Applies GR 14 formatting; covers King County District Court (East/Redmond, South/Burien, West/Seattle), King County Superior Court (Seattle / Kent — MRJC), and the most-populous counties' roll-up (Pierce, Snohomish, Spokane, Clark, Thurston, Kitsap, Yakima, Whatcom, Benton). The `wa-consumer-debt` bundle covers FDCPA / Reg F / RCW 19.16 / WA CPA debt-defense. Statute corpus: **75 chapters / 1,547 sections** across the RCW spanning civil procedure, evidence, special proceedings, family law, landlord-tenant, real property, business regulation, admin law, and the UCC.

- **`or-court-docs`** — **Oregon.** Applies UTCR 2.010 formatting; covers Multnomah County Circuit Court (Portland / Central Courthouse), Washington County Circuit Court (Hillsboro), and the most-populous counties' roll-up (Clackamas, Lane, Marion, Jackson, Deschutes, Linn, Benton, Yamhill, Polk, Douglas). The `or-consumer-debt` bundle covers FDCPA / Reg F / Oregon UTPA (ORS 646.605) / ORS 697 Collection Agency Registration / chain-of-title. Statute corpus: **35 ORS chapters / 5.6 MB**. Notable Oregon quirk: **no written interrogatories under ORCP without court order**.

- **`ca-court-docs`** — **California.** Applies CRC 2.100-2.119 formatting; covers Los Angeles Superior Court (LASC — Stanley Mosk), San Francisco Superior Court (SFSC — Civic Center, Dept. 302 law-and-motion), and the most-populous-counties roll-up (Orange, San Diego, Riverside, San Bernardino, Santa Clara, Alameda, Sacramento, Contra Costa, Fresno, Kern). The `ca-consumer-debt` bundle covers FDCPA / Reg F / Rosenthal Act (Cal. Civ. Code §§ 1788) / FDBPA / CDCLA (Cal. Fin. Code §§ 100000+, 2022) / chain-of-title under Cal. Comm. Code Art. 9. Statute corpus: **32 files** covering CCP (SOL, service, pleadings, motions, discovery, relief, enforcement, exemptions, trial / writs / unlawful detainer / arbitration), Civ. Code (Rosenthal Act, FDBPA, CLRA, contracts, damages, Song-Beverly), Evid. Code (key relevance/hearsay/authentication sections), Fam. Code (dissolution, property, custody, support), Prob. Code (intestate + procedure), Lab. Code (wages), B&P (UCL), Fin. Code (CDCLA), Comm. Code (UCC Articles 2/3/9). CRC corpus: **9 titles** (Titles 2/3/5/7/8 hand-authored curated commentary; Titles 1/4/9/10 puller-verbatim).

- **`co-court-docs`** — **Colorado.** Applies C.R.C.P. 10 + Chief Justice Directive 11-01 formatting (two-block caption with case-number / division / courtroom box); covers Denver District Court (2nd JD — Lindsey-Flanigan Courthouse), Arapahoe County District Court (18th JD — Centennial / Aurora / Littleton), and the most-populous-counties roll-up (Jefferson, El Paso, Adams, Boulder, Larimer, Douglas, Weld, Pueblo, Mesa, Broomfield). **Two subject-matter bundles** ship in the initial release: `co-consumer-debt` (FDCPA, Reg F, CFDCPA, CCPA, UCCC, chain-of-title, 6-year SOL on liquidated debt) and `co-family-law` (UDMA — dissolution, parental responsibilities, § 14-10-115 income-shares child support with the 93-overnight rule, maintenance, common-law marriage under *Hogsett & Neale*) — Colorado is the first state with two bundles at initial release, **22 SKILL.md files**. Statute corpus: 14 articles / 2.0 MB covering UCC, UCCC, CFDCPA, CCPA, mediation, judgments, exemptions, garnishment, limitations, UDMA, UCCJEA, APA. Court rules corpus: **80 files** — 72 verbatim Chief Justice Directives (CJDs) including the Jan-2026 statewide eFiling standards, 6 paywall stubs for the commercially-licensed C.R.C.P. / CRE / C.A.R. / Colo. RPC.

- **`in-court-docs`** — **Indiana.** Applies Ind. Trial R. 5(E) formatting (Indiana lacks a single consolidated format rule; the requirements live across T.R. 5(E), T.R. 11, and county local rules); covers Marion Superior Court (Indianapolis — 36 numbered courtrooms in the City-County Building, statewide's highest civil-case-volume court) and Lake Superior Court (Crown Point with Hammond and East Chicago branches), plus the populous-counties roll-up (Allen, Hamilton, St. Joseph, Vanderburgh, Elkhart, Tippecanoe, Porter, Madison). Pro se under the *Goossens v. Goossens* same-standard rule. The `in-consumer-debt` bundle covers FDCPA / Reg F / **Indiana Uniform Consumer Credit Code** (IUCCC, IC 24-4.5) / **Deceptive Consumer Sales Act** (DCSA, IC 24-5-0.5 — Indiana's UDAP analog with treble damages + fees) / chain-of-title under Indiana UCC Article 9 (IC 26-1-9.1) / the four debt SOLs at IC 34-11-2-7/-9/-11/-13. Indiana procedural quirks worth flagging: (1) summary judgment under T.R. 56 follows ***Jarboe v. Landmark*** — movant must AFFIRMATIVELY negate an element with admissible evidence (rejected federal *Celotex* burden-shifting); (2) **T.R. 59 motion to correct error** is a required prerequisite to appeal for some issues; (3) Indiana does NOT require collection-agency licensing (defense focus shifts to chain-of-title + FDCPA + DCSA). Statewide Odyssey e-filing system since 2017.

- **`ny-court-docs`** — **New York.** Applies 22 NYCRR § 202.5 paper format and 22 NYCRR § 202.5-b NYSCEF electronic-filing format with the New York caption ("-against-" party separator, Index Number, assigned Justice + Part); covers **five flagship Supreme Court venues each as its own skill** — New York County (1st JD / Manhattan / 60 Centre Street with the $500k-threshold Commercial Division under 22 NYCRR § 202.70), Kings County (2nd JD / Brooklyn / 360 Adams Street with the high-volume CPLR 3408 foreclosure conference part), Bronx County (12th JD / 851 Grand Concourse), Nassau County (10th JD / Mineola with a $200k-threshold Commercial Division), and Queens County (11th JD / Jamaica) — **plus two dedicated Long Island District Court skills** (`ny-nassau-dc` at 99 Main Street, Hempstead, and `ny-suffolk-dc` at the Cohalan Court Complex, Central Islip) covering the Uniform District Court Act / 22 NYCRR Part 212 forum — civil jurisdiction up to $15,000, RPAPL Article 7 L&T summary proceedings, small-claims and commercial-claims parts; the principal pro-se debt-defense forum on Long Island — plus dedicated venue skills for the rest of NY's fragmented civil-court system: **`ny-nyc-civil-court`** (Civil Court of the City of New York; Civil Court Act $50k cap; 5 borough branches; the highest-volume consumer-debt-collection forum in the country; UCMS / CCEF e-filing; 22 NYCRR Part 208 with § 208.6-a default-scrutiny), **`ny-nyc-housing-court`** (Housing Part of NYC Civil Court; RPAPL Article 7 summary proceedings; Local Law 136 universal Right to Counsel; ERAP automatic stay; rent regulation overlays), **`ny-city-courts`** (~60 upstate City Courts under UCCA / 22 NYCRR Part 210, $15k cap; Buffalo / Rochester / Syracuse / Albany / Yonkers / White Plains / etc.), **`ny-justice-courts`** (~1,250 Town and Village Justice Courts under UJCA / 22 NYCRR Part 214, $3k cap; the only civil forum for eastern Suffolk County matters under $3k), and **`ny-family-court`** (FCA Articles 3-10 / 22 NYCRR Part 205; CSSA child support at FCA § 413 with $183k 2024 cap; Article 6 custody; Article 8 family-offense Orders of Protection; Article 10 abuse and neglect) — plus a long-tail Supreme Court roll-up **`ny-county-courts`** covering Suffolk / Westchester / Erie / Monroe / Onondaga / Richmond / Rockland / Albany / Orange / Dutchess / Saratoga / Oneida Supreme Court Civil Term. Pro se under the post-2023 CPLR 2106 universal affirmation under penalty of perjury (L 2023, ch 559 ended the notary-bottleneck for pro se filers). **Five subject-matter bundles** ship in the initial release: `ny-consumer-debt` (FDCPA, Reg F, **2022 Consumer Credit Fairness Act** including the 3-year SOL on consumer-credit at CPLR 213(a), heightened pleading at CPLR 3015(e), heightened default-judgment evidence at 22 NYCRR § 202.27-a, additional notice mailing at CPLR 308(six); N.Y. GBL § 600 collection-agency licensing; N.Y. GBL §§ 349 / 350 deceptive acts; CPLR 4544 small-print contracts; chain of title under N.Y. UCC Article 9 with CPLR 4518 business-records foundation per *Bank of NY Mellon v. Gordon*, 171 AD3d 197 (2d Dept 2019)); `ny-landlord-tenant` (RPAPL Article 7 summary proceedings, **2019 HSTPA** reforms, the **2024 Good Cause Eviction Law** at RPL Article 6-A, RPL § 235-b warranty of habitability, NYC right-to-counsel under Local Law 136 of 2017, ERAP stays); `ny-personal-injury` (CPLR Article 14-A pure comparative fault + Article 16 several-liability cap; **Insurance Law § 5102(d)** no-fault "serious injury" threshold + Article 51 PIP; **Labor Law § 240(1)** absolute scaffold-law liability + § 241(6) Industrial Code; **GML § 50-e** 90-day Notice of Claim against state actors; CPLR 214-a 30-month medical-malpractice SOL with continuous-treatment toll; CVA / ASA revival windows); `ny-employment` (**NYS Human Rights Law** § 296, **NYC Human Rights Law** § 8-107 with *Williams v. NYCHA* construed-broadly rule and mandatory attorney's fees; Labor Law § 191 frequency-of-pay with *Vega* late-payment liquidated damages; § 198 wage theft with 6-year SOL; **Labor Law § 740** whistleblower post-2022 expansion; NYS WARN Act 90-day notice for 50+ employees; 2018 Sexual Harassment Act; CROWN Act); `ny-commercial-disputes` (**22 NYCRR § 202.70 Commercial Division** with county-by-county $50k-$500k thresholds; **CPLR 3016(b)** fraud particularity; **BCL § 720** derivative actions and **§ 1104-a** judicial dissolution with § 1118 buyout election; **Faithless Servant Doctrine**; **GOL §§ 5-1401 / 5-1402** NY-as-destination-forum at $250k / $1M thresholds). **35 SKILL.md files** total — by far the largest state plugin in the marketplace because of NY's unusually fragmented civil-court system: 5 flagship Supreme Court skills + 1 Supreme Court roll-up + 2 Long Island District Court skills + 2 dedicated NYC Civil Court / Housing Court skills + upstate City Courts roll-up + Justice Courts roll-up + Family Court + 5 subject-matter bundles (consumer-debt + landlord-tenant + personal-injury + employment + commercial-disputes) + 13 procedural skills. NY procedural quirks worth flagging: (1) **CPLR 2103(b)(2) 5-day mail-service rule** (longer than the federal/WA/OR 3-day rule); (2) **verified-vs-unverified pleadings** under CPLR 3020 with the tactical forced-verification trigger when account-stated is alleged; (3) **CPLR 2106 universal affirmation** (post-2023) eliminating notary for pro se filers; (4) **Individual Assignment System** under 22 NYCRR § 202.3 where a single Justice owns the case through judgment with their own Part Rules; (5) **22 NYCRR § 202.48 settle-order procedure** with a jurisdictional 60-day clock under *Funk v. Barry*; (6) **20-year SOL on money judgments** at CPLR 211(b) — the longest in the U.S.; (7) **Long Island's unique District Court layer** at 22 NYCRR Part 212 — the UDCA's $15,000 civil ceiling doesn't exist in any other state and Suffolk's coverage stops at the five western towns + Brookhaven (eastern towns route to Town Justice Courts). NYSCEF mandatory e-filing in most counties since 2014-2022 rollouts.

All six state plugins are architected the same way: matter-neutral civil-procedure skills (statewide format, civil rules, evidence rules, fees and costs, local rules, citation format, online sources, discovery, first-30-days response, hearings, filing packets, post-judgment, fact-checking, deadlines) plus subject-matter bundles that plug into the procedural skills. They share federal/UCC/Bankruptcy reference content via the `claude-legal-federal-laws` dependency rather than copying it into each plugin.

The marketplace is organized one plugin per state; more state plugins can be added under `plugins/` as it grows.

## Install

Add this marketplace to Claude Code or Cowork, then install the state plugins you want:

```
/plugin marketplace add https://github.com/codearranger/claude-legal
/plugin install wa-court-docs@claude-legal
/plugin install or-court-docs@claude-legal
/plugin install ca-court-docs@claude-legal
/plugin install co-court-docs@claude-legal
/plugin install in-court-docs@claude-legal
/plugin install ny-court-docs@claude-legal
```

Each state plugin declares `claude-legal-federal-laws` as a `dependencies:` entry, so the marketplace runtime installs the shared plugin automatically — no need to install it explicitly.

## Reference corpora at a glance

| Plugin | Statutes | Court rules | Federal / UCC / Bankruptcy |
|---|---|---|---|
| `wa-court-docs` | 75 RCW chapters / 1,547 sections / 2.8 MB | 1,233 rules / 35 sets / 4.6 MB | shared (20 + 4 + 8 chapters) |
| `or-court-docs` | 35 ORS chapters / 5.6 MB | 7 rule sets / 2.3 MB | shared |
| `ca-court-docs` | 32 files (CCP / Civ / Evid / Fam / Prob / Lab / B&P / Fin / Comm) | 9 CRC titles / 17 files | shared |
| `co-court-docs` | 14 articles / 2.0 MB | 80 files (72 CJDs + 6 paywall stubs) | shared |
| `in-court-docs` | 18 articles (IGA SPA-blocked; stubs + API-key fallback) | 7 rule sets / 2.1 MB | shared |
| `ny-court-docs` | 36 NY consolidated-laws targets / ~2.9 MB verbatim via NYSENATE API (CPLR 15 articles + GOB + GBS + RPAPL + RPL + UCC + DRL + FCT + EPT + GCN + BNK) | 20 rule sets via `pull_ny_court_rules.py`: 15 Parts of 22 NYCRR pulled verbatim / ~1.2 MB (Parts 100 / 104 / 125 / 130 / 202 incl. § 202.70 Comm Div / 205 / 206 / 207 / 208 incl. § 208.42 Housing / 210 / 212 / 214 / 216 / 220 / 221) + 5 pointer stubs (Part 1200 Rules of Prof Conduct, Tanbook, NYC Civil Court directives, Nassau / Suffolk DC local rules) | shared |
| `claude-legal-federal-laws` | n/a | n/a | **20 federal-debt-laws + 4 UCC + 8 Bankruptcy** |

## Repo layout

```
claude-legal/
├── .claude-plugin/
│   └── marketplace.json              # Marketplace manifest
├── .github/workflows/
│   ├── lint-skills.yml               # CI: runs lint on every push/PR
│   └── refresh-references.yml        # Quarterly cron + workflow_dispatch refresh
├── plugins/
│   ├── claude-legal-federal-laws/    # SHARED data-only plugin
│   │   ├── .claude-plugin/plugin.json
│   │   ├── README.md
│   │   └── references/
│   │       ├── federal-debt-laws/    # FDCPA, FCRA, TILA, ECOA, EFTA, Garnishment, RESPA, SCRA, FHA, TSR + Reg B/E/F/M/N/P/V/X/Z/DD
│   │       ├── federal-bankruptcy/   # Title 11 U.S.C. chapters 1, 3, 5, 7, 11, 12, 13, 15
│   │       └── ucc-model/            # Model UCC Articles 1, 2, 3, 9
│   ├── wa-court-docs/                # Washington (21 skills)
│   ├── or-court-docs/                # Oregon (21 skills)
│   ├── ca-court-docs/                # California (21 skills)
│   ├── co-court-docs/                # Colorado (22 skills — incl. co-family-law)
│   ├── in-court-docs/                # Indiana (21 skills)
│   └── ny-court-docs/                # New York (35 skills — 5 flagship Supreme Court venues + 2 dedicated Long Island District Courts + 2 NYC Civil/Housing Court skills + upstate City Courts + Justice Courts + Family Court + 5 subject bundles)
└── scripts/                          # Shared marketplace scripts
    ├── lint-skills.py                # Frontmatter + name/dir-match linter
    ├── hooks/pre-commit              # Symlink target for git hook
    ├── pull_court_rules.py           # courts.wa.gov → WA court rules
    ├── pull_wa_rcw.py                # app.leg.wa.gov → WA RCW chapters
    ├── pull_oregon_rules.py          # oregonlegislature.gov + courts.oregon.gov SharePoint → OR court rules
    ├── pull_oregon_ors.py            # oregonlegislature.gov → OR ORS chapters
    ├── pull_ca_court_rules.py        # courts.ca.gov/cms/rules → CA court rules
    ├── pull_ca_statutes.py           # leginfo.legislature.ca.gov → CA statute sections
    ├── pull_co_court_rules.py        # coloradojudicial.gov → CO Chief Justice Directives + paywall stubs
    ├── pull_co_statutes.py           # content.leg.colorado.gov C.R.S. PDFs → CO statute articles
    ├── pull_indiana_rules.py         # rules.incourts.gov + in.gov/courts/files → IN court rules
    ├── pull_indiana_statutes.py      # iga.in.gov (API-key fallback) → IN Code articles
    ├── pull_federal_debt_laws.py     # USC titles 11/12/15/42/50 + CFR titles 12/16 → shared federal corpus
    └── pull_ucc.py                   # law.cornell.edu/ucc → shared model UCC
```

Each state plugin's directory mirrors the same shape:

```
<state>-court-docs/
├── .claude-plugin/plugin.json        # declares: dependencies: [claude-legal-federal-laws]
├── skills/                           # 21 SKILL.md files (22 for co with co-family-law)
│   ├── <state>-statewide-format/     # state's format rule (GR 14 / UTCR 2.010 / CRC 2.100 / C.R.C.P. 10 / T.R. 5(E))
│   ├── <state>-<primary-court>/      # high-volume court 1
│   ├── <state>-<secondary-court>/    # high-volume court 2
│   ├── <state>-county-courts/        # populous-counties roll-up
│   ├── <state>-pro-se/               # pro-se drafting framework adapted for the state
│   ├── <state>-law-references/       # canonical reference corpora (court-rules, statutes, federal symlinks)
│   ├── <state>-discovery/            # state's discovery rules
│   ├── <state>-hearings/             # oral argument, courtroom etiquette
│   ├── <state>-post-judgment/        # vacation, garnishment, exemptions
│   ├── <state>-first-30-days/        # answer, defenses, counterclaims
│   ├── <state>-fact-check/           # citation verification
│   ├── <state>-deadlines/            # time computation + state holidays
│   ├── <state>-draft-{motion,declaration,note,order}/  # scaffolders
│   ├── <state>-quality-check/        # pre-filing format + content QC
│   ├── <state>-schedule-hearing/     # state's scheduling protocol
│   ├── <state>-file-packet/          # assemble + preflight a packet
│   ├── <state>-submit-order/         # post-hearing signed-order transmittal
│   └── <state>-consumer-debt/        # consumer-debt subject-matter bundle
├── scripts/
│   ├── format-check.py               # state's format-rule compliance
│   └── case-calendar.py              # state-specific deadline arithmetic
└── evals/                            # drafting / formatting / procedural / subject-matter / integration
```

## Quarterly refresh

A GitHub Actions workflow (`.github/workflows/refresh-references.yml`) runs every quarter (Jan / Apr / Jul / Oct 1 at 17:00 UTC) plus on `workflow_dispatch`, with a `target` selector covering `all` / `federal` / `wa` / `or` / `ca` / `co` / `in` / `ny`. Each leg refreshes its state's content corpora via the matching pull scripts above, lints, and opens a PR auto-assigned for review. Federal content refreshes once per quarter (single canonical copy in the shared plugin) instead of per state. **New York is fully wired in**: `pull_ny_court_rules.py` uses **curl_cffi** with Chrome TLS impersonation (optionally over a warpsocks HTTP proxy via the `NY_RULES_PROXY` env var) to pull **15 Parts of 22 NYCRR verbatim** from `www.nycourts.gov` (~1.2 MB: Parts 100 / 104 / 125 / 130 / 202 incl. § 202.70 Commercial Division / 205 / 206 / 207 / 208 incl. § 208.42 Housing Part / 210 / 212 / 214 / 216 / 220 / 221) plus 5 pointer stubs for paywalled / PDF-only sources (Part 1200 Rules of Professional Conduct, Tanbook, NYC Civil Court Directives, Nassau / Suffolk DC local rules). `pull_ny_statutes.py` hits the NY State Senate Open Legislation API at `legislation.nysenate.gov` (requires the `NYSENATE_API_KEY` repo secret to produce verbatim text — without the secret it writes well-formed pointer stubs covering the same 36 NY consolidated-laws targets).

## Key differences across states

The plugins are intentionally parallel, but they encode the genuine procedural differences between the jurisdictions. A few worth highlighting:

| Concept | Washington | Oregon | California | Colorado | Indiana | New York |
|---------|------------|--------|------------|----------|---------|----------|
| Format rule | GR 14 | UTCR 2.010 | CRC 2.100-2.119 | C.R.C.P. 10 + CJD 11-01 | Ind. T.R. 5(E) (distributed) | 22 NYCRR § 202.5 (paper) + § 202.5-b (NYSCEF) |
| Page 1 top margin | 3 inches | 2 inches | 1 inch | 1 inch (uniform) | 2 inches (T.R. 5(E)(2)) | 1 inch (uniform) |
| Civil rules | CR (superior) + CRLJ (district) | ORCP (unified — no district court) | CCP (Code of Civil Procedure) | C.R.C.P. (district) + Chapter 18 county-court rules | Ind. Trial Rules (T.R.) — unified | CPLR (Civil Practice Law and Rules) |
| Evidence rules | ER (court rule) | OEC (statutory at ORS Ch. 40) | CEC (statutory at Cal. Evid. Code) | CRE (court rule) | Ind. Evid. R. (IRE — court rule) | **Guide to NY Evidence** (uncodified) + CPLR Article 45 |
| Answer due | 20 days | 30 days | 30 days | **21 days** (in-state); 35 (out-of-state) | **20 days** (T.R. 6(C)) | **20 days** in-state personal / **30 days** substituted / out-of-state / mail |
| Failure to state | CR 12(b)(6) / CRLJ 12(b)(6) | ORCP 21 A(8) | CCP § 430.10(e) (general demurrer) | C.R.C.P. 12(b)(5) (Twombly/Iqbal under *Warne v. Hall*) | T.R. 12(B)(6) | CPLR 3211(a)(7) — pre-answer motion; consolidation rule at 3211(e) |
| Discovery — interrogatories | CR 33 (available) | **Not available** without court order | CCP § 2030.030 (**35-special-rog cap**) | C.R.C.P. 33 (available; **25-cap**) | T.R. 33(A) (available; **25-cap**) | CPLR 3130/3133(b) (available; **25-cap**) |
| Discovery — RFPs | CR 34 | ORCP 43 | CCP § 2031.010 | C.R.C.P. 34 | T.R. 34 | CPLR 3120 — "Notice for Discovery and Inspection" |
| Discovery — RFAs | CR 36 | ORCP 45 | CCP § 2033.010 | C.R.C.P. 36 | T.R. 36 | CPLR 3123 — "Notice to Admit" |
| Motion to compel | CR 37 / CRLJ 37 | ORCP 46 A | CCP § 2031.310 / § 2030.300 / § 2033.290 | C.R.C.P. 37(a) | T.R. 37 | CPLR 3124; 22 NYCRR § 202.20-f good-faith conferral |
| Motion practice timing | CR 6(d) | UTCR 5.030 + SLRs | CCP § 1005 (16 court days notice) | C.R.C.P. 121 § 1-15: 21-day response / 7-day reply / 15-page limit | T.R. 7(B) | CPLR 2214: **8-day** min service; 22 NYCRR § 202.8-b: 25-page memo / 15-page reply |
| Summary judgment | CR 56 | ORCP 47 | CCP § 437c (longer notice period than FRCP 56) | C.R.C.P. 56; ≥ 91 days before trial | T.R. 56 — ***Jarboe v. Landmark*** affirmative-negation; **rejected *Celotex* burden-shifting** | CPLR 3212 — only after issue is joined; tentative-ruling regime varies by Part |
| Vacate judgment | CR 60 | ORCP 71 | CCP § 473 / § 663 | C.R.C.P. 60(b); 182-day outer for (b)(1)-(3) | T.R. 60(B); **T.R. 59 motion to correct error** is a separate prerequisite for some appeals | CPLR 5015(a)(1)-(5); **1-year** clock for (a)(1) excusable default; no time limit for (a)(4) lack of jurisdiction |
| Time computation | CR 6 | ORCP 10 | CCP §§ 12, 12a, 12c | C.R.C.P. 6 + C.R.S. § 24-11-101 holidays | T.R. 6 + IC 1-1-9-1 holidays (incl. Good Friday + even-year Election Days) | CPLR 2103; **5-day mail rule** (longer than federal/WA/OR 3-day); NY Gen. Constr. Law § 24 holidays (incl. Lincoln's Birthday + annual Election Day) |
| Statute citation | RCW 19.16.260 (no §) | ORS 697.015 (no §) | Cal. Civ. Code § 1788.13 (with §) | C.R.S. § 13-80-103.5 (with §) | IC 34-11-2-9 (no § typically) | CPLR 3211(a)(7) (no "N.Y." prefix in body text); Tanbook style |
| Case citation | Wn.2d, Wn. App., P.3d (periods) | Or, Or App, P3d (no periods) | Cal., Cal. App. (per California Style Manual) | `[YEAR] CO [###]` / `[YEAR] COA [###]` (post-2012 neutral + parallel P.3d) | N.E.3d (Ind. or Ind. Ct. App.) | NY3d / AD3d / Misc 3d (no periods — Tanbook convention) |
| Parties separator | "vs." | "v." | "v." | "v." | "v." | **"-against-"** |
| Exhibit labels | Letters (A, B, C) | Numbers (1, 2, 3) | Letters (A, B, C) — or numbers; varies | Letters (A, B, C) | Letters (A, B, C) | Letters (A, B, C) |
| Consumer-protection statute | RCW 19.86 (CPA) | ORS 646.605 (UTPA) | Cal. Civ. Code §§ 1788 et seq. (Rosenthal Act) + Bus. & Prof. Code §§ 17200 (UCL) | C.R.S. art. 1 of title 6 (CCPA; 3x damages + fees) | IC 24-5-0.5 (DCSA — 3x damages + fees, deceptive-consumer-sales focus) | N.Y. GBL §§ 349/350 (deceptive acts and false advertising; $50 min / $1,000 willful cap) |
| State debt-collection statute | RCW 19.16 | ORS 697 | Cal. Fin. Code §§ 100000 et seq. (CDCLA, 2022); Cal. Civ. Code § 1788 (Rosenthal) | C.R.S. art. 16 of title 5 (CFDCPA — recodified from Title 12 in 2022) | None directly — Indiana piggybacks on federal FDCPA; IC 24-4.5 IUCCC governs consumer credit | N.Y. GBL §§ 600-606 (collection-agency licensing — NYC + certain counties); **2022 Consumer Credit Fairness Act** (CPLR 213(a) / 3015(e) / 22 NYCRR § 202.27-a / CPLR 308(six)) |
| Collection-agency licensure | RCW 19.16 (Washington Collection Agency Act) | ORS 697 (mandatory) | CDCLA (Cal. Fin. Code §§ 100000 et seq.) | C.R.S. § 5-16-115 (AG's Collection Agency Board) | **None** — Indiana doesn't require licensing | N.Y. GBL § 600 (NYC license + certain other localities) |
| Credit-card SOL | 6 yr (written) / 3 yr (open account) | 6 yr (written) | 4 yr (written; CCP § 337) | **6 yr** under C.R.S. § 13-80-103.5(1)(a) | **6 yr** on accounts (IC 34-11-2-7) / **6 yr** on written contract for money (IC 34-11-2-11) | **3 yr** on consumer-credit transactions under CPLR 213(a) (post-CCFA 2022, down from 6 yr) |
| eFiling system | KCDC/KCSC portals + statewide eFile | OJD File and Serve (Tyler) | Per-county (LASC, SFSC via Tyler / ImageSoft / vendor mix) | CCEFS — statewide | **Odyssey — statewide** since 2017 | **NYSCEF** (Supreme/County mandatory in most counties since 2014-2022); UCMS/CCEF (NYC Civil) |
| Family-law framework | RCW Title 26 (not yet bundled) | ORS Chapter 107 (not yet bundled) | Fam. Code (not yet bundled) | **UDMA (C.R.S. art. 10 of title 14) — bundled in `co-family-law`** | IC 31-15 + IC 31-17 (not yet bundled) | DRL (Domestic Relations Law) — not yet bundled |
| Landlord-tenant framework | RCW Ch. 59.18 (RLTA) — not yet bundled | ORS Ch. 90 — not yet bundled | Civ. Code §§ 1940 et seq. — not yet bundled | C.R.S. art. 12 of title 38 — not yet bundled | IC 32-31 — not yet bundled | **RPAPL Article 7 — bundled in `ny-landlord-tenant`** (incl. HSTPA 2019, Good Cause Eviction 2024, RPL § 235-b) |
| Custody terminology | "Parenting plan" / RCW 26.09 | "Custody" / "parenting time" (ORS 107) | "Custody" / "visitation" / Fam. Code | "Parental responsibilities" — replaced "custody" in 1998 | "Custody" / "parenting time" (IC 31-17) | "Custody" / "parenting time" (DRL) |

These differences are captured throughout the skill bodies and reference files — porting templates across states requires more than search-and-replace.

## Disclaimer

Not legal advice. These plugins provide drafting assistance only. Review all generated content and confirm compliance with current court rules and local practice before filing.

## License

MIT. See [LICENSE](LICENSE).
