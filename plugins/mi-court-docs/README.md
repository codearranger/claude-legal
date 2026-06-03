# mi-court-docs — Michigan

Draft and format pleadings, declarations, motions, and proposed orders for Michigan circuit and district courts.

> **NOT LEGAL ADVICE.** Output is a drafting aid; verify every rule, deadline, and citation against current law before filing.

## What it covers

Applies **MCR 1.109 / 2.113** formatting (the Michigan caption, MiFILE e-filing, line-numbering; court-rule-based, not statutory). Covers Michigan's unified **Circuit Court / District Court** topology: two dedicated Circuit Court venues (Wayne — 3rd Circuit, Detroit; Oakland — 6th Circuit, Pontiac; each running a designated Business Court under MCL 600.8031) plus a Circuit Court roll-up (`mi-circuit-courts`); the `mi-36th-district` skill (the busiest district court in the state — the dominant consumer-debt + eviction forum) plus a District Court roll-up (`mi-district-courts`, $25,000 civil cap + summary proceedings + small claims); and `mi-family-court` (Family Division of Circuit Court; Friend of the Court; PPOs under MCL 600.2950; the MCR 3.200-series).

**Six subject-matter bundles:** `mi-consumer-debt` (FDCPA / Reg F / Regulation of Collection Practices Act MCL 445.251 / Occupational Code Article 9 licensing / Michigan CPA / chain of title), `mi-family-law` (no-fault divorce MCL 552.6 + 60/180-day waiting periods, equitable distribution per *Sparks*, Child Custody Act MCL 722.23, Michigan Child Support Formula, 100-mile rule MCL 722.31, no common-law marriage), `mi-landlord-tenant` (summary proceedings MCL 600.5701 + MCR 4.201, MCL 554.134 notices, security deposits MCL 554.602/.613, Truth in Renting Act, retaliation MCL 600.5720), `mi-personal-injury` (modified comparative fault with the 51% noneconomic bar MCL 600.2959, No-Fault Auto MCL 500.3101 + serious-impairment threshold per *McCormick*, product liability, med-mal NOI + affidavit of merit), `mi-employment` (Elliott-Larsen Civil Rights Act MCL 37.2101, Whistleblowers' Protection Act, wage law incl. *Mothering Justice*, non-compete under MARA MCL 445.774a, workers'-comp exclusive remedy MCL 418.131), `mi-commercial-disputes` (Michigan Business Court MCL 600.8031, UCC, LLC Act / BCA incl. shareholder oppression MCL 450.1489, MUTSA MCL 445.1901, statutory conversion MCL 600.2919a, arbitration MCL 691.1681).

**29 SKILL.md files.** Follows the thin-skill architecture.

## Reference corpora

Under `skills/mi-law-references/references/` (each corpus dir has its own README): `mi-statutes-debt/` (verbatim MCL via legislature.mi.gov), `court-rules/` (verbatim MCR ch. 1-4 + MRE via the courtrules.net mirror — courts.michigan.gov gates its rule-asset URLs), plus curated `civil-rules.md` / `evidence-rules.md` / `key-cases.md` / etc. and the shared federal symlinks.

## Refresh

`scripts/pull_michigan_statutes.py` · `scripts/pull_michigan_rules.py`. Plugin scripts: `format-check.py` (MCR 1.109 / 2.113) · `case-calendar.py` (MCR 1.108 + MCL 435.101 holidays).

---
Part of the [claude-legal](../../README.md) marketplace. Skills are indexed in [CLAUDE.md](../../CLAUDE.md).
