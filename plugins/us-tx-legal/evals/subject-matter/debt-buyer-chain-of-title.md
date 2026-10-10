# tx-consumer-debt — debt-buyer chain of title + records affidavit

## Prompt

A debt buyer is suing me in Texas. All they attached is an affidavit
from their own employee and a one-page "bill of sale." How do I attack
their proof that I owe this and that they own it?

## Expected triggers

- `tx-consumer-debt`

## Acceptance criteria

### Business-records affidavit attack

- [ ] Identifies that the debt buyer relies on a **TRE 902(10)
      self-authenticating business-records affidavit** (with the **TRE
      803(6)** hearsay exception) in lieu of a live custodian, and that
      the **pre-trial notice/filing mechanics** of 902(10) can be
      challenged — reading the current 902(10) notice timing from
      `../tx-law-references/references/evidence-rules.md` /
      `court-rules/`
- [ ] Frames the core attack: the affiant typically lacks personal
      knowledge of the **original creditor's** record-keeping, so the
      original-creditor account records are inadmissible hearsay-within-
      hearsay through the debt buyer's affiant

### Chain of title

- [ ] Requires tracing **original creditor → each intermediate assignee
      → plaintiff** with an **account-specific** assignment / bill of
      sale, not a generic portfolio bill of sale, and that a gap defeats
      standing/ownership

### Bond check (Texas-specific)

- [ ] Raises the **Tex. Fin. Code § 392.101** requirement that a
      third-party debt collector file a **surety bond with the Texas
      Secretary of State** (a bond, NOT a license — Texas has no
      debt-collector licensing regime), reading the current bond amount
      from the corpus, and that failure to bond is litigable

### Procedure

- [ ] Routes discovery (RFP / RFA / interrogatories) at the chain-of-
      title documents via `tx-discovery`

## Common failure modes

- Treats the 902(10) affidavit as conclusive
- Accepts a generic portfolio bill of sale as proof of this account
- Calls § 392.101 a "license" or hard-codes the bond amount
