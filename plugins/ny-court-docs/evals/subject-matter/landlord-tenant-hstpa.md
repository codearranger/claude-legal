# ny-landlord-tenant — HSTPA 2019 rent-demand + notice regime

## Prompt

I'm a tenant in Brooklyn. My landlord just served me with a
notice saying I owe two months of rent and have 3 days to pay
or vacate. Is that valid?

## Expected triggers

- `ny-landlord-tenant`
- `ny-kings`

## Acceptance criteria

- [ ] Identifies the case venue as **NYC Housing Court (Kings
      County)**
- [ ] Notes that the **2019 Housing Stability and Tenant
      Protection Act (HSTPA)** rewrote RPAPL § 711(2): the
      pre-2019 **3-day rent demand** was extended to a
      **14-day rent demand** as a precondition to nonpayment
      summary proceedings
- [ ] Concludes the notice as described is **NOT valid** —
      3 days violates RPAPL § 711(2) post-HSTPA
- [ ] References **Real Property Law § 232-a / § 232-b**
      for the holdover-notice tenancy-length scale:
      - <1 year tenancy: 30 days
      - 1-2 years: 60 days
      - 2+ years: 90 days
- [ ] Notes the **rent-demand cure** procedure — tenant
      pays during the 14-day window, proceeding cannot be
      commenced
- [ ] References the NYC **Right to Counsel** program
      (Local Law 136) for low-income tenants in eviction
- [ ] Recommends specific defenses: failure to serve proper
      rent demand; failure to specify amount due; serving
      the wrong tenant

## Common failure modes

- Cites the pre-2019 3-day rent demand without HSTPA
- Treats the holdover notice timeline as a flat 30 days
  regardless of tenancy length
- Misses Right to Counsel for the tenant
