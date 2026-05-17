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
- [ ] Confirms CPA covers **B2B disputes** as well as
      consumer disputes (despite the "consumer" in the name)
- [ ] Walks the **Hangman Ridge 5-element test** for a
      private CPA claim per *Hangman Ridge Training Stables
      v. Safeco Title Ins. Co.*, 105 Wn.2d 778 (1986):
      1. Unfair or deceptive act or practice
      2. Occurring in trade or commerce
      3. Public-interest impact
      4. Injury to plaintiff's business or property
      5. Causation
- [ ] Applies to facts: deceptive non-disclosure of
      refurbished status = element 1; commercial sale =
      element 2; potential to deceive others = element 3;
      diminished value of equipment = element 4; reliance
      on representation = element 5
- [ ] Identifies damages: actual damages + **treble damages
      up to $25,000 cap** at court's discretion +
      **mandatory attorney's fees** for prevailing
      plaintiff under RCW 19.86.090
- [ ] Notes **4-year SOL** under RCW 19.86.120 (longer than
      general tort 3-year SOL)
- [ ] Notes equitable relief: injunction, restitution

## Common failure modes

- Treating CPA as consumer-only (it's not)
- Missing the public-interest element
- Wrong SOL (3-year general doesn't apply; CPA-specific
  is 4-year)
- Missing the treble-damages cap ($25k, not unlimited)
