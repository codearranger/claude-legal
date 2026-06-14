# co-family-law — Child support + 93-overnight rule + JDF 1820 E worksheet

## Prompt

I'm going through a divorce in Colorado and we're working
out child support. My spouse wants a lot — I'll have the
kids about half the time, probably around 180 nights a
year. Does my time with the kids affect the support
calculation, and how does Colorado figure out the amount?

## Expected triggers

- `co-family-law`

## Acceptance criteria

### Income-shares model

- [ ] States Colorado uses an **income-shares** child-
      support guideline under **C.R.S. § 14-10-115** —
      both parents' incomes are combined to determine
      the total support obligation, then allocated in
      proportion to each parent's share of combined
      income
- [ ] Directs the user to compute support using the
      official statewide online **JDF 1820 E worksheet**
      — reads the current worksheet reference from the
      skill rather than asserting specific support
      amounts from memory

### The 93-overnight rule

- [ ] Explains the **93-overnight shared-physical-care
      adjustment**: when the **obligor** has **93 or
      more overnights per year** with the children, the
      guideline applies a parenting-time adjustment that
      reduces (but does not eliminate) the support
      obligation — reads the current threshold and
      formula from **C.R.S. § 14-10-115** / the
      references corpus rather than asserting the
      adjustment percentage from memory
- [ ] Notes that at **180 nights** the filer is well
      above the 93-overnight threshold and the shared-
      physical-care adjustment applies; instructs the
      filer to run the JDF 1820 E worksheet with the
      actual overnight count

### Deviation factors

- [ ] Notes the court may **deviate** from the guideline
      amount for good cause (extraordinary expenses,
      shared physical care beyond the guideline, etc.)
      — reads the deviation factors from the corpus
      rather than asserting them from memory

### Modification

- [ ] Notes that child support is **modifiable** upon a
      showing of **changed circumstances** producing at
      least a **10% change** in the support amount
      (**C.R.S. § 14-10-122**) — reads the threshold
      from the corpus

## Common failure modes

- Asserts a specific support dollar amount instead of
  pointing to the JDF 1820 E worksheet
- States the 93-overnight threshold as some other
  number from memory
- Fails to apply the shared-physical-care adjustment
  when overnight count is disclosed
- Conflates the 93-overnight rule with a 50/50 split
  that eliminates support entirely
