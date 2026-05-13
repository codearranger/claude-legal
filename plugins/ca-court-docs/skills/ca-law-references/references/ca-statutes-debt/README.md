# California Statutes — Debt-Relevant Chapters Corpus

California statutory chapters most relevant to civil practice
and consumer-debt defense. One MD per chapter / topic.

- Last verified: 2026-05-13
- Source: leginfo.legislature.ca.gov

> Authored from canonical California statutory sources; verify
> against leginfo.legislature.ca.gov before relying. A future
> `scripts/pull_ca_statutes.py` will automate refresh from the
> California Legislative Information XML feed.

## Files

### Code of Civil Procedure (CCP)

| File | Citation | Subject |
|---|---|---|
| [CCP-Service.md](CCP-Service.md) | §§ 412.10-417.40 | Service of summons (personal, substituted, NORF mail, entity, publication) |
| [CCP-Pleadings.md](CCP-Pleadings.md) | §§ 425.10-440 | Complaint, demurrer, motion to strike, anti-SLAPP, summary judgment (§ 437c — 75-day notice, separate-statement requirement) |
| [CCP-Motions-1005-to-1020.md](CCP-Motions-1005-to-1020.md) | §§ 1005-1020 | Motion notices, service of papers, 16-court-day notice / 9-court-day opposition / 5-court-day reply framework |
| [CCP-SOL.md](CCP-SOL.md) | §§ 312-366 | Statutes of limitation — § 337 (written contract 4 years), § 339 (oral 2 years), § 360 (revival), § 361 (borrowing) |
| [CCP-Discovery.md](CCP-Discovery.md) | §§ 2016.010-2036.050 | Civil Discovery Act — 35-special-interrogatory cap, 45-day jurisdictional motion-to-compel-further deadline, sanctions |
| [CCP-Time-Computation.md](CCP-Time-Computation.md) | §§ 12-13 | Time computation; court days; California judicial holidays |
| [CCP-Relief-473.md](CCP-Relief-473.md) | §§ 473-473.5 | Discretionary and mandatory relief from default; void judgments; § 473.5 actual-notice motions |
| [CCP-Enforcement.md](CCP-Enforcement.md) | §§ 683-708 | Enforcement of judgments — 10-year life, judgment liens, writ of execution, garnishment, supplemental proceedings |
| [CCP-Exemptions.md](CCP-Exemptions.md) | §§ 703.140 + 704.010-995 | Exemptions — homestead ($300K-$600K per AB 1885), motor vehicle, tools of trade, deposit account, retirement |

### Civil Code

| File | Citation | Subject |
|---|---|---|
| [CivCode-Rosenthal.md](CivCode-Rosenthal.md) | §§ 1788-1788.33 | Rosenthal Fair Debt Collection Practices Act — first-party reach, FDCPA incorporation, statutory damages, attorney's fees |
| [CivCode-FDBPA.md](CivCode-FDBPA.md) | §§ 1788.50-1788.66 | Fair Debt Buying Practices Act — heightened pleading + documentation for debt buyers |
| [CivCode-CLRA.md](CivCode-CLRA.md) | §§ 1750-1784 | Consumers Legal Remedies Act — 24 enumerated practices, 30-day pre-suit notice, 3-year SOL |
| [CivCode-Atty-Fees.md](CivCode-Atty-Fees.md) | § 1717 | Reciprocal attorney's fees on contracts |

### Business & Professions Code

| File | Citation | Subject |
|---|---|---|
| [BPC-UCL.md](BPC-UCL.md) | §§ 17200-17210 | Unfair Competition Law — unlawful/unfair/fraudulent prongs, 4-year SOL, restitution + injunction |

### Financial Code

| File | Citation | Subject |
|---|---|---|
| [FinCode-CDCLA.md](FinCode-CDCLA.md) | §§ 100000-100027 | California Debt Collection Licensing Act — DFPI licensure (2022+) |

### Commercial Code (UCC enactments)

| File | Citation | Subject |
|---|---|---|
| [CommCode-Art-2-Sales.md](CommCode-Art-2-Sales.md) | §§ 2101-2725 | UCC Article 2 (Sales) — § 2725 4-year SOL on sale of goods |
| [CommCode-Art-3-Negotiable.md](CommCode-Art-3-Negotiable.md) | §§ 3101-3605 | UCC Article 3 (Negotiable Instruments) — § 3118 6-year SOL, § 3302 HDC analysis, § 3305 defenses |
| [CommCode-Art-9-Secured.md](CommCode-Art-9-Secured.md) | §§ 9101-9809 | UCC Article 9 (Secured Transactions) — § 9404 assignee takes subject to defenses, § 9406 notification of assignment |

## Re-pulling

A future `scripts/pull_ca_statutes.py` will fetch from the
California Legislative Information bulk XML feed
(`leginfo.legislature.ca.gov/faces/XmlDownloadResults.xhtml`).
Until then, files are authored from canonical sources and
should be verified periodically.

## Quick-reference for consumer-debt defense

The most-cited California statutory provisions in a typical
consumer-debt-defense action:

| Issue | Citation | File |
|---|---|---|
| 4-year SOL on credit-card debt | CCP § 337 | CCP-SOL.md |
| 30-day answer deadline | CCP § 412.20(a)(3) | CCP-Service.md |
| Demurrer for failure to state cause | CCP § 430.10(e) | CCP-Pleadings.md |
| Anti-SLAPP motion (60-day window) | CCP § 425.16 | CCP-Pleadings.md |
| 45-day jurisdictional compel deadline | CCP §§ 2030.300(c), 2031.310(c), 2033.290(c) | CCP-Discovery.md |
| 35-special-interrogatory cap | CCP § 2030.030(a) | CCP-Discovery.md |
| Discretionary relief from default | CCP § 473(b) | CCP-Relief-473.md |
| Rosenthal Act remedies | Civ. Code § 1788.30 | CivCode-Rosenthal.md |
| FDBPA pleading requirements | Civ. Code § 1788.58 | CivCode-FDBPA.md |
| UCL "unlawful" prong | Bus. & Prof. Code § 17200 | BPC-UCL.md |
| CDCLA licensure requirement | Cal. Fin. Code § 100002 | FinCode-CDCLA.md |
| Assignee takes subject to defenses | Cal. Comm. Code § 9404(a) | CommCode-Art-9-Secured.md |
| Reciprocal attorney's fees | Civ. Code § 1717 | CivCode-Atty-Fees.md |
| Homestead exemption ($300K-$600K) | CCP § 704.730 | CCP-Exemptions.md |
| Wage garnishment limits | CCP § 706.050 | CCP-Enforcement.md |

## Cross-references to related corpora

- [`../court-rules/`](../court-rules/) — California Rules of
  Court (CRC), California Evidence Code (CEC), local rules for
  LASC / SFSC / OCSC, Rules of Professional Conduct
- [`../federal-debt-laws/`](../federal-debt-laws/) — Federal
  consumer-credit statutes (FDCPA, FCRA, TILA, ECOA) and CFPB
  regulations (Reg F, Reg V, Reg Z, Reg B)
- [`../ucc-model/`](../ucc-model/) — Model UCC Articles 1, 2,
  3, 9 (the texts California enacted as Cal. Comm. Code
  Divisions 1, 2, 3, 9)

## Cross-references to skills

- `../../../ca-law-references/SKILL.md` — canonical reference
  catalog
- `../../../ca-consumer-debt/SKILL.md` — consumer-debt defense
  bundle
- `../../../ca-deadlines/SKILL.md` — workflow using these statutes
- `../../../ca-first-30-days/SKILL.md` — response-window workflow
- `../../../ca-discovery/SKILL.md` — discovery workflow
- `../../../ca-post-judgment/SKILL.md` — post-judgment workflow
