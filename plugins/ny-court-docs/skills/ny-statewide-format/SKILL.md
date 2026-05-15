---
name: ny-statewide-format
description: >
  Use when drafting or formatting any document for a New York
  state court (Supreme Court, County Court, Civil Court of the
  City of New York, District Court, City Court, or Town/Village
  Justice Court). Triggers include 'draft a New York pleading',
  'format an affidavit', 'apply 22 NYCRR § 202.5', '22 NYCRR
  202.5-b NYSCEF format', 'build a New York caption', 'serif
  vs. sans serif on a New York filing', 'verify NY citation
  style', 'Tanbook citation', 'New York Law Reports Style
  Manual', 'CPLR caption', 'put the index number on a NY
  filing', 'verified complaint format', 'affirmation under
  CPLR 2106'. Covers 22 NYCRR § 202.5 page/font/margin
  requirements, 22 NYCRR § 202.5-b NYSCEF electronic-filing
  technical requirements, the New York caption (CPLR 305(a) /
  CPLR 2101), document-title conventions, the verified-vs.-
  unverified pleading distinction (CPLR 3020–3021), affidavit
  (CPLR 2309) vs. affirmation (CPLR 2106) signature blocks,
  and citation format per the New York Law Reports Style Manual
  (Tanbook).
version: 0.1.0
---

# New York Statewide Format

> **NOT LEGAL ADVICE.** This skill provides drafting assistance
> only. Verify against current rules and case law before filing.

New York has no single, all-encompassing format rule the way
Washington has GR 14 or California has CRC 2.100. Format
requirements live across three layers:

1. **22 NYCRR § 202.5** — Uniform Civil Rules for the Supreme
   Court and County Court: page/font/margin rules for paper
   filings.
2. **22 NYCRR § 202.5-b** — NYSCEF (New York State Courts
   Electronic Filing) technical requirements for e-filed
   documents. NYSCEF is mandatory in most Supreme Court
   counties.
3. **Part rules** — every Justice of the Supreme Court
   publishes individual "Part Rules" (sometimes called "Rules
   of Practice") that override or supplement the uniform
   rules. Check the assigned Justice's Part Rules **before
   every filing.**

## Paper / page rules (22 NYCRR § 202.5(a))

- **Paper size**: 8½ × 11 inch (Letter)
- **Margins**: 1 inch on top, bottom, and both sides
- **Spacing**: Double-spaced text; quotations of 50+ words
  may be single-spaced and indented
- **Font**: Typeface that produces a clear copy; the rule
  is silent on a specific point size, but Times New Roman
  12-point or Courier New 12-point is the de facto standard.
  The Commercial Division (NY County, Kings County, Nassau,
  Westchester, Erie, etc.) requires **12-point** specifically
  under 22 NYCRR § 202.70(g) Rule 17.
- **Color**: Black ink on white paper for paper filings;
  NYSCEF accepts black-and-white or color PDFs but the body
  text must be readable monochrome.
- **Page numbering**: Bottom center or bottom right; format
  per Part Rules (some Justices require "Page X of Y").
- **Stapling / binding**: Paper filings — top-stapled, no
  fancy binding. NYSCEF — single PDF per document.

## NYSCEF technical requirements (22 NYCRR § 202.5-b)

NYSCEF is mandatory in: NY County, Kings, Bronx, Queens,
Richmond (commercial only), Nassau, Suffolk, Westchester,
Rockland, Erie, Monroe, Onondaga, and most other Supreme
Court counties. Civil Court of the City of New York uses a
parallel system (UCMS / CCEF).

- **File format**: PDF (text-searchable preferred; image-
  only PDFs allowed for true-paper exhibits)
- **Bookmarks**: Required for documents with multiple
  exhibits; bookmark to first page of each exhibit
- **File size**: 100 MB per upload cap
- **Naming**: Descriptive document title; no special
  characters
- **Signature**: An "/s/ Name" typed line plus an `e-filed
  by [Name]` line on the cover page; NYSCEF stamps the
  document automatically
- **Document codes**: NYSCEF requires selecting a document
  type from a controlled list (Affirmation, Affidavit,
  Memorandum of Law, Notice of Motion, Order, etc.). Pick
  the closest match.

## The New York caption (CPLR 305(a) and 2101)

```
SUPREME COURT OF THE STATE OF NEW YORK
COUNTY OF [COUNTY]
----------------------------------------- X
[PLAINTIFF NAME(S)],                       :
                                           :  Index No. [#####/YYYY]
                          Plaintiff(s),    :
                                           :  [DOCUMENT TITLE]
            -against-                      :
                                           :  Hon. [JUSTICE NAME]
[DEFENDANT NAME(S)],                       :  Part [##]
                                           :
                          Defendant(s).    :
----------------------------------------- X
```

Notes:

- **"-against-"** is the New York convention for the party
  separator. Not "v." or "vs."
- **Index Number**: assigned at the time of action
  commencement under CPLR 306-a. Format `[######/YYYY]`
  (e.g., `651234/2024`). Required on every paper after
  commencement.
- **The "X" enclosure** on the left side is traditional;
  the dotted-line ladder on the right is common but not
  mandated.
- **County name** appears in all caps below the court name.
- **"Hon. [Justice]"** and **"Part [##]"** are added once a
  case is assigned; can be omitted before assignment.

## Document title conventions

NY uses descriptive document titles centered below the
caption box, in bold or underlined or all-caps:

- **NOTICE OF MOTION** — formal scheduling document (CPLR
  2214); see `ny-draft-note`
- **VERIFIED COMPLAINT** — verified-pleading prefix
  (CPLR 3020) when the complaint is sworn-to
- **COMPLAINT** — unverified pleading (less common in
  consumer-debt and matrimonial matters)
- **AFFIRMATION OF [NAME] IN SUPPORT OF [MOTION]** — sworn
  statement by an attorney (CPLR 2106); see
  `ny-draft-declaration`
- **AFFIDAVIT OF [NAME] IN SUPPORT OF [MOTION]** — sworn
  statement by a non-attorney (CPLR 2309)
- **MEMORANDUM OF LAW IN SUPPORT OF [MOTION]** — legal
  argument; not required if all law is in the affirmation
  but Commercial Division Rule 17 prefers a separate memo
- **PROPOSED ORDER** — see `ny-draft-order`

## Verified vs. unverified pleadings (CPLR 3020)

**CPLR 3020(b)** *requires* verification when:

- The complaint alleges an account-stated claim (most
  consumer-debt complaints) — CPLR 3020(d)(2)
- The pleading must be served on the State of New York or
  a State official sued in an official capacity
- Either party has demanded verification

**CPLR 3020(a)** says a *verified pleading* may be served on
*any* opposing party who must then *answer with a verified
answer* (CPLR 3020(a)). This creates a tactical decision:
verifying your complaint forces the defendant to verify
their answer, which can deter frivolous denials.

Verification is a sworn statement at the foot of the
pleading: "[Affiant] swears the following pleading is true
to the affiant's own knowledge, except as to matters
alleged on information and belief which the affiant
believes to be true." Signed and notarized (CPLR 3021).

## Citation format — Tanbook

The **New York Law Reports Style Manual** ("Tanbook") is the
official citation manual for New York state court filings.
Key conventions vs. Bluebook:

- **Court of Appeals**: `Roe v. Doe, 1 NY3d 100, 105 (2003)`
  — note the missing periods (`NY3d` not `N.Y.3d`)
- **Appellate Division**: `Smith v. Jones, 50 AD3d 200,
  201 (1st Dept 2008)` — `AD3d`, department in parens
- **Supreme/County Trial**: `Roe v. Doe, 15 Misc 3d 100
  (Sup Ct, NY County 2007)` — published trial decisions go
  to `Misc 3d` (Miscellaneous Reports, 3rd Series)
- **Statutes**: `CPLR 3211(a)(7)` — no italics, no "N.Y."
  prefix in body text; "N.Y. C.P.L.R. § 3211(a)(7)" in
  out-of-state Bluebook context
- **Sessions Laws**: `L 2021, ch 593` — chapter laws
- **Public Authorities**: `Public Authorities Law § 1276`
- **Spaces in citations**: no spaces in compound abbreviations
  (`NYS2d` not `N.Y.S. 2d`)
- **Pinpoint cites**: `at 105` for parallel reporter; no
  pinpoint with "p." or "pp."

## State context

| Layer | Authority |
|---|---|
| Format rule | 22 NYCRR § 202.5 (paper) + § 202.5-b (NYSCEF) |
| Civil rules | CPLR (Civil Practice Law and Rules) |
| Evidence | Guide to NY Evidence + selected CPLR evidence sections (no codified code) |
| Statute | N.Y. CPLR; N.Y. Gen. Bus. Law; N.Y. Gen. Oblig. Law; N.Y. Real Prop. Law; N.Y. Real Prop. Acts. Law; etc. |
| Style manual | New York Law Reports Style Manual (Tanbook) |
| E-filing | NYSCEF (Supreme/County); UCMS/CCEF (NYC Civil Court) |

## Composition with other ny- skills

- `ny-nyco` / `ny-kings` / `ny-bronx` / `ny-nassau` /
  `ny-queens` / `ny-county-courts` — venue-specific overlays
  (Part Rules, courthouse logistics, scheduling)
- `ny-pro-se` — pro se conventions
- `ny-draft-motion`, `-declaration`, `-note`, `-order` —
  scaffolders that use these format conventions
- `ny-law-references` — full CPLR + Tanbook + 22 NYCRR
  reference corpora
- `ny-quality-check` — pre-filing QC against this format
  rule
