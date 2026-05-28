# Integration — End-to-end eviction defense packet

## Prompt

I'm a tenant in Seattle. Yesterday my landlord served me a
"Notice to Pay or Vacate." I think the notice form is wrong —
it doesn't have the legal-aid info I've heard tenants are
supposed to receive. I'm low-income and want to apply for the
right to counsel. Help me draft a notice of appearance and
explain the eviction-defense framework.

## Expected triggers

- `wa-landlord-tenant`
- `wa-first-30-days`
- `wa-pro-se`
- `wa-statewide-format`
- (Possibly) `wa-kcsc` or `wa-kcdc` depending on rent /
  forum

### Caption + format

- [ ] Correct King County caption (Superior or District,
      depending on the case posture)
- [ ] GR 14 formatting
- [ ] Pro se signature block

### Substantive guidance

- [ ] Identifies the **2019 SB 5600 mandatory-form
      requirement** at RCW 59.18.057 — pay-or-vacate notice
      MUST use the statutorily-mandated form including legal-
      aid contact info. Defective notice = defective
      foundation for eviction.
- [ ] References the **HB 1815 statewide tenant Right to
      Counsel** — recommends applying through the Office of
      Civil Legal Aid; notes the income-eligibility threshold
      (current threshold per Office of Civil Legal Aid —
      doesn't hard-code a figure)
- [ ] References **ERP** (Eviction Resolution Program) where
      applicable
- [ ] References affirmative defenses: defective notice
      (mandatory-form violation); habitability (RCW 59.18.060);
      retaliation presumption (RCW 59.18.240 — within a
      statutory window of protected activity); rental-
      assistance defenses
- [ ] References the response window (current day count via
      `wa-deadlines`; the unlawful-detainer summons is
      abbreviated, not standard CR 4 — that's a critical trap)
- [ ] Notes show-cause hearing framework

### References corpus integration

- [ ] Cites RCW 59.18 at chapter level; current notice
      periods, retaliation presumption window, and habitability
      remedies live in `RCW-59_18.md`
- [ ] Cites HB 1815 income eligibility as "current threshold
      per Office of Civil Legal Aid" rather than embedding a
      number

## Common failure modes

- Hard-coding a specific income-eligibility threshold for RTC
- Hard-coding a specific notice period
- Treating the unlawful-detainer summons as a standard CR 4
  summons (response window is much shorter)
- Skipping the mandatory-form defense
