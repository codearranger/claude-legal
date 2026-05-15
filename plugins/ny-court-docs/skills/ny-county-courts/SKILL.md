---
name: ny-county-courts
description: >
  Use when filing in a New York trial court other than the
  five flagship counties (New York, Kings, Bronx, Nassau,
  Queens) and other than the two dedicated Long Island
  District Courts. Triggers include 'Suffolk County Supreme
  Court', 'Westchester County Supreme Court', 'Erie County
  Supreme Court', 'Monroe County Supreme Court', 'Onondaga
  County Supreme Court', 'Richmond County Supreme Court'
  (Staten Island), 'Civil Court of the City of New York',
  'City Court', 'Town and Village Justice Court', 'small
  claims part'. Covers the next-largest counties' Supreme
  Courts, the four NYC borough Civil Courts under the Civil
  Court Act, upstate City Courts, and Town & Village Justice
  Courts. For the Nassau and Suffolk District Courts use the
  dedicated skills `ny-nassau-dc` and `ny-suffolk-dc`.
version: 0.2.0
---

# New York County Courts — Long-tail Roll-up

> **NOT LEGAL ADVICE.** Verify the specific court's local
> rules before filing.

This skill covers New York's trial courts **other than** the
five flagship Supreme Court venues already covered by
`ny-nyco`, `ny-kings`, `ny-bronx`, `ny-nassau`, and
`ny-queens`. New York has an unusually fragmented trial-court
system — far more layers than most states. The principal
courts:

## Supreme Court (other counties)

The Supreme Court is New York's court of general jurisdiction
in every county. Beyond the five flagship counties, the
next-largest civil-trial venues:

| County | JD | Courthouse | Comm Div threshold |
|--------|----|----|----------------|
| Suffolk | 10th | Riverhead | $100,000 |
| Westchester | 9th | White Plains | $200,000 |
| Richmond (Staten Island) | 2nd (admin); separate filing | St. George Courthouse | $150,000 |
| Erie | 8th | Buffalo | $100,000 |
| Monroe | 7th | Rochester | $50,000 |
| Onondaga | 5th | Syracuse | $50,000 |
| Rockland | 9th | New City | $100,000 |
| Albany | 3rd | Albany | $50,000 |
| Orange | 9th | Goshen | $100,000 |
| Dutchess | 9th | Poughkeepsie | (no Comm Div) |
| Saratoga | 3rd | Ballston Spa | $50,000 |
| Oneida | 5th | Utica | (no Comm Div) |

Filings use NYSCEF in nearly all counties. Confirm the
assigned Justice's Part Rules before motion practice.

## Civil Court of the City of New York

A **separate trial court** from Supreme Court, established by
the Civil Court Act, with jurisdiction over civil actions up
to **$50,000** and small-claims matters up to **$10,000**.
Five boroughs, each its own branch:

- **New York County** — 111 Centre Street
- **Kings County** — 141 Livingston Street, Brooklyn
- **Bronx County** — 851 Grand Concourse
- **Queens County** — 89-17 Sutphin Boulevard, Jamaica
- **Richmond County** — 927 Castleton Avenue, Staten Island

NYC Civil Court is the **primary forum for consumer-debt
collection actions** under $50,000. The court has been the
focus of the 2022 Consumer Credit Fairness Act (CCFA)
reforms — heightened pleading (CPLR 3015(e)) and default-
judgment scrutiny (22 NYCRR § 202.27-a). See `ny-consumer-
debt`.

NYC Civil Court also operates the **Housing Court Part** —
covered separately under `ny-landlord-tenant`.

E-filing: UCMS / CCEF (the Civil Court's electronic-filing
system) — not NYSCEF.

## District Courts (Nassau & Suffolk)

Long Island has its own **District Court** layer (not present
elsewhere in the state). Each District Court is now covered
by a **dedicated skill**:

- **Nassau District Court** — see [`ny-nassau-dc`]. Six
  districts; 99 Main Street, Hempstead. Jurisdiction up to
  $15,000 civil; full L&T Part; small / commercial claims;
  misdemeanor + violation criminal. 22 NYCRR Part 212.
- **Suffolk District Court** — see [`ny-suffolk-dc`]. Six
  districts covering the five **western** towns + Brookhaven
  only; eastern Suffolk routes to Town Justice Courts.
  Cohalan Court Complex, Central Islip. Jurisdiction up to
  $15,000 civil. 22 NYCRR Part 212.

Pro se debt-collection cases and L&T summary proceedings are
the dominant case categories at both courts. Use the
dedicated skills for filing detail.

## City Courts (upstate)

Outside NYC, **City Courts** (Uniform City Court Act) sit in
~60 cities with civil jurisdiction up to **$15,000**. Major
examples: Buffalo City Court, Rochester City Court, Syracuse
City Court, Albany City Court, Yonkers City Court.

E-filing: NYSCEF in many City Courts, expanding.

## Town & Village Justice Courts

Approximately **1,250 Town & Village Justice Courts** across
the state — the small-claims and minor-civil layer in
suburban / rural towns. **Civil jurisdiction up to $3,000**;
small-claims up to **$3,000** (UJCA § 1801).

Justice Courts use a separate set of rules — Uniform Justice
Court Act (UJCA). Pro se litigation is the norm; the court is
often a part-time judge in a town hall meeting room.

## Surrogate's Court, Family Court, Court of Claims

Specialized trial courts:

- **Surrogate's Court** — wills, estates, guardianship,
  adoption (one per county)
- **Family Court** — child custody/support, juvenile, family
  offense (one per county, two in NYC boroughs)
- **Court of Claims** — claims against the State of New
  York; sits statewide

These are outside the scope of consumer-debt and general-
civil pro se practice but linked from `ny-law-references`.

## Cross-references

- `ny-statewide-format` — format baseline (22 NYCRR § 202.5
  applies to Supreme/County Court; UCCA / UCA / UJCA mirror
  the format requirements with adjustments)
- `ny-consumer-debt` — debt cases in Civil Court of the City
  of New York, Nassau/Suffolk District Courts, and City
  Courts
- `ny-landlord-tenant` — Housing Court Part of NYC Civil
  Court; District Court housing parts on Long Island
- `ny-file-packet` — NYSCEF / UCMS / county-specific filing
  protocols
