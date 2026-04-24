---
name: wa-statewide-format
description: >
  This skill should be used when the user asks to "draft a pleading",
  "format a Washington court document", "apply GR 14", "build a caption",
  "create a declaration", "format a motion", "note for motion docket", or
  "proposed order" for any Washington State court (superior, district, or
  municipal). Covers GR 14 page formatting, two-column pleading captions,
  numbered paragraphs, signature blocks, exhibit lists and cover pages,
  and citation format per the Washington Reporter of Decisions.
version: 0.1.0
---

# Washington Statewide Court Document Formatting

Use these rules whenever drafting a paper to be filed in a Washington State
court. They derive from **GR 14** (Format for Pleadings and Other Papers) and
common statewide drafting conventions.

## GR 14 format requirements (mandatory)

| Item | Rule |
|------|------|
| Paper size | US Letter, 8½ × 11 inches |
| Sides | Single-sided only |
| Page 1 top margin | **Minimum 3 inches** |
| All other margins | **Minimum 1 inch** (top, bottom, left, right on subsequent pages) |
| Color | No colored pages, highlighting, or colored markings |
| Attachments | Same rule applies unless the nature of the attachment makes compliance impractical (native screenshots, color photos as evidence, etc.) |
| Citations | Conform to the Reporter of Decisions format (see Appendix 1 to GR 14) |

When producing a `.docx` programmatically, apply a 1-inch top margin to the
whole section and add roughly 2 inches of leading space before the caption on
page 1 so that the effective top margin for page 1 is 3 inches. Subsequent
pages then fall at 1 inch automatically.

**Do not use colored highlighting or colored text** anywhere in the pleading
body. Color is permitted in attachments only when the nature of the
attachment makes B&W impractical (for example, native phone screenshots).

## Default typography

- **Font**: Times New Roman 12 pt (most WA courts accept Arial 12 pt as well)
- **Line spacing**: 1.5 or double-spaced for body text; single-spaced for
  block quotations, signature blocks, and tables
- **Paragraph numbering**: Bold Arabic numeral followed by a tab, e.g.
  `1.\tI am the Defendant...`
- **Bold lead-ins** for labeled paragraphs: `**Pre-Hearing Baseline.**` at
  the start of a paragraph, then regular text

## Required footer (mandatory on every generated document)

Every generated document MUST carry a running footer on every page with:

- **Left**: a short document identifier — typically
  `[Document title] — Case No. [case number]` (e.g., `Motion to Compel — Case
  No. 25CIV######KCX`). Keep it to a single line so it never wraps.
- **Right**: `Page X of Y`, where `X` is the current page number and `Y` is
  the total page count. Use Word's `PAGE` and `NUMPAGES` fields — never a
  static number.
- **Font**: 10 pt Times New Roman (matches body font family; smaller for
  visual hierarchy).
- **Alignment**: a right-aligned tab stop at 9,360 DXA (6.5″) places the
  page counter flush right while the title stays flush left.

The footer runs continuously from page 1 through the last exhibit page — do
not restart or suppress pagination anywhere. `scripts/format-check.py`
validates the footer and will FAIL on a document that is missing the
`NUMPAGES` field, the `PAGE` field, or a non-pagination title on the left.

See `references/docx-generation.md` for the exact `docx-js` recipe.

## Caption structure

Two columns separated by a vertical rule:

```
               [Court name, centered, bold]
       [State of Washington line, centered, bold]

VELOCITY INVESTMENTS, LLC,         │  No. [case number]
                                   │
        Plaintiff,                 │  [DOCUMENT TITLE IN ALL CAPS,
                                   │   BOLD, WRAPPED TO 4–6 LINES]
vs.                                │
                                   │
JOHN DOE,                          │
                                   │
        Defendant/Counter-         │
        Claimant.                  │
```

Build the caption as a two-cell borderless table; add a vertical border on
the right edge of the left cell (or the left edge of the right cell — not
both). Set cell widths to 4,680 DXA each on a 9,360 DXA (6.5-inch) content
area. Add a horizontal rule below the caption before the body.

## Required body elements

Every declaration and affidavit needs:

1. **Salutation clause** at the top of the body:
   "I, [Name], declare under penalty of perjury under the laws of the State
   of Washington as follows:"
2. **Numbered paragraphs** with substantive content
3. **Verification clause** at the end:
   "I declare under penalty of perjury under the laws of the State of
   Washington that the foregoing is true and correct."
4. **Date and place of execution**:
   "DATED this ____ day of __________, 20__."
   "Executed at [city], Washington."
5. **Signature block** with signer name, role, address, email

Motions and memoranda do not need a perjury clause but do need a signature
block with name, role, address, and email, and a short certification of
service if served with the filing.

## Exhibits

Embed exhibits at the end of the paper, after the signature block, in this
order:

1. **Exhibit List** page, centered title, each entry like:
   `Exhibit A:    [one-line description]`
2. One **cover page per exhibit**: `EXHIBIT A` centered and bold at the top
   of the page, followed by an italic caption describing the exhibit, then
   the exhibit image or text
3. Footer pagination continues through the exhibits — do not restart the
   page counter

Reference exhibits in the body by letter: "True and correct screenshots are
attached as **Exhibits A through D**."

## The four document templates

See the `references/templates/` directory for complete scaffolds:

- `declaration.md` — declaration with numbered paragraphs and exhibits
- `motion-with-memo.md` — noted motion with companion memorandum
- `note-for-motion-docket.md` — WA-standard note form
- `proposed-order.md` — findings and order for judge signature

Each template includes the caption, body skeleton, signature block, and (for
declarations) exhibit list scaffolding.

## Citation format (GR 14(d))

Follow the Washington Reporter of Decisions style. Common forms:

- Washington Supreme Court: `Griggs v. Averbeck Realty, 92 Wn.2d 576, 599 P.2d 1289 (1979)`
- Washington Court of Appeals: `State v. Smith, 100 Wn. App. 1, 995 P.2d 1232 (2000)`
- 9th Circuit: `Weinstein v. Mandarich Law Grp., No. 19-35130, ___ F. App'x ___ (9th Cir. 2019)`
- RCW: `RCW 19.16.260` (no section symbol for RCWs in WA style)
- Federal statutes: `15 U.S.C. § 1692k(a)(1)`

Italicize case names (including `v.`). Use the U.S. court reporter citation
for federal cases, not regional reporters.

## Producing documents programmatically

For `.docx` generation, use the `docx` npm package and follow the patterns
in `references/docx-generation.md`. Key points:

- Set page size explicitly to US Letter (12,240 × 15,840 DXA) — `docx-js`
  defaults to A4
- Use `Times New Roman` at `size: 24` (half-points = 12 pt)
- Add a leading paragraph with `spacing: { before: 2880 }` (2 inches) on
  page 1 to yield the 3-inch effective top margin
- Use `LevelFormat.BULLET` with a numbering config for bullets — never
  unicode bullet characters
- Build the footer with a right-aligned tab stop at 9,360 DXA and use
  `PageNumber.CURRENT` / `PageNumber.TOTAL_PAGES` for "Page X of Y"

For format validation, use the bundled `scripts/format-check.py` on a
generated `.docx`.

## References

- `references/gr-14-full-text.md` — the full rule text for quick citation
- `references/caption-format.md` — caption structure with full docx-js example
- `references/exhibit-handling.md` — exhibit list, cover page, and pagination
- `references/docx-generation.md` — `docx` npm library patterns for WA pleadings
- `references/templates/` — the four document templates
