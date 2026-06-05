# ar-draft-motion — Motion + brief with the Arkansas SJ standard

## Prompt

I'm in Pulaski County Circuit Court in Arkansas and need to draft a motion
for summary judgment with a supporting brief. Set it up for me.

## Expected triggers

- `ar-draft-motion`
- `ar-statewide-format`

## Acceptance criteria

- [ ] Produces a captioned motion under **Ark. R. Civ. P. 10** (court/county
      caption, numbered paragraphs) with a separate supporting brief
- [ ] Applies the **Rule 11** signature block with the Arkansas Bar Number
      (or "Pro Se" if self-represented) and a **Rule 5** certificate of service
- [ ] States the Arkansas summary-judgment standard — once the movant makes a
      prima facie showing, the non-movant must **"meet proof with proof"** and
      show a genuine issue of material fact (*Wallace v. Broyles* / *Flentje*)
- [ ] Applies line-numbered pleading paper and a "Page X of Y" footer by default
- [ ] Reads the SJ response window from the references corpus rather than
      asserting a fixed day count from memory

## Common failure modes

- Imports another state's caption or motion vocabulary
- Hard-codes the response deadline instead of pointing to references
