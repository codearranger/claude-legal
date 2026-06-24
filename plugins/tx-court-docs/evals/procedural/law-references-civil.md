# tx-law-references — mapping TRCP rules to the corpus

## Prompt

I'm defending a Texas civil collection suit. Which Texas rules govern
the answer deadline, no-evidence summary judgment, suit on a sworn
account, and the discovery plan — and where do I find them?

## Expected triggers

- `tx-law-references`

## Acceptance criteria

### Correct rule mapping

- [ ] Maps the **answer deadline** to **TRCP 99** (the "Monday rule")
      for district/county court, and notes the **TRCP 502.5** 14-day
      answer for justice court
- [ ] Maps **no-evidence summary judgment** to **TRCP 166a(i)** and
      traditional summary judgment to **166a(c)**
- [ ] Maps **suit on a sworn account** to **TRCP 185**, paired with the
      mandatory **verified denial under TRCP 93(10)**
- [ ] Maps **discovery control plans** to **TRCP 190** (Levels 1/2/3)
      and **expedited actions** to **TRCP 169**

### Sourcing

- [ ] Points to the verbatim rule text in
      `../tx-law-references/references/court-rules/` and the
      civil-practice map in `references/civil-rules.md`, rather than
      reciting full rule text from memory
- [ ] Reads any drift-prone figure (justice-court ceiling, expedited-
      action ceiling, interrogatory cap) from the corpus

## Common failure modes

- Cites a flat 20-day answer instead of the TRCP 99 Monday rule
- Misses the TRCP 185 / 93 sworn-account ↔ verified-denial pairing
- Attributes summary judgment to "Rule 56"
