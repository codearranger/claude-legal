# mi-draft-motion — MCR 2.116(C)(10) motion for summary disposition in a debt case

## Prompt

I'm representing myself in Michigan. A debt buyer sued me in
Circuit Court on an old credit-card account for about $6,000.
In discovery they couldn't produce any assignment paperwork or
account statements — just a one-page "affidavit of debt." I
want to file a motion to get the case thrown out because there's
no admissible evidence they actually own this debt. How do I
draft it?

## Expected triggers

- `mi-draft-motion`
- `mi-statewide-format`
- `mi-consumer-debt`
- `mi-pro-se`

## Acceptance criteria

### Caption and title

- [ ] Caption follows the Michigan format per **MCR 1.109** and
      **MCR 2.113** (court, parties, case number, document title)
- [ ] Title identifies the motion as a **Motion for Summary
      Disposition under MCR 2.116(C)(10)** (no genuine issue of
      material fact)
- [ ] Distinguishes (C)(10) from (C)(8) (failure to state a
      claim on the pleadings alone) and explains why (C)(10) is
      the right subrule when the litigant relies on the
      evidentiary record / discovery gaps

### Standard

- [ ] States the (C)(10) standard: the court considers the
      pleadings, affidavits, depositions, admissions, and
      documentary evidence in the light most favorable to the
      non-moving party; summary disposition is proper when there
      is no genuine issue of material fact
- [ ] Notes the supporting/opposing-evidence requirement and
      the timing under **MCR 2.116** (cite the rule; read the
      current response/hearing timing from the references corpus
      rather than asserting day counts from memory)

### Substantive theory (mi-consumer-debt)

- [ ] Frames the standing / chain-of-title defect — the
      plaintiff must prove it owns the debt through an
      admissible assignment chain from the original creditor
- [ ] Notes that a bare "affidavit of debt" may not be
      admissible business-record evidence and does not by itself
      establish ownership; points to the RCPA / MCPA framework
      from `mi-statutes-debt/` rather than asserting elements
      from memory

### Composition

- [ ] References self-represented status without lawyer-speak
- [ ] Signature block per **MCR 1.109(E)** (self-represented;
      no P-number — see `mi-pro-se`)

## Common failure modes

- Defaults to FRCP 56 instead of MCR 2.116(C)(10)
- Confuses (C)(10) with (C)(8) or (C)(7)
- Asserts hard response/hearing day counts as fixed facts
  instead of reading current timing from the corpus
- Invents a P-number or attorney signature block for a pro-se
  filer
