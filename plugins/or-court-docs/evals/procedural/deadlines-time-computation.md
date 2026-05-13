# or-deadlines — Time computation under ORCP 10

## Prompt

I was served by mail with a complaint on April 1, 2025. The
service was by USPS first-class to my Portland address. When
is my answer due?

## Expected triggers

- `or-deadlines`

## Acceptance criteria

### Date arithmetic

- [ ] Computes: 30 days (ORCP 7 C(2)) + 3 days for mail
      (ORCP 10 C) = **33 days**
- [ ] From April 1 + 33 days = **May 4, 2025**
- [ ] May 4, 2025 is a Sunday → next business day (ORCP 10
      A end-of-period rule) → **May 5, 2025**
- [ ] Identifies May 5, 2025 (Monday) as the final answer
      deadline

### Authorities cited

- [ ] ORCP 7 C(2) for 30-day base period
- [ ] ORCP 10 A for end-of-period rule
- [ ] ORCP 10 C for 3-day mail rule
- [ ] ORS 187.010 for legal holidays (incidentally)

### Methodology

- [ ] Suggests using `scripts/case-calendar.py` for
      deterministic computation
- [ ] Recommends a buffer (file by day 25 or so, not day 30)

## Common failure modes

- Forgetting the 3-day mail rule under ORCP 10 C
- Adding 3 days for eService (the rule applies to USPS mail,
  not eService)
- Computing from April 2 (including the day of service)
  instead of April 1 (excluding it per ORCP 10 A)
- Not extending past the Sunday end-of-period
- Citing the WA CR 6 rule instead of ORCP 10
