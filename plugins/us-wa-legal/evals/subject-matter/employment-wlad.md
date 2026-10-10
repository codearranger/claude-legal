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
- [ ] Confirms employer coverage: WLAD covers smaller employers
      than federal Title VII — checks the current employee-count
      threshold against the 10-employee restaurant size (read from
      `wa-law-references/references/wa-rcw-debt/RCW-49_60.md`)
- [ ] Identifies **sex / pregnancy** as protected class under
      WLAD
- [ ] Walks possible claims: pregnancy discrimination (disparate
      treatment); hostile work environment (severe-OR-pervasive);
      retaliation under RCW 49.60.210 for protected activity
      (requesting medical leave)
- [ ] Notes **no statutory damages cap** under WLAD (a structural
      feature, distinct from federal Title VII)
- [ ] Notes **mandatory attorney's fees** for prevailing
      plaintiff
- [ ] Walks remedies: file with WSHRC within the WSHRC filing
      window OR file directly in court; the SOL for direct court
      action is RCW 4.16's general PI SOL per *Antonius v. King
      County*. Day counts in `RCW-49_60.md` and `RCW-4_16.md`.
- [ ] References Healthy Starts Act for pregnancy accommodation

## Common failure modes

- Treating federal Title VII as the primary cause of action
  (WLAD is broader, has more damages, has mandatory fees)
- Stating employer not covered without checking current threshold
- Missing the WSHRC filing-window clock
- Wrong SOL
