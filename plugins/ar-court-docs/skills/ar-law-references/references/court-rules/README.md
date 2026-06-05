# court-rules Corpus — Arkansas

This corpus holds **verbatim text** of the Arkansas court rules most
relevant to civil practice. It is the canonical home for the rule text
that the `ar-court-docs` skills point at; the summaries in
`../civil-rules.md` and `../evidence-rules.md` describe these rules but
the **verbatim text here governs**.

> **Current status: curated summaries (not yet verbatim).** This
> directory ships **curated, citation-rich structural summaries** of
> each rule set — every file is clearly labeled "CURATED SUMMARY — NOT
> VERBATIM" and points at the canonical **arcourts.gov** text. They were
> authored offline because the verbatim puller needs network access.
> Running `pull_arkansas_rules.py` from a networked environment replaces
> them with verbatim text (the `_file_is_stub` guard preserves the
> curated content until a successful pull supersedes it).

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
copyrighted, and only as to the annotations. The canonical publisher is
**arcourts.gov**. **courtrules.net** is a structured free mirror used
as a fallback when the official site is gated (the same pattern other
state pullers use).

## How to re-pull

Author / run `scripts/pull_arkansas_rules.py`, which fetches the rule
sets and Administrative Orders from **arcourts.gov** (fallback:
courtrules.net), converts to Markdown (one file per rule set), and
writes atomically. Wire it into the quarterly `refresh-references`
workflow under `target=ar`. Expected invocation:

```bash
python3 scripts/pull_arkansas_rules.py --workers 2 \
  --out plugins/ar-court-docs/skills/ar-law-references/references/court-rules
```

On a successful pull, update `_manifest.json` (version + `last_pulled`)
and bump the `ar-law-references` `SKILL.md` `version:` (PATCH for a
routine refresh, MINOR if a new rule-set file is added).
