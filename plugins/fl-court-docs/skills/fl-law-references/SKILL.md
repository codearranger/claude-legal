---
name: fl-law-references
description: >
  Canonical reference corpora for Florida civil practice — Fla. R. Civ. P., Florida Evidence Code (§ 90), Florida Statutes debt/consumer chapters (§§ 95.11 SOLs, 559.55 FCCPA, 501.204 FDUTPA), and federal symlinks (FDCPA, FCRA, TILA, UCC model, federal bankruptcy). Triggers include 'Florida rules of civil procedure', 'Florida evidence code', 'FCCPA', 'FDUTPA', 'Florida statutes', 'Florida SOL'. Layer on ca-law-references as the federal reference layer.
version: 0.1.0
---

# Florida Law References

This skill provides canonical reference access for Florida
civil-practice research.

## Statewide rules

| Source | URL |
|---|---|
| Florida Rules of Civil Procedure | `https://www.flcourts.gov/Florida-Courts/Court-Administration/Rules-of-Court/Civil-Rules` |
| Florida Rules of Evidence (§ 90) | `https://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0000-0099/0090` |
| Florida Rules of Judicial Admin. | `https://www.flcourts.gov/Florida-Courts/Court-Administration/Rules-of-Court/Judicial-Admin-Rules` |
| Florida Small Claims Rules | `https://www.flcourts.gov` (Small Claims Rules) |

## Florida Statutes — debt and consumer

| Chapter/Section | Topic |
|---|---|
| § 95.11 | Statutes of limitations (5 yr written K; 4 yr negligence; 5 yr UCC) |
| § 559.55-559.785 (FCCPA) | Florida Consumer Collection Practices Act |
| § 501.201-501.213 (FDUTPA) | Florida Deceptive and Unfair Trade Practices Act |
| § 726 (FUFTA) | Florida Uniform Fraudulent Transfer Act |
| § 671-680 (UCC as enacted in Florida) | Florida UCC |
| § 83 | Residential and non-residential landlord-tenant |
| § 61 | Family law (dissolution, custody, support) |
| § 48 | Service of process |
| § 34.01 | County court jurisdiction |

## Federal law (symlinks)

The following directories are symlinked to the
`claude-legal-federal-laws` shared plugin:

- `references/federal-debt-laws/` — FDCPA, FCRA, TILA, ECOA,
  Reg B-Z
- `references/federal-bankruptcy/` — Title 11 U.S.C.
- `references/ucc-model/` — Model UCC Articles 1, 2, 3, 9

## Citation format

Florida citation format uses the Florida Bar's style:
- Cases: *Party v. Party*, ### So. 3d ### (Fla. [Dist.] 20##)
- Statutes: Fla. Stat. § ####
- Rules: Fla. R. Civ. P. #.###
- Use the current Florida courts citation guide for official format

