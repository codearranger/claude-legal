---
name: federal-law-references
description: >
  Use this skill to read the verbatim federal reference corpora shipped
  in us-federal-legal: FDCPA, FCRA, TILA, ECOA, EFTA, RESPA,
  SCRA, FHA, the FTC Telemarketing Sales Rule, CFPB Regulations B / DD /
  E / F / M / N / P / V / X / Z, federal garnishment limits (15 U.S.C.
  ch. 41 subch. II), the Bankruptcy Code (Title 11 chapters 1, 3, 5, 7,
  11, 12, 13, 15), the model UCC (Articles 1, 2, 3, 9), and the ADA with
  29 CFR 1630 and 28 CFR 35/36. Triggers include "FDCPA text", "what
  does 1692g say", "Reg F", "Reg Z", "TILA section", "FCRA 1681i",
  "automatic stay 362", "discharge 727", "UCC 9-609", "UCC 3-302",
  "holder in due course", "ADA Title III text", "federal statute
  text". Also the fallback for every state plugin's
  `<state>-law-references` skill when its `federal-debt-laws/`,
  `federal-bankruptcy/`, or `ucc-model/` directory is missing or a
  dangling link (some install methods, such as a git-subdir
  marketplace entry, copy only the state plugin's own folder).
version: 0.1.0
---

# Federal Law References

> **NOT LEGAL ADVICE.** These are snapshots of primary-source text for drafting and research.
> Verify against the current official source before filing.

## Purpose

This plugin holds the single canonical copy of the federal corpora. Every state plugin in the
legal-skills marketplace declares `us-federal-legal` as a dependency and links its
`<state>-law-references/references/federal-debt-laws/`, `federal-bankruptcy/`, and `ucc-model/`
directories here.

Those links resolve when a state plugin is installed from the legal-skills marketplace, which
copies the targets into the install. They do **not** resolve when a state plugin is installed
on its own folder (for example a `git-subdir` entry in another marketplace): the link survives
but its target was never downloaded. The dependency itself is still installed, so the text is
always available here.

## Where the files are

All paths are relative to this plugin's root, `${CLAUDE_PLUGIN_ROOT}` (two directories above
this skill's base directory):

| Corpus | Directory | Contents |
|---|---|---|
| Federal debt / consumer-finance | `references/federal-debt-laws/` | `FDCPA.md`, `FCRA.md`, `TILA.md`, `ECOA.md`, `EFTA.md`, `RESPA.md`, `SCRA.md`, `FHA.md`, `TSR.md`, `Garnishment.md`, `Reg-B.md`, `Reg-DD.md`, `Reg-E.md`, `Reg-F.md`, `Reg-M.md`, `Reg-N.md`, `Reg-P.md`, `Reg-V.md`, `Reg-X.md`, `Reg-Z.md` |
| Bankruptcy Code (Title 11) | `references/federal-bankruptcy/` | `Chapter-1.md`, `Chapter-3.md`, `Chapter-5.md`, `Chapter-7.md`, `Chapter-11.md`, `Chapter-12.md`, `Chapter-13.md`, `Chapter-15.md` |
| Model UCC | `references/ucc-model/` | `Article-1.md`, `Article-2.md`, `Article-3.md`, `Article-9.md` |
| ADA | `references/ada-laws/` | `ADA.md`, `EEOC-Title-I-29-CFR-1630.md`, `DOJ-Title-II-28-CFR-35.md`, `DOJ-Title-III-28-CFR-36.md` |

Each directory has a `README.md` with the source URL, retrieval date, and section index. Search a
file for the section number (for example `§ 1692g` or `9-609`) rather than reading it whole;
`federal-debt-laws/Reg-Z.md` and `FCRA.md` are large.

## Resolving a path a state skill cites

When a state skill cites `../<state>-law-references/references/federal-debt-laws/FDCPA.md` (or
`federal-bankruptcy/...`, `ucc-model/...`):

1. Try the cited path. If it exists, use it.
2. If it is missing or a dangling link, read the same file name from this plugin:
   `${CLAUDE_PLUGIN_ROOT}/references/federal-debt-laws/FDCPA.md`. The file names and layout are
   identical, so only the prefix changes.
3. If neither resolves, `us-federal-legal` is not installed. Tell the user to install
   it (it is a declared dependency of every state plugin) and do not quote federal text from
   memory.

## Citation discipline

- Quote statutory and regulatory text only from these files, never from memory.
- Cite the U.S. Code or CFR section, not the file path. The UCC files are the ALI/ULC **model**
  text: cite the state's enacted version (in the state plugin's statutes corpus) in a filing and
  use the model text only to compare.
- Case law is not snapshotted. Use the `case-law-research` skill for cases interpreting these
  provisions.
