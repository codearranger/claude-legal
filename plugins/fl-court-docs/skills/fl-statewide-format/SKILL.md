---
name: fl-statewide-format
description: >
  Apply Florida statewide pleading format — Fla. R. Civ. P. 1.100 caption and 1.080 signature block, PACE mandatory e-filing, court-paper requirements. Triggers include 'Florida pleading format', 'Fla. R. Civ. P. 1.100', 'Florida caption', 'PACE Florida eFiling', 'Florida mandatory e-filing'.
version: 0.1.0
---

# Florida Statewide Pleading Format

Florida trial-court pleading format is governed primarily by the
**Florida Rules of Civil Procedure (Fla. R. Civ. P.)** and the
**Florida Rules of Court** for case administration.

## Key formatting rules

### Fla. R. Civ. P. 1.100 — Pleadings and Motions

All pleadings and motions must be:
- Dated and **signed** by the attorney of record or the
  party (if pro se), with the party's address, phone, and
  Florida Bar number (if attorney) — Rule 1.030
- The **caption** includes: court name, case number, division
  letter (in multi-division counties like Miami-Dade and
  Broward), and the nature of the pleading
- **Double-spaced** (or readable equivalent); 12-point or
  larger font; 1-inch margins; 8.5 x 11 white paper

### Florida caption standard

```
     IN THE CIRCUIT COURT OF THE [Nth] JUDICIAL CIRCUIT
              IN AND FOR [COUNTY] COUNTY, FLORIDA

[PLAINTIFF NAME],
         Plaintiff,             Case No.: [YYYY-CA-NNNNNN]
                                Division: [letter]
v.

[DEFENDANT NAME],
         Defendant.
_________________________________/
```

The distinctive **"v."** format with the closing
underscore line is standard in Florida captions.

For **County Court** (limited civil, ≤ $50,000):
```
     IN THE COUNTY COURT IN AND FOR [COUNTY] COUNTY, FLORIDA
```

### PACE — mandatory e-filing

Florida mandates electronic filing through the **Florida
Courts E-Filing Portal (PACE)** for all civil cases:
`https://myflcourtaccess.flcourts.org`

- Self-represented litigants may file electronically or
  in paper (some courts still accept paper from pro se)
- Filing cut-off for same-day processing: varies by
  circuit — most courts accept until **11:59 p.m.**
  via PACE (document deemed filed when received by the
  portal, not when processed by the clerk — Fla. R.
  Jud. Admin. 2.525)
- Service via PACE: e-service through the portal is
  required for parties registered in the portal

## Composition

- `fl-statewide-format` is the base layer for all FL skills
- Layer court-specific skills (fl-miami-dade, fl-broward,
  fl-orange, fl-county-courts) on top

