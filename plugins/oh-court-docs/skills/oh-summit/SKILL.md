---
name: oh-summit
description: >
  Use when drafting or filing in Summit County Court of Common Pleas (Akron). Triggers include the court name, its case number format, and local-rule references. Layers on top of `oh-statewide-format`.
version: 0.2.0
---

# Summit County Court of Common Pleas (Akron)

> **NOT LEGAL ADVICE.** Verify the assigned judge's chambers
> practice + the court's current Loc. R. before every filing.

## At a glance

- **Court**: Summit County Court of Common Pleas (Akron)
- **Region**: Northeast Ohio / Akron metro
- **Population**: 0.54M
- **Address**: Summit County Courthouse, 209 S High St., Akron, OH 44308
- **Appellate district**: 9th Judicial District (Ohio Court of Appeals)
- **E-filing**: Tyler Technologies eFiling

## Distinctives

- Summit is Ohio's fourth-largest county and the Akron metro civil-litigation hub.
- Loc. R. typically caps motion briefs at 20 pages.
- Magistrate practice common for pretrial civil matters under Civ. R. 53.

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
