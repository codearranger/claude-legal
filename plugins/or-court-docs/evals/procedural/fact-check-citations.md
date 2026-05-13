# or-fact-check — Citation verification pass

## Prompt

Fact-check the attached motion. Verify every citation against
the canonical sources.

[Attach a sample motion containing a mix of correct and
incorrect citations — e.g., "Mattiza v. Foster, 311 Or. 1,
803 P.3d 723 (1990)" — both periods incorrect, and 803 P3d
should be P2d.]

## Expected triggers

- `or-fact-check`
- `or-law-references` (for citation conventions)

## Acceptance criteria

### Citation pass

- [ ] Identifies "Or." as wrong format (Oregon Style omits
      period — should be "Or")
- [ ] Identifies "P.3d" as wrong format (should be "P3d")
- [ ] Identifies "803 P3d 723 (1990)" as inconsistent —
      1990 predates the P3d series; should be P2d
- [ ] Correctly outputs the verified citation form:
      "Mattiza v. Foster, 311 Or 1, 803 P2d 723 (1990)"
- [ ] Uses WebFetch to verify on CourtListener
- [ ] References `or-law-references/references/citation-
      format.md` for the Oregon Style Manual conventions

### Internal consistency

- [ ] Checks that dates referenced in the motion match the
      declaration
- [ ] Checks party names match the caption
- [ ] Checks paragraph cross-references actually point to the
      claimed paragraphs

### Output

- [ ] Returns a pass/warn/fail report
- [ ] Suggests specific corrections
- [ ] Does NOT silently rewrite the motion — user review
      required

## Common failure modes

- Missing the "Or." vs. "Or" issue (Bluebook vs. OACSM)
- Accepting "P.3d" with periods
- Not catching the P2d vs. P3d era mismatch
- Skipping consistency checks
- Auto-rewriting without flagging
