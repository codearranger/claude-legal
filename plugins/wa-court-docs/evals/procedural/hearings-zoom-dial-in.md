# wa-hearings — Remote hearing logistics

## Prompt
My motion is set for KCDC Burien Division on [date]. How do I appear
remotely?

## Expected triggers
- `wa-hearings`
- `wa-kcdc` (division-specific references)

## Acceptance criteria
- Identifies the **Burien Division** (South Division)
- Provides the Zoom link / dial-in / meeting ID for the Burien civil
  motion docket (or directs user to the current KCDC page if data
  could have changed)
- Notes that the Judge is Laumann (BU2)
- Notes the **KCDC.CivilMGT@kingcounty.gov** routing address for
  confirmation and working copies
- Notes GR 14 / KCDCLCR remote-appearance rules (camera on, proper
  appearance, "silent and visible" expectations)
- Reminds user to test audio/video in advance, join 10 minutes early
- Reminds user to file a Note for Motion Docket with correct hearing
  date

## Common failure modes
- Giving stale or fabricated Zoom details (should point to current
  KCDC page if uncertain)
- Wrong judge or division
- Omitting the CivilMGT routing address
- Missing working-copy requirement
