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
version: 0.3.0
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
13. **Family-court topology** — does the state have a separate
    Family Court (NY, MA, DE) or does it hear family matters
    in a Family Division of the general-jurisdiction trial
    court (most states)? Either way, the `<abbr>-family-court`
    venue skill ships. Note the venue, the rule set, and
    whether jurisdiction is concurrent with the regular
    civil-trial court for any topic (NY Supreme Court +
    Family Court both hear custody, for example).
14. **State's family-law code** (e.g., NY Domestic Relations
    Law + Family Court Act; California Family Code; Colorado
    C.R.S. art. 10 of title 14 — UDMA-based; Texas Family
    Code)
15. **State's child-support guideline model** — income-shares
    (most states; CO, NY's CSSA percentages on combined-
    income basis) vs. percentage-of-payor-income (a shrinking
    minority). Note the statutory cap on combined parental
    income.
16. **State's property-distribution regime** — community-
    property (CA, TX, WA, AZ, NM, ID, LA, NV, WI) vs.
    equitable-distribution (everyone else).
17. **State's divorce grounds** — no-fault available (now
    universal) but waiting periods + fault grounds vary
    (NY's 6-month no-fault separation period; CO's 91-day
    waiting period; etc.).

If the user hasn't supplied all of these, ASK before scaffolding
— the substance of every skill depends on getting these right.

## The pattern to mirror

The **23-skill base** is the minimum a new state plugin
should ship. Baseline coverage includes:

- **All civil court rules** for every civil-trial-court
  layer in the state (the state's pleading-format rule, the
  CPLR / CCP / TRCP / ORCP / FRCP-analog rules, the local
  rules of the flagship counties)
- **All civil practice** procedural skills (the 21-skill
  core: format, discovery, hearings, post-judgment, etc.)
- **All civil substantive laws** in the statutes corpus
  (the state's analog to CPLR + consolidated-laws articles
  covering procedure, evidence, fees, limitations,
  exemptions, garnishment, UCC Article 9, consumer-debt
  statutes)
- **Family court rules** for the state's family-court
  venue (e.g., 22 NYCRR Part 205 in NY; the equivalent
  Family Division rules where applicable)
- **Family practice** — the `<abbr>-family-court` venue
  skill + the `<abbr>-family-law` subject bundle
- **Family law** statutes (the state's family-law code in
  the statutes corpus — e.g., DRL + FCT in NY; Fam. Code
  in CA; C.R.S. art. 10 of title 14 in CO)

States with complex civil-court systems can and should add
more — NY ships 35 (5 flagship Supreme Court venues, 2
dedicated Long Island District Courts, NYC Civil Court +
NYC Housing Court, upstate City Courts, Justice Courts,
Family Court, plus 5 subject-matter bundles), CO ships 22.

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
- Substantive body text covering the state's rules
- References specific to the state (rule numbers, statute
  citations, case citations in the state's style manual
  format)
- Composition notes pointing to other skills in the plugin

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

- `civil-rules.md` — state's civil-procedure rules summarized
  (must cover both civil-practice rules AND family-court
  rules — e.g., for NY: 22 NYCRR Parts 202 + 205 + 208 +
  210 + 212 + 214)
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
  - State civil-procedure rules (CPLR / CCP / TRCP / ORCP /
    CR equivalent)
  - State evidence code (where codified as rule)
  - **State family-court rules** (e.g., 22 NYCRR Part 205
    for NY; check for state-specific family-court rule set
    even when family law sits in a Family Division)
  - Sealing of court records rule (statewide)
  - Costs and sanctions rule (statewide)
  - Rules of Professional Conduct
  - Sub-trial-court rule sets where applicable (NYC Civil
    Court, NY District Courts, NY City Courts, Justice
    Courts; NJ Special Civil Part Rules; etc.)
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
  - **Civil procedure** — state's procedure code (CPLR / CCP
    / TRCP / ORCP / CR equivalent)
  - **Evidence** — state's evidence code where statutory
  - **Limitations** — state's SOL chapter
  - **Garnishment + exemptions** — state's enforcement +
    exemption chapter
  - **UCC** — state's enactment of Articles 2, 3, 9
  - **Consumer protection** — state's UTPA analog
  - **Debt collection** — state's mini-FDCPA
  - **Real Property + summary proceedings** — for L&T cases
  - **Family law** — state's family-law code (e.g., NY DRL +
    FCT; CA Fam. Code; CO C.R.S. art. 10 of title 14 UDMA;
    TX Family Code)
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
separation / custody / child support / maintenance. Mirror
the CO precedent (`co-family-law`):

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
  combined-income; modification threshold (e.g., NY's 15%
  / CSSA review; CO's 10% threshold)
- `references/parenting-plan.md` — decision-making
  allocation; parenting time (overnights); relocation
  notice + standard for permission
- `references/maintenance.md` — duration formulas; income-
  based formulas (NY's CSSA-modeled approach; CO's 2014 +
  2024 reforms); modification + termination triggers
- `references/family-offense.md` — Order of Protection
  framework; qualifying-relationship + qualifying-offense
  catalog; duration; firearm-surrender mechanics
- `references/uccjea.md` — Uniform Child Custody
  Jurisdiction and Enforcement Act implementation in state;
  home-state jurisdiction analysis
- `references/uifsa.md` — Uniform Interstate Family Support
  Act implementation in state
- `references/common-law-marriage.md` — for the handful of
  states that still recognize it (CO recognizes;
  *Hogsett & Neale* in CO; NY does not recognize but
  honors marriages valid where contracted)
- `references/forms.md` — state-specific divorce / custody /
  child-support forms (e.g., NY JDF 1099 / 1111; CO JDF
  catalog; CA FL-100 series)
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

### CRITICAL: No cross-state references inside the plugin

Plugins install **one state at a time**. End users will not
have WA + OR + CA + CO + IN installed alongside the new
state's plugin. Comparisons to other states inside SKILL.md
bodies, eval bodies, plugin.json descriptions, or reference
READMEs are pure noise to the end user and **must be
removed before the plugin ships**.

What this means in practice when authoring the new plugin:

- **Don't frame state-specific quirks comparatively.** Write
  the rule directly. ❌ "Unlike Oregon's no-interrogatories
  rule, NY allows 25 interrogatories under CPLR 3130." ✓ "NY
  allows 25 interrogatories under CPLR 3130/3133(b)."
- **Don't reference sibling-state SKILL.md files.** The new
  plugin's `README.md`, `evals/README.md`, and reference-corpus
  READMEs must not say "see `wa-court-docs/evals/`" or "mirrors
  `co-court-docs/skills/co-law-references/...`". The end user
  will not have those plugins installed.
- **Don't import another state's terminology.** California's
  "In Pro Per" doesn't appear in NY filings; Washington's
  "Note for Motion Docket" doesn't appear in OR filings.
- **Don't use "the same as Washington's GR 14" or similar
  framing.** Cite the state's own rule directly.

**Internal cross-references between skills in the SAME plugin
are fine** and encouraged — e.g., `ny-discovery` referencing
`ny-statewide-format` is exactly what the marketplace runtime
expects.

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
  most states' Gen. Constr. or Govt. Codes, **not** a
  cross-state comparison. Keep it.
- **`in-person`** as a hyphenated phrase — matches the
  `\bin-` pattern when looking for `in-court-docs` references.
  Keep it.
- **`co-parents`, `co-counsel`, `co-defendant`** — match the
  `\bco-` pattern. Keep them.
- **Verbatim statutory text from the state's own consolidated
  laws** — e.g., NY's General Construction Law § 24 names the
  federal holiday "Washington's Birthday"; that's the literal
  state statute and not a cross-state reference.

Distinguish state-as-comparison from state-as-statute-author
before deleting.

### Verify URL slugs, locationIds, and Part numbers against the live source

**Don't rely on memory or example data for state-specific
identifiers.** Multiple identifiers have been wrong in past
authorship and triggered silent puller failures:

- **22 NYCRR Part 214 is Justice Courts, not Court of Claims**
  (Court of Claims is Part 206). Adjacent Parts get conflated
  easily.
- **NY GOB uses Article numbering (A5, A17), not Title
  numbering (T5, T17)** — even though many secondary sources
  refer to "Title 5" / "Title 17".
- **NY GBS uses `A22-A` and `A29-H`** (hyphenated), not `A22A`
  / `A29H`.
- **Child support and UIFSA in NY are in Family Court Act
  (FCT) Articles 4 and 5-B**, not in Domestic Relations Law.
  DOM Article 9 is Annulment, Article 10 is Divorce.
- **CMS migrations change URL patterns** — NY courts moved
  from `/rules/trialcourts/{N}.shtml` to `/rules/part-{N}-{slug}`
  in their Drupal 10 rollout. The legacy URLs redirect to an
  index page, not the rule content. Discover the actual URL
  slug at fetch time rather than assuming.

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
  `\n` decoding, regression protection (`_file_is_stub`), and
  workflow-yaml integration
- `references/scaffold-script.md` — usage notes for
  `scripts/scaffold-state.py`
- `scripts/scaffold-state.py` — the scaffolder
