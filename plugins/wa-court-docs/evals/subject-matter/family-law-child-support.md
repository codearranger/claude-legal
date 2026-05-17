# wa-family-law — Child support calculation

## Prompt

I'm in a Washington dissolution. We have two kids (ages 6 and
9). My net monthly income is $4,200; my spouse's is $7,800.
The kids will live primarily with me. How is child support
calculated?

## Expected triggers

- `wa-family-law`
- `wa-family-court`

## Acceptance criteria

- [ ] Identifies Washington's income-shares model under RCW
      26.18 + 26.19
- [ ] References the **Washington Economic Table** at RCW
      26.19.020
- [ ] Walks combined-net-income calculation:
      $4,200 + $7,800 = $12,000
- [ ] Notes Economic Table cap at $12,000/month combined net
      income — at-or-above cap triggers court discretion
- [ ] References mandatory child-support worksheets (WSCSS)
- [ ] Each parent's pro rata share = (their net income) /
      (combined): 35% / 65%
- [ ] References RCW 26.19.071 net-income definition (gross
      MINUS tax, FICA, mandatory pension, mandatory union,
      court-ordered support)
- [ ] Notes adjustments: health insurance, daycare,
      extraordinary medical (RCW 26.19.080)
- [ ] Notes potential residential-schedule deviation if
      shared residential time

## Common failure modes

- Applying Ohio's $300k cap or CO's 93-overnight rule
- Missing the $12,000/mo Washington-Economic-Table cap
- Forgetting the mandatory worksheet
- Using gross income (should be net)
