# ca-consumer-debt — Rosenthal Act counterclaim

## Prompt

A debt collector called my workplace 4 times after I told them to
contact me only by mail. Can I file a counterclaim in my California
state-court collection case?

## Expected triggers

- `ca-consumer-debt`

## Acceptance criteria

### Counterclaim viability

- [ ] **Rosenthal Act** (Cal. Civ. Code §§ 1788-1788.33) is the
      primary state-law vehicle
- [ ] § 1788.17 — incorporates FDCPA standards as state-law
      violations
- [ ] § 1788.11 — prohibits causing telephone to ring
      repeatedly; prohibits contacting at work after notified

### Rosenthal vs. FDCPA distinction (CRITICAL)

- [ ] **Rosenthal covers first-party AND third-party collectors**
      — unlike federal FDCPA which is third-party only
- [ ] Definition of "debt collector" under Cal. Civ. Code
      § 1788.2(c) is broader than 15 U.S.C. § 1692a(6)

### Damages

- [ ] Actual damages (Cal. Civ. Code § 1788.30(a))
- [ ] Statutory damages: $100-$1,000 per case (§ 1788.30(b))
- [ ] **Attorney's fees** (§ 1788.30(c)) — one-way fee shifting
      for prevailing consumer

### Federal FDCPA cumulative

- [ ] May plead both Rosenthal AND FDCPA — they're cumulative,
      not duplicative
- [ ] FDCPA: actual + up to $1,000 statutory (15 U.S.C.
      § 1692k(a))

### UCL hook

- [ ] Cal. Bus. & Prof. Code § 17200 — "unlawful" prong
      borrows the FDCPA / Rosenthal violation as predicate
- [ ] Injunctive relief + restitution
- [ ] 4-year SOL (Bus. & Prof. Code § 17208)

### Procedural

- [ ] Counterclaim under CCP §§ 426.10-426.50 (cross-complaint
      in CA)
- [ ] **Compulsory** if related to plaintiff's claim (§ 426.30)
- [ ] Filed with answer typically

### 1-year SOL

- [ ] Cal. Civ. Code § 1788.30(f) — 1-year SOL from violation
- [ ] Asks for date of violations

## Common failure modes

- Reporting that Rosenthal only covers third-party collectors
  (it covers first-party too — KEY CA distinction)
- Calling it a "counterclaim" instead of "cross-complaint"
  (California uses cross-complaint terminology)
- Missing the one-way fee-shifting under § 1788.30(c)
- Importing Oregon's UTPA (ORS 646.605) framework
- Missing the UCL "unlawful" predicate hook
- Missing the cumulative FDCPA + Rosenthal pleading
