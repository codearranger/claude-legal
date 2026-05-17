# wa-employment — WLAD discrimination claim

## Prompt

I work at a 10-employee Seattle restaurant. My boss has been
making demeaning comments about my pregnancy and just cut my
hours after I asked for time off for a doctor's appointment.
Do I have a claim?

## Expected triggers

- `wa-employment`
- `wa-kcsc`

## Acceptance criteria

- [ ] Identifies **Washington Law Against Discrimination
      (WLAD)** at RCW 49.60
- [ ] Confirms employer coverage: **WLAD covers employers
      with 8+ employees** under RCW 49.60.040(11) — broader
      than federal Title VII's 15+ threshold; a 10-employee
      restaurant IS covered
- [ ] Identifies **sex / pregnancy** as protected class under
      RCW 49.60.180
- [ ] Walks possible claims: pregnancy discrimination
      (disparate treatment); hostile work environment
      (severe-OR-pervasive); retaliation under RCW
      49.60.210 for protected activity (requesting medical
      leave)
- [ ] Notes **no statutory damages cap** under WLAD (vs.
      federal Title VII $300k cap)
- [ ] Notes **mandatory attorney's fees** for prevailing
      plaintiff under RCW 49.60.030(2)
- [ ] Walks remedies: file with WSHRC within 6 months OR
      file directly in court; **3-year SOL** for direct
      court action under RCW 4.16.080(2) per *Antonius v.
      King County*
- [ ] References **Healthy Starts Act** (RCW 49.86) for
      pregnancy accommodation requirements

## Common failure modes

- Treating federal Title VII as the primary cause of
  action (WLAD is broader, more damages, mandatory fees)
- Stating employer not covered (10 IS above 8-employee
  threshold)
- Missing the 6-month WSHRC clock
- Wrong SOL
