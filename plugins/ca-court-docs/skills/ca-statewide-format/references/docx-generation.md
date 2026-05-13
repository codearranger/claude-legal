# docx-js Generation Patterns — California CRC 2.100-2.119

Working recipes for producing CRC-compliant `.docx` files using
the `docx` npm package (https://docx.js.org/) for conversion to
PDF and upload to a California eCourt filing portal.

## Why .docx, not direct PDF?

California courts accept (and for represented parties in most
courts, require) PDF for eFiling. The clean workflow is:

1. Generate the `.docx` from a template using `docx-js`
2. Save it locally so the litigant can review/edit in Word
3. Print or "Save As PDF" to produce the upload file
4. Upload the PDF to the eFiling portal (Odyssey eFileCA or
   File & ServeXpress) with the correct document code

Producing `.docx` gives the litigant a review surface —
essential for pro se filers who need to read and verify before
filing.

## California-specific formatting challenges

California CRC formatting has three elements that are unique
compared to Oregon and federal courts:

1. **2.5-inch top margin on page 1** (compared to Oregon's 3 inches
   or federal's 1 inch) — requires a section break between page 1
   and subsequent pages in `docx-js`
2. **Line numbers on the left margin** — consecutive numbers
   1-28 (or 1-33 for 1.5-spaced) — requires a two-column table
   or Word line-number feature
3. **CRC 2.110 footer on every page** including page 1

## Document setup

```javascript
import {
  Document, Packer, Paragraph, PageOrientation,
  SectionType, SectionProperties, Footer, AlignmentType,
  TextRun, PageNumber, TabStopType, TabStopPosition,
  Table, TableRow, TableCell, WidthType, BorderStyle,
  convertInchesToTwip
} from "docx";

const LETTER_WIDTH  = 12240;  // 8.5" in twips
const LETTER_HEIGHT = 15840;  // 11" in twips
const MARGIN_1IN    = 1440;   // 1" in twips
const MARGIN_2_5IN  = 3600;   // 2.5" in twips (page-1 top margin)
const CONTENT_WIDTH = 9360;   // 6.5" content area (8.5 - 1 - 1)

const doc = new Document({
  styles: {
    default: {
      document: {
        run: {
          font: "Times New Roman",
          size: 24,           // 12 pt (docx uses half-points)
        },
        paragraph: {
          spacing: {
            line: 480,        // double-spaced: 480 twips (240 × 2)
            lineRule: "auto",
          },
        },
      },
    },
  },
  sections: [
    // ─── Section 1: Page 1 (2.5" top margin) ────────────────────
    {
      properties: {
        type: SectionType.CONTINUOUS,
        page: {
          size: { width: LETTER_WIDTH, height: LETTER_HEIGHT },
          margin: {
            top:    MARGIN_2_5IN,  // 2.5" on page 1 for attorney block
            right:  MARGIN_1IN,
            bottom: MARGIN_1IN,
            left:   MARGIN_1IN,
            header: 720,           // 0.5"
            footer: 720,
          },
        },
      },
      footers: {
        default: makeFooter("DEFENDANT'S MOTION TO COMPEL", "24STCV12345"),
      },
      children: [
        ...attyBlock,      // attorney / party info block
        courtNamePara,     // centered court name
        captionTable,      // party block + case info table
        dividerParagraph,  // horizontal rule below caption
        ...bodyContent,    // body paragraphs (in line-number table)
        // End of page 1 — section break after last line of page 1
        // docx-js auto-paginates; the section break fires at the
        // end of this section's content
      ],
    },
    // ─── Section 2: Pages 2+ (1" top margin) ────────────────────
    {
      properties: {
        type: SectionType.NEXT_PAGE,
        page: {
          size: { width: LETTER_WIDTH, height: LETTER_HEIGHT },
          margin: {
            top:    MARGIN_1IN,    // 1" on subsequent pages
            right:  MARGIN_1IN,
            bottom: MARGIN_1IN,
            left:   MARGIN_1IN,
            header: 720,
            footer: 720,
          },
        },
      },
      footers: {
        default: makeFooter("DEFENDANT'S MOTION TO COMPEL", "24STCV12345"),
      },
      children: [
        ...remainingBodyContent,
        ...exhibits,
      ],
    },
  ],
});
```

**Note on section breaks**: `docx-js` v7+ supports the two-section
pattern. Place page-1 content (attorney block, caption, first page
of body) in section 1, and the rest of the document in section 2.
The `NEXT_PAGE` section type forces the margin change at the exact
page boundary.

## Footer with "Page X of Y" (CRC 2.110)

```javascript
function makeFooter(docTitle, caseNo) {
  return new Footer({
    children: [
      new Paragraph({
        tabStops: [{ type: TabStopType.RIGHT, position: 9360 }],
        children: [
          new TextRun({
            text: `${docTitle} — Case No. ${caseNo}`,
            font: "Times New Roman",
            size: 20,   // 10 pt
          }),
          // Right-aligned page counter
          new TextRun({ children: ["\t"] }),
          new TextRun({
            text: "Page ",
            font: "Times New Roman",
            size: 20,
          }),
          new TextRun({
            children: [PageNumber.CURRENT],
            font: "Times New Roman",
            size: 20,
          }),
          new TextRun({
            text: " of ",
            font: "Times New Roman",
            size: 20,
          }),
          new TextRun({
            children: [PageNumber.TOTAL_PAGES],
            font: "Times New Roman",
            size: 20,
          }),
        ],
      }),
    ],
  });
}
```

## Line numbers (CRC 2.108(b)) — two-column table approach

California requires consecutively numbered lines on the left
margin. The cleanest implementation in `docx-js` is a borderless
two-column table, with the left column containing line numbers
and the right column containing body text.

```javascript
// Build a "page" of 28 numbered lines (double-spaced, 12-pt)
// Each logical paragraph = one line in the table

function makeBodyWithLineNumbers(paragraphs) {
  const MAX_LINES_PER_PAGE = 28;
  const rows = [];

  paragraphs.forEach((para, i) => {
    rows.push(
      new TableRow({
        children: [
          // Left cell: line number
          new TableCell({
            width: { size: 360, type: WidthType.DXA },  // ~0.25"
            borders: allNoBorders(),
            children: [
              new Paragraph({
                alignment: AlignmentType.RIGHT,
                children: [
                  new TextRun({
                    text: String(i + 1),
                    font: "Times New Roman",
                    size: 20,   // 10 pt numbers
                  }),
                ],
                spacing: { line: 480, lineRule: "auto" },
              }),
            ],
          }),
          // Right cell: body text paragraph
          new TableCell({
            width: { size: 9000, type: WidthType.DXA },  // ~6.25"
            borders: allNoBorders(),
            children: [para],  // the pre-built paragraph
          }),
        ],
      })
    );
  });

  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    borders: allNoBorders(),
    rows,
  });
}

function allNoBorders() {
  const none = { style: BorderStyle.NONE };
  return { top: none, bottom: none, left: none, right: none,
           insideH: none, insideV: none };
}
```

**Alternative**: Use Word's built-in line-numbering feature
(`Document → Layout → Line Numbers → Continuous`). This is
simpler for documents that won't be programmatically generated
but doesn't work in a pure `docx-js` headless workflow.

## Caption table (CRC 2.111)

```javascript
// ) column separating party block from case info
// Left cell: ~3.5" wide; right cell: ~3" wide
const captionTable = new Table({
  width: { size: CONTENT_WIDTH, type: WidthType.DXA },
  borders: allNoBorders(),
  rows: [
    new TableRow({
      children: [
        new TableCell({
          width: { size: 5040, type: WidthType.DXA },
          borders: allNoBorders(),
          children: [
            cPara("VELOCITY INVESTMENTS, LLC,             )"),
            cPara("                                       )"),
            cPara("          Plaintiff,                   )"),
            cPara("                                       )"),
            cPara("    vs.                                )"),
            cPara("                                       )"),
            cPara("JANE DOE,                              )"),
            cPara("                                       )"),
            cPara("          Defendant.                   )"),
          ],
        }),
        new TableCell({
          width: { size: 4320, type: WidthType.DXA },
          borders: allNoBorders(),
          children: [
            cPara("Case No. 24STCV12345"),
            cPara(""),
            cPara("DEFENDANT'S NOTICE OF MOTION"),
            cPara("AND MOTION TO COMPEL;"),
            cPara("MEMORANDUM OF POINTS AND"),
            cPara("AUTHORITIES"),
            cPara(""),
            cPara("Date:  March 15, 2025"),
            cPara("Time:  10:00 a.m."),
            cPara("Dept.: 36"),
            cPara("Judge: Hon. John Smith"),
          ],
        }),
      ],
    }),
  ],
});

function cPara(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: "Times New Roman", size: 24 })],
    spacing: { before: 0, after: 0, line: 320, lineRule: "auto" },
  });
}
```

## Attorney/party info block (page 1, upper-left)

The attorney block appears in the top-left of page 1, within the
2.5-inch top margin space. Because the page margin is 2.5 inches,
the content area begins 2.5 inches from the top. The attorney
block is the first content in section 1.

```javascript
const attyBlock = [
  aPara("JANE DOE"),
  aPara("123 Main Street"),
  aPara("Los Angeles, CA 90012"),
  aPara("Tel: (213) 555-0100"),
  aPara("Email: jane.doe@email.com"),
  aPara(""),
  aPara("Defendant, self-represented"),
  aPara(""),
];

function aPara(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: "Times New Roman", size: 22 })],
    spacing: { before: 0, after: 0, line: 240, lineRule: "auto" },
  });
}
```

## Packaging and saving

```javascript
const buffer = await Packer.toBuffer(doc);
fs.writeFileSync("motion-to-compel.docx", buffer);
```

To convert to PDF for filing, use the `.docx` as the working
copy and either:
- Open in Microsoft Word → File → Save as PDF (best fidelity)
- Use `libreoffice --headless --convert-to pdf motion-to-compel.docx`
  (for server-side conversion; minor formatting differences from Word)
- Use the `docx-pdf` npm package (wraps LibreOffice)

## Validation

Run `plugins/ca-court-docs/scripts/format-check.py` on the
generated `.docx` to validate:
- 2.5-inch top margin on page 1
- CRC 2.110 footer present on all pages
- Font: Times New Roman 12 pt
- Line spacing: double or 1.5
- Line numbers present on left margin

The script will FAIL on a document missing the footer, having
the wrong top margin, or missing line numbers.

## Differences from Oregon and Washington docx patterns

| Element | California | Oregon | Washington |
|---------|------------|--------|------------|
| Top margin, page 1 | 2.5" | 3" | 1" |
| Section break needed? | Yes (2.5" → 1") | Yes (3" → 1") | No |
| Line numbers | Required | Not required | Not required |
| Footer | CRC 2.110: title + case no. + page | UTCR: title + page | CR: varies |
| Caption style | `)`-column | Explicit vertical rule | Horizontal rule |
| Two-hole punch | Top center | Not required | Not required |
