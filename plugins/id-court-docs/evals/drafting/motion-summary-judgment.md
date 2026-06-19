# id-draft-motion — motion + memorandum (summary judgment)

## Prompt

Draft a motion for summary judgment and supporting memorandum for an
Idaho District Court case, with the notice of hearing and a proposed
order.

## Expected triggers

- `id-draft-motion`
- `id-statewide-format`

## Acceptance criteria

- [ ] Produces a **Motion for Summary Judgment** with a separate
      supporting **Memorandum** (Idaho uses "Memorandum" for the
      brief), citing **I.R.C.P. 56**
- [ ] Produces a **Notice of Hearing** (I.R.C.P. 7(b)(3)) and accounts
      for the summary-judgment service timing before the hearing —
      reading the day-counts from the corpus / `id-deadlines`
- [ ] Produces a **separate proposed order**, noting only the judge
      signs it
- [ ] Applies the I.R.C.P. 2 format via `id-statewide-format` (caption,
      line numbering, footer) and includes a certificate of service
- [ ] Supports the motion with an Affidavit or Declaration rather than
      unsworn argument

## Common failure modes

- Merges the memorandum into the motion with no separate brief
- Omits the Notice of Hearing or uses the wrong service window
- Drafts an order the movant signs
