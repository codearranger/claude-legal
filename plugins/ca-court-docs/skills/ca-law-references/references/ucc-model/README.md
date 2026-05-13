# UCC Model Articles — California Plugin Pointer

The Uniform Commercial Code is enacted in every U.S. state
with state-by-state variations. California has enacted UCC
Articles 1, 2, 3, 4, 4A, 5, 7, 8, and 9 in the **California
Commercial Code (Com. Code)**.

## California UCC by article

| UCC Article | Subject | California Com. Code |
|-------------|---------|---------------------|
| Article 1 — General Provisions | Definitions, scope | Com. Code §§ 1101-1310 |
| Article 2 — Sales | Sale of goods | Com. Code §§ 2101-2725 |
| Article 2A — Leases | Leases of goods | Com. Code §§ 10101-10532 |
| Article 3 — Negotiable Instruments | Notes, drafts, checks | Com. Code §§ 3101-3605 |
| Article 4 — Bank Deposits | Banking operations | Com. Code §§ 4101-4504 |
| Article 4A — Funds Transfers | Wire transfers | Com. Code §§ 11101-11507 |
| Article 5 — Letters of Credit | Letters of credit | Com. Code §§ 5101-5118 |
| Article 6 — Bulk Sales (repealed) | — | repealed |
| Article 7 — Documents of Title | Bills of lading, warehouses | Com. Code §§ 7101-7603 |
| Article 8 — Investment Securities | Securities | Com. Code §§ 8101-8511 |
| Article 9 — Secured Transactions | Liens, security interests | Com. Code §§ 9101-9809 |

## What lives here

The **Model UCC** text from the Uniform Law Commission (ULC)
and Cornell Legal Information Institute (LII), for quick
reference to the uniform language before California's
enactment. California's enacted Commercial Code text controls
in California courts.

| File | Subject |
|------|---------|
| `Article-1.md` | General Provisions |
| `Article-2.md` | Sales |
| `Article-3.md` | Negotiable Instruments |
| `Article-9.md` | Secured Transactions |

## How to populate

Re-use the existing WA plugin script:

```bash
python3 scripts/pull_ucc.py --workers 8 \
  --output plugins/ca-court-docs/skills/ca-law-references/references/ucc-model/
```

The script extracts UCC text from Cornell LII
(law.cornell.edu/ucc).

## California Commercial Code text

For California's **enacted** Commercial Code text (which
controls in California courts), pull from leginfo:

- Com. Code Article 1 (§§ 1101-1310):
  https://leginfo.legislature.ca.gov/faces/codesTOCSelected.xhtml?tocCode=COM

Navigate to the Commercial Code table of contents; divisions
correspond to UCC articles.

The California Commercial Code is available at:
**https://leginfo.legislature.ca.gov/faces/codesTOCSelected.xhtml?tocCode=COM**

## California-specific UCC deviations

California has adopted several non-uniform amendments to the
model UCC:

### Article 2 (Sales)

California has not adopted the 2003 amendments to UCC Article
2 (which were proposed to address software transactions).
California's Article 2 is the pre-2003 version.

### Article 9 (Secured Transactions)

California enacted revised Article 9 (2000 ULC version) with
minor non-uniform amendments. Key for debt collection:

- **Com. Code § 9317** — Buyers and lessees in ordinary
  course of business; lien creditors; when security interest
  is cut off
- **Com. Code § 9320** — Buyers of goods; protection from
  perfected security interest
- **Com. Code § 9601-9629** — Default; enforcement of
  security interest; self-help repossession; deficiency
  and surplus

**California-specific Article 9 issue**: California prohibits
deficiency judgments on purchase-money security interests
in consumer goods (except motor vehicles) under Com. Code
§ 9626(b). This is a significant deviation from the Model
UCC and from the WA/OR approach; a consumer who loses personal
property to repossession on a purchase-money loan may not owe
a deficiency balance.

### Article 3 (Negotiable Instruments)

California has adopted revised Article 3 (1990 ULC version)
substantially as uniform. Key for debt cases:

- **Com. Code § 3301** — Person entitled to enforce instrument
- **Com. Code § 3308** — Proof of signatures; defenses
- **Com. Code § 3309** — Enforcement of lost, destroyed, or
  stolen instrument
- **Com. Code § 3415** — Obligation of indorser

## Why both model UCC and California Commercial Code?

- **Model UCC** is the citation courts use in inter-state
  cases, or when discussing underlying doctrine and history
  of a rule
- **California Commercial Code** is the actual law that
  California judges apply

In a debt-collection case involving a credit card charge-off
and assignment to a debt buyer, citing both is often useful:

> Cal. Com. Code, § 9203 (governing attachment and
> perfection of security interests under California's
> enactment of UCC Article 9).

## Cross-references

- `../ca-statutes-debt/README.md` — California statutes
  governing debt, including UCC Article 9 as enacted
- `../../ca-consumer-debt/` — California consumer-debt
  subject-matter bundle, which addresses chain-of-title
  issues under Article 3 and Article 9
- Cornell LII UCC: https://www.law.cornell.edu/ucc

## Status

Empty in the initial PR — only this README.
