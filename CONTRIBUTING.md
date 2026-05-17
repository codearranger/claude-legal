# Contributing to claude-legal

Thanks for thinking about contributing. This guide covers
local setup, the kinds of changes the project takes, the
conventions that keep the plugins consistent across states,
and the PR workflow.

> **NOT LEGAL ADVICE.** Every plugin in this marketplace
> ships behind that disclaimer. Contributions inherit it.
> Don't represent yourself or this project as providing
> legal advice in commits, PR descriptions, or generated
> content.

## What the project is

`claude-legal` is a Claude Code / Cowork marketplace of
court-document plugins, organized **one plugin per state**
plus a single shared data-only plugin (`claude-legal-
federal-laws`) that every state plugin depends on.

- **Marketplace** — `.claude-plugin/marketplace.json` at
  the repo root lists every plugin and gates the
  marketplace's own `metadata.version`.
- **Plugin** — `plugins/<plugin>/.claude-plugin/plugin.json`
  describes a state plugin (or the shared federal-laws
  plugin); it has its own `version`.
- **Skill** — `plugins/<plugin>/skills/<skill>/SKILL.md`
  is the unit the Claude Code runtime loads. Each `SKILL.md`
  has a `version:` in its YAML frontmatter.

The skill runtime loads skills by their **directory name**;
the `name:` field in `SKILL.md` frontmatter must equal the
directory name exactly. `scripts/lint-skills.py` enforces
this.

For the architectural overview, read `README.md` and
`CLAUDE.md`. For the patterns established across state
plugins, read `.claude/skills/scaffold-state-plugin/SKILL.md`
and its `references/` directory — those documents codify
the lessons from every state plugin in the marketplace.

## Quick start

Prereqs: Python 3.10+. Some pullers need `poppler` (for
`pdftotext`); install via Homebrew on macOS: `brew install
poppler`.

```bash
# 1. Clone
git clone https://github.com/codearranger/claude-legal
cd claude-legal

# 2. Install the pre-commit hook (one-time, per checkout)
ln -sf ../../scripts/hooks/pre-commit .git/hooks/pre-commit

# 3. Verify the lint passes
python3 scripts/lint-skills.py

# 4. Validate JSON manifests
python3 -m json.tool .claude-plugin/marketplace.json > /dev/null
python3 -m json.tool plugins/wa-court-docs/.claude-plugin/plugin.json > /dev/null
```

The lint also runs in CI on every push and PR
(`.github/workflows/lint-skills.yml`). PRs cannot land
with a failing lint.

## Kinds of contributions

### 1. Adding a new state plugin

The expected pattern. Invoke the project-scoped
`scaffold-state-plugin` skill (lives at
`.claude/skills/scaffold-state-plugin/`) — it codifies the
21-to-30-skill structure every existing state plugin
follows.

Before scaffolding, the skill asks for the state's
specifics: pleading-format rule, civil rules, evidence
code, statute code, family-law code, child-support
guideline model, property-distribution regime, primary +
secondary courts, etc. Have those answers ready.

The scaffold script (`scaffold-state.py`) produces a
**lint-clean skeleton** — the substantive content for each
SKILL.md and reference file still has to be researched and
authored against the state's authoritative sources.

Read these three docs before starting:

- `.claude/skills/scaffold-state-plugin/SKILL.md` —
  workflow + Important rules
- `.claude/skills/scaffold-state-plugin/references/thin-skill-architecture.md` —
  **READ FIRST** before authoring any SKILL.md body
- `.claude/skills/scaffold-state-plugin/references/puller-design-lessons.md` —
  patterns for the state's `pull_<state>_*.py` scripts

### 2. Adding a venue or subject-matter bundle to an existing state

A high-volume court can get its own skill within a state
plugin (`wa-pierce` for Pierce County Superior Court,
`oh-cuya` for Cuyahoga County Common Pleas). A new subject-
matter bundle adds a `<state>-<topic>/SKILL.md` (e.g.,
`wa-personal-injury`, `ca-family-law`).

Mirror the conventions in the state's existing skills:

- Directory + `name:` frontmatter must match
- Version starts at `0.1.0`
- Description must include realistic trigger phrases
- Body follows the **thin-skill architecture** — chapter
  pointers + procedural framework + composition pointers;
  no embedded current statutory specifics

Update the state's `plugin.json` description, the
marketplace `marketplace.json` description, `CLAUDE.md`'s
skills-index table for that state, and `README.md`'s
plugin description — all in the same PR.

### 3. Refreshing reference corpora

The quarterly `refresh-references.yml` workflow runs each
state's pullers automatically. Manual refresh from a
workstation is supported and sometimes necessary (e.g., NY
court rules require a Cloudflare-Warp proxy that GitHub
Actions runners can't reach).

Manual refresh commands are in `CLAUDE.md` under "Common
commands." Bump the affected `<state>-law-references`
SKILL.md `version:` (PATCH for routine refresh; MINOR if a
new corpus directory was added). Do not also bump
`plugin.json` for a routine corpus refresh.

### 4. Fixing a bug in a puller

The pullers live in `scripts/pull_<state>_*.py`. They share
a common shape: probe an upstream index, fetch each
target, render verbatim Markdown, write atomically. Common
patterns and known failure modes are in
`.claude/skills/scaffold-state-plugin/references/puller-design-lessons.md`
— that's the canonical guide for puller authorship and
debugging.

Don't ship empty stubs. The puller must distinguish:

- **Dispositioned-redirect** (chapter repealed; upstream
  serves a disposition table) — emit a `! WARNING`,
  increment a warnings counter, DO NOT write a stub
  file. The right next step is to prune the entry from
  `CHAPTERS` in the puller.
- **Parse-failure on a normal-shaped page** — emit a `!
  ERROR`, increment a fetch-error counter, DO NOT write a
  stub. This is a real regression; CI must fail.

A puller that silently writes a stub when zero sections
are extracted has shipped wrong content. We hit this three
times in WA before fixing it (RCW 26.10, 26.50, 49.78).
The fix lives in lesson 13 of `puller-design-lessons.md`.

### 5. Updating SKILL.md content

Two patterns to follow strictly:

- **Thin-skill architecture** — keep the law in references,
  not in skill bodies. SKILL.md bodies describe procedural
  frameworks + chapter pointers ("WPLA at RCW 7.72 — see
  `references/wa-rcw-debt/RCW-7_72.md` for current text").
  Current statutory text + dollar thresholds + day counts
  + section subsections + damages multipliers live ONLY
  in the references corpus. The quarterly puller refresh
  then updates canonical law without requiring SKILL.md
  edits.
- **No cross-state references inside a plugin body** — end
  users install one state at a time. Comparisons to other
  states ("unlike Oregon", "the same as Washington's...")
  are noise to the end user. Don't write them in plugin
  SKILL.md bodies, evals, plugin.json descriptions, or
  reference READMEs.

See the "Project conventions" section below for the full
detail on both rules.

Bump the affected skill's `SKILL.md` `version:` per the
semver rules below.

### 6. Documentation-only changes

Edits to `README.md`, `CLAUDE.md`, `CONTRIBUTING.md`,
plugin descriptions, reference-corpus READMEs are
welcome. No version bumps needed for typo / clarification
fixes; bump the relevant manifest only if the change is
material enough to surface to downstream installers.

## Project conventions

### Thin-skill architecture

**SKILL.md bodies and eval acceptance criteria describe
procedural frameworks + chapter pointers. Current
statutory text, dollar thresholds, day counts, exact
subsection numbers, damages multipliers, and other values
that drift live ONLY in the references corpus.**

This is the dominant lesson from the marketplace's
authorship. Every embedded statutory specific is a
maintenance debt that a future amendment silently breaks.
The quarterly puller refreshes the corpus without
requiring any SKILL.md edits — and that property is what
makes the marketplace scale.

What to keep in a skill body:

- Chapter-level pointers (`"WPLA at RCW 7.72"`)
- Qualitative framework descriptions (`"Washington is a
  pure-comparative-fault state"`)
- Decision trees + procedural workflows
- Stable historical reform attributions (`"1986 Reform
  Act"`, `"2019 SB 5600"`, `"2022 RCW 7.105
  consolidation"`)
- Composition pointers to other skills
- Stable case-law citations

What to REMOVE from a skill body:

- Specific dollar thresholds with year tags
  (`"$116,594.96 / 2024"`)
- Specific SOL day counts (`"6 years on written
  contract"`)
- Specific notice period day counts
- Specific employer-coverage / income thresholds
- Specific damages multipliers in body text
- Specific subsection-level cause-of-action cites
- Specific motion-day timing
- Specific MAR jurisdictional caps + revision-motion
  windows

**The same applies to eval acceptance criteria.** User-
stated hypothetical facts in eval prompts (`"I make
$80,000 a year"`) are OK — those are scenario context.
Embedded current law values in acceptance criteria
(`[ ] $80k is below the $116,594.96 threshold`) are not —
those go stale annually.

Full discussion + category-by-category citation-drift
hazard catalog: see
`.claude/skills/scaffold-state-plugin/references/thin-skill-architecture.md`.

### No cross-state references in plugin bodies

Plugins install **one state at a time**. End users will
not have WA + OR + CA + CO + IN + NY + OH installed
alongside the new state's plugin. Comparisons to other
states inside SKILL.md bodies, eval bodies, plugin.json
descriptions, or reference-corpus READMEs are noise to the
end user.

- Don't write "the same as Washington's GR 14"
- Don't write "unlike Oregon's no-interrogatories rule"
- Don't reference sibling-state SKILL.md files
- Don't import another state's terminology

State the rule directly without comparing. Internal
cross-references between skills in the **same** plugin
are fine (`<state>-discovery` referencing
`<state>-statewide-format`).

**Top-level docs are different**: `README.md`,
`CLAUDE.md`, and `CONTRIBUTING.md` are marketplace-level
and routinely compare states (the comparison table in
`README.md` is the canonical example). The no-cross-state-
references rule applies to **plugin content**, not to the
repo-wide docs.

### Versioning

Three independent version fields. Bump only what changed.

| File | Field | When to bump |
|---|---|---|
| `.claude-plugin/marketplace.json` | `metadata.version` | New plugin added; materially rewritten plugin listing |
| `plugins/<plugin>/.claude-plugin/plugin.json` | `version` | Anything in the plugin a downstream installer might care about — new skill, removed skill, changed triggers, new corpus, bumped keywords |
| `plugins/<plugin>/skills/<skill>/SKILL.md` | `version:` (frontmatter) | That **specific** skill's content, body, or triggers changed |

Semver mapping for this repo:

- **PATCH** (`0.1.0 → 0.1.1`) — typo, clarification, link
  repair, routine corpus refresh
- **MINOR** (`0.1.0 → 0.2.0`) — new section, new reference
  file, additional triggers, new procedural feature
- **MAJOR** (`0.x.y → 1.0.0`) — breaking change to a
  skill's contract or triggers, removed/renamed skill,
  relocated reference path

The repo is intentionally pre-1.0 across the board while
shape is settling.

### Linting

`scripts/lint-skills.py` checks every `SKILL.md` for:

- Valid YAML frontmatter
- `name:` present and matches the containing directory
- `description:` present
- `version:` present (semver format not validated, but the
  field must exist)

Run `python3 scripts/lint-skills.py` locally before every
commit. The pre-commit hook (installed via the symlink in
the Quick Start) re-runs it automatically. CI re-runs it
on every push and PR.

The linter does NOT semantically validate body content,
trigger phrases, or cross-references. That's on the
author.

## Reference-corpus discipline

The references corpus under each state plugin's
`<state>-law-references/references/` is the canonical
source of truth for statutory text + court-rule text +
case law + agency guidance.

- **Court rules** — pulled from each state's judicial
  branch by `scripts/pull_<state>_court_rules.py`
- **Statutes** — pulled from each state's legislature by
  `scripts/pull_<state>_statutes.py`
- **Federal law** — pulled once into the shared
  `claude-legal-federal-laws` plugin; each state plugin
  symlinks into it via `references/federal-debt-laws/`
  and `references/ucc-model/`

Direct edits to pulled content are reverted on the next
refresh. To change what's in the corpus:

1. Update the puller's target catalog (the `CHAPTERS`
   list, the `LAWS` list, or equivalent in the puller
   script)
2. Run the puller to regenerate the affected files
3. Commit the puller change AND the regenerated content
   together so the corpus stays reproducible

When the corpus has no free authoritative source for some
content (paywalled rules, PDF-only style manuals,
interactive-page-only local rules), ship a **pointer
stub** — a short Markdown file naming the canonical URL,
describing the scope, and explaining what's needed to
retrieve verbatim text. The puller's regression-protection
check (`_file_is_stub`) preserves verbatim content even
when the puller would otherwise overwrite with a stub. See
puller lesson 6.

## PR conventions

### Branch + commit

- Branch off `main`. Use a descriptive branch name (e.g.,
  `add-texas-plugin`, `expand-ca-civil-practice`,
  `fix-ny-rules-cf-bypass`).
- One concern per PR. A new state plugin can be one PR;
  multiple small concerns should be separate PRs.
- Commit messages are substantive — a one-line summary +
  detail body explaining the why. Pre-commit hook runs the
  linter.

### What goes in a PR

For any change that affects what's installed:

- Updated plugin.json + marketplace.json + CLAUDE.md +
  README.md in the **same PR** as the code/skill changes.
  These files describe the marketplace surface; out-of-
  sync metadata is a real bug.
- Bumped the affected `version:` fields per the semver
  rules above.
- Updated any affected evals so they continue to match the
  skill they test against.

### CI

- `lint-skills.yml` runs on every push and PR. Must pass.
- `refresh-references.yml` runs quarterly on cron + on
  manual dispatch. Not a PR gate, but if your PR changes a
  puller, you should manually trigger it on your branch to
  verify the puller works.

### Review

- PRs to `main` are reviewed for adherence to the
  conventions above. The lint passing is necessary, not
  sufficient.
- Cross-state references inside plugin bodies, embedded
  statutory specifics, and missing version bumps are the
  three most common review findings.

## Disclaimer

This project produces drafting aids. It does NOT produce
legal advice. Every generated document carries a "NOT
LEGAL ADVICE" disclaimer; every reference corpus describes
itself as a snapshot that must be verified against current
authority before reliance.

If you're contributing substantive legal content (statute
summaries, case-law commentary, fact-pattern triage),
remember:

- The marketplace serves pro se filers and practitioners
  who will rely on what we ship. Accuracy matters.
- Cite authoritative sources for substantive law claims.
- The "thin-skill" architecture exists in part because
  embedded statute claims drift; the quarterly puller
  refresh is the canonical accuracy mechanism.
- If you're unsure whether a claim is current, prefer
  framing it as "see the chapter file" rather than
  asserting a specific value.

## License

MIT. See [LICENSE](LICENSE).

By contributing, you agree your contributions will be
licensed under the same MIT terms.
