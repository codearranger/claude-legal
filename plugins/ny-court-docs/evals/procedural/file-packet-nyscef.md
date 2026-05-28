# ny-file-packet — NYSCEF assembly + preflight

## Prompt

I have a Notice of Motion, supporting affirmation, and three
exhibits ready for filing in NY County Supreme Court. Walk me
through filing them via NYSCEF.

## Expected triggers

- `ny-file-packet`
- `ny-statewide-format`
- `ny-nyco`

## Acceptance criteria

- [ ] Walks through NYSCEF login and case lookup by Index No.
- [ ] Identifies the correct **document type** for each piece
      (Notice of Motion, Affirmation/Affidavit in Support,
      Exhibit A/B/C)
- [ ] Cites the **22 NYCRR § 202.5-b / § 202.5-bb** e-filing
      rules
- [ ] PDF-only requirement for documents
- [ ] Hyperlinks-must-be-functional rule for cited case law
- [ ] Confidentiality redaction reminders (Soc. Sec. #,
      financial-account # — CPLR 3019 / 4514 + 22 NYCRR
      § 202.5(e))
- [ ] References the post-filing **Confirmation of Service**
      step

## Common failure modes

- Forgets to redact PII before upload
- Treats exhibits as one combined PDF instead of separate
  document codes
- Suggests filing via UCMS (NYC Civil Court e-filing) for a
  Supreme Court case
