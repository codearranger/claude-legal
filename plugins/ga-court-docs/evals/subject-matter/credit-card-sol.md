# ga-consumer-debt — Credit-card SOL: 6-year written contract, not 4-year open account

## Prompt

A debt buyer sued me in Georgia on an old credit card. My last payment
was in March 2019. They're calling it an "open account." Is this lawsuit
too old, and which statute of limitations applies to a credit card in
Georgia?

## Expected triggers

- `ga-consumer-debt`
- `ga-first-30-days`

## Acceptance criteria

### Which SOL applies

- [ ] Explains that under Georgia law a **credit-card debt is treated as a
      written contract** governed by the **6-year SOL of O.C.G.A. § 9-3-24**
      — because use of the card is acceptance of the written cardmember
      agreement — per **Hill v. American Express, 289 Ga. App. 576 (2008)**
      (and **Phoenix Recovery Group v. Mehta, 289 Ga. App. 576 (2008)**) —
      verified against `key-cases.md` rather than asserted from memory
- [ ] Distinguishes the **4-year open-account / oral SOL of O.C.G.A.
      § 9-3-25** and explains the plaintiff cannot shorten the limitations
      period merely by **labeling** the claim an "open account" or
      "account stated" when a written cardmember agreement governs
- [ ] The 6-year and 4-year periods are statutory and stable, so citing
      the periods directly is acceptable; the **accrual date** must be
      determined from the user's facts (last payment / default), not
      asserted

### The escape-hatch flip

- [ ] Notes the strategic flip: if the debt buyer **cannot produce the
      written cardmember agreement** and pleads only open account /
      account stated, the shorter **4-year § 9-3-25** period may apply —
      and the absence of the agreement is also a **proof / foundation
      defect** (cross-reference `debt-buyer-chain-of-title.md`)

### Revival traps

- [ ] Warns about revival: a **new promise must be in writing**
      (O.C.G.A. § 9-3-110) and a **part payment** on written evidence can
      restart the clock (O.C.G.A. § 9-3-112) — reads these from the corpus

### Pleading the defense

- [ ] Routes the time-bar into the **answer as an affirmative defense**
      and notes it can support a motion for summary judgment

## Common failure modes

- Applies the **4-year open-account SOL (§ 9-3-25)** to a credit card,
  missing that Georgia treats it as a 6-year written contract under
  § 9-3-24 / *Hill v. American Express*
- Accepts the plaintiff's "open account" label at face value
- Cites *Hill* without verifying it against `key-cases.md` (secondary
  sources conflate the S.E.2d pin-cites)
- Misses the part-payment / written-new-promise revival traps
