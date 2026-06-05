# claude-legal

A Claude Code / Cowork marketplace of plugins for preparing U.S. court documents, organized one plugin per state plus a shared plugin for federal law.

> **NOT LEGAL ADVICE.** These plugins are a **drafting aid** for self-represented litigants and the practitioners who help them. They produce document drafts and procedural information; they do **not** provide legal advice, do **not** select a legal strategy for any particular user, and do **not** create an attorney-client relationship. The user is the decision-maker on every choice — what motion to file, what defense to plead, what facts to swear to, whether to settle, whether to appeal. For complex matters, or matters with substantial sums at stake, **consider consulting a licensed attorney in your jurisdiction**. Verify every rule, deadline, dollar threshold, and statutory citation against current law before filing.

## What's in here

**Thirteen plugins** — eleven state plugins plus two shared federal reference plugins. **Each plugin's `README.md` is the canonical detail**; this list links to them.

### Shared federal reference plugins

| Plugin | What it covers |
|---|---|
| [`claude-legal-federal-laws`](plugins/claude-legal-federal-laws/README.md) | Canonical federal consumer-finance corpora (FDCPA / FCRA / TILA / ECOA / Reg B-Z, RESPA / SCRA / FHA / TSR), the Bankruptcy Code, and the model UCC — a dependency of every state plugin — plus a nationwide FCRA consumer credit-report-rights skills layer. |
| [`claude-legal-immigration-laws`](plugins/claude-legal-immigration-laws/README.md) | U.S. immigration law (INA / 8 CFR / 22 CFR / FAM mirrored verbatim + EOIR court rules), an on-demand case-law index (circuits / BIA / AAO), and an 11-skill venue-independent self-help layer. |

### State plugins

| Plugin | Coverage |
|---|---|
| [`wa-court-docs`](plugins/wa-court-docs/README.md) | Washington — GR 14; 6 venues + 6 subject bundles + CPA + CEMA; 32 skills |
| [`or-court-docs`](plugins/or-court-docs/README.md) | Oregon — UTCR 2.010; Multnomah + Washington Co + roll-up; consumer-debt (no-interrogatories quirk) |
| [`ca-court-docs`](plugins/ca-court-docs/README.md) | California — CRC 2.100-2.119; LASC + SFSC + roll-up; consumer-debt |
| [`co-court-docs`](plugins/co-court-docs/README.md) | Colorado — C.R.C.P. 10 + CJD 11-01; Denver + Arapahoe + roll-up; consumer-debt + family-law; 22 skills |
| [`in-court-docs`](plugins/in-court-docs/README.md) | Indiana — T.R. 5(E); Marion + Lake + roll-up; consumer-debt + family-law; 23 skills |
| [`ny-court-docs`](plugins/ny-court-docs/README.md) | New York — 22 NYCRR § 202.5 / NYSCEF; 5 flagship Supreme Courts + District / City / Justice / Family / Housing courts; 5 subject bundles; 35 skills |
| [`oh-court-docs`](plugins/oh-court-docs/README.md) | Ohio — Civ. R. 10; 8 Common Pleas venues + municipal + family; consumer-debt + family-law; 30 skills |
| [`tn-court-docs`](plugins/tn-court-docs/README.md) | Tennessee — local-rule format; Circuit / Chancery / General Sessions; 4 subject bundles; 29 skills |
| [`mi-court-docs`](plugins/mi-court-docs/README.md) | Michigan — MCR 1.109 / 2.113; Wayne + Oakland + 36th District + family; 6 subject bundles; 29 skills |
| [`az-court-docs`](plugins/az-court-docs/README.md) | Arizona — Ariz. R. Civ. P. 10 / 7.1; Maricopa + Pima + Justice + family; 6 subject bundles; 28 skills |
| [`ar-court-docs`](plugins/ar-court-docs/README.md) | Arkansas — Ark. R. Civ. P. 10/11 + Admin. Order 19/21 (no statewide format rule); unified Circuit Court (Amendment 80) — Pulaski + Benton + Washington + District Courts + family; 6 subject bundles; 29 skills |

All state plugins are architected the same way: matter-neutral civil-procedure skills (statewide format, civil + evidence rules, fees, local rules, citation, discovery, first-30-days, hearings, filing, post-judgment, fact-check, deadlines) plus subject-matter bundles, sharing federal / UCC / Bankruptcy content via the `claude-legal-federal-laws` dependency rather than copying it per plugin. The marketplace is organized one plugin per state; more can be added under `plugins/` as it grows.

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
/plugin install oh-court-docs@claude-legal
/plugin install tn-court-docs@claude-legal
/plugin install mi-court-docs@claude-legal
/plugin install az-court-docs@claude-legal
/plugin install ar-court-docs@claude-legal
```

Each state plugin declares `claude-legal-federal-laws` as a `dependencies:` entry, so the marketplace runtime installs the shared plugin automatically — no need to install it explicitly.

## Reference corpora at a glance

| Plugin | Statutes | Court rules | Federal / UCC / Bankruptcy |
|---|---|---|---|
| `wa-court-docs` | 93 RCW chapters / 3,266 sections / ~5.5 MB | 1,233 rules / 35 sets / 4.6 MB | shared (20 + 4 + 8 chapters) |
| `or-court-docs` | 35 ORS chapters / 5.6 MB | 7 rule sets / 2.3 MB | shared |
| `ca-court-docs` | 32 files (CCP / Civ / Evid / Fam / Prob / Lab / B&P / Fin / Comm) | 9 CRC titles / 17 files | shared |
| `co-court-docs` | 14 articles / 2.0 MB | 80 files (72 CJDs + 6 paywall stubs) | shared |
| `in-court-docs` | 27 articles incl. full IC 31 family-law coverage (IGA SPA-blocked; stubs + API-key fallback) | 7 rule sets / 2.1 MB | shared |
| `ny-court-docs` | 36 NY consolidated-laws targets / ~2.9 MB verbatim via NYSENATE API (CPLR 15 articles + GOB + GBS + RPAPL + RPL + UCC + DRL + FCT + EPT + GCN + BNK) | 20 rule sets via `pull_ny_court_rules.py`: 15 Parts of 22 NYCRR pulled verbatim / ~1.2 MB (Parts 100 / 104 / 125 / 130 / 202 incl. § 202.70 Comm Div / 205 / 206 / 207 / 208 incl. § 208.42 Housing / 210 / 212 / 214 / 216 / 220 / 221) + 5 pointer stubs (Part 1200 Rules of Prof Conduct, Tanbook, NYC Civil Court directives, Nassau / Suffolk DC local rules) | shared |
| `oh-court-docs` | 20 R.C. chapters / 1,335 sections / ~2.7 MB verbatim from `codes.ohio.gov` (R.C. Chapter 1 holidays + 1302/1303/1309 UCC + 1345 CSPA + 2151/2305/2329/2333 civil enforcement + 3105/3109/3113/3115/3119/3127 family + 5321/1923 L&T + 1901/1907/1925 court-specific) | 14 rule sets via `pull_ohio_court_rules.py`: Civ. R. + Evid. R. + App. R. + Crim. R. + Juv. R. + Traffic R. + Sup. R. + Sup. Ct. Prac. R. + Prof. Cond. R. + Code of Jud. Cond. + Gov. Bar R. + Gov. Jud. R. + Rep. R. + Court of Claims local rules / ~4.8 MB | shared |
| `tn-court-docs` | 25 Tenn. Code Ann. chapters via `pull_tn_statutes.py`; well-formed pointer stubs when Justia 403s the runner | 4 statewide rule sets / ~2.7 MB / 473 rule sub-pages verbatim via `pull_tn_court_rules.py` from tncourts.gov; county local rules as a pointer stub | shared |
| `mi-court-docs` | verbatim MCL — 13 topic files / ~70 sections / ~211 KB via `pull_michigan_statutes.py` from legislature.mi.gov (objectName=mcl-600-5701 per-section scheme) | verbatim MCR (ch. 1-4) + MRE — 362 rules / ~1.4 MB via `pull_michigan_rules.py` (courtrules.net mirror; courts.michigan.gov gates its rule-asset URLs) + curated civil-rules / evidence-rules / fees / citation / key-cases / online-sources | shared |
| `az-court-docs` | verbatim A.R.S. — 12 topic files / ~60 sections via `pull_arizona_statutes.py` from azleg.gov (ungated per-section .htm fragments) | verbatim ARCP + Ariz. R. Evid. + ARFLP + JCRCP — 4 files / ~406 rules via `pull_arizona_rules.py` (courtrules.net mirror; azcourts.gov is Cloudflare-gated) + curated civil-rules / evidence-rules / family-rules / fees / citation / key-cases / online-sources | shared |
| `ar-court-docs` | verbatim Ark. Code Ann. — 36 civil + family + consumer chapters via `pull_arkansas_statutes.py` from law.justia.com/codes/arkansas (curl_cffi Chrome impersonation; retries Cloudflare 403s; BFS-walks Title→Subtitle→Chapter→part/subchapter→Section) | verbatim Ark. R. Civ. P. + Ark. R. Evid. + Arkansas District Court Rules + Sup. Ct./Ct. App. Rules — 233 rules / ~900 KB via `pull_arkansas_rules.py` (`pdftotext` from the official opinions.arcourts.gov Court Rules PDFs) + curated civil-rules / evidence-rules / fees / citation / key-cases / online-sources / legal-data-apis | shared |
| `claude-legal-federal-laws` | n/a | n/a | **20 federal-debt-laws + 4 UCC + 8 Bankruptcy** |
| `claude-legal-immigration-laws` | INA = 8 U.S.C. ch 12, 5 subchapters / ~1.6 MB verbatim via `pull_ina.py` (+ INA↔8 USC crosswalk) | 33 CFR parts / ~3.6 MB verbatim via `pull_immigration_cfr.py` (8 CFR DHS ch I + EOIR/BIA ch V + 22 CFR visa/passport); EOIR court-rules corpus (binding 8 CFR 1003/1240/1208 + ICPM / BIA-PM stubs via `pull_eoir_manuals.py`) | n/a — standalone; FAM ~3.6 MB verbatim via `pull_fam.py`; **11-skill self-help layer** (v0.3.0); case law (circuits / BIA / AAO) on-demand per `legal-data-apis.md` |

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
│   ├── claude-legal-immigration-laws/  # SHARED immigration plugin: reference corpora + 11-skill self-help layer (v0.3.0)
│   │   ├── .claude-plugin/plugin.json
│   │   ├── skills/                        # 11 venue-independent skills (immigration-pro-se, eoir-immigration-courts, eoir-removal-defense, bia-appeals, circuit-petition-for-review, consular-visa-refusal, …)
│   │   └── references/
│   │       ├── immigration-statutes/      # INA = 8 U.S.C. ch 12 (5 subchapters) + INA↔8 USC crosswalk
│   │       ├── immigration-regulations/   # curated 8 CFR (DHS ch I + EOIR/BIA ch V) + 22 CFR visa/passport
│   │       ├── foreign-affairs-manual/    # FAM verbatim (~3.6 MB; puller AIA-chases fam.state.gov's omitted TLS intermediate + crawls its JSON TOC API)
│   │       ├── court-rules/               # EOIR ICPM + BIA Practice Manual stubs (binding rules = 8 CFR 1003/1240/1208)
│   │       ├── legal-data-apis.md         # on-demand case law: circuits / BIA / AAO
│   │       └── online-sources.md          # canonical human-facing URLs
│   ├── wa-court-docs/                # Washington (30 skills — 6 venues incl. wa-family-court + 6 subject bundles: consumer-debt + family-law + landlord-tenant + personal-injury + employment + commercial-disputes)
│   ├── or-court-docs/                # Oregon (21 skills)
│   ├── ca-court-docs/                # California (21 skills)
│   ├── co-court-docs/                # Colorado (22 skills — incl. co-family-law)
│   ├── in-court-docs/                # Indiana (23 skills — adds in-family-court + in-family-law)
│   ├── ny-court-docs/                # New York (35 skills — 5 flagship Supreme Court venues + 2 dedicated Long Island District Courts + 2 NYC Civil/Housing Court skills + upstate City Courts + Justice Courts + Family Court + 5 subject bundles)
│   ├── oh-court-docs/                # Ohio (30 skills — 8 flagship Common Pleas + Common Pleas roll-up + Municipal Court layer + Family Court + 2 subject bundles)
│   ├── tn-court-docs/                # Tennessee (29 skills — 4 flagship counties + General Sessions + county roll-up + split family/juvenile + 4 subject bundles)
│   ├── mi-court-docs/                # Michigan (29 skills — Wayne/Oakland Circuit + 36th District + Circuit/District roll-ups + Family Division + 6 subject bundles)
│   ├── az-court-docs/                # Arizona (28 skills — Maricopa/Pima Superior + Justice Courts + Superior-courts roll-up + Family Department + 6 subject bundles)
│   └── ar-court-docs/                # Arkansas (29 skills — Amendment 80 unified Circuit Court: Pulaski/Benton/Washington + District Courts + county roll-up + Domestic Relations family court + 6 subject bundles)
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
    ├── pull_ny_court_rules.py        # nycourts.gov via curl_cffi + warpsocks → 22 NYCRR Parts
    ├── pull_ny_statutes.py           # legislation.nysenate.gov API → NY consolidated laws
    ├── pull_ohio_court_rules.py      # supremecourt.ohio.gov PDFs → 14 Ohio rule sets
    ├── pull_ohio_statutes.py         # codes.ohio.gov HTML → R.C. chapters
    ├── pull_tn_court_rules.py        # tncourts.gov per-rule HTML sub-pages → TN court rules
    ├── pull_tn_statutes.py           # law.justia.com/codes/tennessee/ → TN Code chapters (stubs on 403)
    ├── pull_michigan_rules.py        # courtrules.net mirror → MI MCR (ch. 1-4) + MRE verbatim (courts.michigan.gov gates its asset URLs)
    ├── pull_michigan_statutes.py     # legislature.mi.gov (objectName per-section scheme) → verbatim MCL
    ├── pull_arizona_rules.py         # courtrules.net mirror → AZ ARCP + Ariz. R. Evid. + ARFLP + JCRCP verbatim (azcourts.gov is Cloudflare-gated)
    ├── pull_arizona_statutes.py      # azleg.gov (ungated per-section .htm fragments) → verbatim A.R.S.
    ├── pull_federal_debt_laws.py     # USC titles 11/12/15/42/50 + CFR titles 12/16 → shared federal corpus
    ├── pull_ucc.py                   # law.cornell.edu/ucc → shared model UCC
    ├── pull_ina.py                   # uscode.house.gov USLM XML → INA (8 U.S.C. ch 12)
    ├── pull_immigration_cfr.py       # ecfr.gov versioner API → 8 CFR + 22 CFR immigration parts
    ├── pull_fam.py                   # fam.state.gov JSON TOC API + /FAM/<vol>/<id>.html (AIA-chases the server's omitted TLS intermediate) → FAM verbatim
    └── pull_eoir_manuals.py          # justice.gov EOIR ICPM + BIA Practice Manual (JS-rendered + Akamai-gated) → court-rules/ pointer stubs
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

A GitHub Actions workflow (`.github/workflows/refresh-references.yml`) runs every quarter (Jan / Apr / Jul / Oct 1 at 17:00 UTC) plus on `workflow_dispatch`, with a `target` selector covering `all` / `federal` / `immigration` / `wa` / `or` / `ca` / `co` / `in` / `ny` / `oh` / `tn` / `mi` / `az`. Each leg refreshes its state's content corpora via the matching pull scripts above, lints, and opens a PR auto-assigned for review. Federal content refreshes once per quarter (single canonical copy in the shared plugin) instead of per state. **New York is fully wired in**: `pull_ny_court_rules.py` uses **curl_cffi** with Chrome TLS impersonation to pull **15 Parts of 22 NYCRR verbatim** from `www.nycourts.gov` (~1.2 MB: Parts 100 / 104 / 125 / 130 / 202 incl. § 202.70 Commercial Division / 205 / 206 / 207 / 208 incl. § 208.42 Housing Part / 210 / 212 / 214 / 216 / 220 / 221) plus 5 pointer stubs for paywalled / PDF-only sources (Part 1200 Rules of Professional Conduct, Tanbook, NYC Civil Court Directives, Nassau / Suffolk DC local rules). For developer workstations the puller honors an optional **`NY_RULES_PROXY`** env var pointing at a Cloudflare-Warp HTTP endpoint so nycourts.gov sees a Cloudflare-trusted source IP — this proxy is LAN-only; the quarterly CI workflow runs without it and the per-file regression check keeps committed verbatim content in place. `pull_ny_statutes.py` hits the NY State Senate Open Legislation API at `legislation.nysenate.gov` (requires the `NYSENATE_API_KEY` repo secret to produce verbatim text — without the secret it writes well-formed pointer stubs covering the same 36 NY consolidated-laws targets).

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
| Family-law framework | **RCW Title 26 — bundled in `wa-family-law`** (community-property regime under RCW 26.16; RCW 26.09 dissolution; RCW 26.18/26.19 income-shares CS with Washington Economic Table; RCW 26.26A UPA) | ORS Chapter 107 (not yet bundled) | Fam. Code (not yet bundled) | **UDMA (C.R.S. art. 10 of title 14) — bundled in `co-family-law`** | IC 31-15 + IC 31-17 (not yet bundled) | DRL (Domestic Relations Law) — not yet bundled |
| Landlord-tenant framework | **RCW Ch. 59.18 RLTA — bundled in `wa-landlord-tenant`** (incl. SB 5160 just-cause 2021, HB 1815 statewide tenant Right to Counsel, ERP) | ORS Ch. 90 — not yet bundled | Civ. Code §§ 1940 et seq. — not yet bundled | C.R.S. art. 12 of title 38 — not yet bundled | IC 32-31 — not yet bundled | **RPAPL Article 7 — bundled in `ny-landlord-tenant`** (incl. HSTPA 2019, Good Cause Eviction 2024, RPL § 235-b) |
| Personal-injury framework | **RCW 4.22 + 7.70 + 7.72 — bundled in `wa-personal-injury`** (pure comparative fault; WPLA; 8-year statute of repose for med-mal; Notice of Tort Claim under 4.92/4.96) | Not yet bundled | Not yet bundled | Not yet bundled | Not yet bundled | **CPLR Article 14-A + Labor Law § 240 — bundled in `ny-personal-injury`** |
| Employment framework | **RCW 49 + 50A + 51 — bundled in `wa-employment`** (WLAD at RCW 49.60 with no damages cap + 8+ employer; PFML; non-compete reform at RCW 49.62; L&I exclusive remedy) | Not yet bundled | Not yet bundled | Not yet bundled | Not yet bundled | **NYS/NYC HRL + Labor Law — bundled in `ny-employment`** |
| Commercial-disputes framework | **RCW 19.86 + 23B + 25.15 + 62A — bundled in `wa-commercial-disputes`** (WA CPA with *Hangman Ridge* 5-element test + treble damages; WBCA; LLC Act; UCC; MAR under RCW 7.06) | Not yet bundled | Not yet bundled | Not yet bundled | Not yet bundled | **CPLR § 202.70 Commercial Division + BCL — bundled in `ny-commercial-disputes`** |
| Custody terminology | "Parenting plan" / RCW 26.09 | "Custody" / "parenting time" (ORS 107) | "Custody" / "visitation" / Fam. Code | "Parental responsibilities" — replaced "custody" in 1998 | "Custody" / "parenting time" (IC 31-17) | "Custody" / "parenting time" (DRL) |

These differences are captured throughout the skill bodies and reference files — porting templates across states requires more than search-and-replace.

## Disclaimer

**Not legal advice.** These plugins provide drafting assistance only — they produce document drafts and procedural information for self-represented litigants and the practitioners who help them. They do **not** provide legal advice, do **not** select a strategy for any particular user, and do **not** create an attorney-client relationship. The user is the decision-maker on every legal choice.

**Consider consulting a licensed attorney in your jurisdiction** for complex matters, matters with substantial sums at stake, criminal matters, or any matter where the law or its application to specific facts is unclear.

Review all generated content carefully. Verify every rule, deadline, dollar threshold, and statutory citation against current law before filing. Court rules change, statutes are amended, and case law evolves — what these plugins encode at any given version may not reflect the law in force when the document is filed.

## License

MIT. See [LICENSE](LICENSE).
