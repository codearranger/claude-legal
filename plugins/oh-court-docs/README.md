# oh-court-docs — Ohio

Draft and format pleadings, declarations, motions, and proposed orders for Ohio courts.

> **NOT LEGAL ADVICE.** Output is a drafting aid; verify every rule, deadline, and citation against current law before filing.

## What it covers

Applies **Ohio Civ. R. 10 + per-court local rules** (Ohio has no statewide pleading-format rule). Covers **eight flagship Court of Common Pleas venues each as its own skill** — Cuyahoga (Cleveland), Franklin (Columbus), Hamilton (Cincinnati), Summit (Akron), Montgomery (Dayton), Lucas (Toledo), Stark (Canton), Butler (Hamilton, OH) — plus a county-courts roll-up for the other 80 counties, a dedicated `oh-municipal-courts` skill (R.C. Chapter 1901; $15,000 civil cap; $6,000 small-claims division; the primary pro-se consumer-debt forum), and `oh-family-court` (the Domestic Relations Division + the Juvenile Division under R.C. Chapter 2151).

**Five subject-matter bundles:**
- `oh-consumer-debt` — FDCPA + Reg F + **Ohio Consumer Sales Practices Act** (R.C. Chapter 1345; R.C. 1345.09 treble damages + mandatory fees); chain of title under Ohio UCC Article 9 (R.C. Chapter 1309); the auto-repossession stack (UCC Art. 9 + **RISA** at R.C. Chapter 1317 + **Certificate of Motor Vehicle Title Law** at R.C. Chapter 4505); R.C. 2305.06 six-year written-contract SOL; no Ohio collection-agency licensing regime.
- `oh-family-law` — R.C. Chapter 3105 divorce + equitable distribution at R.C. 3105.171 (NOT community property); R.C. Chapter 3109 custody/parenting/support; R.C. Chapter 3119 income-shares CS guidelines ($300k combined-income cap); R.C. 3105.18 spousal support; R.C. Chapter 3127 UCCJEA; R.C. Chapter 3115 UIFSA.
- `oh-personal-injury` — **modified comparative negligence** with the 51% bar (R.C. 2315.33) + several liability for noneconomic damages (R.C. 2307.22); the **2005 S.B. 80 damages caps** (noneconomic R.C. 2315.18, punitive R.C. 2315.21); the **Ohio Products Liability Act** (R.C. 2307.71-.80) with the 10-year repose; medical malpractice (1-yr SOL R.C. 2305.113, affidavit of merit Civ. R. 10(D)(2), caps R.C. 2323.43); wrongful death (R.C. Chapter 2125); **political-subdivision immunity** (R.C. Chapter 2744); dog-bite strict liability (R.C. 955.28).
- `oh-employment` — **R.C. Chapter 4112** civil-rights/discrimination **as overhauled by the 2021 Employment Law Uniformity Act (H.B. 352)** — 2-year SOL, mandatory OCRC exhaustion, no individual supervisor liability, codified Faragher/Ellerth defense; minimum wage (R.C. Chapter 4111 + Ohio Const. art. II § 34a); prompt-pay (R.C. 4113.15); whistleblower (R.C. 4113.52); workers'-comp exclusive remedy (R.C. Chapter 4123) with the narrow R.C. 2745.01 intentional-tort exception; non-compete under *Raimonde v. Van Vlerah*; Ohio is **not** right-to-work.
- `oh-commercial-disputes` — **Ohio Uniform Trade Secrets Act** (R.C. 1333.61-.69); **Deceptive Trade Practices Act** (R.C. Chapter 4165); UFTA fraudulent transfer (R.C. Chapter 1336); corporations (R.C. Chapter 1701) with *Crosby v. Beam* close-corporation duty; the **Ohio Revised LLC Act** (R.C. Chapter 1706, eff. 2022, replacing R.C. 1705) with the charging-order exclusive remedy; arbitration (R.C. Chapter 2711); Civ. R. 9(B) fraud particularity; business torts.

**33 SKILL.md files.** Ohio quirks worth flagging: public-domain citation `YYYY-Ohio-NNNN` (mandatory in appellate cases since 2002); Columbus Day legal holiday (R.C. 1.14); 28-day answer; Civ. R. 53 magistrates with a 14-day objection clock; Civ. R. 41(A) one-dismissal rule.

## Reference corpora

Under `skills/oh-law-references/references/` (each corpus dir has its own README): `oh-statutes-debt/`, `court-rules/`, plus the shared federal symlinks.

## Refresh

`scripts/pull_ohio_statutes.py` · `scripts/pull_ohio_court_rules.py`. Plugin scripts: `format-check.py` · `case-calendar.py`.

---
Part of the [claude-legal](../../README.md) marketplace. Skills are indexed in [CLAUDE.md](../../CLAUDE.md).
