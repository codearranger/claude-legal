# Evals — Skill Regression Tests (Georgia)

This folder contains prompt-based regression tests for the
skills in the `ga-court-docs` plugin. Each eval specifies a
natural-language Georgia pro se scenario, the skills expected
to activate, acceptance criteria organized into logical
sections, and the most common failure modes.

**21 evals across five categories.**

## Folder layout

- `drafting/` — document-drafting skill evals
- `formatting/` — caption, format, and county-specific evals
- `procedural/` — matter-neutral civil-procedure evals
- `subject-matter/` — subject-bundle evals (consumer debt,
  family law)
- `integration/` — end-to-end multi-skill evals

## Coverage map

### drafting/ (4 evals)

| File | Skill(s) exercised | Georgia distinctive |
|---|---|---|
| `motion.md` | `ga-draft-motion`, `ga-discovery` | O.C.G.A. § 9-11-7 motion; Rule Nisi hearing (USCR 6.3/6.4) |
| `declaration.md` | `ga-draft-declaration` | Notarized affidavit + § 9-11-56(e) personal knowledge |
| `notice-of-hearing.md` | `ga-draft-note`, `ga-schedule-hearing` | Rule Nisi — court sets the date, no self-calendaring |
| `proposed-order.md` | `ga-draft-order`, `ga-submit-order` | Separated findings/ordering clause; consent-order path |

### formatting/ (4 evals)

| File | Skill(s) exercised | Georgia distinctive |
|---|---|---|
| `statewide-format.md` | `ga-statewide-format`, `ga-pro-se` | No statewide pleading-paper rule; § 9-11-10 caption; "Civil Action File No." |
| `cobb-caption.md` | `ga-cobb`, `ga-file-packet` | "SUPERIOR/STATE COURT OF COBB COUNTY / STATE OF GEORGIA"; PeachCourt |
| `pro-se.md` | `ga-pro-se`, `ga-statewide-format` | Pro Se block (no Bar No.); poverty affidavit (§ 9-15-2) |
| `quality-check.md` | `ga-quality-check`, `ga-fact-check` | Pre-filing format + citation QC; official reporters (Rule 22) |

### procedural/ (6 evals)

| File | Skill(s) exercised | Georgia distinctive |
|---|---|---|
| `law-references.md` | `ga-law-references` | Corpus map; federal symlinks; Ga./Ga. App. reporters |
| `deadlines.md` | `ga-deadlines` | § 9-11-6(a)/§ 1-3-1(d)(3); § 1-4-1 holidays (Juneteenth + Columbus Day) |
| `discovery.md` | `ga-discovery`, `ga-draft-motion` | § 9-11-33 interrogatory cap; § 9-11-36 deemed admissions; USCR 5 six-month period |
| `fact-check.md` | `ga-fact-check`, `ga-quality-check` | Citation verification; *Hill* pin-cite caution |
| `first-30-days.md` | `ga-first-30-days`, `ga-deadlines` | 30-day answer (§ 9-11-12); State Court forum; § 9-11-13 compulsory counterclaim |
| `file-packet.md` | `ga-file-packet`, `ga-pro-se` | PeachCourt vs Odyssey eFileGA by county; poverty affidavit |

### subject-matter/ (5 evals)

| File | Skill(s) exercised | Georgia distinctive |
|---|---|---|
| `consumer-debt-fact-pattern.md` | `ga-consumer-debt` | FBPA (§ 10-1-390 et seq.) as state vehicle; no collector licensing; § 10-1-399(b) demand |
| `debt-buyer-chain-of-title.md` | `ga-consumer-debt`, `ga-draft-motion` | *Nyankojo* / *Wirth* / *Rutledge*; § 24-8-803(6) business records |
| `credit-card-sol.md` | `ga-consumer-debt` | 6-year written-contract SOL (§ 9-3-24, *Hill v. American Express*) not 4-year open account (§ 9-3-25) |
| `family-law-dissolution.md` | `ga-family-law`, `ga-family-court` | Superior-Court-exclusive; equitable distribution (*Stokes*); § 19-9-3 child election |
| `child-support-income-shares.md` | `ga-family-law` | Income-shares worksheet (§ 19-6-15, revised eff. 1/1/2026) |

### integration/ (2 evals)

| File | Skills exercised | Scenario |
|---|---|---|
| `debt-defense-end-to-end.md` | `ga-first-30-days`, `ga-consumer-debt`, `ga-discovery`, `ga-draft-motion`, `ga-statewide-format`, `ga-fact-check` | Debt-buyer suit in State Court of Cobb County — answer through summary judgment |
| `divorce-intake.md` | `ga-family-law`, `ga-family-court`, `ga-deadlines`, `ga-file-packet`, `ga-statewide-format` | Cobb County dissolution with minor children — filing through decree |

## Authoring conventions

- **Corpus-first**: every drift-prone legal number (day
  counts, dollar thresholds, percentage caps, the post-2026
  child-support figures) must be backed by
  `reads the current [X] from the references corpus` rather
  than asserted as a fixed value. Statutory limitations
  periods that are stable (the § 9-3-24 6-year and § 9-3-25
  4-year SOLs) may be cited directly.
- **Georgia authority**: cite O.C.G.A. / USCR sections and
  the verified Georgia cases (*Lau's Corp.*, *Hill v.
  American Express*, *Nyankojo*, *Wirth*, *Rutledge*,
  *Stokes v. Stokes*); flag that case cites must be verified
  against `key-cases.md` or CourtListener and use the
  official Ga. / Ga. App. + S.E.2d reporters (Ga. Sup. Ct.
  Rule 22).
- **Honest failure modes**: each eval lists the most likely
  wrong answers to catch regressions (e.g., the 4-year SOL
  trap, the State-vs-Superior forum confusion, PeachCourt vs
  Odyssey by county).
- **Format mirror**: every eval follows the `## Prompt` /
  `## Expected triggers` / `## Acceptance criteria` /
  `## Common failure modes` structure.
