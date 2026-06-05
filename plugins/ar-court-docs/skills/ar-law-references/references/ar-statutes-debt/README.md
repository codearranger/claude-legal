# ar-statutes-debt Corpus — Arkansas

This corpus holds **verbatim text** of the **Arkansas Code Annotated**
chapters most relevant to civil practice. The directory slug
(`ar-statutes-debt`) is **legacy, retained for path stability** — the
scope is the full **civil + family + consumer** surface, not debt-only.

> **Current status: VERBATIM.** This directory holds the **full verbatim
> section text** of each chapter (one `Ark-Code-T<T>-Ch<C>.md` file per
> pull target), extracted from the Justia mirror of the public-domain
> Arkansas Code by `pull_arkansas_statutes.py`. Each file's header
> records the Justia source and the fetch date. Re-run the puller (with
> `curl_cffi` installed) to refresh.

## Scope — pull targets (the civil + family + consumer surface)

| Title / chapter | Subject | Key sections |
|---|---|---|
| **Title 16, ch. 56** | Limitations of actions | § 16-56-105 (3-yr oral/open account/tort), § 16-56-111 (5-yr written contract), § 16-56-114 (judgments) |
| **Title 16, ch. 22** | Attorneys / fees | **§ 16-22-308** (attorney's fees in contract/account/note actions) |
| **Title 16, ch. 62** | Wrongful death | § 16-62-102 |
| **Title 16, ch. 64** | Comparative fault | § 16-64-122 (modified comparative fault, 49% bar) |
| **Title 16, ch. 65** | Judgments / enforcement | § 16-65-501 (scire facias revival) |
| **Title 16, ch. 55** | Civil Justice Reform Act of 2003 | § 16-55-201 (several liability); § 16-55-208 (punitive cap — struck, *Bayer*) |
| **Title 16, ch. 108** | Arbitration | § 16-108-201 et seq. (Revised UAA) |
| **Title 16, ch. 114** | Medical malpractice | § 16-114-201 et seq.; § 16-114-203 (2-yr SOL) |
| **Title 16, ch. 123** | Arkansas Civil Rights Act of 1993 | § 16-123-101 et seq.; § 16-123-102 (9+ employees) |
| **Title 9** | Family law | 9-11 (marriage / covenant marriage), 9-12 (divorce / property / support), 9-13 (custody), 9-15 (domestic abuse / OP), 9-17 (UIFSA), 9-19 (UCCJEA), 9-27 (Juvenile Code) |
| **Title 4** | Commercial / consumer | UCC 4-1 / 4-2 / 4-3 / 4-9; 4-27 (Business Corporation Act); 4-38 (Uniform LLC Act); 4-59 (UFTA); 4-75 (trade secrets / non-compete); **4-88 (ADTPA)** |
| **Title 17, ch. 24** | Collection agencies | § 17-24-101 et seq. (State Board of Collection Agencies licensing) |
| **Title 18** | Property / landlord-tenant | 18-16 (failure to vacate / deposits), 18-17 (Residential Landlord-Tenant Act + habitability), 18-60 (unlawful detainer) |
| **Title 11** | Labor | 11-3 (right-to-work), 11-4 (Minimum Wage Act), 11-9 (workers' comp — exclusive remedy) |
| **Title 21** | Public officers / immunity | 21-1-601 et seq. (Whistle-Blower Act), 21-9-301 (political-subdivision tort immunity) |
| **Title 19, ch. 10** | State Claims Commission | § 19-10-201 et seq. (forum for claims against the State) |
| **Title 1, ch. 5** | Holidays | § 1-5-101 (state holidays — used by deadline arithmetic) |

## Citation form

`Ark. Code Ann. § 16-56-111` (subsections `§ 4-88-113(f)`; ranges
`§ 17-24-101 et seq.`).

## Access posture

The **bare section text of the Arkansas Code is public domain** (a
government edict; the LexisNexis copyright covers only the
annotations). The official lookup is **arkleg.state.ar.us**; the
puller mirrors the public-domain text from **Justia**
(`law.justia.com/codes/arkansas/`), which sits behind Cloudflare and
typically requires **curl_cffi Chrome impersonation**. Spot-check
pulled text against the official source before citing.

## How to re-pull

Author / run `scripts/pull_arkansas_statutes.py`, which fetches the
configured Title/chapter targets from the Justia mirror (fallback /
spot-check: arkleg.state.ar.us), slices by section, and emits one
Markdown file per topic with `## § NN-N-NNN. Title` headings. Write
atomically and wire into the quarterly `refresh-references` workflow
under `target=ar`. Expected invocation:

```bash
python3 scripts/pull_arkansas_statutes.py --workers 4 \
  --out plugins/ar-court-docs/skills/ar-law-references/references/ar-statutes-debt
```

On a successful pull, update `_manifest.json` (version + `last_pulled`)
and bump the `ar-law-references` `SKILL.md` `version:` (PATCH for a
routine refresh, MINOR if a new target file is added).
