# in-deadlines — T.R. 6(A) time computation + Indiana holidays

## Prompt

I need to calculate several deadlines in my Indiana civil
case: when my response to a summary-judgment motion is due,
when a T.R. 59 motion to correct error must be filed after
a judgment, and whether Indiana courts are closed on Good
Friday and Election Day. I was served by certified mail on
a Monday.

## Expected triggers

- `in-deadlines`

## Acceptance criteria

### T.R. 6(A) time computation

- [ ] States the T.R. 6(A) rules:
      (1) exclude Day 0 (the triggering event),
      (2) include the last day unless it falls on a
      weekend or IC 1-1-9-1 legal holiday,
      (3) for periods **under 7 days**, intermediate
      Saturdays, Sundays, and holidays are **excluded**
      from the count; for periods of **7 days or more**,
      they are included
- [ ] Notes the **no-mail-extension rule**: T.R. 6(E)
      was abolished in 2009; service by certified mail
      does NOT add 3 days (unlike FRCP 6(d))

### Summary-judgment response deadline — T.R. 56(C)

- [ ] States the **30-day response period** for T.R.
      56(C) summary-judgment motions (reads the current
      day count from the corpus; notes any Marion CPC
      or court-specific variation) and applies the
      weekend/holiday roll-forward

### T.R. 59 motion to correct error — 30-day jurisdictional deadline

- [ ] States the **30-day filing deadline** from the
      entry of final judgment under T.R. 59(C) —
      describes it as **jurisdictional** (missing it
      cannot be cured by extension under T.R. 6(B))
- [ ] Notes that failure to rule within **45 days** of
      filing deems the T.R. 59 motion denied under
      T.R. 59(B)
- [ ] Notes the T.R. 59 motion's role as a **prerequisite
      for some appeals** under Ind. App. R. 9(A)(1)

### Indiana-specific holidays — IC 1-1-9-1

- [ ] Confirms **Good Friday** is an Indiana-specific
      state legal holiday (most other states do not
      observe it)
- [ ] Confirms **Primary Election Day** (even years,
      1st Tuesday after 1st Monday in May) and
      **General Election Day** (even years, 1st Tuesday
      after 1st Monday in November) are Indiana-specific
      legal holidays — courts closed on those days in
      even-numbered years
- [ ] Notes the distinction from states like Tennessee
      that observe Columbus Day but not Election Day, or
      Michigan that observes Lincoln's Birthday

## Common failure modes

- Adds a 3-day mail extension to any deadline (Indiana
  abolished T.R. 6(E) in 2009)
- States the T.R. 59 deadline is extendable by
  stipulation or court order (it is jurisdictional)
- Omits Good Friday as an Indiana court holiday
- Fails to note the even-year Election Day closure
- Applies the sub-7-day exclusion rule to periods of
  7 or more days
