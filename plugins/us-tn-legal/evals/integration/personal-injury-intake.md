# Integration — Personal-injury intake against a city

## Prompt

I slipped on a broken city sidewalk in Tennessee and broke my
wrist about four months ago. The city says it's not their
fault and I was being careless. Can I sue the city, how long
do I have, and what should I know before I do?

## Expected triggers

- `tn-personal-injury`
- `tn-deadlines`

## Acceptance criteria

### Statute of limitations

- [ ] States the **1-year personal-injury statute of
      limitations** under **T.C.A. § 28-3-104**
- [ ] Flags that suing a governmental entity triggers the
      **shortened SOL** under the GTLA (T.C.A. § 29-20-305,
      ~12 months — verify the current figure against the
      references corpus) and to treat the deadline as urgent
      given it is already ~4 months out

### Governmental Tort Liability Act (GTLA)

- [ ] Identifies the **GTLA (T.C.A. § 29-20-101 et seq.)** as
      the framework for suing a Tennessee city: governmental
      immunity is removed only in enumerated categories
      (immunity-removal framework §§ 29-20-201 to -205)
- [ ] States the GTLA **damages caps** (per-person /
      per-occurrence aggregate under § 29-20-403) and cites the
      statute, reading the current cap figures from the
      references corpus rather than asserting fixed dollar
      amounts

### Comparative fault

- [ ] Applies **modified comparative fault with a 49% bar**
      under ***McIntyre v. Balentine*, 833 S.W.2d 52 (Tenn.
      1992)**: the plaintiff recovers only if their fault is
      **less than 50%**, and recovery is reduced by the
      plaintiff's percentage of fault
- [ ] Responds to the city's "you were careless" position
      through the comparative-fault lens (allocation, not
      automatic bar unless fault reaches 50%)

### Deadlines (tn-deadlines)

- [ ] Computes the filing deadline urgency from the date of
      injury; applies **Tenn. R. Civ. P. 6.01** roll-forward and
      the **§ 15-1-101** holiday list where the deadline lands
      on a weekend/holiday

## Common failure modes

- Uses a 2-year or 3-year tort SOL instead of the 1-year
  § 28-3-104 period
- Misses the GTLA shortened SOL and damages caps entirely
- Asserts GTLA cap figures as fixed dollar amounts rather than
  citing the statute / current law
- Treats the plaintiff's carelessness as an automatic bar
  rather than applying McIntyre's 49% modified comparative-fault
  rule
