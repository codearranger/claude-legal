# Evals — Skill Regression Tests (Indiana)

This folder contains prompt-based regression tests for each
skill in the `in-court-docs` plugin. Each eval specifies a
natural-language prompt, the skills expected to activate,
acceptance criteria organized into logical sections, and
the most common failure modes.

**22 evals across five categories** mirror the CO / AZ / TN
peer baselines.

## Folder layout

- `drafting/` — document-drafting skill evals
- `formatting/` — caption, format, and local-rule evals
- `procedural/` — matter-neutral civil-procedure evals
- `subject-matter/` — subject-bundle evals (consumer debt,
  family law, CHINS/protection orders, UCCJEA)
- `integration/` — end-to-end multi-skill evals

## Coverage map

### drafting/ (5 evals)

| File | Skill(s) exercised | Indiana distinctive |
|---|---|---|
| `motion-summary-judgment.md` | `in-draft-motion`, `in-consumer-debt`, `in-statewide-format`, `in-pro-se` | *Jarboe* affirmative-negation burden; Indiana rejects *Celotex*; proposed order required in Marion |
| `motion-to-correct-error.md` | `in-draft-motion`, `in-post-judgment`, `in-statewide-format` | T.R. 59 post-trial motion; 30-day jurisdictional deadline; required for some appeals |
| `declaration-affidavit.md` | `in-draft-declaration`, `in-statewide-format`, `in-pro-se` | T.R. 11(B) "I affirm, under the penalties for perjury" — no California / federal language |
| `notice-of-hearing.md` | `in-draft-note`, `in-lake`, `in-statewide-format` | Indiana "Notice of Hearing" (not a Note for Motion Calendar); court issues the setting |
| `proposed-order.md` | `in-draft-order`, `in-marion`, `in-submit-order`, `in-statewide-format` | Marion every-motion proposed-order requirement; findings + ordering clause; Odyssey transmittal |

### formatting/ (4 evals)

| File | Skill(s) exercised | Indiana distinctive |
|---|---|---|
| `statewide-format.md` | `in-statewide-format`, `in-pro-se` | T.R. 5(E) margins / font; T.R. 10(A) `)` chain caption; T.R. 10(B) numbered paragraphs; 2-inch top margin for Odyssey |
| `marion-caption.md` | `in-marion`, `in-statewide-format`, `in-file-packet` | Marion 49Dxx cause-number encoding; random Odyssey assignment; CPC case management; proposed order requirement |
| `pro-se.md` | `in-pro-se`, `in-statewide-format`, `in-marion` | *Goossens* equal-standards doctrine; T.R. 3.1 Appearance; IC 33-37-3-2 fee waiver; Odyssey optional for pro se |
| `quality-check.md` | `in-quality-check`, `in-fact-check`, `in-statewide-format` | Two-pass: T.R. 5(E) + T.R. 10 format check, then citation verification; 2-inch top-margin check |

### procedural/ (5 evals)

| File | Skill(s) exercised | Indiana distinctive |
|---|---|---|
| `first-30-days.md` | `in-first-30-days`, `in-deadlines`, `in-statewide-format` | 20-day answer (not 30/21); T.R. 6(E) mail extension abolished 2009; T.R. 8(C) affirmative-defense waiver |
| `deadlines.md` | `in-deadlines` | T.R. 6(A) computation; no mail extension; Good Friday; even-year Election Day closures; T.R. 59 30-day jurisdictional |
| `discovery.md` | `in-discovery`, `in-draft-motion`, `in-deadlines` | 25-interrogatory cap (T.R. 33(A)); no initial disclosures; pre-2015 broad scope; T.R. 37(E) meet-and-confer |
| `post-judgment.md` | `in-post-judgment`, `in-deadlines` | T.R. 59 / T.R. 60(B) interplay; 25% wage-garnishment cap; IC 34-55-10 exemptions; T.R. 69 supplemental |
| `file-packet.md` | `in-file-packet`, `in-statewide-format` | Odyssey unified statewide e-filing; PDF only; document codes; auto-service of registered contacts; PII redaction |

### subject-matter/ (6 evals)

| File | Skill(s) exercised | Indiana distinctive |
|---|---|---|
| `motion-summary-judgment.md` *(in drafting/)* | see above | *Jarboe* SJ standard |
| `family-law-child-support-guidelines.md` | `in-family-law` | Income-shares Guidelines; Worksheet A/B; combined-income cap |
| `family-law-dissolution-equitable-distribution.md` | `in-family-law`, `in-family-court` | IC 31-15-7 rebuttable presumption of equal division; equitable distribution (not community property) |
| `paternity-jp-case.md` | `in-family-law`, `in-family-court` | IC 31-14 JP case type; biological-mother presumption; genetic-testing threshold |
| `consumer-debt-dcsa-fdcpa.md` | `in-consumer-debt`, `in-first-30-days` | No state licensing; FDCPA § 1692i wrong-venue; DCSA treble damages + 30-day cure demand |
| `chins-protection-order.md` | `in-family-law`, `in-family-court` | CHINS IC 31-34 (DCS initiates); IC 34-26-5 ex parte TPO; T.R. 11(B) verified petition |
| `uccjea-jurisdiction.md` | `in-family-law`, `in-family-court`, `in-county-courts` | IC 31-21 home-state / ICC analysis; Bartholomew Circuit Court consolidated jurisdiction |

### integration/ (2 evals)

| File | Skills exercised | Scenario |
|---|---|---|
| `debt-defense-end-to-end.md` | `in-first-30-days`, `in-consumer-debt`, `in-discovery`, `in-draft-motion`, `in-statewide-format`, `in-marion`, `in-fact-check` | Debt-buyer suit in Marion Superior — answer through T.R. 56 summary judgment |
| `family-law-paternity-intake.md` | `in-family-law`, `in-family-court`, `in-lake`, `in-pro-se`, `in-statewide-format`, `in-deadlines` | JP case for unmarried father in Lake County — paternity through child support |

## Authoring conventions

- **Corpus-first**: every legal number (day counts, dollar
  thresholds, percentage caps, factor enumerations) must
  be backed by `reads the current [X] from the references
  corpus` rather than asserted as a fixed value from memory.
- **Indiana authority**: cite T.R. / IC / case names (N.E.3d
  reporter); flag when a case cite must be verified against
  `key-cases.md` or CourtListener.
- **Indiana-distinctive markers**: the *Jarboe* SJ standard,
  the abolished T.R. 6(E) mail extension, Good Friday and
  Election Day closures, Bartholomew consolidated jurisdiction,
  no state collection-agency licensing, the DCSA 30-day cure
  demand, and the T.R. 59 jurisdictional post-trial deadline
  are the most common regression failure modes — each is
  called out in the relevant eval's "Common failure modes."
- **Honest failure modes**: each eval lists the most likely
  wrong answers to catch regressions.
- **Format mirror**: every eval follows the
  `## Prompt` / `## Expected triggers` /
  `## Acceptance criteria` / `## Common failure modes`
  structure of the CO / AZ / TN peers.
