# Integration — end-to-end Idaho debt-defense answer

## Prompt

I was served last week with a complaint in Ada County, Idaho. A debt
buyer is suing me for $3,800 on an old credit card. I want to file an
answer that protects all my defenses. Walk me through it and draft the
answer.

## Expected triggers

- `id-first-30-days`
- `id-consumer-debt`
- `id-ada`
- `id-statewide-format`

## Acceptance criteria

### Procedure

- [ ] States the **21-day** answer deadline (I.R.C.P. 12(a)(1)(A)) and
      computes it via I.R.C.P. 2.2 (`id-deadlines`)
- [ ] Identifies the venue as the **District Court of the Fourth
      Judicial District, Ada County**, and routes by amount in
      controversy between the Magistrate Division and District Court
      (reading the current line from the corpus)

### Substance preserved in the answer

- [ ] Pleads the **statute-of-limitations** defense and **standing /
      chain-of-title** challenge as affirmative defenses (I.R.C.P. 8(c))
- [ ] Raises the **Idaho Collection Agency Act** licensing / capacity
      issue and the Idaho Consumer Protection Act / FDCPA overlay where
      supported — reading provisions from the corpus
- [ ] Avoids admitting the debt or its amount; responds to each
      numbered paragraph

### Form

- [ ] Applies the I.R.C.P. 2 caption/format (line numbering, footer)
      and includes a certificate of service
- [ ] Self-represented signature block (no Idaho State Bar number)

## Common failure modes

- Misses the 21-day window or uses Rule 6 for the count
- Omits an affirmative defense, waiving it
- Recites Idaho statute subsections / dollar figures from memory
