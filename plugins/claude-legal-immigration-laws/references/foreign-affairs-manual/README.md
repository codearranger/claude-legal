# Foreign Affairs Manual (FAM) — immigration-relevant volumes

The **Foreign Affairs Manual** is the U.S. Department of State's internal
guidance. It is **not binding law** and creates no enforceable rights, but it
is highly persuasive evidence of the Department's interpretation of the INA and
22 CFR, and it is routinely cited in visa-refusal, consular-processing, and
nationality matters. Always pair a FAM cite with the controlling statute
(INA / 8 U.S.C.) and regulation (8 CFR / 22 CFR).

- Pulled by: `scripts/pull_fam.py`
- Canonical source: <https://fam.state.gov>

## Status: verbatim

This corpus is mirrored **verbatim** from fam.state.gov. Two upstream quirks
that previously blocked mirroring are now handled by `scripts/pull_fam.py`:

1. **Incomplete TLS chain.** fam.state.gov serves only its leaf certificate and
   omits the issuing intermediate (*Sectigo Public Server Authentication CA OV
   R36*). A browser repairs this by *AIA fetching*; Python's `ssl` does not, so a
   default `urlopen` fails with `CERTIFICATE_VERIFY_FAILED`. This is the server's
   own misconfiguration — **not** an egress proxy or bot-gate — and is fixable
   from any machine. The puller opens an unverified handshake purely to read the
   leaf's Authority Information Access "CA Issuers" URL, downloads the
   intermediate, and adds it to a verify bundle (certifi roots + intermediate),
   after which every content fetch is fully TLS-verified.
2. **Stale URLs.** The old `/fam/*.html` paths are dead (404). The site is now an
   ASP.NET/Kendo app that serves its table of contents as JSON from
   `/api/Tree/GetTreeByVolumeId?Id=<vol>` and per-section content at
   `/FAM/<vol>/<sectionId>.html` (uppercase `/FAM/`, windows-1252 Word HTML). The
   puller crawls the tree API per volume and reduces each section page to
   Markdown.

To refresh:

```bash
python3 scripts/pull_fam.py            # all targets; --only <token> to limit
python3 scripts/pull_fam.py --stubs-only   # force pointer stubs (offline)
```

The `_file_is_stub` regression guard means a stub-only or network-unreachable
re-run will **not** clobber verbatim content a prior successful run committed.

### Scope

The puller mirrors the immigration-relevant slices of each volume, not whole
volumes (8 FAM and 7 FAM are mostly SBU/redacted or tangential to immigration):
9 FAM chapter 100 (overview) + 302 (ineligibilities) + 402 (NIV classes) +
502/504 (IV categories + processing); 8 FAM chapter 300 (the only substantive
public nationality chapter); 7 FAM 000 (consular-protection overview) + 1400
(documentation of major life events / CRBA). Sections marked "Unavailable"
upstream are mirrored as headings with a redaction note.

## Files

| File | Volume | Subject |
|---|---|---|
| [09FAM-visas-overview.md](09FAM-visas-overview.md) | 9 FAM | Visa adjudication manual (overview) |
| [09FAM-302-ineligibilities.md](09FAM-302-ineligibilities.md) | 9 FAM 302 | INA § 212(a) ineligibilities + waivers as applied by consular officers |
| [09FAM-402-niv-classifications.md](09FAM-402-niv-classifications.md) | 9 FAM 402 | Nonimmigrant visa classifications |
| [09FAM-502-504-iv-processing.md](09FAM-502-504-iv-processing.md) | 9 FAM 502/504 | Immigrant visa categories + NVC / consular processing |
| [08FAM-nationality.md](08FAM-nationality.md) | 8 FAM 300 | U.S. citizenship and nationality (acquisition, derivation, CRBA) |
| [07FAM-consular-affairs.md](07FAM-consular-affairs.md) | 7 FAM 000 / 1400 | Consular protection overview + documentation of major life events |

> **NOT LEGAL ADVICE.** The FAM is agency guidance, not law; verify against the
> current text at fam.state.gov and the controlling INA / CFR provisions.
