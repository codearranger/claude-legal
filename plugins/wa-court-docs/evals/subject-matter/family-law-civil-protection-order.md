# wa-family-law — Civil protection order under RCW 7.105 (2022 consolidation)

## Prompt

My partner has been threatening me and showed up at my
workplace last week. I'm scared. I'm in King County. What
protection-order options do I have?

## Expected triggers

- `wa-family-law`
- `wa-family-court`

## Acceptance criteria

- [ ] Identifies **RCW 7.105** as the **2022 consolidated**
      civil-protection-order regime (replaces the former
      RCW 26.50 DV / 7.90 sexual-assault / 7.92 stalking /
      10.14 anti-harassment / 74.34 vulnerable-adult / 7.94
      extreme-risk fragmentation)
- [ ] Walks the six order categories (DV / sexual assault /
      stalking / anti-harassment / vulnerable adult /
      extreme risk) and identifies which apply on these
      facts (most likely DV or stalking)
- [ ] Identifies the **ex parte temporary order** mechanism
      — same-day issuance on a showing of immediate /
      present danger
- [ ] References the **full hearing** within the statutory
      window after ex parte issuance. **Read the current
      hearing-window day count from `wa-law-references/
      references/wa-rcw-debt/RCW-7_105.md`** rather than
      embedding a number
- [ ] References **final order duration** — set by statute
      / by category. **Read current duration limits from
      `RCW-7_105.md`** — do NOT embed a year count
- [ ] References **firearm-surrender** requirement under
      federal 18 U.S.C. § 922(g)(8) and state RCW 9.41.800
      when triggered
- [ ] References the King County Family Law Commissioner
      docket as the typical intake forum

## Common failure modes

- Citing the pre-2022 fragmented chapter numbers (26.50,
  7.90, etc.) as still controlling
- Hard-coding the full-hearing window
- Hard-coding the final-order duration
- Missing the firearm-surrender requirement
