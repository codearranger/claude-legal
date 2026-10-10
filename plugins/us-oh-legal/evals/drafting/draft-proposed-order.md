# oh-draft-order — Proposed Order

## Prompt

The court just orally granted my motion to compel in Ohio.
The magistrate said "submit a proposed order." How do I
draft it? My case is in Hamilton County, CV-25-009876.

## Expected triggers

- `oh-draft-order`
- `oh-hamil`
- `oh-submit-order`
- `oh-statewide-format`

## Acceptance criteria

### Structure

- [ ] Civ. R. 10(A) caption with Hamilton County Common
      Pleas court name
- [ ] Title: `ORDER GRANTING DEFENDANT'S MOTION TO COMPEL`
- [ ] One short "This matter came before the Court..."
      paragraph
- [ ] "IT IS THEREFORE ORDERED..." operative provisions in
      numbered subparts
- [ ] Specific relief (deadline for production; sanction
      reserved)
- [ ] Date line + judge signature line
- [ ] "JUDGE _________________" + line for printed name
- [ ] Distribution list / certificate of service block at
      bottom

### Content

- [ ] Tracks the relief actually granted (not broader)
- [ ] Date-certain deadlines (e.g., "within 14 days of
      this order")
- [ ] No findings of fact beyond what the court stated

## Common failure modes

- Drafting findings the judge did not make
- Overbroad operative provisions
- Missing date line
- Forgetting magistrates sign as MAGISTRATE, not JUDGE —
  if the magistrate ruled, the order should accommodate
  Civ. R. 53 magistrate-decision format with the 14-day
  objection clock
