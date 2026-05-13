# ca-consumer-debt — Statute of limitations analysis

## Prompt

A debt buyer is suing me on a credit card account. The last
payment I made was December 15, 2021. The complaint was filed
March 10, 2026. Is the case time-barred?

## Expected triggers

- `ca-consumer-debt`
- `ca-deadlines`

## Acceptance criteria

### Applicable SOL

- [ ] CCP § 337 — written contract / open book account, 4 years
- [ ] Credit card = written contract (controlling CA case law)

### Computation

- [ ] Last payment: Dec 15, 2021
- [ ] 4-year SOL → Dec 15, 2025
- [ ] Complaint filed: Mar 10, 2026
- [ ] **Result: Time-barred by ~3 months**

### Revival doctrine

- [ ] CCP § 360 — written acknowledgment of debt or partial
      payment can restart the clock
- [ ] Asks whether any payments / written acknowledgments after
      Dec 15, 2021

### Other relevant SOLs

- [ ] FDCPA: 1 year (15 U.S.C. § 1692k(d)) — relevant if
      counterclaim
- [ ] Rosenthal Act: 1 year (Cal. Civ. Code § 1788.30(f))
- [ ] FDBPA: 1 year (Cal. Civ. Code § 1788.62)

### FDCPA § 1692f(1) hook

- [ ] Federal FDCPA prohibits collection of time-barred debt
      through litigation — *Crawford v. LVNV Funding, LLC*
      (11th Cir. 2014) line of authority

### Strategic guidance

- [ ] Affirmative defense in answer
- [ ] Potential basis for demurrer (CCP § 430.10(e)) if SOL
      apparent on face
- [ ] Counterclaim potential under Rosenthal + UCL

## Common failure modes

- Citing CCP § 339 (2 years, oral contracts) for credit card
- Citing the federal FDCPA 1-year as the underlying SOL on
  contract claim (it's the counterclaim SOL)
- Importing ORS 12.080(1)'s 6-year SOL (Oregon) — California
  is 4 years
- Importing RCW 4.16.040 6-year SOL (Washington) — California
  is 4 years
- Missing CCP § 360 revival doctrine
