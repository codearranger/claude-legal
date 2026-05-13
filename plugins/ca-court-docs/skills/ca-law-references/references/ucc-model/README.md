# Uniform Commercial Code — Model Text

The **model** UCC as drafted by the American Law Institute and
Uniform Law Commission. The version actually in force in
California is in [`../ca-statutes-debt/`](../ca-statutes-debt/)
under Cal. Comm. Code — cite the Cal. Comm. Code for state-
court matters and reference the model + comments only when
interpreting uniform language.

- Pulled: 2026-05-02
- Source: [Cornell Legal Information Institute](https://www.law.cornell.edu/ucc)

## Articles

| File | Article | Title | CA equivalent |
|---|---|---|---|
| [Article-1.md](Article-1.md) | UCC art. 1 | General Provisions | Cal. Comm. Code § 1101 et seq. |
| [Article-2.md](Article-2.md) | UCC art. 2 | Sales | Cal. Comm. Code § 2101 et seq. |
| [Article-3.md](Article-3.md) | UCC art. 3 | Negotiable Instruments | Cal. Comm. Code § 3101 et seq. |
| [Article-9.md](Article-9.md) | UCC art. 9 | Secured Transactions | Cal. Comm. Code § 9101 et seq. |

## California enactment specifics

California enacted Articles 1, 2, 3, and 9 of the UCC into the
Cal. Comm. Code. California's enactment is generally faithful
to the Model UCC but with state-specific variations:

- **Cal. Comm. Code § 9101 et seq.** (Art. 9) — California's
  enactment includes specific California modifications
  affecting deficiency judgments after non-judicial foreclosure
  (interaction with CCP § 580a, § 580b, § 580d), the "one
  action rule" (CCP § 726), and the anti-deficiency rules.
- **Cal. Comm. Code § 3118** — California's enactment of UCC
  § 3-118 (limitation of actions on negotiable instruments) is
  cited as the 6-year statute of limitations for notes and
  drafts.
- **Cal. Comm. Code § 2725** — California's enactment of UCC
  § 2-725 (4-year SOL on contracts for the sale of goods).

For day-to-day consumer-debt practice, the most relevant
California UCC provisions are Cal. Comm. Code § 9101 et seq.
(secured transactions, including holder-in-due-course analysis
for assigned debt-buyer claims) and §§ 3118 / 2725 (statutes
of limitation). See [`../../../ca-consumer-debt/references/ucc-article-9.md`](../../../ca-consumer-debt/references/ucc-article-9.md)
for the debt-buyer chain-of-title analysis under Cal. Comm.
Code Art. 9.

## Re-pulling

```
python3 scripts/pull_ucc.py
```
