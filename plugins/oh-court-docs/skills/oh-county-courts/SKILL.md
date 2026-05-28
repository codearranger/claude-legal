---
name: oh-county-courts
description: >
  Use when filing in an Ohio Court of Common Pleas other than the 8 flagship counties (Cuyahoga, Franklin, Hamilton, Summit, Montgomery, Lucas, Stark, Butler). Triggers include any other Ohio county's Common Pleas name (Mahoning / Youngstown, Warren, Lake, Lorain, Trumbull, Clark, Greene, etc.). Layers on top of `oh-statewide-format` with the common-denominator Loc. R. patterns across Ohio's 88 county Courts of Common Pleas.
version: 0.2.0
---

# Ohio County Common Pleas (Long-tail Roll-up)

> **NOT LEGAL ADVICE.** Each Ohio county Court of Common
> Pleas publishes its own Loc. R. The 80 non-flagship
> counties vary significantly. Always verify per-court
> rules before filing.

## What this covers

This skill covers Common Pleas courts in the **80 Ohio
counties not separately covered by dedicated flagship
skills** (the 8 flagships are `oh-cuya`, `oh-frank`,
`oh-hamil`, `oh-summit`, `oh-montgomery`, `oh-lucas`,
`oh-stark`, `oh-butler`).

## Court of Common Pleas overview

Ohio has **88 county Courts of Common Pleas** — one per
county under the Ohio Constitution. Each is a court of
general jurisdiction:

- **General Division** — civil + criminal
- **Domestic Relations Division** — divorce, custody,
  support (see `oh-family-court`)
- **Juvenile Division** — juvenile cases + unmarried-
  parent custody (see `oh-family-court`)
- **Probate Division** — wills, estates, adoption

Smaller counties may combine divisions; larger counties
operate them as separate courts within Common Pleas.

## Higher-volume non-flagship counties

| County | Seat | Approx. pop. | Notable |
|---|---|---|---|
| Mahoning | Youngstown | 0.23M | Steelbelt; significant L&T volume |
| Warren | Lebanon | 0.24M | Cincinnati's northern exurbs |
| Lake | Painesville | 0.23M | Cleveland's eastern suburbs |
| Lorain | Elyria | 0.31M | Cleveland's western suburbs |
| Trumbull | Warren | 0.20M | Northeast / steel-belt |
| Clark | Springfield | 0.13M | Central / industrial |
| Greene | Xenia | 0.17M | Dayton's eastern suburbs |
| Wood | Bowling Green | 0.13M | Toledo's southern suburbs |
| Portage | Ravenna | 0.16M | Kent State; Cleveland exurbs |
| Delaware | Delaware | 0.22M | Columbus's northern suburbs |
| Allen | Lima | 0.10M | Northwest / industrial |
| Mercer / Auglaize / Putnam | rural | low | low-volume rural civil dockets |

## Common Loc. R. patterns across non-flagship Common Pleas

Smaller Common Pleas courts share most procedural
conventions:

- **Civ. R. baseline** governs unless a Loc. R. modifies
- **Page limits on briefs** — typically 15-25 pages
- **Working copies** — many smaller courts require paper
  bench copies; verify
- **Notice of hearing** — typically scheduled with
  chambers / bailiff
- **Magistrates** under Civ. R. 53 handle pretrial civil
  matters in most courts

## E-filing landscape

- Larger non-flagship Common Pleas courts use Tyler
  Technologies (Odyssey) or county-built portals
- Smaller rural Common Pleas may still require paper
  filings or partial e-filing

Verify per-court before assuming e-filing is available.

## Composition with other oh- skills

- `oh-statewide-format` — Civ. R. 10 format baseline
- `oh-pro-se` — pro-se framework
- `oh-discovery`, `oh-first-30-days`, `oh-hearings`,
  `oh-post-judgment` — procedural skills used across all
  Common Pleas courts
- `oh-consumer-debt`, `oh-family-law` — subject bundles
- `oh-municipal-courts` — Municipal Court layer (separate
  from Common Pleas; $15k cap)
