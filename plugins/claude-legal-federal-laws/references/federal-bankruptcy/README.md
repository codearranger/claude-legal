# Federal Bankruptcy Code

Title 11 of the United States Code — the Bankruptcy Code. One Markdown file per USC chapter. Verbatim text from the Office of the Law Revision Counsel USLM XML.

- Pulled: 2026-05-13
- Statute source: [uscode.house.gov USLM XML](https://uscode.house.gov/download/download.shtml), release point Public Law **119-84**.

## Chapters of Title 11

| File | Citation | Chapter |
|---|---|---|
| [Chapter-1.md](Chapter-1.md) | 11 U.S.C. §§ 101–112 | Chapter 1 — General Provisions (definitions, rules of construction, power of the court) |
| [Chapter-3.md](Chapter-3.md) | 11 U.S.C. §§ 301–366 | Chapter 3 — Case Administration (commencement, officers, administration) |
| [Chapter-5.md](Chapter-5.md) | 11 U.S.C. §§ 501–562 | Chapter 5 — Creditors, the Debtor, and the Estate (claims, exemptions, automatic stay, the estate) |
| [Chapter-7.md](Chapter-7.md) | 11 U.S.C. §§ 701–784 | Chapter 7 — Liquidation |
| [Chapter-11.md](Chapter-11.md) | 11 U.S.C. §§ 1101–1195 | Chapter 11 — Reorganization (including Subchapter V small-business reorganization) |
| [Chapter-12.md](Chapter-12.md) | 11 U.S.C. §§ 1201–1232 | Chapter 12 — Adjustment of Debts of a Family Farmer or Fisherman with Regular Annual Income |
| [Chapter-13.md](Chapter-13.md) | 11 U.S.C. §§ 1301–1330 | Chapter 13 — Adjustment of Debts of an Individual with Regular Income |
| [Chapter-15.md](Chapter-15.md) | 11 U.S.C. §§ 1501–1532 | Chapter 15 — Ancillary and Other Cross-Border Cases |

Chapter 9 (Adjustment of Debts of a Municipality) is intentionally omitted — outside the consumer- and small-business-bankruptcy scope of every claude-legal state plugin to date. If a future plugin needs it, add a single new row to `USC_TARGETS` in `scripts/pull_federal_debt_laws.py`.

## Re-pulling

```
python3 scripts/pull_federal_debt_laws.py
```

The same script pulls both `federal-debt-laws/` and `federal-bankruptcy/`. Update `USC_RELEASE` in the script when refreshing — every USC title is republished at every release point, so a single bump covers all five titles (11, 12, 15, 42, 50).

## Scope

This corpus is the verbatim statutory text of Title 11 only. The Federal Rules of Bankruptcy Procedure (Fed. R. Bankr. P.) and local district / division rules are separate sources and are not pulled here. State exemption schedules are in each state plugin's statutes corpus (e.g., Colorado at `co-statutes-debt/`, Washington at `wa-rcw-debt/`).

> **NOT LEGAL ADVICE.** Bankruptcy procedure is jurisdiction-specific and intersects with non-bankruptcy state law on exemptions, security interests, and family-support obligations. Verify against the current statute and local rules of the relevant bankruptcy court before relying on any text in this corpus.
