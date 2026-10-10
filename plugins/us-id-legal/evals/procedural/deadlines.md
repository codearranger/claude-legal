# id-deadlines — time computation (I.R.C.P. 2.2) + holidays

## Prompt

I was served with a summons and complaint in an Idaho civil case on
Friday. When is my answer due, and how do I count the days?

## Expected triggers

- `id-deadlines`
- `id-first-30-days`

## Acceptance criteria

### Correct answer window

- [ ] States the answer is due **21 days** after service of the
      summons and complaint (I.R.C.P. 12(a)(1)(A))

### Correct time-computation rule (Idaho quirk)

- [ ] Computes time under **I.R.C.P. 2.2**, NOT "Rule 6" — and does
      not claim Idaho time computation lives at Rule 6 (Rule 6 is
      *[Reserved]* in Idaho)
- [ ] Applies the method: exclude the day of service, count every
      intervening day including weekends and holidays, include the
      last day, but if the last day is a Saturday, Sunday, or **legal
      holiday** roll forward to the next day that is not
- [ ] Notes the **+3 days** added when the period runs from service by
      mail (I.R.C.P. 2.2)

### Holidays

- [ ] Uses **Idaho Code § 73-108** legal holidays (and recognizes
      Columbus Day is observed and Juneteenth is not a state holiday)
      if a deadline lands on one

### Tooling

- [ ] Offers `scripts/case-calendar.py` (e.g.,
      `--rule answer-due`) and uses a valid named rule key

## Common failure modes

- Cites "I.R.C.P. 6" for time computation
- Uses a 20- or 30-day answer window instead of 21 days
- Adds Juneteenth as an Idaho state holiday
