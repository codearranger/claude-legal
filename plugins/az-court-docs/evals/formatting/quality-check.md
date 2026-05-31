# az-quality-check — Catch a Rule 8(c) affirmative-defense defect + ARCP/ARFLP/JCRCP forum check

## Prompt

Before I file my answer in Arizona, can you review it for problems?
I want to make sure my defenses are pleaded correctly and that I'm
using the right set of rules — I got confused because some forms I
found online cite the family-law rules and some cite the justice
court rules, and my case is a regular civil debt case in Superior
Court.

## Expected triggers

- `az-quality-check`
- `az-statewide-format`
- `az-first-30-days`

## Acceptance criteria

### Affirmative-defense defect (Rule 8(c))

- [ ] Checks that affirmative defenses are **affirmatively pleaded**
      under **Ariz. R. Civ. P. 8(c)** rather than buried in general
      denials, and flags the **waiver risk** for defenses not raised
      (read the current rule from the corpus)
- [ ] Flags common omissions for a debt case (e.g., statute of
      limitations, lack of standing/ownership, payment, accord and
      satisfaction) as candidates to plead under Rule 8(c) —
      cross-reference `az-first-30-days`

### Forum / rule-set check (ARCP vs. ARFLP vs. JCRCP)

- [ ] Confirms the document uses the **Arizona Rules of Civil
      Procedure (ARCP)** for a general civil Superior Court matter —
      NOT the **Arizona Rules of Family Law Procedure (ARFLP)** and
      NOT the **Justice Court Rules of Civil Procedure (JCRCP)**
- [ ] Explains when each rule set applies: ARFLP for family-law
      matters in Superior Court; JCRCP for Justice Court limited
      civil matters; ARCP otherwise — read the scope of each set
      from the references corpus rather than asserting from memory
- [ ] Flags any citation to the wrong rule set as a defect to fix

### Format pass

- [ ] Checks the **Ariz. R. Civ. P. 10** caption, line numbering,
      and self-represented signature (no bar number) via
      `az-statewide-format`

## Common failure modes

- Misses affirmative defenses buried in general denials
- Fails to catch a filing that cites ARFLP or JCRCP in a general
  civil Superior Court matter
- Asserts the scope of each rule set from memory instead of reading
  it from the corpus
