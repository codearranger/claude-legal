# id-fact-check — citation verification

## Prompt

Check the citations in my Idaho brief before I file it.

## Expected triggers

- `id-fact-check`

## Acceptance criteria

- [ ] Verifies case citations are in **Idaho form**: official **Idaho
      Reports** plus the **Pacific Reporter** parallel (e.g.,
      `113 Idaho 730, 747 P.2d 752 (1987)`), with the **(Ct. App.
      YEAR)** designation for Court of Appeals decisions and no court
      designation for Supreme Court decisions
- [ ] Confirms statutory cites use `Idaho Code § ...` / `I.C. § ...`
      and rule cites use `I.R.C.P.` / `I.R.E.` / `I.R.F.L.P.` / `I.A.R.`
- [ ] Notes Idaho has **no neutral / public-domain citation** format
- [ ] Checks cited authority against the references corpus and routes
      unknown or unverifiable cases to case-law research
      (CourtListener `idaho` / `idahoctapp`) rather than asserting them
- [ ] Does not invent reporter page numbers or parallel cites

## Common failure modes

- Accepts a citation with no Pacific Reporter parallel
- Invents a neutral-citation format for Idaho
- Fabricates a reporter cite instead of flagging it for lookup
