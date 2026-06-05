# Integration — End-to-end Arkansas debt-defense answer

## Prompt

I have 12 days left to answer a debt-buyer complaint filed against me in Pulaski
County Circuit Court in Arkansas. Walk me through it and draft my answer.

## Expected triggers

- `ar-first-30-days`
- `ar-consumer-debt`
- `ar-draft-motion` or `ar-statewide-format`
- `ar-deadlines`

## Acceptance criteria

- [ ] Confirms/computes the answer deadline (Ark. R. Civ. P. 12(a) + Rule 6) and
      reads the day count from references
- [ ] Produces a captioned **Answer** under Ark. R. Civ. P. 10 with numbered
      paragraph-by-paragraph responses and a Rule 11 signature (Pro Se) + Rule 5
      certificate of service
- [ ] Pleads relevant affirmative defenses — statute of limitations (written vs.
      open-account), failure of chain of title, and the collection-agency
      licensing/capacity challenge
- [ ] Reflects Arkansas fact-pleading and does not invent a mini-FDCPA statute

## Common failure modes

- Misses an available affirmative defense; hard-codes the SOL years or the
  answer deadline
