# wa-quality-check — Pre-filing QA sweep

## Prompt
I finished my motion packet. Do a quality check before I file.

## Expected triggers
- `wa-quality-check`
- `wa-fact-check`

## Acceptance criteria
- Caption consistency across all documents in packet (Motion,
  Declaration, Note, Proposed Order)
- Cause number with clerk date is identical on every document
- Party names and designations match on every document
- Cross-references (Ex. A-F) match actual exhibits attached
- Page numbers and footers present
- GR 14 compliance (margins, font, spacing, line numbers)
- Signature block on every signed document
- Certificate of Service on motion, declaration, and note
- No color markings, track changes, or comments left in
- Spelling and grammar
- **No stale facts** (dates match the evidence; party names correctly
  spelled throughout)
- **Exhibit index** matches exhibits attached
- Document-title footer reflects the correct title

## Common failure modes
- Stale dates after revision
- Mismatched exhibit letters between motion and declaration
- Track changes or "[PLACEHOLDER]" strings left in
- Page numbers that skip or restart incorrectly
- Missing Certificate of Service on one of the documents
