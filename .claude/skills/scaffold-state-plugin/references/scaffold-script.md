# Using `scaffold-state.py`

The scaffolder generates a complete 21-skill directory tree
with lint-clean SKILL.md stubs, a plugin.json, scripts copied
from `or-court-docs`, and eval-directory scaffolding. After
the script runs, the agent (or a human) authors substantive
content into each stub.

The script lives at:

```
.claude/skills/scaffold-state-plugin/scripts/scaffold-state.py
```

## Quick start

```bash
python3 .claude/skills/scaffold-state-plugin/scripts/scaffold-state.py \
  --state ca \
  --name California \
  --primary-court "lasc:Los Angeles Superior Court" \
  --secondary-court "sfsc:San Francisco Superior Court" \
  --format-rule "California Rules of Court 2.100-2.119" \
  --civil-rules CCP \
  --evidence CEC \
  --statute "Cal. Civ. Code" \
  --style-manual "California Style Manual"
```

Run from the repo root.

## Arguments

### Required

- `--state` — two-letter state abbreviation (lowercase),
  e.g., `ca`, `tx`, `fl`, `ny`. This determines the plugin
  name (`<abbr>-court-docs`) and the skill name prefix
  (`<abbr>-`).
- `--name` — full state name, used in skill bodies and
  descriptions. E.g., `California`, `Texas`.
- `--primary-court` — primary high-volume court in the
  format `<slug>:<display>`. The slug becomes the skill
  name component (`ca-lasc`); the display name is used in
  bodies. E.g., `lasc:Los Angeles Superior Court`.

### Optional

- `--secondary-court` — second high-volume court, same
  format. If omitted, defaults to a placeholder; you should
  always provide a real value for a real state.
- `--format-rule` — state's pleading-format rule. E.g.,
  `California Rules of Court 2.100-2.119`. Used in skill
  descriptions and bodies.
- `--civil-rules` — state's civil-rules code. E.g., `CCP`,
  `TRCP`, `Fla. R. Civ. P.`.
- `--evidence` — state's evidence-rules code. E.g., `CEC`,
  `Tex. R. Evid.`.
- `--statute` — state's statute-code prefix. E.g.,
  `Cal. Civ. Code`, `Tex. Bus. & Com. Code`.
- `--style-manual` — name of the state's citation style
  manual. E.g., `California Style Manual`.
- `--root` — repo root (default: current dir). Useful if
  you're running from a subdir.
- `--force` — overwrite an existing plugin directory.
  Without this, the script refuses to write if
  `plugins/<abbr>-court-docs/` already exists.
- `--dry-run` — print what would be created without
  writing.

## What the script generates

For state abbreviation `ca`, the script writes:

```
plugins/ca-court-docs/
├── .claude-plugin/plugin.json     (NEW; from template)
├── scripts/
│   ├── case-calendar.py           (COPIED from or-court-docs;
│   │                                prefixed with TODO marker)
│   └── format-check.py            (COPIED; prefixed with TODO)
├── skills/
│   ├── ca-statewide-format/
│   │   ├── SKILL.md               (NEW; stub)
│   │   └── references/templates/  (NEW; empty dir)
│   ├── ca-lasc/
│   │   ├── SKILL.md               (NEW; stub)
│   │   └── references/            (NEW; empty dir)
│   ├── ca-sfsc/...
│   ├── ca-county-courts/...
│   ├── ca-pro-se/...
│   ├── ca-law-references/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── court-rules/README.md          # real dir
│   │       ├── federal-debt-laws -> ../../../../claude-legal-federal-laws/references/federal-debt-laws  (symlink)
│   │       ├── ucc-model         -> ../../../../claude-legal-federal-laws/references/ucc-model          (symlink)
│   │       └── ca-statutes-debt/README.md     # real dir
│   ├── ca-discovery/...
│   ├── ca-hearings/...
│   ├── ca-post-judgment/...
│   ├── ca-first-30-days/SKILL.md  (no references)
│   ├── ca-fact-check/SKILL.md
│   ├── ca-deadlines/SKILL.md
│   ├── ca-draft-motion/SKILL.md
│   ├── ca-draft-declaration/SKILL.md
│   ├── ca-draft-note/SKILL.md
│   ├── ca-draft-order/SKILL.md
│   ├── ca-quality-check/SKILL.md
│   ├── ca-schedule-hearing/SKILL.md
│   ├── ca-file-packet/SKILL.md
│   ├── ca-submit-order/SKILL.md
│   └── ca-consumer-debt/
│       ├── SKILL.md
│       └── references/examples/   (NEW; empty dir)
└── evals/
    ├── README.md                  (NEW; stub)
    ├── drafting/
    ├── formatting/
    ├── procedural/
    ├── subject-matter/
    └── integration/
```

That's 21 SKILL.md files, 2 corpus READMEs (only the state-specific
corpora — `court-rules/` and `<state>-statutes-debt/` — get a real
directory with a README; `federal-debt-laws` and `ucc-model` are
created as symlinks into the shared `claude-legal-federal-laws`
plugin), 1 plugin.json declaring
`"dependencies": ["claude-legal-federal-laws"]`, 1 evals README,
2 copied scripts, and ~30 empty directories.

## What the script does NOT do

The script handles **mechanical scaffolding only**. After it
runs, the substantive work begins:

- ❌ Does not author substantive content in SKILL.md bodies
  (just stubs with TODO markers)
- ❌ Does not author the references/*.md files (just creates
  the directories)
- ❌ Does not adapt the scripts for state-specific holidays
  or named rules (prepends a TODO marker)
- ❌ Does not register the plugin in `marketplace.json`
  (prints a reminder to do so)
- ❌ Does not update `CLAUDE.md` or `README.md`
- ❌ Does not author evals (just creates directories)

The script's stubs are **lint-clean** — they pass
`scripts/lint-skills.py`. That's the bar for the
mechanical pass. Substance is the next phase.

## Verifying the scaffold

After running:

```bash
# Lint must pass
python3 scripts/lint-skills.py

# The new plugin's directory should be populated
ls plugins/<abbr>-court-docs/

# The 21 SKILL.md files should exist
find plugins/<abbr>-court-docs/skills -name SKILL.md | wc -l   # expects 21

# Scripts should be present and executable
python3 plugins/<abbr>-court-docs/scripts/format-check.py --help
```

## Idempotency

The script is NOT idempotent without `--force`. Running it
twice with the same `--state` fails the second time. If you
want to regenerate, either:

- Delete the existing plugin dir first
- Pass `--force` to overwrite (DESTRUCTIVE — wipes any
  substantive content you've authored)

Generally: run the scaffolder once at the start, then make
all subsequent changes manually so you don't lose substance.

## Worked examples

### California

```bash
python3 .claude/skills/scaffold-state-plugin/scripts/scaffold-state.py \
  --state ca \
  --name California \
  --primary-court "lasc:Los Angeles Superior Court" \
  --secondary-court "sfsc:San Francisco Superior Court" \
  --format-rule "California Rules of Court 2.100-2.119" \
  --civil-rules CCP \
  --evidence CEC \
  --statute "Cal. Civ. Code" \
  --style-manual "California Style Manual"
```

### Texas

```bash
python3 .claude/skills/scaffold-state-plugin/scripts/scaffold-state.py \
  --state tx \
  --name Texas \
  --primary-court "hcdc:Harris County District Court" \
  --secondary-court "dcdc:Dallas County District Court" \
  --format-rule "TRCP 21a" \
  --civil-rules TRCP \
  --evidence "Tex. R. Evid." \
  --statute "Tex. Bus. & Com. Code" \
  --style-manual "Texas Rules of Form"
```

### New York

```bash
python3 .claude/skills/scaffold-state-plugin/scripts/scaffold-state.py \
  --state ny \
  --name "New York" \
  --primary-court "supny:NY Supreme Court — NY County" \
  --secondary-court "supkings:NY Supreme Court — Kings County" \
  --format-rule "CPLR 2101" \
  --civil-rules CPLR \
  --evidence "CPLR Article 45" \
  --statute "NY GBL" \
  --style-manual "New York Reporter Style"
```

### Florida

```bash
python3 .claude/skills/scaffold-state-plugin/scripts/scaffold-state.py \
  --state fl \
  --name Florida \
  --primary-court "mdcc:Miami-Dade Circuit Court" \
  --secondary-court "bcc:Broward Circuit Court" \
  --format-rule "Fla. R. Gen. Prac. Jud. Admin. 2.520" \
  --civil-rules "Fla. R. Civ. P." \
  --evidence "Fla. Stat. § 90" \
  --statute "Fla. Stat." \
  --style-manual "Florida Style Manual"
```

## Troubleshooting

### "Root doesn't look like the claude-legal repo"

The script requires `scripts/lint-skills.py` to exist at the
specified root. Run from the marketplace root, or pass
`--root /path/to/claude-legal`.

### "Plugin already exists"

The plugin directory exists. Either:

- Delete it (`rm -rf plugins/<abbr>-court-docs/`) and re-run
- Pass `--force` (destructive)
- Choose a different `--state` abbreviation

### Lint fails after running

Either:

- A SKILL.md template substitution went wrong (file a bug)
- An existing WA/OR plugin already fails lint (fix the pre-
  existing issue first)

### Scripts don't work after copying

The copied `format-check.py` and `case-calendar.py` have a
TODO marker prepended. The Python syntax should still parse,
but the substantive state-specific content needs to be
adapted by hand:

- `format-check.py`: update the rule reference in the report
  header; adjust acceptable-fonts list and color-handling per
  state convention
- `case-calendar.py`: update `FIXED_HOLIDAYS`, `WEEK_HOLIDAYS`,
  and `RULES` dict for the state

## After the scaffold

Once the script runs successfully:

1. Open `references/checklist.md` and start working through
   Phase 3 (SKILL.md content) and Phase 4 (reference content)
2. Use `references/state-research-protocol.md` to gather
   state-specific law
3. Use `references/cross-state-quirks.md` to identify and
   flag procedural quirks in the new state
4. Reference the WA and OR plugins as concrete examples — but
   do NOT search-and-replace; research the state's actual law

The scaffold gets you to lint-clean; substance gets you to
useful.
