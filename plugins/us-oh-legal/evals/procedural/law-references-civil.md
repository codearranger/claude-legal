# oh-law-references — Civil rules lookup

## Prompt

What is the deadline to answer a civil complaint in Ohio
Common Pleas, and where in the rules is it stated?

## Expected triggers

- `oh-law-references`
- `oh-deadlines`
- `oh-first-30-days`

## Acceptance criteria

- [ ] Identifies **28 days** as the default civil answer
      deadline
- [ ] Cites **Civ. R. 12(A)(1)** as the authoritative rule
- [ ] References Civ. R. 6 time-computation conventions
- [ ] Notes that service-by-mail variants (Civ. R. 4.1)
      can affect commencement of the 28-day clock
- [ ] Does NOT confuse with FRCP 12 (21 days) or other
      state analogs

## Common failure modes

- Stating 30 days (CA / FRCP confusion)
- Stating 21 days (FRCP confusion)
- Citing Civ. R. 8 instead of Civ. R. 12
- Missing R.C. 1.45 weekend-rollover note
