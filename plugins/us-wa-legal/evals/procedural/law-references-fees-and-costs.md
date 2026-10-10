# wa-law-references — Fees and Costs

## Prompt
My contract with the plaintiff has a clause that says if they sue me
and win, I pay their attorney fees. I won on a motion to dismiss. Can
I recover my fees even though I'm pro se?

## Expected triggers
- `wa-law-references` (fees-and-costs.md)

## Acceptance criteria
- Cites **RCW 4.84.330** — reciprocal fee-shifting statute
- Explains that unilateral contract fee clauses are made reciprocal by
  operation of the statute
- Cites *Mellor v. Chamberlin* as the leading authority
- Addresses the **pro se limitation**: pro se parties generally cannot
  recover attorney fees for their own time, but can recover statutory
  costs under RCW 4.84.010 and, where applicable, statutory attorney
  fees under RCW 4.84.080
- Does **not** claim pro se can bill their time under the lodestar
  method

## Common failure modes
- Telling the user they can charge hourly for their own time
- Omitting the pro se limitation entirely
- Missing *Mellor v. Chamberlin*
- Citing only the contract clause without RCW 4.84.330
