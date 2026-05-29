# Foreign Affairs Manual (FAM) — immigration-relevant volumes

The **Foreign Affairs Manual** is the U.S. Department of State's internal
guidance. It is **not binding law** and creates no enforceable rights, but it
is highly persuasive evidence of the Department's interpretation of the INA and
22 CFR, and it is routinely cited in visa-refusal, consular-processing, and
nationality matters. Always pair a FAM cite with the controlling statute
(INA / 8 U.S.C.) and regulation (8 CFR / 22 CFR).

- Pulled by: `scripts/pull_fam.py`
- Canonical source: <https://fam.state.gov>

## Status: pointer stubs

`fam.state.gov` is JavaScript-rendered and fronted by bot mitigation that
returns **HTTP 503** to scripted clients, so this corpus currently ships as
**well-formed pointer stubs** — each file carries the canonical URL plus a
scope description — rather than mirrored verbatim text. This mirrors how the
NY court-rules and TN statutes corpora handle Cloudflare-gated upstreams.

To mirror FAM verbatim, run the puller from an environment that can reach
fam.state.gov (a browser-impersonating client or proxy):

```bash
python3 scripts/pull_fam.py
```

The `_file_is_stub` regression guard will replace a stub with fetched text and
will **not** clobber verbatim content a prior successful run committed.

## Files

| File | Volume | Subject |
|---|---|---|
| [09FAM-visas-overview.md](09FAM-visas-overview.md) | 9 FAM | Visa adjudication manual (overview) |
| [09FAM-302-ineligibilities.md](09FAM-302-ineligibilities.md) | 9 FAM 302 | INA § 212(a) ineligibilities + waivers as applied by consular officers |
| [09FAM-402-niv-classifications.md](09FAM-402-niv-classifications.md) | 9 FAM 402 | Nonimmigrant visa classifications |
| [09FAM-502-504-iv-processing.md](09FAM-502-504-iv-processing.md) | 9 FAM 502/504 | Immigrant visa categories + NVC / consular processing |
| [08FAM-nationality.md](08FAM-nationality.md) | 8 FAM | Nationality and naturalization (consular) |
| [07FAM-consular-affairs.md](07FAM-consular-affairs.md) | 7 FAM | Consular affairs: passports, CRBA, citizen services |

> **NOT LEGAL ADVICE.** The FAM is agency guidance, not law; verify against the
> current text at fam.state.gov and the controlling INA / CFR provisions.
