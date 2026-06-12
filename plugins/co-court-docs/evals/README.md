# Evals — Skill Regression Tests (Colorado)

This folder contains prompt-based regression tests for each
skill in the `co-court-docs` plugin. Each eval specifies a
natural-language prompt, the skills expected to activate,
acceptance criteria organized into logical sections, and
the most common failure modes.

**22 evals across five categories** mirror the OR / WA /
AZ / TN peer baselines.

## Folder layout

- `drafting/` — document-drafting skill evals
- `formatting/` — caption, format, and local-rule evals
- `procedural/` — matter-neutral civil-procedure evals
- `subject-matter/` — subject-bundle evals (consumer debt,
  family law, post-judgment, county court)
- `integration/` — end-to-end multi-skill evals

## Coverage map

### drafting/ (5 evals)

| File | Skill(s) exercised | Colorado distinctive |
|---|---|---|
| `declaration.md` | `co-draft-declaration` | C.R.S. § 13-27-104 unsworn declaration; no notary |
| `motion-to-compel.md` | `co-draft-motion`, `co-discovery` | C.R.C.P. 121 § 1-15(8) Certificate of Conferral |
| `notice-of-setting.md` | `co-draft-note`, `co-schedule-hearing` | Court issues Notice of Setting; party-filed variants |
| `motion-for-summary-judgment.md` | `co-draft-motion`, `co-fact-check` | C.R.C.P. 56 + *Warne v. Hall*; no conferral on dispositive motions |
| `proposed-order.md` | `co-draft-order`, `co-submit-order` | Word-format chambers transmittal; separated findings/ordering clause |

### formatting/ (4 evals)

| File | Skill(s) exercised | Colorado distinctive |
|---|---|---|
| `statewide-format.md` | `co-statewide-format`, `co-pro-se` | C.R.C.P. 10 + CJD 11-01 two-block caption with COURT USE ONLY box |
| `denver-caption.md` | `co-denver`, `co-file-packet` | Denver 2nd JD specifics; CCEFS document codes |
| `pro-se.md` | `co-pro-se`, `co-statewide-format` | JDF forms; CCEFS Pro Se; JDF 205/206 fee waiver |
| `quality-check.md` | `co-quality-check`, `co-fact-check` | Parker four-part framework; C.R.C.P. 121 page-limit check |

### procedural/ (5 evals)

| File | Skill(s) exercised | Colorado distinctive |
|---|---|---|
| `first-30-days.md` | `co-first-30-days`, `co-deadlines` | 21-day answer; *Warne v. Hall* plausibility; waiver of affirmative defenses |
| `deadlines.md` | `co-deadlines` | C.R.C.P. 6(a) + Cabrini Day + Juneteenth; mail add-on |
| `discovery.md` | `co-discovery`, `co-draft-motion` | 25-interrogatory cap; C.R.C.P. 311 county-court distinction |
| `file-packet.md` | `co-file-packet`, `co-pro-se` | CCEFS upload; document codes; JDF 205/206 |
| `fact-check.md` | `co-fact-check`, `co-quality-check` | Four-pass framework; Colorado neutral-citation format |

### subject-matter/ (6 evals)

| File | Skill(s) exercised | Colorado distinctive |
|---|---|---|
| `consumer-debt-cfdcpa.md` | `co-consumer-debt` | CFDCPA (Title 5 recodification); CCPA treble damages; licensure |
| `debt-buyer-chain-of-title.md` | `co-consumer-debt`, `co-draft-motion` | UCC Art. 9 assignment; C.R.E. 803(6); *Hassler v. Account Brokers* 6-yr SOL |
| `family-law-dissolution.md` | `co-family-law` | UDMA equitable distribution; 91-day wait; C.R.C.P. 16.2 JDF 1111 |
| `child-support-93-overnight.md` | `co-family-law` | C.R.S. § 14-10-115; 93-overnight shared-care rule; JDF 1820 E |
| `common-law-marriage.md` | `co-family-law` | *Hogsett & Neale* 2021 CO 1 totality-of-circumstances test |
| `post-judgment-garnishment.md` | `co-post-judgment` | C.R.S. § 13-54.5; SB22-086 expanded exemptions ($250k homestead) |
| `county-court-small-claims.md` | `co-county-courts` | C.R.C.P. 311 simplified procedure; small-claims C.R.C.P. 501–521 |

### integration/ (2 evals)

| File | Skills exercised | Scenario |
|---|---|---|
| `debt-defense-end-to-end.md` | `co-first-30-days`, `co-consumer-debt`, `co-discovery`, `co-draft-motion`, `co-statewide-format`, `co-fact-check` | Debt-buyer suit in district court — answer through summary judgment |
| `divorce-intake.md` | `co-family-law`, `co-deadlines`, `co-file-packet`, `co-statewide-format` | Dissolution with minor children — filing through decree |

## Authoring conventions

- **Corpus-first**: every legal number (day counts, dollar
  thresholds, percentage caps) must be backed by
  `reads the current [X] from the references corpus`
  rather than asserted as a fixed value from memory.
- **Colorado authority**: cite C.R.C.P. / C.R.S. / case
  names; flag when a case cite must be verified against
  `key-cases.md` or CourtListener.
- **Honest failure modes**: each eval lists the most likely
  wrong answers to catch regressions.
- **Format mirror**: every eval follows the
  `## Prompt` / `## Expected triggers` /
  `## Acceptance criteria` / `## Common failure modes`
  structure of the WA / OR / AZ / TN peers.
