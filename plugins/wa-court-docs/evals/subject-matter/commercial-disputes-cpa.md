# wa-commercial-disputes — Washington CPA Hangman Ridge test

## Prompt

A Washington vendor sold me a "new" piece of equipment that
turned out to be refurbished. They knew but didn't disclose.
I'm a contractor (not a consumer). Can I bring a Washington
CPA claim?

## Expected triggers

- `wa-commercial-disputes`

## Acceptance criteria

- [ ] Identifies **Washington Consumer Protection Act** at
      RCW 19.86
- [ ] Confirms CPA covers **B2B disputes** as well as consumer
      disputes (despite the "consumer" in the name)
- [ ] Walks the **Hangman Ridge 5-element test** for a private
      CPA claim per *Hangman Ridge Training Stables v. Safeco
      Title Ins. Co.*, 105 Wn.2d 778 (1986):
      1. Unfair or deceptive act or practice
      2. Occurring in trade or commerce
      3. Public-interest impact
      4. Injury to plaintiff's business or property
      5. Causation
- [ ] Applies to facts: deceptive non-disclosure of refurbished
      status = element 1; commercial sale = element 2; potential
      to deceive others = element 3; diminished value of
      equipment = element 4; reliance on representation =
      element 5
- [ ] Identifies damages: actual damages + treble damages up to
      the **statutory cap** (current cap in
      `wa-law-references/references/wa-rcw-debt/RCW-19_86.md`)
      + mandatory attorney's fees for prevailing plaintiff
- [ ] Notes CPA SOL (current day count in chapter file —
      longer than the general tort 3-year SOL)
- [ ] Notes equitable relief: injunction, restitution

## Common failure modes

- Treating CPA as consumer-only (it's not)
- Missing the public-interest element
- Hard-coding a specific treble cap (read from references)
- Hard-coding a specific SOL day count
