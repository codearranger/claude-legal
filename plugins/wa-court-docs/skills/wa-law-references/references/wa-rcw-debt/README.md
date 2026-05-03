# Washington RCW — Debt-Relevant Chapters

A curated subset of the Revised Code of Washington focused on chapters that come up in consumer-debt and collections cases. One MD file per chapter; every section preserved verbatim with citation history and notes.

- Pulled: 2026-05-02
- Source: [app.leg.wa.gov/RCW](https://app.leg.wa.gov/RCW/)
- Total sections: 477 across 21 chapters

## Title 4 — Civil Procedure

| File | Citation | Chapter |
|---|---|---|
| [RCW-4_16.md](RCW-4_16.md) | RCW 4.16 | Limitation of Actions (statute of limitations) |
| [RCW-4_28.md](RCW-4_28.md) | RCW 4.28 | Commencement of Actions / Service of Process |
| [RCW-4_56.md](RCW-4_56.md) | RCW 4.56 | Judgments |
| [RCW-4_84.md](RCW-4_84.md) | RCW 4.84 | Costs |

## Title 6 — Enforcement of Judgments

| File | Citation | Chapter |
|---|---|---|
| [RCW-6_01.md](RCW-6_01.md) | RCW 6.01 | Enforcement of Judgments — General Provisions |
| [RCW-6_13.md](RCW-6_13.md) | RCW 6.13 | Homesteads |
| [RCW-6_15.md](RCW-6_15.md) | RCW 6.15 | Personal Property Exempt from Execution |
| [RCW-6_17.md](RCW-6_17.md) | RCW 6.17 | Executions |
| [RCW-6_21.md](RCW-6_21.md) | RCW 6.21 | Sales Under Execution |
| [RCW-6_25.md](RCW-6_25.md) | RCW 6.25 | Attachment |
| [RCW-6_27.md](RCW-6_27.md) | RCW 6.27 | Garnishment |
| [RCW-6_32.md](RCW-6_32.md) | RCW 6.32 | Proceedings Supplemental to Execution |
| [RCW-6_36.md](RCW-6_36.md) | RCW 6.36 | Uniform Enforcement of Foreign Judgments Act |

## Title 12 — District Courts and Justices of the Peace

| File | Citation | Chapter |
|---|---|---|
| [RCW-12_40.md](RCW-12_40.md) | RCW 12.40 | Small Claims |

## Title 19 — Business Regulations — Miscellaneous

| File | Citation | Chapter |
|---|---|---|
| [RCW-19_16.md](RCW-19_16.md) | RCW 19.16 | **Collection Agencies** (WA's parallel to the FDCPA) |
| [RCW-19_36.md](RCW-19_36.md) | RCW 19.36 | Contracts and Credit Agreements Requiring Writings (statute of frauds) |
| [RCW-19_52.md](RCW-19_52.md) | RCW 19.52 | Interest — Usury |
| [RCW-19_86.md](RCW-19_86.md) | RCW 19.86 | Unfair Business Practices — Consumer Protection Act |

## Title 62A — Uniform Commercial Code

| File | Citation | Chapter | Model |
|---|---|---|---|
| [RCW-62A_1.md](RCW-62A_1.md) | RCW 62A.1 | UCC — General Provisions | [UCC art. 1](../ucc-model/Article-1.md) |
| [RCW-62A_3.md](RCW-62A_3.md) | RCW 62A.3 | UCC — Negotiable Instruments | [UCC art. 3](../ucc-model/Article-3.md) |
| [RCW-62A_9A.md](RCW-62A_9A.md) | RCW 62A.9A | UCC — Secured Transactions | [UCC art. 9](../ucc-model/Article-9.md) |

## Re-pulling

```
python3 scripts/pull_wa_rcw.py --workers 12
```
