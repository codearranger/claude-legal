# mi-deadlines — Answer deadline under MCR 1.108 / MCR 2.108 with holiday roll-forward

## Prompt

I was personally served with a summons and complaint in
Michigan. I need to figure out exactly what day my answer is
due, and I'm worried because the deadline might land on a
weekend or one of those weird state holidays. Walk me through
the math.

## Expected triggers

- `mi-deadlines`
- `mi-first-30-days`

## Acceptance criteria

### The answer period (MCR 2.108)

- [ ] Identifies **MCR 2.108** as the rule setting the time to
      serve and file an answer, and notes the period **depends
      on the manner of service** (personal service vs. mail vs.
      out-of-state vs. service by publication) — cite MCR 2.108
      and **read the current day counts for each service mode
      from the references corpus** rather than asserting a single
      number from memory

### Time computation (MCR 1.108)

- [ ] Applies **MCR 1.108** time-computation rules: the day of
      the triggering act is excluded, the last day is included,
      and if the last day falls on a **Saturday, Sunday, or legal
      holiday**, the period **rolls forward** to the next day
      that is not a Saturday, Sunday, or legal holiday
- [ ] Notes the **mail-service add-on** where the triggering
      service was by mail (cite the controlling rule; read the
      current add-on from the corpus)

### Michigan legal holidays

- [ ] Uses the Michigan legal-holiday list for the roll-forward,
      and specifically flags Michigan-distinctive observances —
      **Lincoln's Birthday** and the **day after Thanksgiving** —
      that affect court-deadline computation; read the current
      holiday list from the references corpus rather than
      asserting it from memory
- [ ] Demonstrates a worked example: start date, count, and the
      rolled-forward due date

## Common failure modes

- Assumes one fixed answer period regardless of service mode
- Forgets to exclude the trigger day or to roll forward off a
  weekend/holiday
- Omits Lincoln's Birthday / day-after-Thanksgiving from the
  holiday set
- Asserts day counts and the holiday list from memory instead of
  reading them from the corpus
