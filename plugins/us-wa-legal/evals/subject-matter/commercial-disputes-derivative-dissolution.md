# wa-commercial-disputes — Derivative + judicial dissolution

## Prompt

I own 25% of a Washington corporation. The majority shareholder
has frozen me out of management, refuses to pay dividends, and
is paying himself an excessive salary that is depleting the
company. The other minority shareholder agrees with me. What
remedies are available?

## Expected triggers

- `wa-commercial-disputes`

## Acceptance criteria

- [ ] Identifies the WBCA at RCW 23B
- [ ] Walks the **derivative-action** framework under RCW
      23B.07.400 — plaintiff must be a contemporaneous
      shareholder; demand on board required unless excused
- [ ] Walks the **judicial-dissolution** framework under RCW
      23B.14 — court may dissolve on shareholder showing of
      illegality / oppression / fraud / waste of corporate
      assets
- [ ] References the **reasonable-expectations** test for
      oppression in close corporations per *Scott v.
      Trans-System, Inc.* (148 Wn.2d 701)
- [ ] Notes alternative remedies short of dissolution:
      buy-out at fair value; appointment of receiver;
      injunctive relief
- [ ] Notes director duties at RCW 23B.08 (duty of care +
      duty of loyalty + good faith) — relevant if directors
      are complicit in the freeze-out
- [ ] References `wa-law-references/references/wa-rcw-debt/`
      RCW-23B chapter files for current statutory text on
      derivative-action procedure, dissenters' rights, and
      dissolution

## Common failure modes

- Confusing derivative claims (corporate harm) with direct
  claims (shareholder-specific harm)
- Missing the reasonable-expectations test from *Scott v.
  Trans-System*
- Skipping the demand-on-board prerequisite
- Hard-coding specific procedural day counts for derivative
  actions rather than reading from chapter files
