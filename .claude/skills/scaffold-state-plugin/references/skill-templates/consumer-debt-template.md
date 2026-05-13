---
name: {{ABBR}}-consumer-debt
description: >
  Use this skill for {{STATE_NAME}} consumer-debt defense —
  debt-buyer suits, original-creditor collection cases, and
  any matter turning on the FDCPA, CFPB Regulation F, the
  {{STATE_CONSUMER_STATUTE}}, or the {{COLLECTION_REGIME}}
  as applied to debt collection. Triggers include "debt
  buyer", "I was sued on a credit card", "collection agency
  sued me", "FDCPA", "1692e", "1692f", "1692g", "validation
  notice", "Regulation F", "12 CFR 1006", "{{STATE_CONSUMER_STATUTE}}",
  "statute of limitations on this debt" ({{CONTRACT_SOL}}-year
  SOL on contract debt in {{STATE_NAME}}), "time-barred
  debt", "chain of title", "bill of sale", "assignment
  schedule", "original cardholder agreement", "monthly
  statements", "remote custodian", "{{EVIDENCE_RULES}} 803
  business records", "{{EVIDENCE_RULES}} 901 authentication",
  the names of major debt-buyer plaintiffs (CACH, Unifund,
  Palisades, Midland, Portfolio Recovery, LVNV, Velocity
  Investments, Jefferson Capital). Subject-matter bundle of
  FDCPA / Reg F / state UTPA-equivalent / state collection-
  agency law plus chain-of-title doctrine and discovery banks.
  Composes with all matter-neutral procedural skills.
version: 0.1.0
---

# {{STATE_NAME}} Consumer-Debt Defense

This skill is the **subject-matter bundle** for {{STATE_NAME}}
consumer-debt litigation. It assumes the procedural framework
is in place via the matter-neutral skills and adds:

- **Substantive law**: FDCPA, Reg F, {{STATE_CONSUMER_STATUTE}},
  {{COLLECTION_REGIME}}
- **Chain-of-title doctrine**: what a debt-buyer plaintiff
  must prove
- **Evidence patterns**: business-records foundation
  ({{EVIDENCE_RULES}} 803(6) / 902(11)) and authentication
- **Fact-pattern triage**: 5 common debt-defense scenarios
- **Discovery banks**: pre-built RFPs and RFAs
- **Example filings**: synthetic filings for a debt-buyer-
  defense fact pattern

> **NOT LEGAL ADVICE.** This skill provides a procedural and
> substantive framework — not strategic advice for any
> specific case.

## Five common {{STATE_NAME}} debt-defense fact patterns

### Pattern 1: Debt-buyer suit on an unfamiliar account

> **TODO**: Adapt the WA/OR Pattern 1 to {{STATE_NAME}}-
> specific defenses and counterclaims.

**Strongest defenses**:

- Lack of standing (chain of title)
- SOL ({{CONTRACT_SOL}}-year under {{STATE_NAME}} law)
- {{STATE_NAME}} licensing / registration requirement if any
- {{EVIDENCE_RULES}} 803(6) / 902(11) foundation challenge

**Strongest counterclaims**:

- FDCPA (15 USC § 1692e/f/g)
- {{STATE_CONSUMER_STATUTE}} (state UTPA-analog)
- {{COLLECTION_REGIME}} if plaintiff is unlicensed

### Pattern 2: Original creditor collection on a known account

> **TODO**: Adapt to {{STATE_NAME}}.

### Pattern 3: Time-barred debt revival attempt

> **TODO**: Document the state's SOL and revival rule:
> - State SOL on contract: {{CONTRACT_SOL}} years
> - Revival rule: written promise only? or partial payment?
> - State analog to ORS 12.230 / RCW 4.16.270

### Pattern 4: Default judgment entered improperly

> **TODO**: Adapt the OR ORCP 71 framework to the state's
> vacation rule (state's FRCP 60 analog).

### Pattern 5: Unauthorized debt collection

> **TODO**: Adapt to the state's collection-agency law.

## Substantive law — quick reference

### FDCPA (15 USC § 1692 et seq.)

Same federal statute applies in every state. See
`references/fdcpa.md`.

### Regulation F (12 CFR pt 1006)

Same federal regulation. See `references/reg-f.md`.

### {{STATE_CONSUMER_STATUTE}}

> **TODO**: Document the state's consumer-protection
> statute analogous to OR UTPA / WA CPA:

- Coverage (who is liable; debt-collector vs. any "person")
- Damages and remedies (statutory minimums, caps, punitive)
- Statute of limitations
- Fee-shifting
- "Ascertainable loss" or similar standing requirement

See `references/{{STATE_CONSUMER_STATUTE_SLUG}}.md`.

### {{COLLECTION_REGIME}}

> **TODO**: Document the state's collection-agency
> licensing / registration regime if any:
> - Definitions of "collection agency"
> - Registration / licensing requirement
> - Effect of non-compliance (capacity to sue?)
> - Private right of action
> - Public-facing licensing database URL

See `references/{{COLLECTION_REGIME_SLUG}}.md`.

### Chain of title

The doctrinal core of debt-buyer cases. See
`references/chain-of-title.md`.

## Discovery banks

This skill's RFP / RFA banks adapt the OR templates to
{{STATE_NAME}}'s discovery rules. See:

- `references/rfp-debt-buyer.md`
- `references/rfa-debt-buyer.md`
- `references/interrogatories-debt-buyer.md` (state-
  specific — note availability and use)
- `references/meet-and-confer-debt-buyer.md`

## Evidence patterns

The {{EVIDENCE_RULES}} 803(6) / 902(11) foundation is the
critical evidentiary battleground. See
`references/evidence-debt-buyer.md`.

## Key cases — {{STATE_NAME}} and federal

> **TODO**: Identify state-specific decisions on:
> - Business-records foundation in debt cases
> - State UTPA-equivalent scope and remedies
> - Collection-agency licensing requirements
> - Chain-of-title authentication

Federal:
- Henson v. Santander Consumer USA (debt-buyer "debt
  collector" status)
- Heintz v. Jenkins (attorneys as debt collectors)
- Marx v. General Revenue (FDCPA fees)

See `references/key-cases.md`.

## Example filings

The `references/examples/` directory contains synthetic
example filings for a debt-buyer-defense fact pattern:

- `example-answer.md`
- `example-declaration.md`
- `example-motion-to-compel.md`
- `example-meet-and-confer.md`
- `example-proposed-order.md`
- `example-certificate-of-service.md`

> **TODO**: Adapt the OR examples to {{STATE_NAME}}'s
> procedural conventions.

## Companion procedural skills

This subject-matter bundle composes with:

- `{{ABBR}}-statewide-format`
- `{{ABBR}}-{{PRIMARY_COURT_SLUG}}` / `{{ABBR}}-{{SECONDARY_COURT_SLUG}}` /
  `{{ABBR}}-county-courts`
- `{{ABBR}}-pro-se`
- `{{ABBR}}-law-references`
- `{{ABBR}}-discovery`
- `{{ABBR}}-first-30-days`
- `{{ABBR}}-deadlines`
- `{{ABBR}}-fact-check`
- `{{ABBR}}-quality-check`
- `{{ABBR}}-draft-*` skills
- `{{ABBR}}-post-judgment`

## References

> **TODO**: Build out each of these:
- `references/fdcpa.md`
- `references/reg-f.md`
- `references/{{STATE_CONSUMER_STATUTE_SLUG}}.md`
- `references/{{COLLECTION_REGIME_SLUG}}.md` (if applicable)
- `references/{{ABBR}}-statutes-of-limitations.md`
- `references/chain-of-title.md`
- `references/evidence-debt-buyer.md`
- `references/fact-patterns.md`
- `references/key-cases.md`
- `references/recent-decisions.md`
- `references/fees-consumer-debt.md`
- `references/rfp-debt-buyer.md`
- `references/rfa-debt-buyer.md`
- `references/interrogatories-debt-buyer.md`
- `references/meet-and-confer-debt-buyer.md`
- `references/online-sources-consumer-debt.md`
- `references/ucc-article-9.md`
- `references/examples/`
