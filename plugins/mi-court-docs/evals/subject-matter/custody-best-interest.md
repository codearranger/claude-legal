# mi-family-law — Custody dispute applying the MCL 722.23 best-interest factors + established custodial environment

## Prompt

My ex and I are fighting over custody of our two kids in
Michigan. The kids have lived with me for the last three years
and I want to keep primary custody. My ex is asking the court to
change it. What does a Michigan court actually look at when it
decides custody, and does the fact that the kids have been with
me matter?

## Expected triggers

- `mi-family-law`
- `mi-family-court`

## Acceptance criteria

### The best-interest factors (MCL 722.23)

- [ ] Identifies the **Child Custody Act** and that custody is
      decided on the **best interests of the child** under
      **MCL 722.23** — and **walks the statutory best-interest
      factors (a)–(l) read from `mi-statutes-debt/` (Michigan
      family corpus)** rather than reciting the factor list from
      memory
- [ ] Applies the litigant's facts to several relevant factors
      (e.g., stability/continuity, the home environment, moral
      fitness, the child's preferences where age-appropriate)
      without asserting outcomes

### Established custodial environment (ECE)

- [ ] Identifies the **established custodial environment**
      concept (MCL 722.27) — where the child looks to a parent
      for guidance, discipline, the necessities of life, and
      parental comfort over an appreciable time
- [ ] Explains the **burden-of-proof consequence**: if a
      proposed change would alter an established custodial
      environment, the moving party must show **clear and
      convincing evidence** that the change is in the child's
      best interests; otherwise the **preponderance** standard
      applies — cite the controlling authority and read the
      current standard from the corpus rather than asserting it

### Modification gate

- [ ] Notes the **proper-cause / change-of-circumstances**
      threshold the moving party must clear before the court
      revisits a prior custody order (cite the controlling
      authority; read current standard from the corpus)
- [ ] Routes the matter through the **Family Division of Circuit
      Court** (cross-reference `mi-family-court`)

## Common failure modes

- Recites or invents best-interest factors instead of reading
  MCL 722.23 from the corpus
- Ignores the established custodial environment and its effect
  on the burden of proof
- Skips the proper-cause / change-of-circumstances modification
  threshold
- Predicts a custody outcome rather than framing the analysis
