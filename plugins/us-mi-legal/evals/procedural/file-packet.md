# mi-file-packet — Assembling a MiFILE packet with MCR 1.109(D)(9) PII redaction

## Prompt

I'm ready to e-file my Michigan documents through MiFILE. I
have my motion, an affidavit, and an exhibit that's a copy of a
billing statement with my full Social Security number and bank
account number on it. How do I put the packet together and is
there anything I need to do about the personal information on
that exhibit?

## Expected triggers

- `mi-file-packet`
- `mi-statewide-format`
- `mi-quality-check`

## Acceptance criteria

### MiFILE assembly

- [ ] Identifies **MiFILE / MiFILE (Tyler/Odyssey) e-filing** as
      Michigan's statewide e-filing system and walks the packet
      assembly: lead document + attachments/exhibits, correct
      document-type/category selection, and proof of service
      (read current MiFILE mechanics and any per-court overrides
      from the references corpus rather than asserting them)
- [ ] Confirms each document carries the MCR 1.109 / MCR 2.113
      caption and signature before submission (cross-reference
      `mi-quality-check`)

### PII redaction (MCR 1.109(D)(9))

- [ ] **Flags the MCR 1.109(D)(9) personal-identifying-
      information protection requirement**: protected PII (full
      Social Security number, financial-account numbers, etc.)
      must be **redacted / not included** in publicly filed
      documents — cite MCR 1.109(D)(9) and **read the current
      list of protected identifiers and the redaction/partial-
      display convention from the references corpus** rather than
      asserting them from memory
- [ ] Specifically directs redacting the SSN and bank-account
      number on the billing-statement exhibit (e.g., partial
      display per the rule) and notes any separate
      confidential-information / nonpublic-filing mechanism the
      rule provides
- [ ] Notes the filer — not the clerk — bears responsibility for
      redaction

### Preflight

- [ ] Recommends a preflight pass (titles, captions, signatures,
      redaction, service) before submission

## Common failure modes

- Files the exhibit with the SSN/account number unredacted
- Misses MCR 1.109(D)(9) entirely
- Asserts the protected-identifier list from memory rather than
  reading it from the corpus
- Assumes the clerk will redact PII for the filer
