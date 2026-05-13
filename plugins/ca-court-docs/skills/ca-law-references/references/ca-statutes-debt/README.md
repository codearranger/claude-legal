# California Statutes — Debt-Relevant Chapters Corpus

This directory holds verbatim text of the California statutory
provisions most relevant to consumer-debt defense, civil
collection, and general civil practice in California. Contents
are pulled from **https://leginfo.legislature.ca.gov/** via the
quarterly `scripts/pull_ca_statutes.py` agent routine (to be
created).

## Statutes and code sections covered

| Code / Chapter | Subject | File | Update cycle |
|----------------|---------|------|--------------|
| CCP §§ 337, 337a | 4-year SOL on written contract | `CCP-SOL.md` | Quarterly |
| CCP § 339 | 2-year SOL on oral contract | `CCP-SOL.md` | Quarterly |
| CCP §§ 412.20-417.40 | Service of process | `CCP-Service.md` | Quarterly |
| CCP §§ 1010-1020 | Notices and motions | `CCP-Motions.md` | Quarterly |
| CCP § 437c | Summary judgment | `CCP-437c.md` | Quarterly |
| CCP §§ 2016.010-2036.050 | Civil Discovery Act | `CCP-Discovery.md` | Quarterly |
| CCP §§ 683.010-708.320 | Enforcement of judgments | `CCP-Enforcement.md` | Quarterly |
| Civ. Code §§ 1788-1788.33 | Rosenthal Act | `Rosenthal.md` | Quarterly |
| Fin. Code §§ 100000-100027 | CA Debt Collection Licensing Act | `DCLA.md` | Quarterly |
| Bus. & Prof. Code §§ 17200-17210 | UCL | `UCL.md` | Quarterly |
| Civ. Code §§ 1750-1784 | CLRA | `CLRA.md` | Quarterly |
| Civ. Code § 1788.50 et seq. | Fair Debt Buying Practices Act | `FDBPA.md` | Quarterly |
| Com. Code §§ 9101-9809 | UCC Article 9 (CA) | `CommCode-Art9.md` | Quarterly |

## Key sections by chapter

### CCP — Statutes of Limitations

- **CCP § 337** — 4-year statute of limitations for actions
  on a written contract or obligation. Applies to:
  - Actions on any contract, obligation, or liability founded
    upon an instrument in writing
  - Actions to recover on a book account (open book account)
  - Note: "written" includes electronically stored contracts
    and account agreements, but the SOL runs from breach, not
    from the date of last payment (though last payment may
    toll under the partial-payment rule)
- **CCP § 337a** — 4-year SOL on an account stated when
  reduced to writing (an account stated arises when the
  parties agree, expressly or impliedly, to the balance of
  an open account)
- **CCP § 339** — 2-year SOL for actions on an oral contract,
  obligation, or liability

**California debt SOL note**: The 4-year written-contract SOL
under § 337 applies to credit card agreements, which are
written (even when terms are mailed or posted online). Courts
have generally held that the SOL for a credit card debt begins
at the time of default (missed payment) or when the account
is closed due to nonpayment. A debt buyer cannot re-start the
SOL by sending a collection letter; partial payment may revive
the SOL under CCP § 360 (written acknowledgment or payment
before SOL expires).

### CCP — Service of Process

- **CCP § 412.20** — Required contents of summons
- **CCP § 413.10** — Methods of service: personal, substituted,
  mail with acknowledgment, publication
- **CCP § 415.10** — Personal service: delivering a copy to
  the person served
- **CCP § 415.20** — Substituted service: leaving with
  competent household member at dwelling plus mailing; or
  leaving with person apparently in charge at business plus
  mailing; service complete 10 days after mailing
- **CCP § 415.30** — Service by mail: person served must
  execute and return an acknowledgment of receipt; if not
  returned within 20 days, service may be completed by
  another method; costs of service may be assessed against
  party who unreasonably refused mail service
- **CCP § 416.10** — Service on a corporation: officers,
  registered agent, person in charge of office
- **CCP § 417.10** — Proof of service: must be filed; service
  by personal delivery is complete at delivery; by substituted
  service, complete 10 days after mailing

### CCP — Summary Judgment

- **CCP § 437c** — The California summary judgment statute.
  For detailed coverage, see `../civil-rules.md` and
  `CCP-437c.md` (when populated).
  - Burden-shifting framework per *Aguilar v. Atlantic
    Richfield Co.* (2001) 25 Cal.4th 826
  - Separate statement of undisputed material facts required
    (CRC 3.1350)
  - Opposition due 51 days before hearing; reply 21 days
  - Summary adjudication of individual issues available under
    § 437c(f)

### CCP — Civil Discovery Act

- **CCP § 2016.010-2016.070** — General provisions: scope,
  meet and confer, protective orders
- **CCP § 2019.010** — Methods of discovery: depositions,
  interrogatories, document production, physical/mental
  examinations, RFAs, expert discovery
- **CCP §§ 2030.010-2030.410** — Written interrogatories:
  form (DISC-001) and special interrogatories; responses
  in 30 days; objections must be specific
- **CCP §§ 2031.010-2031.510** — Document production:
  30-day response period; ESI rules (CCP § 2031.280)
- **CCP §§ 2033.010-2033.420** — RFAs: 30-day response;
  unanswered RFAs deemed admitted (§ 2033.280)
- **CCP §§ 2025.010-2025.620** — Oral depositions: 10-day
  notice; 7-hour limit; non-party subpoena required
- **CCP §§ 2023.010-2023.040** — Sanctions for misuse of
  discovery: monetary, issue, evidence, terminating,
  contempt

### CCP — Enforcement of Judgments

- **CCP § 683.020** — Judgment duration: 10 years; renewable
  by motion filed before expiration
- **CCP § 683.110** — Renewal of judgment: extends
  enforceability for 10 more years
- **CCP §§ 695.010-695.230** — Property subject to enforcement
- **CCP §§ 699.010-699.560** — Writ of execution: issued by
  court clerk; served on levying officer (sheriff)
- **CCP §§ 703.010-703.610** — Exemptions:
  - **§ 703.140** — Bankruptcy exemptions (federal opt-out)
  - **§ 704.010** — Homestead exemption: up to $300,000 or
    median sale price, whichever is greater (as of 2021)
  - **§ 704.070** — Vehicle exemption
  - **§ 704.080** — Tools of the trade
  - **§ 704.090** — Health aids
  - **§ 704.113** — Pension, annuity, retirement plans
  - **§ 704.210** — Wages: 25% of disposable earnings or
    50 times federal minimum wage, whichever is less
- **CCP §§ 706.010-706.154** — Earnings withholding order
  (wage garnishment): employer receives writ, withholds
  earnings; consumer may claim exemptions
- **CCP §§ 708.010-708.205** — Judgment debtor examination:
  judgment creditor may subpoena debtor to appear and answer
  questions about finances (OEX or debtor's exam)

### Civ. Code §§ 1788-1788.33 — Rosenthal Fair Debt Collection Practices Act (Rosenthal Act)

California's state analog to the FDCPA, codified at Civil Code
§§ 1788-1788.33.

**Critical distinction**: The Rosenthal Act applies to
**original creditors** as well as third-party debt collectors —
broader than the FDCPA, which covers only debt collectors.

- **§ 1788.2** — Definitions: "debt collector" includes
  creditors collecting their own debts in their own name,
  extending coverage beyond the FDCPA
- **§ 1788.10-1788.17** — Prohibited practices: essentially
  incorporates all FDCPA prohibited practices and extends
  them to original creditors
- **§ 1788.17** — State law debt collectors subject to
  FDCPA §§ 1692b-1692j as a matter of California law
- **§ 1788.18** — Unlawful to collect debts beyond the
  applicable SOL without disclosing that the debt is time-
  barred (added 2013)
- **§ 1788.30** — Liability: actual damages; statutory
  damages up to $1,000 per debt collection action; court
  costs and attorney fees mandatory for prevailing debtor

### Fin. Code §§ 100000-100027 — California Debt Collection Licensing Act (DCLA, 2022)

Effective January 1, 2022 (licensure required by December 31,
2021 for existing collectors):

- **§ 100001** — Definitions: "debt collector" includes
  persons and entities that engage in debt collection, broadly
  defined
- **§ 100004** — License required to collect consumer debts
  in California; administered by the Department of Financial
  Protection and Innovation (DFPI)
- **§ 100025** — Exempt entities: banks, credit unions, and
  certain other regulated entities
- **§ 100027** — Enforcement: DFPI may suspend or revoke
  license; civil actions by consumers for violations

**Practical significance**: A debt collector who lacks a
DCLA license cannot lawfully collect debts in California. A
debt buyer who is not licensed may be subject to the "unlicensed
collector" defense. Verify licensure at:
https://dfpi.ca.gov/debt-collection/

### Bus. & Prof. Code §§ 17200-17210 — Unfair Competition Law (UCL)

- **§ 17200** — Defines "unfair competition" as any unlawful,
  unfair, or fraudulent business act or practice, and unfair,
  deceptive, untrue, or misleading advertising
- **§ 17203** — Injunctive relief is the primary remedy under
  the UCL; restitution may be awarded; attorney fees are NOT
  available directly under the UCL (but may be recovered
  under CCP § 1021.5 in appropriate cases)
- **§ 17204** — Standing: a person who has suffered injury in
  fact and lost money or property as a result of unfair
  competition; also the Attorney General and certain
  prosecutors
- **§ 17205** — 4-year statute of limitations
- **§ 17206** — Civil penalties available in AG/prosecutor
  actions
- **§ 17208** — Any person may bring an action; class actions
  permitted (subject to CCP § 382 class certification)

**UCL "unlawful" prong**: Any violation of another law can
constitute an unlawful business practice under the UCL. This
means a violation of the Rosenthal Act, FDCPA, CLRA, or DCLA
can also be pleaded as a UCL claim.

### Civ. Code §§ 1750-1784 — Consumers Legal Remedies Act (CLRA)

- **§ 1750** — Declaration of purpose
- **§ 1760** — Definitions: "consumer" (natural person);
  "goods" or "services" (for personal, family, or household
  purposes)
- **§ 1770** — Enumerated prohibited practices (27 categories):
  includes passing off goods, misrepresentation, false
  advertising, failure to disclose, bait and switch, etc.
- **§ 1780** — Civil action: actual damages (minimum $1,000);
  punitive damages; injunctive relief; restitution; attorney
  fees mandatory for prevailing plaintiff
- **§ 1782** — Pre-suit notice required: 30 days before filing,
  consumer must demand that the defendant correct or remedy
  the unlawful practice; if remedied, plaintiff may seek
  only injunctive relief and attorney fees
- **§ 1784** — 3-year statute of limitations from discovery

**CLRA in debt cases**: The CLRA applies to the sale of
goods and services; it does not directly apply to debt
collection. However, CLRA claims may arise in the underlying
transaction that gave rise to the debt (e.g., fraudulent
sale of goods on credit).

### Civ. Code § 1788.50 et seq. — Fair Debt Buying Practices Act (FDBPA)

- **§ 1788.50** — Definitions: "debt buyer" (person who
  purchases charged-off consumer debt for collection or resale)
- **§ 1788.52** — Requirements before filing suit: the debt
  buyer must possess the debt purchase agreement, a copy of
  the original credit contract, a complete account statement,
  and documentation of the chain of title
- **§ 1788.53** — Resale of debt: restrictions on reselling
  debts that have been judicially resolved or that are beyond
  the SOL
- **§ 1788.54** — Verification: debt buyer must provide
  verification documents within 30 days of consumer demand
- **§ 1788.56** — Remedies: actual damages; $100 per violation,
  $500 if willful; injunctive relief; attorney fees

**FDBPA significance**: The FDBPA imposes requirements
specific to California debt buyers that go beyond the FDCPA
and Rosenthal Act. A debt buyer who cannot produce the chain
of title may be barred from filing suit in California.

### Com. Code §§ 9101-9809 — UCC Article 9 (California)

California's enactment of revised UCC Article 9, with minor
non-uniform amendments. See `../ucc-model/README.md` for the
model UCC and California deviations.

Key sections for debt cases:
- **§ 9203** — Attachment of security interest
- **§ 9317** — Subordination and priority against lien
  creditors
- **§ 9601-9629** — Default; enforcement; self-help
  repossession; deficiency and surplus

**California deviation**: No deficiency on purchase-money
security interests in consumer goods (except motor vehicles);
see Com. Code § 9626(b).

## Key SOL table

| Obligation | SOL | Code Section |
|-----------|-----|-------------|
| Written contract | 4 years | CCP § 337 |
| Account stated (written) | 4 years | CCP § 337a |
| Oral contract | 2 years | CCP § 339 |
| Judgment renewal | 10 years | CCP § 683.020 |
| UCL claim | 4 years | Bus. & Prof. Code § 17208 |
| CLRA claim | 3 years (from discovery) | Civ. Code § 1784 |
| Rosenthal Act claim | 1 year | Civ. Code § 1788.30(f) |
| FDCPA claim | 1 year (from violation) | 15 U.S.C. § 1692k(d) |

## How to re-pull

```bash
python3 scripts/pull_ca_statutes.py \
  --workers 12 \
  --manifest plugins/ca-court-docs/skills/ca-law-references/references/ca-statutes-debt/_manifest.json
```

(Script to be created in parallel with the existing WA
`pull_wa_rcw.py`.) The script fetches verbatim section text
from leginfo.legislature.ca.gov and writes individual markdown
files by code/section range.

## Status

Empty in the initial PR — only this README and a placeholder.
The first re-pull will populate the verbatim chapter files.

## Cross-references

- `../online-sources.md` — canonical URLs for California
  statutes
- `../legal-data-apis.md` — programmatic access to
  leginfo.legislature.ca.gov
- `../../ca-consumer-debt/` — California consumer-debt
  subject-matter bundle, which relies on this corpus for
  substantive law
- `../federal-debt-laws/README.md` — federal FDCPA, FCRA,
  TILA, ECOA
