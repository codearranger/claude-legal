# Skill template: `<abbr>-family-law`

Subject-matter bundle covering the state's family-law
substantive framework. Mirrors the `co-family-law`
precedent. **Ships as part of the baseline alongside
`<abbr>-consumer-debt`** — every state plugin gets both
bundles in the initial release.

## Template

```markdown
---
name: <abbr>-family-law
description: >
  Use when handling a <STATE> family-law / domestic-
  relations matter — dissolution of marriage (divorce),
  declaration of invalidity (annulment), legal separation,
  allocation of parental responsibilities, parenting time,
  child support, and maintenance (spousal support).
  Triggers include 'divorce in <STATE>', '<STATE>
  dissolution of marriage', '<STATE> custody', '<STATE>
  parenting plan', '<STATE FAMILY CODE CITE>', '<STATE
  CHILD SUPPORT GUIDELINE NAME>', '<STATE MAINTENANCE
  STATUTE>', 'annulment <STATE>', 'legal separation
  <STATE>', '<STATE>'s mandatory financial disclosure
  form', 'post-decree modification <STATE>'. A subject-
  matter bundle covering the state's <UDMA-based OR
  community-property OR equitable-distribution> framework,
  mandatory financial-disclosure obligations, decision-
  making and parenting time, child-support guidelines and
  online worksheet (where available), maintenance formulas,
  modification thresholds, common-law marriage status,
  and the Hague / UCCJEA / UIFSA jurisdictional layers.
version: 0.1.0
---

# <STATE> Family Law — Divorce, Custody, Support

> **NOT LEGAL ADVICE.** Family-law cases involve
> significant long-term consequences for property,
> children, and finances. Strongly consider consulting a
> licensed <STATE> family-law attorney even on
> "uncontested" matters.

This subject-matter bundle covers the principal <STATE>
domestic-relations cases: **dissolution of marriage**
(divorce), **declaration of invalidity** (annulment),
**legal separation**, **allocation of parental
responsibilities**, **parenting time**, **child support**,
and **maintenance** (spousal support / alimony).

## Snapshot — <STATE> family-law principles

| Principle | <STATE> rule |
|---|---|
| Divorce grounds | No-fault available (<cite>); fault grounds: <list> |
| Waiting period | <number> days after filing / service before decree |
| Residency | <duration + cite> |
| Property regime | <community-property OR equitable-distribution> |
| Child support model | <income-shares OR percentage-of-payor-income> |
| CS combined-income cap | $<amount> (<effective date>) |
| Custody standard | Best-interests of child + <state's statutory factors> |
| Maintenance formula | <state's statutory or guideline framework> |
| Common-law marriage | <recognized / not recognized; cite> |
| Mandatory financial disclosure | <state's rule + form name> |
| Modification threshold (CS) | <e.g., 10% in CO; 15% in NY> |

## Dissolution (divorce)

<state's divorce procedural framework with cites>

- Petition + response + service
- Residency requirement
- Waiting period
- Mandatory financial disclosure
- Property division standard
- Maintenance award standard
- Decree finalization

## Annulment (declaration of invalidity)

<state's annulment grounds — usually narrow>

- Fraud / duress
- Bigamy / incest
- Underage
- Incapacity (mental or physical)
- Prohibited relationship

## Legal separation

<state's legal-separation framework where available>

## Property distribution

<state's property regime in detail>

### Community-property states

(CA, TX, WA, AZ, NM, ID, LA, NV, WI)

- Community property = property acquired during marriage
- 50/50 split presumption
- Separate property = pre-marital, gift, inheritance
- Commingling doctrines

### Equitable-distribution states

(everyone else)

- Factor-based discretionary division
- Common factors: duration of marriage, contributions,
  earning capacity, age, health, custodial duties, etc.
- No presumption of 50/50; courts may award up to 100%
  in unusual cases

## Child support

<state's guideline framework in detail>

- Statutory cap on combined parental income
- Guideline calculation worksheet (form name)
- Add-ons: child care, health insurance, unreimbursed
  medical, educational expenses
- Imputation of income
- Deviation grounds
- Modification threshold (e.g., 10% in CO; 15% in NY's
  CSSA review)

## Custody / parenting time

<state's framework in detail>

- Best-interests standard
- <state-specific factors codified in the family-law code>
- Decision-making vs. parenting time
- Joint vs. sole defaults
- Parenting-plan content requirements
- Relocation: notice + standard

## Maintenance (spousal support / alimony)

<state's framework>

- Duration formulas
- Income-based formulas (where applicable)
- Modification + termination triggers (cohabitation,
  remarriage, retirement)
- Tax treatment (post-TCJA: no deduction for payor on
  post-2018 decrees)

## Family offense / Protective orders

<state's family-offense framework where the family-law
bundle covers it (some states route this to the family
court bundle, others to the venue skill)>

## UCCJEA + UIFSA

- **UCCJEA** (Uniform Child Custody Jurisdiction and
  Enforcement Act) — home-state jurisdiction analysis;
  initial-custody jurisdiction; modification jurisdiction;
  emergency jurisdiction
- **UIFSA** (Uniform Interstate Family Support Act) —
  controlling-order doctrine; continuing exclusive
  jurisdiction; registration of out-of-state orders

## Common-law marriage

<state's status — recognized / not recognized; if
recognized, the test and any modernizing case law>

States that still recognize common-law marriage as of
2026: Colorado (modernized by *Hogsett & Neale*), Iowa,
Kansas, Montana, Rhode Island, South Carolina, Texas,
Utah, plus DC. New York does not recognize but honors
marriages valid where contracted.

## Filing forms catalog

<state-specific forms — e.g., NY JDF 1099, 1111; CA FL-100,
FL-110, FL-150; CO JDF 1099, 1111, 1820>

## Composition with other <abbr>- skills

- `<abbr>-family-court` — the venue skill (procedural
  framing)
- `<abbr>-statewide-format` — caption + paper format
- `<abbr>-deadlines` — family-specific clocks
- `<abbr>-fact-check` — citation verification (family-law
  citations differ in format from civil litigation in
  some states)
- `<abbr>-pro-se` — pro-se framework (family-court
  pro-se filing is dominant for petitioners on most
  matters)
- `<abbr>-draft-motion` / `-declaration` / `-order` —
  scaffolders adapted to family-court conventions

## Example synthetic filings (references/examples/)

- Petition for Dissolution of Marriage
- Sworn Financial Statement (or state's equivalent)
- Parenting-Plan / Custody Motion
- Child-Support Calculation Worksheet
- Motion to Modify Custody (post-decree)
- Motion to Modify Child Support (15% / 10% threshold)
```

## Notes for the author

- **Don't import another state's family-law framework.**
  Property distribution, child-support model, divorce
  grounds, waiting periods, and modification thresholds
  all vary materially state-to-state. Research the
  authoritative cites for the specific state.
- **Cross-state family-law quirks are catalogued in
  `references/cross-state-quirks.md`.** Use that catalog
  for research framing — but don't import cross-state
  comparisons into the new plugin's bodies (see SKILL.md's
  "CRITICAL: No cross-state references" rule).
- **The CO precedent (`co-family-law`) is the most fleshed-
  out family-law bundle currently shipping.** Use it as a
  structural reference, not as content to copy-paste from.
