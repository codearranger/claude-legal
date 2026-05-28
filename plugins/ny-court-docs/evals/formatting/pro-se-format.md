# ny-pro-se — Pro se drafting framework

## Prompt

I'm representing myself in NY County Supreme Court. What
should my signature block look like and how should I sign my
papers?

## Expected triggers

- `ny-pro-se`
- `ny-statewide-format`

## Acceptance criteria

- [ ] Identifies the user as "Self-Represented" / "Pro Se"
- [ ] Signature block format with name, address, phone,
      email; explicitly **omits** OCA attorney bar number
      and NY Attorney Registration #
- [ ] Recommends the **post-2023 CPLR 2106 universal
      affirmation** as the simpler alternative to a CPLR 2309
      notarized affidavit (pro se can now affirm under
      penalty of perjury without a notary)
- [ ] References CLARO clinics (Civil Legal Advice and
      Resource Office) and NYC Right-to-Counsel under Local
      Law 136 where applicable
- [ ] Encourages neutral, professional tone in filings — no
      ALL-CAPS shouting, no emotional language

## Common failure modes

- Recommends a CPLR 2309 affidavit with notary instead of
  the CPLR 2106 affirmation
- Includes a placeholder for a bar number in the signature
  block
- Recommends informal / first-person colloquial tone
