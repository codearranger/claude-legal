---
name: or-lanecc
description: >
  Use when drafting or filing in Lane County Circuit Court (Eugene /
  Springfield), Oregon's third-largest circuit court. Triggers include
  "Lane County Circuit Court", "Lane County Oregon court", "Eugene
  courthouse Oregon", "Springfield Oregon court", "Lane County civil
  case", "LSCC Oregon", "Lane County OJIN", "LaneCounty OJD eCourt",
  "Eugene Oregon civil litigation". Covers Lane County Circuit Court
  specifics — courthouse locations, civil departments, OJIN eCourt
  eFiling, local supplemental local rules (SLR), scheduling and
  hearing procedures, and fee schedule. Layer on `or-statewide-format`.
version: 0.1.0
---

# Lane County Circuit Court

Use this skill in addition to `or-statewide-format` when the
case is in the Lane County Circuit Court. Lane County (population
~390,000; county seat Eugene, with the City of Springfield as the
second-largest city) has the third-highest civil caseload in Oregon
after Multnomah and Washington Counties.

## Court locations

| Location | Address | Case types |
|---|---|---|
| **Lane County Courthouse** (primary) | 125 E. 8th Ave., Eugene, OR 97401 | All civil, family, criminal, probate |
| **Justice Building** | 101 W. 10th Ave., Eugene, OR 97401 | Criminal overflow; some civil calendars |

The clerk's office and filing window are at the Lane County Courthouse,
main floor. Phone: (541) 682-4020. Court website:
`https://www.courts.oregon.gov/courts/lane/Pages/default.aspx`

## eFiling — OJD eCourt (OJIN)

Lane County Circuit Court participates in **OJD eCourt** (Oregon's
statewide e-filing system):
`https://ecourt.ojd.state.or.us`

- Mandatory eFiling for represented parties in civil cases
- Self-represented litigants may file electronically or in paper
  at the clerk's window
- Filing cut-off for same-day processing: **4:30 p.m.** (check
  the OJD eCourt website for current cut-off times)
- eFiling requires an OJD eCourt account; register at
  `https://oregonlegislature.gov` / OJD website
- Service via eFiling: eFiled documents served through OJD eCourt
  constitute electronic service when all parties are registered

## Civil departments and scheduling

Lane County Circuit Court has multiple civil judges who rotate
assignments. The presiding judge and civil assignments are posted on
the court's website. Key scheduling features:
- **Law and motion** hearings are typically held **Monday mornings**
  (verify current schedule with the clerk)
- **Civil trials**: bench and jury trials scheduled by the civil
  presiding judge; parties must contact the scheduling clerk after
  the case is at-issue
- **Mediation**: the court has an active ADR program; parties may
  stipulate to mediation at any time; some civil cases are referred
  to mediation by the judge

## Lane County SLR (Supplemental Local Rules)

Lane County's SLR supplements the UTCR. Current SLR available at:
`https://www.courts.oregon.gov/courts/lane/Pages/localrules.aspx`

Key Lane County SLR provisions:
- **SLR 3.025** (or applicable section): scheduling orders and
  trial management; Lane County typically issues a scheduling order
  after issue is joined, setting discovery cutoffs and trial dates
- **SLR 7.015**: ex parte communications protocol
- Family-law SLR: separate provisions for parenting-time disputes
  and child-support matters

Verify the current SLR before filing; Lane County updates its SLR
periodically.

## Fee schedule

Oregon circuit court fees are set statewide (ORS 21.100-21.115)
with some county-level variations. Verify current fees at the
clerk's window or at `https://www.courts.oregon.gov/programs/
opu/Pages/fees.aspx` for civil filing-fee schedule.

## Composition

Layer this skill on `or-statewide-format` for all Lane County filings:
- `or-pro-se` — pro-se framework; Lane County has a Law Library
  at the courthouse (541-682-4586) and participates in the OJD
  self-help program
- `or-consumer-debt` — Lane County Circuit Court is an active
  consumer-debt forum (Eugene is the second-largest Oregon metro)
- `or-landlord-tenant` — active FED docket; Lane County has a
  significant rental market (University of Oregon student population)
- `or-deadlines` — ORCP 10 deadline arithmetic applies; Lane County
  has no unique holiday schedule beyond Oregon state holidays
