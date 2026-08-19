---
name: fl-consumer-debt
description: >
  Subject-matter bundle for Florida consumer-debt defense — FDCPA, Regulation F, FCCPA (Fla. Stat. § 559.72), FDUTPA (§ 501.204), Florida SOLs (5-yr written K, 2-yr FCCPA), chain of title, debt-buyer defenses, DCBS-equivalent registration requirements. Triggers include 'Florida consumer debt', 'Florida debt collection', 'FCCPA Florida', 'Florida debt buyer', 'Florida 559.72', 'FDUTPA Florida debt', 'Florida chain of title debt'.
version: 0.1.0
---

# Florida Consumer-Debt Defense

> **NOT LEGAL ADVICE.** This skill provides a procedural and
> substantive framework for Florida consumer-debt defense. Verify
> all cites against current Florida Statutes and applicable federal
> law before relying.

## Florida-specific consumer-debt landscape

Florida has two powerful state consumer-protection statutes
that layer on top of the federal FDCPA:

### Florida Consumer Collection Practices Act (FCCPA) — Fla. Stat. § 559.55-559.785

The FCCPA is **broader than the FDCPA**:
- Applies to **both first-party and third-party** creditors
  (unlike FDCPA, which applies only to debt collectors)
- Covers **any person** collecting consumer debts — not
  limited to professionals
- **SOL**: 2 years from the violation (§ 559.77(4))
- **Remedies**: actual damages; statutory damages up to
  $1,000 per action; attorney's fees (mandatory to
  prevailing plaintiff)

Key § 559.72 prohibitions:
- Simulating legal process (§ 559.72(9))
- Communicating with a consumer who has retained an attorney
  (§ 559.72(18))
- Threatening arrest or criminal prosecution for a civil debt
- Using profane or obscene language
- Contacting a consumer's employer without written consent

### Florida Deceptive and Unfair Trade Practices Act (FDUTPA) — § 501.201-501.213

FDUTPA applies to **any person** engaged in trade or commerce,
including debt collection:
- Private right of action: actual damages + attorney's fees
  (§ 501.2105)
- AG enforcement available
- **SOL**: 4 years (§ 501.2077)
- No requirement to show deception was directed at a particular
  plaintiff — objective "likely to deceive" standard

## Chain of title — Florida

Florida applies the same chain-of-title requirements as other
states: a debt buyer must prove each link from original creditor
to itself with authenticated bills of sale and assignment
schedules.

**Florida business records** foundation: under Fla. Stat.
§ 90.803(6) (Florida Evidence Code), business records are
admissible if the custodian or another qualified witness
establishes the foundational requirements. For debt buyers,
the "remote custodian" limitation — inability to authenticate
the original creditor's records — is a powerful defense.

## Composition

- `fl-statewide-format` + `fl-miami-dade` / `fl-broward` /
  `fl-orange` / `fl-county-courts` — venue
- `fl-discovery` — targeted RFPs and RFAs for debt buyers
- `fl-first-30-days` — affirmative defenses and FCCPA
  counterclaims in the answer
- `fl-deadlines` — 5-yr K SOL, 2-yr FCCPA, 4-yr FDUTPA,
  1-yr FDCPA

