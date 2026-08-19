---
name: fl-fact-check
description: >
  Florida pre-filing fact-check skill — verifies Florida case citations, statutory cites, SOL arithmetic, FCCPA/FDUTPA applicability, and packet completeness before filing. Triggers include 'Florida fact check', 'verify Florida citation', 'check Florida SOL', 'Florida filing checklist'.
version: 0.1.0
---

# Florida Fact-Check

Run this skill on every draft before filing.

## Checklist

### Format check
- [ ] Caption format: `IN THE [CIRCUIT/COUNTY] COURT...IN AND FOR [COUNTY] COUNTY, FLORIDA`
- [ ] Caption ends with underscore line and `/`
- [ ] Case number in correct format for this court (verify on court portal)
- [ ] Division letter present where required
- [ ] Document dated and signed with address/phone (Rule 1.030)
- [ ] Filed through PACE (or confirmed paper-filing is permitted)

### Citation verification
- [ ] Every case citation includes state court reporter (So. 3d) or
  federal reporter, with court and year
- [ ] Every statutory citation is to the **current** Florida Statutes
  (verify at `https://www.leg.state.fl.us/statutes/`)
- [ ] Rule citations use Fla. R. Civ. P. format (not Fed. R. Civ. P.)

### SOL and timeliness
- [ ] Identify the applicable SOL under § 95.11
- [ ] Confirm complaint is filed within the SOL
- [ ] For FCCPA claims: verify within 2-year SOL from violation
- [ ] For FDUTPA claims: verify within 4-year SOL

### Consumer-debt cases
- [ ] FCCPA § 559.72 prohibitions applicable to the conduct
- [ ] FDCPA parallel claims properly pled
- [ ] Chain of title / standing of plaintiff verified

### Service of process
- [ ] Sheriff or certified process server (not self-service)
- [ ] Proof of service filed within 120 days of filing (Rule 1.070(j))

