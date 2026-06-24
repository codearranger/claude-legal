# tx-draft-order — proposed order (judge-only signature block)

## Prompt

Draft a proposed order granting my motion to compel in my Texas
district court case.

## Expected triggers

- `tx-draft-order`

## Acceptance criteria

### Right structure

- [ ] Produces a **separate proposed order** captioned in the same case
      — not merged into the motion
- [ ] Uses decretal language ("IT IS ORDERED that ...") that disposes
      of the specific relief requested (granting the motion to compel
      and specifying the discovery to be produced and a deadline)
- [ ] Leaves a blank for the **date signed** and a **judge-only
      signature block** ("JUDGE PRESIDING") — does NOT place the
      movant's or any party's signature on the order

### Form

- [ ] Applies the `tx-statewide-format` caption and the `Page X of Y`
      footer
- [ ] Does not attach a certificate of service to the order itself (the
      order is the court's act), though the underlying motion has one

## Common failure modes

- Adds a party/attorney signature line to the order
- Writes argument into the order instead of clean decretal language
- Merges the order into the motion as a single document
