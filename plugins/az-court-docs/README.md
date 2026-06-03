# az-court-docs — Arizona

Draft and format pleadings, declarations, motions, and proposed orders for Arizona Superior and Justice Courts.

> **NOT LEGAL ADVICE.** Output is a drafting aid; verify every rule, deadline, and citation against current law before filing.

## What it covers

Applies **Ariz. R. Civ. P. 10 / 7.1** formatting (the Superior Court of Arizona caption, AZTurboCourt e-filing, line-numbering). Covers a dedicated **Maricopa County Superior Court** skill (Phoenix — the state's largest court, a designated Commercial Court program + compulsory-arbitration limit), a **Pima County Superior Court** skill (Tucson), and a Superior Court roll-up (`az-superior-courts`, the other 13 counties); the `az-justice-courts` skill for the limited-jurisdiction Justice Courts (limited civil + small claims + residential eviction "special detainer" under the separate **JCRCP** rule set — the high-volume consumer-debt + eviction forum); and `az-family-court` for the Family Department (separate **Arizona Rules of Family Law Procedure (ARFLP)**).

**Six subject-matter bundles:** `az-consumer-debt` (FDCPA / Reg F / Arizona Consumer Fraud Act A.R.S. § 44-1521 / collection-agency licensing A.R.S. Title 32 ch. 9 / chain of title; *Mertola v. Santos* acceleration SOL; two-way fee-shifting A.R.S. § 12-341.01), `az-family-law` (community property A.R.S. § 25-211/§ 25-318, no-fault dissolution, covenant marriage § 25-901, legal decision-making/parenting time § 25-403, Arizona Child Support Guidelines, 2023 Spousal Maintenance Guidelines, no common-law marriage), `az-landlord-tenant` (ARLTA A.R.S. § 33-1301, special-detainer eviction § 33-1377, 5/10-day notices § 33-1368, security deposits § 33-1321, RPEA), `az-personal-injury` (pure comparative negligence § 12-2505, several liability / nonparty-at-fault § 12-2506, the constitutional prohibition on damages caps, public-entity 180-day notice § 12-821.01, med-mal expert affidavit § 12-2603), `az-employment` (Arizona Employment Protection Act § 23-1501, Arizona Civil Rights Act § 41-1461, Wage Act treble damages § 23-355, minimum wage § 23-363, non-compete under *Valley Medical Specialists v. Farber*, workers'-comp exclusive remedy § 23-1022; right-to-work), `az-commercial-disputes` (Maricopa Commercial Court, UCC, 2019 Arizona LLC Act § 29-3101, Arizona Uniform Trade Secrets Act § 44-401, UFTA § 44-1001, civil racketeering § 13-2314.04, fee-shifting § 12-341.01).

**28 SKILL.md files.** Follows the thin-skill architecture.

## Reference corpora

Under `skills/az-law-references/references/` (each corpus dir has its own README): `az-statutes-debt/` (verbatim A.R.S. via azleg.gov), `court-rules/` (verbatim ARCP + Ariz. R. Evid. + ARFLP + JCRCP via the courtrules.net mirror — azcourts.gov is Cloudflare-gated), plus curated reference files and the shared federal symlinks.

## Refresh

`scripts/pull_arizona_statutes.py` · `scripts/pull_arizona_rules.py`. Plugin scripts: `format-check.py` (Ariz. R. Civ. P. 10 / 7.1) · `case-calendar.py` (Ariz. R. Civ. P. 6 + A.R.S. § 1-301 holidays).

---
Part of the [claude-legal](../../README.md) marketplace. Skills are indexed in [CLAUDE.md](../../CLAUDE.md).
