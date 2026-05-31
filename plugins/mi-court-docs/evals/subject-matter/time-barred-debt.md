# mi-consumer-debt — Time-barred debt: SOL defense via MCR 2.116(C)(7) / pleaded under MCR 2.111(F)

## Prompt

A collector is suing me in Michigan on a credit-card debt I
stopped paying more than six years ago. I've heard there's a
time limit on how long they have to sue. Is this debt too old,
and how do I raise that in court?

## Expected triggers

- `mi-consumer-debt`
- `mi-first-30-days`
- `mi-draft-motion`

## Acceptance criteria

### The limitations period (read from the corpus)

- [ ] Identifies the Michigan **statute of limitations on
      contract claims** as the operative defense and **cites
      MCL 600.5807, reading the current limitations period from
      `mi-statutes-debt/`** rather than asserting "six years" (or
      any number) as a fact from memory
- [ ] Notes that **accrual** is fact-dependent (the clock
      generally runs from breach / last activity depending on
      the claim) and that the litigant must pin down the accrual
      date; reads the accrual framework from the corpus
- [ ] Flags that a **partial payment or written acknowledgment**
      can affect / restart the limitations analysis (cite the
      controlling authority; read current rule from the corpus)
      and warns against admissions that could revive the clock

### Raising it procedurally

- [ ] **Plead the SOL as a separate affirmative defense under
      MCR 2.111(F)** in the answer or risk waiver (cross-
      reference `mi-first-30-days`)
- [ ] Move for **summary disposition under MCR 2.116(C)(7)**
      (claim barred by the statute of limitations) — explains
      (C)(7) is the correct subrule for a limitations bar and
      drafts it per `mi-draft-motion`

### Collection-context cautions

- [ ] Notes that suing on / threatening suit on a time-barred
      debt, and that re-aging, can implicate the FDCPA and the
      Michigan RCPA/MCPA (read specifics from the corpus)

## Common failure modes

- Asserts the limitations period as a hard number from memory
  instead of reading MCL 600.5807 from the corpus
- Raises the SOL as a (C)(8) or (C)(10) motion instead of (C)(7)
- Forgets the MCR 2.111(F) separate-defense pleading requirement
- Misses that partial payment / acknowledgment can restart the
  clock
