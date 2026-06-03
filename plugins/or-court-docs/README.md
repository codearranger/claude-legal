# or-court-docs — Oregon

Draft and format pleadings, declarations, motions, and proposed orders for Oregon circuit courts.

> **NOT LEGAL ADVICE.** Output is a drafting aid; verify every rule, deadline, and citation against current law before filing.

## What it covers

Applies **UTCR 2.010** formatting; covers Multnomah County Circuit Court (Portland / Central Courthouse), Washington County Circuit Court (Hillsboro), and the most-populous counties' roll-up (Clackamas, Lane, Marion, Jackson, Deschutes, Linn, Benton, Yamhill, Polk, Douglas). The `or-consumer-debt` bundle covers FDCPA / Reg F / Oregon UTPA (ORS 646.605) / ORS 697 Collection Agency Registration / chain-of-title.

Statute corpus: **35 ORS chapters / 5.6 MB**.

**Notable Oregon quirk:** no written interrogatories under ORCP without court order.

## Reference corpora

Under `skills/or-law-references/references/` (each corpus dir has its own README): `or-ors-debt/` (ORS chapters), `court-rules/`, plus the shared `federal-debt-laws/` / `federal-bankruptcy/` / `ucc-model/` symlinks into `claude-legal-federal-laws`.

## Refresh

`scripts/pull_oregon_ors.py` · `scripts/pull_oregon_rules.py`. Plugin scripts: `format-check.py` (UTCR 2.010) · `case-calendar.py` (ORCP 10 + ORS 187 holidays).

---
Part of the [claude-legal](../../README.md) marketplace. Skills are indexed in [CLAUDE.md](../../CLAUDE.md).
