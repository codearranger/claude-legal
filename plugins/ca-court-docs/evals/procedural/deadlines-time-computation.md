# ca-deadlines — Time computation under CCP § 12 / § 12a

## Prompt

I was served with a complaint by mail on April 15, 2026 in
California. When is my answer due?

## Expected triggers

- `ca-deadlines`
- `ca-first-30-days`

## Acceptance criteria

### Answer baseline

- [ ] 30 days from completed service under CCP § 412.20(a)(3)

### Service-by-mail addition

- [ ] CCP § 415.30 (mail service with NORF) — completed service
      runs from acknowledgment receipt OR 20 days, whichever
      first
- [ ] Distinguishes mail-with-NORF from mail under CCP § 1013
      (the latter adds 5 days for OTHER papers but doesn't apply
      to the summons itself)

### CCP § 12 / § 12a application

- [ ] Excludes the first day, includes the last (CCP § 12)
- [ ] If last day falls on weekend or judicial holiday, extends
      to next court day (CCP § 12a)
- [ ] Identifies California holidays per Govt. Code § 6700

### Practical computation

- [ ] Concrete deadline date
- [ ] References to the §§ used

## Common failure modes

- Confusing mail-with-NORF service (CCP § 415.30) with mail
  service of papers (CCP § 1013)
- Importing OR's 33-day "mail-add 3" rule (Oregon-specific)
- Importing WA's CR 6 calendar instead of CCP § 12
- Forgetting Cesar Chavez Day (Mar 31), Lincoln's Birthday
  (Feb 12), or day-after-Thanksgiving as CA judicial holidays
- Missing that CCP § 1005(b) motion deadlines are COURT days,
  not calendar days
