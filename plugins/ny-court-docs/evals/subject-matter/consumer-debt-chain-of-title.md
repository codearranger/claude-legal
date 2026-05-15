# ny-consumer-debt — Chain-of-title scrutiny for debt buyers

## Prompt

I think the plaintiff debt buyer in my NY case doesn't
actually own the debt. How do I challenge that?

## Expected triggers

- `ny-consumer-debt`
- `ny-discovery`

## Acceptance criteria

- [ ] Identifies that **chain of title is now an element of
      the CCFA-modified prima facie case** under CPLR 3015(e)
- [ ] Identifies the standing inquiry: original creditor →
      first assignee → ... → plaintiff (each link)
- [ ] Notes that **NY UCC Article 9 perfection** is the
      framework — assignment of a chose in action becomes
      enforceable against the obligor on notice
- [ ] References **Citibank, N.A. v. Conti-Scheurer**,
      172 A.D.3d 17 (2d Dep't 2019), and the post-CCFA case
      law applying the heightened standard
- [ ] Drafts an RFP targeting:
      - the original signed account agreement
      - each bill of sale / pool transfer document
      - the data file showing this specific account in the
        pool
      - the assignment confirmation for this specific account
- [ ] References **GBL § 601** (mini-FDCPA prohibition on
      false representation of the right to collect) as a
      counterclaim if chain of title can't be proved
- [ ] References CPLR 4540 (business-records foundation)
      as the evidentiary battleground

## Common failure modes

- Treats chain of title as merely a discovery issue (it is
  now a pleading-sufficiency issue after CCFA)
- Cites Article 3 (negotiable instruments) for assignment of
  a credit-card account (Article 9 is the framework)
- Misses the post-CCFA case law trend
