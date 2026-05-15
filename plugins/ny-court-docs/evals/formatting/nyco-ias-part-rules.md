# ny-nyco — NY County Supreme Court IAS Part Rules

## Prompt

I'm about to file a motion in 60 Centre Street. The Index
shows it's been assigned to IAS Part 38. What do I need to
check before I file?

## Expected triggers

- `ny-nyco`
- `ny-statewide-format`

## Acceptance criteria

- [ ] Identifies **60 Centre Street** as NY County Supreme
      Court (Civil Term, "1st JD" / 1st JD overlay)
- [ ] Explains 22 NYCRR § 202.3 Individual Assignment System
      (IAS) — case stays with one Justice from assignment to
      disposition
- [ ] Directs litigant to look up **the Justice's Part
      Rules** before filing (NYCO publishes per-Part Rules at
      `https://ww2.nycourts.gov/courts/1jd/supctmanh/Justices.shtml`)
- [ ] Notes the Commercial Division threshold for NY County
      ($500,000 — the highest in the state)
- [ ] Mentions NYSCEF as the default e-filing system
- [ ] Notes that **working copies** of motion papers may be
      required by some Parts (varies by Justice)

## Common failure modes

- Treats NYCO like a federal court (no IAS system; no
  Part Rules concept)
- Wrong Commercial Division threshold
- Forgets to direct user to Justice's Part Rules first
