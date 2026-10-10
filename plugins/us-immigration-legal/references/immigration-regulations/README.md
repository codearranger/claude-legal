# Immigration Regulations — 8 CFR and 22 CFR

Verbatim regulation text implementing the INA, one Markdown file per CFR Part.
Two titles carry immigration practice:

- **8 CFR — Aliens and Nationality.** Chapter I is the DHS component
  (USCIS / CBP / ICE) regulations; Chapter V is the DOJ **Executive Office for
  Immigration Review (EOIR)** — the immigration courts and the **Board of
  Immigration Appeals** — at 8 CFR Parts 1001–1337.
- **22 CFR — Foreign Relations.** The State Department visa, passport, and
  exchange-visitor parts that pair with the Foreign Affairs Manual.

Many subjects appear **twice** — once in DHS regulations and once in the
parallel EOIR regulation (e.g., asylum at 8 CFR 208 (DHS) and 8 CFR 1208
(EOIR); removal at 8 CFR 240 (DHS) and 8 CFR 1240 (EOIR)). Cite the version
that governs the forum you are in.

- Pulled by: `scripts/pull_immigration_cfr.py`
- Source: [eCFR XML versioner API](https://www.ecfr.gov/api)
- As-of date: see `_manifest.json` (`as_of`)

## 8 CFR Chapter I — DHS (USCIS / CBP / ICE)

| File | Part | Subject |
|---|---|---|
| [8CFR-001-definitions.md](8CFR-001-definitions.md) | 1 | Definitions |
| [8CFR-103-powers-fees.md](8CFR-103-powers-fees.md) | 103 | Benefits; biometrics; records; fees |
| [8CFR-204-immigrant-petitions.md](8CFR-204-immigrant-petitions.md) | 204 | Immigrant petitions (I-130 / I-140 / I-360 / I-526) |
| [8CFR-207-refugees.md](8CFR-207-refugees.md) | 207 | Admission of refugees |
| [8CFR-208-asylum-dhs.md](8CFR-208-asylum-dhs.md) | 208 | Asylum and withholding (DHS / USCIS asylum office) |
| [8CFR-209-adjustment-refugee.md](8CFR-209-adjustment-refugee.md) | 209 | Adjustment of refugees and asylees |
| [8CFR-211-lpr-documents.md](8CFR-211-lpr-documents.md) | 211 | Documentary requirements: immigrants |
| [8CFR-212-inadmissibility.md](8CFR-212-inadmissibility.md) | 212 | Waivers; parole; admission of inadmissible aliens |
| [8CFR-214-nonimmigrants.md](8CFR-214-nonimmigrants.md) | 214 | Nonimmigrant classes (B/F/H/L/O/P, etc.) |
| [8CFR-216-conditional-residence.md](8CFR-216-conditional-residence.md) | 216 | Conditional permanent residence (I-751) |
| [8CFR-217-visa-waiver.md](8CFR-217-visa-waiver.md) | 217 | Visa Waiver Program |
| [8CFR-235-inspection.md](8CFR-235-inspection.md) | 235 | Inspection at ports of entry; expedited removal |
| [8CFR-236-detention-removal.md](8CFR-236-detention-removal.md) | 236 | Apprehension and detention; bond |
| [8CFR-240-removal-proceedings.md](8CFR-240-removal-proceedings.md) | 240 | Removability proceedings (DHS) |
| [8CFR-241-removal-execution.md](8CFR-241-removal-execution.md) | 241 | Detention and removal of aliens ordered removed |
| [8CFR-244-tps.md](8CFR-244-tps.md) | 244 | Temporary Protected Status |
| [8CFR-245-adjustment.md](8CFR-245-adjustment.md) | 245 | Adjustment of status to LPR |
| [8CFR-245a-legalization.md](8CFR-245a-legalization.md) | 245a | Adjustment under INA § 245A |
| [8CFR-248-change-of-status.md](8CFR-248-change-of-status.md) | 248 | Change of nonimmigrant classification |
| [8CFR-264-registration.md](8CFR-264-registration.md) | 264 | Registration and fingerprinting |
| [8CFR-274a-employment.md](8CFR-274a-employment.md) | 274a | Control of employment of aliens (I-9 / E-Verify) |
| [8CFR-287-enforcement.md](8CFR-287-enforcement.md) | 287 | Field officers; powers and duties |
| [8CFR-292-representation.md](8CFR-292-representation.md) | 292 | Representation and appearances; EOIR recognition/accreditation |

## 8 CFR Chapter V — EOIR (DOJ): immigration courts + BIA

| File | Part | Subject |
|---|---|---|
| [8CFR-1001-eoir-definitions.md](8CFR-1001-eoir-definitions.md) | 1001 | Definitions (EOIR) |
| [8CFR-1003-eoir-bia.md](8CFR-1003-eoir-bia.md) | 1003 | Immigration courts and the Board of Immigration Appeals (appeals, motions, practice) |
| [8CFR-1208-asylum-eoir.md](8CFR-1208-asylum-eoir.md) | 1208 | Asylum and withholding (in removal proceedings) |
| [8CFR-1240-removal-eoir.md](8CFR-1240-removal-eoir.md) | 1240 | Removability proceedings (before the immigration judge) |

## 22 CFR — State Department (visas / passports / exchange)

| File | Part | Subject |
|---|---|---|
| [22CFR-040-visas-general.md](22CFR-040-visas-general.md) | 40 | Rules common to NIV + IV |
| [22CFR-041-nonimmigrant-visas.md](22CFR-041-nonimmigrant-visas.md) | 41 | Nonimmigrant visa documentation |
| [22CFR-042-immigrant-visas.md](22CFR-042-immigrant-visas.md) | 42 | Immigrant visa documentation |
| [22CFR-051-passports.md](22CFR-051-passports.md) | 51 | Passports |
| [22CFR-053-entry-departure.md](22CFR-053-entry-departure.md) | 53 | Passport requirement and exceptions |
| [22CFR-062-exchange-visitor.md](22CFR-062-exchange-visitor.md) | 62 | Exchange Visitor (J) Program |

## Extending coverage

Add a row to `CFR_PARTS` in `scripts/pull_immigration_cfr.py` and re-run. The
list is curated to the most-cited parts rather than every part in Titles 8 / 22.

> **NOT LEGAL ADVICE.** Reference text is a drafting/research aid; verify against
> the current eCFR before relying on it.
