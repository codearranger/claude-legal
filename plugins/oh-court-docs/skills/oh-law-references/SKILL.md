---
name: oh-law-references
description: >
  Use to look up Ohio civil-procedure rules (Civ. R.), evidence rules (Evid. R.), Rules of Superintendence, Rules of Professional Conduct, statutes (R.C.), and citation format. Triggers include 'Ohio Civ. R.', 'Ohio Evid. R.', 'Ohio Revised Code', 'R.C. lookup', 'Ohio Sup. R.', 'Ohio Prof. Cond. R.', 'Ohio public-domain citation', 'codes.ohio.gov', 'Ohio rule of court'. Canonical reference corpora for the plugin live in this skill's references/ directory.
version: 0.5.0
---

# Ohio Law References

> **NOT LEGAL ADVICE.** Verify against the current
> authoritative source before relying on any reference here.

This skill is the canonical reference host for the Ohio
plugin. Verbatim text of every major Ohio rule of court +
20 R.C. chapters lives under `references/`.

## What's in references/

### `court-rules/` — 14 rule sets verbatim

Pulled from `supremecourt.ohio.gov` by
`scripts/pull_ohio_court_rules.py`:

- **CivilProcedure.md** — Ohio Rules of Civil Procedure
  (Civ. R.) — the FRCP-style framework that governs all
  Common Pleas civil practice
- **Evidence.md** — Ohio Rules of Evidence (Evid. R.)
- **AppellateProcedure.md** — Ohio Rules of Appellate
  Procedure (App. R.) — including the 30-day notice-of-
  appeal clock at App. R. 4(A)
- **CriminalProcedure.md** — Crim. R. (referenced by some
  consumer-debt actions involving check kiting / theft)
- **JuvenileProcedure.md** — Juv. R. (Juvenile Division
  of Common Pleas)
- **Traffic.md** — Traffic Rules (Municipal Court traffic
  practice)
- **Superintendence.md** — Sup. R. — chambers practice +
  case-management standards + records management
- **RulesOfPractice.md** — Ohio Supreme Court's own
  practice rules
- **ProfessionalConduct.md** — Prof. Cond. R. — Ohio's
  attorney-conduct rules
- **JudicialConduct.md** — Code of Judicial Conduct
- **GovBar.md** — Government of the Bar (lawyer
  registration, fee dispute resolution, attorney discipline)
- **GovJud.md** — Government of the Judiciary
- **Reporting.md** — Rules of Reporting (court reporters)
- **CourtOfClaims.md** — Court of Claims local rules

### `oh-statutes-debt/` — 20 R.C. chapters verbatim

Pulled from `codes.ohio.gov` by
`scripts/pull_ohio_statutes.py`:

- **Chapter 1** — Definitions including R.C. 1.14 legal
  holidays + R.C. 1.45 time computation
- **Chapter 1302** — UCC Article 2 (Sales)
- **Chapter 1303** — UCC Article 3 (Negotiable Instruments)
- **Chapter 1309** — UCC Article 9 (Secured Transactions)
- **Chapter 1345** — Consumer Sales Practices Act (CSPA)
- **Chapter 1901** — Municipal Court Act
- **Chapter 1907** — County Court Act
- **Chapter 1923** — Forcible Entry and Detainer (eviction)
- **Chapter 1925** — Small Claims Division
- **Chapter 2151** — Juvenile Court
- **Chapter 2305** — Statutes of Limitations + General Civil
  Procedure
- **Chapter 2329** — Execution of Judgments + Exemptions
- **Chapter 2333** — Aid of Execution + Debtor's Exam
- **Chapter 3105** — Divorce, Annulment, Legal Separation
- **Chapter 3109** — Children — Custody, Parenting, Support
- **Chapter 3113** — Support Enforcement
- **Chapter 3115** — UIFSA
- **Chapter 3119** — Child Support Guidelines
- **Chapter 3127** — UCCJEA
- **Chapter 5321** — Residential Landlord-Tenant Act

### Symlinks into shared federal corpus

- `federal-debt-laws/` — FDCPA, FCRA, TILA, ECOA, Reg B/F/V/Z,
  RESPA, SCRA, FHA, TSR
- `federal-bankruptcy/` — 11 U.S.C. Chapters 1, 3, 5, 7, 11,
  12, 13, 15
- `ucc-model/` — Model UCC Articles 1, 2, 3, 9

## Online sources (canonical URLs)

- **Ohio Supreme Court** — `supremecourt.ohio.gov`
- **Ohio Revised Code** — `codes.ohio.gov/ohio-revised-code/`
- **Ohio Court of Claims** — `ohiocourtofclaims.gov`
- **Ohio Bar Association attorney lookup** —
  `ohiobar.org/about-the-osba/find-a-lawyer/`

## Composition with other oh- skills

Every other oh- skill cross-references this one when it
needs a verbatim rule or statute. The pullers refresh the
corpus quarterly via `.github/workflows/refresh-references.yml`.
