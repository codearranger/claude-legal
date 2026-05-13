# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

The `claude-legal` **marketplace** — a Claude Code / Cowork marketplace of court-document plugins organized one plugin per state. It ships **two** plugins today:

- **`wa-court-docs`** — Washington State (GR 14 formatting, King County District + Superior + populous-counties roll-up, RCW 19.16 / WA CPA consumer-debt bundle).
- **`or-court-docs`** — Oregon (UTCR 2.010 formatting, Multnomah + Washington County Circuit Court + populous-counties roll-up, ORS 697 / UTPA consumer-debt bundle).

Both plugins are architected identically: matter-neutral civil-procedure skills plus subject-matter bundles (starting with consumer-debt defense in each state). The structure leaves clean slots for plugins covering additional states.

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
| `wa-pro-se` | Pro se workflows; Parker framework; service |
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
| `or-pro-se` | Pro se workflows; Parker framework adapted for Oregon; signature block omits OSB#; service under ORCP 9 |
| `or-law-references` | ORCP civil rules, OEC evidence rules, ORS 20 fees, Oregon Style Manual citation format, local SLRs — **canonical reference corpora live here** |
| `or-discovery` | RFPs, RFAs, depositions, meet-and-confer (SLR 5.045/5.046), motion to compel under ORCP 46 A. **Key Oregon distinction: no written interrogatories under ORCP without court order.** |
| `or-hearings` | Oral argument, WebEx, courtroom etiquette, hearing-day checklist |
| `or-post-judgment` | ORCP 71 vacation, ORS 18.600+ garnishment, ORS 18.345-385 exemptions, ORS 18.265+ debtor exam, ORS 18.235 satisfaction |
| `or-first-30-days` | Answer, ORCP 21 motion-to-dismiss triage, affirmative defenses, counterclaims |
| `or-fact-check` | Citation verification against canonical sources; Oregon Style Manual conventions |
| `or-deadlines` | ORCP 10 time computation with ORS 187.010 holidays (note: no day-after-Thanksgiving in Oregon) |
| `or-draft-motion` / `-declaration` / `-note` / `-order` | Scaffolders |
| `or-quality-check` | Pre-filing format + content QC (UTCR 2.010 + Parker framework) |
| `or-schedule-hearing` | JA date-request email (Multnomah) / Civil Division (Washington Co) / per-county routing |
| `or-file-packet` | Assemble + preflight a packet for OJD File and Serve |
| `or-submit-order` | Post-hearing signed-order transmittal; UTCR 5.100 3-court-day service |
| `or-consumer-debt` | Subject bundle: FDCPA, Reg F, **ORS 697 collection-agency registration**, **Oregon UTPA (ORS 646.605)**, chain of title, 5 fact-pattern triage, RFP/RFA banks, synthetic example filings |

## Reference corpora — Washington (`wa-law-references/references/`)

Verbatim text pulled from official sources, organized by domain:

- **`court-rules/`** — 1,233 WA court rules across 35 sets (CR, CRLJ, ER, GR, RAP, etc.) extracted from courts.wa.gov PDFs.
- **`federal-debt-laws/`** — FDCPA, FCRA, TILA, ECOA + Reg F/V/Z/B from `uscode.house.gov` USLM XML and the eCFR Versioner API.
- **`ucc-model/`** — Model UCC Articles 1, 2, 3, 9 (Cornell LII).
- **`wa-rcw-debt/`** — 477 sections across 21 debt-relevant RCW chapters from `app.leg.wa.gov`.
- **`legal-data-apis.md`** — agent-facing index of the structured APIs above.
- **`online-sources.md`** — canonical human-facing URLs for the same sources.

## Reference corpora — Oregon (`or-law-references/references/`)

Mirrors the WA corpora structure; populated by future pull scripts (initial PR ships scaffolding + READMEs + manifests):

- **`court-rules/`** — Oregon court rules (ORCP, UTCR, OEC, ORAP, Multnomah SLR, Washington Co SLR) from counciloncourtprocedures.org and courts.oregon.gov.
- **`federal-debt-laws/`** — FDCPA, FCRA, TILA, ECOA, Reg F/V/Z/B (federal law; identical content to the WA corpus — re-populate from `pull_federal_debt_laws.py`).
- **`ucc-model/`** — Model UCC Articles 1, 2, 3, 9.
- **`or-ors-debt/`** — Oregon Revised Statutes chapters most relevant to civil practice (ORS 12, 14, 18, 19, 20, 21, 36, 40, 71-79, 82, 90, 105, 174, 187, 646, 697).
- **`legal-data-apis.md`** — Oregon-flavored agent-facing API index (oregonlegislature.gov, CourtListener Oregon courts, etc.).
- **`online-sources.md`** — canonical URLs for Oregon law.

Each corpus dir has its own `README.md` with citation tables and a "re-pull" command. The `scripts/pull_*.py` are reusable across plugins; they are wired into the quarterly remote-agent routine (`trig_018yahbiUwS1uTUJSuDNrCqG`) which runs Jan/Apr/Jul/Oct 1 at 17:00 UTC and opens a single PR if anything changed.

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
6. **Federal law is shared content but per-plugin copies**: the FDCPA/FCRA/TILA text is identical across all states; mirror it into each plugin's `federal-debt-laws/` corpus rather than cross-linking (keeps each plugin self-contained for downstream installers).
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
.github/workflows/lint-skills.yml   # CI: runs lint on push/PR
plugins/wa-court-docs/
  .claude-plugin/plugin.json        # plugin manifest (version)
  skills/<skill>/SKILL.md           # one per skill (version: in frontmatter)
  skills/<skill>/references/*.md    # reference content the skill cites
  scripts/format-check.py           # GR 14 compliance
  scripts/case-calendar.py          # CR 6 deadline arithmetic
  evals/                            # drafting / formatting / procedural / subject-matter / integration
plugins/or-court-docs/
  .claude-plugin/plugin.json        # plugin manifest (version)
  skills/<skill>/SKILL.md
  skills/<skill>/references/*.md
  scripts/format-check.py           # UTCR 2.010 compliance
  scripts/case-calendar.py          # ORCP 10 deadline arithmetic with ORS 187 holidays
  evals/
scripts/
  lint-skills.py                    # frontmatter + name/dir-match linter
  hooks/pre-commit                  # symlink target for .git/hooks/pre-commit
  pull_court_rules.py               # courts.wa.gov → wa court-rules/
  pull_federal_debt_laws.py         # uscode.house.gov + ecfr.gov → federal-debt-laws/ (shared content; copied to each state plugin)
  pull_ucc.py                       # law.cornell.edu/ucc → ucc-model/ (shared)
  pull_wa_rcw.py                    # app.leg.wa.gov → wa-rcw-debt/
  # TODO: pull_oregon_rules.py       # counciloncourtprocedures.org + courts.oregon.gov → or court-rules/
  # TODO: pull_oregon_ors.py         # oregonlegislature.gov → or-ors-debt/
```
