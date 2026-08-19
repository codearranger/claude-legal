---
name: ca-sdsc
description: >
  Use when drafting or filing in San Diego Superior Court (SDSC),
  the second-busiest California superior court serving 3.3 million
  residents. Triggers include "San Diego Superior Court", "SDSC",
  "Hall of Justice San Diego", "Central Courthouse San Diego",
  "Kearny Mesa courthouse", "El Cajon courthouse", "Vista courthouse",
  "North County courthouse San Diego", "Chula Vista courthouse",
  "San Diego tentative ruling", "SDSC eFiling", "eFileSD",
  "File and ServeXpress San Diego", "San Diego local rules CRC",
  or any case with an SDSC case number (e.g., 2024-00123456,
  37-2024-NNNNNNN). Covers SDSC local rules, tentative-ruling
  practice, mandatory eFiling through File & ServeXpress (FSX),
  courthouse divisions, and case management conferences.
  Layer on top of `ca-statewide-format`.
version: 0.1.0
---

# San Diego Superior Court (SDSC)

Use this skill in addition to `ca-statewide-format` when the
case is in the San Diego Superior Court. SDSC serves San Diego
County (approximately 3.3 million residents) and handles one
of the highest civil case volumes in California outside Los
Angeles County.

## Court locations and civil divisions

| Courthouse | Address | Civil case types |
|---|---|---|
| **Central Courthouse** (Hall of Justice) | 1100 Union St., San Diego 92101 | Unlimited civil (general); law and motion; complex civil |
| **Kearny Mesa Courthouse** | 8950 Clairemont Mesa Blvd., San Diego 92123 | Unlimited civil (north central divisions) |
| **El Cajon Courthouse** | 250 E. Main St., El Cajon 92020 | Unlimited civil (East County) |
| **Vista Courthouse** | 325 S. Melrose Dr., Vista 92081 | Unlimited civil (North County) |
| **Chula Vista Courthouse** | 500 3rd Ave., Chula Vista 91910 | Unlimited civil (South County) |
| **North County Division** (Oceanside) | 321 S. Nevada St., Oceanside 92054 | Unlimited civil (Coastal North) |

**Case assignment**: the Initial Case Management Conference (ICMC)
determines the courthouse and department assignment based on the
plaintiff's address, defendant's address, and the nature of the case.
Confirm the assigned courthouse and department on the SDSC case portal.

## Case number format

SDSC uses two formats:
- **Long form**: `37-YYYY-NNNNNN-CU-[type]-[region]`
  (e.g., `37-2024-00123456-CU-BC-CTL` for breach of contract, Central)
- **Short form**: `YYYY-NNNNNNN` in some filings

Pull the exact case number from **https://www.sdcourt.ca.gov** by
searching under "Civil Division / Case Inquiry."

## Caption — SDSC variant

```
         SUPERIOR COURT OF CALIFORNIA
              COUNTY OF SAN DIEGO
             [Courthouse Name] Division
```

The Department number (e.g., "Department C-65") appears in the caption
block after the county line when the department is known.

## Mandatory eFiling — File & ServeXpress (FSX)

SDSC mandates electronic filing for represented parties in unlimited
civil cases via **File & ServeXpress (FSX)**: `https://www.fileandservexpress.com`

- Pro se litigants may file electronically or in paper (paper still
  accepted at the clerk's window)
- Emergency / ex parte filings may be submitted directly at the
  clerk's window even if FSX is down
- Filing hours: FSX accepts filings 24/7; the clerk's acceptance
  cut-off for same-day processing is **4:00 p.m.** local time
- Filing fee: unlimited civil cases, verify current fees at
  `https://www.sdcourt.ca.gov/sdcourt/civil` (baseline CRC schedules)

## Law and motion — tentative rulings

SDSC uses a **tentative-ruling regime** for most civil law-and-motion
matters. Tentative rulings are posted **by 1:30 p.m.** on the court
day before the hearing. Access tentative rulings at:
`https://www.sdcourt.ca.gov/sdcourt/civil/tentativerulings`

### Responding to tentatives

If **no party contests** the tentative by **4:00 p.m.** on the court
day before the hearing, the tentative becomes the order without
argument. To contest:
1. Notify all opposing parties AND the courtroom clerk by telephone
   (or by email per the department's posted procedures)
2. Both sides must appear at the hearing
3. A party who failed to notify waives the right to argue

**Exception**: some departments post their own tentative-ruling
procedures (check the department's "Civil Procedures" link on the
SDSC website).

## Complex civil litigation

SDSC has a **Complex Civil Litigation Division** at the Central
Courthouse. Cases assigned to the complex program (class actions,
antitrust, mass torts, construction defect over $25M, securities,
insurance coverage, and similar matters) follow the SDSC Complex
Program rules posted on the court's website. Local Rule 2.1.9
governs designation requests.

## Case Management Conference (CMC)

SDSC schedules a **Case Management Conference (CMC)** approximately
120-150 days after filing. Parties must file a Case Management
Statement (CM-110) at least **15 calendar days** before the CMC.
The CMC sets the discovery cut-off, expert designation dates,
trial date, and any additional case management orders.

## ADR program

SDSC operates a robust **Alternative Dispute Resolution (ADR)** program.
The court maintains a list of approved mediators and arbitrators. Parties
may be ordered into ADR at the CMC. For judicial arbitration under CCP
§ 1141.10: cases at or below the current jurisdictional cap are subject
to mandatory judicial arbitration (currently $25,000 in SDSC — verify).

## Key SDSC local rules

SDSC has adopted local rules (SDSC Local Rules, available at
`https://www.sdcourt.ca.gov/sdcourt/general/rules`) that supplement
the California Rules of Court. Key provisions:

| Rule area | SDSC Local Rule |
|---|---|
| General civil — e-filing | Local Rule 2.1.6 |
| Case management | Local Rule 2.1.8 |
| Complex civil | Local Rule 2.1.9 |
| Law and motion | Local Rules 2.1.14-2.1.16 |
| Trial | Local Rules 2.1.17-2.1.22 |
| Unlawful detainer | Local Rules 2.2.1-2.2.5 |
| Family law | Local Rules 5.1.1 et seq. |
| Probate | Local Rules 7.1 et seq. |

Always confirm current local rules against the SDSC website — local
rules are amended periodically.

## Composition

Layer this skill on `ca-statewide-format` for all SDSC civil filings.
Compose with:
- `ca-consumer-debt` — for SDSC consumer-debt cases
- `ca-landlord-tenant` — for SDSC UD cases (SDSC has an active UD
  docket at multiple courthouses)
- `ca-family-law` — for SDSC family cases (Family Court Services
  at Central Courthouse + South Bay Family Court in Chula Vista)
- `ca-deadlines` — CCP § 12 deadline arithmetic + court-closure
  calendar (SDSC posts its own holiday closure calendar)
