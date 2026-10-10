# ga-family-law — Child support: income-shares worksheet (O.C.G.A. § 19-6-15)

## Prompt

I'm going through a divorce in Georgia and we're working out child
support. I make about $40,000 a year and my spouse makes more. I'll have
the kids a good portion of the time. How does Georgia calculate child
support, and does my parenting time affect the amount?

## Expected triggers

- `ga-family-law`

## Acceptance criteria

### Income-shares model

- [ ] States Georgia uses an **income-shares** child-support guideline
      under **O.C.G.A. § 19-6-15** — both parents' **adjusted gross
      monthly incomes** are combined, the combined figure is run against
      the **Basic Child Support Obligation (BCSO) table**, and the
      obligation is **prorated by each parent's share** of combined income
      — reads the methodology from the corpus rather than asserting a
      dollar amount
- [ ] Directs the user to the official **Georgia Child Support Commission
      worksheet / online calculator** (csconlinecalc.georgiacourts.gov)
      and instructs running it with the actual income figures — reads the
      current worksheet reference from the skill rather than asserting a
      support amount from memory
- [ ] Notes the guideline is a **rebuttable presumption**; deviations
      require **written findings** — reads the deviation factors from the
      corpus

### Add-ons and adjustments

- [ ] Identifies the statutory add-ons and adjustments — **health
      insurance**, **work-related child care**, and the **parenting-time
      adjustment** — and the **low-income / self-support reserve**
      adjustment — reads each from the corpus rather than asserting
      figures
- [ ] Flags that **O.C.G.A. § 19-6-15 was revised effective January 1,
      2026**, so the **current post-2026 text and BCSO table must be read
      from the references corpus** — does not rely on a remembered version

### Modification

- [ ] Notes child support is **modifiable** on a substantial change in
      circumstances, including an involuntary income loss meeting the
      statutory threshold (O.C.G.A. § 19-6-15(k)) — reads the threshold
      from the corpus

## Common failure modes

- Asserts a specific support dollar amount instead of pointing to the
  Commission worksheet/calculator
- Describes a percentage-of-obligor-income model (Georgia is income
  shares, not flat percentage)
- Relies on a pre-2026 version of § 19-6-15 instead of reading the current
  post-January-2026 text from the corpus
- Omits the parenting-time adjustment or the deviation-findings
  requirement
