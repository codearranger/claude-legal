# ar-deadlines — Computation and Arkansas holidays

## Prompt

My Arkansas answer deadline lands around Presidents' Day weekend. How is the
deadline computed?

## Expected triggers

- `ar-deadlines`

## Acceptance criteria

- [ ] Applies **Ark. R. Civ. P. 6(a)** (exclude the first day, include the last
      unless a weekend or legal holiday) and the **Rule 6(d)** 3-day mail add-on
- [ ] Recognizes the third Monday in February as **George Washington's Birthday
      and Daisy Gatson Bates Day** (a state holiday under § 1-5-101)
- [ ] Notes **Christmas Eve** is also an Arkansas state holiday
- [ ] References `scripts/case-calendar.py` and reads the answer-due count from
      the rule/references rather than hard-coding it

## Common failure modes

- Treats the third Monday in February as merely "Presidents' Day" and misses the
  Daisy Gatson Bates Day designation; encodes Columbus Day/Juneteenth as state holidays
