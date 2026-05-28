---
name: {{ABBR}}-statewide-format
description: >
  This skill should be used when the user asks to "draft a
  pleading", "format a {{STATE_NAME}} court document",
  "apply {{FORMAT_RULE}}", "build a caption", "create a
  declaration", "format a motion", or "proposed order" for
  any {{STATE_NAME}} court. Covers {{FORMAT_RULE}} page
  formatting, caption structure, document titles, exhibit
  conventions, signature blocks, and citation format per the
  {{STYLE_MANUAL}}.
version: 0.1.0
---

# {{STATE_NAME}} Statewide Court Document Formatting

Use these rules whenever drafting a paper to be filed in a
{{STATE_NAME}} court. They derive from **{{FORMAT_RULE}}**
and common statewide drafting conventions.

> **NOT LEGAL ADVICE.** Generated content is a drafting aid;
> verify against current rules before filing.

## {{FORMAT_RULE}} format requirements (mandatory)

> **TODO**: Research and document the state's specific
> requirements for:

| Item | Rule |
|------|------|
| Paper size | TODO (typically US Letter 8½ × 11) |
| Sides | TODO (single-sided typical) |
| Top margin, page 1 | TODO |
| All other margins | TODO |
| Color | TODO |
| Font | TODO |
| Line spacing | TODO |
| Citations | Per the {{STYLE_MANUAL}} |
| eFiling | TODO (identify state's eFiling system) |

## Default typography

> **TODO**: Document the state's default typography
> conventions.

## Required footer

> **TODO**: Most states require some form of pagination on
> the footer. Document the state's convention. The plugin's
> footer convention (which `scripts/format-check.py`
> enforces) is:
> - **Left**: document title — case number
> - **Right**: "Page X of Y" using Word's PAGE / NUMPAGES
>   fields
> - **Font**: smaller than body (typically 10 pt)

## Caption structure

> **TODO**: Document the state's caption requirements:
> - Court-header text
> - Party-block format
> - Case-number format and placement
> - Document-title format and placement
> - Separator style (vertical rule, column layout, etc.)

```
[court header]
[parties left]              │  [case number right]
                            │
                            │  [document title]
[v. or vs.?]                │
                            │
                            │
```

## Required body elements

> **TODO**: Document the state's required body elements:
> - Salutation for declarations (state's penalty-of-perjury
>   clause)
> - Numbered-paragraph convention
> - Verification clause for declarations
> - Date / execution-place convention
> - Signature-block content

## Exhibits

> **TODO**: Document the state's exhibit convention:
> - **Numbered vs. lettered** (state-specific — OR uses
>   numbers, WA uses letters)
> - Exhibit list format
> - Cover-page format
> - Pagination continuity

## The four document templates

See the `references/templates/` directory:

- `declaration.md`
- `motion-with-memo.md`
- `notice-of-hearing.md` (or state-specific scheduling
  terminology — adjust accordingly)
- `proposed-order.md`

## Citation format ({{STYLE_MANUAL}})

> **TODO**: Document the state's citation form for:
> - State supreme court
> - State intermediate appellate court
> - Federal cases (state's variation from Bluebook)
> - State statutes ({{STATUTE_CODE}})
> - Court rules ({{CIVIL_RULES}}, {{EVIDENCE_RULES}})
> - Federal statutes (USC) and regulations (CFR)

**Distinctive {{STATE_NAME}} style choices**:

> **TODO**: Identify any conventions that differ from
> Bluebook (e.g., Oregon's no-period rule for Or, P3d, USC).

## Producing documents programmatically

For `.docx` generation, follow `references/docx-generation.md`.
Key points (state-agnostic, but verify):

- Set page size explicitly to US Letter
- Use the state's required font and size
- Build the footer with PAGE / NUMPAGES Word fields (not
  static text)
- Add leading paragraph space on page 1 if the state requires
  a larger top margin on page 1

For format validation, use the bundled
`scripts/format-check.py`.

## eFiling — {{STATE_NAME}}

> **TODO**: Document the state's eFiling system:
> - Portal URL
> - Document codes (state-specific)
> - File size limits
> - Format requirements (PDF only? .docx accepted?)

## Compose with court-specific skills

This skill is **always** layered with:

- `{{ABBR}}-{{PRIMARY_COURT_SLUG}}` — if the case is in
  {{PRIMARY_COURT_NAME}}
- `{{ABBR}}-{{SECONDARY_COURT_SLUG}}` — if in
  {{SECONDARY_COURT_NAME}}
- `{{ABBR}}-county-courts` — for any other county
- `{{ABBR}}-pro-se` — if the litigant is self-represented

## References

- `references/{{FORMAT_RULE_SLUG}}-full-text.md` — verbatim
  text of the format rule
- `references/caption-format.md` — caption structure with
  docx-js example
- `references/exhibit-handling.md` — exhibit conventions
- `references/docx-generation.md` — docx-js patterns
- `references/templates/` — the four document templates
