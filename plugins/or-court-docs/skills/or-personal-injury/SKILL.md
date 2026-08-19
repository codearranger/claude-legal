---
name: or-personal-injury
description: >
  Subject-matter bundle for Oregon personal-injury litigation — negligence
  (modified comparative fault, ORS 31.600), wrongful death (ORS 30.020),
  product liability (ORS 30.900-30.920), medical malpractice (ORS 12.110(4),
  ORS 677 prelitigation panel), government tort claims (Oregon Tort Claims
  Act, ORS 30.260-30.300), motor vehicle accidents, premises liability
  (Oregon premises categories), and economic-loss doctrine. Triggers include
  "Oregon personal injury", "Oregon negligence", "ORS 31.600 comparative
  fault", "Oregon wrongful death ORS 30.020", "Oregon product liability",
  "Oregon medical malpractice", "Oregon Tort Claims Act", "ORS 30.260",
  "premises liability Oregon", "OTCA notice". Composes with
  or-statewide-format, or-county-courts / or-multcc / or-wccc, or-pro-se,
  or-discovery, or-deadlines, and draft-* skills.
version: 0.1.0
---

# Oregon Personal Injury — Subject-Matter Bundle

> **NOT LEGAL ADVICE.** Oregon's comparative-fault statute and damages
> rules turn on facts and evolving case law; SOLs for different torts
> differ; the medical-malpractice prelitigation panel adds a threshold
> step. Verify every deadline and procedural requirement against current
> ORS and case law before filing. Personal-injury cases often involve
> fee arrangements and complex damages; consult a licensed Oregon
> personal-injury attorney.

## At a glance

- **Comparative fault**: Oregon uses **modified comparative fault** —
  plaintiff recovers only if plaintiff's fault is **less than** that of
  the combined fault of the defendants (ORS 31.600(1)). Plaintiff at
  50% or more fault recovers nothing.
- **Primary SOL**: **2 years** for most tort claims (ORS 12.110(1));
  **3 years** for product liability claims; **2 years** for medical
  malpractice with a **5-year statute of ultimate repose** (ORS 12.110(4))
- **Wrongful death**: **3 years** from date of death, max **3 years**
  from injury (ORS 30.020(1))
- **OTCA notice** is a prerequisite for suits against Oregon
  government entities (ORS 30.275); strict notice deadlines apply

## Negligence doctrine — ORS 31.600 framework

### Modified comparative fault (51% bar)

Under ORS 31.600-31.620:
- Trier of fact allocates fault percentages among all at-fault parties
  (including plaintiff, defendants, and any non-party fault designated
  under ORS 31.600(2))
- Plaintiff recovers if plaintiff's fault is **less than** the combined
  fault of all defendants
- Plaintiff's recovery is reduced proportionally by plaintiff's
  percentage of fault
- **Economic damages**: each defendant pays their share of economic
  damages (several liability)
- **Non-economic damages**: each defendant pays their share (several
  liability) except for defendants ≥ 15% at fault who are jointly
  liable for non-economic damages when the plaintiff is not at fault
  (ORS 31.610 — verify the current section for the carve-outs)

### Premises liability

Oregon courts have retained the **invitee / licensee / trespasser**
categories for landowner liability, though the distinctions are somewhat
blurred by the Restatement (Second) approach. Invitees (business
visitors, public invitees) receive the highest duty. Child-trespasser
"attractive nuisance" doctrine under Oregon common law.

## Wrongful death (ORS 30.020-30.100)

Oregon's wrongful-death statute creates a statutory action that did not
exist at common law. Key points:
- Action belongs to the **personal representative** of the decedent's
  estate (not the survivors directly)
- Recoverable damages: economic loss to survivors, non-economic losses
  of survivors (loss of society, companionship, services), and the
  decedent's own pre-death pain and suffering (if any)
- **3-year SOL** from date of death, but **no later than 3 years from
  injury** (ORS 30.020(1)) — the shorter deadline controls
- Notice requirements for OTCA claims apply if the defendant is a
  government entity

## Medical malpractice — prelitigation panel (ORS 677.053-677.097)

Before a medical malpractice complaint may be filed, Oregon requires
submission of the claim to a **prelitigation screening panel** (ORS
677.053-677.097). The panel is an informal, confidential proceeding.

### Panel procedure
1. **Request for review** filed with the Oregon Health Authority
2. Panel convened (physician + non-physician members)
3. Panel issues a written opinion (not binding, not admissible)
4. If panel opinion adverse, the plaintiff may still file suit

**Time impact**: the running of the SOL is **tolled** while the panel
is pending (ORS 677.067). Critical: start the prelitigation process
early — if the SOL runs before the panel concludes, the toll may not
save the claim.

## Oregon Tort Claims Act (OTCA) — ORS 30.260-30.300

Suits against Oregon government entities (state, county, city,
school district) require **notice under ORS 30.275** as a
prerequisite to filing.

| Entity | Notice deadline (from loss/injury) |
|---|---|
| State of Oregon | **180 days** (ORS 30.275(2)(b)) |
| Local government (county, city, etc.) | **180 days** (ORS 30.275(2)(b)) |
| Notice to public body | Required form elements: claimant's name/address, description of circumstances, date/place/circumstances of injury, description of injury/loss, amount claimed |

**Strict compliance** required — courts have rejected claims for
late or incomplete OTCA notices. Failure to file timely notice is
a complete defense (ORS 30.275(1)).

**Damage caps** apply under ORS 30.271 (state) and 30.272 (local
government). Verify current cap amounts against the statute (they
may be adjusted by the legislature).

## Product liability (ORS 30.900-30.920)

Oregon has codified product liability at ORS Chapter 30:
- **Strict liability** for manufacturing defects; **negligence or
  strict liability** for design defects and warning defects
- **3-year SOL** from date of discovery (ORS 30.905(1)) — longer
  than the general 2-year tort SOL
- **10-year statute of ultimate repose** from the date the product
  was first sold (ORS 30.905(2)) — verify the current version

## Composition with other skills

- `or-statewide-format` — UTCR 2.010 formatting
- `or-discovery` — personal-injury discovery (subpoenas for medical
  records, employment records; ORCP 44 physical/mental examinations)
- `or-deadlines` — SOL tracking + OTCA notice deadlines
- `or-first-30-days` — defendant's initial response
- `or-fact-check` — verify all case citations and SOL calculations
- `or-multcc` / `or-wccc` / `or-county-courts` — venue (personal-injury
  cases filed where injury occurred or defendant resides)
