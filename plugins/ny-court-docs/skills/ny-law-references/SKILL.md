---
name: ny-law-references
description: >
  Matter-neutral reference catalog for New York civil
  practice. Triggers include 'CPLR rule', 'CPLR section',
  'New York civil rules', 'Guide to NY Evidence', 'NY
  evidence rules', '22 NYCRR', 'Uniform Civil Rules', 'New
  York Law Reports Style Manual', 'Tanbook citation', 'New
  York court system structure', 'NY court rules', 'find a
  CPLR cite', 'Bill McKinney Consolidated Laws', 'where do
  I find NY statutes'. Indexes the CPLR (Civil Practice Law
  and Rules), the Guide to NY Evidence (in lieu of a
  codified evidence code), the Uniform Civil Rules at 22
  NYCRR (Parts 202, 208, 210, 212), the New York Law
  Reports Style Manual (Tanbook), fees and costs (CPLR Art
  81–84 / 88 / 89), local rules for the flagship courts,
  online sources, and a key-cases reference. **Canonical
  reference corpora live in this skill's references/
  directory.**
version: 0.1.0
---

# New York Law References

> **NOT LEGAL ADVICE.** Reference catalog. Verify against
> current rules before relying.

## What lives here

This is the **canonical reference catalog** for New York
civil practice. Other `ny-*` skills cross-reference these
files rather than duplicating the content.

### Body files (state-curated)

- `references/civil-rules.md` — CPLR Article-by-Article
  summary (Articles 1–88)
- `references/evidence-rules.md` — Guide to NY Evidence
  topic index + selected CPLR Article 45 / 31 evidence
  provisions
- `references/uniform-civil-rules.md` — 22 NYCRR Part 202
  (Supreme/County), Part 208 (Civil Court of NYC), Part 210
  (City Courts), Part 212 (District Court)
- `references/citation-format.md` — Tanbook conventions
- `references/fees-and-costs.md` — CPLR Arts 81–89 fee
  shifting
- `references/local-rules.md` — flagship-court Part Rules
  and the Commercial Division Rules (22 NYCRR § 202.70)
- `references/key-cases.md` — general-civil controlling
  precedents
- `references/online-sources.md` — canonical URLs catalog
- `references/legal-data-apis.md` — programmatic-access index

### Reference corpora (verbatim text — populated by future
pull scripts)

- `references/court-rules/` — 22 NYCRR (Uniform Rules) +
  CPLR text + Commercial Division Rules
- `references/federal-debt-laws/` *(symlink)* — points into
  the shared `claude-legal-federal-laws` plugin
- `references/ucc-model/` *(symlink)* — points into the
  shared plugin
- `references/ny-statutes-debt/` — N.Y. CPLR, N.Y. Gen. Bus.
  Law, N.Y. Gen. Oblig. Law, N.Y. Real Prop. Acts. Law, N.Y.
  Real Prop. Law, N.Y. Banking Law, N.Y. UCC (Article 9
  enacted at N.Y. UCC §§ 9-101 to 9-809) — relevant chapters

## CPLR at a glance

The **Civil Practice Law and Rules (CPLR)** is New York's
master civil-procedure statute. Notable architecture:

| Article | Subject |
|---------|---------|
| 1 | Short title; application |
| 2 | Limitations of time |
| 3 | Jurisdiction and service, appearance and choice of court |
| 4 | Special proceedings |
| 5 | Venue |
| 6 | Joinder of claims, consolidation and severance |
| 7 | Parties generally |
| 8 | Costs |
| 9 | Class actions |
| 10 | Parties generally — substitution |
| 21 | Papers |
| 22 | Stays, motions, orders and mandates |
| 23 | Subpoenas, oaths and affirmations |
| 30 | Remedies and pleading |
| 31 | Disclosure |
| 32 | Accelerated judgment |
| 40 | Trial generally |
| 41 | Trial by a jury |
| 42 | Trial by the court |
| 43 | Trial by referee |
| 44 | Trial motions |
| 45 | Evidence |
| 50 | Judgments generally |
| 51 | Enforcement of judgments |
| 52 | Enforcement of money judgments |
| 53 | Recognition of foreign country money judgments |
| 54 | Enforcement of judgments entitled to full faith and credit |
| 55 | Appeals generally |
| 56 | Appeals to the court of appeals |
| 57 | Appeals to the appellate division |
| 58 | Appellate division terms |
| 62 | Attachment |
| 63 | Injunction |
| 64 | Receivership |
| 65 | Notice of pendency |
| 70 | Habeas corpus |
| 71 | Action to recover a chattel |
| 72 | Action concerning a will |
| 75 | Arbitration |
| 76 | Special proceeding to enforce statutory right |
| 77 | Special proceeding relating to express trust |
| 78 | Proceeding against body or officer |
| 81 | Costs generally |
| 82 | Amount of costs |
| 83 | Allowance of costs |
| 84 | Taxation of costs |
| 85 | Indemnity for costs |
| 86 | Disbursements |
| 87 | Security for costs |
| 88 | Fees |
| 89 | Poor persons |

## Evidence — Guide to NY Evidence

New York does **not** have a codified evidence code. Instead,
evidence rules live across:

1. **Common-law decisional rules** — extensive case law
   ("Stigemeier" hearsay rules, "Holiday" past-recollection-
   recorded, etc.)
2. **CPLR Article 45** — selected codified evidence
   provisions (4504 physician-patient privilege, 4518
   business records, 4521 government records, 4533
   authentication of writings, 4544 small-print contracts,
   4545 collateral source)
3. **Guide to NY Evidence** — non-codified but authoritative
   secondary source published by the NY Unified Court
   System Evidence Guide Committee, available at
   nycourts.gov/judges/evidence

The Guide is organized in eleven articles mirroring the
Federal Rules of Evidence numbering:

- Art 1: General Provisions (1.00–1.13)
- Art 2: Judicial Notice (2.00–2.05)
- Art 3: Presumptions
- Art 4: Relevance and Limits (4.00–4.27)
- Art 5: Privileges
- Art 6: Witnesses
- Art 7: Opinions and Expert Testimony
- Art 8: Hearsay
- Art 9: Authentication and Identification
- Art 10: Best Evidence Rule
- Art 11: Miscellaneous

## Citation format — Tanbook quick reference

- **Court of Appeals**: `Roe v. Doe, 1 NY3d 100, 105 (2003)`
- **Appellate Division**: `Smith v. Jones, 50 AD3d 200,
  201 (1st Dept 2008)`
- **Misc. Reports (trial level)**: `Roe v. Doe, 15 Misc 3d
  100 (Sup Ct, NY County 2007)`
- **Reporter abbreviations**: no periods (NY, NYS, AD, Misc)
- **Statutes**: `CPLR 3211(a)(7)` — no "N.Y." prefix; in
  body text use the section number only
- **Session laws**: `L 2021, ch 593`
- **Pinpoint cite**: `at 105` (no "p.")

## Composition with other ny- skills

This skill is matter-neutral and **referenced by all other
ny-* skills**. When a downstream skill needs the
authoritative text of a CPLR section, an evidence rule, a
22 NYCRR provision, or a Tanbook convention, it cites or
links into this skill's `references/` tree.
