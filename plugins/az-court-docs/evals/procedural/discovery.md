# az-discovery — Rule 26.1 mandatory disclosure + Rule 26.2 tier + Rule 37 motion to compel

## Prompt

I'm defending a debt case in Arizona Superior Court. The plaintiff
hasn't given me any documents proving they own the account. What is
each side automatically required to disclose, how much discovery
am I allowed, and what do I do if they refuse to produce the
assignment paperwork?

## Expected triggers

- `az-discovery`
- `az-consumer-debt`

## Acceptance criteria

### Mandatory disclosure (Rule 26.1)

- [ ] Identifies **Ariz. R. Civ. P. 26.1** mandatory initial
      disclosure as Arizona's distinctive feature — each side must
      disclose witnesses, documents, and the factual/legal bases of
      claims and defenses **without waiting for a request** — and
      reads the current scope and timing from the references corpus
      rather than asserting them
- [ ] Frames the debt buyer's Rule 26.1 obligation to disclose the
      assignment chain and account records (cross-reference
      `az-consumer-debt`)

### Discovery tiers (Rule 26.2)

- [ ] Identifies the **Ariz. R. Civ. P. 26.2 tiered** discovery
      system — the assigned tier (based on amount in controversy /
      complexity) sets discovery limits (deposition hours,
      interrogatory counts, time to complete) — and reads the
      tier definitions and limits from the corpus rather than
      asserting the numbers

### Motion to compel (Rule 37)

- [ ] Identifies **Ariz. R. Civ. P. 37** as the route to compel,
      and the **meet-and-confer / good-faith-consultation**
      prerequisite before moving — read the current certification
      requirement and timing from the corpus
- [ ] Notes the availability of sanctions / fee-shifting for
      unjustified non-disclosure (read from the corpus)

## Common failure modes

- Misses Rule 26.1 mandatory disclosure (treating Arizona like a
  request-only discovery state)
- Asserts the tier limits or interrogatory/deposition caps from
  memory
- Skips the meet-and-confer prerequisite before a Rule 37 motion
