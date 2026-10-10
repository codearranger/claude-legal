# az-draft-declaration — Notarized affidavit + the Rule 80(c) unsworn-declaration alternative

## Prompt

I'm self-represented in Arizona. My summary-judgment motion needs
a sworn statement from me laying out the facts — that the debt
buyer never sent me any account records and that I don't recognize
the account. Do I need to get this notarized, or is there a way to
sign it under penalty of perjury without a notary?

## Expected triggers

- `az-draft-declaration`
- `az-statewide-format`
- `az-pro-se`

## Acceptance criteria

### Form selection

- [ ] Explains the two routes: a **notarized affidavit** (sworn
      before a notary) versus an **unsworn declaration under
      Ariz. R. Civ. P. 80(c)** signed under penalty of perjury
      without a notary
- [ ] States the Rule 80(c) declaration requirements — read the
      exact certification language and any in-state/out-of-state
      distinctions from the references corpus rather than asserting
      the wording from memory
- [ ] Notes that the Rule 80(c) unsworn declaration is the
      pro-se-friendly default when a notary is not readily
      available

### Caption and structure

- [ ] Caption per **Ariz. R. Civ. P. 10** matching the related
      motion; title identifies it as an Affidavit or Declaration of
      [name]
- [ ] Numbered paragraphs, each stating facts **on personal
      knowledge** — distinguishes facts (sworn) from argument
      (belongs in the motion, not the affidavit/declaration)
- [ ] For the notarized route, includes a jurat block; for the
      Rule 80(c) route, includes the penalty-of-perjury
      certification (language read from the corpus) — does not mix
      the two

### Composition (az-pro-se)

- [ ] Self-represented signature block; no State Bar of Arizona
      number
- [ ] Avoids conclusory or legal-argument statements dressed up as
      sworn facts

## Common failure modes

- Assumes notarization is always required and omits the Rule 80(c)
  unsworn-declaration alternative
- Recites the penalty-of-perjury certification language from
  memory instead of reading it from the corpus
- Blends argument into the sworn paragraphs
- Adds a bar number to a pro-se signature block
