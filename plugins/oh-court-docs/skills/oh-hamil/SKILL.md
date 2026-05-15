---
name: oh-hamil
description: >
  Use when drafting or filing in Hamilton County Court of Common Pleas (Cincinnati). Triggers include the court name, its case number format, and local-rule references. Layers on top of `oh-statewide-format`.
version: 0.2.0
---

# Hamilton County Court of Common Pleas (Cincinnati)

> **NOT LEGAL ADVICE.** Verify the assigned judge's chambers
> practice + the court's current Loc. R. before every filing.

## At a glance

- **Court**: Hamilton County Court of Common Pleas (Cincinnati)
- **Region**: Southwest Ohio / Greater Cincinnati
- **Population**: 0.83M
- **Address**: Hamilton County Courthouse, 1000 Main St., Cincinnati, OH 45202
- **Appellate district**: 1st Judicial District (Ohio Court of Appeals)
- **E-filing**: courtclerk.org Court Connect

## Distinctives

- Hamilton County is the third-largest Ohio county and Greater Cincinnati's principal civil venue.
- Loc. R. 18 requires meet-and-confer before discovery motions.
- Online motion-hearing scheduling via the court's case-management system.
- Some judges decide motions on the briefs without oral argument.

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
