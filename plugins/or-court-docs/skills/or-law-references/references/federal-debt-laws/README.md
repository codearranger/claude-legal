# Federal Debt Laws — Oregon Plugin Pointer

This directory mirrors the federal debt-law corpus from the
Washington plugin (`wa-court-docs`). Federal law applies
identically across state lines, so the substantive content
does not change between the WA and OR plugins.

## What lives here when fully populated

| Statute / Regulation | File | Source |
|----------------------|------|--------|
| FDCPA (15 USC § 1692 et seq.) | `FDCPA.md` | uscode.house.gov |
| FCRA (15 USC § 1681 et seq.) | `FCRA.md` | uscode.house.gov |
| TILA (15 USC § 1601 et seq.) | `TILA.md` | uscode.house.gov |
| ECOA (15 USC § 1691 et seq.) | `ECOA.md` | uscode.house.gov |
| Reg F (12 CFR pt 1006) | `Reg-F.md` | ecfr.gov |
| Reg V (12 CFR pt 1022, FCRA implementing) | `Reg-V.md` | ecfr.gov |
| Reg Z (12 CFR pt 1026, TILA implementing) | `Reg-Z.md` | ecfr.gov |
| Reg B (12 CFR pt 1002, ECOA implementing) | `Reg-B.md` | ecfr.gov |

## How to populate

Re-use the existing WA plugin script:

```bash
python3 scripts/pull_federal_debt_laws.py \
  --output plugins/or-court-docs/skills/or-law-references/references/federal-debt-laws/
```

The script extracts USLM XML and eCFR XML and writes Markdown
with verbatim text and citation tables.

## Cross-references

- `../or-consumer-debt/references/fdcpa.md` — Oregon-flavored
  agent-facing summary
- `../or-consumer-debt/references/reg-f.md` — agent-facing
  Reg F summary
- `../online-sources.md` — canonical URLs

## Status

Empty in the initial PR — only this README. The first
`pull_federal_debt_laws.py` run will populate.

## Oregon-specific notes

Federal law applies in Oregon civil cases as state-law claims
under the FDCPA, FCRA, TILA, etc. — Oregon state courts have
concurrent jurisdiction with federal district courts. The 9th
Circuit interprets these statutes for federal purposes; Oregon
state courts give Ninth Circuit interpretations **persuasive
weight** but are not bound by them.

The Oregon UTPA (ORS 646.605 et seq.) provides **state-law
parallel** claims to most FDCPA violations — sometimes with
better remedies (no $500 cap; broader injunctive relief).

See `../or-consumer-debt/references/utpa.md` for the
state-federal interaction in debt-collection cases.
