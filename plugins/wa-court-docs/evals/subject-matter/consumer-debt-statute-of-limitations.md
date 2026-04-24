# wa-consumer-debt — Statute of limitations

## Prompt
I have a credit-card debt the plaintiff says I stopped paying in
2019. They sued me in 2026. What's the statute of limitations and
does it apply?

## Expected triggers
- `wa-consumer-debt` (wa-statutes-of-limitations.md)

## Acceptance criteria
- Cites **RCW 4.16.040(2)** — written contracts: **6 years**
- Cites **RCW 4.16.080(3)** — unwritten / oral contracts: **3 years**
- Addresses the **debt-buyer evidentiary problem** — can plaintiff
  actually prove there is a written contract? If plaintiff cannot
  produce the signed cardholder agreement, the 3-year SOL may apply
- **Accrual** — typically runs from **date of default / last payment**
  — 2019 + 6 = 2025 (expired) OR 2019 + 3 = 2022 (expired)
- **Tolling / revival** — partial payment or written acknowledgment
  can revive; address both and warn that loose correspondence with
  the debt buyer can accidentally revive
- Affirmative defense — **must be pled** or waived (CRLJ 8(c))
- Cites **RCW 4.16.270 / .280** — revival and acknowledgment rules
- Notes this is a federal **FDCPA § 1692e** violation if debt
  collector sues on time-barred debt (Midland Funding v. Johnson
  addressed this in bankruptcy but Ninth Circuit precedent applies
  more broadly in state court)

## Common failure modes
- Using generic "6 years" without addressing whether a written
  contract exists in admissible form
- Missing the revival-by-payment trap
- Missing affirmative-defense pleading requirement
- Missing FDCPA counterclaim possibility for time-barred debt
