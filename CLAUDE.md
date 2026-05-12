# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

The `claude-legal` **marketplace** — a Claude Code / Cowork marketplace of court-document plugins organized one plugin per state. It ships one plugin today: `wa-court-docs`, a drafting/format/research toolkit for Washington State court filings (consumer-debt focus, with clean slots for future subject bundles); the structure leaves clean slots for plugins covering additional states. Output is documents, not advice; everything is bracketed by a "not legal advice" disclaimer that downstream skills repeat.

> **NOT LEGAL ADVICE.** Generated content is a drafting aid; verify against current rules and case law before filing.

## Big-picture architecture

Three layers, three things to know:

1. **Marketplace → Plugin → Skill.** Two manifests (`.claude-plugin/marketplace.json` at repo root, `plugins/<plugin>/.claude-plugin/plugin.json` per plugin) plus per-skill `SKILL.md` files. The runtime loads skills by their **directory name**; the `name:` field in `SKILL.md` frontmatter must match the directory exactly or the skill won't load. The linter enforces this.

2. **Skills only — no slash commands.** Every workflow is a skill auto-invoked from natural-language triggers in its `description:` frontmatter. When adding a workflow, write it as a skill; do not add a slash command.

3. **Matter-neutral procedural skills + subject-matter bundles.** The procedural skills (`wa-statewide-format`, `wa-discovery`, `wa-hearings`, `wa-fact-check`, `wa-deadlines`, draft-* skills, etc.) know nothing about a specific area of law. Subject-matter bundles (`wa-consumer-debt` is the first; landlord-tenant / family / PI are the future slots) plug into them via composition. Don't bake subject-matter law into procedural skills.

## Skills index (19 skills)

| Skill | Role |
|---|---|
| `wa-statewide-format` | GR 14 + statewide drafting conventions |
| `wa-kcdc` | King County District Court (East/Redmond, South/Burien, West/Seattle) |
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

## Reference corpora (under `wa-law-references/references/`)

Verbatim text pulled from official sources, organized by domain:

- **`court-rules/`** — 1,233 WA court rules across 35 sets (CR, CRLJ, ER, GR, RAP, etc.) extracted from courts.wa.gov PDFs.
- **`federal-debt-laws/`** — FDCPA, FCRA, TILA, ECOA + Reg F/V/Z/B from `uscode.house.gov` USLM XML and the eCFR Versioner API.
- **`ucc-model/`** — Model UCC Articles 1, 2, 3, 9 (Cornell LII).
- **`wa-rcw-debt/`** — 477 sections across 21 debt-relevant RCW chapters from `app.leg.wa.gov`.
- **`legal-data-apis.md`** — agent-facing index of the structured APIs above (USLM XML, eCFR Versioner, CourtListener, Caselaw Access Project, RECAP). Read this when fact-checking or pulling fresh law programmatically.
- **`online-sources.md`** — canonical human-facing URLs for the same sources.

Each corpus dir has its own `README.md` with citation tables and a "re-pull" command. The four `scripts/pull_*.py` are reusable; they are also wired into the quarterly remote-agent routine (`trig_018yahbiUwS1uTUJSuDNrCqG`) which runs Jan/Apr/Jul/Oct 1 at 17:00 UTC and opens a single PR if anything changed.

## Common commands

```bash
# Lint every SKILL.md in the marketplace (frontmatter + name/dir match)
python3 scripts/lint-skills.py

# Install the pre-commit hook (one-time, per checkout)
ln -sf ../../scripts/hooks/pre-commit .git/hooks/pre-commit

# Refresh reference corpora (need: python3.10+, poppler for court-rules)
brew install poppler   # one-time
python3 scripts/pull_court_rules.py --workers 12 \
  --manifest plugins/wa-court-docs/skills/wa-law-references/references/court-rules/_manifest.json
python3 scripts/pull_federal_debt_laws.py
python3 scripts/pull_ucc.py --workers 8
python3 scripts/pull_wa_rcw.py --workers 12

# Plugin-internal helpers (used by certain skills)
python3 plugins/wa-court-docs/scripts/format-check.py <file>   # GR 14 compliance
python3 plugins/wa-court-docs/scripts/case-calendar.py ...     # CR 6 deadline arithmetic
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

- The diff lives entirely under `plugins/wa-court-docs/skills/wa-law-references/references/<corpus>/`.
- Bump `wa-law-references`'s `SKILL.md` `version:` (PATCH for routine refresh, MINOR if a new corpus dir was added).
- Do **not** also bump `plugin.json` for a routine corpus refresh; reserve plugin-version bumps for things that change which skills exist.

The quarterly agent routine handles this automatically — it stages only the references dir and opens a PR. When reviewing that PR, decide whether the bump is PATCH (routine refresh) or MINOR (e.g., new release point worth flagging) and edit the SKILL.md before merging.

## Repo layout (at a glance)

```
.claude-plugin/marketplace.json     # marketplace manifest (metadata.version)
.github/workflows/lint-skills.yml   # CI: runs lint on push/PR
plugins/wa-court-docs/
  .claude-plugin/plugin.json        # plugin manifest (version)
  skills/<skill>/SKILL.md           # one per skill (version: in frontmatter)
  skills/<skill>/references/*.md    # reference content the skill cites
  scripts/format-check.py           # GR 14 compliance (used by some skills)
  scripts/case-calendar.py          # CR 6 deadline arithmetic
  evals/                            # drafting / formatting / procedural / subject-matter / integration
scripts/
  lint-skills.py                    # frontmatter + name/dir-match linter
  hooks/pre-commit                  # symlink target for .git/hooks/pre-commit
  pull_court_rules.py               # courts.wa.gov → court-rules/
  pull_federal_debt_laws.py         # uscode.house.gov + ecfr.gov → federal-debt-laws/
  pull_ucc.py                       # law.cornell.edu/ucc → ucc-model/
  pull_wa_rcw.py                    # app.leg.wa.gov → wa-rcw-debt/
```
