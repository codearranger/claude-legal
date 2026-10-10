# mi-landlord-tenant — 7-day demand for possession / MCR 4.201 summary proceeding + security-deposit counterclaim

## Prompt

My Michigan landlord taped a notice to my door saying I have 7
days to pay rent or get out, and now there's a court date. I'm
behind on rent but the place has had a broken furnace for two
months and the landlord still has my $1,500 security deposit
from a prior unit. What is this court process and can I fight
back?

## Expected triggers

- `mi-landlord-tenant`
- `mi-district-courts`

## Acceptance criteria

### The demand for possession

- [ ] Identifies the document as a **demand for possession /
      notice to quit** for nonpayment of rent and that Michigan
      uses a **7-day demand for nonpayment of rent** — cite the
      controlling statute (the **MCL 600.5714** summary-
      proceedings grounds and the demand-for-possession
      provisions) and **read the current notice period and form
      requirements from `mi-statutes-debt/` (Michigan
      landlord-tenant corpus)** rather than asserting them from
      memory
- [ ] Notes that the form/content of the demand is regulated and
      that defects in the demand can be a defense

### Summary proceedings forum (MCR 4.201)

- [ ] Identifies the **summary proceedings to recover possession
      of premises** as governed by **MCR 4.201** in the
      **District Court** (cross-reference `mi-district-courts`),
      and that the process is expedited with short timelines —
      read current timing from the corpus
- [ ] Notes the appearance/answer mechanics and that summary
      proceedings under MCR 4.201 differ from ordinary civil
      timelines

### Habitability + security-deposit counterclaim

- [ ] Raises the **warranty of habitability / repair-and-
      deduct** angle and the landlord's statutory repair
      obligations (cite the controlling MCL provision; read from
      the corpus)
- [ ] Identifies the **Michigan security-deposit statute** and
      the landlord's notice/return obligations — cite the
      governing MCL provision and **read the deadlines and
      potential damages (e.g., the double-amount remedy for
      noncompliance) from the corpus** rather than asserting the
      figures from memory — and frames the deposit dispute as a
      **counterclaim** within the summary proceeding where
      permitted

## Common failure modes

- Treats the 7-day demand like an ordinary civil complaint with
  a long answer period
- Asserts notice periods, deposit deadlines, or the deposit
  damages multiplier from memory instead of the corpus
- Misses MCR 4.201 as the controlling procedural rule
- Overlooks the habitability defense and the deposit counterclaim
