# oh-consumer-debt — Fact-pattern triage

## Prompt

I was sued in Ohio Common Pleas by Midland Funding LLC.
They claim I owe $3,400 on a Capital One credit card. The
last payment on the account was in 2018. The complaint
was filed in 2025. What's my best defense strategy?

## Expected triggers

- `oh-consumer-debt`
- `oh-first-30-days`
- `oh-discovery`

## Acceptance criteria

- [ ] Identifies plaintiff as **debt buyer** (not original
      creditor) — triage to debt-buyer fact pattern
- [ ] Flags **SOL** issue under R.C. 2305.06 (6-yr
      written contract) — last payment 2018, filed 2025 =
      facially time-barred
- [ ] Flags **chain of title** as core defense (Midland
      bought from Capital One or intermediate)
- [ ] Notes Ohio CSPA **counterclaim** under R.C. 1345.09
      (treble + mandatory fees) if plaintiff's conduct
      violates R.C. 1345.02 / 1345.03 or OAC 109:4-3-11
- [ ] Notes federal **FDCPA** counterclaim against the
      debt buyer
- [ ] References authentication / foundation challenges
      under Evid. R. 803(6) / 901

## Common failure modes

- Missing SOL flag (the headline defense here)
- Missing CSPA counterclaim
- Treating Midland as original creditor (it is not)
- Skipping chain of title
