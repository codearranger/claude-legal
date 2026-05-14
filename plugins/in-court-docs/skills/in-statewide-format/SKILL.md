---
name: in-statewide-format
description: >
  This skill should be used when the user asks to "draft a pleading",
  "format an Indiana court document", "apply Indiana Trial Rule 5(E)",
  "Indiana Trial Rule 10", "Indiana caption format", "build a
  caption", "create a declaration for Indiana", "format a motion for
  Marion Superior Court", "Indiana proposed order", "Indiana
  pleading paper", or any similar request for statewide Indiana
  document formatting. Covers Indiana Trial Rule 5(E) page format
  (paper size, margins, font, line spacing, footer pagination),
  Indiana Trial Rule 10 (caption + paragraph numbering), Indiana
  Trial Rule 11(A) signature block, the statewide Odyssey e-filing
  conventions, certifications under Indiana Trial Rule 11(B), and
  citation format per the Indiana Supreme Court Rules on Citation.
  Trigger phrases: "format an Indiana pleading", "Indiana caption",
  "T.R. 5(E)", "T.R. 10", "Trial Rule 11 signature", "Indiana
  declaration", "Odyssey eFile Indiana", "Marion County caption",
  "Indiana Supreme Court Rule on Citation".
version: 0.1.0
---

# Indiana Statewide Court Document Formatting

Use these rules whenever drafting a paper for filing in an Indiana
trial court — a Circuit Court, a Superior Court, a County Court, or
a Small Claims docket within a Superior Court. They derive from the
**Indiana Trial Rules** (most importantly Trial Rules 5, 10, and
11), the **Indiana Rules of Evidence**, and the **Indiana Supreme
Court Rules on Admission, Discipline and Citation** (which the
Indiana Supreme Court adopts and publishes alongside the Trial
Rules at `courts.in.gov/rules`).

Indiana does not have a unified small-claims court statewide. Most
populous counties (Marion, Lake, Allen, St. Joseph, etc.) operate
small-claims dockets inside the county's Superior Court or, in
Marion County, within the **Marion County Small Claims Courts**
which are statutorily separate township-based courts (IC 33-34).
For monetary claims above the small-claims cap ($10,000 in most
counties, $8,000 in Marion County township small-claims courts per
IC 33-34-3-2), file in the Circuit Court or the civil division of
the Superior Court of the venue county.

> **NOT LEGAL ADVICE.** Generated content is a drafting aid; verify
> against the current Indiana Trial Rules, Local Rules of the
> filing court, and any applicable Indiana Supreme Court Order
> before filing.

## Trial Rule 5(E) — Format of Papers

| Item | Rule | Requirement |
|------|------|-------------|
| Paper size | T.R. 5(E)(1) | 8½ × 11 inches |
| Sides | T.R. 5(E)(1) | One side only |
| Color | T.R. 5(E)(1) | White paper |
| Top margin, page 1 | T.R. 5(E)(2) | At least 2 inches (room for clerk's stamp + e-filing header) |
| All other margins | T.R. 5(E)(2) | At least 1 inch on every side |
| Font / size | T.R. 5(E)(3) | 12-point type minimum; serif body (Times New Roman or equivalent); monospaced fonts permitted but disfavored |
| Line spacing | T.R. 5(E)(3) | Double-spaced body text; single-spacing permitted for block quotations of 50+ words, footnotes, headings, captions, and signature blocks |
| Page numbers | T.R. 5(E)(4) | Bottom center or bottom right of each page |
| Caption | T.R. 10(A) | First page; identifies the court, parties, cause number, and document title |
| Signature | T.R. 11(A) | Every paper signed by at least one attorney (or by the party if pro se) at end |
| Verification | T.R. 11(B) | When required by statute or rule, signed under penalties of perjury per IC 35-44.1-2-1 |

Indiana does **not** require line numbering on the left margin
(unlike California's CRC 2.108(b)). Numbered paragraphs are
required under T.R. 10(B) — see the paragraph-numbering section
below.

When producing a `.docx` for conversion to PDF and upload to
Odyssey, set page-1 top margin to 2 inches (to clear the clerk's
e-filing banner) and remaining pages to 1 inch. The repo's
`scripts/format-check.py` validates these constraints.

## Default typography

- **Font**: Times New Roman 12 pt (Cambria, Century Schoolbook,
  Garamond, Book Antiqua, and other serif body fonts of equivalent
  legibility are accepted)
- **Line spacing**: double-spaced body; single-spacing only for
  block quotations of 50+ words, footnotes, captions, signature
  blocks, and the "Distribution" service list
- **Paragraph style**: T.R. 10(B) requires that "all averments of
  claim or defense shall be made in numbered paragraphs, the
  contents of each of which shall be limited as far as practicable
  to a statement of a single set of circumstances." Use numbered
  paragraphs (`1.`, `2.`, `3.` ...) for every pleading, motion
  argument, and declaration.
- Bold lead-ins for labeled paragraphs are permissible:
  `**Background.** Plaintiff is ...`

## Footer (required on every page)

T.R. 5(E)(4) requires a page number on every page; Marion County
LR49-TR5-203 and most populous-county local rules additionally
require the **document short title and cause number** in the
footer for hardcopy chambers copies and courtesy copies. The
working convention statewide is:

- **Left or center**: short title of the document (e.g.,
  "DEFENDANT'S MOTION TO DISMISS")
- **Right**: `Page X of Y` using Word `PAGE` and `NUMPAGES` fields
- **Font**: 10 pt Times New Roman

Example: `DEFENDANT'S MOTION TO DISMISS — Cause No. 49D01-2503-PL-001234     Page 3 of 8`

The footer runs on every page including page 1. Do not suppress
it. The format-check.py script in this plugin verifies the footer
contains both `PAGE` and `NUMPAGES` fields and at least one
literal title token to the left.

## Caption — Trial Rule 10(A)

Indiana uses a single-column caption with the parties stacked on
the left and the document title stacked on the right separated by
a closing parenthesis chain `)`. The cause number is set off
immediately below the right column or beneath the document title.

```
                     STATE OF INDIANA
                  IN THE [COURT NAME] COURT
              [COUNTY NAME] COUNTY, INDIANA

[PARTY A NAME],                     )
                                    )
            Plaintiff,              )    Cause No. [NN]D[NN]-YYMM-[CT]-NNNNNN
                                    )
        v.                          )
                                    )
[PARTY B NAME],                     )
                                    )
            Defendant.              )
```

Key conventions:

- Court name line uses the canonical court designation: "Marion
  Superior Court," "Lake Circuit Court," "Allen Superior Court 3,"
  etc. (See `in-marion`, `in-lake`, `in-county-courts` for the
  exact form per court.)
- County line: "[COUNTY NAME] COUNTY, INDIANA" in all caps.
- Parties: stacked, left-justified, in normal case (not all caps).
  Role designation ("Plaintiff," "Defendant," "Petitioner,"
  "Respondent") indented under the party name.
- Use **"v."** (no "vs.") between parties — Indiana citation
  convention.
- Cause number: Indiana cause numbers follow the format
  `[County 2-digit]D[Court 2-digit]-YYMM-[Case Type]-NNNNNN`,
  e.g., `49D01-2503-PL-001234` (Marion County 49, Superior 1 ("D01"
  for the first division per the IOJA naming convention; Circuit
  Court of Marion County is `49C01`), filed March 2025, Plaintiff
  case type "PL," sequence 1234). The Odyssey portal generates this
  automatically; do not invent one when drafting a complaint.

The "STATE OF INDIANA" line is conventional but not strictly
required by T.R. 10(A). Most populous-county local rules include
it, and Marion Superior follows the practice.

## Document title

Just below the caption, centered and in ALL CAPS or bold title
case, give the document title:

- "COMPLAINT FOR DAMAGES"
- "DEFENDANT'S ANSWER, AFFIRMATIVE DEFENSES, AND COUNTERCLAIM"
- "DEFENDANT'S MOTION TO DISMISS UNDER TRIAL RULE 12(B)(6)"
- "MEMORANDUM IN SUPPORT OF DEFENDANT'S MOTION TO DISMISS"
- "DEFENDANT'S MOTION TO CORRECT ERROR (TRIAL RULE 59)"

For motions, follow the motion title with a colon-separated
description of the relief sought when appropriate.

## Signature block — Trial Rule 11(A)

Every paper filed in an Indiana court must be signed at the end by
counsel of record or by the party if self-represented. T.R. 11(A)
requires the signer's name, address, telephone, and **Attorney
Number** ("Atty. No." — assigned by the Indiana Supreme Court Roll
of Attorneys) for represented parties.

Pro se signature block (T.R. 11(A); see `in-pro-se`):

```
                              Respectfully submitted,


                              _______________________________
                              [PARTY NAME], Pro Se
                              [Street Address]
                              [City, IN ZIP]
                              Telephone: (___) ___-____
                              Email: ________________________
```

Counsel signature block:

```
                              Respectfully submitted,


                              _______________________________
                              [ATTORNEY NAME], Atty. No. [#####-##]
                              [FIRM NAME]
                              [Street Address]
                              [City, IN ZIP]
                              Telephone: (___) ___-____
                              Email: ________________________
                              Attorney for [Party]
```

## Verification — Trial Rule 11(B)

Where a verified pleading or declaration is required by rule (e.g.,
T.R. 65 preliminary injunction declarations) or by statute (e.g.,
IC 34-26-5 protective-order petitions), the signer must affirm:

> "I affirm, under the penalties for perjury, that the foregoing
> representations are true."
> /s/ [Name]
> [Date]

The phrase derives from IC 35-44.1-2-1 (perjury) and is the
Indiana statutory equivalent to a notarized oath under T.R. 11(B)
and IC 34-37-2-2. **Do not** import the California "I declare
under penalty of perjury under the laws of the State of
California ..." formulation; Indiana courts have rejected non-
conforming verifications.

## Distribution / certificate of service

Every filing other than the initial complaint must include a
**Certificate of Service** at the end stating how every party was
served. T.R. 5(B) is the underlying authority; the Odyssey system
auto-generates a Service Contacts certificate for e-filed
documents, but the working convention is to include the
certificate of service in the document body for the chambers copy
and for hardcopy back-up:

```
                       CERTIFICATE OF SERVICE

I certify that on [DATE], a copy of the foregoing was served on
all counsel of record via the Indiana E-Filing System and on the
following non-registered party by U.S. Mail, postage prepaid:

  [Name]
  [Address]

                              _______________________________
                              [SIGNER NAME], [Pro Se / Atty. No.]
```

## Exhibits

Indiana practice uses **lettered exhibits** (Exhibit A, Exhibit B,
Exhibit C ...) for documentary attachments, paralleling the
Bluebook/federal convention. Number exhibits sequentially in the
order they are first referenced. Each exhibit should be tabbed (in
hardcopy) or bookmarked in the PDF (e-filed) so the court can
navigate to it.

The Odyssey portal requires each exhibit to be uploaded as a
separate sub-document or appended to the main document as a single
PDF with a Table of Contents. Marion LR49-TR5-203 prefers the
single combined PDF with bookmarks for civil filings.

## Paragraph numbering — Trial Rule 10(B)

T.R. 10(B) requires:

> "All averments of claim or defense shall be made in numbered
> paragraphs, the contents of each of which shall be limited as
> far as practicable to a statement of a single set of
> circumstances; and a paragraph may be referred to by number in
> all succeeding pleadings."

Practical rules:

- Number every substantive paragraph of a complaint, answer,
  counterclaim, third-party complaint, declaration, or affidavit.
- Number arguments in a memorandum (`1.`, `2.`, ... within each
  section heading) when each numbered point states a discrete
  legal proposition.
- Number paragraphs in a motion's body when the motion sets out a
  factual basis; the prayer for relief is typically not numbered.
- Cross-reference earlier paragraphs by number when incorporating
  by reference: "Defendant incorporates the allegations in
  Paragraphs 1-14 of the Complaint by reference."

## Citation format

Indiana follows the **Indiana Supreme Court Rule on Citation**
(part of the Indiana Rules of Admission, Discipline, and Citation,
the "ARD"). Common forms:

- **Indiana Supreme Court**: *Hughley v. State*, 15 N.E.3d 1000
  (Ind. 2014)
- **Indiana Court of Appeals**: *Goossens v. Goossens*, 829 N.E.2d
  36 (Ind. Ct. App. 2005)
- **Trial Rules**: Ind. Trial R. 56(C) (preferred) or T.R. 56(C)
  (shortcut used in this skill bundle)
- **Evidence Rules**: Ind. Evid. R. 803(6) or IRE 803(6)
- **Indiana Code**: IC 34-11-2-9 (no "§" symbol in Indiana
  citation; some practitioners use "IC § 34-11-2-9" — both are
  accepted)
- **Indiana Constitution**: Ind. Const. art. 1, § 12
- **Federal cases**: *Iqbal*, 556 U.S. 662 (2009)
- **Federal statutes**: 15 U.S.C. § 1692k(a)(1)
- **Federal regulations**: 12 C.F.R. § 1006.30

**Distinctive Indiana style choices**:

- Year in parentheses **after** the reporter citation:
  *Smith v. Jones*, 123 N.E.3d 456 (Ind. 2023) — same as Bluebook
- Reporter abbreviations: **N.E.3d** (third series) for current
  cases; N.E.2d for 1936-2003 cases; N.E. for pre-1936 cases
- Italicize case names. Indiana does **not** italicize "Id." or
  "Ibid."
- Use "*Id.*" for the immediately preceding cite (no signal
  needed); use "*Id.* at [pin]" for a different page in the same
  source
- Indiana cases include the parallel "Ind." Reporter cite for
  older cases (pre-1981): *State v. Adams*, 274 Ind. 366, 412
  N.E.2d 1213 (1980) — but the parallel cite is dropping out of
  modern practice
- "art." and "§" used in constitutional citations: Ind. Const.
  art. 1, § 12

## The four document templates

For complete scaffolds, see:

- `in-draft-motion` — motion with memorandum of law and proposed
  order
- `in-draft-declaration` — declaration or affidavit with T.R.
  11(B) verification
- `in-draft-note` — proposed Notice of Setting / Notice of
  Hearing / Notice of Trial (Indiana does not use "Note for
  Motion Calendar" as Washington does; the analog is a Notice of
  Hearing)
- `in-draft-order` — proposed order for judge signature

## e-Filing — Indiana Odyssey

Indiana has a **statewide unified e-filing system** (the only
state besides Illinois that runs e-filing through Tyler Odyssey
statewide). Mandatory for represented parties in every county
since 2018; self-represented filers may e-file optionally.

- Portal: https://efile.courts.in.gov
- Accepted format: PDF only for filed documents (the .docx is the
  working copy)
- File size limit: 25 MB per document; multi-document filings can
  go up to 100 MB total
- Document codes: select from a dropdown matching the document
  title (the dropdown labels mirror T.R. 7 motion types)
- Service Contacts: configure for the case at first filing; every
  subsequent filing serves all listed contacts automatically

Compare to other states: Indiana's unified Odyssey portal is
**different from California's per-county vendor mix** (Odyssey
eFileCA + File & ServeXpress + county portals) and is closer to
Colorado's CCEFS in being a single statewide gateway.

## Compose with court-specific skills

This skill is **always** layered with one of:

- `in-marion` — Marion Superior Court / Marion County Small Claims
- `in-lake` — Lake Superior Court (Crown Point / Hammond / East
  Chicago)
- `in-county-courts` — every other county
- `in-pro-se` — for self-represented filers

The court-specific skill adds local rule variations, courtroom
divisions, chambers practice, and venue-specific filing quirks.

## References

- `references/trial-rule-5-summary.md` — concise summary of T.R. 5
- `references/trial-rule-10-caption.md` — caption layout with
  examples for each county
- `references/cause-number-format.md` — the Indiana case-number
  taxonomy
- `references/docx-generation.md` — `.docx` library patterns for
  Indiana captions and footers
- `references/templates/` — the four document templates

**NOT LEGAL ADVICE.** Generated content is a drafting aid; verify
against current rules and case law before filing.
