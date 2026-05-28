# wa-consumer-debt — CPA five elements (debt context)

## Prompt

A debt buyer sued me in Washington. They re-aged my debt with
the credit bureaus and threatened to sue on a debt that was
clearly time-barred. Can I counterclaim under the WA Consumer
Protection Act?

## Expected triggers

- `wa-consumer-debt`

## Acceptance criteria

- [ ] Identifies the WA CPA at RCW 19.86
- [ ] Walks the **Hangman Ridge 5-element test** per
      *Hangman Ridge Training Stables v. Safeco Title Ins. Co.*,
      105 Wn.2d 778 (1986):
      1. Unfair or deceptive act or practice (re-aging + time-
         barred threat both qualify)
      2. Occurring in trade or commerce (debt collection is
         trade)
      3. Public-interest impact (per-se pathway available via
         RCW 19.16 collection-agency licensing violation)
      4. Injury to plaintiff's business or property
      5. Causation
- [ ] Notes the **per-se pathway via RCW 19.16** — a violation
      of the Collection Agency Act is per se unfair/deceptive
      under the CPA, bypassing the public-interest analysis
- [ ] Notes damages: actual damages + treble up to the
      statutory cap (current cap in
      `wa-law-references/references/wa-rcw-debt/RCW-19_86.md`)
      + mandatory attorney's fees + costs
- [ ] Notes CPA SOL (current day count in chapter file)

## Common failure modes

- Hard-coding the treble cap dollar figure
- Missing the per-se pathway via RCW 19.16
- Treating the public-interest element as fatal when the
  per-se pathway is available
- Confusing CPA SOL with general tort SOL
