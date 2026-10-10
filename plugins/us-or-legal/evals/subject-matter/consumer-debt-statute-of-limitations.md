# or-consumer-debt — Statute of Limitations analysis

## Prompt

The debt buyer alleges I made a partial payment of $50 on
April 1, 2023, on an account that was charged off in 2017.
They say this restarted the 6-year SOL. Is that right under
Oregon law?

## Expected triggers

- `or-consumer-debt`
- `or-deadlines`

## Acceptance criteria

- [ ] Cites **ORS 12.080(1)** for the 6-year SOL
- [ ] Cites **ORS 12.230** for revival rules
- [ ] Correctly states that under ORS 12.230, **a partial
      payment alone does NOT revive the SOL** in Oregon
- [ ] Notes that only a **written promise to pay** can
      revive
- [ ] Distinguishes Oregon's rule from some other states
      where partial payment revives
- [ ] Identifies this as a potentially strong defense for
      the debtor

### Counterclaim implications

- [ ] If the SOL has run, suit on the debt may violate FDCPA
      § 1692e(5) and Reg F § 1006.26(b)
- [ ] Oregon UTPA (ORS 646.607(3)) — demanding payment not
      legally owed

## Common failure modes

- Treating partial payment as automatic revival (wrong for
  Oregon)
- Missing the ORS 12.230 written-promise requirement
- Citing Washington analog (RCW 4.16.270 — partial-payment
  revival; different rule)
- Generic "consult an attorney" without legal analysis
