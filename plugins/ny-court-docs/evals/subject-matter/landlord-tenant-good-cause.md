# ny-landlord-tenant — Good Cause Eviction (2024)

## Prompt

I'm a tenant. My landlord just gave me a 90-day notice not
to renew my lease. The unit is in Buffalo. Does the new
Good Cause Eviction law protect me?

## Expected triggers

- `ny-landlord-tenant`
- `ny-county-courts`

## Acceptance criteria

- [ ] Identifies the **Good Cause Eviction Law (2024 NY
      Laws Ch 56, Part HH)** as the controlling regime in
      opt-in localities
- [ ] Notes that the **statewide statute applies by
      default in NYC**; outside NYC the law is **opt-in by
      municipality**
- [ ] Identifies **Buffalo** specifically: the City of
      Buffalo has opted in (verify current status with
      Buffalo's municipal code)
- [ ] Catalogs **what counts as good cause**:
      - non-payment after notice (with cure right)
      - violation of lease obligations
      - landlord recovering for personal/family use
      - removing unit from rental market
      - tenant nuisance
- [ ] Notes the **rent-cap exception**: tenants in units with
      monthly rent > 245% of fair market rent (2024 ceiling)
      are excluded from Good Cause protection
- [ ] Identifies the **unreasonable rent-increase** ceiling
      under the law (10% or 5% + CPI, whichever is lower)
- [ ] References the relevant **City Court** as the forum
      (Buffalo City Court for Buffalo)

## Common failure modes

- Treats Good Cause as a federal statute or a NYC-only law
- Forgets the opt-in mechanics outside NYC
- Suggests Supreme Court rather than City Court for a
  Buffalo eviction
