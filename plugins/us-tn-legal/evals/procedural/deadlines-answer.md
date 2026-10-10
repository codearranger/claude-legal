# tn-deadlines — Answer due date and Rule 6.01 roll-forward

## Prompt

I was personally served with a summons and complaint in my
Tennessee Circuit Court case. When is my answer due, and what
happens if the deadline lands on a weekend or a holiday?

## Expected triggers

- `tn-deadlines`
- `tn-first-30-days`

## Acceptance criteria

### Answer deadline

- [ ] States the answer is due **30 days** after service of
      the summons and complaint, citing **Tenn. R. Civ. P.
      12.01**
- [ ] Counts from the date of service (does not count the day
      of the event)

### Time computation (Rule 6.01)

- [ ] Cites **Tenn. R. Civ. P. 6.01** for time computation:
      exclude the day of the act/event; include the last day
- [ ] States the **weekend/holiday roll-forward**: if the last
      day is a Saturday, Sunday, or legal holiday, the period
      runs to the next day that is not a Saturday, Sunday, or
      legal holiday
- [ ] Identifies legal holidays from **T.C.A. § 15-1-101**
      (read the current list from the references corpus rather
      than reciting a fixed table); correctly treats Good
      Friday and Columbus Day as observed Tennessee holidays
- [ ] If service was by mail, notes the **Rule 6.05 3-day mail
      add-on** where applicable

## Common failure modes

- Uses a 20-day or 21-day answer period instead of 30 days
- Counts the day of service
- Rolls the deadline only past weekends but ignores legal
  holidays (or omits Good Friday / Columbus Day)
- Hard-codes a holiday table instead of pointing to
  § 15-1-101 / the references corpus
