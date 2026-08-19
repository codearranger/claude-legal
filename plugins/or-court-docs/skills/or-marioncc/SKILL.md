---
name: or-marioncc
description: >
  Use when drafting or filing in Marion County Circuit Court (Salem),
  Oregon's fourth-largest circuit court and the county seat of state
  government. Triggers include "Marion County Circuit Court", "Salem
  Oregon court", "Marion County Oregon civil case", "Salem courthouse
  Oregon", "Marion County OJIN", "Marion County OJD eCourt", "Salem
  Oregon civil litigation". Covers Marion County Circuit Court specifics —
  courthouse locations, civil departments, OJD eCourt eFiling, local
  supplemental local rules (SLR), scheduling, and hearing procedures.
  Layer on `or-statewide-format`.
version: 0.1.0
---

# Marion County Circuit Court

Use this skill in addition to `or-statewide-format` when the
case is in Marion County Circuit Court. Marion County (population
~340,000; county seat Salem, the Oregon state capital) is Oregon's
fourth-largest circuit court by civil caseload. Many state-agency
administrative proceedings have their judicial-review venue in
Marion County under ORS Chapter 183 (Administrative Procedures Act).

## Court location

| Location | Address |
|---|---|
| **Marion County Courthouse** | 100 High St. NE, Salem, OR 97301 |

Clerk's office: main floor. Phone: (503) 588-5105. Court website:
`https://www.courts.oregon.gov/courts/marion/Pages/default.aspx`

## eFiling — OJD eCourt (OJIN)

Marion County participates in **OJD eCourt** (Oregon's statewide
e-filing system): `https://ecourt.ojd.state.or.us`

- Mandatory eFiling for represented parties in civil cases
- Self-represented litigants may file electronically or in paper
- Filing cut-off: **4:30 p.m.** local time for same-day processing
- Service: eFiled documents serve registered parties electronically
  through OJD eCourt

## Administrative-law appeals — ORS Chapter 183

A distinctive feature of Marion County Circuit Court is its role as
the **venue for judicial review of Oregon agency final orders** under
ORS 183.480-183.500. When an agency issues a final order in a contested
case, a person aggrieved may petition the circuit court in:
- **Marion County** (the primary venue — where the agency maintains
  its principal office), **or**
- The county where the petitioner resides or does business

**ORS 183.484 procedure**:
1. File a **Petition for Judicial Review** within **60 days** of the
   effective date of the agency's final order (ORS 183.484(1))
2. Serve the agency and the Attorney General
3. The agency must file the administrative record within 30 days
4. Briefing schedule and argument set by the court

This makes Marion County a significant venue for professional-license
appeals, public-benefits (OHP, SNAP) appeals, regulatory matters, and
employment disputes involving state agencies.

## Civil departments and scheduling

Marion County civil judges handle the standard civil docket plus
the heavy administrative-review load. Key practices:
- **Law and motion calendar**: typically Tuesday or Wednesday mornings
  (verify with the clerk)
- **Summary judgment**: the court usually schedules oral argument on
  dispositive motions; confirm with the assigned judge's clerk
- **Arbitration**: Marion County participates in ORAM (Oregon
  Mandatory Arbitration) for cases within the jurisdictional cap

## Marion County SLR (Supplemental Local Rules)

Marion County's SLR is available at:
`https://www.courts.oregon.gov/courts/marion/Pages/localrules.aspx`

Key provisions cover ex parte motions, scheduling orders, and family-
law procedures. Verify the current SLR before filing.

## Composition

Layer on `or-statewide-format` for all Marion County filings:
- `or-consumer-debt` — active consumer-debt and debt-collection forum
- `or-family-law` — Marion County Family Court (separate family
  department; active caseload)
- `or-deadlines` — ORCP 10 + ORS 183.484 60-day APA petition window
  (for administrative review cases); ORS 187.010 holidays
- `or-pro-se` — Marion County Law Library is at the courthouse;
  Oregon State Bar Volunteer Lawyers Project (VLP) serves Salem
