# az-law-references — Locating the controlling Arizona civil authority

## Prompt

I'm self-represented in an Arizona civil case and I keep seeing
references to "the rules" and "the statutes." Where do I actually
find the controlling Arizona civil procedure rules, the evidence
rules, the relevant statutes, and how Arizona citations are
supposed to look?

## Expected triggers

- `az-law-references`

## Acceptance criteria

### Rule and statute sources

- [ ] Points to the **Arizona Rules of Civil Procedure (ARCP)** and
      **Arizona Rules of Evidence** in the `court-rules/` corpus, and
      the **Arizona Revised Statutes (A.R.S.)** in `az-statutes-debt/`
      — reads the actual contents from the corpus rather than
      asserting section numbers from memory
- [ ] Notes the distinct rule sets (ARCP general civil, ARFLP family,
      JCRCP justice court) and that the correct set depends on forum
      / matter type

### Citation format

- [ ] References the Arizona citation conventions in
      `citation-format.md` (A.R.S. § form, Ariz. R. Civ. P. form,
      Arizona Reports / P.3d reporter form) rather than asserting a
      citation style from memory

### Online / API sources

- [ ] Points to `online-sources.md` and `legal-data-apis.md` for the
      canonical human-facing URLs and structured sources, rather than
      inventing URLs

### Honest sourcing

- [ ] Treats `az-law-references` as the canonical corpus host and
      reads current contents from it rather than reciting from memory

## Common failure modes

- Asserts A.R.S. section numbers or rule numbers from memory
- Invents citation conventions or source URLs
- Conflates the three Arizona rule sets
