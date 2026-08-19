---
name: pa-landlord-tenant
description: >
  Subject-matter bundle for Pennsylvania landlord-tenant law — Landlord Tenant Act of 1951 (68 Pa. C.S. § 250.101 et seq.), landlord's right to recover possession (unlawful detainer via the Act), security deposits (§ 250.511a — 1 or 2 month cap depending on tenancy length; double-damages remedy), habitability (implied warranty), retaliatory eviction, and MDJ eviction procedure. Triggers: 'Pennsylvania landlord tenant', 'Pennsylvania eviction MDJ', 'Pennsylvania security deposit § 250.511a', 'Landlord Tenant Act Pennsylvania', 'Pennsylvania habitability'.
version: 0.1.0
---

# Pennsylvania Landlord-Tenant — Subject-Matter Bundle

> **NOT LEGAL ADVICE.** Pennsylvania's landlord-tenant law is
> governed primarily by the Landlord Tenant Act of 1951 (LTA).
> Notice requirements must be strictly followed. Evictions
> proceed before the MDJ as the primary forum.

## At a glance

- **Primary statute**: Landlord Tenant Act of 1951 (68 Pa. C.S.
  § 250.101 et seq.)
- **Forum**: MDJ (Magisterial District Judge) for possession;
  CCP for significant damages
- **Security deposits**: § 250.511a — capped; significant
  double-damages remedy for wrongful retention

## Notice requirements (§ 250.501)

| Situation | Notice required |
|---|---|
| Month-to-month tenancy | 15-day notice to quit |
| Year-to-year tenancy | 30-day notice to quit |
| Nonpayment of rent (any term) | 10-day notice to quit |

These are **minimum** periods; the lease may specify longer
periods.

**Notice requirements strictly construed**: defective notices
(wrong period, wrong address, wrong content) defeat the
eviction action. Pennsylvania courts are strict.

## MDJ eviction procedure

1. Serve proper written notice to quit
2. Wait for notice period to expire
3. File a **Complaint for Possession** with the local MDJ
4. MDJ schedules a hearing (typically 7-15 days)
5. If MDJ grants judgment: tenant has **10 days** to vacate
   (§ 250.501(c))
6. If tenant does not vacate: **Order for Possession**
   (writ) → constable executes
7. Tenant may appeal within 30 days → CCP de novo
   (with mandatory supersedeas bond — current rent must
   be paid into court to stay the writ)

## Security deposits (§ 250.511a-250.512)

- **Cap**: 2 months' rent during first year of tenancy;
  1 month's rent thereafter
- **Return deadline**: within **30 days** after termination
  of tenancy (§ 250.512(a))
- **Itemized statement** required with any deductions
  (§ 250.512(a)(1))
- **Failure to comply**: landlord forfeits right to retain
  deposit + liable for **double damages** (§ 250.512(c))

## Composition

- `pa-statewide-format` — Pa. R.C.P. format
- `pa-mdj` — primary eviction venue
- `pa-deadlines` — 10-day vacate period; 30-day deposit
  return; 30-day MDJ appeal window

