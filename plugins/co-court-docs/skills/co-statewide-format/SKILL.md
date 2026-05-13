---
name: co-statewide-format
description: >
  This skill should be used when the user asks to "draft a pleading",
  "format a Colorado court document", "apply C.R.C.P. 10", "apply CJD
  11-01", "build a Colorado caption", "create a declaration", "format
  a motion", "draft a motion under Rule 121", or "draft a proposed
  order" for any Colorado state court (district court, county court,
  water court, or probate court). Covers C.R.C.P. 10 form-of-pleadings
  requirements, Chief Justice Directive 11-01 statewide standards for
  pleading filing, the two-block Colorado caption (party block + case
  number / division / courtroom block), numbered paragraphs, signature
  blocks (with Colorado attorney-registration number when applicable),
  exhibit lists, and citation format per the Colorado Appellate Court
  conventions and the ICW Style Manual.
version: 0.1.0
---

# Colorado Statewide Court Document Formatting

> **NOT LEGAL ADVICE.** This skill assists with drafting and
> formatting only. Verify against current Colorado Rules of Civil
> Procedure, Chief Justice Directives, and the local rules of the
> filing court before submitting any document.

Use these rules whenever drafting a paper to be filed in a Colorado
state court. They derive from **C.R.C.P. 10** (Form of Pleadings,
Motions, and Other Documents) and **Chief Justice Directive 11-01**
(Standards for the Filing of Pleadings in Colorado State Courts).

## C.R.C.P. 10 + CJD 11-01 format requirements (mandatory)

| Item | Rule |
|------|------|
| Paper size | US Letter, 8½ × 11 inches |
| Sides | Single-sided only |
| Margins (all sides) | **Minimum 1 inch** (top, bottom, left, right) |
| Line spacing | **Double-spaced** for pleadings and motion text; single-spaced permitted for block quotes, footnotes, captions, and signature blocks |
| Body font size | **12 point** minimum |
| Font family | Clear, legible — Times New Roman, Arial, Century Schoolbook, or Calibri are all accepted |
| Color | **Black ink only** — no colored highlighting or colored text in the body. Color is permitted in exhibits only when grayscale would lose meaning (color photos, screenshots where color carries information) |
| Page numbers | Each page numbered consecutively; convention is `Page X of Y` in the footer |
| Caption | Two-block layout: party block on the left, case-number / division / courtroom block on the right |

Unlike Washington's GR 14 (3-inch top margin on page 1) or Oregon's
UTCR 2.010 (2-inch top margin), Colorado uses a **uniform 1-inch
margin on every side and every page**. Place the caption against the
top margin on page 1 — there is no required leading whitespace.

`scripts/format-check.py` validates these requirements against a
generated `.docx`.

## Default typography

- **Font**: Times New Roman 12 pt (most common in district court);
  Arial 12 pt also accepted under CJD 11-01
- **Line spacing**: Double for pleadings and motion text; single for
  block quotes, signature blocks, and captions
- **Paragraph numbering**: Bold Arabic numeral followed by a period
  and a tab, e.g. `1.\tI am the Petitioner...`
- **Bold lead-ins** for labeled paragraphs: `**Background.**` at the
  start of a paragraph, then regular text in roman

## Required footer (mandatory on every generated document)

Every generated document MUST carry a running footer on every page
with:

- **Left**: a short document identifier — typically
  `[Document title] — Case No. [case number]` (e.g.,
  `Motion to Dismiss — Case No. 2025CV031234`). Keep it to a single
  line so it never wraps.
- **Right**: `Page X of Y`, where `X` is the current page number and
  `Y` is the total page count. Use Word's `PAGE` and `NUMPAGES`
  fields — never a static number.
- **Font**: 10 pt; matches body font family.
- **Alignment**: right-aligned tab stop at 9,360 DXA (6.5") places
  the page counter flush right while the title stays flush left.

The footer runs continuously from page 1 through the last exhibit
page — do not restart or suppress pagination anywhere.

## Caption structure (C.R.C.P. 10(a) + CJD 11-01)

Colorado captions are distinctive: a **two-block layout** with the
party block at the upper-left and a separate boxed block on the
upper-right containing the case number, division, and courtroom.
The court name is centered above both blocks.

```
DISTRICT COURT, [COUNTY] COUNTY, COLORADO
[Street address]
[City, CO ZIP]

Plaintiff(s): VELOCITY INVESTMENTS, LLC,        ▲ COURT USE ONLY ▲
                                                ┌──────────────────┐
v.                                              │ Case Number:     │
                                                │  2025CV031234    │
Defendant(s): JOHN DOE.                         │                  │
                                                │ Division: 12     │
                                                │ Courtroom: 270   │
                                                └──────────────────┘
                       MOTION TO DISMISS
                  (UNDER C.R.C.P. 12(b)(5))
```

Build the caption as a two-cell table for the lower portion:

- **Left cell**: party block; wider (≈ 4,800 DXA)
- **Right cell**: case-number / division / courtroom box; narrower
  (≈ 2,160 DXA), with a 1-pt black border on all four sides

The "▲ COURT USE ONLY ▲" banner sits above the right cell (or above
the whole caption block). Place the document title in ALL CAPS,
centered, between the caption and the body.

## Required body elements

Every affidavit or declaration needs:

1. **Salutation clause** at the top of the body:
   "I, [Name], being first duly sworn upon oath" (affidavit) **or**
   "I, [Name], under penalty of perjury pursuant to C.R.S.
   § 13-27-104, declare as follows:" (declaration)
2. **Numbered paragraphs** with substantive content
3. **Verification clause** at the end (declaration form):
   "I declare under penalty of perjury pursuant to the laws of the
   State of Colorado that the foregoing is true and correct."
4. **Date and place of execution**:
   "Executed on [date] at [city], [state]."
5. **Signature block** with signer name, role, address, phone, email

Motions and memoranda do not need a perjury clause but do need:

- A signature block with name, address, phone, email
- A Colorado attorney-registration number (`#XXXXX`) if the signer is
  a Colorado-licensed lawyer; pro se filers omit this
- A short **certificate of service** at the foot of the document
  showing how, when, and on whom the document was served

## Signature block format

```
Respectfully submitted this ___ day of __________, 20__.

                                        ____________________________
                                        [Name]
                                        [Reg. No. ##### (if attorney)]
                                        [Street address]
                                        [City, CO ZIP]
                                        Phone: (###) ###-####
                                        Email: name@example.com
                                        [Pro Se / Attorney for Party]
```

The attorney-registration number is **mandatory** on every pleading
filed by a Colorado-licensed lawyer — see C.R.C.P. 11(a). Pro se
filers omit the number and add "Pro Se" or "Self-Represented" on the
last line.

## Certificate of service

Every document filed with the court must include a certificate of
service unless filed under seal or otherwise excused. Place it at the
foot of the document **above the signature block**:

```
                    CERTIFICATE OF SERVICE

I certify that on [date], a true and correct copy of the foregoing
[Document Title] was served on:

  [Opposing party name]
  [Address]
  via [E-Service through CCEFS / U.S. Mail, postage prepaid /
       email at name@example.com per C.R.C.P. 5(b)(2)(E)]

                                        ____________________________
                                        [Signer name]
```

Under C.R.C.P. 5(b), service by Colorado Courts E-Filing (CCEFS)
constitutes valid electronic service; pro se filers without a CCEFS
account must serve by mail, hand delivery, or email per C.R.C.P.
5(b)(2)(E).

## Exhibits

Embed exhibits at the end of the document, after the signature block
and certificate of service, in this order:

1. **Exhibit List** page, centered title, each entry like:
   `Exhibit A:    [one-line description]`
2. One **cover page per exhibit**: `EXHIBIT A` centered and bold at
   the top of the page, followed by an italic caption describing the
   exhibit, then the exhibit image or text
3. Footer pagination continues through the exhibits — do not restart
   the page counter

Reference exhibits in the body by letter: "True and correct copies of
the disputed account statements are attached hereto as **Exhibits A
through D**."

## The four document templates

See `references/templates/` for complete scaffolds:

- `declaration.md` — declaration / affidavit with numbered paragraphs
  and exhibits
- `motion-with-memo.md` — C.R.C.P. 121 § 1-15 motion with the
  combined motion-and-brief format (Colorado allows a unified
  document under the local Rule 121 conventions)
- `notice-of-setting.md` — notice that places a motion on the
  court's calendar after the JA/clerk has assigned a hearing
- `proposed-order.md` — proposed order for judge signature, with the
  caption replicated and the dispositional language sliced into
  numbered findings and a separate "IT IS THEREFORE ORDERED" block

Each template includes the caption, body skeleton, signature block,
certificate of service, and (for declarations) exhibit list
scaffolding.

## Citation format

Follow the Colorado Appellate Court conventions and the ICW Style
Manual. Common forms:

- Colorado Supreme Court: `People v. Smith, 2020 CO 12, ¶ 15, 456 P.3d 789` (post-2012 cases) or `People v. Jones, 252 P.3d 1191 (Colo. 2011)` (pre-2012)
- Colorado Court of Appeals: `Smith v. Jones, 2019 COA 45, ¶ 22, 432 P.3d 100`
- Tenth Circuit: `Spann v. Carter, 23 F.4th 1131 (10th Cir. 2022)`
- C.R.S.: `C.R.S. § 13-80-103.5` (always use the `§` symbol for
  Colorado statutes)
- C.R.C.P.: `C.R.C.P. 12(b)(5)` (no section symbol for rules)
- C.R.E.: `C.R.E. 803(6)`
- Federal statutes: `15 U.S.C. § 1692g`

Italicize case names (including `v.`). Use the public-domain neutral
citation format (`2020 CO 12, ¶ 15`) for Colorado Supreme Court and
Court of Appeals decisions issued after January 1, 2012; the parallel
P.3d citation is required.

## Producing documents programmatically

For `.docx` generation, use the `docx` npm package. Key points:

- Set page size explicitly to US Letter (12,240 × 15,840 DXA) —
  `docx-js` defaults to A4
- Use Times New Roman at `size: 24` (half-points = 12 pt)
- Apply uniform 1,440 DXA margins to all four sides on every section
- Build the right-block table cell with a 1-pt border on all four
  sides for the case-number / division / courtroom box
- Use `LevelFormat.BULLET` with a numbering config for bullets —
  never unicode bullet characters
- Build the footer with a right-aligned tab stop at 9,360 DXA and
  use `PageNumber.CURRENT` / `PageNumber.TOTAL_PAGES` for
  "Page X of Y"

For format validation, run `scripts/format-check.py` on the generated
`.docx`.

## Filing mechanics: paper vs. e-filing

Colorado is largely on **Colorado Courts E-Filing (CCEFS)** for
attorneys (mandatory for represented parties in most counties);
pro se filers may file electronically through CCEFS Pro Se if
available in the filing county, otherwise by paper at the clerk's
window. See `co-file-packet` for the full e-filing workflow.

## Composition

- For drafting a Colorado motion or memorandum: `co-draft-motion`
- For drafting a Colorado declaration: `co-draft-declaration`
- For drafting a notice of setting / hearing: `co-draft-note`
- For drafting a proposed order: `co-draft-order`
- For court-specific overlays: `co-denver`, `co-arapahoe`,
  `co-county-courts`
- For pro se conventions: `co-pro-se`
- For pre-filing QC: `co-quality-check`

## References

- `references/templates/declaration.md`
- `references/templates/motion-with-memo.md`
- `references/templates/notice-of-setting.md`
- `references/templates/proposed-order.md`
- `references/crcp-10-full-text.md` — the full rule text
- `references/cjd-11-01-full-text.md` — full text of the CJD
- `references/caption-format.md` — caption structure with the two-block layout and docx-js recipe
- `references/exhibit-handling.md` — exhibit list, cover page, and pagination
- `references/citation-format.md` — Colorado neutral-citation conventions
