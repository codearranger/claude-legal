# wa-personal-injury — Comparative fault + several liability

## Prompt

I was rear-ended in Tacoma. The other driver was clearly at
fault but the police said I had a brake light out. I have
$50,000 in medical bills. Can I still recover?

## Expected triggers

- `wa-personal-injury`
- `wa-pierce`

## Acceptance criteria

- [ ] Identifies Washington as **pure comparative fault**
      state under RCW 4.22.005
- [ ] Explains: plaintiff recovers reduced by plaintiff's
      own fault — even at 99% at fault, plaintiff still
      recovers 1%
- [ ] Contrasts with **modified comparative fault** states
      (50% / 51% bar — most other states)
- [ ] Walks application: if jury finds plaintiff 10% at
      fault (brake light), defendant 90% at fault, plaintiff
      recovers 90% of damages
- [ ] Identifies **RCW 4.22.070** several-liability rule
      (post-1986 Reform Act) — defendant pays only their
      proportional share unless concert-of-action / agency /
      vicarious / non-delegable duty / damages caused
      intentionally
- [ ] Notes the **3-year SOL** under RCW 4.16.080(2) for
      ordinary tort
- [ ] Notes practical concerns: PIP coverage; settlement
      vs. trial; comparative-fault discovery

## Common failure modes

- Stating contributory negligence bars recovery (wrong —
  that's a different rule)
- Stating 51% bar (wrong — WA is pure, no bar)
- Wrong SOL
- Treating defendants as jointly liable for all damages
