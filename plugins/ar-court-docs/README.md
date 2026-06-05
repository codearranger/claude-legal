# ar-court-docs — Arkansas

Draft and format pleadings, declarations, motions, notices, and proposed
orders for Arkansas courts.

> **NOT LEGAL ADVICE.** Output is a drafting aid; verify every rule,
> deadline, and citation against current law before filing.

## What it covers

Arkansas unified its trial courts under **Amendment 80** (effective July 1,
2001), merging the former chancery (equity), probate, and circuit (law)
courts into a single **Circuit Court** of general jurisdiction organized
into five administrative divisions (criminal, civil, probate, domestic
relations, juvenile). Below it sits the limited-jurisdiction **District
Court** — the high-volume consumer-debt and eviction forum.

Arkansas has **no single statewide page/margin/font rule** for trial
pleadings: form is governed by **Ark. R. Civ. P. 10** (caption + numbered
paragraphs + written instruments) and **Rule 11** (signature), plus
**Administrative Order No. 19** (redaction of confidential information +
certificate of compliance) and **Administrative Order No. 21** (eFlex
e-filing); typography and page limits come from each court's local rules.
`ar-statewide-format` is the canonical layout home and ships the
marketplace-universal conventions (line-numbered pleading paper, the
"Page X of Y" footer) by default. Citation is the Arkansas medium-neutral
/ public-domain form (`2015 Ark. 100` / `2015 Ark. App. 200`) under
**Ark. Sup. Ct. R. 5-2**.

**29 SKILL.md files**:

- **Statewide + procedural core**: `ar-statewide-format`, `ar-pro-se`,
  `ar-law-references`, `ar-discovery`, `ar-hearings`, `ar-post-judgment`,
  `ar-first-30-days`, `ar-fact-check`, `ar-deadlines`, the four
  `ar-draft-*` scaffolders (motion, declaration, note, order),
  `ar-quality-check`, `ar-schedule-hearing`, `ar-file-packet`,
  `ar-submit-order`.
- **Venues**: `ar-pulaski` (Pulaski County Circuit, 6th Circuit, Little
  Rock — the state's largest court), `ar-benton` (Benton County Circuit,
  19th-W, Bentonville), `ar-washington` (Washington County Circuit, 4th,
  Fayetteville/Springdale), `ar-district-courts` (the limited-jurisdiction
  civil + small-claims + unlawful-detainer forum with the 30-day de novo
  appeal to Circuit Court), `ar-county-courts` (28-circuit / 75-county
  roll-up), and `ar-family-court` (the Domestic Relations + Juvenile
  Divisions of Circuit Court — Arkansas has no separate family court).
- **Six subject-matter bundles**: `ar-consumer-debt` (FDCPA + Reg F + the
  ADTPA at Ark. Code Ann. § 4-88-101 with the Act 986 of 2017
  private-action narrowing + collection-agency licensing under the
  Arkansas State Board of Collection Agencies at § 17-24-101 + chain of
  title + the 5-year written / 3-year open-account SOL split + Arkansas
  fact-pleading), `ar-family-law` (Title 9 — the 18-month-separation
  no-fault ground + the Arkansas corroboration-of-grounds requirement +
  **covenant marriage** at § 9-11-801 + equitable distribution with the
  one-half presumption at § 9-12-315 + **income-shares** child support
  under Administrative Order No. 10 (eff. July 1, 2020) + the **Act 604
  of 2021 rebuttable joint-custody presumption** at § 9-13-101 + UCCJEA /
  UIFSA + the Domestic Abuse Act), `ar-landlord-tenant` (the criminal
  failure-to-vacate statute at § 18-16-101 + civil unlawful detainer at
  § 18-60-301 + the **Act 1052 of 2021 implied-habitability** standards at
  § 18-17-501 — Arkansas was the last state to adopt any), `ar-personal-injury`
  (the § 16-64-122 modified comparative-fault "less than" bar + several
  liability under the 2003 Civil Justice Reform Act with the parts struck
  down in *Johnson v. Rockwell* and *Bayer CropScience v. Schafer* + the
  Ark. Const. art. 5 § 32 no-damages-caps rule + near-absolute state
  sovereign immunity routing to the Arkansas State Claims Commission +
  the Medical Malpractice Act with its struck affidavit-of-merit
  requirement), `ar-employment` (the Arkansas Civil Rights Act at
  § 16-123-101 + the Minimum Wage Act + the Whistle-Blower Act + the
  § 4-75-101 non-compete-reformation statute + workers'-comp exclusive
  remedy + right-to-work), and `ar-commercial-disputes` (no dedicated
  business court; UCC + the Arkansas Trade Secrets Act + the 2021 Uniform
  LLC Act + the Business Corporation Act + the Arkansas UFTA + the
  Uniform Arbitration Act).

Follows the thin-skill architecture: SKILL.md bodies describe procedural
frameworks and point at the references corpus for current statutory text,
dollar thresholds, day counts, and exact subsections, so the quarterly
puller can refresh canonical law without SKILL.md edits.

## Reference corpora

Under `skills/ar-law-references/references/` (each corpus dir has its own
README): `ar-statutes-debt/` (curated Ark. Code Ann. civil + family +
consumer chapters; legacy slug retained for path stability), `court-rules/`
(Ark. R. Civ. P., Ark. R. Evid., Arkansas District Court Rules, Supreme
Court / Court of Appeals Rules), plus the shared `federal-debt-laws/` /
`federal-bankruptcy/` / `ucc-model/` symlinks into
`claude-legal-federal-laws`. Each subject bundle also carries its own
`references/` set.

## Refresh

- `scripts/pull_arkansas_statutes.py` — Justia mirror
  (`law.justia.com/codes/arkansas/`) → `ar-statutes-debt/` (curl_cffi
  Chrome impersonation; discovers section URLs by walking
  Title→Chapter→Subchapter→Section; stub fallback on Cloudflare block).
- `scripts/pull_arkansas_rules.py` — courtrules.net mirror →
  `court-rules/` (verbatim where reachable, else canonical-URL pointer
  stubs).
- Wired into `.github/workflows/refresh-references.yml` under `target=ar`.

Plugin scripts: `scripts/format-check.py` (Ark. R. Civ. P. 10/11 +
common-practice defaults; WARN where typography is a local-rule matter) ·
`scripts/case-calendar.py` (Ark. R. Civ. P. 6 deadline arithmetic with
Ark. Code Ann. § 1-5-101 holidays — including the combined Washington's
Birthday / Daisy Gatson Bates Day and Christmas Eve; `--rules` lists the
named-deadline catalog).

---
Part of the [claude-legal](../../README.md) marketplace. Skills are indexed in [CLAUDE.md](../../CLAUDE.md).
