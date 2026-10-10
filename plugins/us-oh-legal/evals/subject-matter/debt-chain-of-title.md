# oh-consumer-debt — Chain of title

## Prompt

A debt buyer in Ohio Common Pleas attached a single "Bill
of Sale" to its complaint, signed by the debt buyer's own
custodian. Is that enough to prove ownership of the
account?

## Expected triggers

- `oh-consumer-debt`
- `oh-fact-check`

## Acceptance criteria

- [ ] Identifies the foundation deficit: a single Bill of
      Sale + buyer-side custodian is generally insufficient
- [ ] References Ohio UCC Article 9 at **R.C. Chapter 1309**
      (especially R.C. 1309.406 assignment rights)
- [ ] Walks the required chain elements: original
      cardmember agreement, every intermediate Bill of
      Sale / Assignment, **account-level data files** at
      each hop, seller-side custodian affidavits, power-of-
      attorney chains where applicable
- [ ] Cites **Evid. R. 803(6) / 901 / 902(11)** as the
      authentication framework
- [ ] References *LVNV Funding, LLC v. Henderson*,
      2018-Ohio-3535 (1st Dist.) or comparable Ohio
      appellate authority

## Common failure modes

- Treating buyer-side custodian as sufficient
- Missing the account-level-data-file requirement
- No Ohio case law cited
- Conflating Article 3 negotiable-instrument transfer
  with Article 9 account assignment
