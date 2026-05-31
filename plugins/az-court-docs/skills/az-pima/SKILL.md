---
name: az-pima
description: >
  This skill should be used when drafting or filing documents in
  the Pima County Superior Court in Tucson — Arizona's
  second-largest court. Triggers include "Pima County Superior
  Court", "file in Pima County", "sued in Pima County", "Tucson
  superior court", "Pima County courthouse", "Pima local rules",
  "Pima compulsory arbitration", "Pima County case number", and
  "Pima County scheduling order". Covers the court's general
  civil jurisdiction, the Pima County Superior Court local rules,
  the local-rule compulsory-arbitration jurisdictional limit,
  case-management / scheduling-order practice, AZTurboCourt
  e-filing, and case-type / case-number conventions. Layer on top
  of `az-statewide-format`.
version: 0.1.0
---

# Pima County Superior Court (Tucson)

> **NOT LEGAL ADVICE.** These notes describe the venue's
> procedural mechanics as a drafting aid, not legal advice.
> Local rules and judge-specific practices change; verify with
> the clerk and the current local rules before relying on
> anything here.

Use this skill in addition to `az-statewide-format` when the case
is in the **Pima County Superior Court**, seated in **Tucson**.
Pima is Arizona's second-most-populous county, and its Superior
Court is the state's second-largest, high-volume general-civil
trial court after Maricopa.

## Location and divisions

- The Superior Court sits in the **Pima County Superior Court /
  courthouse complex in downtown Tucson**. Confirm the current
  street address, division/courtroom, and any annex or remote
  hearing locations with the Clerk of the Superior Court before
  filing or appearing.
- Superior Court is Arizona's single court of general
  jurisdiction; Pima organizes its civil work into divisions
  presided over by individual judges, with court commissioners
  handling certain matters. Confirm your assigned division and the
  judge's individual practices before noticing anything.
- Family, probate/mental-health, and juvenile matters run on
  separate calendars and rules — see `az-family-court` /
  `az-family-law`. This skill addresses the **general civil** side.

## Jurisdiction

- The Superior Court hears general civil actions; the **Pima
  County Justice Courts** handle lower-value civil claims and
  evictions (see `az-justice-courts`). Confirm the
  amount-in-controversy threshold and any small-claims overlap
  before choosing the forum.
- Equity, special actions, and appeals from the limited-
  jurisdiction courts also lie in Superior Court.

## Compulsory arbitration (local-rule limit)

- Arizona's compulsory-arbitration program runs under **A.R.S.
  § 12-133** and **Ariz. R. Civ. P. 72–77**, with each county's
  Superior Court setting the **jurisdictional dollar limit by
  local rule**. Pima County sets its own threshold by local rule.
- A civil case at or below the Pima limit is **assigned to
  compulsory arbitration** and proceeds through an arbitrator
  before any trial; an appeal from the award is a **trial de novo**
  in Superior Court. Pleading the amount in controversy (or a
  certificate as to compulsory arbitration) drives this routing.
- **Do not hard-code the dollar figure** — it is set by Pima local
  rule and revised periodically. Read the current limit from the
  Pima County Superior Court local rules in `az-law-references`,
  and confirm with the clerk. For the substantive
  arbitration/ADR framework see `az-commercial-disputes` and
  `az-hearings`.

## Pima County Superior Court local rules

- Beyond the statewide Arizona Rules of Civil Procedure, Pima
  County Superior Court operates under its **own local rules**
  (adopted under the supervision of the Arizona Supreme Court),
  which govern case assignment, motion practice, the compulsory-
  arbitration threshold, scheduling, and local filing conventions.
- Read the current Pima local rules from the corpus in
  `az-law-references` before relying on any page limit, conferral
  requirement, or motion-call procedure. Where the corpus is a
  pointer stub rather than verbatim text, **confirm the current
  rule with the clerk or the court's website**.

## Case-type and case-number conventions

- Pima Superior Court civil case numbers follow Arizona's Superior
  Court pattern — generally a county/court designator, a two- or
  four-digit year, a case-type code, and a sequential number.
  **Confirm the exact case-type code and number format the Pima
  clerk assigns** for your cause of action; the case-type code
  drives docket routing and the arbitration determination.
- Once assigned, the case number anchors the caption per
  `az-statewide-format`. **Do not guess the case-type code** —
  verify it against the Pima clerk's intake practice.

## Case management and scheduling orders

- After the case is at issue, the court manages civil cases through
  **case-management and scheduling orders** setting discovery
  cutoffs, disclosure deadlines (Arizona's Rule 26.1 mandatory
  disclosure), motion and dispositive-motion dates, ADR/arbitration
  milestones, and the trial date.
- **Calendar your obligations from the scheduling order entered in
  your specific case**, not from a generic template, and confirm
  the assigned judge's individual practices, motion-call day, and
  any chambers-copy or lodging requirement. See
  `az-schedule-hearing`, `az-hearings`, and `az-deadlines`.

**Agent behavior:** before drafting a notice of hearing, setting a
page-limited brief, or calendaring a deadline, read the current
Pima County Superior Court local rules in `az-law-references`, the
scheduling order entered in the case, and the assigned judge's
practices. Confirm the compulsory-arbitration limit, motion-call
procedure, and any chambers-copy requirement with the clerk.

## E-filing — AZTurboCourt

- Arizona's statewide electronic-filing platform is
  **AZTurboCourt**. Pima County Superior Court accepts civil
  filings through AZTurboCourt; confirm whether e-filing is
  **mandatory** for your case type and party, the current
  document-type selections, and the filing-fee / fee-waiver
  workflow with the clerk.
- See `az-file-packet` for packet assembly and preflight and
  `az-statewide-format` for the statewide document-format
  requirements.

## Composition

- For statewide format and the caption: `az-statewide-format`
- For other Arizona venues: `az-maricopa` (Phoenix),
  `az-superior-courts` (other counties), `az-justice-courts`
  (limited-jurisdiction / evictions)
- For the first responsive pleading: `az-first-30-days`
- For drafting motions / declarations / notices / orders:
  `az-draft-motion`, `az-draft-declaration`, `az-draft-note`,
  `az-draft-order`
- For discovery and Rule 26.1 disclosure: `az-discovery`
- For scheduling and hearings: `az-schedule-hearing`,
  `az-hearings`; deadlines: `az-deadlines`
- For arbitration/ADR substance: `az-commercial-disputes`
- For filing mechanics: `az-file-packet`; pre-filing QC:
  `az-quality-check`; citation/quote checking: `az-fact-check`
- For pro se conventions: `az-pro-se`

## References

- `az-law-references` — Ariz. R. Civ. P., Ariz. R. Evid., A.R.S.
  (incl. § 12-133 compulsory arbitration), and the Pima County
  Superior Court local-rules corpus
- Pima County Superior Court local rules and the assigned judge's
  individual practices (confirm current versions with the clerk
  and the court's website, sc.pima.gov)
