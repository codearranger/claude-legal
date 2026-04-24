# wa-file-packet — Packet preflight

## Prompt
I'm about to file my Motion to Compel packet in KCDC. Can you do a
final check before I submit?

## Expected triggers
- `wa-file-packet`
- `wa-quality-check`
- `wa-fact-check`

## Acceptance criteria
- Runs through a checklist:
  - Correct caption (court, division, cause number, parties)
  - **Cause number has a clerk-issued date** (KCDC requirement)
  - GR 14 formatting (margins, line spacing, font, 3" first-page top
    margin)
  - Page numbers, document title, footer
  - Signature block with pro se name, address, email, phone
  - Certificate of Service with correct parties and date
  - Note for Motion Docket with correct hearing date and routing
  - All exhibits referenced in the motion are present
  - Cross-references (Ex. A, Ex. B, etc.) match the actual exhibits
  - Fact-check summary on citations
  - CR 26(i) / CRLJ 26(f) certification included if motion to compel
- Identifies any deficiencies for correction before filing

## Common failure modes
- Missing clerk-issued date preflight
- Skipping exhibit cross-reference check
- Missing Certificate of Service verification
- Omitting CR 26(i) / CRLJ 26(f) certification check for compel
  motions
