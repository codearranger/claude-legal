---
name: or-landlord-tenant
description: >
  Subject-matter bundle for Oregon landlord-tenant disputes — residential
  evictions, unlawful detainer, FED (forcible entry and detainer), 72-hour
  nonpayment notices, just-cause termination, Portland relocation assistance,
  security deposits, habitability (ORS 90.320), retaliation (ORS 90.385),
  tenant-screening (ORS 90.295), and COVID-era debt provisions. Triggers
  include "Oregon eviction", "FED Oregon", "72-hour notice Oregon",
  "ORS 90 Oregon", "Residential Landlord and Tenant Act", "RLTA Oregon",
  "Portland relocation assistance", "security deposit Oregon",
  "habitability Oregon ORS 90.320", "retaliatory eviction Oregon".
  Composes with or-statewide-format, or-multcc / or-wccc / or-county-courts,
  or-pro-se, or-deadlines, and draft-* skills.
version: 0.1.0
---

# Oregon Landlord-Tenant — Subject-Matter Bundle

> **NOT LEGAL ADVICE.** Oregon's Residential Landlord and Tenant Act
> (RLTA, ORS Chapter 90) was significantly amended in 2019 (SB 608
> statewide just-cause eviction) and 2021-2023 (COVID-relief provisions
> mostly wound down). Portland and other jurisdictions have supplemental
> tenant-protection ordinances. Verify notice periods, termination
> grounds, and relocation-assistance amounts against current ORS and local
> code before relying. Contact Oregon Law Center or Community Alliance of
> Tenants for tenant assistance.

## At a glance

- **Primary statute**: ORS Chapter 90 (Residential Landlord and Tenant
  Act — RLTA); ORS Chapter 105 (property law context); ORS Chapter 88
  (landlord liens in limited circumstances)
- **Eviction procedure**: ORS 105.110 (forcible entry and detainer — FED);
  UTCR Supplement section 9 (FED-specific procedural rules)
- **Just-cause eviction**: SB 608 (2019) added ORS 90.427 requiring
  just-cause for termination during tenancy and at end of fixed term for
  residential tenancies (with exemptions for owner-occupied 4-plex or
  less, first year of tenancy in some cases)
- **Forum**: Circuit Court (FED cases proceed as summary proceedings;
  some counties have separate FED dockets)

## Notice requirements (verify all day counts against ORS 90)

Oregon's notice regime is layered and frequently amended:

| Notice type | Statute | Notes |
|---|---|---|
| Nonpayment — 72-hour notice | ORS 90.394 | Must include specific language; $150 max late fee cap; **must** offer payment-plan information per 2021 amendments |
| Nonpayment — 144-hour notice | ORS 90.394(4) | Alternative for tenants with prior nonpayment history (limited use) |
| Lease violation — 30-day notice | ORS 90.392 | Curable violation; cure period within the notice period |
| Lease violation — 10-day notice | ORS 90.392(3) | For second similar violation within 6 months |
| Termination (just-cause, tenant-conduct) | ORS 90.427(3)-(4) | Specific grounds enumerated; month-to-month tenancy varies |
| Owner-side termination | ORS 90.427(5)-(8) | Requires relocation assistance in most cases |
| No-cause (year 1 only, exempt properties) | ORS 90.427(1)-(2) | Very narrow; verify eligibility |

**Portland-specific**: Portland City Code Ch. 30.01.085 requires
additional relocation assistance (amount varies; based on bedroom count
and rent level) beyond state law requirements. Gresham, Bend, and other
cities have adopted similar ordinances.

## Just-cause eviction (ORS 90.427)

SB 608 (2019) created a statewide just-cause eviction requirement for
residential tenancies. Landlords may not terminate a tenancy without a
qualifying ground:

### Tenant-conduct grounds (no relocation assistance required)
- Nonpayment of rent
- Violation of rental agreement (with required notice + cure period)
- Repeat violations
- Material/substantial violation
- Illegal activity
- Waste or nuisance

### Owner-side grounds (relocation assistance required — 1 month's rent)
- Owner or owner's immediate family to occupy
- Substantial renovations (government-required)
- Demolition or change of use

**Relocation assistance**: for owner-side terminations, the landlord
must pay 1 month's rent as relocation assistance (ORS 90.427(7)(b)).
Portland requires additional amounts. Failure to pay forfeits the
ability to terminate for that ground.

**Exemptions from ORS 90.427**: owner-occupied 4-plex or less (if owner
occupies a unit); manufactured-dwelling communities governed separately.

## FED eviction procedure

Oregon evictions proceed as **forcible entry and detainer (FED)**
summary proceedings under ORS 105.110 and UTCR Supplement 9.

1. Serve proper written notice with all required statutory language
2. Wait for notice period to expire without cure or surrender
3. File **Complaint for Forcible Entry and Detainer** in Circuit Court
   for the county where the property is located
4. Pay filing fee (verify current fee at court website)
5. **Sheriff service** of summons + complaint on tenant (UTCR 9.010)
6. **Return date** — typically the first available FED calendar date
   (within ~7-14 days in most counties)
7. **FED hearing** — tenant may appear and raise defenses
8. If landlord prevails: **Judgment of Restitution** + writ of execution
   to restore possession

**Answer window**: tenant must appear at the return date; failure to
appear results in default judgment. Some courts have a standing calendar;
others require scheduling.

## Security deposits (ORS 90.300)

- No statutory maximum on the deposit amount
- Must be returned (with itemized statement of any deductions) within
  **31 days** after the tenancy ends and the landlord receives a
  forwarding address (ORS 90.300(9))
- Deductions must be for actual damages beyond normal wear and tear
- Failure to return timely: tenant entitled to **twice the amount
  wrongfully withheld** plus attorney's fees (ORS 90.300(16))

## Habitability (ORS 90.320)

Landlord must maintain premises in habitable condition throughout the
tenancy, including:
- Effective weatherproofing; watertight roof/walls
- Plumbing and heating facilities in working order
- Hot and cold running water
- Safe and sanitary premises
- Working smoke and CO detectors

**Repair-and-deduct** (ORS 90.365): if landlord fails to make essential
repairs after proper notice, tenant may arrange repairs and deduct the
cost from rent (up to the lesser of 1 month's rent or $300 per repair).

## Retaliation (ORS 90.385)

Landlord may not retaliate for tenant's complaint about habitability,
contact with a government agency, or tenant union activity by terminating
the tenancy, increasing rent, or decreasing services.

**Rebuttable presumption of retaliation** arises if adverse action is
taken within **90 days** after protected activity.

Remedies: recovery of possession, 3 months' rent or actual damages
(whichever is greater), and attorney's fees.

## Composition with other skills

- `or-statewide-format` — UTCR 2.010 formatting
- `or-multcc` / `or-wccc` / `or-county-courts` — venue specifics
- `or-deadlines` — notice day-count computation (ORCP 10 + ORS 90 notice rules)
- `or-first-30-days` — tenant's response to FED complaint
- `or-post-judgment` — writ of execution defense; habitability counterclaims
- `or-pro-se` — pro-se framework for tenants
