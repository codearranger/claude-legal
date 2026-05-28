# Integration — End-to-end motion-to-compel packet

## Prompt

I served Civ. R. 33 interrogatories and Civ. R. 34 RFPs
on the plaintiff (LVNV Funding LLC) on April 1, 2025,
in my Hamilton County Common Pleas case. They have not
responded. I sent a meet-and-confer letter on May 7,
2025 — no response. Build me the motion-to-compel packet
for filing today, May 15, 2025: motion + supporting
affidavit + proposed order + certificate of service.
Pro se.

## Expected triggers

- `oh-discovery`
- `oh-draft-motion`
- `oh-draft-declaration`
- `oh-draft-order`
- `oh-hamil`
- `oh-statewide-format`
- `oh-pro-se`
- `oh-file-packet`

## Acceptance criteria

### Motion

- [ ] Caption per Civ. R. 10(A) (Hamilton County Common
      Pleas)
- [ ] Cites **Civ. R. 37(A)** + **Civ. R. 37(E)** good-
      faith conferral
- [ ] Recites the discovery served + dates; absence of
      response; meet-and-confer (May 7) + lack of response
- [ ] Prays for: order compelling responses within ≤ 14
      days; fees + costs under Civ. R. 37(A)(5)(a);
      sanctions reserved under Civ. R. 37(B)
- [ ] Certificate of service

### Affidavit

- [ ] Notarized (R.C. 2319.04)
- [ ] Authenticates the served-discovery exhibits + the
      meet-and-confer letter exhibit
- [ ] Personal-knowledge basis

### Proposed order

- [ ] Caption matches motion
- [ ] Operative IT IS ORDERED provisions with date-
      certain deadlines
- [ ] Judge / Magistrate signature line

### Packet integrity

- [ ] Caption + case number consistent
- [ ] Exhibits referenced are actually attached
- [ ] No PII beyond what redaction rules allow
- [ ] Filing-fee + chambers-copy plan addressed

## Common failure modes

- Skipping the Civ. R. 37(E) good-faith-conferral recital
- Missing affidavit
- Unnotarized affidavit
- Caption mismatch between motion and proposed order
- Federal FRCP 37 cited instead of Ohio Civ. R. 37
- Proposed order overbroad relative to motion's prayer
