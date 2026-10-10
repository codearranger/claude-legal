# mi-commercial-disputes — Michigan Business Court (MCL 600.8031) trade-secret / MUTSA matter

## Prompt

I co-own a small Michigan manufacturing company. A former
operations manager left and took our confidential supplier list
and pricing formulas to a competitor. I want to sue to stop him
from using them. Which Michigan court handles this kind of
business case, and what claim do I bring for the stolen trade
secrets?

## Expected triggers

- `mi-commercial-disputes`
- `mi-circuit-courts`

## Acceptance criteria

### Business Court assignment (MCL 600.8031)

- [ ] Identifies the **Michigan Business Court** as a specialized
      docket within the **Circuit Court** and cites
      **MCL 600.8031** for the business-court framework / what
      qualifies as a "business or commercial dispute" — **reading
      the current statutory definition and assignment/threshold
      criteria from `mi-statutes-debt/` (Michigan commercial
      corpus)** rather than asserting them from memory
- [ ] Notes that not every circuit has a Business Court and that
      assignment depends on the dispute meeting the statutory
      definition (read current specifics from the corpus);
      cross-references `mi-circuit-courts`

### The trade-secret claim (MUTSA)

- [ ] Identifies the **Michigan Uniform Trade Secrets Act
      (MUTSA)** as the governing claim and cites the controlling
      MCL provisions, **reading the definition of "trade secret,"
      the "misappropriation" elements, and available remedies
      from the corpus** rather than asserting them from memory
- [ ] Notes MUTSA's **displacement** of conflicting common-law
      tort theories for trade-secret misappropriation (read the
      preemption/displacement scope from the corpus)
- [ ] Identifies available relief — **injunctive relief**,
      damages (actual loss + unjust enrichment, or a reasonable
      royalty), and **exemplary damages / attorney fees for
      willful and malicious misappropriation** — reading the
      current remedy provisions and any multiplier from the
      corpus rather than asserting figures from memory

### Practice notes

- [ ] Flags the need to plead with sufficient specificity to
      identify the trade secrets and notes confidentiality /
      protective-order handling given PII/trade-secret content

## Common failure modes

- Sends the case to a generic civil docket without identifying
  the Business Court / MCL 600.8031 framework
- Recites MUTSA elements, remedies, or the exemplary-damages
  multiplier from memory rather than the corpus
- Misses MUTSA displacement of overlapping common-law claims
- Asserts every circuit has a Business Court
