# ca-consumer-debt — Fact-pattern triage

## Prompt

I just got served with a complaint by a company called "Cavalry SPV
I, LLC" in LASC. They're suing me for $4,800 on a Chase credit
card I haven't paid since 2020. What kind of case is this and
what should I think about?

## Expected triggers

- `ca-consumer-debt`
- `ca-first-30-days`

## Acceptance criteria

### Fact-pattern identification

- [ ] Identifies as debt-buyer lawsuit on credit-card debt
      (Pattern 2 of the 5-pattern triage)
- [ ] Notes Cavalry SPV is a debt buyer (not original creditor)

### Applicable laws flagged

- [ ] **FDBPA** (Cal. Civ. Code §§ 1788.50-1788.66) — debt-
      buyer-specific heightened pleading + documentation
- [ ] **Rosenthal Act** (Cal. Civ. Code §§ 1788-1788.33)
- [ ] **CDCLA** (Cal. Fin. Code §§ 100000+) — licensing
- [ ] FDCPA + Reg F (federal)

### Statute of limitations

- [ ] CCP § 337 — 4-year SOL on written contract; credit card
      = written contract
- [ ] Last activity 2020 → SOL ~2024 → potentially within or
      just outside SOL depending on exact date
- [ ] Flags need for client to identify last-payment date
      precisely

### Initial discovery priorities

- [ ] Chain of title from Chase to Cavalry SPV
- [ ] Charge-off statement (FDBPA § 1788.58 required content)
- [ ] CDCLA license status of Cavalry SPV
- [ ] Account-level documentation

### Defense theory

- [ ] SOL affirmative defense
- [ ] FDBPA pleading-sufficiency challenge
- [ ] Standing / capacity challenges
- [ ] Potential counterclaim under Rosenthal Act / UCL

### Response window

- [ ] 30 days to respond (CCP § 412.20)

## Common failure modes

- Identifying as Pattern 1 (original creditor) when Cavalry
  SPV is a known debt buyer
- Missing FDBPA application (CA-specific debt-buyer statute)
- Missing CDCLA licensing analysis (2022 effective date)
- Importing OR's ORS 697 collection-agency framework
- Citing CCP § 339 (oral contract — 2 years) for credit card
- Missing the Rosenthal Act counterclaim potential
