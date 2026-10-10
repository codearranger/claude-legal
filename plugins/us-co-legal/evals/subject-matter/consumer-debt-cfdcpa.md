# co-consumer-debt — CFDCPA + CCPA treble damages + collection-agency licensure

## Prompt

A debt collector in Colorado has been calling me five times
a day and they told me I'd be arrested if I didn't pay.
The debt is from a credit card that I stopped paying about
four years ago. What Colorado and federal laws apply, and
what can I actually do?

## Expected triggers

- `co-consumer-debt`
- `co-first-30-days`

## Acceptance criteria

### Colorado statutory overlay

- [ ] Identifies the **Colorado Fair Debt Collection
      Practices Act (CFDCPA)** at **C.R.S. art. 16 of
      title 5** (recodified from Title 12 in 2022) as
      the primary Colorado law — reads the prohibited
      practices and remedies from the `co-statutes-debt/`
      corpus rather than asserting section numbers from
      memory
- [ ] Identifies the **Colorado Consumer Protection Act
      (CCPA)** at **C.R.S. art. 1 of title 6** with
      its **treble damages + mandatory attorney's fees**
      provision — reads the current remedy provisions
      from the corpus; does not assert specific dollar
      caps or multipliers from memory

### Federal overlay

- [ ] Pairs the Colorado statutes with the **FDCPA**
      (15 U.S.C. § 1692 et seq.) from the shared
      `federal-debt-laws/` corpus — identifying "arrest"
      threats and excessive calls as potential violations
      of both regimes — without conflating the two

### Collection-agency licensure

- [ ] Notes Colorado's **collection-agency licensing
      requirement** administered by the Attorney
      General's **Collection Agency Board** under
      C.R.S. art. 16 of title 5 — an unlicensed
      collector is operating in violation of Colorado
      law; reads the current licensure requirement
      from the corpus

### SOL defense

- [ ] Identifies the **6-year SOL for liquidated debt**
      under **C.R.S. § 13-80-103.5(1)(a)** as confirmed
      by ***Hassler v. Account Brokers of Larimer County,
      Inc.*, 2012 CO 24** — notes this case must be
      **verified against `key-cases.md`** rather than
      asserted from memory
- [ ] Notes that a time-barred debt defense goes into
      the answer as an affirmative defense (C.R.C.P. 8(c))

## Common failure modes

- Cites the pre-2022 Title 12 location for the CFDCPA
  instead of the recodified Title 5 location
- Asserts CCPA remedy amounts from memory
- Conflates the CFDCPA with the FDCPA
- Misses the collection-agency licensure defense
- States the SOL period from memory without verifying
  *Hassler v. Account Brokers*
