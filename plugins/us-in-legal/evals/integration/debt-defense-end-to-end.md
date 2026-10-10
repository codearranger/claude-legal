# Integration — End-to-end debt defense in Indiana (Marion Superior Court)

## Prompt

A debt buyer filed a lawsuit against me in Marion Superior
Court claiming I owe $8,500 on a credit card I stopped
paying six years ago. They attached a one-page affidavit
but no account records or assignment papers. Walk me
through everything — the court, the deadline to respond,
what to file, my defenses including the SOL and their
missing paperwork, how to get their records in discovery,
and how to format everything so the clerk doesn't bounce it.

## Expected triggers

- `in-first-30-days`
- `in-consumer-debt`
- `in-discovery`
- `in-draft-motion`
- `in-statewide-format`
- `in-marion`
- `in-fact-check`

## Acceptance criteria

### Forum identification (in-marion)

- [ ] Identifies **Marion Superior Court Civil Division**
      as the court; notes the random assignment to one
      of 14 Civil Division courtrooms via Odyssey; reads
      the Marion cause-number encoding from `in-marion`
- [ ] Notes the Marion local-practice requirement to
      include a **proposed order with every motion**

### Answer + affirmative defenses (in-first-30-days)

- [ ] States the **20-day answer deadline** under
      T.R. 6(C) with no mail extension (T.R. 6(E)
      abolished in 2009) and applies the weekend/holiday
      roll-forward using Indiana IC 1-1-9-1 holidays
- [ ] Pleads affirmative defenses **under T.R. 8(C)**:
      statute of limitations (IC 34-11-2-7, 6-year open
      account), lack of standing / chain of title
      (T.R. 17(A)), FDCPA / DCSA counterclaims
- [ ] Includes the T.R. 3.1 Appearance for a pro se
      defendant

### Substantive defense (in-consumer-debt)

- [ ] Identifies the **SOL defense** — 6-year limit for
      open account / credit card under IC 34-11-2-7,
      running from last activity; notes whether the
      facts suggest the SOL is expired or nearly expired
      (reads the SOL from the corpus, does not assert
      the period solely from memory)
- [ ] Raises the **chain-of-title defense**: plaintiff
      must prove ownership through an admissible
      assignment chain under T.R. 17(A); a bare affidavit
      of debt does not meet the IRE 803(6) business-
      records foundation for ownership
- [ ] Notes Indiana's **no-state-licensing** posture —
      defense rests on FDCPA + DCSA, not a licensing
      claim

### Discovery (in-discovery)

- [ ] Serves RFPs + interrogatories targeting the full
      assignment chain (all Bills of Sale, Loan
      Schedules, original-creditor records, validation
      notice); notes the **25-interrogatory cap**
      under T.R. 33(A)
- [ ] Notes **30-day response period** for T.R. 34(B)
      RFPs (reads from corpus); outlines the T.R. 37(E)
      meet-and-confer prerequisite before filing a
      motion to compel

### Dispositive motion (in-draft-motion)

- [ ] After discovery confirms SOL or missing chain,
      frames a **T.R. 56 motion for summary judgment**
      under the ***Jarboe* affirmative-negation burden**
      — movant must affirmatively negate an element with
      admissible evidence, not merely point to the
      record's gap (Indiana rejects *Celotex*)

### Format + verification (in-statewide-format + in-fact-check)

- [ ] All filings carry the T.R. 10(A) Indiana caption,
      T.R. 5(E) format, numbered paragraphs, pro se
      signature block (no Attorney Number)
- [ ] Every IC, T.R., and case citation is verified
      against the corpus before filing; does not assert
      cites from memory

## Common failure modes

- States a 30-day or 21-day answer period
- Adds a 3-day mail extension (abolished 2009)
- Drafts the summary-judgment motion under the federal
  *Celotex* standard (Indiana *Jarboe* is different)
- Treats the bare affidavit of debt as sufficient proof
  of chain of title
- States Indiana has a collection-agency licensing
  regime (it does not)
- Omits the proposed order from the Marion filing packet
