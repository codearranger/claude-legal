# tx-draft-declaration — unsworn declaration (CPRC § 132.001)

## Prompt

I need to swear to the facts supporting my motion but I can't get to a
notary. Can I do an unsworn declaration in Texas, and draft one for me.

## Expected triggers

- `tx-draft-declaration`

## Acceptance criteria

### Right instrument

- [ ] Explains that **Tex. Civ. Prac. & Rem. Code § 132.001** lets an
      **unsworn declaration** substitute for a written sworn
      declaration, verification, certification, oath, or affidavit — so
      no notary is required
- [ ] Notes the limited statutory exceptions where § 132.001 does NOT
      apply (e.g., certain instruments concerning real property,
      oaths of office) and routes the user to confirm the current
      exclusions against `../tx-law-references/references/tx-statutes-debt/`

### The jurat (load-bearing)

- [ ] Ends with the statutory **penalty-of-perjury jurat** in the
      § 132.001 form: a statement that the declarant declares under
      penalty of perjury that the foregoing is **true and correct**,
      executed on a stated date
- [ ] Includes the declarant's **date and place of birth** (the
      § 132.001 jurat requires this), reading the exact required jurat
      elements from the corpus rather than inventing a generic
      "subscribed and sworn" notary block
- [ ] Does **not** include a notary acknowledgment / seal block (that
      would defeat the point of an unsworn declaration)

### Form

- [ ] Numbered factual paragraphs, signed by the declarant, with the
      `tx-statewide-format` caption and footer

## Common failure modes

- Produces a notarized affidavit block instead of the § 132.001 jurat
- Omits the date/place of birth required by the statutory jurat
- Uses "under the laws of the United States" federal-28-U.S.C.-§-1746
  language instead of the Texas § 132.001 form
