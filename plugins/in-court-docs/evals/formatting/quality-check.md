# in-quality-check — Pre-filing format and content QC

## Prompt

I drafted a motion and supporting memorandum to file in
Allen Superior Court. Can you run a format check on it
before I submit it? I want to catch anything that would
get it bounced by the clerk or that the judge would note
as defective.

## Expected triggers

- `in-quality-check`
- `in-fact-check`
- `in-statewide-format`

## Acceptance criteria

### Format pass — T.R. 5(E)

- [ ] Checks that the document satisfies T.R. 5(E)
      requirements: reads current margin, font-size, and
      spacing specs from the references corpus rather than
      asserting fixed numbers from memory
- [ ] Checks the **2-inch top margin on page 1** (Odyssey
      clerk-stamp clearance) and 1-inch margins elsewhere
- [ ] Verifies the **footer** is present on every page
      (document short title + page X of Y per the Marion /
      statewide convention — reads the footer requirement
      from `in-statewide-format` rather than asserting
      specific local rule numbers from memory)

### Caption and structure pass — T.R. 10

- [ ] Checks the caption for T.R. 10(A) compliance: court
      ID line / county line / parties / cause number /
      document title
- [ ] Checks for **numbered paragraphs** per T.R. 10(B)
      in the body of any pleading or factual motion
- [ ] Verifies the signature block is correctly formatted
      per T.R. 11(A) — pro se (no bar number) or counsel
      (Attorney Number required)

### Citation pass — fact-check hook

- [ ] Cross-invokes `in-fact-check` to verify every
      cited Indiana rule number (T.R. XX, IC XX-XX-XX-X),
      case citation (NE3d reporter + court + year), and
      statutory reference against the references corpus
      or a structured source
- [ ] Flags any citation asserted only from memory and
      marks it for verification before filing

### Service and packet completeness

- [ ] Confirms a Certificate of Service is present at the
      end of every non-initial filing (T.R. 5(B))
- [ ] For Marion County filings, checks that a proposed
      order is included per local practice

## Common failure modes

- Asserts specific margin/spacing values from memory
  instead of reading from the corpus
- Runs only a format check and skips the citation
  verification pass
- Fails to flag the 2-inch page-1 top-margin requirement
  (the most common Odyssey rejection reason)
- Omits the Certificate of Service check
