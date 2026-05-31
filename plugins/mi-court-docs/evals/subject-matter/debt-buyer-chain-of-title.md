# mi-consumer-debt — Debt-buyer standing / chain of title + RCPA / MCPA

## Prompt

A company I've never heard of is suing me in Michigan for about
$4,000 on a credit card that was originally with a big bank.
They say they "bought" my account. I don't think they've proven
they actually own it. What's my defense, and are there Michigan
consumer-protection laws that apply to how they've been
collecting?

## Expected triggers

- `mi-consumer-debt`
- `mi-first-30-days`

## Acceptance criteria

### Standing / chain of title

- [ ] Frames the core defense: a **debt buyer must prove it owns
      the debt** through an **unbroken, admissible chain of title
      / assignment** from the original creditor through each
      intermediate purchaser to the plaintiff
- [ ] Notes that a generic **affidavit of debt** or a single
      bill of sale referencing an unattached "pool" of accounts
      may be insufficient to establish ownership of the
      **specific** account, and ties admissibility to the
      business-records foundation under the Michigan Rules of
      Evidence (cite the evidence rule; read current foundation
      requirements from the corpus)
- [ ] Channels the standing challenge into the answer (separate
      affirmative defense under MCR 2.111(F)) and/or a summary-
      disposition motion (cross-reference `mi-first-30-days`)

### Michigan statutory overlay (RCPA / MCPA)

- [ ] Identifies the **Michigan Regulatory Collection Practices
      Act / Occupational Code collection provisions (RCPA)** and
      the **Michigan Collection Practices Act**, citing the
      governing MCL provisions **read from `mi-statutes-debt/`**
      rather than asserting the section numbers or prohibited-
      conduct list from memory
- [ ] Notes the **Michigan Consumer Protection Act (MCPA)** as a
      potential overlay and reads its scope/limits from the
      corpus (including any regulated-conduct exemptions) rather
      than asserting them
- [ ] Pairs Michigan law with the federal **FDCPA** (from the
      shared `federal-debt-laws/` corpus) without conflating the
      two regimes

### Honest-sourcing

- [ ] Reads statutory section numbers, prohibited practices, and
      remedies from the corpus rather than reciting from memory

## Common failure modes

- Treats the affidavit of debt as conclusive proof of ownership
- Recites RCPA/MCPA section numbers or elements from memory
- Conflates the federal FDCPA with the Michigan RCPA/MCPA
- Forgets to plead standing as a separate MCR 2.111(F) defense
