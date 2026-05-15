# Skill template: `<abbr>-family-court`

Venue skill for the state's family court. Mirrors the
`ny-family-court` precedent. **Ships as part of the
baseline** — every state plugin has this skill, even when
family matters are heard in a "Family Division" of the
general-jurisdiction trial court rather than a separate
Family Court.

## Template

```markdown
---
name: <abbr>-family-court
description: >
  Use when drafting or filing in <STATE>'s family court —
  the trial court (separate or as a Family Division of the
  general-jurisdiction court) handling child custody,
  visitation, child support, paternity, juvenile
  delinquency where applicable, foster care +
  termination of parental rights, family-offense /
  protective orders, and divorce / dissolution where
  applicable. Triggers include '<STATE> family court',
  '<STATE FAMILY CODE/ACT>', '<STATE CHILD SUPPORT
  GUIDELINE NAME>', '<STATE FAMILY-OFFENSE PROTECTIVE
  ORDER NAME>', '<STATE CUSTODY STANDARD>'. Covers the
  state's family-court rule set, the support-magistrate /
  referee judicial structure (if any), the predicate
  notices for each petition type, and the form catalog
  (e.g., JDF series, FL series, etc.).
version: 0.1.0
---

# <STATE> Family Court (<STATE FAMILY-COURT ACT CITE>)

> **NOT LEGAL ADVICE.** Family-law cases involve
> significant long-term consequences. Verify against
> current statutes and consider consulting a licensed
> attorney before relying on this skill's output.

## At a glance

- **Court**: <STATE> Family Court (or "Family Division of
  the <STATE> Superior Court" / equivalent)
- **Authority**: <statutory cite for the court>
- **Procedural rules**: <22 NYCRR Part 205 in NY / Cal.
  Rules of Court Title 5 in CA / equivalent>
- **Filing fee**: <amount / fee-waived-by-default if so>
- **Coverage**: one per county / one per circuit / single
  statewide court (depends on state)
- **E-filing**: <state's family-court e-filing system if any>
- **Right to counsel**: <where the state provides assigned
  counsel — typically abuse/neglect respondents; in NY,
  also family-offense respondents facing OP consequences>

## Article / topic overview

### Child support

<state's child-support guideline framework with statutory cite>

- Guideline model: <income-shares OR percentage-of-payor-
  income>
- Statutory cap on combined parental income: <$ amount,
  effective date>
- Add-ons: child care, health insurance, unreimbursed medical,
  educational expenses
- Imputation-of-income standard: <state's standard>
- Modification threshold: <e.g., 15% in NY's CSSA review;
  10% in CO>

### Custody / parenting time

<state's custody framework with key statutory and case cites>

- Standard: best-interests-of-the-child (universal)
- <state-specific factors codified in the family-law code>
- Decision-making allocation vs. parenting time
- Joint vs. sole custody defaults
- Relocation: notice + standard for permission

### Paternity / parentage

<state's paternity framework — genetic-marker testing rules,
acknowledgment of parentage, presumed parentage>

### Family offense / Order of Protection

<qualifying-relationship catalog + qualifying-offense catalog>

- Duration: temporary (ex parte) → final
- Stay-away + no-contact + firearm-surrender clauses
- Interplay with parallel criminal-court orders

### Divorce / dissolution (where the family court hears it)

<some states route divorce to family court; others to
superior court matrimonial part>

### Abuse and neglect

<state's child-protective-services petitioner: ACS, DSS,
DCFS, etc.>

- Right to assigned counsel for parent respondent
- Disposition outcomes: adjustment, placement, termination
  of parental rights

## Court structure — judges, magistrates, referees

<state-specific judicial structure for family court>

- Family-court judges
- Support magistrates (where applicable — NY uses these
  exclusively for child-support matters under FCA § 439)
- Referees / commissioners
- 35-day written-objection clock for support-magistrate
  orders where applicable

## Distinctives

<state-specific quirks worth flagging>

## Filing checklist

1. **Identify the correct petition type** — each topic has
   its own form
2. **Determine the proper county / venue**
3. **Filing fee** — typically waived for family-court
   filings; verify
4. **First appearance** — typically 2-4 weeks after filing
5. **Court-appointed counsel** for the respondent on
   abuse/neglect, TPR, family-offense facing OP, JD

## Composition with other ny- skills

- `<abbr>-statewide-format` — baseline format
- `<abbr>-family-law` — the substantive bundle (uses this
  venue skill for procedural framing)
- `<abbr>-pro-se` — pro-se framework
- `<abbr>-deadlines` — family-court-specific clocks
- `<abbr>-first-30-days` — answer / counter-petition
- `<abbr>-file-packet` — state e-filing or paper

## Pro-se resources

- <state's family-court self-help center / forms catalog>
- <Family Justice Centers if state has them>
- <legal-aid orgs serving family-court clients>
```

## Notes for the author

- **Some states route divorce + property distribution to
  the Superior Court Matrimonial Part rather than Family
  Court.** In those states, the family-court skill should
  explicitly note that divorce is handled elsewhere and
  cross-reference the appropriate Superior Court skill. NY
  is an example: Family Court has concurrent jurisdiction
  with Supreme Court for **custody + support** but Supreme
  Court has exclusive jurisdiction over **divorce itself**.
- **Family-court records are usually confidential by
  statute.** The Distinctives section should flag this and
  note any limited-access exceptions.
- **The "Article overview" framing comes from NY's Family
  Court Act structure.** States with different family-law
  code structures should adapt (e.g., chapter-based, topic-
  based) but preserve the topic-coverage breadth.
