# oh-consumer-debt — Ohio CSPA counterclaim

## Prompt

Walk me through the Ohio Consumer Sales Practices Act as
a counterclaim against a debt-buyer plaintiff.

## Expected triggers

- `oh-consumer-debt`

## Acceptance criteria

- [ ] Cites **R.C. Chapter 1345** as the CSPA
- [ ] Confirms debt buyers are "suppliers" within CSPA
      coverage per *Brown v. Liberty Clubs*, 45 Ohio St.3d
      191 (1989)
- [ ] Cites **R.C. 1345.02** (unfair/deceptive) and
      **R.C. 1345.03** (unconscionable)
- [ ] Cites **OAC 109:4-3-11** — AG's debt-collection
      regulations
- [ ] Damages: **R.C. 1345.09(B)** — treble damages OR
      $200 per violation
- [ ] **Mandatory attorney's fees** for prevailing
      consumers under **R.C. 1345.09(F)** (where supplier
      acted knowingly)
- [ ] **2-year SOL** under **R.C. 1345.10(C)**
- [ ] Notes Ohio CSPA is significantly more powerful
      than federal FDCPA alone (treble damages with no
      cap)

## Common failure modes

- Confusing 2-year CSPA SOL with 6-year contract SOL
- Missing OAC 109:4-3-11
- Missing *Brown v. Liberty Clubs* cite
- Wrong damages framework
- Treating fees as discretionary (they are mandatory under
  R.C. 1345.09(F))
