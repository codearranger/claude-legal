# Checklist — Adding a New State Plugin

Step-by-step checklist for the manual path. Use this alongside
the `scaffold-state.py` script, or independently if you want
maximum control.

## Phase 0 — Research the state

Before touching the codebase, gather the inputs. See
`state-research-protocol.md` for the WebFetch recipes.

- [ ] State name and two-letter abbreviation
- [ ] State pleading-format rule (citation + name; e.g.,
      "CRC Rule 2.100, 2.110, 2.111" for California)
- [ ] State civil rules code (CCP, ORCP, TRCP, etc.)
- [ ] State evidence rules code (CEC, OEC, ER, etc.)
- [ ] State statute code prefix (e.g., "Cal. Civ. Code",
      "Tex. Bus. & Com. Code", "Fla. Stat.")
- [ ] Citation style manual URL
- [ ] Two flagship high-volume courts:
  - Slug (short identifier, e.g., `lasc` for Los Angeles
    Superior Court)
  - Display name
  - Address
  - Civil-scheduling protocol (JA-based / Civil Division /
    centralized motion docket)
- [ ] 10 most-populous counties for the roll-up (excluding
      the two flagship counties)
- [ ] State legal-holiday list (federal + any state-specific)
- [ ] State analog to FDCPA at state level (e.g., California
      Rosenthal Act, Tex. Bus. & Com. Code Ch. 392)
- [ ] State collection-agency registration regime if any
- [ ] State statute of limitations on written contract debt
      (typically 3–6 years)
- [ ] Court eFiling system (state-specific portal)

### Family law — baseline research items

The `<abbr>-family-court` venue skill and `<abbr>-family-
law` subject bundle ship as part of the baseline. Research
these state-specific items before authoring either:

- [ ] **Family-court topology** — separate Family Court
      trial court OR Family Division of the general-
      jurisdiction trial court?
- [ ] **Family-court rule set** — citation
- [ ] **Family-law code** — citation
- [ ] **Divorce grounds** — no-fault waiting period; fault
      grounds catalog if still recognized
- [ ] **Residency requirement** — duration before filing
- [ ] **Property regime** — community-property (CA, TX,
      WA, AZ, NM, ID, LA, NV, WI) vs. equitable-
      distribution (everyone else)
- [ ] **Child-support guideline model** — income-shares
      (most states) vs. percentage-of-payor-income
      (shrinking minority) vs. Melson formula (rare)
- [ ] **Child-support combined-income cap** — $ amount +
      effective date
- [ ] **Modification threshold for child support** —
      percentage change required to revisit
- [ ] **Custody standard** — best-interests is universal;
      statutory factors are state-specific
- [ ] **Maintenance / spousal-support framework** —
      duration formula; income-based formula where
      applicable; modification + termination triggers
- [ ] **Common-law marriage** — recognized in the state?
      As of 2026: yes in CO, IA, KS, MT, RI, SC (pre-2019),
      TX, UT, DC. All other states honor marriages valid
      where contracted.
- [ ] **Family-court forms catalog** — state's pro-se form
      numbering
- [ ] **Support magistrate / referee structure** — where
      applicable, the judicial layer that hears support
      matters before a Family Court Judge can review
- [ ] **Right to assigned counsel** — which family-court
      proceedings provide assigned counsel (typically
      abuse-and-neglect respondents; sometimes family-
      offense respondents facing protective orders;
      sometimes termination of parental rights)
- [ ] **UCCJEA implementation** — verify the state has
      adopted UCCJEA (all 50 states + DC have) and note
      any state-specific quirks
- [ ] **UIFSA implementation** — verify the state has
      adopted UIFSA (all 50 states + DC have)

### Civil-court venue layers — survey before deciding on
### dedicated skills

Don't assume the state has a flat Superior/Supreme + county-
courts topology. Some states have civil-court layers that
justify **dedicated venue skills** rather than rolling
everything into the county-courts roll-up:

- [ ] Does the state have a separate **lower civil court**
      with a monetary cap below the general-jurisdiction
      trial court (e.g., a "Civil Court" or "Special Civil
      Part" under its own act)? If so, consider a dedicated
      skill.
- [ ] Does the state have a **dedicated housing court** as
      a separate trial court or a structurally distinct
      part of the lower civil court? Often worth dedicated
      coverage given volume.
- [ ] Does the state have **District Courts** as an
      intermediate civil layer between Justice/Town courts
      and Superior/Supreme? Dedicated skills.
- [ ] Does the state have **City Courts** distinct from
      rural Justice Courts? Both layers may warrant their
      own skill.
- [ ] Does the state have a separate **Family Court** trial
      court (vs. a Family Division of the general-
      jurisdiction court)? The `<abbr>-family-court` venue
      skill always ships in the baseline, but the body
      framing differs.

The shape of the state's trial-court system dictates the
total skill count. Existing plugins in the marketplace
range from 21 to 35 skills.

### Phase 0.5 — Probe the live upstream

Before authoring the puller's target catalog, verify
identifiers against the actual source-of-truth API or HTML
index. Common pitfalls:

- [ ] Confirm the URL pattern is current (CMS migrations
      change paths; legacy URLs often redirect to an index
      page rather than to the rule content)
- [ ] Confirm Part / Article numbering against the live
      index (adjacent Parts get conflated easily — never
      infer a Part's title from the table-of-contents
      ordering)
- [ ] Confirm Article identifiers match the API's
      `locationId` format (hyphenated vs. unhyphenated
      sub-articles often look interchangeable but only one
      resolves)
- [ ] Confirm which **law** owns each topic — a topic that
      seems like it should be in one statute may live in
      another (e.g., procedural details may sit in the
      domestic-relations procedural code rather than in the
      substantive family-law code)
- [ ] If the upstream has an API: probe the JSON response
      shape (e.g., `{documents: {items: [...]}}` vs.
      `{documents: [...]}`) before assuming the walker
      structure
- [ ] If the upstream has authentication: identify whether
      it's an API key, OAuth, or something else; register
      for any keys before the puller is wired into CI

See [`puller-design-lessons.md`](puller-design-lessons.md)
for the full puller-design discipline.

## Phase 1 — Plugin manifest

- [ ] Create `plugins/<abbr>-court-docs/.claude-plugin/plugin.json`
- [ ] Set `name`, `version: "0.1.0"`, `description`, keywords
- [ ] **Add `"dependencies": ["claude-legal-federal-laws"]`** —
      the new plugin reaches federal-debt-laws / ucc-model via
      symlinks into the shared `claude-legal-federal-laws`
      plugin. Without this declaration, the marketplace runtime
      won't auto-install the shared plugin and the symlinks
      won't resolve at install time.
- [ ] Description follows the WA/OR pattern: a comprehensive
      paragraph naming all 21 skills' roles and the consumer-
      debt bundle
- [ ] Keywords include state, court types, civil rules code,
      consumer-protection statute, registration system, etc.

## Phase 2 — Directory scaffolding

- [ ] Create the 21 skill directories under
      `plugins/<abbr>-court-docs/skills/`:
  - [ ] `<abbr>-statewide-format/references/templates/`
  - [ ] `<abbr>-<primary-court-slug>/references/`
  - [ ] `<abbr>-<secondary-court-slug>/references/`
  - [ ] `<abbr>-county-courts/references/`
  - [ ] `<abbr>-pro-se/references/`
  - [ ] `<abbr>-law-references/references/`
    - [ ] `court-rules/` (real directory)
    - [ ] `federal-debt-laws` — **SYMLINK** pointing to
          `../../../../claude-legal-federal-laws/references/federal-debt-laws`.
          Do NOT create a real directory here.
    - [ ] `ucc-model` — **SYMLINK** pointing to
          `../../../../claude-legal-federal-laws/references/ucc-model`.
          Do NOT create a real directory here.
    - [ ] `<state>-statutes-debt/` (e.g., `ca-statutes-debt/`)
  - [ ] `<abbr>-discovery/references/`
  - [ ] `<abbr>-hearings/references/`
  - [ ] `<abbr>-post-judgment/references/`
  - [ ] `<abbr>-first-30-days/` (no references typically)
  - [ ] `<abbr>-fact-check/` (no references typically)
  - [ ] `<abbr>-deadlines/` (no references typically)
  - [ ] `<abbr>-draft-motion/` (no references)
  - [ ] `<abbr>-draft-declaration/`
  - [ ] `<abbr>-draft-note/` (or `-notice-of-motion` per
        state terminology)
  - [ ] `<abbr>-draft-order/`
  - [ ] `<abbr>-quality-check/`
  - [ ] `<abbr>-schedule-hearing/`
  - [ ] `<abbr>-file-packet/`
  - [ ] `<abbr>-submit-order/`
  - [ ] `<abbr>-family-court/` (NEW BASELINE — venue skill)
  - [ ] `<abbr>-consumer-debt/references/examples/`
  - [ ] `<abbr>-family-law/references/examples/` (NEW
        BASELINE — subject bundle alongside consumer-debt)
- [ ] Create `plugins/<abbr>-court-docs/scripts/`
- [ ] Create `plugins/<abbr>-court-docs/evals/` with the five
      subdirs: drafting, formatting, procedural, subject-
      matter, integration

## Phase 3 — SKILL.md files

For each of the 23 base skills (plus any additional venue
or subject-matter skills the state warrants), author a
`SKILL.md` using the matching template in `skill-templates/`.
Required for every SKILL.md:

- [ ] YAML frontmatter with `name`, `description`, `version`
- [ ] `name` exactly matches the containing directory
- [ ] `version: 0.1.0`
- [ ] `description` block with realistic trigger phrases
- [ ] Body with substantive content (not just "TODO")
- [ ] Cross-references to other skills in the plugin
- [ ] Disclaimer ("NOT LEGAL ADVICE...")
- [ ] **NO cross-state references** — see Phase 8
      verification grep. Don't write "the same as Washington's
      GR 14", "unlike Oregon's no-interrogatories rule",
      "California's In Pro Per" comparisons. State the rule
      directly without comparing.

Run lint after each batch:
```bash
python3 scripts/lint-skills.py
```

## Phase 4 — Reference content

For each skill that has a `references/` directory, author
the reference files using the OR or WA equivalent as a
guide. Don't search-and-replace — research the state's
specific law.

### `<abbr>-statewide-format/references/`

- [ ] `<format-rule>-full-text.md` — verbatim or summary of
      the state's format rule
- [ ] `caption-format.md` — caption structure with docx-js
      example
- [ ] `exhibit-handling.md` — exhibit numbering convention
      and pagination
- [ ] `docx-generation.md` — docx-js patterns for the state
- [ ] `templates/declaration.md`
- [ ] `templates/motion-with-memo.md`
- [ ] `templates/notice-of-hearing.md` (or state equivalent)
- [ ] `templates/proposed-order.md`

### `<abbr>-<primary-court>/references/`

- [ ] Courthouse info file (`central-courthouse.md` or
      similar)
- [ ] Civil-motion-scheduling protocol
- [ ] Local-rule summary

### `<abbr>-<secondary-court>/references/`

- Same structure as primary court

### `<abbr>-county-courts/references/`

- [ ] `county-courts-directory.md` — full county list with
      contact info
- [ ] `filing-and-service.md` — county-by-county quirks

### `<abbr>-pro-se/references/`

- [ ] `pro-se-drafting-framework.md` — pro-se drafting framework adapted for
      the state
- [ ] `service-protocol.md` — state's service rules under
      the state's civil rules
- [ ] `pro-se-toolkit.md` — common pro se motion types

### `<abbr>-law-references/references/`

- [ ] `civil-rules.md` — rule-by-rule summary of state civil
      rules
- [ ] `evidence-rules.md` — section-by-section summary of
      state evidence code
- [ ] `fees-and-costs.md` — state's fee-shifting framework
- [ ] `local-rules.md` — high-volume courts' local rules
- [ ] `citation-format.md` — state style-manual conventions
- [ ] `key-cases.md` — general-civil precedents
- [ ] `online-sources.md` — canonical URLs (WebFetch
      catalog)
- [ ] `legal-data-apis.md` — programmatic-access index
- [ ] `court-rules/README.md` — corpus README
- [ ] `court-rules/_manifest.json` — corpus manifest
- [ ] `federal-debt-laws/README.md`
- [ ] `ucc-model/README.md`
- [ ] `<state>-statutes-debt/README.md`
- [ ] `<state>-statutes-debt/_manifest.json`

### `<abbr>-discovery/references/`

- [ ] `meet-and-confer.md`
- [ ] `objection-responses.md`

### `<abbr>-hearings/references/`

- [ ] `oral-argument.md`
- [ ] `courtroom-etiquette.md`
- [ ] `zoom-hearings.md` (or state remote-hearing platform)
- [ ] `hearing-day-checklist.md`

### `<abbr>-post-judgment/references/`

- [ ] `motion-to-vacate.md` (state's analog to ORCP 71 / CR
      60 / FRCP 60(b))
- [ ] `garnishment-response.md`
- [ ] `exemptions.md` — state's exemption catalog
- [ ] `supplemental-proceedings.md` — state's debtor exam
- [ ] `satisfaction-of-judgment.md`

### `<abbr>-consumer-debt/references/`

- [ ] `SKILL.md` (main bundle)
- [ ] `fdcpa.md`
- [ ] `reg-f.md`
- [ ] `<state>-utpa-or-equiv.md` (e.g., `ca-rosenthal-act.md`
      for California)
- [ ] `<state>-collection-agency-law.md` (if applicable)
- [ ] `chain-of-title.md`
- [ ] `evidence-debt-buyer.md`
- [ ] `<state>-statutes-of-limitations.md`
- [ ] `key-cases.md`
- [ ] `recent-decisions.md`
- [ ] `fees-consumer-debt.md`
- [ ] `rfp-debt-buyer.md`
- [ ] `rfa-debt-buyer.md`
- [ ] `interrogatories-debt-buyer.md` (always include, even
      if state allows interrogatories — explain availability
      and use)
- [ ] `meet-and-confer-debt-buyer.md`
- [ ] `online-sources-consumer-debt.md`
- [ ] `ucc-article-9.md`
- [ ] `fact-patterns.md` — 5 fact-pattern triage
- [ ] `examples/README.md`
- [ ] `examples/example-answer.md`
- [ ] `examples/example-declaration.md`
- [ ] `examples/example-motion-to-compel.md`
- [ ] `examples/example-meet-and-confer.md`
- [ ] `examples/example-proposed-order.md`
- [ ] `examples/example-certificate-of-service.md`

### `<abbr>-family-court/references/`

The venue skill's reference content. Use the
`family-court-template.md` as the starting shape (no
separate references dir is required — the SKILL.md body
carries the substantive coverage), but include these where
state-specific:

- [ ] `forms-catalog.md` — state's family-court pro-se form
      catalog
- [ ] `support-magistrate-procedure.md` (where applicable)
- [ ] `confidentiality-and-sealing.md`

### `<abbr>-family-law/references/`

The substantive bundle. Mirror `co-family-law` structure:

- [ ] `SKILL.md` (main bundle)
- [ ] `dissolution.md` — divorce mechanics + procedural
      flow
- [ ] `annulment.md` — declaration-of-invalidity grounds
- [ ] `legal-separation.md` — where state recognizes
- [ ] `property-distribution.md` — community-property
      presumptions OR equitable-distribution factors
- [ ] `child-support.md` — guideline framework + cap +
      modification threshold
- [ ] `parenting-plan.md` — decision-making + parenting
      time + relocation
- [ ] `maintenance.md` — spousal-support / alimony
      framework + modification
- [ ] `family-offense.md` — Order of Protection
      framework + qualifying-relationship + qualifying-
      offense
- [ ] `uccjea.md` — Uniform Child Custody Jurisdiction +
      Enforcement Act implementation
- [ ] `uifsa.md` — Uniform Interstate Family Support Act
      implementation
- [ ] `common-law-marriage.md` — state's status; if
      recognized, the test + modernizing case law
- [ ] `forms.md` — state-specific divorce + custody + CS
      forms
- [ ] `key-cases.md` — state appellate family-law
      precedents
- [ ] `online-sources.md` — state's family-court / self-
      help / form-catalog URLs
- [ ] `examples/example-petition-for-dissolution.md`
- [ ] `examples/example-sworn-financial-statement.md`
- [ ] `examples/example-parenting-plan-motion.md`
- [ ] `examples/example-cs-modification-motion.md`

## Phase 5 — Scripts

- [ ] Adapt `plugins/<abbr>-court-docs/scripts/format-check.py`
      from the OR plugin
  - Update rule reference in the report header
  - Adjust acceptable-fonts list to state convention
  - Adjust color-handling per state rule (some states allow
    color in certain contexts)
- [ ] Adapt `plugins/<abbr>-court-docs/scripts/case-calendar.py`
      from the OR plugin
  - Update FIXED_HOLIDAYS list with state-specific holidays
  - Update WEEK_HOLIDAYS list if state has unique week-based
    holidays (e.g., WA's day after Thanksgiving)
  - Update RULES dict with state-specific named rules
  - Update SOL entries with state-specific SOLs

## Phase 6 — Evals

Author at least **20 evals** across the five categories.
Both subject-matter bundles ship in the baseline, so the
subject-matter category needs evals covering both:

- [ ] `evals/README.md`
- [ ] `evals/drafting/` — 4 evals
- [ ] `evals/formatting/` — 4 evals
- [ ] `evals/procedural/` — 7-8 evals
- [ ] `evals/subject-matter/` — 6-8 evals split between
      consumer-debt (chain-of-title, SOL, mini-FDCPA,
      default-judgment scrutiny) AND family-law
      (child-support calculation, custody best-interests,
      family-offense OP elements, property-distribution
      regime)
- [ ] `evals/integration/` — 2 evals (one end-to-end on
      each bundle's flagship fact pattern)

## Phase 7 — Marketplace updates

- [ ] Add new plugin to `.claude-plugin/marketplace.json`
- [ ] Bump `marketplace.json`'s `metadata.version`
- [ ] Update `CLAUDE.md`:
  - Add new skills-index table
  - Add new reference-corpora section
  - Add new plugin's scripts to "Common commands"
  - Bump comparison-state count if applicable
- [ ] Update `README.md`:
  - Add new plugin to the "What's in here" list
  - Add new plugin to the directory-tree section
  - Update the install command
  - Add new column to the WA-vs-OR-vs-new comparison table
  - Update the disclaimer / closing if needed

## Phase 8 — Verification

### Lint + scripts

- [ ] Run `python3 scripts/lint-skills.py` — must show 0 fails
- [ ] Run the new plugin's `format-check.py` against a sample
      `.docx` to verify it works
- [ ] Run the new plugin's `case-calendar.py --rules` to
      verify the rules list is populated
- [ ] Spot-check 3–5 randomly chosen SKILL.md files for
      substance (not just template stubs)
- [ ] Spot-check a few cross-references — broken paths are
      common

### Cross-state-reference scan (must come back clean)

Run this grep over the new plugin's tree before commit. Any
hit needs to be resolved before the plugin ships:

```bash
grep -rnE "\b(Washington|Oregon|California|Colorado|Indiana|New York)\b\
|wa-court-docs|or-court-docs|ca-court-docs|co-court-docs|in-court-docs|ny-court-docs\
|like (Oregon|California|Colorado|Indiana|Washington|New York)\
|unlike (Oregon|California|Colorado|Indiana|Washington|New York)\
|federal/(WA|OR|CA|CO|IN|NY)" plugins/<abbr>-court-docs/ \
  --include="*.md" --include="*.json"
```

- [ ] Grep returns no real hits (false positives like
      `Washington's Birthday` as a holiday name, `in-person`,
      `co-parents`, or verbatim statutory text mentioning a
      state name are OK — distinguish before deleting)
- [ ] No SKILL.md cross-references another state's plugin
- [ ] No reference-corpus README cross-references another
      state's plugin
- [ ] No evals/README.md "see WA / OR / CA / etc. evals"
      section

### JSON validation

- [ ] `python3 -m json.tool .claude-plugin/marketplace.json`
      — must round-trip
- [ ] `python3 -m json.tool plugins/<abbr>-court-docs/.claude-plugin/plugin.json`
      — must round-trip
- [ ] Any `_manifest.json` files produced by pull scripts
      round-trip cleanly
- [ ] Long description strings have all internal double
      quotes backslash-escaped (`\"`)

### Internal cross-reference resolution

Run this scan to confirm every `<state>-XXX` reference inside
the plugin resolves to an actual skill directory:

```bash
for f in plugins/<abbr>-court-docs/skills/*/SKILL.md; do
  base=$(basename $(dirname $f))
  grep -oE '<abbr>-[a-z0-9][a-z0-9-]+' "$f" | sort -u | while read ref; do
    if [ "$ref" = "$base" ] || [ "$ref" = "<abbr>-court-docs" ]; then continue; fi
    if [ ! -d "plugins/<abbr>-court-docs/skills/$ref" ]; then
      echo "  $base -> BROKEN: $ref"
    fi
  done
done
```

- [ ] No broken cross-references reported

### Verbatim corpus sanity

If pull scripts ran successfully:

- [ ] At least one statute / rule file is > 5 KB (most should
      be much larger — sub-1 KB usually means the puller got
      a navigation page or stub instead of content)
- [ ] Spot-check one file's section text against the canonical
      source — no embedded `\n` literal sequences, no
      duplicated section headings, no Cloudflare interstitial
      text
- [ ] `_manifest.json` reflects today's date and the correct
      mode (`api` vs `stubs`)

## Phase 9 — Commit

- [ ] Stage all new files
- [ ] Commit with a substantive message describing what
      shipped (mirror the OR commit-message style)
- [ ] Push to the user-designated branch

## Phase 10 — Followup tasks (not blocking)

- [ ] Add `scripts/pull_<state>_rules.py` — pulls state
      court rules from the state's authoritative source
- [ ] Add `scripts/pull_<state>_<statute>.py` — pulls
      state statutes
- [ ] Register the quarterly remote-agent routine to refresh
      the state's reference corpora

## Final sanity check

A new state plugin is **not done** until:

1. Every SKILL.md passes lint
2. Every cross-reference resolves
3. Every citation is in the state's correct style
4. The plugin can be loaded by Claude Code and at least one
   skill auto-invokes from a natural-language prompt
5. The README and CLAUDE.md reflect the new plugin
