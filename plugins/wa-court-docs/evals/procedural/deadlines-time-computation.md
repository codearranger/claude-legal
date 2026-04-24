# wa-deadlines — Computing motion deadlines

## Prompt
I want to file a motion to compel in KCDC. The hearing is set for
Friday, May 15, 2026. What are my filing and service deadlines for the
motion, response, and reply?

## Expected triggers
- `wa-deadlines`
- `wa-law-references` (civil-rules.md — CRLJ 6(d))

## Acceptance criteria
- Cites **CRLJ 6(d)** (district court, not CR 6)
- Motion must be filed and served at least **5 court days** before the
  hearing
- Response at least **3 court days** before
- Reply no later than **noon the day before** the hearing
- Counts **court days** (excludes weekends and Washington court
  holidays)
- Recognizes that May 15, 2026 is a Friday; backing up 5 court days
  should land around Friday, May 8 (verify exact date against court
  holiday calendar)
- Does not confuse with superior court CR 6 timing (which uses
  different lead times)

## Common failure modes
- Using CR 6 lead times (14+ calendar days) for a district court case
- Counting calendar days instead of court days
- Forgetting the noon deadline for reply
- Missing Washington state holidays (MLK, Presidents Day, Memorial
  Day, Independence Day, Labor Day, Veterans Day, Thanksgiving + day
  after, Christmas, New Year's)
