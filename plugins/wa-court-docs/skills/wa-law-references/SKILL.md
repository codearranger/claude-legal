---
name: wa-law-references
description: >
  This skill should be used when the user needs to cite, apply, or
  research law that bears on Washington civil court practice across
  any subject matter. Triggers include "CR 12", "CR 26", "CR 37",
  "CR 56", "CR 60", "CRLJ", "civil rules", "evidence rules", "ER
  803", "ER 901", "ER 902", "ER 1002", "best evidence", "hearsay
  exception", "business records", "authentication", "meet and
  confer", "motion to compel", "summary judgment standard",
  "attorney fees", "prevailing party", "RCW 4.84", "CR 11 sanctions",
  "CR 37(a)(4)", "reciprocal fee-shifting", "lodestar", "GR 14",
  "Bluebook", "Washington citation format", "Wn.2d", "P.3d",
  "KCLCR", "KCDCLCR", "King County local rule", "canonical URL",
  "verify citation", "fetch court rule". Covers statewide civil
  rules (CR / CRLJ), evidence rules (ER), GR 14 citation format,
  RCW 4.84 fees-and-costs, local rules for King County Superior
  and District Court, general civil key cases (SJ standard,
  fee-shifting, CR 60), and the canonical online-sources catalog
  for fetching current rule text, statutes, and case law. For
  subject-matter-specific law (debt collection, landlord-tenant,
  family, personal injury, criminal), compose with the relevant
  subject-matter skill (e.g., wa-consumer-debt). Compose with
  wa-statewide-format, wa-kcdc, wa-pro-se, and wa-fact-check as
  needed.
version: 0.3.1
---

# Washington Law References — General Civil Practice

This skill is a matter-neutral reference index — a pointer to the
statutes, rules, and doctrines most often invoked in Washington
civil practice *across any subject matter*. The body below
summarizes each source. Detailed sections, elements, and citation
examples live in `references/`.

> **NOT LEGAL ADVICE.** These notes are drafting aids, not legal
> advice. Every citation should be verified against the current
> RCW, current court rule, or current case law before it goes
> into a filing. Use `wa-fact-check` before any packet is filed.

## How to use this skill

Ask: *what is the user trying to establish procedurally?*

- **A procedural motion** (compel, dismiss, strike, default, SJ,
  vacate) → start with `references/civil-rules.md`
- **An evidentiary objection** (hearsay, authentication, best
  evidence, foundation) → start with `references/evidence-rules.md`
- **A fee-and-cost request or objection** → start with
  `references/fees-and-costs.md`
- **A local-rule question** (KCLCR for Superior; KCDCLCR for
  District) → start with `references/local-rules.md`
- **Citation format** → `references/citation-format.md`
- **Canonical URL or citation verification** → start with
  `references/online-sources.md` and hand off to `wa-fact-check`
  for per-filing verification
- **Programmatic / structured lookup** (USC XML, eCFR API,
  CourtListener for cite-checking, bulk extraction, change
  detection) → `references/legal-data-apis.md`. Prefer the APIs
  listed there over HTML scraping when the result will be parsed
- **A general civil case** (SJ standard, lodestar,
  default-vacation) → start with `references/key-cases.md`
- **Subject-matter law** (FDCPA, Reg F, consumer protection,
  landlord-tenant, family, PI, criminal) → use the relevant
  subject-matter skill (e.g., `wa-consumer-debt` for debt
  collection)

## Washington civil rules

Two parallel sets of rules:

- **CR** — Civil Rules (Superior Court)
- **CRLJ** — Civil Rules for Courts of Limited Jurisdiction
  (District and Municipal — includes KCDC)

Key rules (both systems, unless noted):

- **CR/CRLJ 11** — signing of pleadings; 21-day safe harbor for
  sanctions
- **CR/CRLJ 12** — defenses and objections; motions to dismiss;
  response deadlines
- **CR/CRLJ 26** — general discovery scope; proportionality; **CR
  26(i) / CRLJ 26(f)**: conference of counsel before discovery
  motion
- **CR/CRLJ 33, 34, 36, 37** — interrogatories, requests for
  production, requests for admission, motion to compel
- **CR 55** — default; **CR 56** — summary judgment (superior
  court only; CRLJ does not have a direct SJ analogue)
- **CR/CRLJ 6** — time computation; notice periods
- **CR/CRLJ 60** — relief from judgment (vacation)

Evidence Rules (**ER**) apply in both superior and district court.

See `references/civil-rules.md` for rule-by-rule coverage and
`references/evidence-rules.md` for ER 602/801–803/901–902/1002.

## Fees and costs

**RCW 4.84** — the costs and fees chapter. Recovery mechanisms:

- § 4.84.010 — prevailing-party costs
- § 4.84.030 — prevailing defendant
- § 4.84.080 — statutory attorney fee
- § 4.84.185 — frivolous-actions fee
- § 4.84.250–.300 — actions under $10,000 (attorney-fee
  recovery mechanism often critical in KCDC cases)
- § 4.84.330 — reciprocal fee-shifting for one-sided contract
  clauses (*Mellor v. Chamberlin*)

Rule-based fee-shifting:

- **CR 37(a)(5)** / **CRLJ 37(a)(4)** — mandatory fee-shifting
  to the prevailing party on a motion to compel, unless one of
  the enumerated exceptions applies
- **CR 11** — sanctions for frivolous or unsigned filings
- **CR 68** — offer-of-judgment cost-shifting

See `references/fees-and-costs.md` for full coverage, the
lodestar method (*Bowers*), pro-se recovery limits, and
pleading templates.

## Local rules

Each superior court and district court maintains local rules
layered on top of the statewide CR / CRLJ:

- **KCLCR** — King County Local Rules (Superior Court):
  motion-practice rules, confirmation, working copies, remote
  hearings (KCLCR 43), summary judgment (KCLCR 56)
- **KCDCLCR** — King County District Court Local Rules:
  clerk-issued date, e-filing deadlines, motion scheduling

See `references/local-rules.md` for the full coverage, division
variation, and the interaction with GR 14 statewide formatting.

## Citation format

Washington uses the Washington Reporter of Decisions. Form for a
Washington case citation:

> *Smith v. Jones*, 123 Wn.2d 456, 789 P.2d 123 (1994)

Federal citations follow Bluebook. See
`references/citation-format.md` for patterns for Washington and
federal citations, parallel cites, short-form references, and
GR 14 compliance.

## Canonical online sources

`references/online-sources.md` is the AI-agent-friendly catalog
of canonical URLs for:

- Washington court rules (courts.wa.gov)
- RCW text (app.leg.wa.gov)
- eCFR (for federal regulations)
- Cornell LII (for U.S.C. sections)
- CourtListener and Google Scholar (for case law)
- KCSC and KCDC local procedural pages

The catalog is the **only approved fetch source** for verification
work. Per the plugin's safety policy, **WebFetch is the only
mechanism used** — no curl, wget, Python requests, or other
bypasses are permitted. See `wa-fact-check` for the per-filing
verification workflow.

## Key general-civil cases

`references/key-cases.md` catalogs the general-civil cases this
plugin relies on most — SJ burden (*Young*), SJ non-movant
favorable inferences (*Folsom*), reciprocal fee-shifting
(*Mellor*), lodestar (*Bowers*), American rule baseline
(*McCready*), CR 60 default-vacation (*Morin*, *White*).

**Subject-matter cases** — FDCPA, CPA, business-records foundation
in debt cases, chain-of-title — live alongside their subject-matter
bundle (e.g., `wa-consumer-debt/references/key-cases.md`).

## Notes

- These references are neutral summaries. They do not tell the
  user whether they win or lose.
- Always **shepardize or KeyCite** a case before citing — Washington
  case law has evolved on several doctrines (business-records
  foundation, CR 60, fee-shifting scope).
- For federal law, check the most recent Ninth Circuit opinion
  where controlling in federal court; WA state courts treat Ninth
  Circuit federal-statute interpretations as persuasive.
- **Before filing**, run `wa-fact-check` against the packet to
  catch fabricated, misquoted, or superseded citations.
