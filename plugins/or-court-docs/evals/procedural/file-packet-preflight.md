# or-file-packet — Pre-filing packet check

## Prompt

I have my motion, declaration, exhibits, proposed order, and
notice of hearing ready. I'm in Multnomah, Case 25CV01234.
Can you preflight the packet before I file?

## Expected triggers

- `or-file-packet`
- Likely chains to `or-quality-check` and `or-fact-check`

## Acceptance criteria

### Packet components

- [ ] Motion + Memorandum
- [ ] Supporting Declaration
- [ ] Exhibits (numbered)
- [ ] Proposed Order
- [ ] Notice of Hearing
- [ ] Certificate of Service

### Cross-document checks

- [ ] Captions identical across all documents
- [ ] Case number `25CV01234` consistent
- [ ] Hearing date/time/mode consistent between motion,
      Notice of Hearing, and proposed order
- [ ] Party names spelled identically
- [ ] Document titles match what each document contains

### Multnomah-specific

- [ ] References Multnomah SLR 5.100 working-copy
      threshold (25 pages)
- [ ] References Multnomah SLR 5.015 Notice-of-Hearing
      timing (3 business days)
- [ ] Confirms hearing date was reserved with JA
- [ ] References File and Serve as the eFiling system

### Quality checks

- [ ] Recommends running `or-quality-check` (UTCR 2.010)
- [ ] Recommends running `or-fact-check` (citations)
- [ ] Confirms each document is in PDF format
- [ ] Confirms file size under 25 MB per document

## Common failure modes

- Treating each document separately rather than as a packet
- Missing the working-copy requirement for Multnomah > 25 pp
- Failing to cross-check hearing details across documents
- Suggesting paper filing (Oregon is eFile-only with
  exceptions)
