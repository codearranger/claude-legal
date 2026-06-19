# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

The `claude-legal` **marketplace** — a Claude Code / Cowork marketplace of court-document plugins organized one plugin per state, plus two shared federal reference plugins. It ships **thirteen plugins total — eleven state plugins + two shared federal reference plugins**. **Each plugin's `README.md` is the canonical detail** on skills, venues, subject bundles, reference corpora, and quirks.

- **`claude-legal-federal-laws`** — Shared plugin holding the canonical copy of federal U.S. debt-collection and consumer-finance law (FDCPA, FCRA, TILA, ECOA, Reg B–Z), the model UCC (Articles 1, 2, 3, 9), the Bankruptcy Code (Title 11 chapters 1–15), and the Americans with Disabilities Act (42 U.S.C. ch. 126) with its DOJ/EEOC implementing regulations (29 CFR 1630; 28 CFR 35/36 incl. the 2010 ADA Standards). Every state plugin declares this as a dependency and symlinks into its `references/` tree. Also ships a 5-skill nationwide FCRA consumer credit-report-rights self-help layer (`consumer-report-ordering`, `consumer-credit-disputes`, `consumer-report-accuracy`, `consumer-harm-documentation`, `consumer-credit-monitoring`), an `ada-rights` ADA self-help skill (Title I/II/III accommodation requests, grievances, DOJ complaints, EEOC charge intake), plus a `case-law-research` skill that drives the bundled CourtListener + Legal Data Hunter MCP servers.

- **`claude-legal-immigration-laws`** — Shared, venue-independent plugin for U.S. immigration law. Snapshotted verbatim: INA (8 U.S.C. Chapter 12), curated 8 CFR (DHS ch. I + EOIR/BIA ch. V) + 22 CFR visa/passport, and the Foreign Affairs Manual (AIA-chased from fam.state.gov). EOIR court-rules corpus (binding 8 CFR 1003/1240/1208 + ICPM/BIA-manual pointer stubs). Case law is on-demand (not snapshotted) via CourtListener + Legal Data Hunter. Also ships a 12-skill venue-independent self-help layer.

- **`wa-court-docs`** — Washington State. GR 14 formatting; 33 skills including 6 venue skills + 6 subject bundles (consumer-debt, family-law, landlord-tenant, personal-injury, employment, commercial-disputes) + wa-cpa + wa-cema + a federal W.D. Wash. pro se venue skill. Pioneers the "thin-skill" architecture.

- **`or-court-docs`** — Oregon. UTCR 2.010 formatting; Multnomah + Washington County Circuit Court + populous-counties roll-up; consumer-debt bundle (ORS 697 / UTPA); 21 skills. Key quirk: no written interrogatories without court order.

- **`ca-court-docs`** — California. CRC 2.100-2.119 formatting; LASC + SFSC + populous-counties roll-up; consumer-debt bundle (Rosenthal Act / FDBPA / CDCLA); 21 fully-authored skills.

- **`co-court-docs`** — Colorado. C.R.C.P. 10 + CJD 11-01 formatting (two-block caption with case-number/division/courtroom box); Denver + Arapahoe + roll-up; consumer-debt + family-law bundles; 22 skills.

- **`in-court-docs`** — Indiana. Ind. T.R. 5(E) formatting; Marion + Lake + populous-counties roll-up; consumer-debt + family-law bundles; 23 skills. Key quirks: *Jarboe v. Landmark* summary-judgment standard; T.R. 59 motion-to-correct-error; no collection-agency licensing regime.

- **`ny-court-docs`** — New York. 22 NYCRR § 202.5 / § 202.5-b NYSCEF formatting; broadest civil-court coverage in the marketplace — 5 flagship Supreme Court venues + Long Island District Courts + NYC Civil/Housing Courts + upstate City and Justice Courts + Family Court; 5 subject bundles; 35 skills.

- **`oh-court-docs`** — Ohio. Ohio Civ. R. 10 + per-court local rules; 8 flagship Court of Common Pleas venues + municipal courts + family court; 5 subject bundles; 33 skills.

- **`tn-court-docs`** — Tennessee. No statewide page/margin/font rule (Tenn. R. Civ. P. 10/11 + local rules); Circuit / Chancery / General Sessions court layers; 4 flagship county venues + split family-court/juvenile-court venue skills; 6 subject bundles; 31 skills.

- **`mi-court-docs`** — Michigan. MCR 1.109 / 2.113 formatting; Wayne + Oakland Circuit Courts + 36th District Court (Detroit) + roll-ups + Family Division; 6 subject bundles; 29 skills.

- **`az-court-docs`** — Arizona. Ariz. R. Civ. P. 10 / 7.1 formatting; Maricopa + Pima Superior Courts + Justice Courts + Family Department + Superior-courts roll-up; 6 subject bundles; 28 skills.

- **`id-court-docs`** — Idaho. I.R.C.P. 2 / 10 form-of-documents formatting; unified District Court (7 judicial districts) + Magistrate Division; Ada County (Fourth Judicial District / Boise) + Bonneville County (Seventh Judicial District / Idaho Falls) + judicial-district roll-up + Family Court; consumer-debt + family-law bundles; 23 skills. Key quirks: time computation lives in **I.R.C.P. 2.2** (Rule 6 is *[Reserved]*), the statewide format spec lives in **I.R.C.P. 2** (not Rule 10), a separate **Idaho Rules of Family Law Procedure (I.R.F.L.P.)** set heard in the Magistrate Division, community property, and Idaho Code § 73-108 holidays (no state Juneteenth; Columbus Day observed). Idaho allows interrogatories (40-cap, I.R.C.P. 33).

Output is documents, not advice; everything is bracketed by a "not legal advice" disclaimer that downstream skills repeat.

> **NOT LEGAL ADVICE.** Generated content is a drafting aid; verify against current rules and case law before filing.

## Big-picture architecture

Three layers, three things to know:

1. **Marketplace → Plugin → Skill.** Two manifests (`.claude-plugin/marketplace.json` at repo root, `plugins/<plugin>/.claude-plugin/plugin.json` per plugin) plus per-skill `SKILL.md` files. The runtime loads skills by their **directory name**; the `name:` field in `SKILL.md` frontmatter must match the directory exactly or the skill won't load. The linter enforces this.

2. **Skills only — no slash commands.** Every workflow is a skill auto-invoked from natural-language triggers in its `description:` frontmatter. When adding a workflow, write it as a skill; do not add a slash command.

3. **Matter-neutral procedural skills + subject-matter bundles.** The procedural skills (statewide-format, discovery, hearings, fact-check, deadlines, draft-* skills, etc.) know nothing about a specific area of law. Subject-matter bundles (`wa-consumer-debt`, `or-consumer-debt`; landlord-tenant / family / PI are the future slots) plug into them via composition. Don't bake subject-matter law into procedural skills.

**County coverage is skills inside the state plugin, not separate plugins.** One plugin per state; within it, a high-volume court can get its own skill (`wa-kcdc` for King County District Court, `wa-kcsc` for King County Superior Court, `or-multcc` for Multnomah Circuit, `or-wccc` for Washington County Circuit), and the long tail of counties is carried as a single roll-up skill plus reference data (`wa-county-courts`, `or-county-courts`). Name court skills `<state>-<court>` (e.g., `wa-kcdc`, `or-multcc`) or use the state-level roll-up. Don't create a plugin or a skill per county — that doesn't scale to 3,000+ U.S. counties; add detail to the roll-up's reference files on demand.

## Plugins at a glance

Per-plugin detail (full skills list, venues, subject bundles, reference corpora, refresh scripts) lives in each plugin's `README.md`. This table is the quick index.

| Plugin | Skills | Venue skills | Subject bundles | Distinctive | README |
|---|---|---|---|---|---|
| `claude-legal-federal-laws` | 7 | — | — | FCRA self-help (5) + `ada-rights` (ADA Title I/II/III) + `case-law-research`; bundled CourtListener + Legal Data Hunter MCP; shared federal corpora dependency of every state plugin | [README](plugins/claude-legal-federal-laws/README.md) |
| `claude-legal-immigration-laws` | 12 | 2 (EOIR + USCIS forums) | — | INA / 8 CFR / FAM verbatim; case law on-demand; notario-fraud warnings; severe-consequence gates | [README](plugins/claude-legal-immigration-laws/README.md) |
| `wa-court-docs` | 33 | 6 + federal W.D. Wash. pro se | consumer-debt, family-law, landlord-tenant, personal-injury, employment, commercial-disputes + wa-cpa + wa-cema | GR 14; community property; RCW 7.105 CPO; thin-skill architecture pioneer | [README](plugins/wa-court-docs/README.md) |
| `or-court-docs` | 21 | 2 + roll-up | consumer-debt | UTCR 2.010; **no interrogatories** without court order | [README](plugins/or-court-docs/README.md) |
| `ca-court-docs` | 21 | 2 + roll-up | consumer-debt | CRC 2.100-2.119; tentative-ruling regime; 35-special-rog cap; CDCLA licensing | [README](plugins/ca-court-docs/README.md) |
| `co-court-docs` | 22 | 2 + roll-up | consumer-debt, family-law | C.R.C.P. 10 + CJD 11-01; two-block caption; Frances Xavier Cabrini Day replaces Columbus Day | [README](plugins/co-court-docs/README.md) |
| `in-court-docs` | 23 | 2 + roll-up + family | consumer-debt, family-law | T.R. 5(E); *Jarboe* SJ standard; T.R. 59 as appeal prerequisite; no licensing regime | [README](plugins/in-court-docs/README.md) |
| `ny-court-docs` | 35 | 5 Supreme + 2 District + NYC Civil/Housing + City/Justice + Family + roll-up | consumer-debt, landlord-tenant, personal-injury, employment, commercial-disputes | 22 NYCRR § 202.5-b NYSCEF; CCFA 3-yr SOL; scaffold law § 240(1); "-against-" separator | [README](plugins/ny-court-docs/README.md) |
| `oh-court-docs` | 33 | 8 Common Pleas + municipal + family + roll-up | consumer-debt, family-law, personal-injury, employment, commercial-disputes | Civ. R. 10; `YYYY-Ohio-NNNN` citation; 2021 ELUA overhaul of R.C. 4112; no licensing | [README](plugins/oh-court-docs/README.md) |
| `tn-court-docs` | 31 | 4 county + General Sessions + family + juvenile + roll-up | consumer-debt, family-law, landlord-tenant, personal-injury, employment, commercial-disputes | No statewide format rule; 10-day de novo appeal; Chancery / Clerk & Master titles; Good Friday + Columbus Day holidays | [README](plugins/tn-court-docs/README.md) |
| `mi-court-docs` | 29 | 2 Circuit + 36th District + roll-ups + Family | consumer-debt, family-law, landlord-tenant, personal-injury, employment, commercial-disputes | MCR 1.109 / 2.113; no-fault auto; 100-mile rule; Lincoln's Birthday + day-after-Thanksgiving | [README](plugins/mi-court-docs/README.md) |
| `az-court-docs` | 28 | 2 Superior + Justice + Family + roll-up | consumer-debt, family-law, landlord-tenant, personal-injury, employment, commercial-disputes | ARCP 10 / 7.1 + separate ARFLP + JCRCP; community property; constitutional bar on damages caps; covenant marriage | [README](plugins/az-court-docs/README.md) |
| `id-court-docs` | 23 | 2 District (Ada + Bonneville) + Magistrate Division + judicial-district roll-up + Family Court | consumer-debt, family-law | I.R.C.P. 2 / 10; **time computation at I.R.C.P. 2.2 (Rule 6 reserved)**; separate I.R.F.L.P. family rules; community property; allows interrogatories (40-cap); § 73-108 holidays (no state Juneteenth; Columbus Day) | [README](plugins/id-court-docs/README.md) |

## Reference corpora at a glance

Each plugin's `README.md` carries full corpus detail (scope, pull mechanics, access posture). Federal / UCC / Bankruptcy content lives once in `claude-legal-federal-laws` and is symlinked into every state plugin's `references/` tree.

| Plugin | State-specific corpora | State-specific pullers | Access notes |
|---|---|---|---|
| `claude-legal-federal-laws` | `federal-debt-laws/` (20 sources), `federal-bankruptcy/` (8 chapters), `ucc-model/` (Arts 1/2/3/9), `ada-laws/` (ADA statute + 29 CFR 1630 + 28 CFR 35/36) | `pull_federal_debt_laws.py`, `pull_ucc.py`, `pull_ada.py` | uscode.house.gov USLM XML + ecfr.gov versioner; open |
| `claude-legal-immigration-laws` | `immigration-statutes/` (INA), `immigration-regulations/` (8 CFR + 22 CFR), `foreign-affairs-manual/` (FAM verbatim), `court-rules/` (EOIR stubs) | `pull_ina.py`, `pull_immigration_cfr.py`, `pull_fam.py`, `pull_eoir_manuals.py` | fam.state.gov AIA-chases omitted TLS intermediate; EOIR manuals = pointer stubs (JS-rendered + Akamai-gated) |
| `wa-court-docs` | `court-rules/` (1,233 rules / 35 sets), `wa-rcw-debt/` (93 RCW chapters / 3,266 sections) | `pull_court_rules.py`, `pull_wa_rcw.py` | courts.wa.gov PDFs; app.leg.wa.gov; open |
| `or-court-docs` | `court-rules/` (7 rule sets / ~2.4 MB), `or-ors-debt/` (35 ORS chapters / ~5.6 MB) | `pull_oregon_rules.py`, `pull_oregon_ors.py` | oregonlegislature.gov HTML/PDF; OJD SharePoint REST API; open |
| `ca-court-docs` | `court-rules/` (CRC Titles 1-10 verbatim + local rules), `ca-statutes-debt/` (33 files / ~724 KB — 19 files are hand-authored curated content; `pull_ca_statutes.py` skips any existing file lacking its verbatim marker unless `--overwrite-curated` is passed) | `pull_ca_court_rules.py`, `pull_ca_statutes.py` | courts.ca.gov / leginfo.legislature.ca.gov; open; `pull_ca_statutes.py` runs in quarterly workflow with curated-file guard |
| `co-court-docs` | `court-rules/` (72 CJDs verbatim + 6 paywalled-rule stubs; ~1.3 MB), `co-statutes-debt/` (14 C.R.S. articles / ~2.0 MB) | `pull_co_court_rules.py`, `pull_co_statutes.py` | coloradojudicial.gov CJD PDFs open; C.R.C.P./CRE/C.A.R. text paywall-gated (stubs) |
| `in-court-docs` | `court-rules/` (7 rule sets / ~2.1 MB), `in-statutes-debt/` (27 articles incl. full IC 31) | `pull_indiana_rules.py`, `pull_indiana_statutes.py` | rules.incourts.gov PDFs open; iga.in.gov API key-gated (stubs without `IGA_API_KEY`) |
| `ny-court-docs` | `court-rules/` (15 verbatim 22 NYCRR Parts + 5 stubs; ~1.2 MB), `ny-statutes-debt/` (36 consolidated-laws targets / ~2.9 MB) | `pull_ny_court_rules.py`, `pull_ny_statutes.py` | nycourts.gov Cloudflare-gated (curl_cffi + optional `NY_RULES_PROXY`; stubs on CF interstitial); NYSENATE API key-gated (`NYSENATE_API_KEY`; stubs without key) |
| `oh-court-docs` | `court-rules/` (14 rule sets / ~4.8 MB), `oh-statutes-debt/` (40 R.C. chapters / ~5.5 MB) | `pull_ohio_court_rules.py`, `pull_ohio_statutes.py` | supremecourt.ohio.gov PDFs + codes.ohio.gov HTML; open |
| `tn-court-docs` | `court-rules/` (4 statewide rule sets / ~2.7 MB / 473 sub-pages verbatim + local-rules directory), `tn-statutes-debt/` (25 TCA chapters / ~2.6 MB) | `pull_tn_court_rules.py`, `pull_tn_statutes.py` | tncourts.gov Drupal HTML open; Justia Cloudflare-gated (curl_cffi Chrome impersonation; stubs on 403) |
| `mi-court-docs` | `court-rules/` (MCR ch. 1-4 + MRE / 362 rules / ~1.4 MB), `mi-statutes-debt/` (13 topic files / ~211 KB) | `pull_michigan_rules.py`, `pull_michigan_statutes.py` | courts.michigan.gov bot-gated (mirrors courtrules.net); legislature.mi.gov open (objectName= scheme) |
| `az-court-docs` | `court-rules/` (ARCP + Evid. + ARFLP + JCRCP / ~406 rules verbatim), `az-statutes-debt/` (12 topic files) | `pull_arizona_rules.py`, `pull_arizona_statutes.py` | azcourts.gov Cloudflare-gated (mirrors courtrules.net); azleg.gov ungated .htm fragments |
| `id-court-docs` | `court-rules/` (I.R.C.P. + I.R.E. + I.R.F.L.P. + I.A.R. + I.R.E.F.S. pointer stubs), `id-statutes-debt/` (curated Idaho Code digests — Title 5/11/12/28/32/55/73 + consumer-protection/collection-agency) | `pull_idaho_rules.py`, `pull_idaho_statutes.py` | isc.idaho.gov (JS-rendered; stubs pending puller), legislature.idaho.gov Idaho Code open |

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
python3 scripts/pull_ada.py                                    # ADA statute + 29 CFR 1630 + 28 CFR 35/36 → ada-laws/
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
python3 scripts/pull_fam.py                 # FAM verbatim (AIA-chases the omitted TLS intermediate + crawls the JSON TOC API) → foreign-affairs-manual/
python3 scripts/pull_eoir_manuals.py        # EOIR ICPM + BIA Practice Manual pointer stubs (JS-rendered + Akamai-gated) → court-rules/
python3 scripts/pull_fam.py --stubs-only    # force stub shape (skip the network fetch)
# Refresh just one piece:
python3 scripts/pull_ina.py --only schII                       # just INA Subchapter II
python3 scripts/pull_immigration_cfr.py --only 8CFR-1003-eoir-bia  # just the EOIR/BIA part

# Refresh reference corpora — Michigan
python3 scripts/pull_michigan_statutes.py --workers 4 \
  --out plugins/mi-court-docs/skills/mi-law-references/references/mi-statutes-debt
python3 scripts/pull_michigan_rules.py --workers 2 \
  --out plugins/mi-court-docs/skills/mi-law-references/references/court-rules

# Michigan scripts
python3 plugins/mi-court-docs/scripts/format-check.py <file>   # MCR 1.109 / 2.113 compliance
python3 plugins/mi-court-docs/scripts/case-calendar.py ...     # MCR 1.108 deadline arithmetic with MCL 435.101 holidays (incl. Lincoln's Birthday + day-after-Thanksgiving)
python3 plugins/mi-court-docs/scripts/case-calendar.py --rules # List Michigan named deadline rules

# Refresh reference corpora — Arizona
python3 scripts/pull_arizona_statutes.py --workers 4 \
  --out plugins/az-court-docs/skills/az-law-references/references/az-statutes-debt
python3 scripts/pull_arizona_rules.py --workers 2 \
  --out plugins/az-court-docs/skills/az-law-references/references/court-rules

# Arizona scripts
python3 plugins/az-court-docs/scripts/format-check.py <file>   # Ariz. R. Civ. P. 10 / 7.1 compliance
python3 plugins/az-court-docs/scripts/case-calendar.py ...     # Ariz. R. Civ. P. 6 deadline arithmetic with A.R.S. § 1-301 holidays
python3 plugins/az-court-docs/scripts/case-calendar.py --rules # List Arizona named deadline rules

# Refresh reference corpora — Idaho
python3 scripts/pull_idaho_statutes.py --workers 4 \
  --out plugins/id-court-docs/skills/id-law-references/references/id-statutes-debt
python3 scripts/pull_idaho_rules.py --workers 2 \
  --out plugins/id-court-docs/skills/id-law-references/references/court-rules

# Idaho scripts
python3 plugins/id-court-docs/scripts/format-check.py <file>   # I.R.C.P. 2 / 10 compliance
python3 plugins/id-court-docs/scripts/case-calendar.py ...     # I.R.C.P. 2.2 deadline arithmetic (Rule 6 reserved) with Idaho Code § 73-108 holidays
python3 plugins/id-court-docs/scripts/case-calendar.py --rules # List Idaho named deadline rules
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
7. **Document output is a cross-marketplace dependency on Anthropic's document skills**: every plugin (the ten state plugins + the two shared federal plugins) declares `{"name": "document-skills", "marketplace": "anthropic-agent-skills"}` in its `plugin.json` `dependencies` array, pulling in Anthropic's DOCX / PDF / PPTX / XLSX skills from the [anthropics/skills](https://github.com/anthropics/skills) marketplace so generated filings can be produced as real Word/PDF documents. The root `marketplace.json` allowlists this via `"allowCrossMarketplaceDependenciesOn": ["anthropic-agent-skills", "claude-for-legal"]` — without that field, cross-marketplace installs fail with a `cross-marketplace` error. The dependency auto-installs only if the user has added the `anthropics/skills` marketplace (`/plugin marketplace add anthropics/skills`); otherwise it is left unresolved until they do (the root README documents this). When adding a new state plugin, copy this dependency declaration too (the scaffolder emits it). The second allowlisted marketplace, Anthropic's [claude-for-legal](https://github.com/anthropics/claude-for-legal) (practice-area plugins: commercial / privacy / corporate / employment / litigation / regulatory / AI-governance / IP / law-student / legal-clinic + the Thomson Reuters cocounsel-legal connector), is a **companion marketplace** documented in the root README install steps — no claude-legal plugin currently declares a dependency on it, but the allowlist means one can without users hitting the `cross-marketplace` error.
8. **Procedural quirks should be flagged prominently** in the relevant skill descriptions: Oregon's no-interrogatories quirk is in `or-discovery`; California's CCP 437c summary judgment timing differs from FRCP, etc.
9. **Per-plugin README is the canonical plugin detail** (the marketplace standard): every plugin carries its own `plugins/<plugin>/README.md` describing coverage, venues, subject bundles, reference corpora, and refresh scripts. The root `README.md` links to it as a one-row table entry (not an embedded paragraph), and `marketplace.json` carries only a one-sentence blurb ending "Full detail in the plugin README." Keep plugin detail in that one file so the root `README.md`, `marketplace.json`, and this `CLAUDE.md` stay slim and don't drift. When adding a plugin, author its `README.md` (the scaffolder lays down a starter).

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
  .claude-plugin/plugin.json
  references/federal-debt-laws/     # FDCPA, FCRA, TILA, ECOA, EFTA, RESPA, SCRA, FHA, TSR + Reg B/E/F/M/N/P/V/X/Z/DD — canonical source
  references/federal-bankruptcy/    # Title 11 U.S.C. chapters 1, 3, 5, 7, 11, 12, 13, 15 — canonical source
  references/ucc-model/             # Model UCC Articles 1, 2, 3, 9 — canonical source
  references/ada-laws/              # ADA (42 U.S.C. ch. 126) + 29 CFR 1630 + 28 CFR 35/36 (incl. 2010 ADA Standards) — canonical source
  skills/                           # 7 skills: consumer-report-ordering, consumer-credit-disputes, consumer-report-accuracy, consumer-harm-documentation, consumer-credit-monitoring, ada-rights, case-law-research
  .mcp.json                         # bundled free MCP servers: courtlistener + legal-data-hunter
plugins/claude-legal-immigration-laws/  # SHARED immigration-law plugin: reference corpora + 12-skill self-help layer
  .claude-plugin/plugin.json
  .mcp.json                             # bundled free MCP servers: courtlistener + legal-data-hunter
  references/immigration-statutes/      # INA = 8 U.S.C. ch 12 (5 subchapters) + INA↔8 USC crosswalk
  references/immigration-regulations/   # curated 8 CFR (DHS ch I + EOIR/BIA ch V) + 22 CFR visa/passport
  references/foreign-affairs-manual/    # FAM verbatim (~3.6 MB); puller AIA-chases fam.state.gov's omitted TLS intermediate
  references/court-rules/               # EOIR ICPM + BIA Practice Manual stubs (binding rules = 8 CFR 1003/1240/1208)
  skills/                               # 12 skills: immigration-pro-se, eoir-immigration-courts, eoir-removal-defense, eoir-motions-to-reopen-reconsider, bia-appeals, circuit-petition-for-review, consular-visa-refusal, uscis-benefit-requests, immigration-foia, immigration-deadlines, immigration-fact-check, immigration-case-law
plugins/wa-court-docs/              # 33 skills
  .claude-plugin/plugin.json        # declares dependencies: [claude-legal-federal-laws]
  skills/<skill>/SKILL.md
  skills/wa-law-references/references/
    federal-debt-laws -> ../../../../claude-legal-federal-laws/references/federal-debt-laws  (symlink)
    federal-bankruptcy -> ../../../../claude-legal-federal-laws/references/federal-bankruptcy  (symlink)
    ucc-model         -> ../../../../claude-legal-federal-laws/references/ucc-model          (symlink)
    court-rules/, wa-rcw-debt/     # state-specific content stays in-plugin
  scripts/format-check.py           # GR 14 compliance
  scripts/case-calendar.py          # CR 6 deadline arithmetic
  evals/
plugins/or-court-docs/              # 21 skills; same shape as wa-court-docs
plugins/ca-court-docs/              # 21 skills; fully-authored CA-specific content (CRC 2.100-2.119)
plugins/co-court-docs/              # 22 skills (21 standard + co-family-law)
plugins/in-court-docs/              # 23 skills (adds in-family-court + in-family-law)
plugins/ny-court-docs/              # 35 skills (5 Supreme Courts + 2 Long Island DCs + NYC Civil/Housing + City/Justice + Family + roll-up + 5 subject bundles)
plugins/oh-court-docs/              # 33 skills (8 Common Pleas + municipal + family + roll-up + 5 subject bundles)
plugins/tn-court-docs/              # 31 skills (4 county + General Sessions + family + juvenile + roll-up + 6 subject bundles)
plugins/mi-court-docs/              # 29 skills (Wayne/Oakland Circuit + 36th District + roll-ups + Family + 6 subject bundles)
plugins/az-court-docs/              # 28 skills (Maricopa/Pima + Justice Courts + Superior roll-up + Family + 6 subject bundles)
plugins/id-court-docs/              # 23 skills (Ada/Bonneville District Courts + Magistrate Division + judicial-district roll-up + Family Court + consumer-debt & family-law bundles)
scripts/
  lint-skills.py                    # frontmatter + name/dir-match linter
  hooks/pre-commit                  # symlink target for .git/hooks/pre-commit
  pull_court_rules.py               # courts.wa.gov → WA court rules
  pull_wa_rcw.py                    # app.leg.wa.gov → WA RCW chapters
  pull_federal_debt_laws.py         # uscode.house.gov + ecfr.gov → shared federal corpus
  pull_ucc.py                       # law.cornell.edu/ucc → shared model UCC
  pull_ada.py                       # uscode.house.gov + ecfr.gov → ADA statute + DOJ/EEOC regs
  pull_oregon_rules.py              # oregonlegislature.gov + courts.oregon.gov SharePoint → OR court rules
  pull_oregon_ors.py                # oregonlegislature.gov → OR ORS chapters
  pull_ca_court_rules.py            # courts.ca.gov/cms/rules → CA court rules
  pull_ca_statutes.py               # leginfo.legislature.ca.gov → CA statute sections (curated-file guard; --overwrite-curated to force)
  pull_co_court_rules.py            # coloradojudicial.gov → CO Chief Justice Directives + paywall stubs
  pull_co_statutes.py               # content.leg.colorado.gov C.R.S. PDFs → CO statute articles
  pull_indiana_rules.py             # rules.incourts.gov + in.gov/courts/files → IN court rules
  pull_indiana_statutes.py          # iga.in.gov (API-key fallback) → IN Code articles
  pull_ny_court_rules.py            # nycourts.gov via curl_cffi + optional NY_RULES_PROXY → 22 NYCRR Parts
  pull_ny_statutes.py               # legislation.nysenate.gov API → NY consolidated laws
  pull_ohio_court_rules.py          # supremecourt.ohio.gov PDFs → 14 Ohio rule sets
  pull_ohio_statutes.py             # codes.ohio.gov HTML → R.C. chapters
  pull_tn_court_rules.py            # tncourts.gov per-rule HTML sub-pages → TN court rules
  pull_tn_statutes.py               # law.justia.com/codes/tennessee/ → TN Code chapters (stubs on 403)
  pull_michigan_rules.py            # courtrules.net mirror → MI MCR (ch. 1-4) + MRE verbatim
  pull_michigan_statutes.py         # legislature.mi.gov (objectName per-section scheme) → verbatim MCL
  pull_arizona_rules.py             # courtrules.net mirror → AZ ARCP + Ariz. R. Evid. + ARFLP + JCRCP verbatim
  pull_arizona_statutes.py          # azleg.gov (ungated per-section .htm fragments) → verbatim A.R.S.
  pull_idaho_rules.py               # isc.idaho.gov → ID I.R.C.P. + I.R.E. + I.R.F.L.P. + I.A.R. + I.R.E.F.S. (JS-rendered; pointer stubs pending puller)
  pull_idaho_statutes.py            # legislature.idaho.gov → Idaho Code chapters (curated digests)
  pull_ina.py                       # uscode.house.gov USLM XML → INA (8 U.S.C. ch 12)
  pull_immigration_cfr.py           # ecfr.gov versioner API → 8 CFR + 22 CFR immigration parts
  pull_fam.py                       # fam.state.gov JSON TOC API + /FAM/<vol>/<id>.html (AIA-chases omitted TLS intermediate) → FAM verbatim
  pull_eoir_manuals.py              # justice.gov EOIR ICPM + BIA Practice Manual (JS-rendered + Akamai-gated) → pointer stubs
```

Each state plugin's directory mirrors the same shape:

```
<state>-court-docs/
├── .claude-plugin/plugin.json        # declares: dependencies: [claude-legal-federal-laws]
├── skills/                           # 21+ SKILL.md files
│   ├── <state>-statewide-format/     # state's format rule
│   ├── <state>-<primary-court>/      # high-volume court 1
│   ├── <state>-<secondary-court>/    # high-volume court 2
│   ├── <state>-county-courts/        # populous-counties roll-up
│   ├── <state>-pro-se/               # pro-se drafting framework
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
