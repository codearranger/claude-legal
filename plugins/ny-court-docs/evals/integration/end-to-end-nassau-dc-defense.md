# Integration — End-to-end Nassau District Court debt-defense

## Prompt

I got served at my home in Hicksville with a Summons and
Complaint from Cavalry SPV LLC in Nassau District Court,
First District. They are seeking $9,200 on a Discover card
account. I have 30 days to answer. Walk me through what to
draft, where to file it, and what deadlines I need to track.

## Expected triggers

- `ny-nassau-dc`
- `ny-first-30-days`
- `ny-consumer-debt`
- `ny-statewide-format`
- `ny-deadlines`
- `ny-pro-se`
- `ny-file-packet`

## Acceptance criteria

### Court identification

- [ ] **Nassau County District Court** (not Supreme Court)
- [ ] First District covers Nassau countywide for civil
- [ ] Filing address: **99 Main Street, Hempstead, NY 11550**
- [ ] 22 NYCRR **Part 212** governs format
- [ ] NYSCEF available for civil case types here

### Substantive Answer

- [ ] Format per `ny-nassau-dc` + `ny-statewide-format`
      baseline
- [ ] Affirmative defenses anchored in **CCFA**:
      - CPLR 3015(e) heightened pleading deficiencies
      - CPLR 214-i 3-year SOL (post-CCFA)
      - lack of standing / chain-of-title
      - GBL § 600-602 mini-FDCPA
- [ ] Federal counterclaim under FDCPA § 1692e / 1692f

### Deadlines

- [ ] Answer due **30 days** from service in District Court
      Civil Part (CPLR 320(a) / UDCA Article 4)
- [ ] CCFA-mandated notice + return of service receipt
      timing
- [ ] Calendar entry: **pre-trial conference** within
      60-90 days

### Filing

- [ ] NYSCEF preferred for civil case types; if NYSCEF
      unavailable, mail or hand-deliver to clerk at 99 Main
      Street, Hempstead
- [ ] Filing fee for Answer: $0 (Answer fee is waived)
- [ ] Service back on plaintiff by mail (CPLR 2103(b)(2))

### Self-represented signature

- [ ] **"Self-Represented"** designation
- [ ] No OCA bar number
- [ ] Address, phone, email
- [ ] Verification via the **post-2023 CPLR 2106** universal
      affirmation

## Common failure modes

- Sends the litigant to Nassau Supreme Court (`ny-nassau`)
  instead of Nassau District Court (`ny-nassau-dc`)
- Cites 22 NYCRR Part 202 instead of Part 212
- Tries to file at the Mineola Supreme Courthouse instead
  of 99 Main Street, Hempstead
- Treats the Answer deadline as 20 days (Supreme Court
  personal-service default) instead of 30 days (District
  Court Civil Part)
