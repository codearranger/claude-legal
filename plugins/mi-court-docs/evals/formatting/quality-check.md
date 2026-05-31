# mi-quality-check — Pre-filing QC catching an MCR 2.111(F) affirmative-defense defect

## Prompt

Here's the answer I drafted to a Michigan complaint before I
file it. Can you do a pre-filing check and tell me if anything
is wrong with the format or content? I admitted some
paragraphs, denied others, and at the bottom I wrote one
sentence saying "the statute of limitations has run and they
don't own the debt."

## Expected triggers

- `mi-quality-check`
- `mi-statewide-format`
- `mi-first-30-days`

## Acceptance criteria

### Format pass (MCR 1.109 / MCR 2.113)

- [ ] Verifies caption, document title, and signature against
      **MCR 1.109** and **MCR 2.113** (cite the rules; read
      current specifics from the references corpus)
- [ ] Confirms the **MCR 1.109(E)** signature block is present
      and, for a self-represented filer, carries no P-number

### Content pass — the MCR 2.111(F) defect

- [ ] **Flags the affirmative-defense defect**: under
      **MCR 2.111(F)**, affirmative defenses (including statute
      of limitations and lack of standing / failure of a
      condition) must be **stated separately** in the responsive
      pleading or they may be **waived** — a one-sentence mention
      buried at the end of the answer is not adequate
- [ ] Recommends restating each affirmative defense in a
      separately captioned "Affirmative Defenses" section, each
      defense pleaded distinctly, citing MCR 2.111(F)
- [ ] Notes that the SOL defense in particular must be
      affirmatively pleaded to be preserved (cross-reference
      `mi-first-30-days`)

### Consistency

- [ ] Checks internal consistency (paragraph-by-paragraph
      admit/deny tracks the complaint's numbered allegations per
      MCR 2.111)

## Common failure modes

- Passes the answer as fine despite the buried, non-separated
  affirmative defenses
- Misses MCR 2.111(F) and the waiver risk
- Treats the SOL as something that can be raised any time
  without pleading it
- Focuses only on format and skips the content/waiver pass
