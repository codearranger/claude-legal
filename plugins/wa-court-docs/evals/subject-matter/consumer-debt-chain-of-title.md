# wa-consumer-debt — Chain of title

## Prompt

A debt buyer sued me in Washington. They attached a "Bill of
Sale" listing me along with thousands of other accounts, and a
"Certificate of Indebtedness" signed by their own custodian of
records. Is that enough to prove they own my account?

## Expected triggers

- `wa-consumer-debt`
- `wa-law-references`

## Acceptance criteria

- [ ] Identifies the chain-of-title issue: plaintiff must
      prove ownership of THIS specific account (CR 17(a) real-
      party-in-interest)
- [ ] References UCC Article 9 mechanics at RCW 62A.9A (see
      `wa-law-references/references/wa-rcw-debt/RCW-62A_9A.md`)
- [ ] Walks the foundation gaps in a typical bulk-portfolio
      bill of sale:
      - Generic portfolio schedule — doesn't identify the
        specific account
      - Custodian-of-records affidavit from buyer's own
        custodian (the *Ziegler* / *Discover Bank v. Bridges*
        problem — buyer's custodian can authenticate buyer's
        records but not seller's records that buyer received)
      - Missing original cardholder agreement (specimen ≠
        actual agreement)
- [ ] Walks evidence-law objections at ER 803(6) (business
      records hearsay exception) + ER 901 (authentication) +
      ER 902 (self-authentication)
- [ ] Suggests discovery targeting: complete chain documents;
      account-specific assignment records; original cardholder
      agreement; all monthly statements

## Common failure modes

- Treating the bill-of-sale as authenticating individual
  accounts in a portfolio
- Missing the remote-custodian foundation problem (*Ziegler*)
- Confusing specimen agreements with the actual signed
  agreement
