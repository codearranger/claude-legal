# claude-legal-immigration-laws

Shared, venue-independent plugin for **U.S. immigration law** — the federal counterpart to `claude-legal-federal-laws`, built for immigration practice.

> **NOT LEGAL ADVICE.** Generated content is a drafting/research aid, not legal advice, and creates no attorney-client relationship. Immigration consequences are severe and often irreversible — verify against current law and consult a licensed attorney or EOIR-accredited representative before filing. Beware notario fraud.

## What it covers

Snapshots the canonical **rules** verbatim:

- **INA** — the Immigration and Nationality Act, 8 U.S.C. Chapter 12, one file per subchapter, with an INA-section ↔ 8 U.S.C.-section crosswalk.
- **Regulations** — curated **8 CFR** (DHS/USCIS/CBP/ICE chapter I + the DOJ/EOIR chapter V for the immigration courts and the Board of Immigration Appeals) and the State-Department **22 CFR** visa/passport/exchange parts.
- **Foreign Affairs Manual (FAM)** — verbatim 9 FAM 100/302/402/502/504 + 8 FAM 300 + 7 FAM 000/1400.
- **EOIR court rules** — the binding 8 CFR Part 1003/1240/1208 regs (in `immigration-regulations/`) plus pointer stubs for the Immigration Court Practice Manual and the BIA Practice Manual.

**Case law is indexed for on-demand lookup, not snapshotted** (it is too large/fast-moving to mirror): the federal **circuit courts** (petitions for review under INA § 242 / 8 U.S.C. § 1252, via CourtListener), the **Board of Immigration Appeals** (I&N Dec., via the EOIR Virtual Law Library), and the USCIS **Administrative Appeals Office (AAO)**.

**As of v0.3.0** it also ships an **11-skill, venue-independent, document-producing self-help layer** (matter-neutral, documents-not-advice, with prominent get-a-lawyer / notario-fraud warnings): `immigration-pro-se`, `eoir-immigration-courts`, `immigration-deadlines`, `immigration-fact-check`, `eoir-removal-defense`, `eoir-motions-to-reopen-reconsider`, `bia-appeals`, `uscis-benefit-requests`, `immigration-foia`, `circuit-petition-for-review`, `consular-visa-refusal`.

## Reference corpora

Each lives under `references/` with its own README (scope, pull mechanics, access posture): `immigration-statutes/`, `immigration-regulations/`, `foreign-affairs-manual/`, `court-rules/`, plus `legal-data-apis.md` (the on-demand case-law index) and `online-sources.md`.

## Refresh

`scripts/pull_ina.py` · `scripts/pull_immigration_cfr.py` · `scripts/pull_fam.py` (AIA-chases fam.state.gov's omitted TLS intermediate, then crawls its JSON TOC API) · `scripts/pull_eoir_manuals.py`.

---
Part of the [claude-legal](../../README.md) marketplace. Skills are indexed in [CLAUDE.md](../../CLAUDE.md).
