---
name: oh-stark
description: >
  Use when drafting or filing in Stark County Court of Common Pleas (Canton). Triggers include the court name, its case number format, and local-rule references. Layers on top of `oh-statewide-format`.
version: 0.2.0
---

# Stark County Court of Common Pleas (Canton)

> **NOT LEGAL ADVICE.** Verify the assigned judge's chambers
> practice + the court's current Loc. R. before every filing.

## At a glance

- **Court**: Stark County Court of Common Pleas (Canton)
- **Region**: Northeast Ohio / Canton metro
- **Population**: 0.37M
- **Address**: Stark County Common Pleas Court, 115 Central Plaza North, Canton, OH 44702
- **Appellate district**: 5th Judicial District (Ohio Court of Appeals)
- **E-filing**: Stark County eFiling

## Distinctives

- Stark County is Ohio's seventh-largest county.
- Mixed urban + rural civil docket; consumer-debt + L&T volume both significant.
- Loc. R. typically caps briefs at 20 pages.

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
