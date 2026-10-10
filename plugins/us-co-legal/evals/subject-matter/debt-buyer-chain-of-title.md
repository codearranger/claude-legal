# co-consumer-debt — Debt-buyer standing / chain of title + Colorado UCC Article 9

## Prompt

A company I've never dealt with just sued me in Colorado
District Court claiming they bought my old credit card
account from a bank. They attached only a spreadsheet and
a generic affidavit saying they purchased a "pool" of
accounts. Do they actually own my debt, and how do I raise
that defense?

## Expected triggers

- `co-consumer-debt`
- `co-first-30-days`
- `co-draft-motion`

## Acceptance criteria

### Standing / chain of title

- [ ] Frames the core defense: a **debt buyer must
      prove it owns the specific account** through
      an **unbroken, admissible chain of assignments**
      from the original creditor through each
      intermediate purchaser to the plaintiff
- [ ] Notes that a generic affidavit referencing a
      "pool" of accounts, without an account-specific
      exhibit, may be **insufficient to establish
      ownership** of the specific account — ties
      admissibility to the business-records foundation
      under **C.R.E. 803(6)** (read the current rule
      from the corpus rather than asserting the
      foundation elements from memory)
- [ ] Identifies the applicable Colorado UCC Article 9
      framework for **assignment of payment
      intangibles** at **C.R.S. art. 9 of title 4** —
      reads the current controlling provisions from
      `co-statutes-debt/` rather than asserting them
      from memory

### Pleading the defense

- [ ] Routes the standing challenge into the **answer
      as an affirmative defense** under C.R.C.P. 8(c)
      and/or a summary-judgment motion once discovery
      reveals the assignment documents
- [ ] Notes discovery strategy: request for production
      of the full assignment chain + original account
      agreement (cross-reference `co-discovery`)

### CFDCPA / CCPA overlay

- [ ] Notes that a debt buyer may also be subject to
      the **CFDCPA + CCPA** if it engages in abusive
      collection practices — reads the relevant
      provisions from the corpus

## Common failure modes

- Treats the generic "pool" affidavit as conclusive
  proof of account ownership
- Asserts UCC section numbers from memory without
  reading the corpus
- Fails to plead standing as an affirmative defense
- Skips the discovery strategy for forcing production
  of the assignment chain
