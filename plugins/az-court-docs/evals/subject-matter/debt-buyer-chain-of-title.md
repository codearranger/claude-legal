# az-consumer-debt — Debt-buyer standing / chain of title + Arizona collection law

## Prompt

A company I've never heard of is suing me in Arizona for about
$4,000 on a credit card that was originally with a big bank. They
say they "bought" my account. I don't think they've proven they
actually own it. What's my defense, and are there Arizona laws that
apply to how they've been collecting?

## Expected triggers

- `az-consumer-debt`
- `az-first-30-days`

## Acceptance criteria

### Standing / chain of title

- [ ] Frames the core defense: a **debt buyer must prove it owns the
      debt** through an **unbroken, admissible chain of title /
      assignment** from the original creditor through each
      intermediate purchaser to the plaintiff
- [ ] Notes that a generic **affidavit of debt** or a single bill of
      sale referencing an unattached "pool" of accounts may be
      insufficient to establish ownership of the **specific**
      account, and ties admissibility to the business-records
      foundation under **Ariz. R. Evid. 803(6)** (cite the rule; read
      current foundation requirements from the corpus)
- [ ] Channels the standing challenge into the answer (affirmative
      defense under **Ariz. R. Civ. P. 8(c)**) and/or a Rule 56
      motion (cross-reference `az-first-30-days`)

### Arizona statutory / regulatory overlay

- [ ] Identifies the relevant **Arizona collection-agency licensing
      regime** at **A.R.S. Title 32, Chapter 9 (collection agencies)**
      and the **Arizona Consumer Fraud Act (A.R.S. § 44-1521 et seq.)**
      as possible overlays — citing the governing provisions **read
      from `az-statutes-debt/`** rather than asserting section numbers
      or prohibited conduct from memory
- [ ] Pairs Arizona law with the federal **FDCPA** (from the shared
      `federal-debt-laws/` corpus) without conflating the regimes

### Honest sourcing

- [ ] Reads statutory section numbers, prohibited practices, and
      remedies from the corpus rather than reciting from memory

## Common failure modes

- Treats the affidavit of debt as conclusive proof of ownership
- Recites Arizona statute section numbers or elements from memory
- Conflates the federal FDCPA with the Arizona Consumer Fraud Act /
  collection-agency statute
- Forgets to plead standing as an affirmative defense under
  Rule 8(c)
