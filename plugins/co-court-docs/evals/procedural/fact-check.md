# co-fact-check — Citation verification + internal consistency + corpus-sourced cites

## Prompt

I've drafted a motion for summary judgment in a Colorado
consumer-debt case. Before I file it, I want to verify that
all my citations are accurate, the facts in my declaration
match what I said in the motion, and there are no internal
inconsistencies. How do I do that?

## Expected triggers

- `co-fact-check`
- `co-quality-check`

## Acceptance criteria

### Citation verification (pass 1)

- [ ] Checks every **C.R.C.P. / C.R.S. / case citation**
      against the corpus or a structured source —
      specifically:
      - C.R.C.P. rule numbers match the rules corpus
      - C.R.S. section numbers and titles verified
        against `co-statutes-debt/` or the references
        corpus
      - Case citations (especially *Warne v. Hall*,
        *Hassler v. Account Brokers*) verified against
        `key-cases.md` — never asserted from memory
- [ ] Notes the **Colorado neutral-citation format**
      (post-2012 `[YEAR] CO [###]` for Supreme Court,
      `[YEAR] COA [###]` for Court of Appeals) and
      confirms the format is used where applicable

### Internal consistency (pass 2)

- [ ] Verifies the **motion body and declaration** tell
      the same factual story — no date conflicts,
      amount discrepancies, or conflicting party
      descriptions
- [ ] Checks that **exhibit references** in the
      motion ("attached as Exhibit A") correspond to
      an actual exhibit attached to the declaration

### Packet consistency (pass 3)

- [ ] Confirms the **caption is identical** across all
      filed documents (motion, declaration, proposed
      order): same court, case number, division,
      parties, and title format
- [ ] Confirms the **proposed order** grants exactly
      the relief requested in the motion body — no
      broader or narrower relief

### Sworn-vs-argued consistency (pass 4)

- [ ] Verifies that any legal conclusions in the motion
      are NOT repeated as sworn facts in the
      declaration — declarations contain personal-
      knowledge facts; arguments live in the motion

## Common failure modes

- Accepts a case citation without verifying it in
  key-cases.md or a structured source
- Misses a date discrepancy between the motion and
  the declaration
- Applies Old-style citation format (P.2d / Colo.)
  to a post-2012 opinion instead of the neutral
  citation
- Lets legal argument creep into the declaration
  as a "sworn fact"
