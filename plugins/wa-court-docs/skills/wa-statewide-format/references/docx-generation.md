# docx-js Generation Patterns for WA Pleadings

Reference patterns for producing GR 14-compliant Washington court documents
with the `docx` npm package.

## Install

```bash
npm install docx
```

## Skeleton

```javascript
const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, ImageRun,
  Header, Footer, AlignmentType, PageNumber,
  Table, TableRow, TableCell, WidthType, BorderStyle,
  TabStopType, VerticalAlign,
} = require('docx');

const TNR = "Times New Roman";
const SIZE_12 = 24;  // half-points
const SIZE_10 = 20;

const doc = new Document({
  creator: "[Filer name]",
  title: "Document Title",
  styles: {
    default: {
      document: {
        run: { font: TNR, size: SIZE_12 },
        paragraph: { spacing: { line: 360, lineRule: "auto" } },
      },
    },
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },    // US Letter
        margin: {
          top: 1440, right: 1440, bottom: 1440, left: 1440,
          footer: 720, header: 720, gutter: 0,
        },
      },
    },
    footers: { default: buildFooter() },
    children: buildBody(),
  }],
});

Packer.toBuffer(doc).then(buf => fs.writeFileSync("out.docx", buf));
```

## Three-inch top margin on page 1

docx-js doesn't support a different first-page margin directly. The
clean workaround is to add ~2 inches of leading space on the first
paragraph:

```javascript
new Paragraph({
  spacing: { before: 2880, line: 240, lineRule: "auto", after: 0 },  // 2 inches
  children: [new TextRun("")],
});
```

With a 1-inch section top margin, this yields an effective 3-inch top
margin on page 1 and a 1-inch top margin on all subsequent pages — exactly
what GR 14 requires.

## Required footer: title left, "Page X of Y" right

**Every generated document must include this footer.** It is validated by
`scripts/format-check.py` and a missing or incomplete footer FAILs the check.

```javascript
function buildFooter() {
  return new Footer({
    children: [new Paragraph({
      tabStops: [{ type: TabStopType.RIGHT, position: 9360 }],
      spacing: { line: 240, lineRule: "auto", after: 0 },
      children: [
        new TextRun({ text: FOOTER_TITLE, font: TNR, size: SIZE_10 }),
        new TextRun({ text: "\t", font: TNR, size: SIZE_10 }),
        new TextRun({ text: "Page ", font: TNR, size: SIZE_10 }),
        new TextRun({ children: [PageNumber.CURRENT], font: TNR, size: SIZE_10 }),
        new TextRun({ text: " of ", font: TNR, size: SIZE_10 }),
        new TextRun({ children: [PageNumber.TOTAL_PAGES], font: TNR, size: SIZE_10 }),
      ],
    })],
  });
}
```

Requirements:

- `FOOTER_TITLE` is a single-line identifier such as
  `"Motion to Compel — Case No. 25CIV######KCX"`. It must be non-empty and
  must not consist only of the word "Page" or "of".
- Both `PageNumber.CURRENT` (renders as a `PAGE` field) and
  `PageNumber.TOTAL_PAGES` (renders as `NUMPAGES`) must be present — use
  "Page X of Y", not "Page X" alone.
- Pass the footer via `section.footers.default` so it applies to every
  page including exhibit pages. Do not restart pagination after the
  signature block.

## Numbered paragraphs with hanging indent

```javascript
function numPara(num, leadIn, rest) {
  const runs = [new TextRun({ text: `${num}.\t`, bold: true, font: TNR, size: SIZE_12 })];
  if (leadIn) runs.push(new TextRun({ text: leadIn, bold: true, font: TNR, size: SIZE_12 }));
  if (rest) runs.push(new TextRun({ text: rest, font: TNR, size: SIZE_12 }));
  return new Paragraph({
    spacing: { line: 360, lineRule: "auto", after: 240 },
    tabStops: [{ type: TabStopType.LEFT, position: 720 }],
    indent: { left: 720, hanging: 720 },
    children: runs,
  });
}
```

Use `numPara(3, "Court Hearing of March 9, 2026. ", "On March 9, 2026, I attended...")`
for bold-lead-in-style paragraphs.

## Bullet sub-lines under a paragraph

Use a numbering config rather than unicode bullet characters:

```javascript
new Document({
  numbering: {
    config: [{
      reference: "bullets",
      levels: [{
        level: 0,
        format: LevelFormat.BULLET,
        text: "\u2022",
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 1440, hanging: 360 } } },
      }],
    }],
  },
  // ...
});

new Paragraph({
  numbering: { reference: "bullets", level: 0 },
  children: [new TextRun("10:10 AM — 117 BPM")],
});
```

## Images

```javascript
new Paragraph({
  alignment: AlignmentType.CENTER,
  children: [new ImageRun({
    type: "png",    // REQUIRED
    data: fs.readFileSync(imgPath),
    transformation: { width: 280, height: 607 },
    altText: { title, description, name },   // all three required
  })],
});
```

## Common pitfalls

- **Default page size is A4** — always set US Letter explicitly
- **`\n` does not create paragraphs** — use separate `Paragraph` objects
- **`PageBreak` must be inside a `Paragraph`** — not a standalone element
- **Tables require both `columnWidths` and cell `width`** with matching DXA
  values — otherwise tables render wrong in Google Docs
- **Use `WidthType.DXA`, not `PERCENTAGE`** — percentage breaks in Google Docs
- **Use `ShadingType.CLEAR`, not `SOLID`** — SOLID produces black backgrounds
- **Never insert unicode bullet characters directly** — always use
  `LevelFormat.BULLET` with a numbering config

## Validation

After generating:

```bash
python scripts/office/validate.py out.docx
```

And run the bundled GR 14 check:

```bash
python scripts/format-check.py out.docx
```
