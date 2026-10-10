# az-commercial-disputes — Maricopa Commercial Court + Arizona Uniform Trade Secrets Act

## Prompt

My small Arizona company is in a dispute with a former partner who
took our customer list and pricing formulas to a competitor. The
amounts involved are substantial. Is there a special court for
business cases in Arizona, and what's my claim for the stolen trade
secrets?

## Expected triggers

- `az-commercial-disputes`
- `az-maricopa`

## Acceptance criteria

### Commercial Court forum

- [ ] Identifies the **Commercial Court** program in **Maricopa
      County Superior Court** as the specialized docket for qualifying
      business/commercial disputes, and reads the **eligibility
      criteria** (case types, the amount-in-controversy threshold, the
      assignment/transfer mechanism) from the references corpus rather
      than asserting the threshold number from memory
      (cross-reference `az-maricopa`)
- [ ] Notes the matter still proceeds under the **Arizona Rules of
      Civil Procedure (ARCP)** plus any Commercial Court supplemental
      procedures (read from the corpus)

### Trade-secret claim (AUTSA)

- [ ] Identifies the **Arizona Uniform Trade Secrets Act (AUTSA),
      A.R.S. § 44-401 et seq.** as the governing claim, and reads the
      **definition of a trade secret**, the **misappropriation**
      elements, and the **remedies** (injunction, damages, exemplary
      damages, attorney's fees) from `az-statutes-debt/` rather than
      asserting the elements or section numbers from memory
- [ ] Notes AUTSA's **displacement/preemption** of conflicting
      common-law tort claims for the same misappropriation (read the
      scope from the corpus)

### Honest sourcing

- [ ] Reads the Commercial Court eligibility threshold and the AUTSA
      elements/remedies from the corpus; cites Arizona authority by
      A.R.S. section / rule number

## Common failure modes

- Asserts the Commercial Court eligibility amount from memory
- Recites the AUTSA elements, remedies, or section numbers from
  memory
- Misses AUTSA's displacement of duplicative common-law claims
- Treats the Commercial Court as a separate court rather than a
  docket within Maricopa County Superior Court
