# mi-law-references — Locating an MCR civil rule

## Prompt

I keep seeing people cite "the MCR" for Michigan procedure. I
need the rule that governs how and when I have to respond to a
request for production of documents. Where do I find it and
what does it actually say?

## Expected triggers

- `mi-law-references`
- `mi-discovery`

## Acceptance criteria

### Locating the corpus

- [ ] Identifies that the **Michigan Court Rules (MCR)** are the
      canonical procedural source and points to the
      `court-rules/` corpus under `mi-law-references` references
      as the place to read verbatim rule text
- [ ] Identifies the correct rule for document requests in the
      **MCR 2.300-series discovery rules** (production of
      documents is in **MCR 2.310**) and notes timing/response
      mechanics live in that rule — **read the current response
      window and contents from the references corpus** rather
      than asserting day counts from memory

### Reading vs. asserting

- [ ] Quotes/paraphrases the rule from the corpus rather than
      reciting it from memory, and gives the citation by **rule
      number** (e.g., MCR 2.310)
- [ ] Cross-references the broader discovery framework
      (MCR 2.301 scope/timing, MCR 2.302 general provisions and
      required disclosures) via `mi-discovery`

### Navigation help

- [ ] Explains the MCR numbering convention (Chapter 1 general,
      Chapter 2 civil procedure, Chapter 4 district-court /
      special proceedings, etc.) so the litigant can find related
      rules
- [ ] Points to `online-sources.md` / `legal-data-apis.md` for
      the canonical public URL of the MCR

## Common failure modes

- Cites a federal discovery rule (FRCP 34) instead of MCR 2.310
- Recites a response deadline from memory instead of reading the
  corpus
- Can't locate the rule within the MCR numbering scheme
- Confuses the MCR with the (substantive) MCL statutes
