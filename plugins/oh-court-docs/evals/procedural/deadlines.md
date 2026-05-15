# oh-deadlines — Time computation

## Prompt

I was served a complaint in Cuyahoga County Common Pleas
on Friday, April 11, 2025. When is my answer due?

## Expected triggers

- `oh-deadlines`
- `oh-first-30-days`

## Acceptance criteria

- [ ] Applies Civ. R. 12(A)(1) 28-day default
- [ ] Applies Civ. R. 6(A) time-computation conventions
- [ ] Applies R.C. 1.14 weekend / holiday rollover if the
      28th day lands on weekend / observed holiday
- [ ] Result: **Friday, May 9, 2025**
- [ ] Notes whether the 28-day clock varies if service was
      by certified mail under Civ. R. 4.1

## Common failure modes

- Using FRCP 21-day answer
- Using CA 30-day answer
- Not applying weekend rollover
- Wrong holiday list (e.g., including only federal
  holidays; Ohio also observes Columbus Day per R.C.
  1.14)
