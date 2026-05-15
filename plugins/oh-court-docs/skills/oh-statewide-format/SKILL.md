---
name: oh-statewide-format
description: >
  Use when drafting any Ohio court filing — applies Ohio
  Civ. R. 10 caption + signature requirements, the common
  local-rule format conventions adopted by most Ohio Common
  Pleas and Municipal Courts (Letter paper; 1-inch margins
  with 1.5-inch top on first page for caption; 12-point
  minimum body font; double-spaced body), the Ohio public-
  domain citation format `YYYY-Ohio-NNNN` mandatory in
  appellate cases since 2002, and the affidavit-vs-
  declaration terminology distinction (Ohio uses
  "affidavit" under R.C. 2319.04 + Civ. R. 56; "declaration
  under penalty of perjury" is federal practice). Triggers
  include "Ohio court filing format", "Ohio Civ. R. 10",
  "Ohio caption", "Ohio attorney registration number", "Ohio
  public-domain citation", "Ohio affidavit format", "first
  page caption Ohio", "Common Pleas local rules format".
version: 0.2.0
---

# Ohio Statewide Format — Civ. R. 10 + Per-Court Local Rules

> **NOT LEGAL ADVICE.** Verify the specific court's local
> rules before every filing. Format compliance varies
> materially between Common Pleas, Municipal, County, and
> Court of Claims venues.

## At a glance

Ohio has **no single statewide pleading-format rule**
analogous to a uniform civil-rules code that dictates
formatting across all courts. Format requirements live
across three layers:

1. **Ohio Civ. R. 10** — caption + signature block + form
   of pleadings (statewide minimum)
2. **Ohio Rules of Superintendence** (Sup. R. — most
   relevant: Sup. R. 26 on records and Sup. R. 44-47 on
   case-management standards)
3. **Per-court local rules** — each Common Pleas court
   publishes its own Loc. R. with page limits, certificate-
   of-service requirements, working-copy conventions, etc.

This skill enforces the common-denominator baseline. Always
cross-reference the assigned court's local rules.

## Caption format (Civ. R. 10(A))

Every pleading caption must include:

- **Court name** in full: `IN THE COURT OF COMMON PLEAS OF
  CUYAHOGA COUNTY, OHIO` (or the applicable court)
- **Division** if applicable: `CIVIL DIVISION` /
  `DOMESTIC RELATIONS DIVISION` / `JUVENILE DIVISION` /
  `PROBATE DIVISION`
- **Case number** — Common Pleas case numbers typically
  follow `CVNNNNNN` (general civil), `DRNNNNNN` (domestic
  relations), or court-specific patterns
- **Parties** — `<Plaintiff Name>` / `vs.` / `<Defendant
  Name>` (Ohio uses `vs.` with periods)
- **Title of the document** — e.g., `DEFENDANT'S ANSWER`,
  `MOTION TO DISMISS`, `NOTICE OF HEARING`

The first-page caption block typically occupies the top
1.5 inches; body text begins below.

## Paper format (statewide common denominator)

- **Paper**: Letter (8.5 x 11 inches)
- **Margins**: 1.5-inch top on first page (caption block);
  1-inch top on subsequent pages; 1-inch sides + bottom
- **Font**: 12-point minimum (Times New Roman or
  comparable serif preferred)
- **Line spacing**: double-spaced body (most local rules)
- **Page numbering**: footer with page number; some courts
  require `Page X of Y` format
- **Color**: black text on white paper

## Signature block (Civ. R. 11)

- **Counsel signature** must include:
  - Attorney's name
  - **Ohio Supreme Court attorney registration number**
    (`Atty. Reg. #NNNNNNN` — required under Gov. Bar R.
    VI(1)(B))
  - Firm name (if any)
  - Address + phone + fax + email
- **Pro se signature** must include:
  - Name + address + phone + email
  - The designation `Pro Se` or `Self-Represented`
  - **Omit attorney registration number** (don't fabricate)

## Affidavit vs. Declaration terminology

Ohio practice uses **affidavit** under **R.C. 2319.04** for
notarized sworn statements and uses **affidavit** under
**Civ. R. 56(C)** for summary-judgment support. The
federal-style "declaration under penalty of perjury"
terminology (28 U.S.C. § 1746) is **not** Ohio civil
practice. The `oh-draft-declaration` skill produces Ohio-
correct affidavits despite its scaffolder-conventional
name.

## Citation format (Ohio public-domain citation)

Ohio adopted a **public-domain citation system in 2002** —
**`YYYY-Ohio-NNNN`** format is **mandatory** in appellate
cases. Examples:

- *Smith v. Jones*, 100 Ohio St.3d 543, 2003-Ohio-1234,
  paragraph 12
- *State v. Brown*, 2018-Ohio-5678 (10th Dist.)

Trial-court citations follow the reporter's conventions:

- Ohio Supreme Court: `Ohio St.3d`
- Ohio Court of Appeals: `Ohio App.3d`
- Trial court: `Ohio Misc.2d`

For statutory citations:

- `R.C. 1345.01` (preferred) or `Ohio Rev. Code Ann.
  § 1345.01`
- Ohio Civ. R.: `Civ. R. 10(A)` (no `Ohio` prefix in
  in-state filings)
- Ohio Evid. R.: `Evid. R. 803(6)`

## Common per-court local-rule variations

These vary materially by court. Verify before filing:

- **Page limits on briefs** — many Common Pleas courts cap
  motion briefs at 15-25 pages; some impose 30
- **Working copies** — some judges require courtesy paper
  copies; others rely on electronic filing only
- **Certificate of service** — format and signature
  requirements vary; verify Loc. R.
- **Proposed orders** — some courts require a Word version
  emailed to chambers; others require a tendered paper
  original

## Composition with other oh- skills

- `oh-quality-check` — runs pre-filing format + content QC
- `oh-cuya` / `oh-frank` / etc. — flagship Common Pleas
  local-rule overlays
- `oh-county-courts` — long-tail roll-up
- `oh-municipal-courts` — Municipal Court format
  conventions
- `oh-pro-se` — pro-se signature + tone framework
- `oh-fact-check` — Ohio public-domain citation
  verification
