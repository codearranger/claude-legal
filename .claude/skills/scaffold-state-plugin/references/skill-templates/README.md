# Skill Templates — Canonical Starting Points

Each `*-template.md` here is a starting point for one of the
21 skill roles. Templates include:

- Frontmatter with placeholders for state-specific values
- Body structure (sections, headings, conventions)
- Cross-reference pointers
- TODO markers where research is needed

When `scaffold-state.py` runs, it generates a minimal stub
for every skill. **These templates are richer than the
stubs** — use them when authoring substantive content by hand
(or when prompting the agent to flesh out a stub).

## Templates included

Templates exist for the highest-variance roles (where every
state requires substantial research and adaptation):

- `statewide-format-template.md` — state pleading-format rule
- `law-references-template.md` — civil rules, evidence, citation,
  fees, local rules, key cases
- `pro-se-template.md` — pro-se drafting framework + state pro se
  conventions
- `discovery-template.md` — discovery framework (note the OR
  no-interrogatories quirk pattern)
- `consumer-debt-template.md` — the subject-matter bundle

## Templates not included (use WA/OR as the example)

For roles where the structure is largely state-agnostic and the
WA/OR equivalents are nearly drop-in (with minimal state-
specific adaptation), use those plugins directly as your
template:

- `*-fact-check` — substantively mirrors WA/OR; adjust citation-
  pattern lists for the state's style manual
- `*-deadlines` — adjust holiday list and named-rules dict;
  body is mostly the same shape
- `*-draft-motion`, `*-draft-declaration`, `*-draft-note`,
  `*-draft-order` — adjust rule citations and terminology
- `*-quality-check` — adjust rule references; body is similar
- `*-file-packet`, `*-submit-order`, `*-schedule-hearing` —
  adjust to state procedure
- `*-hearings` — adjust remote-hearing platform (Zoom / WebEx /
  state-specific); body is similar
- `*-post-judgment` — adjust state vacation rule (state's
  FRCP 60 analog), garnishment chapter, exemption catalog
- `*-first-30-days` — adjust answer-deadline rule and state's
  ORCP 21 / CR 12 analog
- `*-county-courts` — adjust the county directory
- `*-<primary-court>`, `*-<secondary-court>` — research the
  court's local rules

Refer to:
- `plugins/wa-court-docs/skills/wa-<role>/SKILL.md`
- `plugins/or-court-docs/skills/or-<role>/SKILL.md`

These are concrete, complete examples that have been
substantively reviewed for the WA / OR legal context.

## How to use a template

1. **Copy** the template to the new plugin's skill directory:
   `cp .claude/skills/scaffold-state-plugin/references/skill-templates/<role>-template.md plugins/<abbr>-court-docs/skills/<abbr>-<role>/SKILL.md`
2. **Substitute** the placeholders ({{STATE_NAME}}, {{ABBR}},
   etc.) for the new state's values
3. **Research and fill in** every TODO marker with the
   state-specific content (rule numbers, statute citations,
   case names in the state's style)
4. **Add references** in `references/` for each cited topic
5. **Lint** — `python3 scripts/lint-skills.py`

## Placeholders used in templates

| Placeholder | Substitution |
|-------------|--------------|
| `{{STATE_NAME}}` | Full state name (e.g., "California") |
| `{{ABBR}}` | Two-letter state abbreviation (e.g., "ca") |
| `{{FORMAT_RULE}}` | State's pleading-format rule (e.g., "CRC 2.100-2.119") |
| `{{CIVIL_RULES}}` | State's civil-rules code (e.g., "CCP") |
| `{{EVIDENCE_RULES}}` | State's evidence-rules code (e.g., "CEC") |
| `{{STATUTE_CODE}}` | State's statute prefix (e.g., "Cal. Civ. Code") |
| `{{STYLE_MANUAL}}` | State's citation style manual (e.g., "California Style Manual") |
| `{{PRIMARY_COURT_SLUG}}` | Slug for primary court (e.g., "lasc") |
| `{{PRIMARY_COURT_NAME}}` | Display name (e.g., "Los Angeles Superior Court") |
| `{{SECONDARY_COURT_SLUG}}` | Slug for secondary court |
| `{{SECONDARY_COURT_NAME}}` | Display name |
| `{{STATE_CONSUMER_STATUTE}}` | State's UTPA-analog (e.g., "California Rosenthal Act") |
| `{{COLLECTION_REGIME}}` | State's collection-agency law (e.g., "Cal. Fin. Code § 100001 et seq. (CDCLA)") |
| `{{CONTRACT_SOL}}` | State's contract SOL in years (e.g., "4") |

## Verification after substitution

After substituting placeholders, search the file for `{{` —
unsubstituted placeholders are a common bug.

```bash
grep -n '{{' plugins/<abbr>-court-docs/skills/<abbr>-<role>/SKILL.md
```

Should return no matches.

## When the template is wrong for a state

Some states have idiosyncrasies the templates don't anticipate:

- **Oregon**: no written interrogatories under ORCP — flagged
  prominently in `or-discovery`. Adapt `discovery-template.md`
  if your new state has a similar quirk.
- **California**: "in pro per" vs. "pro se" — adapt
  `pro-se-template.md` accordingly.
- **New York**: verified vs. unverified pleadings — note in
  `first-30-days` and `draft-motion`.

Document any new state-specific quirks in
`../cross-state-quirks.md` so the next state plugin benefits.
