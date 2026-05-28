# wa-consumer-debt — Fees recovery

## Prompt

I'm defending a Washington consumer-debt case. I want to plead
counterclaims that can recover my attorney fees if I prevail.
What fee-shifting grounds are available?

## Expected triggers

- `wa-consumer-debt`
- `wa-law-references`

## Acceptance criteria

- [ ] Walks the **debt-specific fee-shifting** grounds in this
      order:
      - **FDCPA** § 1692k: mandatory attorney fees + costs for
        prevailing consumer
      - **WA CPA** RCW 19.86: mandatory attorney fees + costs for
        prevailing plaintiff/counterclaim plaintiff; treble
        damages up to the statutory cap (current cap in
        `wa-law-references/references/wa-rcw-debt/RCW-19_86.md`)
      - **WA Collection Agency Act** RCW 19.16: per-se WA CPA
        pathway for licensing / collection-conduct violations
      - **FDCPA + WA CPA together** can be pleaded; recovery
        from each is independent
- [ ] References `wa-consumer-debt/references/fees-consumer-
      debt.md` for the debt-specific consolidated framework
- [ ] References `wa-law-references/references/fees-and-costs.md`
      for the general RCW 4.84 cost-shifting framework
- [ ] Notes the **prayer for relief** must include a fee request
      — unclaimed fees may be waived

## Common failure modes

- Missing the WA CPA per-se pathway via RCW 19.16
- Hard-coding specific dollar figures for the treble cap rather
  than referring to the chapter file
- Forgetting to include the fee request in the prayer for relief
