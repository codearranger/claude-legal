# in-family-law — Child support under the Indiana Guidelines

## Prompt

I'm in an Indiana paternity (JP) case. We have one child
(age 4). My weekly gross income is $1,100. The mother's
weekly gross income is $900. The child lives primarily
with the mother. How is child support calculated in
Indiana?

## Expected triggers

- `in-family-law`
- `in-family-court`

## Acceptance criteria

- [ ] Identifies the **Indiana Child Support Guidelines**
      as the controlling source — a court rule, not
      statute. Statutory backbone at IC 31-16.
- [ ] Identifies Indiana as an **income-shares** state
- [ ] Walks the calculation framework:
      1. Each parent's **weekly gross income** (broad
         definition — wages, salary, commissions, bonuses,
         self-employment, investment income, government
         benefits)
      2. Guideline deductions (other court-ordered
         support, prior-born-children deduction, health
         insurance, etc.) → **weekly adjusted gross
         income**
      3. Sum to **combined weekly adjusted gross income**
         (here, $1,100 + $900 = $2,000 if no deductions)
      4. Look up basic obligation on the schedule
      5. Each parent's pro rata share: father 55%, mother
         45% (derived from $1,100 / $2,000 and $900 /
         $2,000 — deterministic math from the prompt)
      6. Parenting-time credit (Worksheet B) applies if
         shared physical custody; here the child lives
         primarily with the mother so Worksheet A applies
      7. Additional credits: uninsured medical, work-
         related childcare
- [ ] References **Worksheet A vs. Worksheet B**
      distinction (sole physical vs. shared physical
      custody)
- [ ] **Reads current schedule + combined-income cap from
      the Indiana Child Support Guidelines** (in
      `court-rules/Indiana-Child-Support-Guidelines.md`
      once corpus populated; pointer-stub for now). Does
      NOT hard-code dollar figures for the basic
      obligation
- [ ] References modification framework at IC 31-16-8 —
      substantial and continuing change of circumstances,
      with the statutory shortcut (Guidelines
      recalculation differing by a defined percentage
      threshold creates a presumption). **Reads current
      threshold from `IC-31-16.md`** rather than embedding

## Common failure modes

- Treating support as a percentage-of-payor-income
  calculation (Indiana is income-shares, not percentage)
- Using gross income end-to-end (the Guidelines call for
  weekly **adjusted** gross income for the pro-rata
  step)
- Hard-coding the combined-income cap
- Hard-coding the modification-percentage threshold
- Confusing the Worksheet A / Worksheet B distinction
  (which controls in shared-physical-custody cases)
- Treating the Indiana Parenting Time Guidelines as the
  child-support source (they're a separate court rule
  for parenting time only)
