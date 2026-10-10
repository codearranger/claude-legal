# Integration — End-to-end debt-defense answer packet

## Prompt

I was served a debt-collection complaint in Ohio
Common Pleas (Cuyahoga County) by Midland Funding LLC
yesterday, May 15, 2025. The complaint alleges $5,200
owed on a Capital One credit card. I don't recognize any
recent charges; the last payment I made was over 6
years ago. Build me the answer packet: answer + CSPA
counterclaim + affidavit + certificate of service.

## Expected triggers

- `oh-first-30-days`
- `oh-consumer-debt`
- `oh-draft-motion` (or `oh-draft-declaration`)
- `oh-statewide-format`
- `oh-cuya`
- `oh-pro-se`

## Acceptance criteria

### Across the packet

- [ ] Consistent caption (Cuyahoga County Common Pleas;
      Civ. R. 10(A))
- [ ] Consistent case number
- [ ] Consistent signature block (pro se, no Atty. Reg.
      #)
- [ ] All documents dated within the 28-day Civ. R.
      12(A)(1) window

### Answer

- [ ] Paragraph-by-paragraph denials / admissions
- [ ] Affirmative defenses including: SOL (R.C. 2305.06),
      lack of standing / chain of title, failure to state
      a claim
- [ ] **Counterclaim** under R.C. Chapter 1345 (Ohio
      CSPA) — alleges supplier status of debt buyer,
      identifies prohibited acts under R.C. 1345.02 /
      OAC 109:4-3-11, prays for treble damages + fees
      under R.C. 1345.09

### Affidavit

- [ ] Notarized (Ohio practice)
- [ ] R.C. 2319.04 form
- [ ] Personal-knowledge basis
- [ ] Authenticates exhibits if any

### Service

- [ ] Civ. R. 5(B) certificate
- [ ] Identifies mode of service

## Common failure modes

- Forgetting CSPA counterclaim entirely
- Citing federal FDCPA as if it were the primary
      counterclaim (FDCPA is parallel; CSPA is more
      powerful in Ohio)
- Unnotarized "declaration under penalty of perjury"
- Inconsistent caption / case number across documents
