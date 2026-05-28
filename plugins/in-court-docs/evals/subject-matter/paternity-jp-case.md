# in-family-law — Paternity (JP) case in a non-flagship county

## Prompt

I'm in Indiana, Columbus area (Bartholomew County). I'm the
biological father of a 2-year-old child but I'm not married
to the mother. I'd like to establish paternity and get a
parenting-time order. What's the case type, where do I
file, and what's the procedural framework?

## Expected triggers

- `in-family-law`
- `in-family-court`
- `in-county-courts`
- `in-pro-se`

## Acceptance criteria

- [ ] Identifies the case type as **JP — Juvenile
      Paternity** under IC 31-14
- [ ] Identifies Bartholomew County's family-law topology:
      no separate Juvenile Division; **Bartholomew Circuit
      Court (03C01)** hears JP cases directly
- [ ] Provides the expected cause-number shape:
      `03C01-YYYYY-JP-NNNNNN`
- [ ] Identifies the **venue framework** under IC 31-14
      (broader than typical Trial Rule 75 venue —
      petition may be filed in the county of mother's
      residence, alleged father's residence, OR child's
      birth / residence). **Reads current details from
      `in-law-references/references/in-statutes-debt/
      IC-31-14.md`** rather than embedding subsection
      numbers
- [ ] Walks the procedural framework:
      1. Verified petition under IC 31-14
      2. Service under Trial Rule 4
      3. Answer / response window per Trial Rule 6 / 12
         (current day count via `in-deadlines`)
      4. Genetic testing if contested (IC 31-14-6
         framework)
      5. Final order — paternity adjudication + custody +
         parenting time + child support
- [ ] References the **Indiana Parenting Time Guidelines**
      (court rule) for default residential time
- [ ] References the **Indiana Child Support Guidelines**
      (court rule) for support calculation
- [ ] Notes Indiana's filing system: Odyssey statewide
      e-filing (mandatory for represented parties; pro-se
      may use paper or `mycase.in.gov` public portal)
- [ ] Notes that Indiana has no family-law-facilitator
      equivalent — pro-se filers rely on the Indiana
      Self-Service Center forms at courts.in.gov/help/
      self-service and the court clerk (clerks can't give
      legal advice)

## Common failure modes

- Treating Bartholomew as if it has a Juvenile Division
  (it doesn't — Circuit Court handles JP)
- Using a JC, DR, or DC case-type code (JP is the right
  code for non-marital paternity establishment)
- Hard-coding the venue subsection number rather than
  pointing to IC-31-14.md
- Treating the venue as restricted to mother's-county
  Trial Rule 75 venue
- Confusing JP (paternity) with JC (CHINS / DCS abuse-
  neglect-dependency) or JM (juvenile misc)
- Missing the Indiana Parenting Time Guidelines reference
- Inventing a specific worksheet / form name without
  consulting the Self-Service Center
