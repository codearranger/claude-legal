---
name: oh-cuya
description: >
  Use when drafting or filing in Cuyahoga County Court of Common Pleas (Cleveland). Triggers include the court name, its case number format, and local-rule references. Layers on top of `oh-statewide-format`.
version: 0.2.0
---

# Cuyahoga County Court of Common Pleas (Cleveland)

> **NOT LEGAL ADVICE.** Verify the assigned judge's chambers
> practice + the court's current Loc. R. before every filing.

## At a glance

- **Court**: Cuyahoga County Court of Common Pleas (Cleveland)
- **Region**: Lake Erie / Northeast Ohio
- **Population**: 1.26M
- **Address**: Justice Center Complex, 1200 Ontario St., Cleveland, OH 44113
- **Appellate district**: 8th Judicial District (Ohio Court of Appeals)
- **E-filing**: cpdocket.cp.cuyahogacounty.us

## Distinctives

- Cuyahoga is Ohio's largest county by population and the highest civil-filing volume in the state.
- Heavy consumer-debt docket — many cases route to Cleveland Municipal Court (~$15k cap) before reaching Common Pleas.
- Loc. R. 21.4 explicitly requires meet-and-confer before a motion to compel.
- Several judges require working paper copies for briefs over 15 pages.

## Filing flow

1. **Caption** per Civ. R. 10(A) — see `oh-statewide-format`
2. **E-file** via the court's portal (per-court system —
   not a statewide platform)
3. **Working copies** if required by chambers practice
4. **Certificate of service** on every party
5. **Notice of Hearing** if the motion requires a hearing
   date (see `oh-schedule-hearing`)

## Composition with other oh- skills

- `oh-statewide-format` — Civ. R. 10 caption + signature
- `oh-discovery` — Civ. R. 33/34/36 practice
- `oh-first-30-days` — 28-day Civ. R. 12(A)(1) answer
- `oh-draft-motion` / `-declaration` / `-note` / `-order` —
  scaffolders adapted to this court's local rules
- `oh-pro-se` — pro-se conventions
- `oh-file-packet` — court-specific e-filing portal
- `oh-consumer-debt` — debt-buyer defense framework
