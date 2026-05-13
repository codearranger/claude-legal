# Federal Debt Laws

Federal statutes and CFPB regulations relevant to consumer debt
collection. One MD per Act / CFR Part. Federal law is identical
across U.S. states; this directory mirrors the corpus shared
between the `ca-court-docs`, `or-court-docs`, and `wa-court-docs`
plugins so each plugin is self-contained for downstream
installers.

- Pulled: 2026-05-02
- Statute source: [uscode.house.gov USLM XML](https://uscode.house.gov/download/download.shtml), release point Public Law **119-84**.
- Regulation source: [eCFR XML versioner API](https://www.ecfr.gov/api), as-of date **2026-01-01**.

## Statutes — 15 U.S.C. Chapter 41 (Consumer Credit Protection)

| File | Citation | Act |
|---|---|---|
| [FDCPA.md](FDCPA.md) | 15 U.S.C. §§ 1692–1692p | Fair Debt Collection Practices Act |
| [FCRA.md](FCRA.md) | 15 U.S.C. §§ 1681–1681x | Fair Credit Reporting Act |
| [TILA.md](TILA.md) | 15 U.S.C. §§ 1601–1667f | Truth in Lending Act |
| [ECOA.md](ECOA.md) | 15 U.S.C. §§ 1691–1691f | Equal Credit Opportunity Act |

## Regulations — 12 C.F.R. (CFPB)

| File | Citation | Implements |
|---|---|---|
| [Reg-F.md](Reg-F.md) | 12 C.F.R. Part 1006 | FDCPA |
| [Reg-V.md](Reg-V.md) | 12 C.F.R. Part 1022 | FCRA |
| [Reg-Z.md](Reg-Z.md) | 12 C.F.R. Part 1026 | TILA |
| [Reg-B.md](Reg-B.md) | 12 C.F.R. Part 1002 | ECOA |

## California-specific overlays

California consumers and litigants should pair this corpus with
the state-law analogs in [`../ca-statutes-debt/`](../ca-statutes-debt/):

- **Rosenthal Act** (Cal. Civ. Code §§ 1788-1788.33) — state
  analog to the FDCPA; reaches both first-party and third-party
  collectors (broader than FDCPA).
- **FDBPA** (Cal. Civ. Code §§ 1788.50-1788.66) — Fair Debt
  Buying Practices Act; heightened pleading requirements for
  debt buyers.
- **CDCLA** (Cal. Fin. Code §§ 100000-100027) — California
  Debt Collection Licensing Act; DFPI licensure required since
  Jan 2022.
- **UCL** (Cal. Bus. & Prof. Code §§ 17200-17210) — Unfair
  Competition Law; borrows FDCPA / Rosenthal violations as
  "unlawful" prong predicate.
- **CLRA** (Cal. Civ. Code §§ 1750-1784) — Consumers Legal
  Remedies Act.

For day-to-day California-flavored consumer-debt defense, see
the [`ca-consumer-debt`](../../../ca-consumer-debt/) skill;
the federal-law content here provides the underlying citations.

## Re-pulling

```
python3 scripts/pull_federal_debt_laws.py
```

Update `USC15_RELEASE` and `ECFR_AS_OF` constants in the script
when refreshing.
