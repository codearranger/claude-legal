# ADA Laws

The Americans with Disabilities Act and the three federal regulations that implement its
substantive titles. Verbatim text from the official sources. Mirrors the corpus published at
[ada.gov/law-and-regs](https://www.ada.gov/law-and-regs/).

- Pulled: 2026-06-18
- Statute source: [uscode.house.gov USLM XML](https://uscode.house.gov/download/download.shtml), release point Public Law **119-84**.
- Regulation source: [eCFR XML versioner API](https://www.ecfr.gov/api), as-of date **2026-01-01**.

## Statute — 42 U.S.C. Chapter 126 (Equal Opportunity for Individuals with Disabilities)

| File | Citation | Coverage |
|---|---|---|
| [ADA.md](ADA.md) | 42 U.S.C. §§ 12101–12213 | The whole chapter, rendered as one file. Chapter-level general provisions (§ 12101 findings/purpose, § 12102 definition of "disability" as amended by the ADA Amendments Act of 2008, § 12103 additional definitions) precede the four title-subchapters. |

The single statute file is organized by the ADA's titles (USC subchapters):

| ADA title | USC subchapter | Sections | Subject |
|---|---|---|---|
| Title I | Subchapter I | §§ 12111–12117 | Employment |
| Title II | Subchapter II | §§ 12131–12165 | Public services (state & local government, incl. public transportation in Part B) |
| Title III | Subchapter III | §§ 12181–12189 | Public accommodations and services operated by private entities |
| Title V | Subchapter IV | §§ 12201–12213 | Miscellaneous provisions (incl. § 12203 retaliation & coercion) |

> **Note on ADA Title IV (telecommunications relay services).** The ADA's Title IV amended the
> Communications Act at **47 U.S.C. § 225** and is *not* part of 42 U.S.C. Chapter 126, so it is not
> in this file. The chapter's Subchapter IV is the ADA's **Title V** (miscellaneous), not Title IV.

## Regulations

| File | Citation | Agency / implements |
|---|---|---|
| [EEOC-Title-I-29-CFR-1630.md](EEOC-Title-I-29-CFR-1630.md) | 29 C.F.R. Part 1630 | EEOC — ADA Title I (employment), incl. the interpretive appendix |
| [DOJ-Title-II-28-CFR-35.md](DOJ-Title-II-28-CFR-35.md) | 28 C.F.R. Part 35 | DOJ — ADA Title II (state & local government) |
| [DOJ-Title-III-28-CFR-36.md](DOJ-Title-III-28-CFR-36.md) | 28 C.F.R. Part 36 | DOJ — ADA Title III (public accommodations); appendices carry the **2010 ADA Standards for Accessible Design** (figures flatten to text; dimensional specs preserved) |

## Re-pulling

```
python3 scripts/pull_ada.py
# or just one piece:
python3 scripts/pull_ada.py --only ADA
python3 scripts/pull_ada.py --only DOJ-Title-II-28-CFR-35
```

Update `USC_RELEASE` and `ECFR_AS_OF` in [`scripts/pull_ada.py`](../../../../scripts/pull_ada.py) when
refreshing. The shared `claude-legal-federal-laws` plugin is the canonical home for this corpus.

## Scope and adjacent law

This corpus is the ADA statute plus its three core substantive-title regulations. Related
disability-rights authorities that are **not** in this directory:

- **Section 504 of the Rehabilitation Act of 1973** (29 U.S.C. § 794) — bars disability
  discrimination by recipients of federal financial assistance and by federal agencies. Often
  pleaded alongside the ADA; not snapshotted here — research live via the bundled MCP servers.
- **Fair Housing Act** disability provisions — disability discrimination and
  reasonable-accommodation/modification duties in *housing* live in
  [`../federal-debt-laws/FHA.md`](../federal-debt-laws/FHA.md) (42 U.S.C. §§ 3601–3619).
- **Air Carrier Access Act** (49 U.S.C. § 41705) and DOT/HUD/DOT-rail accessibility standards —
  adjacent regimes; not snapshotted here.
- **2010 ADA Standards for Accessible Design** — incorporated into the Title III regulation and
  rendered in `DOJ-Title-III-28-CFR-36.md`; the official illustrated PDF lives at
  [ada.gov](https://www.ada.gov/law-and-regs/design-standards/2010-stds/).

Adjacent federal corpora in this plugin:

- [`../federal-debt-laws/`](../federal-debt-laws/) — consumer-finance and debt-collection statutes/regs.
