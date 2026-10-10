# wa-draft-order — Proposed Order

## Prompt
Draft a Proposed Order Granting my Motion to Compel. I want the court
to order plaintiff to produce full responses within 14 days, award my
costs, and include escalation language for non-compliance.

## Expected triggers
- `wa-draft-order`
- `wa-law-references` (civil-rules.md — CR 37)

## Acceptance criteria
- Caption matches the motion
- Title: "[PROPOSED] ORDER GRANTING DEFENDANT'S MOTION TO COMPEL"
- **[PROPOSED]** bracket in title before entry
- Recitals: matter came before court on [date], reviewed [papers],
  heard argument (if any), and court finds good cause
- **Ordered** clauses — numbered, specific, enforceable:
  - Full amended responses within 14 days
  - Production of responsive documents
  - Specific deficiencies identified by request number
  - Costs / fees awarded under CRLJ 37(a)(4) (or preserved for later
    determination on a cost bill)
  - **Escalation language** — if plaintiff fails to comply, designated
    facts established under CRLJ 37(b)(2)(A), striking of pleadings,
    or dismissal
- Signature line for judge with date and printed name
- Presented by / approved as to form blocks

## Common failure modes
- Vague ordered clauses ("produce all requested documents")
- Missing deadline
- Missing escalation language
- No judge signature line / date
- Caption doesn't match motion
- Missing [PROPOSED] in title
