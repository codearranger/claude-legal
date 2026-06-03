# ny-court-docs — New York

Draft and format pleadings, declarations, motions, and proposed orders across New York's unusually fragmented civil-court system. The largest state plugin in the marketplace (**35 SKILL.md files**).

> **NOT LEGAL ADVICE.** Output is a drafting aid; verify every rule, deadline, and citation against current law before filing.

## What it covers

Applies **22 NYCRR § 202.5** paper format and **§ 202.5-b** NYSCEF e-filing format (the New York caption: "-against-" party separator, Index Number, assigned Justice + Part).

**Venues** — five flagship Supreme Court venues each as its own skill (New York / Kings / Bronx / Nassau / Queens, with the Commercial Division thresholds), the two Long Island District Courts (`ny-nassau-dc`, `ny-suffolk-dc`; UDCA / 22 NYCRR Part 212), `ny-nyc-civil-court` (Civil Court Act $50k cap; highest-volume consumer-debt forum in the country), `ny-nyc-housing-court` (RPAPL Article 7; Local Law 136 Right to Counsel; ERAP), `ny-city-courts` (~60 upstate City Courts, $15k), `ny-justice-courts` (~1,250 Town/Village courts, $3k), `ny-family-court` (FCA Articles 3-10), and a Supreme Court roll-up `ny-county-courts`.

**Five subject-matter bundles:** `ny-consumer-debt` (FDCPA, Reg F, 2022 CCFA, GBL § 600, GBL §§ 349/350, CPLR 4544, UCC Article 9 chain of title), `ny-landlord-tenant` (RPAPL Article 7, 2019 HSTPA, 2024 Good Cause Eviction, RPL § 235-b, Local Law 136, ERAP), `ny-personal-injury` (CPLR Article 14-A + 16, Insurance Law § 5102(d), Labor Law § 240(1)/§ 241(6), GML § 50-e, CPLR 214-a, CVA/ASA), `ny-employment` (NYS HRL, NYC HRL with *Williams* rule, Labor Law § 191/198/740, WARN, CROWN Act), `ny-commercial-disputes` (22 NYCRR § 202.70 Commercial Division, CPLR 3016(b), BCL § 720/§ 1104-a, Faithless Servant, GOL §§ 5-1401/5-1402).

**Procedural quirks worth flagging:** CPLR 2103(b)(2) 5-day mail-service rule; verified-vs-unverified pleadings (CPLR 3020); post-2023 CPLR 2106 universal affirmation (ended the notary bottleneck for pro se); the Individual Assignment System (22 NYCRR § 202.3); the § 202.48 settle-order 60-day clock (*Funk v. Barry*); the 20-year money-judgment SOL (CPLR 211(b)); and Long Island's unique District Court layer.

## Reference corpora

Under `skills/ny-law-references/references/` (each corpus dir has its own README): `ny-statutes-debt/` (36 consolidated-laws targets via the NY Senate Open Legislation API), `court-rules/` (15 Parts of 22 NYCRR verbatim + 5 stubs), plus the shared federal symlinks.

## Refresh

`scripts/pull_ny_statutes.py` (needs `NYSENATE_API_KEY`; stubs otherwise) · `scripts/pull_ny_court_rules.py` (curl_cffi; optional `NY_RULES_PROXY`). Plugin scripts: `format-check.py` · `case-calendar.py`.

---
Part of the [claude-legal](../../README.md) marketplace. Skills are indexed in [CLAUDE.md](../../CLAUDE.md).
