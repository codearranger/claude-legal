# wa-personal-injury — Notice of Tort Claim against state actors

## Prompt

I was injured at a Washington state university campus due
to unsafe stairs. The university is part of the state. What
prerequisites do I have before I can sue?

## Expected triggers

- `wa-personal-injury`

## Acceptance criteria

- [ ] Identifies **RCW 4.92.110** Notice of Tort Claim
      requirement against the State of Washington (suit must
      be preceded by notice filed with the Office of Risk
      Management)
- [ ] References the **pre-suit waiting period** — **read
      the current period from `wa-law-references/
      references/wa-rcw-debt/RCW-4_92.md`** rather than
      embedding a number
- [ ] Walks the mandatory notice contents:
      - Names and addresses of claimants
      - Date / time / place of incident
      - Description of incident + cause
      - Description of damages
      - Amount of damages claimed
      - Verification by claimant
- [ ] References the **SOL tolling effect** during the
      pre-suit period (the wait does not consume the
      underlying SOL). **Read the tolling mechanics from
      `RCW-4_92.md`** rather than embedding the day count
- [ ] References **RCW 4.96.020** parallel requirement
      against local governments (cities, counties, school
      districts, etc.) with the same mandatory content; if
      the university is technically a state agency this is
      a 4.92 case, but flag the parallel for local-government
      tort claims
- [ ] Notes substantial-compliance doctrine — minor
      omissions excused; missing required elements fatal

## Common failure modes

- Missing the pre-suit notice prerequisite entirely
- Hard-coding the waiting period
- Filing notice with the wrong agency
- Forgetting to verify the notice
- Treating 4.92 and 4.96 as identical (they parallel but
  apply to different entities)
