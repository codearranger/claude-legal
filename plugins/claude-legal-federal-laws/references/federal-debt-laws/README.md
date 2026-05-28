# Federal Debt Laws

Federal consumer-finance statutes and the CFPB regulations that implement them. One MD file per Act or CFR Part. Verbatim text from the official sources.

- Pulled: 2026-05-13
- Statute source: [uscode.house.gov USLM XML](https://uscode.house.gov/download/download.shtml), release point Public Law **119-84**.
- Regulation source: [eCFR XML versioner API](https://www.ecfr.gov/api), as-of date **2026-01-01**.

## Statutes — 15 U.S.C. Chapter 41 (Consumer Credit Protection Act)

| File | Citation | Act |
|---|---|---|
| [TILA.md](TILA.md) | 15 U.S.C. §§ 1601–1667f | Truth in Lending Act (CCPA Title I) |
| [Garnishment.md](Garnishment.md) | 15 U.S.C. §§ 1671–1677 | Restrictions on Garnishment (CCPA Title III) |
| [FCRA.md](FCRA.md) | 15 U.S.C. §§ 1681–1681x | Fair Credit Reporting Act (CCPA Title VI) |
| [ECOA.md](ECOA.md) | 15 U.S.C. §§ 1691–1691f | Equal Credit Opportunity Act (CCPA Title VII) |
| [FDCPA.md](FDCPA.md) | 15 U.S.C. §§ 1692–1692p | Fair Debt Collection Practices Act (CCPA Title VIII) |
| [EFTA.md](EFTA.md) | 15 U.S.C. §§ 1693–1693r | Electronic Fund Transfer Act (CCPA Title IX) |

## Statutes — other federal acts

| File | Citation | Act |
|---|---|---|
| [RESPA.md](RESPA.md) | 12 U.S.C. §§ 2601–2617 | Real Estate Settlement Procedures Act |
| [FHA.md](FHA.md) | 42 U.S.C. §§ 3601–3619 | Fair Housing Act (Title VIII of the Civil Rights Act of 1968) |
| [SCRA.md](SCRA.md) | 50 U.S.C. §§ 3901–4043 | Servicemembers Civil Relief Act |

## Regulations — CFPB (12 C.F.R. Chapter X) and FTC (16 C.F.R.)

| File | Citation | Implements |
|---|---|---|
| [Reg-B.md](Reg-B.md) | 12 C.F.R. Part 1002 | ECOA |
| [Reg-E.md](Reg-E.md) | 12 C.F.R. Part 1005 | EFTA |
| [Reg-F.md](Reg-F.md) | 12 C.F.R. Part 1006 | FDCPA |
| [Reg-M.md](Reg-M.md) | 12 C.F.R. Part 1013 | Consumer Leasing Act (TILA) |
| [Reg-N.md](Reg-N.md) | 12 C.F.R. Part 1014 | Mortgage Acts and Practices (MAP Rule) |
| [Reg-P.md](Reg-P.md) | 12 C.F.R. Part 1016 | Gramm-Leach-Bliley financial-privacy disclosures |
| [Reg-V.md](Reg-V.md) | 12 C.F.R. Part 1022 | FCRA |
| [Reg-X.md](Reg-X.md) | 12 C.F.R. Part 1024 | Real Estate Settlement Procedures Act (RESPA) |
| [Reg-Z.md](Reg-Z.md) | 12 C.F.R. Part 1026 | TILA |
| [Reg-DD.md](Reg-DD.md) | 12 C.F.R. Part 1030 | Truth in Savings Act |
| [TSR.md](TSR.md) | 16 C.F.R. Part 310 | FTC Telemarketing Sales Rule (Telemarketing and Consumer Fraud and Abuse Prevention Act) |

## Re-pulling

```
python3 scripts/pull_federal_debt_laws.py
```

Update `USC_RELEASE` and `ECFR_AS_OF` constants in the script when refreshing. The shared `claude-legal-federal-laws` plugin is the canonical home for this corpus — every state plugin reaches it via a symlink, so a single pull refreshes content for all states. The same script also populates the sibling `federal-bankruptcy/` corpus.

## Scope

Despite the directory name, this corpus covers the broader consumer-finance regulatory perimeter (CFPB + FTC) — not just debt-collection laws. Coverage includes credit reporting (FCRA, Reg V), credit access and discrimination (ECOA, Reg B), mortgage disclosures (TILA, Reg Z; RESPA statute and Reg X; MAP Rule, Reg N), electronic payments (EFTA, Reg E), consumer leasing (Reg M), bank-account terms (Reg DD), financial-privacy disclosures (Reg P), federal limits on wage garnishment (CCPA Title III), fair-housing discrimination claims that overlap with consumer credit (FHA), servicemember protections that intersect with collection and foreclosure (SCRA), and FTC-level deception-and-fraud rules applicable to debt-relief telemarketing (TSR). The directory name is preserved for backwards compatibility with downstream skills that cite paths under `federal-debt-laws/`.

Adjacent federal corpora:

- [`../federal-bankruptcy/`](../federal-bankruptcy/) — Title 11 U.S.C., the Bankruptcy Code (chapters 1, 3, 5, 7, 11, 12, 13, 15).
