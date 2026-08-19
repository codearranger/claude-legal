---
name: or-employment
description: >
  Subject-matter bundle for Oregon employment-law matters — discrimination
  (Oregon BOLI / ORS 659A), wage-and-hour (Oregon Minimum Wage, BOLI
  enforcement), paid sick leave (ORS 653.606-653.661), Oregon Family Leave
  Act (OFLA, ORS 659A.150-659A.186), non-competes (ORS 653.295 void unless
  narrow requirements met), whistleblower (ORS 659A.199, 659A.203, 659A.230),
  workers' compensation (ORS 656 exclusive remedy + discrimination), PECBA
  (public-employee collective bargaining, ORS 243.650), and wrongful
  discharge in violation of public policy. Triggers include "Oregon
  employment discrimination", "ORS 659A", "BOLI complaint Oregon",
  "Oregon wage claim", "Oregon sick leave", "OFLA", "Oregon Family Leave
  Act", "non-compete Oregon ORS 653.295", "Oregon whistleblower",
  "workers comp discrimination Oregon". Composes with or-statewide-format,
  or-county-courts / or-multcc / or-wccc, or-pro-se, or-deadlines.
version: 0.1.0
---

# Oregon Employment Law — Subject-Matter Bundle

> **NOT LEGAL ADVICE.** Oregon employment law is enforced by the
> Bureau of Labor and Industries (BOLI) as the primary state agency.
> Filing deadlines for BOLI charges are short and strictly enforced.
> The minimum wage and OFLA leave thresholds change periodically.
> Verify every deadline, dollar amount, and procedural step against
> current ORS, OAR, and BOLI guidance before relying. Consult a
> licensed Oregon employment attorney before a deadline runs.

## At a glance

- **Anti-discrimination**: ORS Chapter 659A (Oregon Civil Rights Act)
  — enforcement through BOLI + private civil action
- **Wage/hour**: ORS Chapter 652 (payment of wages) + ORS Chapter 653
  (minimum wage, overtime, sick leave)
- **Family leave**: OFLA (ORS 659A.150-659A.186) + interaction with
  federal FMLA (29 U.S.C. § 2601)
- **Non-competes**: ORS 653.295 — very narrow enforceability; most
  are void
- **Workers' comp**: ORS Chapter 656 — exclusive remedy with
  narrow intentional-injury and discrimination exceptions

## Oregon Civil Rights Act (ORS 659A)

### Protected classes and enforcement

ORS 659A prohibits discrimination in employment based on:
race, color, religion, sex, sexual orientation, national origin, marital
status, age (18+), disability (including pregnancy-related conditions),
veteran status, and use of protected leave.

Oregon's anti-discrimination coverage is **broader than federal law**:
smaller employers covered; marital status and sexual orientation
explicitly included; broader disability definition.

### BOLI administrative exhaustion

Before filing a civil action, a claimant must file a **BOLI charge
within 1 year** of the alleged unlawful employment practice
(ORS 659A.820). BOLI investigates and issues either a right-to-sue
notice or proceeds to a hearing.

**BOLI right-to-sue**: after 90 days from BOLI filing, claimant may
request a notice of right to sue (ORS 659A.820(3)). Civil suit must
be filed within **90 days** of the right-to-sue notice (ORS 659A.885).

**Concurrent EEOC filing**: BOLI and EEOC have a worksharing agreement;
a charge filed with one is cross-filed with the other. Federal Title VII
SOL is 300 days in Oregon (a "deferral state").

### Damages

Oregon has no statutory damages cap for employment-discrimination
claims (unlike the federal Title VII $300k cap for large employers).
Available: back pay, front pay, emotional distress (non-economic),
punitive damages (for malicious conduct), attorney's fees to prevailing
plaintiff.

## Wage-and-hour

### Minimum wage (ORS 653.025)

Oregon has a **tiered minimum wage** system:
- **Portland metro** area: highest tier
- **Non-urban** (Rural) Oregon: lower tier  
- **Standard** (all other areas): middle tier

Minimum wage adjusts annually (July 1) tied to CPI. Current rates:
**verify against BOLI's current minimum-wage chart at oregon.gov/boli**.

### Overtime (ORS 653.261)

Oregon follows federal FLSA: time-and-a-half for hours over 40 in
a workweek. Exempt employees (executive, administrative, professional)
must meet the **federal salary basis test** (Oregon has not set a
higher state exemption threshold — verify current status).

### Wage payment (ORS 652.140, 652.150)

- Final wages due to **terminated** employees: next scheduled payday
  or **5 days** after termination, whichever comes first (ORS 652.140)
- Final wages due to **quitting** employees: on the **next scheduled
  payday** (ORS 652.140(2))
- **Penalty wages** for willful failure to pay: up to 30 days'
  additional wages (ORS 652.150)
- Wage-claim SOL: **6 years** (ORS 12.080(1) contract SOL applies)

### Paid sick leave (ORS 653.606-653.661)

Oregon requires employers with **10+ employees** (6+ in Portland) to
provide **paid** sick leave; smaller employers must provide **unpaid**
sick leave. Employees accrue at **1 hour per 30 hours worked** up to
**40 hours/year**.

## Oregon Family Leave Act (OFLA) — ORS 659A.150-659A.186

OFLA provides leave rights independent of (and in addition to) FMLA:
- Applies to employers of **25+ employees** (lower than FMLA's 50+)
- Protections include: pregnancy disability leave, parental leave,
  serious-health-condition leave, sick-child leave, bereavement leave,
  military-family leave
- The overlap and interaction with FMLA is complex — leaves may or
  may not run concurrently depending on type

**Important (2023 update)**: Oregon's **Paid Leave Oregon** program
(ORS 657B, SB 1049 / Measure 112) provides a paid leave insurance
program funded by employer/employee contributions. Paid Leave Oregon
and OFLA interact but are separate programs.

## Non-competes (ORS 653.295)

Oregon non-competes are **void** unless they meet all of these
requirements at execution:
- Signed at start of employment (not mid-employment without additional
  consideration) or signed at bona fide advancement
- Must be accompanied by a signed, written bona-fide advancement offer
  OR the employer must provide the agreement to the employee **2 weeks
  before** the first day of work
- Employee must be **exempt** from overtime (professional/executive/
  administrative exemption under FLSA)
- Employee must be **paid** at least the median Oregon wages for their
  occupation (BOLI publishes the threshold)
- Duration limited to **12 months** after termination
- Employer must have a **protectable interest** (trade secrets,
  confidential information, substantial investment in training)

Non-competes that fail any element are **void and unenforceable**
as a matter of law (ORS 653.295(1)).

## Whistleblower protection (ORS 659A.199, 659A.203, 659A.230)

Oregon provides broad whistleblower protections:
- **ORS 659A.199**: private-sector employee reporting criminal activity
  or law violations in good faith
- **ORS 659A.203**: public employee whistleblower
- **ORS 659A.230**: employee refusing to participate in unlawful activity

Retaliation is prohibited. Remedy: reinstatement, back pay, damages,
attorney's fees. File BOLI charge (for administrative exhaustion) or
proceed directly to circuit court (for some statutory claims).

## Composition

- `or-statewide-format` — UTCR 2.010 formatting
- `or-deadlines` — BOLI charge deadlines (1-year); right-to-sue
  window (90 days); FMLA/OFLA notice periods
- `or-discovery` — employment records, personnel files (ORCP 39 + 44)
- `or-multcc` / `or-wccc` / `or-county-courts` — venue
