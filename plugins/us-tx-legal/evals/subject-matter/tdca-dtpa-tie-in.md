# tx-consumer-debt — TDCA violation as a DTPA tie-in claim

## Prompt

A Texas debt collector kept calling my workplace after I told them to
stop and threatened to garnish my wages, which I know they can't do.
Can I sue them in Texas, and is there extra leverage I should know
about before I file?

## Expected triggers

- `tx-consumer-debt`

## Acceptance criteria

### TDCA claim

- [ ] Identifies the conduct as a potential violation of the **Texas
      Debt Collection Act, Tex. Fin. Code Ch. 392** (prohibited conduct
      §§ 392.301–.306, e.g., threats of action that cannot legally be
      taken), and points to **§ 392.403** remedies (actual damages,
      injunction, attorney fees) — reading the specific subsections
      from `../tx-law-references/references/tx-statutes-debt/`

### DTPA tie-in (the leverage)

- [ ] Explains the **§ 392.404 tie-in**: a TDCA violation is a
      **deceptive trade practice actionable under the DTPA** (Bus. &
      Com. Code Ch. 17), opening **§ 17.50** remedies including
      **treble / additional damages** for a knowing or intentional
      violation (confirm the multiplier against the corpus)

### 60-day pre-suit notice (a gate)

- [ ] Flags the **DTPA § 17.505 60-day pre-suit written notice**
      requirement (stating the complaint and amount of economic /
      mental-anguish damages and expenses) as a prerequisite before
      filing, and the **§ 17.565 2-year DTPA limitations** period —
      reading exact day/period figures from the corpus
- [ ] Notes the federal FDCPA overlay lives in the shared
      `federal-debt-laws/` corpus and cross-references it rather than
      duplicating it

## Common failure modes

- Pleads only the TDCA and misses the § 392.404 DTPA tie-in
- Files without the § 17.505 60-day notice
- Hard-codes the treble-damages multiplier or the notice period
