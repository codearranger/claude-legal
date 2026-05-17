# wa-landlord-tenant — Warranty of habitability + repair-and-deduct

## Prompt

My Washington apartment has a broken furnace in February.
The landlord ignored two written requests to fix it. The
landlord just told me she's not renewing my lease. What
remedies do I have?

## Expected triggers

- `wa-landlord-tenant`
- `wa-first-30-days`

## Acceptance criteria

- [ ] Identifies the **warranty of habitability** at RCW
      59.18.060 — landlord obligation to maintain premises
      fit for habitation, including heat / hot water /
      electricity functioning
- [ ] Identifies the **tenant remedies** framework at RCW
      59.18.100 — notice + reasonable time to repair;
      repair-and-deduct (cap set by statute — read from
      `wa-law-references/references/wa-rcw-debt/RCW-59_18.md`);
      diminution-of-rent action; rent into court registry;
      rescission
- [ ] Identifies the **retaliation presumption** at RCW
      59.18.240 — adverse landlord action within the
      statutory window after protected activity (such as
      a repair request) is presumed retaliatory. **Read
      the current presumption window from `RCW-59_18.md`**
      rather than embedding a day count
- [ ] Notes the non-renewal-after-repair-request scenario
      strongly invokes the retaliation presumption
- [ ] Suggests procedural steps: document the prior repair
      requests + the non-renewal timing; file a defective-
      notice + retaliation defense; consider an affirmative
      claim under RLTA
- [ ] References Office of Civil Legal Aid for HB 1815 RTC
      appointment if income-eligible
- [ ] References local code-enforcement for the
      habitability violation

## Common failure modes

- Hard-coding the repair-and-deduct cap (a dollar / month
  figure that lives in the statute)
- Hard-coding the retaliation-presumption window
- Missing the retaliation presumption entirely
- Treating non-renewal as automatically permissible (post-
  2021, just-cause applies — see `landlord-tenant-just-
  cause.md`)
