# ar-consumer-debt — Statute of limitations split

## Prompt

How long is the statute of limitations on a credit-card debt in Arkansas?

## Expected triggers

- `ar-consumer-debt`

## Acceptance criteria

- [ ] Distinguishes the **written-contract** SOL (§ 16-56-111) from the
      **oral/open-account** SOL (§ 16-56-105) and explains which theory a card
      debt may fall under
- [ ] Reads the exact year counts from the references corpus rather than asserting
      them from memory
- [ ] Notes a time-barred suit as an affirmative defense / FDCPA concern

## Common failure modes

- States a single flat SOL without the written-vs-open-account distinction
