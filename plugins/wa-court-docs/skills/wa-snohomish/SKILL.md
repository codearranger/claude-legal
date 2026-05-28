---
name: wa-snohomish
description: >
  Use when handling a Snohomish County, Washington
  Superior Court case — civil practice at the **Snohomish
  County Mission Building courthouse in Everett** (3000
  Rockefeller Avenue), Washington's third-most-populous
  county with ~830,000 residents. Snohomish County
  Superior Court handles general civil + family +
  criminal + juvenile matters with **Snohomish County
  Local Rules of Superior Court (SCLR)** overlaying the
  general CR + GR. Coverage includes Snohomish's **e-
  filing system**, the case-management order issued under
  SCLR 16, the family-law calendar at the Mission
  Building, the Snohomish County Family Law Commissioner
  system under RCW 2.24, Snohomish's participation in
  **Mandatory Arbitration of Civil Actions (MAR) under
  RCW 7.06** (current cap per RCW 7.06.020 and the local
  MAR order — read from the references corpus), and the
  Snohomish County General Order on remote hearings.
  Triggers include "Snohomish County Superior Court",
  "Everett Superior Court", "SCLR", "Snohomish local
  rules", "Snohomish County e-filing", "Snohomish County
  family law", "Snohomish MAR".
version: 0.2.0
---

# Snohomish County Superior Court — Venue Skill

> **NOT LEGAL ADVICE.** SCLR motion-timing, MAR caps,
> and revision-motion windows are amended periodically.
> Current values live in the references corpus
> (`court-rules/`, `wa-rcw-debt/`) — this skill names
> the controlling sources without embedding the day
> counts.

## At a glance

- **Court**: Snohomish County Superior Court
- **Address**: Mission Building, 3000 Rockefeller
  Avenue, Everett, WA 98201
- **Population served**: ~830,000 (third-largest
  Washington county)
- **Jurisdiction**: General-jurisdiction trial court
  (RCW 2.08) — civil, family, criminal, juvenile,
  probate
- **Appellate context**: appeals route to Court of
  Appeals **Division I** (Seattle)

## Local rules

**Snohomish County Local Rules of Superior Court
(SCLR)** overlay the statewide CR + GR.

### SCLR 4 — Initial filings

- Civil cover sheet
- Confidential information form per GR 22

### SCLR 7 — Motion practice

SCLR 7 sets the motion-day timing (motion / response /
reply schedule). **Read the current schedule from
`wa-law-references/references/court-rules/`** (or hand
off to `wa-deadlines`) rather than relying on memory.
Working copies to assigned judge.

### SCLR 16 — Case scheduling

Standing case-management order issued by court setting:

- Status conference
- Discovery cutoff
- Pretrial conference
- Trial date

### Snohomish family-law local rules

Separate family-law local rules — temporary orders,
parenting evaluators, family-law-commissioner practice.

## E-filing

Snohomish County requires e-filing for represented
parties. Pro se parties may use paper filings or
e-filing through the County clerk's portal. Filing
fees per RCW 36.18.020.

## Mandatory Arbitration of Civil Actions — RCW 7.06 + MAR

Snohomish County **participates** in mandatory
arbitration. Civil cases below the local jurisdictional
cap are referred to arbitration. **The cap and the
trial-de-novo window are set by RCW 7.06 and the WA MAR;
read current values from `RCW-7_06.md` and
`court-rules/MAR.md`** rather than relying on memory.

## Commissioners

Snohomish uses commissioners (RCW 2.24) for ex parte,
family-law motions, civil protection orders under RCW
7.105, and some general-civil motions.

**Revision motion** to challenge a commissioner ruling
is governed by RCW 2.24.050. **Read the current revision-
motion window from `RCW-2_24.md`** or hand off to
`wa-deadlines`.

## Remote appearances

Snohomish maintains a General Order on Remote
Appearances. WebEx is the dominant platform; check
specific judge's standing order.

## Family law

Snohomish County has a dedicated family-law calendar at
the Mission Building. Family Law Facilitator available
under RCW 26.12.180.

## Composition with other wa- skills

- `wa-statewide-format` — CR + GR 14
- `wa-deadlines` — current SCLR motion timing + RCW
  2.24.050 revision-motion window
- `wa-discovery` — CR 26-37
- `wa-first-30-days` — answer (current day count via
  `wa-deadlines`)
- `wa-family-court` + `wa-family-law`
- Subject-matter bundles (consumer-debt, L&T, PI,
  employment, commercial)
- `wa-fact-check`
