---
name: ca-ocsc
description: >
  Use when drafting or filing in Orange County Superior Court (OCSC),
  California's third-largest superior court serving approximately
  3.2 million residents. Triggers include "Orange County Superior Court",
  "OCSC", "Central Justice Center Santa Ana", "Harbor Justice Center
  Newport Beach", "Lamoreaux Justice Center Orange", "West Justice
  Center Westminster", "North Justice Center Fullerton", "OCSC tentative
  ruling", "OCSC eFiling", "File and ServeXpress Orange County", "Orange
  County local rules", or any OCSC case number (e.g.,
  30-2024-NNNNNNN-CU-BC-CJC). Covers OCSC local rules, tentative-ruling
  practice, mandatory eFiling, courthouse divisions, and case management
  procedures. Layer on top of `ca-statewide-format`.
version: 0.1.0
---

# Orange County Superior Court (OCSC)

Use this skill in addition to `ca-statewide-format` when the
case is in the Orange County Superior Court. OCSC serves Orange
County (approximately 3.2 million residents) and is consistently
among the three highest-volume superior courts in California.

## Court locations and civil divisions

| Courthouse | Address | Civil jurisdiction |
|---|---|---|
| **Central Justice Center (CJC)** | 700 Civic Center Drive West, Santa Ana 92701 | Unlimited civil, complex civil, all CJC filings |
| **Harbor Justice Center (HJC)** | 4601 Jamboree Road, Newport Beach 92660 | Unlimited civil (Harbor district) |
| **Lamoreaux Justice Center (LJC)** | 341 The City Drive South, Orange 92868 | Unlimited civil (Central/East Orange County) |
| **West Justice Center (WJC)** | 8141 13th St., Westminster 92683 | Limited civil, unlawful detainer (West OC) |
| **North Justice Center (NJC)** | 1275 N. Berkeley Ave., Fullerton 92832 | Unlimited civil (North OC) |

**Venue within OC**: CCP § 395 governs — file where the defendant
resides or where the contract was to be performed. For consumer-debt
cases, CCP § 395(b) requires filing where the defendant-debtor signed
the contract or resided at the time of the transaction. Confirm
the assigned courthouse using the OCSC case portal.

## Case number format

OCSC case numbers: `30-YYYY-NNNNNNN-CU-[type]-[courthouse code]`
Example: `30-2024-01234567-CU-BC-CJC` (breach of contract, Central
Justice Center).

Courthouse codes: CJC (Central), HJC (Harbor), LJC (Lamoreaux),
WJC (West), NJC (North).

Pull exact case information from **https://www.occourts.org**.

## Caption — OCSC variant

```
      SUPERIOR COURT OF CALIFORNIA
           COUNTY OF ORANGE
     [Courthouse name, e.g., Central Justice Center]
```

Department number appears after the caption when known. Check the
"Case Access" portal at `occourts.org` for the assigned department.

## Mandatory eFiling — File & ServeXpress (FSX)

OCSC requires electronic filing for unlimited civil cases via
**File & ServeXpress**: `https://www.fileandservexpress.com`

- Self-represented litigants: may use FSX or file paper at the
  clerk's window (9:00 a.m. – 4:00 p.m., M–F, closed court holidays)
- Filing cut-off for same-business-day processing: **5:00 p.m.** PST
  on a court day (filings after 5:00 p.m. or on a non-court day are
  deemed filed the next court day — CRC 2.259(a))
- Current fee schedule: `https://www.occourts.org/general-public/fees`

## Law and motion — tentative rulings

OCSC posts tentative rulings on the court website by **1:30 p.m.**
the court day before the hearing.

Tentative-ruling access: `https://www.occourts.org/online-services/tentative-rulings`

### Contesting a tentative

A party wishing to contest the tentative must **notify** the
courtroom clerk AND all opposing parties **by 4:00 p.m.** the court
day before the hearing. If no notice is given, the tentative becomes
the order. Individual departments may post modified tentative-ruling
procedures on the court website.

## Complex civil litigation

OCSC has a dedicated **Complex Civil Litigation Program (CCLP)**
at the Central Justice Center. Complex designation (class actions,
mass torts, antitrust, securities, large construction disputes, etc.)
is governed by OCSC Local Rules 3.401-3.410. Designation request is
made at the time of filing or shortly thereafter.

## Case Management Conferences

OCSC schedules a **CMC** approximately 120-180 days after filing.
Parties must file a Case Management Statement (CM-110) at least
**15 calendar days** before the CMC. The CMC order sets discovery,
expert, and trial scheduling. Active case management is emphasized
under OCSC's trial-delay reduction program.

## Key OCSC local rules

OCSC Local Rules: `https://www.occourts.org/media/pdf/local-rules.pdf`

| Rule area | Coverage |
|---|---|
| General civil rules | CJC, HJC, NJC, LJC, WJC specifics |
| Complex civil | Rules 3.401-3.410 |
| Law and motion | General and department-specific |
| Trial | Pretrial requirements; trial-setting procedures |
| Family law | Separate chapter (OC Family Court at CJC / LJC) |
| Probate | Separate chapter at CJC |

OC Local Rules are updated periodically — always verify against the
current version on the court's website.

## Composition

Layer on `ca-statewide-format` for all OCSC civil filings. Compose with:
- `ca-consumer-debt` — consumer-debt cases (high-volume UD docket at
  WJC for North/West OC; CJC for Central OC)
- `ca-landlord-tenant` — UD cases (WJC is the primary UD venue for
  West Orange County; LJC for Central/East OC)
- `ca-family-law` — Orange County Family Court (CJC and LJC; Orange
  County Family Court Services mediation program)
- `ca-deadlines` — OCSC holiday closure calendar; CCP § 12 arithmetic
