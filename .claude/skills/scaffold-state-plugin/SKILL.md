---
name: scaffold-state-plugin
description: >
  Use this skill when the user asks the coding agent to add a new
  state plugin to the claude-legal marketplace. Triggers include
  "add California plugin", "create a Texas court-docs plugin",
  "scaffold a new state", "add Florida", "I want to cover Arizona",
  "build the New York plugin", "new state — same as Oregon but for
  [STATE]", "port the WA plugin to [STATE]". Generates the
  complete 21-skill directory tree (mirroring wa-court-docs and
  or-court-docs), authors SKILL.md files for every role, lays
  down the reference-corpus scaffolding (court-rules,
  federal-debt-laws, ucc-model, <state>-statutes-debt), copies
  the format-check and case-calendar scripts parameterized to
  the new state's holidays and format rule, registers the plugin
  in marketplace.json, and updates CLAUDE.md and README.md. The
  scaffolder declares "dependencies: [claude-legal-federal-laws]"
  in the new plugin.json and lays down symlinks at references/
  federal-debt-laws and references/ucc-model pointing into the
  shared plugin — federal corpora are NOT duplicated per state.
  This is a **project-scoped skill** — it lives in .claude/
  skills/ and runs against the marketplace repo as a whole. It
  is NOT a marketplace plugin.
version: 0.4.0
---

# Scaffold a New State Plugin

Use this skill when adding a new state plugin to the
`claude-legal` marketplace. The skill codifies the pattern
established by `wa-court-docs` and `or-court-docs` so the
addition stays consistent across states.

> **Project-scoped skill**. This skill lives in `.claude/skills/`
> at the repo root. It runs against the marketplace as a whole.
> It is NOT one of the marketplace's state plugins.

## When to invoke

When the user asks to "add [state]", "create a plugin for
[state]", "scaffold [state]", etc. Confirm with the user:

1. **State name and abbreviation** (e.g., "California" / "ca")
2. **Primary high-volume court** to get its own skill (e.g.,
   "Los Angeles Superior Court" / `ca-lasc`)
3. **Secondary high-volume court** (optional; e.g., "San
   Francisco Superior Court" / `ca-sfsc`)
4. **Roll-up counties** for the long tail (typically the 10
   most-populous, excluding the two flagship counties)
5. **State's pleading-format rule** (e.g., California Rules of
   Court Rule 2.100 et seq.)
6. **State's civil rules** (e.g., California Code of Civil
   Procedure — CCP)
7. **State's evidence rules** (e.g., California Evidence Code
   — CEC, codified at Cal. Evid. Code §§ 1–1605)
8. **State's statute code** (e.g., Cal. Civ. Code, Tex. Bus.
   & Com. Code)
9. **State's style manual** (e.g., California Style Manual)
10. **State legal holidays** (federal + state-specific; for
    the case-calendar script)
11. **State's analog to FDCPA** at the state level (e.g.,
    California Rosenthal Act; Texas Finance Code Ch. 392)
12. **State's collection-agency registration regime** if any
    (e.g., California Debt Collection Licensing Act for debt
    buyers as of 2022)
13. **Family-court topology** — does the state have a
    separate Family Court trial court, or does it hear
    family matters in a Family Division of the general-
    jurisdiction trial court? Either way, the
    `<abbr>-family-court` venue skill ships. Note the venue,
    the rule set, and whether jurisdiction is concurrent
    with the regular civil-trial court for any topic.
14. **State's family-law code** — identify the citation
    (e.g., the state's Domestic Relations Law / Family Code
    / UDMA enactment / equivalent)
15. **State's child-support guideline model** — income-
    shares (most states), percentage-of-payor-income, or
    Melson formula (rare). Note the statutory cap on
    combined parental income.
16. **State's property-distribution regime** — community-
    property (CA, TX, WA, AZ, NM, ID, LA, NV, WI) vs.
    equitable-distribution (everyone else).
17. **State's divorce grounds** — no-fault is now universal
    but waiting periods and any surviving fault grounds vary.

If the user hasn't supplied all of these, ASK before scaffolding
— the substance of every skill depends on getting these right.

## The pattern to mirror

The **23-skill base** is the minimum a new state plugin
should ship. Baseline coverage includes:

- **All civil court rules** for every civil-trial-court
  layer in the state (the state's pleading-format rule, its
  civil-procedure rule set, and the local rules of the
  flagship counties)
- **All civil practice** procedural skills (the 21-skill
  core: format, discovery, hearings, post-judgment, etc.)
- **All civil substantive laws** in the statutes corpus
  (the state's procedure code + consolidated-laws articles
  covering evidence, fees, limitations, exemptions,
  garnishment, UCC Article 9, consumer-debt statutes)
- **Family court rules** for the state's family-court venue
- **Family practice** — the `<abbr>-family-court` venue
  skill + the `<abbr>-family-law` subject bundle
- **Family law statutes** (the state's family-law code in
  the statutes corpus)

States with complex civil-court systems can ship more than
the 23-skill base — dedicated venue skills for separate
lower-civil-court layers (housing court, district court,
city court, justice court, etc.) and additional subject-
matter bundles (personal injury, employment, commercial
disputes, etc.) when the state's civil practice justifies
them. Existing plugins in the marketplace ship between 21
and 35 skills depending on state complexity.

The 23-skill base, parameterized by the items above:

```
plugins/<abbr>-court-docs/
  .claude-plugin/plugin.json
  scripts/
    format-check.py            # state format-rule compliance
    case-calendar.py           # state-specific deadline arithmetic
  skills/
    <abbr>-statewide-format/   # format rule (e.g., CRC 2.100)
    <abbr>-<court1>/           # primary high-volume court
    <abbr>-<court2>/           # secondary high-volume court
    <abbr>-county-courts/      # rest-of-state roll-up
    <abbr>-pro-se/             # pro-se drafting framework adaptation
    <abbr>-law-references/     # civil rules, evidence, citation,
                               #   fees, local rules, online sources,
                               #   legal-data-apis, key cases
    <abbr>-discovery/
    <abbr>-hearings/
    <abbr>-post-judgment/
    <abbr>-first-30-days/
    <abbr>-fact-check/
    <abbr>-deadlines/
    <abbr>-draft-motion/
    <abbr>-draft-declaration/
    <abbr>-draft-note/         # or "draft-notice-of-hearing"
                               #   depending on terminology
    <abbr>-draft-order/
    <abbr>-quality-check/
    <abbr>-schedule-hearing/
    <abbr>-file-packet/
    <abbr>-submit-order/
    <abbr>-family-court/       # Family Court venue skill —
                               #   custody / support / family
                               #   offense / paternity / abuse
                               #   and neglect. Even when the
                               #   state hears family matters
                               #   inside a Family Division of
                               #   Superior Court (rather than
                               #   a separate Family Court),
                               #   ship this as a dedicated skill
                               #   covering the division's rules,
                               #   intake, and pro-se forms.
    <abbr>-consumer-debt/      # Subject bundle: FDCPA + state
                               #   UTPA-equivalent + collection-
                               #   agency law + chain of title
    <abbr>-family-law/         # Subject bundle: divorce /
                               #   custody / support / parenting
                               #   plan / property distribution
                               #   / maintenance. Substantive
                               #   law of the state's family
                               #   code (UDMA-based, community-
                               #   property, equitable-
                               #   distribution — depends on
                               #   state).
  evals/
    drafting/
    formatting/
    procedural/
    subject-matter/
    integration/
    README.md
```

## Workflow

### Step 1: Gather inputs

Use `AskUserQuestion` to collect the 12 items above (in
batches of 4 to avoid overwhelming). Record them. The agent
can suggest defaults based on the state — but the user
confirms.

### Step 2: Generate the scaffold

Two options:

#### Option A — Use the scaffold script

Run the bundled scaffolder:

```bash
python3 .claude/skills/scaffold-state-plugin/scripts/scaffold-state.py \
  --state <abbr> \
  --name <full-name> \
  --format-rule "<rule-code>" \
  --civil-rules "<code>" \
  --evidence "<code>" \
  --statute "<code>" \
  --primary-court "<slug>:<display-name>" \
  --secondary-court "<slug>:<display-name>" \
  --counties "<list>" \
  --citation-style-url "<url>"
```

The script:

- Creates `plugins/<abbr>-court-docs/` and all 21 skill dirs
- Generates a `plugin.json` from the provided metadata
- Copies the OR `format-check.py` and `case-calendar.py` to
  the new plugin, parameterizing the format rule and the
  holidays
- Writes stub `SKILL.md` files for each of the 21 skills with
  frontmatter (`name`, `description`, `version: 0.1.0`) and
  a TODO list of sections to author
- Generates reference-corpus skeletons (READMEs and
  `_manifest.json` for court-rules and `<state>-statutes-debt`)
- Updates `.claude-plugin/marketplace.json` to register the
  new plugin
- Stops short of authoring substantive content — that's the
  next step

#### Option B — Manual scaffolding

For maximum control, follow `references/checklist.md` step by
step. Use `references/skill-templates/` as starting points for
each role.

### Step 3: Author substantive content

The scaffolder produces stubs. Each SKILL.md needs:

- A full description with trigger phrases that match how a
  pro se filer would actually ask
- Substantive body text covering the state's rules — **as
  a thin-skill** (see below)
- References specific to the state (rule numbers, statute
  citations, case citations in the state's style manual
  format)
- Composition notes pointing to other skills in the plugin

> **Read [`references/thin-skill-architecture.md`](references/thin-skill-architecture.md)
> before authoring SKILL.md bodies.** The dominant lesson
> from the WA expansion is that skills should describe
> procedural frameworks + chapter pointers, and current
> statutory text + dollar thresholds + day counts + section
> subsections should live in the references corpus — not
> embedded in skill bodies. Quarterly puller refreshes then
> update canonical law without requiring SKILL.md edits.
> The thin-skill doc has a category-by-category catalog of
> citation-drift hazards and a refactor playbook.

Use `references/skill-templates/` as the starting point for
each role. Each template has:

- The frontmatter shape (name, description triggers, version)
- The body structure (sections, headings, conventions)
- Placeholders for state-specific content (`{{STATE_NAME}}`,
  `{{FORMAT_RULE}}`, etc.)
- Cross-references to the relevant references files

### Step 4: Build reference content

For each skill, the `references/` directory holds the deep
dive. Each `<state>-law-references` skill needs:

- `civil-rules.md` — state's civil-procedure rules
  summarized (must cover both general-civil rules AND
  family-court rules)
- `evidence-rules.md` — state's evidence code summarized
- `fees-and-costs.md` — state's fee-shifting framework
- `local-rules.md` — high-volume courts' local rules
- `citation-format.md` — state style-manual conventions
- `key-cases.md` — general-civil + family-law precedents
- `online-sources.md` — canonical URLs (the WebFetch catalog)
- `legal-data-apis.md` — programmatic-access index
- `court-rules/` — **verbatim rule text for both civil and
  family court rules**. Baseline coverage:
  - State pleading-format rule
  - State civil-procedure rule set
  - State evidence code (where codified as a rule rather
    than a statute)
  - **State family-court rule set** — verify this exists as
    a distinct rule body; check for it even when family law
    sits in a Family Division of the general-jurisdiction
    court
  - Sealing of court records rule (statewide)
  - Costs and sanctions rule (statewide)
  - Rules of Professional Conduct
  - Sub-trial-court rule sets where applicable (state-
    specific lower civil courts, district courts, city
    courts, justice / town / village courts, special civil
    parts, etc.)
- `federal-debt-laws/` *(symlink)* — points into the shared
  `claude-legal-federal-laws/references/federal-debt-laws/`
  plugin via `../../../../claude-legal-federal-laws/...`. Do
  NOT create a real directory here. The scaffold script lays
  this symlink down automatically; if you author the plugin by
  hand, declare `"dependencies": ["claude-legal-federal-laws"]`
  in plugin.json and run `ln -s` for the symlink.
- `ucc-model/` *(symlink)* — same shared plugin; same symlink
  target convention. Same dependency.
- `<state>-statutes-debt/` — **state's civil-practice +
  consumer-debt + family-law statute chapters**. The
  directory name retains the legacy `debt` slug for path
  stability across earlier plugins, but the scope is full
  civil + family practice. Baseline coverage:
  - **Civil procedure** — state's procedure code
  - **Evidence** — state's evidence code where statutory
  - **Limitations** — state's SOL chapter
  - **Garnishment + exemptions** — state's enforcement +
    exemption chapter
  - **UCC** — state's enactment of Articles 2, 3, 9
  - **Consumer protection** — state's UTPA analog
  - **Debt collection** — state's mini-FDCPA
  - **Real Property + summary proceedings** — for L&T cases
  - **Family law** — state's family-law code
  - **Family Court / domestic-relations procedure** — where
    the state codifies it separately from the family-law
    substantive code
  - **General Construction / holidays** — for the case-
    calendar script

### Step 5: Build the two baseline subject-matter bundles

The plugin ships with **two baseline subject-matter bundles**:
`<state>-consumer-debt` and `<state>-family-law`. Both
follow the OR + CO precedent for bundle structure.

#### 5.A — `<state>-consumer-debt`

The substantive centerpiece for consumer-debt defense. Mirror
the OR pattern:

- `SKILL.md` — overview with 5 fact-pattern triage
- `references/fdcpa.md` — state-specific framing / cites to the
  FDCPA verbatim text. The verbatim text itself lives in
  `<state>-law-references/references/federal-debt-laws/FDCPA.md`
  (symlinked into the shared plugin), so cross-reference it
  with a relative path rather than duplicating content.
- `references/reg-f.md` — same: state-specific framing; verbatim
  Reg F text lives in the shared plugin via the symlink.
- `references/<state>-utpa-or-equiv.md` — state UTPA analog
  (Rosenthal Act for CA; Tex. Bus. & Com. Code Ch. 17 for TX;
  etc.)
- `references/<state>-collection-agency-law.md` — state
  registration / licensing regime if any
- `references/chain-of-title.md` — chain-of-title doctrine
  (largely state-agnostic; adapt for state-specific
  authentication law)
- `references/evidence-debt-buyer.md` — state evidence-rule
  analog of OEC 803(6) / 902(11) foundation
- `references/<state>-statutes-of-limitations.md` — state SOLs
  for debt and consumer claims (e.g., CA: 4 years on written
  contract under CCP § 337; TX: 4 years on debt)
- `references/key-cases.md` — state and federal precedents
- `references/recent-decisions.md` — recent appellate
  decisions to track
- `references/fees-consumer-debt.md` — fee mechanics
- `references/rfp-debt-buyer.md` — RFP bank targeting chain
  of title
- `references/rfa-debt-buyer.md` — RFA bank
- `references/interrogatories-debt-buyer.md` — if the state
  has interrogatories (Oregon doesn't!); otherwise mirror the
  OR notes
- `references/meet-and-confer-debt-buyer.md` — state-flavored
  meet-and-confer templates
- `references/online-sources-consumer-debt.md` — state-
  specific URLs
- `references/ucc-article-9.md` — state UCC Article 9
  enactment
- `references/examples/` — 6 synthetic example filings
  (answer, declaration, motion to compel, M&C, proposed
  order, certificate of service)

#### 5.B — `<state>-family-law`

The substantive bundle for divorce / annulment / legal
separation / custody / child support / maintenance. Use
the `family-law-template.md` skill template as the starting
shape:

- `SKILL.md` — overview with state-specific family-law
  framework. Cover: divorce grounds + waiting period;
  property distribution regime (community vs. equitable);
  child-support guideline model + statutory cap; custody
  / parenting-time framework + best-interests standard;
  maintenance / spousal support; modification thresholds;
  common-law marriage status; UCCJEA + UIFSA jurisdictional
  framework.
- `references/dissolution.md` — divorce mechanics; petition
  + response + service; mandatory financial disclosures;
  waiting period; default vs. contested
- `references/annulment.md` — declaration-of-invalidity
  grounds (varies materially by state — fraud, duress,
  bigamy, age, incapacity, prohibited relationship)
- `references/legal-separation.md` — where available
- `references/property-distribution.md` — community-property
  presumptions or equitable-distribution factors; valuation
  of marital business interests; commingling doctrines
- `references/child-support.md` — guideline calculation;
  income imputation rules; deviation grounds; cap on
  combined-income; modification threshold (percentage
  change required to trigger review; state-specific)
- `references/parenting-plan.md` — decision-making
  allocation; parenting time (overnights); relocation
  notice + standard for permission
- `references/maintenance.md` — duration formulas; income-
  based formulas where applicable; modification +
  termination triggers
- `references/family-offense.md` — Order of Protection
  framework; qualifying-relationship + qualifying-offense
  catalog; duration; firearm-surrender mechanics
- `references/uccjea.md` — Uniform Child Custody
  Jurisdiction and Enforcement Act implementation in state;
  home-state jurisdiction analysis
- `references/uifsa.md` — Uniform Interstate Family Support
  Act implementation in state
- `references/common-law-marriage.md` — for the handful of
  states that still recognize it (note the test the state
  applies; otherwise note that the state honors marriages
  valid where contracted)
- `references/forms.md` — state-specific divorce / custody /
  child-support forms (the state's pro-se form catalog)
- `references/examples/` — 4-6 synthetic example filings:
  petition for dissolution, sworn financial statement,
  parenting-plan / custody motion, child-support
  modification motion

### Step 6: Scripts

The `format-check.py` and `case-calendar.py` scripts are
parameterized variants of the WA/OR versions:

- `format-check.py` checks paper size (Letter or Legal),
  margins, fonts, color, line spacing, and footer pagination
  — adjust the substantive rule reference in the report
  output (e.g., "CRC 2.100 Format Check:" instead of "UTCR
  2.010 Format Check:")
- `case-calendar.py` encodes the state's legal-holiday list
  (state-specific holidays beyond federal) and the state's
  rules of time computation (FRCP 6 / state analog) and the
  state's named rules (answer-due, RFP-response,
  SOL-by-claim-type, etc.)

### Step 7: Evals

Mirror the OR eval categories:

- `drafting/` — 4 evals (motion, declaration, notice/note,
  proposed order)
- `formatting/` — 4 evals (statewide-format, primary court
  local rules, pro se, quality-check)
- `procedural/` — 8 evals (law-references civil, law-
  references evidence, deadlines, discovery M&C, discovery
  no-interrog (if applicable), fact-check, first-30-days,
  hearings, file-packet)
- `subject-matter/` — 6 evals on the consumer-debt bundle
  (fact-pattern triage, SOL, UTPA-equivalent, chain of
  title, collection-agency-law capacity, fees recovery)
- `integration/` — 2 evals (end-to-end debt-defense answer;
  end-to-end motion-to-compel packet)

> **Apply the thin-skill principle to eval acceptance
> criteria too** — see `references/thin-skill-architecture.md`.
> User-stated hypothetical facts in eval prompts ("I make
> $80,000 a year") are OK; embedded current law values in
> acceptance criteria (`[ ] $80k is below the $116,594.96
> threshold`) are not. Rewrite criteria to require the agent
> to **read current values from the references corpus**
> rather than hard-coding figures that drift annually.

### Step 8: Update marketplace docs

- `marketplace.json`: register the new plugin; bump
  `metadata.version`
- `CLAUDE.md`: add the new skills index table; add the
  state's reference-corpora section; update the "Common
  commands" with the new plugin's scripts
- `README.md`: add the new plugin's description; update the
  install command; update the WA-vs-OR-vs-new-state
  comparison table

### Step 9: Lint and commit

Run `python3 scripts/lint-skills.py` — must pass on every
new SKILL.md. Commit with a substantive message describing
what shipped. Push to the user's designated branch.

## Important rules

### CRITICAL: Thin-skill architecture — keep the law in references

**SKILL.md bodies and eval acceptance criteria describe
procedural frameworks + chapter pointers. Current
statutory text, dollar thresholds, day counts, exact
subsection numbers, damages multipliers, and other values
that drift live ONLY in the references corpus.**

This is the dominant lesson from the WA expansion: every
embedded statutory specific is a maintenance debt that a
future amendment silently breaks. The quarterly puller
refreshes the corpus without requiring any SKILL.md edits
— and that property is what makes the marketplace scale.

**What to keep in a skill body**: chapter-level pointers
("WPLA at RCW 7.72 — see `references/wa-rcw-debt/
RCW-7_72.md` for current text"); qualitative framework
descriptions ("Washington is a pure-comparative-fault
state"); decision trees + procedural workflows; stable
historical reform attributions (1986 Reform Act, 2019 SB
5600, etc.); composition pointers to other skills; stable
case-law citations.

**What to REMOVE from a skill body**: specific dollar
thresholds with year tags ("$116,594.96 / 2024"); specific
SOL day counts ("6 years on written contract"); specific
notice period day counts ("14-day pay-or-vacate"); specific
employer-coverage / income thresholds ("8+ employees");
specific damages multipliers in body text; specific
subsection-level cites of cause-of-action elements
("RCW 7.72.060(3) provides..."); specific motion-day
timing ("9 court days before hearing"); specific hearing-
window day counts; MAR jurisdictional caps; revision-motion
windows.

**The same applies to eval acceptance criteria**. User-
stated hypothetical facts in eval prompts ("I make $80,000
a year") are OK — those are scenario context. Embedded
current law values in acceptance criteria
(`[ ] $80k is below the $116,594.96 threshold`) are not —
those will be stale next year.

See [`references/thin-skill-architecture.md`](references/thin-skill-architecture.md)
for: the full principle, what to keep vs. remove, a refactor
playbook for existing thick skills, a category-by-category
citation-drift hazard catalog, and the cross-state-port
benefit.

### CRITICAL: No cross-state references inside the plugin

Plugins install **one state at a time**. End users will not
have WA + OR + CA + CO + IN installed alongside the new
state's plugin. Comparisons to other states inside SKILL.md
bodies, eval bodies, plugin.json descriptions, or reference
READMEs are pure noise to the end user and **must be
removed before the plugin ships**.

What this means in practice when authoring the new plugin:

- **Don't frame state-specific quirks comparatively.** Write
  the rule directly. ❌ "Unlike State-X's no-interrogatories
  rule, this state allows 25 interrogatories." ✓ "This
  state allows 25 interrogatories under [cite]."
- **Don't reference sibling-state SKILL.md files.** The new
  plugin's `README.md`, `evals/README.md`, and reference-
  corpus READMEs must not say "see `xx-court-docs/evals/`"
  or "mirrors `yy-court-docs/skills/yy-law-references/...`".
  The end user will not have those plugins installed.
- **Don't import another state's terminology.** Each state
  has its own pleading and motion vocabulary; don't carry
  over labels from a state whose practice you happen to
  know.
- **Don't use "the same as State-X's [rule]" framing.** Cite
  the state's own rule directly.

**Internal cross-references between skills in the SAME plugin
are fine** and encouraged — e.g., `<abbr>-discovery`
referencing `<abbr>-statewide-format` is exactly what the
marketplace runtime expects.

**Final scaffold step**: run a cross-state-reference grep
before committing. Anything that turns up needs either
deletion or rewording into a state-only statement:

```bash
# In the new plugin's directory:
grep -rnE "\b(Washington|Oregon|California|Colorado|Indiana|New York)\b\
|wa-court-docs|or-court-docs|ca-court-docs|co-court-docs|in-court-docs|ny-court-docs\
|like (Oregon|California|Colorado|Indiana|Washington|New York)\
|unlike (Oregon|California|Colorado|Indiana|Washington|New York)\
|federal/(WA|OR|CA|CO|IN|NY)" plugins/<abbr>-court-docs/ \
  --include="*.md" --include="*.json"
```

**False-positive watch:** the scan will hit:

- **"Washington's Birthday"** as the legal name of the
  federal holiday — that's the actual statute language in
  most states' General Construction or Government Codes,
  **not** a cross-state comparison. Keep it.
- **`in-person`** as a hyphenated phrase — matches the
  `\bin-` pattern when looking for `in-court-docs`
  references. Keep it.
- **`co-parents`, `co-counsel`, `co-defendant`** — match
  the `\bco-` pattern. Keep them.
- **Verbatim statutory text from the state's own
  consolidated laws** — many states' General Construction
  laws name federal holidays after the figures they honor;
  that's literal statute, not a cross-state reference.

Distinguish state-as-comparison from state-as-statute-author
before deleting.

### Verify URL slugs, locationIds, and Part numbers against the live source

**Don't rely on memory or example data for state-specific
identifiers.** Past authorship has produced silent puller
failures from each of these patterns:

- **Adjacent rule-Part numbers get conflated** — it is easy
  to label a Part with the wrong subject matter when several
  Parts in the same numbering range cover related but
  distinct courts. Always verify each Part's title against
  the live index.
- **Title vs. Article numbering confusion** — some state
  consolidated laws use Title numbers (T5, T17); others use
  Article numbers (A5, A17). Don't infer the format from a
  secondary source — probe the API or HTML for the canonical
  identifier shape.
- **Hyphenated vs. unhyphenated sub-articles** — sub-
  articles like `A22-A` vs. `A22A` (or any equivalent
  hyphenation choice) often only resolve in one form. Probe
  the actual identifier the API accepts.
- **Topic-to-law assignment is not always intuitive** — a
  topic that seems like it should be in one statute (e.g.,
  child support in a state's Domestic Relations Law) may
  actually live in a different code (e.g., Family Court
  Act). Verify which law owns each topic.
- **CMS migrations change URL patterns** — court-rules
  publishing sites migrate frequently. Legacy URLs may
  redirect to an index page rather than the actual rule
  content. Discover the actual URL slug at fetch time
  rather than assuming the pattern that worked yesterday.

The right pattern: probe the live API or HTML index for the
state's source-of-truth identifiers before populating the
puller's target catalog. See
[`references/puller-design-lessons.md`](references/puller-design-lessons.md)
for the full discipline.

### Do NOT search-and-replace WA or OR

A state plugin is more than a search-and-replace from
Washington or Oregon. The substantive rules differ:

- **SOL on contract debt** varies by state (4 years in
  CA/TX/FL; 6 years in OR/WA; 3 years in NY for credit card)
- **Format rule** is different in every state (GR 14 in WA,
  UTCR 2.010 in OR, CRC 2.100 in CA, TRCP 21a in TX)
- **Civil rules code** is different (CR/CRLJ in WA, ORCP in
  OR, CCP in CA, TRCP in TX)
- **Evidence rules** are different (ER court rule in WA, OEC
  statutory in OR, CEC statutory in CA)
- **Citation style** is different (Bluebook variant in WA,
  Oregon Style Manual in OR, California Style Manual in CA)
- **Consumer-protection statute** is different (WA CPA, OR
  UTPA, CA Rosenthal Act, TX DTPA)
- **Collection-agency registration** varies (mandatory in OR
  with ORS 697; California adopted CDCLA in 2022; many states
  have no equivalent)

Always research the state's specific law. **Use WebFetch
against the state's authoritative sources** before writing
substantive content.

### Trigger phrases must be state-specific

Every skill's `description:` includes trigger phrases. Update
them to match how a litigant in that state would actually
phrase a question. A California pro se filer says "Cal. Civ.
Proc. Code § 437c" for summary judgment, not "ORCP 47".

### Use the state's terminology

- Oregon: "Notice of Hearing"
- Washington: "Note for Motion Docket"
- California: "Notice of Motion" (CCP § 1010)
- Texas: "Notice of Hearing"
- Florida: "Notice of Hearing"

Don't import another state's terminology.

### Quirks deserve prominent flags

Every state has procedural quirks that trip practitioners
from other states. Surface them in the skill descriptions:

- Oregon: no written interrogatories under ORCP
- California: CCP § 437c summary judgment timing differs
  from FRCP 56
- Texas: TRCP 169 expedited-actions rules; "level 1" /
  "level 2" / "level 3" discovery control plans
- Florida: Rule 1.510 summary judgment was amended in 2021
  to align with federal standard
- New York: "verified" pleadings vs. "unverified" — distinct
  treatment under CPLR

### Pre-1.0 versions only

The marketplace is pre-1.0. New plugins ship at 0.1.0; new
skills ship at 0.1.0. Reserve 1.0+ for when the plugin shape
has stabilized.

### One plugin per state

Don't sub-divide. A high-volume court can get its own skill
within the state plugin; a long-tail county is in the
roll-up. There are 3,000+ U.S. counties — per-county plugins
don't scale.

## References

- `references/thin-skill-architecture.md` — **READ FIRST**
  before authoring any SKILL.md body. The "keep the law in
  references, not in skills" principle that drives current
  authorship: what to keep vs. remove, refactor playbook
  for thick skills, citation-drift hazard catalog, and the
  cross-state-port benefit
- `references/checklist.md` — step-by-step checklist for the
  manual path, including the pre-commit cross-state-reference
  scan and post-commit verification phases
- `references/skill-templates/` — canonical SKILL.md templates
  for each of the 21 base roles, with placeholders for state-
  specific content
- `references/state-research-protocol.md` — how to research a
  new state's procedural rules from authoritative sources
- `references/cross-state-quirks.md` — known procedural
  quirks across the most-populous states, useful for the
  initial-research phase (**do not import these comparisons
  into the new plugin's bodies** — they go in the developer's
  understanding, not the end-user-facing skill text)
- `references/puller-design-lessons.md` — technical patterns
  for writing the state's `pull_<state>_*.py` scripts:
  curl_cffi + Chrome TLS impersonation for Cloudflare bypass,
  API-key conditional patterns, prefetch-and-slice, literal-
  `\n` decoding, regression protection (`_file_is_stub`),
  index-parser nested-tag handling, distinguishing
  dispositioned-redirect from parse-failure on zero-section
  results, the never-silent-stub rule, periodic CHAPTERS
  pruning for repealed chapters, and workflow-yaml
  integration
- `references/scaffold-script.md` — usage notes for
  `scripts/scaffold-state.py`
- `scripts/scaffold-state.py` — the scaffolder
