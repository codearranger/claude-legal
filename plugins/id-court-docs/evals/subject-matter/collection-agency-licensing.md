# id-consumer-debt — Idaho Collection Agency Act licensing

## Prompt

How do I check whether the company suing me in Idaho is even allowed
to collect debts here, and what happens if they aren't licensed?

## Expected triggers

- `id-consumer-debt`

## Acceptance criteria

- [ ] Identifies the **Idaho Collection Agency Act (I.C. § 26-2222 et
      seq.)**, administered by the **Idaho Department of Finance**, as
      the licensing regime
- [ ] States that a collection agency — and a **debt buyer** that
      acquired the debt while it was **delinquent or in default** —
      must be **licensed** (§ 26-2223), reading the operative
      subsection scope from `id-statutes-debt/` rather than reciting it
      from memory
- [ ] Explains how to verify licensure (Idaho Department of Finance,
      finance.idaho.gov) and frames unlicensed collection as a
      capacity / affirmative-defense and potential **Idaho Consumer
      Protection Act** angle
- [ ] Does not overstate the remedy — routes the consequence/penalty
      question to the statute text and case-law research

## Common failure modes

- Says Idaho has no collection-agency licensing regime
- Claims debt buyers are categorically exempt
- Recites penalty provisions or subsection numbers from memory
