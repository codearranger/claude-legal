# mi-first-30-days — Answer + MCR 2.111(F) separate affirmative defenses + summary-disposition triage

## Prompt

I just got served with a complaint in Michigan. I think the
claim is too old and I'm not even sure they have the right to
sue me. What do I file first, how do I answer the complaint
correctly, and is there a way to get the whole thing dismissed
early?

## Expected triggers

- `mi-first-30-days`
- `mi-draft-motion`
- `mi-statewide-format`
- `mi-pro-se`

## Acceptance criteria

### Answering the complaint (MCR 2.111)

- [ ] Explains the answer must respond to each numbered
      allegation (admit / deny / state lack of knowledge) per
      **MCR 2.111**, and that an inadequate response can be
      treated as an admission
- [ ] States the time to answer comes from **MCR 2.108** and
      depends on the manner of service (read current day counts
      from the references corpus; cross-reference `mi-deadlines`)

### Separate affirmative defenses (MCR 2.111(F))

- [ ] **Requires that affirmative defenses be stated separately
      under MCR 2.111(F)** — pleaded in a distinct, separately
      captioned section — and warns that affirmative defenses
      **not raised in the responsive pleading may be waived**
- [ ] Lists the candidate affirmative defenses raised by the
      facts (e.g., **statute of limitations**, lack of standing /
      failure of the plaintiff to own the claim, payment,
      accord and satisfaction) and ties SOL to the limitations
      statute read from `mi-statutes-debt/` (MCL 600.5807) rather
      than asserting a number

### Summary-disposition triage (MCR 2.116)

- [ ] Triages the early-dispositive options under **MCR 2.116**:
      **(C)(7)** (claim barred — e.g., statute of limitations),
      **(C)(8)** (failure to state a claim, on the pleadings),
      **(C)(10)** (no genuine issue of material fact, on the
      record) — and matches the litigant's facts to the right
      subrule
- [ ] Notes the relationship between pleading the SOL as an
      affirmative defense and moving for summary disposition
      under (C)(7)

### Composition

- [ ] Self-represented signature block (no P-number)

## Common failure modes

- Buries affirmative defenses in the body instead of a separate
  MCR 2.111(F) section, risking waiver
- Conflates MCR 2.116(C)(7), (C)(8), and (C)(10)
- Asserts the limitations period from memory instead of reading
  MCL 600.5807 from the corpus
- Treats the answer deadline as a fixed number regardless of
  service mode
