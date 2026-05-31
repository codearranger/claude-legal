# az-consumer-debt — Time-barred debt and the *Mertola* acceleration / SOL rule

## Prompt

I'm being sued in Arizona on a credit card I stopped paying years
ago. The card had a clause that the whole balance becomes due if I
miss a payment. I think the lawsuit is too old. When did the clock
actually start, and is this time-barred?

## Expected triggers

- `az-consumer-debt`
- `az-first-30-days`

## Acceptance criteria

### Statute of limitations

- [ ] Identifies the applicable Arizona limitations period for the
      claim — the **written-contract** SOL at **A.R.S. § 12-548** and
      the **open-account / oral-contract** SOL at **A.R.S. § 12-543**
      — and reads the **period length** from `az-statutes-debt/`
      rather than asserting a number
- [ ] Notes that which statute applies depends on how the claim is
      characterized (written contract vs. open/credit-card account)
      and reads that distinction from the corpus

### Accrual / acceleration (*Mertola*)

- [ ] Applies the Arizona Supreme Court's rule in **_Mertola, LLC v.
      Santos_** (read/verified from `key-cases.md`) that, for a
      credit-card debt with an **optional acceleration** clause, the
      limitations period on the **entire debt** begins to run when the
      creditor **exercises the option to accelerate** upon default —
      not payment-by-payment — rather than asserting the holding from
      memory
- [ ] Uses *Mertola* to fix the accrual date and compute whether the
      suit is time-barred (reading the SOL length from the corpus)

### Raising the defense

- [ ] Frames SOL as an **affirmative defense under Ariz. R. Civ. P.
      8(c)** that must be pleaded or is waived (cross-reference
      `az-first-30-days`)
- [ ] Notes that a partial payment or written acknowledgment may
      affect the clock — reads the rule from the corpus rather than
      asserting it

## Common failure modes

- Asserts the SOL length from memory instead of `az-statutes-debt/`
- Misstates *Mertola* (e.g., treating each missed payment as a
  fresh accrual when the creditor accelerated) or asserts it from
  memory
- Forgets to plead SOL as a Rule 8(c) affirmative defense
