# az-deadlines — Rule 6 time computation + Rule 12(a) answer with a holiday roll-forward

## Prompt

I was served with a civil complaint in Arizona Superior Court. I
was personally served here in Arizona. How many days do I have to
answer, and how do I count them — what happens if the last day
lands on a weekend or a holiday?

## Expected triggers

- `az-deadlines`
- `az-first-30-days`

## Acceptance criteria

### Answer deadline (Rule 12(a))

- [ ] Identifies **Ariz. R. Civ. P. 12(a)** as the source of the
      answer deadline and distinguishes the **in-state service**
      period from the **out-of-state service** period (commonly
      framed as 20 vs. 30 days) — read the current day counts from
      the references corpus rather than asserting them
- [ ] Keys the deadline to the **manner/place of service** rather
      than assuming a single fixed number

### Time computation (Rule 6)

- [ ] Applies **Ariz. R. Civ. P. 6** computation: how to count the
      period (excluding/including the trigger day, counting calendar
      days) — read the current method from the corpus
- [ ] Applies the **roll-forward** rule: when the last day falls on
      a Saturday, Sunday, or **legal holiday**, the period runs to
      the next day that is not — and identifies the Arizona legal
      holidays from the corpus rather than asserting the holiday list
      from memory
- [ ] Notes any service-method add-on (e.g., additional time for
      service by mail) by citing the rule and reading the add-on
      from the corpus

### Honest sourcing

- [ ] Reads all day counts, the computation method, and the holiday
      list from the corpus; cites Arizona authority by rule number

## Common failure modes

- Asserts a single fixed answer period without distinguishing
  in-state vs. out-of-state service
- Asserts the holiday list or the mail add-on from memory
- Forgets the weekend/holiday roll-forward
