---
name: fl-family-court
description: >
  Florida Family Court division specifics — dissolution of marriage (Fla. Stat. § 61.052), child custody (parenting plans § 61.13), child support (Florida Child Support Guidelines § 61.30), domestic-violence injunctions (§ 741.30), equitable distribution. Triggers include 'Florida dissolution of marriage', 'Florida divorce', 'Florida child custody parenting plan § 61.13', 'Florida child support guidelines § 61.30', 'Florida domestic violence injunction § 741.30', 'equitable distribution Florida', 'Florida family court'.
version: 0.1.0
---

# Florida Family Court

Layer this skill on `fl-statewide-format` and the relevant
county-level venue skill for Family Division proceedings.

## Key framework — Florida family law

- **No-fault divorce only**: irreconcilable differences
  ("irretrievably broken," Fla. Stat. § 61.052(1)(b))
- **Equitable distribution** (not community property):
  court distributes marital assets and liabilities
  equitably (§ 61.075); marital assets presumed equal
  division subject to factors
- **Child custody**: the term "custody" was replaced in
  2023 by "parental responsibility" and "time-sharing"
  (§ 61.13); parenting plans are required
- **Residency**: at least one party must be a resident
  of Florida for **6 months** before filing (§ 61.021)

## Parenting plans (§ 61.13)

Florida courts require a **parenting plan** in every case
involving minor children. The plan must describe:
- Time-sharing schedule (day-to-day parenting time)
- Division of **parental responsibility** (major decisions)
- Communication methods between child and each parent

**Shared parental responsibility** (§ 61.13(2)(b)(1)) is
the default; sole parental responsibility for one parent
only when shared would be detrimental.

## Child support — Florida Child Support Guidelines (§ 61.30)

Florida uses an **income-shares model** based on both
parents' net incomes and the child's overnight schedule.
The Florida Child Support Guidelines Worksheet (Form 12.902(e))
calculates the guideline amount. Verify the current
income-bracket table against § 61.30.

## Equitable distribution (§ 61.075)

The court must first classify all assets/liabilities as
**marital or non-marital**, then distribute equitably.
Non-marital property is generally excluded from distribution.
Marital assets include: assets acquired during the marriage;
marital enhancement of non-marital assets; interspousal gifts;
retirement benefits earned during marriage.

## Domestic Violence Injunction for Protection (§ 741.30)

Any person who is a victim of domestic violence, or has
reasonable cause to believe they are in imminent danger,
may petition for an injunction.

**Ex parte temporary injunction**: issued same-day if the
petition shows immediate danger. Valid for **15 days**
pending the full hearing.

**Final injunction**: at the noticed hearing, if the court
finds domestic violence occurred or is imminent, a permanent
injunction (initially up to 1 year, renewable) may issue.

Florida forms: Petition for Injunction (Form 12.980(a)-12.980(d)).

## Composition

- `fl-statewide-format` + relevant county venue skill
- `fl-consumer-debt` for financial issues in dissolution
  involving debt obligations
- `fl-deadlines` for service and hearing deadline arithmetic

