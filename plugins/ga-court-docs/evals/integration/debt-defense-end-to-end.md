# Integration — End-to-end debt defense in a Georgia State Court

## Prompt

I just got served with a civil summons and complaint from the State Court
of Cobb County. A debt buyer claims I owe about $6,000 on an old credit
card — my last payment was in early 2019. They attached a spreadsheet and
a one-page affidavit. Walk me through the whole thing — how long I have to
respond, whether they even own the debt, whether it's too old, how to get
their documents, and how to format and file everything.

## Expected triggers

- `ga-first-30-days`
- `ga-consumer-debt`
- `ga-discovery`
- `ga-draft-motion`
- `ga-statewide-format`
- `ga-fact-check`

## Acceptance criteria

### Forum + deadline (ga-first-30-days / ga-deadlines)

- [ ] Confirms **State Court of Cobb County** is the correct forum for a
      debt suit (limited jurisdiction, no dollar ceiling; subject-matter,
      not dollar-amount split) and states the **30-day answer window**
      under **O.C.G.A. § 9-11-12(a)** plus the **15-day open-default**
      window under § 9-11-55(a) — reads day counts and the § 1-4-1 holiday
      list from the corpus and applies § 9-11-6(a) / § 1-3-1(d)(3)
      roll-forward

### Substantive defenses (ga-consumer-debt)

- [ ] Raises **chain-of-title / standing** — the debt buyer must prove an
      admissible assignment chain (*Nyankojo*); a generic "pool" affidavit
      may be insufficient (*Wirth*, *Rutledge*); ties admissibility to
      **O.C.G.A. § 24-8-803(6)** — cases verified against `key-cases.md`
- [ ] Raises the **6-year written-contract SOL (O.C.G.A. § 9-3-24)** for a
      credit card per **Hill v. American Express** — NOT the 4-year
      open-account SOL — and tests the 2019 accrual against it; verified
      against `key-cases.md`
- [ ] Identifies the **FBPA (O.C.G.A. § 10-1-390 et seq.)** + **FDCPA** as
      counterclaim bases if the collector used unlawful tactics, and flags
      the § 10-1-399(b) 30-day demand prerequisite for an FBPA claim

### Counterclaim posture (ga-first-30-days)

- [ ] Pleads any same-transaction collection-abuse claim as a **compulsory
      counterclaim** under **O.C.G.A. § 9-11-13(a)** in the answer

### Discovery (ga-discovery)

- [ ] Uses interrogatories (within the § 9-11-33 cap, read from the corpus)
      and RFPs (§ 9-11-34) to force production of the full assignment chain
      and the original cardmember agreement, within the **USCR 5 six-month
      discovery period**; a non-response routes to a § 9-11-37 motion to
      compel set by **Rule Nisi**

### Dispositive motion (ga-draft-motion)

- [ ] Triages an **O.C.G.A. § 9-11-56 summary-judgment** motion once
      discovery fails to produce the chain — leveraging *Lau's Corp. v.
      Haskins* (movant may point to the absence of evidence) — supported by
      an affidavit on personal knowledge (§ 9-11-56(e)), with a **separate
      proposed order**

### Formatting + verification (ga-statewide-format / ga-fact-check)

- [ ] All filings carry the Georgia caption naming the **STATE COURT OF
      COBB COUNTY / STATE OF GEORGIA** with **"Civil Action File No."**, a
      certificate of service (§ 9-11-5), and a pro-se signature block (no
      Georgia Bar No.); filed via **PeachCourt** (Cobb)
- [ ] Verifies every O.C.G.A. / USCR / case citation against the corpus and
      `key-cases.md` before filing — never from memory

## Common failure modes

- States a 20-day answer window instead of 30 days
- Applies the 4-year open-account SOL to the credit card instead of the
  6-year § 9-3-24 written-contract SOL
- Treats the spreadsheet + affidavit as conclusive proof of ownership
- Routes the Cobb filing to Odyssey eFileGA instead of PeachCourt
- Uses "Case No." instead of "Civil Action File No."
- Cites FRCP rules instead of O.C.G.A. § 9-11 counterparts
