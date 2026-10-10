# Integration — End-to-end Motion to Compel packet

## Prompt
I need a complete Motion to Compel packet for KCDC Burien. Plaintiff
served responses to my First Discovery on [date] that were deficient in
specific ways: [list]. We exchanged a meet-and-confer letter on [date]
and a phone call on [date], with no resolution. Hearing is set for
[date]. Draft the full packet: motion, declaration, note for motion
docket, proposed order, exhibit index, and certificate of service.

## Expected triggers
- `wa-draft-motion`
- `wa-draft-declaration`
- `wa-draft-note`
- `wa-draft-order`
- `wa-file-packet`
- `wa-statewide-format`
- `wa-kcdc`
- `wa-discovery`
- `wa-law-references`

## Acceptance criteria

Produces a **5-document packet** with internal consistency:

### Cross-document consistency
- Caption identical on every document (court, division, cause number
  with clerk date, parties)
- Party designations identical
- Judge / division identified consistently (BU2, Laumann, Burien)
- Hearing date / time / location consistent
- Exhibit letters consistent across motion, declaration, index

### Motion to Compel
- Correctly cites **CRLJ 37** (not CR 37)
- Correctly cites **CRLJ 26(f)** conference requirement
- Contains **CRLJ 26(f) Certification** with dates of meet-and-confer
  efforts (letter date, call date, outcome)
- Request-by-request analysis of each deficient response
- Prayer for relief includes costs / fees

### Declaration
- Establishes personal knowledge
- Facts only — no argument
- Each exhibit referenced as "A true and correct copy of [document]
  is attached hereto as Exhibit [letter]"
- RCW 9A.72.085 penalty-of-perjury language

### Note for Motion Docket
- Correct hearing date, time, division, judge
- CivilMGT routing address
- Signature block

### Proposed Order
- [PROPOSED] bracket in title
- Ordered clauses: produce within 14 days, costs, escalation language
  under CRLJ 37(b)
- Signature line for judge

### Exhibit Index / Certificate of Service
- Exhibit index lists all exhibits with descriptions
- Certificate of service identifies date, method, and recipient(s)

### Format
- GR 14 compliant across all documents (1" margins, 3" first-page
  top, 12pt, double-spaced, line numbers)
- Page numbers and document-title footers
- No color markings, no placeholder strings

## Common failure modes
- Inconsistent caption or exhibit letters between documents
- Wrong rule citations (CR instead of CRLJ)
- Missing CRLJ 26(f) certification
- Missing escalation language in Proposed Order
- Missing certificate of service on any document
- Missing [PROPOSED] bracket in order title
