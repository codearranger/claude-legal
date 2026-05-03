# Federal Debt Laws

Federal statutes and CFPB regulations relevant to consumer debt collection. One MD per Act / CFR Part.

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

## Re-pulling

```
python3 scripts/pull_federal_debt_laws.py
```

Update `USC15_RELEASE` and `ECFR_AS_OF` constants in the script when refreshing.
