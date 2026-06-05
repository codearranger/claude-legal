---
name: ar-county-courts
description: >
  This skill should be used when the user is filing in an Arkansas
  Circuit Court other than Pulaski, Benton, or Washington County — the
  other most-populous counties' circuit courts plus a way to confirm
  the circuit number and local administrative plan for any of the 75
  counties. Triggers include "Faulkner County circuit court", "Conway
  circuit court", "Saline County", "Benton Arkansas circuit court",
  "Craighead County", "Jonesboro circuit court", "Sebastian County",
  "Fort Smith circuit court", "Garland County", "Hot Springs circuit
  court", "Lonoke County", "White County", "Searcy circuit court",
  "Jefferson County", "Pine Bluff circuit court", "Crittenden County",
  "West Memphis circuit court", "Pope County", "Russellville circuit
  court", "which judicial circuit is my county in", and "how many
  judicial circuits are there in Arkansas". Explains the 28-judicial-
  circuit / 75-county structure and how to confirm the circuit number
  and administrative plan. Layers on top of `ar-statewide-format`.
version: 0.1.0
---

# Arkansas County Circuit Courts (roll-up)

> **NOT LEGAL ADVICE.** These notes describe the venue's procedural
> mechanics as a drafting aid, not legal advice. Local rules,
> administrative plans, and judge-specific practices change; verify
> with the clerk and the current administrative plan before relying on
> anything here.

This skill is the **roll-up for every Arkansas Circuit Court outside
the three flagship venues** (Pulaski, Benton, Washington). It covers the
other most-populous counties and explains how to confirm the judicial
circuit and local administrative plan for any of Arkansas's 75
counties. Apply the `ar-statewide-format` baseline and the structure
below.

## The 28-circuit / 75-county structure

Under Amendment 80 (effective July 1, 2001), Arkansas's trial courts
are unified into a single **Circuit Court** of general jurisdiction,
organized into **28 judicial circuits** spanning **75 counties**. Each
circuit comprises one or more counties; a few large counties are a
circuit (or a subdistrict) of their own, while many circuits group
several smaller rural counties together. Within every county the Circuit
Court is administratively divided into the **five subject-matter
divisions** — criminal, civil, probate, domestic relations, and
juvenile — under the Supreme Court's administrative plan. There is **no
separate chancery, probate, or family court**: law and equity are
unified in Circuit Court.

## Confirming the circuit number and administrative plan

Because circuit composition and judge/division assignments are set by
administrative plan (and occasionally redistricted by the legislature),
**always confirm the current circuit number and local administrative
plan for the county at `arcourts.gov`** before captioning or filing. The
caption names the **county**, not the circuit number (`IN THE CIRCUIT
COURT OF [COUNTY] COUNTY, ARKANSAS`), but the circuit number determines
the administrative plan, judge assignments, chambers-copy expectations,
and scheduling procedure that govern the filing. The Arkansas county-
coded case-number format (`[county code]CV-[yy]-[####]`) applies in
every county; each county has its own two-digit code.

## Other most-populous counties (representative)

The counties below are the larger non-flagship counties; the listed
judicial circuit is a starting point — **verify the current circuit and
administrative plan at arcourts.gov**, as redistricting can move county
assignments.

| County | Seat | Judicial circuit |
|---|---|---|
| Faulkner | Conway | 20th |
| Saline | Benton (AR) | 22nd |
| Craighead | Jonesboro | 2nd |
| Sebastian | Fort Smith | 12th |
| Garland | Hot Springs | 18th |
| Lonoke | Lonoke | 23rd |
| White | Searcy | 17th |
| Jefferson | Pine Bluff | 11th |
| Crittenden | West Memphis | 2nd |
| Pope | Russellville | 5th |

Several of these counties share a circuit with neighbors (for example,
Craighead and Crittenden both sit in circuits with multiple counties),
and some circuits are subdistricted (East/West) — another reason to
confirm the plan rather than rely on a fixed number.

## Filing, chambers copies, and scheduling

All counties file through the statewide **eFlex** electronic-filing
system on the **Contexte** platform (Administrative Order No. 21);
confirm whether e-filing is mandatory for the case type and that each
PDF carries the **Administrative Order No. 19** redaction and
certificate of compliance. Whether a judge requires a **chambers copy**
of motion papers and how hearings are set vary by circuit
administrative plan and individual judges' practices — **defer to the
assigned judge's requirements and the circuit plan**, confirmed through
the county Circuit Clerk and arcourts.gov. See `ar-schedule-hearing` and
`ar-hearings`.

## Composition

- Format baseline: `ar-statewide-format`
- Flagship Circuit Court venues with their own overlay skills:
  `ar-pulaski`, `ar-benton`, `ar-washington`
- Limited-jurisdiction / small-claims / eviction matters (and de novo
  appeals up to these Circuit Courts): `ar-district-courts`
- Subject bundles that compose with these venues: `ar-consumer-debt`,
  `ar-family-law`, `ar-landlord-tenant`, `ar-personal-injury`,
  `ar-employment`, `ar-commercial-disputes`
- Pro se conventions: `ar-pro-se`; pre-filing QC: `ar-quality-check`

## References

- `ar-law-references` — Ark. R. Civ. P., Administrative Orders, and the
  county/circuit administrative-plan directory (confirm each county's
  circuit and plan at arcourts.gov)
