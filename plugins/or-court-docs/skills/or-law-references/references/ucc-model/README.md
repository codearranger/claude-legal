# UCC Model Articles — Oregon Plugin Pointer

The Uniform Commercial Code is enacted in every U.S. state with
state-by-state variations. Oregon has enacted Articles 1, 2,
3, 9 (and others) in **ORS Chapters 71–79**.

## Oregon UCC by article

| UCC Article | Subject | ORS Chapter |
|-------------|---------|-------------|
| Article 1 — General Provisions | Definitions, scope | ORS Ch. 71 |
| Article 2 — Sales | Sale of goods | ORS Ch. 72 |
| Article 2A — Leases | Leases of goods | ORS Ch. 72A |
| Article 3 — Negotiable Instruments | Notes, drafts | ORS Ch. 73 |
| Article 4 — Bank Deposits and Collections | Banking | ORS Ch. 74 |
| Article 4A — Funds Transfers | Wire transfers | ORS Ch. 74A |
| Article 5 — Letters of Credit | Letters of credit | ORS Ch. 75 |
| Article 6 — Bulk Sales (repealed) | — | — |
| Article 7 — Documents of Title | Bills of lading, warehouses | ORS Ch. 77 |
| Article 8 — Investment Securities | Securities | ORS Ch. 78 |
| Article 9 — Secured Transactions | Liens, security interests | ORS Ch. 79 |

## What lives here

The **Model UCC** text from the Uniform Law Commission, for
quick reference to the uniform language before Oregon's
enactment. Oregon's enacted text (in ORS 71-79) controls in
Oregon courts.

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
  --output plugins/or-court-docs/skills/or-law-references/references/ucc-model/
```

The script extracts UCC text from Cornell LII
(law.cornell.edu/ucc).

## Oregon UCC text

For Oregon's **enacted** UCC text (which controls in Oregon
courts), pull from ORS:

- ORS 71: https://www.oregonlegislature.gov/bills_laws/ors/ors071.html
- ORS 72: https://www.oregonlegislature.gov/bills_laws/ors/ors072.html
- ORS 73: https://www.oregonlegislature.gov/bills_laws/ors/ors073.html
- ORS 79: https://www.oregonlegislature.gov/bills_laws/ors/ors079.html

(Stored in `../or-ors-debt/` once populated.)

## Why both?

- **Model UCC** is the citation many courts use in inter-state
  cases or when discussing the underlying doctrine
- **Oregon-enacted ORS Ch. 71-79** is the actual law that
  Oregon judges apply

In a debt-collection case, citing both is often useful:

> ORS 79.0203 (governing perfection of security interests in
> Oregon, enacting UCC § 9-203 with the standard "attachment"
> requirements).

## Cross-references

- `../or-consumer-debt/references/ucc-article-9.md` — Oregon-
  flavored agent-facing summary of the UCC Article 9 issues
  most relevant to debt-buyer chain-of-title disputes
- `../or-ors-debt/README.md` — Oregon's enacted UCC chapters

## Status

Empty in initial PR — only this README.
