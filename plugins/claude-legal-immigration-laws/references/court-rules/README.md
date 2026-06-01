# Immigration court rules — EOIR

Procedural authority for practice before the **immigration courts** and the **Board of Immigration Appeals (BIA)** comes in two layers:

## 1. Binding regulations (LAW) — mirrored verbatim elsewhere

The enforceable rules live in **8 CFR**, already mirrored verbatim under [`../immigration-regulations/`](../immigration-regulations/):

- **Part 1003** — EOIR; the Board of Immigration Appeals; immigration-judge proceedings; motions before the Board and the IJ (`8CFR-1003-eoir-bia.md`)
- **Part 1240** — removal proceedings before EOIR (`8CFR-1240-removal-eoir.md`)
- **Part 1208** — asylum and withholding before EOIR (`8CFR-1208-asylum-eoir.md`)

Cite these for anything jurisdictional or substantive.

## 2. Practice manuals (procedural guidance) — pointer stubs here

EOIR publishes two procedural manuals at justice.gov. They are guidance, not law, but courts expect compliance with their filing-format and deadline rules:

| File | Manual | Canonical |
|---|---|---|
| [Immigration-Court-Practice-Manual.md](Immigration-Court-Practice-Manual.md) | ICPM | <https://www.justice.gov/eoir/reference-materials/ic> |
| [BIA-Practice-Manual.md](BIA-Practice-Manual.md) | BIAPM | <https://www.justice.gov/eoir/reference-materials/bia> |

These ship as **pointer stubs** because EOIR renders the manuals client-side (JavaScript) and Akamai-gates the chapter URLs, so verbatim text can't be mirrored from a stdlib client. Each stub carries the canonical chapter URLs and a cross-reference to the binding 8 CFR rules. Refresh with `scripts/pull_eoir_manuals.py`; the `_file_is_stub` guard preserves any verbatim content a future headless/un-gated run commits.

- Pulled by: `scripts/pull_eoir_manuals.py`
- Last updated: 2026-05-28

> **NOT LEGAL ADVICE.** Verify the current manual text and the controlling 8 CFR provision before filing.
