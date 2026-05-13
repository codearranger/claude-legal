# Federal Debt Laws — California Plugin Pointer

This directory mirrors the federal debt-law corpus from the
Washington plugin (`wa-court-docs`). Federal law applies
identically across state lines, so the substantive content
does not change between the WA, OR, and CA plugins.

## What lives here when fully populated

| Statute / Regulation | File | Source | USC / CFR Citation |
|----------------------|------|--------|--------------------|
| FDCPA | `FDCPA.md` | uscode.house.gov | 15 U.S.C. §§ 1692-1692p |
| FCRA | `FCRA.md` | uscode.house.gov | 15 U.S.C. §§ 1681-1681x |
| TILA | `TILA.md` | uscode.house.gov | 15 U.S.C. §§ 1601-1667f |
| ECOA | `ECOA.md` | uscode.house.gov | 15 U.S.C. §§ 1691-1691f |
| Reg F (FDCPA implementing) | `Reg-F.md` | ecfr.gov | 12 C.F.R. pt. 1006 |
| Reg V (FCRA implementing) | `Reg-V.md` | ecfr.gov | 12 C.F.R. pt. 1022 |
| Reg Z (TILA implementing) | `Reg-Z.md` | ecfr.gov | 12 C.F.R. pt. 1026 |
| Reg B (ECOA implementing) | `Reg-B.md` | ecfr.gov | 12 C.F.R. pt. 1002 |

## Statute summaries

### FDCPA — Fair Debt Collection Practices Act

**15 U.S.C. §§ 1692-1692p** (Title VIII of the Consumer Credit
Protection Act). Enacted 1977; significantly amended by the
Dodd-Frank Act (2010).

Key provisions:
- **§ 1692a** — Definitions: "debt collector" (anyone who
  regularly collects debts owed to another); "debt" (personal,
  family, or household purposes); "consumer" (natural person)
- **§ 1692b** — Communication with third parties to acquire
  location information
- **§ 1692c** — Communication restrictions: time/place limits
  (8 a.m.–9 p.m.); prohibition on contact after attorney
  representation; ceasing communication after written
  request
- **§ 1692d** — Harassment or abuse: harassing calls,
  obscene language, threats of violence
- **§ 1692e** — False or misleading representations: the
  broadest prohibition; includes false representation of
  amount, false threat of suit, false representation of
  legal status
- **§ 1692f** — Unfair practices: collecting amounts not
  authorized; cashing postdated checks; removing property
- **§ 1692g** — Validation of debts: 30-day notice required
  at initial communication; written dispute triggers
  verification obligation
- **§ 1692i** — Venue for legal actions: suit must be brought
  in the judicial district where the consumer signed the
  contract or resides
- **§ 1692k** — Civil liability: actual damages; statutory
  damages up to $1,000 per action; attorney fees mandatory
  for prevailing consumer; class action damages capped at
  $500,000 or 1% of net worth

**Reg F** (12 C.F.R. pt. 1006, effective November 30, 2021):
CFPB's implementing regulation. Key additions: electronic
communication rules (email, text), validation notice safe
harbor, convenience fee prohibition.

### FCRA — Fair Credit Reporting Act

**15 U.S.C. §§ 1681-1681x** (Title VI of the Consumer Credit
Protection Act). Governs consumer reporting agencies (CRAs),
furnishers of credit information, and users of credit reports.

Key provisions:
- **§ 1681b** — Permissible purposes for obtaining a
  consumer report
- **§ 1681i** — Reinvestigation of disputed information
- **§ 1681n** — Civil liability for willful noncompliance
  (actual damages, punitive damages, fees)
- **§ 1681o** — Civil liability for negligent noncompliance
  (actual damages, fees)
- **§ 1681s-2** — Furnisher obligations: accuracy, correction
  upon notice of dispute

**Reg V** (12 C.F.R. pt. 1022): CFPB's implementing regulation.

### TILA — Truth in Lending Act

**15 U.S.C. §§ 1601-1667f** (Title I of the Consumer Credit
Protection Act). Governs disclosure requirements for consumer
credit transactions.

Key provisions:
- **§ 1637** — Open-end consumer credit plans (credit cards)
- **§ 1640** — Civil liability: actual damages; statutory
  damages (twice the finance charge, $500 min, $5,000 max);
  fees for prevailing consumer
- **§ 1641** — Assignee liability: purchasers of credit
  instruments are subject to claims that could have been
  raised against the original creditor

**Reg Z** (12 C.F.R. pt. 1026): CFPB's comprehensive TILA
implementing regulation.

### ECOA — Equal Credit Opportunity Act

**15 U.S.C. §§ 1691-1691f** (Title VII of the Consumer Credit
Protection Act). Prohibits discrimination in credit transactions
on the basis of race, color, religion, national origin, sex,
marital status, age, or receipt of public assistance.

Key provisions:
- **§ 1691(a)** — General prohibition on discrimination
- **§ 1691(d)** — Notice of adverse action required
- **§ 1691e** — Civil liability: actual damages, punitive
  damages; fees for prevailing plaintiff

**Reg B** (12 C.F.R. pt. 1002): CFPB's implementing regulation.

## How to populate

Re-use the existing WA plugin script:

```bash
python3 scripts/pull_federal_debt_laws.py \
  --output plugins/ca-court-docs/skills/ca-law-references/references/federal-debt-laws/
```

The script extracts USLM XML and eCFR XML and writes Markdown
with verbatim text and citation tables.

## Cross-references

- `../ca-statutes-debt/README.md` — California state
  debt-collection statutes (Rosenthal, UCL, CLRA, FDBPA)
- `../online-sources.md` — canonical URLs for federal law
- `../legal-data-apis.md` — programmatic access (USLM XML,
  eCFR Versioner API)
- `../../ca-consumer-debt/` — California consumer-debt
  subject-matter bundle

## Status

Empty in the initial PR — only this README. The first
`pull_federal_debt_laws.py` run will populate.

## California-specific notes

Federal consumer protection laws operate in California courts
alongside more protective California state analogs:

- **FDCPA + Rosenthal FDCPA** (Civ. Code §§ 1788-1788.33):
  California's Rosenthal Act applies FDCPA standards to
  original creditors — broader than the federal FDCPA, which
  applies only to third-party debt collectors. Claims are
  often pleaded in parallel.
- **FCRA + California Consumer Credit Reporting Agencies Act**
  (Civ. Code §§ 1785.1-1785.36): California's state analog
  covers the same ground and provides broader protections in
  some areas.
- **TILA + California Department of Financial Protection and
  Innovation (DFPI) consumer lending rules**: California
  has additional disclosure requirements at the state level.
- **ECOA + California Fair Employment and Housing Act (FEHA)
  + Unruh Civil Rights Act**: Federal and state anti-
  discrimination frameworks operate in parallel.

The 9th Circuit interprets these federal statutes for federal
purposes; California state courts give Ninth Circuit
interpretations **persuasive weight** but are not bound by
them. California courts may interpret state analogs more
broadly than their federal counterparts.
