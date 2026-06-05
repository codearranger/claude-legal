# court-rules Corpus — Arkansas

This corpus holds **verbatim text** of the Arkansas court rules most
relevant to civil practice. It is the canonical home for the rule text
that the `ar-court-docs` skills point at; the summaries in
`../civil-rules.md` and `../evidence-rules.md` describe these rules but
the **verbatim text here governs**.

> **Current status: VERBATIM.** This directory holds the **full verbatim
> text** of each rule set, extracted (`pdftotext -layout`) from the
> official Arkansas Judiciary Court Rules PDFs at
> `opinions.arcourts.gov/ark/cr/en/`. Each file's header records the
> source document URL and the rule count. Re-run `pull_arkansas_rules.py`
> (needs `pdftotext`/poppler) to refresh.

## Scope — what gets pulled here

| File (planned) | Source set | Notes |
|---|---|---|
| `Ark-Rules-Civil-Procedure.md` | **ARCP** (Ark. R. Civ. P.) | Rules 4, 5, 6, 8, 9, 10, 11, 12, 13, 15, 26–37, 55, 56, 59, 60, etc. — the civil-practice backbone |
| `Ark-Rules-Evidence.md` | **Ark. R. Evid.** | 401–403, 801–807 (esp. **803(6)**), 901, **902(11)** |
| `Ark-District-Court-Rules.md` | **Arkansas District Court Rules** (formerly Inferior Court Rules) | Limited-jurisdiction + small claims + the de novo appeal to Circuit Court |
| `Ark-Supreme-Court-Rules.md` | **Rules of the Supreme Court and Court of Appeals** | incl. **Ark. Sup. Ct. R. 5-2** (medium-neutral citation) and **R. 4-1 / 4-2** (appellate-brief format) |
| `Ark-Administrative-Orders.md` | **Administrative Orders** | esp. **No. 10** (child-support guidelines / Family Support Chart), **No. 19** (access to court records / redaction), **No. 21** (electronic filing / eFlex) |

## Citation forms (for the pulled content)

- Civil rule: `Ark. R. Civ. P. 12(b)(6)`
- Evidence rule: `Ark. R. Evid. 803(6)`
- Supreme Court rule: `Ark. Sup. Ct. R. 5-2`
- District Court rule: `Ark. Dist. Ct. R. [N]` [verify abbreviation]
- Administrative Order: `Ark. Sup. Ct. Admin. Order No. 19`

## Access posture

The **bare rule text is a public-domain edict** of the Arkansas
Supreme Court; only commercial annotated compilations (LexisNexis) are
copyrighted, and only as to the annotations. The Arkansas Judiciary
publishes the full text of each rule set as a PDF on its official
Lexum-powered Court Rules database at **opinions.arcourts.gov/ark/cr/en/**
(linked from arcourts.gov) — each rule set is one document at
`/ark/cr/en/<docid>/1/document.do`.

## How to re-pull

Run `scripts/pull_arkansas_rules.py`, which discovers the current
document id for each rule set by title from the collection's browse
listing, downloads the PDF, extracts text with `pdftotext -layout`
(poppler), splits it on `Rule N.` headings, and writes one Markdown file
per rule set atomically. Needs `pdftotext` (poppler-utils). Wire it into
the quarterly `refresh-references` workflow under `target=ar`. Expected
invocation:

```bash
python3 scripts/pull_arkansas_rules.py \
  --out plugins/ar-court-docs/skills/ar-law-references/references/court-rules
```

On a successful pull, update `_manifest.json` (version + `last_pulled`)
and bump the `ar-law-references` `SKILL.md` `version:` (PATCH for a
routine refresh, MINOR if a new rule-set file is added).
