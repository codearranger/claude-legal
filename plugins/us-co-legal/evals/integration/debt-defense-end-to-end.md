# Integration — End-to-end debt defense in Colorado District Court

## Prompt

I just got served with a civil summons and complaint in
Colorado District Court. A debt buyer is claiming I owe
about $6,000 on an old credit card. They attached a
spreadsheet and a single-page affidavit. Walk me through
the whole thing — how long I have to respond, how to
challenge whether they even own the debt, how to get their
documents through discovery, and how to format and file
everything.

## Expected triggers

- `co-first-30-days`
- `co-consumer-debt`
- `co-discovery`
- `co-draft-motion`
- `co-statewide-format`
- `co-fact-check`

## Acceptance criteria

### Deadline (co-first-30-days / co-deadlines)

- [ ] States the **21-day answer window** under
      C.R.C.P. 12(a)(1) for in-state service and
      applies **C.R.C.P. 6(a)** roll-forward for
      weekends and Colorado state holidays — reads
      day counts and the C.R.S. § 24-11-101 holiday
      list from the corpus
- [ ] Identifies the **C.R.C.P. 12(b)(5) motion to
      dismiss** option (Twombly-style, *Warne v. Hall*)
      as an alternative to an immediate answer, and
      correctly states its effect on the answer
      deadline (read from the corpus)

### Substantive defense (co-consumer-debt)

- [ ] Raises **chain-of-title / standing** — the debt
      buyer must prove ownership through an admissible
      assignment chain; a generic "pool" affidavit may
      be insufficient; ties admissibility to
      **C.R.E. 803(6)**
- [ ] Raises the **6-year SOL** under **C.R.S.
      § 13-80-103.5(1)(a)** — verified against
      *Hassler v. Account Brokers* from `key-cases.md`
      (not asserted from memory) — as a potential
      affirmative defense if the debt is old enough
- [ ] Identifies the **CFDCPA (C.R.S. art. 16 of
      title 5)** + **CCPA** + **FDCPA** as potential
      counterclaim / affirmative defense bases if the
      collector used unlawful collection tactics

### Discovery strategy (co-discovery)

- [ ] Uses interrogatories and RFPs within the
      **25-interrogatory cap** (C.R.C.P. 33) to force
      production of the complete assignment chain and
      original account agreement
- [ ] Notes the **conferral requirement** before any
      motion to compel (C.R.C.P. 121 § 1-12 + § 1-15(8))

### Dispositive motion (co-draft-motion)

- [ ] Triages a **C.R.C.P. 56 summary-judgment
      motion** once discovery produces (or fails to
      produce) the assignment chain, supported by an
      unsworn declaration under C.R.S. § 13-27-104 —
      no Certificate of Conferral needed for a
      dispositive motion
- [ ] Attaches a **separate proposed order**
      (cross-reference `co-draft-order`)

### Formatting + verification (co-statewide-format / co-fact-check)

- [ ] All filings carry the two-block Colorado caption
      (left case block + COURT USE ONLY box), line
      numbering, and a self-represented signature
      block (no Atty. Reg. #) per C.R.C.P. 10 +
      CJD 11-01
- [ ] Verifies every C.R.C.P. / C.R.S. / case
      citation against the corpus before filing —
      cites by rule number, never from memory

## Common failure modes

- States a 30-day answer window instead of 21 days
- Treats the spreadsheet + affidavit as conclusive
  proof of ownership without raising the chain-of-
  title defense
- Asserts the SOL period or *Hassler* holding from
  memory instead of the corpus
- Files a motion to compel without a Certificate of
  Conferral
- Uses FRCP citations instead of C.R.C.P.
