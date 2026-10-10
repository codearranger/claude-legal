# ny-deadlines — CPLR 2103(b)(2) 5-day mail rule

## Prompt

I served a Notice of Motion on opposing counsel by mail on
April 15, 2026. The return date is May 1, 2026. Did I serve
in time?

## Expected triggers

- `ny-deadlines`

## Acceptance criteria

- [ ] Computes the answer correctly: NO — service is
      insufficient
- [ ] Cites CPLR 2214(b): motion papers must be served at
      least **8 days** before the return date (or 16 days if
      cross-motion served back at least 7 days before
      return)
- [ ] Cites **CPLR 2103(b)(2): 5-day mail rule** — when
      service is by mail, add 5 days to any subsequent
      response/service period
- [ ] Math: 8 + 5 = 13 days before return date by mail
- [ ] May 1 minus 13 days = April 18 latest mailing date;
      April 15 mailing date is **3 days too late**
- [ ] Suggests cure: (a) adjourn the return date by
      stipulation; (b) re-serve with corrected return date
- [ ] References NY Gen. Constr. Law § 25-a for any
      weekend / holiday adjustments

## Common failure modes

- Computes only 8 days without adding the 5-day mail rule
- Treats April 15 → May 1 as 16 calendar days and concludes
  compliant
- Cites CPLR 2103(b)(6) (electronic service, no 5-day
  addition) instead of (b)(2)
