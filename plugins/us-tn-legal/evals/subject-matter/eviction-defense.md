# tn-landlord-tenant — Defending a detainer warrant

## Prompt

My landlord filed a detainer warrant against me in General
Sessions Court in Tennessee for nonpayment of rent. I want to
fight it. What law applies, what notice was I supposed to get,
and what are my options if I lose?

## Expected triggers

- `tn-landlord-tenant`
- `tn-general-sessions`

## Acceptance criteria

### The threshold question (must come first)

- [ ] **Asks the county-population threshold question first**:
      whether the **URLTA (T.C.A. § 66-28-101 et seq.)** applies
      depends on county population — URLTA applies only in
      counties **over 75,000 population** under **T.C.A.
      § 66-28-102**; counties at/below the threshold are
      governed by the general L&T law at **T.C.A. § 66-7-101
      et seq.**
- [ ] Tells the tenant to confirm whether the venue county is a
      covered URLTA county (the covered-county list shifts with
      census data — verify, do not hard-code)

### Notice requirement (URLTA counties)

- [ ] States that in a URLTA county, a nonpayment notice under
      **T.C.A. § 66-28-505** terminates the tenancy not less
      than **14 days** after receipt if rent remains unpaid
- [ ] Notes the notice analysis differs under the general L&T
      framework (§ 66-7) for non-URLTA counties

### Forum and appeal

- [ ] Recognizes the detainer warrant (FED) is filed in
      **General Sessions** (T.C.A. § 29-18-101 et seq.) with
      **unlimited jurisdiction** in detainer matters
- [ ] States the **10-day de novo appeal to Circuit Court**
      (T.C.A. § 27-5-108) from the General Sessions judgment
- [ ] Notes possession-bond considerations on appeal (§
      29-18-130(b)) but flags that a tenant's appeal is not
      automatically dismissed for failure to post a possessory
      bond (verify current case law)

## Common failure modes

- Assumes URLTA applies without checking the county-population
  threshold
- Hard-codes a URLTA covered-county list as fixed
- States the wrong nonpayment notice period
- Misstates the appeal as a 30-day record appeal instead of a
  10-day de novo appeal
- Files the matter in Circuit Court rather than recognizing
  General Sessions as the FED forum
