# ny-consumer-debt — Consumer Credit Fairness Act (CCFA) heightened pleading

## Prompt

I've been served by Midland Credit Management in NYC Civil
Court. The complaint just says they "purchased the account
from Citibank" and demands $4,800. The case is from 2025.
What heightened pleading requirements apply to this kind of
case in NY now?

## Expected triggers

- `ny-consumer-debt`
- `ny-first-30-days`

## Acceptance criteria

- [ ] Identifies the **2022 Consumer Credit Fairness Act
      (CCFA)** as the controlling regime
- [ ] Cites **CPLR 3015(e)** heightened pleading: the
      complaint must allege
      - identity of the original creditor
      - itemization of charges + payments + interest +
        fees (so the litigant can verify default-balance
        math)
      - chain of title (each assignment, with effective date)
      - last activity date on the account
- [ ] Cites **CPLR 214-i**: **3-year SOL** on consumer-credit
      actions (down from 6 under CPLR 213(2)) — the CCFA
      retroactively shortened debt-buyer cases
- [ ] Cites **22 NYCRR § 202.27-a**: default-judgment
      scrutiny — debt-buyer must serve a notice and the
      court reviews submitted proof before judgment
- [ ] Cites **CPLR 306-b**: 120-day service period; debt
      buyers frequently miss this and get dismissed
- [ ] Notes the **mini-FDCPA** at GBL § 600-602 as a
      counterclaim/affirmative-defense source
- [ ] Cross-references chain-of-title via UCC Article 9
      perfection

## Common failure modes

- Treats this like a pre-2022 NY case (no CCFA pleading
  requirements; 6-year SOL)
- Suggests federal FDCPA without the NY mini-FDCPA overlay
- Misses CPLR 214-i and applies the 6-year contract SOL
- Doesn't connect 22 NYCRR § 202.27-a default-judgment
  scrutiny back to the CCFA
