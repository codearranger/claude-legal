---
name: {{ABBR}}-law-references
description: >
  This skill should be used when the user needs to cite,
  apply, or research law that bears on {{STATE_NAME}} civil
  court practice across any subject matter. Triggers include
  {{CIVIL_RULES}} rule references (e.g., "{{CIVIL_RULES}} 12",
  "{{CIVIL_RULES}} 26"), {{EVIDENCE_RULES}} references (e.g.,
  "{{EVIDENCE_RULES}} 803"), state-statute references (e.g.,
  "{{STATUTE_CODE}} § N"), "civil rules", "evidence rules",
  "best evidence", "hearsay exception", "business records",
  "authentication", "meet and confer", "motion to compel",
  "summary judgment standard", "attorney fees", "{{STYLE_MANUAL}}".
  Covers the state's civil rules, evidence rules, citation
  format, fees-and-costs framework, local rules for the
  flagship courts, general civil key cases, and the canonical
  online-sources catalog. For subject-matter-specific law
  (debt collection, landlord-tenant, family, personal injury,
  criminal), compose with the relevant subject-matter skill
  (e.g., {{ABBR}}-consumer-debt). Compose with
  {{ABBR}}-statewide-format, {{ABBR}}-{{PRIMARY_COURT_SLUG}},
  {{ABBR}}-pro-se, and {{ABBR}}-fact-check as needed.
version: 0.1.0
---

# {{STATE_NAME}} Law References — General Civil Practice

This skill is a matter-neutral reference index — a pointer
to the statutes, rules, and doctrines most often invoked in
{{STATE_NAME}} civil practice across any subject matter. The
body below summarizes each source. Detailed sections,
elements, and citation examples live in `references/`.

> **NOT LEGAL ADVICE.** These notes are drafting aids. Every
> citation should be verified before filing. Use
> `{{ABBR}}-fact-check` before any packet is filed.

## How to use this skill

Ask: *what is the user trying to establish procedurally?*

- **A procedural motion** → `references/civil-rules.md`
- **An evidentiary objection** → `references/evidence-rules.md`
- **A fee-and-cost request** → `references/fees-and-costs.md`
- **A local-rule question** → `references/local-rules.md`
- **Citation format** → `references/citation-format.md`
- **Canonical URL or citation verification** →
  `references/online-sources.md` and hand off to
  `{{ABBR}}-fact-check`
- **Programmatic / structured lookup** →
  `references/legal-data-apis.md`
- **A general civil case** → `references/key-cases.md`
- **Subject-matter law** (debt, LL/T, family, PI) → use the
  relevant subject-matter skill

## {{STATE_NAME}} civil rules ({{CIVIL_RULES}})

> **TODO**: Identify the state's civil-rules system. Some
> states have a single set; others split between trial-court
> levels (e.g., WA's CR + CRLJ). Document the key rules.

Key rules:

> **TODO**: List the workhorse rules with one-line summaries:
> - Service of process
> - Initial responsive pleading deadline
> - Motion to dismiss
> - Discovery (scope, RFPs, RFAs, depositions,
>   interrogatories if available)
> - Motion to compel
> - Summary judgment
> - Default and vacation
> - Time computation
> - Pleading amendments

See `references/civil-rules.md` for rule-by-rule coverage.

## Evidence rules ({{EVIDENCE_RULES}})

> **TODO**: Document the state's evidence code or rules:
> - Hearsay (relevance, definition, exceptions including
>   business records)
> - Authentication and self-authentication
> - Best evidence
> - Privileges

See `references/evidence-rules.md`.

## Fees and costs

> **TODO**: Document the state's fee-shifting framework:
> - American Rule baseline
> - Statutory fee-shifting paths
> - Contractual fee-shifting (reciprocal-fee rules?)
> - Rule-based fee-shifting (motion-to-compel fees, sanctions)
> - Lodestar methodology
> - Procedural mechanism (state's ORCP 68 analog)

See `references/fees-and-costs.md`.

## Local rules

Each {{STATE_NAME}} court maintains local rules:

- **{{PRIMARY_COURT_NAME}}**: TODO local-rule reference
- **{{SECONDARY_COURT_NAME}}**: TODO local-rule reference
- Other counties: see `{{ABBR}}-county-courts`

See `references/local-rules.md`.

## Citation format

{{STATE_NAME}} uses the **{{STYLE_MANUAL}}**. Common forms:

> **TODO**: Document the state's citation conventions:
> - State supreme court
> - State Court of Appeals
> - Federal cases (state's Bluebook variation)
> - State statutes ({{STATUTE_CODE}})
> - Court rules ({{CIVIL_RULES}})

See `references/citation-format.md`.

## Canonical online sources

`references/online-sources.md` is the AI-agent-friendly
catalog of canonical URLs for:

> **TODO**: List the state's authoritative sources:
> - State court rules
> - State statutes
> - State case law (CourtListener, state's official
>   publications)
> - Federal law (eCFR, USC)
> - State Style Manual

## Key general-civil cases

`references/key-cases.md` catalogs the general-civil cases
this plugin relies on most:

> **TODO**: Identify the state's leading decisions on:
> - Summary judgment burden
> - Inferences favorable to non-movant
> - Reciprocal fee-shifting
> - Lodestar methodology
> - American rule baseline
> - Default-judgment vacation

## Notes

- These references are neutral summaries. They do not tell
  the user whether they win or lose.
- Always **verify** a case is still good law before citing.
- For federal law, check the most recent {{STATE_CIRCUIT}}
  Circuit opinion where controlling.
- **Before filing**, run `{{ABBR}}-fact-check`.
