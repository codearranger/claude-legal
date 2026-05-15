---
name: oh-butler
description: >
  Use when drafting or filing in Butler County Court of Common Pleas (Hamilton, OH). Triggers include the court name, its case number format, and local-rule references. Layers on top of `oh-statewide-format`.
version: 0.2.0
---

# Butler County Court of Common Pleas (Hamilton, OH)

> **NOT LEGAL ADVICE.** Verify the assigned judge's chambers
> practice + the court's current Loc. R. before every filing.

## At a glance

- **Court**: Butler County Court of Common Pleas (Hamilton, OH)
- **Region**: Southwest Ohio / Cincinnati northern suburbs
- **Population**: 0.39M
- **Address**: Butler County Courthouse, 101 High St., Hamilton, OH 45011
- **Appellate district**: 12th Judicial District (Ohio Court of Appeals)
- **E-filing**: Butler County eFiling

## Distinctives

- Butler County is Ohio's eighth-largest county and includes Cincinnati's northern suburbs.
- **County seat is Hamilton, OH** — not to be confused with Hamilton County (Cincinnati). Verify the venue before filing.
- Loc. R. requires meet-and-confer before discovery motions.

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
