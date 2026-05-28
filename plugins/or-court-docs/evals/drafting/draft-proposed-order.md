# or-draft-order — Proposed Order

## Prompt

Draft a proposed order granting my motion to compel in Oregon
Multnomah case 25CV01234. Order should require production
within 14 days, overrule plaintiff's objections, and award
fees.

## Expected triggers

- `or-draft-order`
- `or-statewide-format`
- `or-multcc`

## Acceptance criteria

### Title

- [ ] "[PROPOSED] ORDER GRANTING DEFENDANT'S MOTION TO
      COMPEL UNDER ORCP 46 A"
- [ ] `[PROPOSED]` bracket present

### Preamble

- [ ] "This matter came before the Court on..."
- [ ] Identifies the underlying motion
- [ ] Lists what the Court considered

### Findings

- [ ] Numbered findings supporting the ruling
- [ ] References ORCP 46 A, ORCP 36 B(1), Multnomah SLR
      5.045
- [ ] States the meet-and-confer was unsuccessful

### Order section

- [ ] "IT IS HEREBY ORDERED" phrase present
- [ ] Numbered relief paragraphs (A, B, C, D)
- [ ] Specific deadline ("14 calendar days of date of this
      Order, or by ____________, whichever is sooner")
- [ ] Overrules objections
- [ ] Awards fees with ORCP 46 A(4)(a) and ORCP 68 C(2)
      mechanism

### Signatures

- [ ] Judge signature line ("CIRCUIT COURT JUDGE")
- [ ] Submitting party block (pro se: no OSB#)
- [ ] Notice of Presentation or Approval as to Form block

### UTCR 5.100 compliance

- [ ] References UTCR 5.100 service requirement
- [ ] Notice of Presentation explains tracking of motion

## Common failure modes

- Forgetting `[PROPOSED]` bracket
- Missing "IT IS HEREBY ORDERED" phrase
- Open-ended deadlines ("promptly")
- Wrong fee mechanism (citing CR 37 instead of ORCP 46)
- Missing UTCR 5.100 Notice of Presentation
- Including OSB# for pro se filer
