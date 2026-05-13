# docx-js Generation Patterns — Oregon UTCR 2.010

Working recipes for producing UTCR 2.010-compliant `.docx` files
using the `docx` npm package
(https://docx.js.org/) for upload to OJD File and Serve.

## Why .docx, not direct PDF?

OJD File and Serve accepts only PDF. The clean workflow is:

1. Generate the `.docx` from a template using `docx-js`
2. Save it locally so the litigant can review/edit in Word
3. Print or "Save As PDF" to produce the upload file
4. Upload the PDF to File and Serve, picking the matching UTCR
   2.110 document code

Producing `.docx` (rather than direct PDF) gives the litigant a
review surface — most pro se filers want to read and tweak before
filing.

## Document setup

```javascript
import { Document, Packer, Paragraph, PageOrientation,
         SectionType, Footer, AlignmentType, TextRun,
         PageNumber, TabStopType, TabStopPosition, HeaderFooter,
         convertInchesToTwip } from "docx";

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "Times New Roman", size: 24 },  // 12 pt
        paragraph: {
          spacing: { line: 360, lineRule: "auto" },  // 1.5x
        },
      },
    },
  },
  sections: [{
    properties: {
      page: {
        size: {
          width: 12240,   // 8.5"
          height: 15840,  // 11"
        },
        margin: {
          top: 1440,      // 1"
          right: 1440,
          bottom: 1440,
          left: 1440,
          header: 720,    // 0.5"
          footer: 720,
        },
      },
    },
    footers: { default: makeFooter("Motion to Compel — Case No. 25CV12345") },
    children: [
      // 2-inch leading spacer to push first content down to ~3" from top of page 1
      new Paragraph({ spacing: { before: 2880 } }),
      ...captionAndBody,
    ],
  }],
});
```

## Footer with "Page X of Y" (UTCR 2.010(4))

```javascript
function makeFooter(documentTitle) {
  return new Footer({
    children: [
      new Paragraph({
        tabStops: [{ type: TabStopType.RIGHT, position: 9360 }],
        children: [
          new TextRun({
            text: documentTitle,
            font: "Times New Roman",
            size: 20,  // 10 pt
          }),
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

The `PageNumber.CURRENT` and `PageNumber.TOTAL_PAGES` constants
emit `PAGE` and `NUMPAGES` Word fields — these are what
`scripts/format-check.py` looks for. A static "Page 5" string in
the footer will FAIL the format check.

## Caption table

See `caption-format.md` for the full caption-table recipe. Key
details:

- Two cells, 4,680 DXA each
- Vertical rule on the right of left cell OR left of right cell
  (not both)
- No top, bottom, left-of-left, right-of-right borders
- Horizontal rule below the table, full width

## Numbered paragraphs

Oregon uses bold Arabic numerals followed by a period and tab:

```javascript
const para = (num, text) => new Paragraph({
  children: [
    new TextRun({ text: `${num}.`, bold: true }),
    new TextRun({ text: "\t" }),
    new TextRun({ text }),
  ],
  indent: { left: 720, hanging: 720 },  // hanging indent for wrapping
});
```

For paragraphs with a bold lead-in label:

```javascript
const labeledPara = (num, label, text) => new Paragraph({
  children: [
    new TextRun({ text: `${num}.`, bold: true }),
    new TextRun({ text: "\t" }),
    new TextRun({ text: `${label}. `, bold: true }),
    new TextRun({ text }),
  ],
  indent: { left: 720, hanging: 720 },
});
```

## Signature block

```javascript
const signatureBlock = (name, role, address, phone, email) =>
  new Paragraph({
    spacing: { before: 480 },
    children: [
      new TextRun({ text: "DATED this ____ day of __________, 20__." }),
      new TextRun({ break: 1 }),
      new TextRun({ text: "Executed at " }),
      new TextRun({ text: "[city], Oregon." }),
      new TextRun({ break: 3 }),
      new TextRun({ text: "______________________________________" }),
      new TextRun({ break: 1 }),
      new TextRun({ text: name, bold: true }),
      new TextRun({ break: 1 }),
      new TextRun({ text: role }),
      new TextRun({ break: 1 }),
      new TextRun({ text: address }),
      new TextRun({ break: 1 }),
      new TextRun({ text: phone }),
      new TextRun({ break: 1 }),
      new TextRun({ text: email }),
    ],
  });
```

## Verification clause (declarations only)

```javascript
const verificationClause = new Paragraph({
  spacing: { before: 360 },
  children: [
    new TextRun({
      text: "I declare under penalty of perjury under the laws " +
            "of the State of Oregon that the foregoing is true " +
            "and correct.",
    }),
  ],
});
```

(Per ORCP 1 E; the longer "I hereby declare..." form is also
acceptable but ORCP 1 E is the cleanest.)

## Common pitfalls

1. **A4 default**. `docx-js` defaults to A4. Set page size
   explicitly to 12,240 × 15,840 DXA.
2. **Static page numbers**. Never type "Page 3 of 7" as literal
   text — Word can't update it. Use `PageNumber.CURRENT` and
   `PageNumber.TOTAL_PAGES`.
3. **Missing leading space**. The 3-inch top margin on page 1 is
   achieved by leaving the section's top margin at 1 inch and
   adding 2 inches of leading paragraph space at the start of the
   body. Without it, page 1 will look identical to page 2 and
   bleed into the clerk's stamp zone.
4. **Color**. Don't use `color: "0000FF"` for hyperlinks or
   `highlight: "yellow"` for emphasis — UTCR 2.010 forbids both
   in the body. Use bold and italic instead.
5. **Unicode bullets**. Use the docx numbering config
   (`LevelFormat.BULLET`) rather than typing `•` or `*` — Word
   handles them differently across systems.
6. **Tab stops not set**. The right-aligned page counter requires
   an explicit tab stop at 9,360 DXA. Without it, "Page X of Y"
   falls in the middle of the footer.

## Verification

After generation, run:

```bash
python3 plugins/or-court-docs/scripts/format-check.py path/to/draft.docx
```

It will validate paper size, margins, fonts, color, line spacing,
and the footer fields. Address every FAIL before saving as PDF and
uploading.
