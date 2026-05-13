# or-consumer-debt — Fact-pattern triage

## Prompt

A debt buyer in Oregon (Velocity Investments, LLC) is suing
me on an alleged Bank of America credit card I don't
recognize. The last activity on the alleged account was 7
years ago. What's my best defense?

## Expected triggers

- `or-consumer-debt`
- `or-first-30-days`
- `or-pro-se`

## Acceptance criteria

### Identifies fact patterns

- [ ] Matches to Pattern 1 (Debt-buyer suit on unfamiliar
      account) AND Pattern 3 (Time-barred debt)
- [ ] Possibly Pattern 5 (Unregistered collection agency) —
      flags the DCBS lookup

### Defenses

- [ ] **Statute of limitations under ORS 12.080** — 6-year
      SOL; 7 years > 6 years; the suit is time-barred (this
      should be the LEAD defense)
- [ ] Lack of standing — Plaintiff cannot prove chain of
      title
- [ ] ORS 697.105 — lack of capacity if Plaintiff is
      unregistered
- [ ] ORCP 21 A(8) — failure to state ultimate facts
- [ ] OEC 803(6) / 902(11) authentication challenge

### Counterclaims

- [ ] FDCPA § 1692e(2), e(5), f(1) — collecting on
      time-barred debt
- [ ] Reg F § 1006.26(b) — time-barred collection
- [ ] Oregon UTPA (ORS 646.605) — ORS 646.607 (demanding
      payment not legally owed); ORS 646.608(1)(s)
- [ ] ORS 697.085 if Plaintiff unregistered

### Discovery

- [ ] Recommends DCBS database lookup
  (https://orcfr.dcbs.oregon.gov/)
- [ ] First RFPs targeting chain of title and registration

### Strategic priority

- [ ] **SOL defense first** — it's dispositive if proven

## Common failure modes

- Leading with the chain-of-title defense (SOL is stronger and
  faster)
- Missing the ORS 697.105 lack-of-capacity defense
- Generic "fight the case" advice without specifics
- Forgetting to flag the 1-year FDCPA SOL on counterclaims
