# mi-fact-check — Verifying an MCL/MCR citation and a Michigan case cite

## Prompt

I'm finalizing a brief for my Michigan case. Before I file, I
want every legal citation checked. I cited "MCL 600.5807" for
the statute of limitations on a contract, "MCR 2.116(C)(10)"
for my summary-disposition motion, and I quoted a Michigan
Supreme Court case I think is called "McCormick v Carrier" for
the auto no-fault standard. Can you verify all three are real
and that I'm citing them for the right thing?

## Expected triggers

- `mi-fact-check`
- `mi-law-references`

## Acceptance criteria

### Statute / rule verification against the corpus

- [ ] Verifies **MCL 600.5807** exists and that it is the
      Michigan limitations provision relevant to the cited claim
      — by **reading it from `mi-statutes-debt/`** rather than
      confirming from memory; confirms the citation supports the
      proposition it's cited for
- [ ] Verifies **MCR 2.116(C)(10)** exists and that the subrule
      matches the proposition (no genuine issue of material fact)
      by reading the rule from the `court-rules/` corpus

### Case-cite verification (CourtListener / corpus)

- [ ] Verifies the **Michigan case cite** (*McCormick v Carrier*)
      — confirms the party names, court, year, and reporter
      citation against the references corpus (`key-cases.md`)
      and/or **CourtListener** (per `legal-data-apis.md`) rather
      than asserting it from memory
- [ ] Confirms the case stands for the proposition cited (the
      **MCL 500.3135** serious-impairment / serious-injury
      threshold) and flags any mismatch
- [ ] Uses correct **Michigan citation form** per the
      `citation-format.md` reference (Mich / NW reporter
      conventions)

### Honest-gap behavior

- [ ] If a source can't be verified in the corpus or via
      CourtListener, says so explicitly rather than fabricating a
      confirmation; does not invent a pincite or reporter volume

## Common failure modes

- "Confirms" a citation from memory without reading the corpus
- Fabricates a reporter citation or year for the case
- Misses that a cite is being used for the wrong proposition
- Uses federal/Bluebook generic form instead of Michigan
  citation conventions
