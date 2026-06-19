# court-rules Corpus — Idaho

> **NOT LEGAL ADVICE.** Reference corpus. Confirm every rule against the
> canonical isc.idaho.gov page and check for pending amendments before
> relying on it.

This corpus holds the Idaho court-rules content most relevant to civil and
family practice. It is **populated verbatim by a future
`scripts/pull_idaho_rules.py`** that fetches from the Idaho Supreme Court
(`isc.idaho.gov`) rules pages.

## Current state — pointer stubs (mode `stub`)

Until the puller runs, this directory holds **well-formed pointer-stub
digests** (header + canonical URL + scope note) for each rule set. They are
**not** verbatim rule text — they direct you to the canonical isc.idaho.gov
source. See `_manifest.json` for the corpus mode, version, and intended
targets.

## Pointer-stub files

- `IRCP-civil-procedure.md` — Idaho Rules of Civil Procedure (I.R.C.P.)
- `IRE-evidence.md` — Idaho Rules of Evidence (I.R.E.)
- `IRFLP-family-law-procedure.md` — Idaho Rules of Family Law Procedure (I.R.F.L.P.)
- `IAR-appellate.md` — Idaho Appellate Rules (I.A.R.)

The **I.R.E.F.S.** (Idaho Rules for Electronic Filing and Service) is also an
intended pull target (see `_manifest.json`); its e-filing mechanics are
summarized in the host skill's `SKILL.md` and `online-sources.md`.

## How it will be populated

`scripts/pull_idaho_rules.py` will fetch the per-rule pages from
`isc.idaho.gov` (print pattern `https://isc.idaho.gov/rules-procedure/print/ircp/<n>`
and the `https://isc.idaho.gov/ircp<n>-new` pages, plus the I.R.E. / I.R.F.L.
/ I.R.E.F.S. rule-set landings), convert them to Markdown, and write verbatim
text here — replacing these stubs. A `_file_is_stub` guard should preserve any
committed verbatim content on a failed run.
