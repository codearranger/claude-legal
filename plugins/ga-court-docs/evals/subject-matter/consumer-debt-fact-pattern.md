# ga-consumer-debt — FBPA + FDCPA overlay + no state collector licensing

## Prompt

A debt collector in Georgia has been calling me five times a day and told
me I'd be arrested if I didn't pay. The debt is from a credit card I
stopped paying a few years ago. What Georgia and federal laws apply, and
what can I actually do?

## Expected triggers

- `ga-consumer-debt`
- `ga-first-30-days`

## Acceptance criteria

### Georgia statutory overlay (FBPA)

- [ ] Identifies the **Georgia Fair Business Practices Act (FBPA)** at
      **O.C.G.A. § 10-1-390 et seq.** as the primary Georgia consumer
      vehicle — Georgia has **no mini-FDCPA**, so FDCPA-type collection
      misconduct is pursued through the FBPA — reads the prohibited-acts
      and remedies provisions from the `ga-statutes-debt/` corpus rather
      than asserting section numbers from memory
- [ ] Notes the FBPA remedies — actual damages (§ 10-1-399(a)), **treble
      damages for intentional violation** (§ 10-1-399(c)), and attorney
      fees (§ 10-1-399(d)) — reading them from the corpus
- [ ] Flags the **30-day pre-suit written demand** prerequisite under
      **O.C.G.A. § 10-1-399(b)** and that it does **not** toll the FBPA's
      **2-year SOL** (§ 10-1-401) — reads both from the corpus

### Federal overlay (FDCPA)

- [ ] Pairs the FBPA with the **FDCPA (15 U.S.C. § 1692 et seq.)** from
      the shared `federal-debt-laws/` corpus — identifying "arrest" threats
      and excessive calls as potential violations of both regimes —
      without conflating the two

### No state collector licensing

- [ ] Notes that Georgia does **not** license most debt collectors or
      debt buyers (the Department of Banking & Finance does not regulate
      collection agencies; the only licensing regime is the Installment
      Loan Act for loans ≤ a statutory amount, read from the corpus) — so
      there is **no unlicensed-collector defense** in Georgia, unlike some
      states; the FDCPA is the primary tool

### SOL defense

- [ ] Identifies the credit-card SOL question and routes to the
      `credit-card-sol.md` analysis (6-year written-contract SOL under
      **O.C.G.A. § 9-3-24**, *Hill v. American Express*) — verified against
      `key-cases.md` rather than asserted from memory

## Common failure modes

- Looks for a Georgia mini-FDCPA instead of using the FBPA as the state
  vehicle
- Asserts an "unlicensed collector" defense (Georgia does not license
  most collectors)
- Asserts the FBPA remedy multipliers or the 2-year SOL from memory
- Omits the § 10-1-399(b) 30-day written-demand prerequisite for an FBPA
  claim
