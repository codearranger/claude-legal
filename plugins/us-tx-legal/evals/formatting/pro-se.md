# tx-pro-se — self-represented signing + Statement of Inability

## Prompt

I'm representing myself in a Texas civil case and I can't afford the
filing fees. How do I sign my filings, and how do I ask the court to
waive the costs?

## Expected triggers

- `tx-pro-se`
- `tx-statewide-format`

## Acceptance criteria

### Self-represented signature

- [ ] Provides a **pro-se signature block with NO State Bar of Texas
      bar number** — name, address, phone, email, and "Defendant" /
      "Plaintiff, Pro Se" (TRCP 57 form adapted for a self-represented
      party)

### Verification by unsworn declaration

- [ ] Where a filing must be sworn/verified, offers a **CPRC § 132.001
      unsworn declaration** with the statutory penalty-of-perjury jurat
      so the pro-se filer need not find a notary (routes to
      `tx-draft-declaration` for the exact jurat)

### Fee waiver

- [ ] Identifies the **Statement of Inability to Afford Payment of
      Court Costs** under **TRCP 145** as the mechanism to proceed
      without paying costs, and notes it replaces the old "affidavit of
      indigence"
- [ ] Reads the qualifying criteria / categories from the corpus
      (`../tx-law-references/references/civil-rules.md` / court-rules)
      rather than reciting income thresholds from memory
- [ ] Notes the Statement of Inability also substitutes for an appeal
      bond on a de-novo JP/county-court appeal where applicable

### Form

- [ ] Applies the `tx-statewide-format` caption, line numbering, and
      footer

## Common failure modes

- Adds a bar-number line to a pro-se signature block
- Calls the fee waiver an "in forma pauperis motion" or "affidavit of
  indigence" instead of the TRCP 145 Statement of Inability
- Hard-codes income-eligibility figures
