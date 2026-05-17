# wa-landlord-tenant — Just-cause eviction

## Prompt

My Washington landlord just told me they're "ending the lease"
at the end of next month with no specific reason. I'm a tenant
in a 4-unit apartment building. Can they do that?

## Expected triggers

- `wa-landlord-tenant`

## Acceptance criteria

- [ ] Identifies the **2021 SB 5160 just-cause-eviction
      reform** at RCW 59.18.650 — purely no-cause
      terminations of periodic tenancies (and most fixed-
      term lease non-renewals) are no longer permitted
- [ ] Walks the **category framework** of just-cause grounds:
      tenant-conduct grounds (nonpayment, lease violation,
      waste / nuisance / criminal); owner-side grounds
      (owner move-in, sale to occupier buyer, substantial
      rehabilitation, change of use); narrow-circumstance
      grounds
- [ ] **Reads current notice periods from
      `wa-law-references/references/wa-rcw-debt/RCW-59_18.md`**
      (especially the .650 section group) — does NOT
      enumerate specific day counts
- [ ] References coverage carve-outs (shared housing with
      landlord; some small-landlord single-family rentals;
      seasonal / transitional housing) and notes that a
      4-unit apartment building does NOT trigger the small-
      landlord exemption
- [ ] References **HB 1815 statewide tenant Right to
      Counsel** for low-income tenants
- [ ] Suggests next steps: demand statement of cause; check
      that the notice form is statutorily compliant; consider
      whether the notice qualifies under any enumerated
      ground; if not, the notice is defective

## Common failure modes

- Treating purely no-cause termination as valid (it is not
  post-2021)
- Hard-coding specific notice periods (read from chapter
  file)
- Treating relocation-assistance / first-right-of-refusal
  protections as universal rather than ground-specific
- Confusing the small-landlord exemption with the larger
  carve-out framework
