# ar-district-courts — District Court forum and de novo appeal

## Prompt

I was sued for a small debt in an Arkansas District Court. If I lose, can I appeal?

## Expected triggers

- `ar-district-courts`

## Acceptance criteria

- [ ] Identifies District Court as the limited-jurisdiction forum (civil cap +
      small-claims division — read the dollar caps from references)
- [ ] Explains the **30-day de novo appeal to Circuit Court** (Arkansas District
      Court Rules)
- [ ] Notes it is the dominant consumer-debt + eviction forum and composes with
      `ar-consumer-debt` / `ar-landlord-tenant`

## Common failure modes

- Describes the appeal as on-the-record rather than de novo; hard-codes the cap
