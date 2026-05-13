# ca-consumer-debt — Chain of title in debt-buyer case

## Prompt

A debt buyer is suing me on an old Citibank credit card. What
should I demand to see about how they got the debt?

## Expected triggers

- `ca-consumer-debt`
- `ca-discovery`

## Acceptance criteria

### Chain-of-title doctrine

- [ ] Plaintiff must allege and prove ownership of the debt
- [ ] Each link in the chain from original creditor to plaintiff
- [ ] Each assignment must be authenticated under Cal. Evid.
      Code § 1271 (business records) + § 1421 (signature)

### FDBPA heightened pleading (Cal. Civ. Code § 1788.58)

- [ ] **Complaint MUST allege**: charge-off balance, date of
      last payment, original creditor name, account number,
      and chain of title
- [ ] **Documentation must be attached** — bill of sale,
      assignment, account-level documentation
- [ ] Missing FDBPA-required allegations = grounds for demurrer

### Key discovery requests

- [ ] All assignments / bills of sale in the chain
- [ ] Pool data / portfolio data showing the specific account
      transfer
- [ ] Account statements from original creditor
- [ ] Charge-off statement (FDBPA-required)
- [ ] Last payment record
- [ ] Custodian-of-records affidavit under Cal. Evid. Code
      § 1561

### Authentication challenges

- [ ] Plaintiff (debt buyer) often cannot lay § 1271 foundation
      for original creditor's records — never had business
      relationship with consumer
- [ ] Secondary Evidence Rule (Cal. Evid. Code § 1521)

### CA UCC Article 9

- [ ] Cal. Comm. Code §§ 9101 et seq. — assignment of payment
      rights, accounts, payment intangibles
- [ ] Notice of assignment to debtor

## Common failure modes

- Missing FDBPA's heightened pleading requirements
- Not demanding the specific pool-data showing the consumer's
  account included in the sold portfolio
- Importing OR's chain-of-title doctrine (ORS 79 / OEC 803(6))
- Importing WA's chain-of-title doctrine (RCW 62A.9A / ER 803)
- Failing to cite Cal. Evid. Code § 1271 / § 1421 / § 1561 /
  § 1521
- Failing to cite Cal. Comm. Code § 9101+ (UCC Art. 9 as
  enacted in California)
