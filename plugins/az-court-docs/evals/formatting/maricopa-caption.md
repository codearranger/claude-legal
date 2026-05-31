# az-maricopa — Superior Court of Arizona / Maricopa County caption

## Prompt

My case is in Maricopa County. What exactly do I put at the top of
the page for the court name and county? I've seen "Superior Court
of Arizona" and "Maricopa County" both used and I don't want to get
it wrong.

## Expected triggers

- `az-maricopa`
- `az-statewide-format`

## Acceptance criteria

### Court identification

- [ ] States the correct caption header for the trial court:
      **Superior Court of Arizona, Maricopa County** (the Superior
      Court is a single statewide court sitting in each county) —
      read the exact wording/format from `az-maricopa` rather than
      asserting from memory
- [ ] Notes Maricopa-specific filing/division practice (read current
      specifics — e-filing, division/department assignment — from
      the corpus) without inventing local rule numbers

### Caption mechanics

- [ ] Ties the rest of the caption to **Ariz. R. Civ. P. 10**
      (parties, case number, document title) via
      `az-statewide-format`
- [ ] Distinguishes the Superior Court caption from a **Justice
      Court** or **Maricopa County Justice Precinct** caption (those
      are a different forum with a different caption — see
      `az-justice-courts`)

### Honest sourcing

- [ ] Reads Maricopa local specifics from the references corpus
      rather than asserting local rule numbers or division names
      from memory

## Common failure modes

- Mislabels the court (e.g., "Maricopa County Superior Court" word
  order, or treating it as a separate court rather than the
  Superior Court of Arizona sitting in Maricopa County)
- Confuses the Superior Court caption with a Justice Court caption
- Invents a local division/department or local rule number
