# oh-file-packet — Packet assembly + preflight

## Prompt

Assemble my motion-to-compel packet for Cuyahoga Common
Pleas e-filing. I have: the motion, the affidavit, three
exhibits (RFP served / meet-and-confer letter / no-
response receipt), and a proposed order.

## Expected triggers

- `oh-file-packet`
- `oh-cuya`
- `oh-statewide-format`

## Acceptance criteria

### Order of assembly

- [ ] Motion (lead document)
- [ ] Memorandum in support (if separate)
- [ ] Affidavit
- [ ] Exhibit cover pages + exhibits (numbered)
- [ ] Proposed order (typically separate document)
- [ ] Certificate of service

### Preflight

- [ ] Caption matches across all documents
- [ ] Case number consistent
- [ ] Page count under Cuyahoga local-rule cap (verify
      current cap)
- [ ] Signature block consistent across documents
- [ ] All exhibits referenced in body are actually
      attached
- [ ] No PII (SSN, account numbers beyond last 4)
- [ ] Civ. R. 5.2 redaction compliant

### E-filing

- [ ] References Cuyahoga e-filing portal conventions
- [ ] References filing-fee schedule

## Common failure modes

- Missing certificate of service
- Caption mismatch across documents
- Unredacted PII
- Exhibits referenced but not attached
- Proposed order missing or attached to wrong document
