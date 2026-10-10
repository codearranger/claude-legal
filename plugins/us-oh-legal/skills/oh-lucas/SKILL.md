---
name: oh-lucas
description: >
  Use when drafting or filing in Lucas County Court of Common Pleas (Toledo). Triggers include the court name, its case number format, and local-rule references. Layers on top of `oh-statewide-format`.
version: 0.2.0
---

# Lucas County Court of Common Pleas (Toledo)

> **NOT LEGAL ADVICE.** Verify the assigned judge's chambers
> practice + the court's current Loc. R. before every filing.

## At a glance

- **Court**: Lucas County Court of Common Pleas (Toledo)
- **Region**: Northwest Ohio / Toledo metro
- **Population**: 0.43M
- **Address**: Lucas County Common Pleas Court, 700 Adams St., Toledo, OH 43604
- **Appellate district**: 6th Judicial District (Ohio Court of Appeals)
- **E-filing**: Lucas County eFiling

## Distinctives

- Lucas County is Ohio's sixth-largest county and the Toledo metro civil hub.
- Significant municipal-court overflow due to Toledo's $15k cap.
- Magistrates hear most pretrial civil matters.

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
