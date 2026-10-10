# in-family-law — UCCJEA IC 31-21 + Bartholomew Circuit Court consolidated jurisdiction

## Prompt

My custody case started in Indiana two years ago. The mother
has now moved with the kids to Ohio and filed a custody
modification case there. I'm in Columbus, Indiana (Bartholomew
County). Which state has jurisdiction to decide custody now,
and what Indiana court would I use if Indiana keeps the case?

## Expected triggers

- `in-family-law`
- `in-family-court`
- `in-county-courts`

## Acceptance criteria

### UCCJEA — IC 31-21

- [ ] Identifies the **Uniform Child Custody Jurisdiction
      and Enforcement Act (UCCJEA)** enacted in Indiana
      as **IC 31-21** as the controlling framework for
      interstate custody jurisdiction
- [ ] States the UCCJEA home-state rule: the state where
      the child lived for the **6 months immediately
      before** the proceeding is the "home state" with
      priority jurisdiction — reads the current period
      from the corpus rather than asserting a number
- [ ] Applies the home-state analysis to the scenario:
      Indiana was the original home state; the question
      is whether Indiana retains **exclusive continuing
      jurisdiction** (ICC) or whether the children's
      new residence in Ohio has become the home state
      — points to the specific UCCJEA factors from
      `IC-31-21.md`
- [ ] Notes the simultaneous-proceeding risk: IC 31-21
      requires Indiana to communicate with the Ohio court
      to determine which state should proceed; the
      parties cannot litigate simultaneously in both
      states

### Bartholomew County — consolidated Circuit Court jurisdiction

- [ ] Identifies Bartholomew County as a county where
      the **Circuit Court** (not a separate Superior
      Court) handles family law — including dissolution,
      paternity (JP cases), custody, and juvenile matters
      — by consolidation of jurisdiction
- [ ] Notes that Indiana's family-court topology varies
      by county: larger counties (Marion, Lake, Allen,
      Hamilton, St. Joseph, Vanderburgh) have dedicated
      Juvenile Divisions; smaller counties like
      Bartholomew consolidate family and juvenile
      jurisdiction in the Circuit Court — reads this
      topology from `in-family-court` / `in-county-courts`
      rather than asserting it from memory

### Corpus-first discipline

- [ ] Reads the UCCJEA home-state period, ICC criteria,
      and Bartholomew venue configuration from the
      references corpus; does not assert specific day
      counts or factors from memory

## Common failure modes

- States that Indiana automatically loses jurisdiction
  once the children move (UCCJEA requires an ICC
  analysis; Indiana retains jurisdiction while a
  connection remains and no other state is the home
  state under certain conditions)
- Asserts the 6-month home-state period from memory
  without verifying against the corpus
- Directs the user to a "Bartholomew Superior Court
  Family Division" (Bartholomew County does not have
  a dedicated family division — the Circuit Court has
  consolidated jurisdiction)
- Fails to note the simultaneous-proceeding prohibition
