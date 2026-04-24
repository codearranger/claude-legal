# wa-consumer-debt — FDCPA counterclaim elements

## Prompt
Plaintiff is a debt buyer that has sent me multiple collection letters
with different balances and no validation after I disputed. Can I
counterclaim under the FDCPA?

## Expected triggers
- `wa-consumer-debt` (fdcpa.md)

## Acceptance criteria
- Cites **15 U.S.C. § 1692** (FDCPA)
- Identifies that FDCPA applies to **debt collectors** (third-party);
  addresses whether a debt buyer qualifies under **§ 1692a(6)**
- Cites relevant violations:
  - **§ 1692e** (false or misleading representations) — different
    balances
  - **§ 1692g** (validation notice and disputed-debt obligations) —
    failure to provide validation after dispute
  - **§ 1692f** (unfair practices) — potentially applicable
- Cites **§ 1692k** statutory damages ($1,000) plus actual damages,
  attorney fees and costs
- Notes **one-year statute of limitations** under § 1692k(d)
- References Regulation F (**12 C.F.R. § 1006**) for recent amplified
  requirements
- Notes **Henson v. Santander** / debt-buyer FDCPA coverage question
  (buyer of defaulted debt may not qualify as "debt collector" if
  collecting its own account)

## Common failure modes
- Missing the Henson debt-buyer coverage limitation
- Giving a federal general 4-year SOL instead of the FDCPA's 1-year
- Missing Regulation F
- Citing state law (RCW 19.16) as if it were FDCPA
