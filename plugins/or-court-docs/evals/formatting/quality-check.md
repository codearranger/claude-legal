# or-quality-check — Pre-filing format and content QC

## Prompt

I just finished drafting a motion to compel for my Multnomah
case. Can you run a compliance check on it before I file?
The file is at ./motion-to-compel.docx

## Expected triggers

- `or-quality-check`
- Possibly `or-fact-check` (depending on prompt)

## Acceptance criteria

### Format pass (Pass 1)

- [ ] Mentions running `scripts/format-check.py` on the file
- [ ] Identifies what is being checked (paper size,
      margins, fonts, color, spacing, footer)
- [ ] References UTCR 2.010 as the authority

### Content pass (Pass 2)

- [ ] Checks caption (court header, case number, parties,
      "v." not "vs.")
- [ ] Checks Parker framework sections (I–VII)
- [ ] Checks citation format (Oregon Style Manual — no
      periods)
- [ ] Checks pro se signature block (no OSB#)
- [ ] Checks for Washington-style errors (RCW, CR/CRLJ, KCDC)
- [ ] Checks UTCR 2.120 confidential-information redaction
- [ ] Checks Multnomah SLR 5.045 meet-and-confer certification

### Output format

- [ ] Returns a structured pass/warn/fail report
- [ ] Identifies each issue specifically
- [ ] Suggests fixes

## Common failure modes

- Running only the format script without the content check
- Missing the Multnomah SLR 5.045 meet-and-confer
  requirement
- Failing to flag Washington-imported patterns ("vs.",
  lettered exhibits, "Wn.2d")
