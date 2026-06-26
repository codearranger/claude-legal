# ga-deadlines — O.C.G.A. § 9-11-6 / § 1-3-1 time computation + § 1-4-1 holidays

## Prompt

I was served with a civil complaint in Georgia. I want to count my answer
deadline correctly, and I'm also worried about a motion-response date that
might land on a Georgia state holiday. How do I count these?

## Expected triggers

- `ga-deadlines`

## Acceptance criteria

### Answer and default windows

- [ ] States the **30-day answer window** under **O.C.G.A. § 9-11-12(a)**
      and reads the current count (and any service-method variants) from
      the references corpus rather than asserting from memory
- [ ] Notes the **15-day "open default as a matter of right"** window
      under **O.C.G.A. § 9-11-55(a)** (reopen on payment of costs) and the
      separate § 9-11-55(b) showing required after that window — reads the
      conditions from the corpus

### Time computation (O.C.G.A. § 9-11-6(a) / § 1-3-1(d)(3))

- [ ] Explains that § 9-11-6(a) incorporates **O.C.G.A. § 1-3-1(d)(3)**:
      exclude the first day, count the last; if the last day is a
      Saturday, Sunday, or legal holiday, roll to the next business day;
      and for periods **under 7 days**, intermediate Saturdays, Sundays,
      and holidays are excluded — reads the rule text from the corpus

### Georgia legal holidays (O.C.G.A. § 1-4-1)

- [ ] Reads the Georgia holiday list from the **O.C.G.A. § 1-4-1** corpus
      entry rather than memory, noting that Georgia observes **Juneteenth**
      and **Columbus Day** (the second Monday in October — not renamed)
- [ ] Flags that several Georgia holidays are **governor-proclamation
      driven** (the § 1-4-1(b) thirteen-day list, the deferred Washington's
      Birthday observance, the April "State Holiday," and the
      day-after-Thanksgiving "State Holiday") and so must be treated as
      approximations — does NOT assert a specific calendar date as
      definitively a state holiday without checking

## Common failure modes

- Asserts the answer/default day counts from memory instead of the corpus
- Forgets to exclude intermediate weekends/holidays on a sub-7-day period
- Treats the governor-proclaimed floating holidays as fixed calendar dates
- Omits Juneteenth or wrongly assumes Columbus Day was renamed in Georgia
