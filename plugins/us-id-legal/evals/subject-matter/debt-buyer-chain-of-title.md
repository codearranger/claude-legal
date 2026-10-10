# id-consumer-debt — debt-buyer standing / chain of title + Idaho collection law

## Prompt

A company I've never heard of is suing me in Idaho for about $4,000
on an old credit card that was originally with a big bank. They say
they "bought" my account. I don't think they've proven they own it.
What's my defense, and do any Idaho laws apply to how they collect?

## Expected triggers

- `id-consumer-debt`
- `id-first-30-days`

## Acceptance criteria

### Standing / chain of title

- [ ] Frames the core defense: a **debt buyer must prove it owns the
      debt** through an unbroken, admissible **chain of title /
      assignment** from the original creditor to the plaintiff
- [ ] Notes a generic affidavit of debt or a bill of sale referencing
      an unattached pool of accounts may be insufficient to prove
      ownership of the **specific** account, and ties admissibility to
      the business-records foundation under **I.R.E. 803(6)** /
      **902(11)** (cite the rules; read current foundation
      requirements from the corpus)
- [ ] Channels the challenge into the answer (affirmative defense,
      **I.R.C.P. 8(c)**) and/or summary judgment (cross-reference
      `id-first-30-days`)

### Idaho statutory overlay

- [ ] Identifies the **Idaho Collection Agency Act (I.C. § 26-2222 et
      seq.)** and that a **debt buyer collecting debt acquired while
      delinquent/in default must be licensed** by the Idaho Department
      of Finance (§ 26-2223), framing licensure/capacity as litigable —
      reading the governing provisions from `id-statutes-debt/` rather
      than reciting subsections from memory
- [ ] Identifies the **Idaho Consumer Protection Act (I.C. § 48-601 et
      seq.)** as a possible overlay
- [ ] Pairs Idaho law with the federal **FDCPA** (from the shared
      `federal-debt-laws/` corpus) without conflating the regimes

## Common failure modes

- Treats the affidavit of debt as conclusive proof of ownership
- Recites Idaho statute subsections or dollar figures from memory
- Conflates the FDCPA with the Idaho statutes
