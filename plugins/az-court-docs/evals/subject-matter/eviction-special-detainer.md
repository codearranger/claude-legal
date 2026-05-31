# az-landlord-tenant — Special detainer eviction + 5-day notice in Justice Court

## Prompt

My landlord in Arizona says I'm behind on rent and is threatening
to evict me. He handed me a notice yesterday. How does eviction
actually work in Arizona, how much time does the notice give me,
and which court does this happen in?

## Expected triggers

- `az-landlord-tenant`
- `az-justice-courts`

## Acceptance criteria

### Special detainer framework

- [ ] Identifies the eviction action as a **special detainer** under
      the **Arizona Residential Landlord and Tenant Act (A.R.S. Title
      33, Chapter 10)** and frames the action at **A.R.S. § 33-1377**
      — reads the current procedure (expedited timeline, when the
      action may be filed) from `az-statutes-debt/` rather than
      asserting it
- [ ] States that for **nonpayment of rent** the landlord must serve a
      written notice giving the tenant time to pay or vacate — cite
      the governing notice statute (**A.R.S. § 33-1368**) and read the
      **notice period (the 5-day notice)** and cure rights from the
      corpus rather than asserting the day count

### Forum and timeline (Justice Court)

- [ ] Identifies the **Justice Court** as the usual forum for a
      residential special detainer and notes it proceeds under the
      **Justice Court Rules of Civil Procedure / the Rules of
      Procedure for Eviction Actions (RPEA)**, NOT the ARCP
      (cross-reference `az-justice-courts`)
- [ ] Notes the **expedited** nature of eviction proceedings (short
      time from filing to hearing) and reads the current timing from
      the corpus

### Tenant defenses

- [ ] Notes defenses/issues to raise (improper notice, payment/
      tender, habitability/repair-and-deduct, retaliation) — reads
      the governing A.R.S. provisions from the corpus rather than
      asserting them

## Common failure modes

- Asserts the notice period (5-day) or hearing timeline as a fixed
  number without reading it from the corpus
- Routes the eviction to Superior Court / ARCP instead of Justice
  Court under the RPEA
- Asserts the RLTA section numbers or tenant defenses from memory
