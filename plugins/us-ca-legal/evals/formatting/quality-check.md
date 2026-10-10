# ca-quality-check — Pre-filing QC

## Prompt

I have a motion to compel I'm about to file in LASC. Can you do a
quality check on it before I file?

## Expected triggers

- `ca-quality-check`
- `ca-statewide-format`
- `ca-fact-check`

## Acceptance criteria

### Pass 1 (format)

- [ ] Paper size (Letter) — CRC 2.104
- [ ] Margins (1") — CRC 2.107
- [ ] Font (12pt+, essentially equivalent to Courier/TNR/Arial)
      — CRC 2.105
- [ ] Line spacing (1.5 or double) — CRC 2.108(a)
- [ ] Line numbers in left margin — CRC 2.108(b)
- [ ] Footer with title + page number — CRC 2.110
- [ ] Black ink only — CRC 2.103

### Pass 2 (content)

- [ ] Caption matches case name and number
- [ ] Document title accurate
- [ ] Signature block (pro per or counsel-of-record + bar #)
- [ ] Proof of Service attached
- [ ] Notice of Motion is a separate document from the
      Memorandum
- [ ] Separate Statement attached if motion to compel further
      (CRC 3.1345)
- [ ] Meet-and-confer declaration if required (demurrer / motion
      to strike / motion to compel discovery)
- [ ] 16-court-day notice met (CCP § 1005(b))
- [ ] 45-day deadline preserved if motion to compel further
- [ ] Judicial Council form versions current (verify date)

### Output format

- [ ] Pass/fail summary by category
- [ ] Specific items to fix listed
- [ ] References to operative rules

## Common failure modes

- Skipping separate-statement check (CRC 3.1345)
- Missing the 45-day jurisdictional check on compel-further
- Importing Oregon's UTCR 2.010 fields instead of CRC
- Reporting "blue-black acceptable" — CA is stricter
- Forgetting to verify form-version currency (Judicial Council
  revises forms periodically)
