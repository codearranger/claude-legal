#!/usr/bin/env python3
"""Pull the Foreign Affairs Manual (FAM) — immigration-relevant volumes.

The FAM is the State Department's internal guidance, published at
https://fam.state.gov. For immigration practice the relevant volumes are:

  - 9 FAM  — Visas (nonimmigrant + immigrant visa adjudication; the
             Department's interpretation of INA admissibility/ineligibility,
             e.g. 9 FAM 302 ineligibilities, 9 FAM 402 NIV classifications,
             9 FAM 504 IV processing). This is the single most-cited FAM
             volume for immigration lawyers.
  - 8 FAM  — Nationality and Naturalization (acquisition/derivation of
             U.S. citizenship through consular determinations).
  - 7 FAM  — Consular Affairs (U.S. citizenship, passports, Consular
             Reports of Birth Abroad, death/estate matters).

fam.state.gov is JavaScript-rendered and fronted by bot mitigation that
returns 503 to scripted clients (stdlib urllib, plain curl). When the fetch
succeeds the puller writes verbatim Markdown; when it is blocked it writes a
**well-formed pointer stub** carrying the canonical URL + a scope description,
mirroring scripts/pull_ny_court_rules.py and scripts/pull_tn_statutes.py.

The `_file_is_stub` regression guard means a stub-only re-run will NOT clobber
verbatim content that a previous (successful) run committed. The canonical way
to refresh verbatim FAM text is to run this puller from an environment that can
reach fam.state.gov (e.g. a browser-impersonating client / proxy) and commit
the diff.

Output: plugins/claude-legal-immigration-laws/references/foreign-affairs-manual/
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

FAM_BASE = "https://fam.state.gov"

# Row: (out_file, title, canonical_url, scope).
FamRow = tuple[str, str, str, str]
FAM_TARGETS: list[FamRow] = [
    ("09FAM-visas-overview", "9 FAM — Visas (overview)",
     "https://fam.state.gov/fam/09fam.html",
     "The Department of State's visa-adjudication manual: nonimmigrant and "
     "immigrant visa classifications, documentary requirements, and the "
     "Department's controlling interpretation of INA admissibility and "
     "ineligibility grounds applied by consular officers."),
    ("09FAM-302-ineligibilities", "9 FAM 302 — Ineligibilities and Waivers",
     "https://fam.state.gov/fam/09FAM/09FAM030200.html",
     "Section-by-section treatment of the INA § 212(a) inadmissibility "
     "grounds (health, criminal, security, public charge, misrepresentation, "
     "unlawful presence, etc.) and the corresponding waivers, as applied in "
     "visa adjudication."),
    ("09FAM-402-niv-classifications", "9 FAM 402 — Nonimmigrant Visa Classifications",
     "https://fam.state.gov/fam/09FAM/09FAM040200.html",
     "Classification-by-classification guidance for nonimmigrant visa "
     "categories (B, F, H, L, O, P, etc.): eligibility, documentary "
     "requirements, and adjudication standards."),
    ("09FAM-502-504-iv-processing", "9 FAM 502 / 504 — Immigrant Visa Categories and Processing",
     "https://fam.state.gov/fam/09FAM/09FAM050200.html",
     "Immigrant visa categories (family-based, employment-based, diversity) "
     "and the National Visa Center / consular immigrant-visa processing "
     "workflow."),
    ("08FAM-nationality", "8 FAM — Nationality and Naturalization",
     "https://fam.state.gov/fam/08fam.html",
     "Acquisition and derivation of U.S. citizenship as determined by the "
     "Department of State (birth abroad, transmission requirements, "
     "expatriation, Consular Reports of Birth Abroad)."),
    ("07FAM-consular-affairs", "7 FAM — Consular Affairs",
     "https://fam.state.gov/fam/07fam.html",
     "U.S. citizenship services abroad: passports, Consular Reports of Birth "
     "Abroad, registration, and related citizen-services guidance."),
]


def http_get(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


STUB_MARKER = "<!-- claude-legal:fam-pointer-stub -->"


def _file_is_stub(path: Path) -> bool:
    if not path.exists():
        return True
    try:
        return STUB_MARKER in path.read_text(encoding="utf-8")
    except OSError:
        return True


def make_stub(title: str, url: str, scope: str) -> str:
    today = date.today().isoformat()
    return (
        f"# {title}\n\n"
        f"{STUB_MARKER}\n\n"
        f"- Citation: Foreign Affairs Manual (FAM), U.S. Department of State\n"
        f"- Canonical URL: {url}\n"
        f"- Status: **pointer stub** — verbatim text not mirrored\n"
        f"- Pulled: {today}\n\n"
        f"> **Why a stub?** fam.state.gov is JavaScript-rendered and fronted by "
        f"bot mitigation that returns HTTP 503 to scripted clients, so this "
        f"corpus cannot be snapshotted from a CI runner. Read the authoritative "
        f"text at the canonical URL above. To mirror it verbatim, run "
        f"`scripts/pull_fam.py` from an environment that can reach fam.state.gov "
        f"(a browser-impersonating client or proxy); the `_file_is_stub` guard "
        f"will replace this stub with the fetched text.\n\n"
        f"## Scope\n\n{scope}\n\n"
        f"## Note on FAM authority\n\n"
        f"The FAM is internal Department of State guidance. It is **not** "
        f"binding law and does not create enforceable rights, but it is highly "
        f"persuasive of the agency's interpretation of the INA and 22 CFR and "
        f"is routinely cited in visa-refusal and consular-processing matters. "
        f"Always pair a FAM cite with the controlling statute (INA / 8 U.S.C.) "
        f"and regulation (8 CFR / 22 CFR).\n"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out",
        default="plugins/claude-legal-immigration-laws/references/foreign-affairs-manual",
    )
    ap.add_argument("--stubs-only", action="store_true",
                    help="Skip the network fetch and (re)write pointer stubs.")
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    wrote_verbatim, wrote_stub, preserved = 0, 0, 0
    for (out_file, title, url, scope) in FAM_TARGETS:
        path = out_dir / f"{out_file}.md"
        html = None
        if not args.stubs_only:
            try:
                raw = http_get(url)
                text = raw.decode("utf-8", errors="replace")
                # Heuristic: a real FAM page carries the section heading text,
                # not just a bot-block interstitial.
                if len(text) > 5000 and "FAM" in text and "503" not in text[:200]:
                    html = text
            except Exception as e:
                print(f"  ! fetch failed for {url}: {e}", flush=True)

        if html is not None:
            # Minimal HTML -> text reduction (FAM markup is shallow).
            body = re.sub(r"(?is)<script.*?</script>", " ", html)
            body = re.sub(r"(?is)<style.*?</style>", " ", body)
            body = re.sub(r"(?s)<[^>]+>", " ", body)
            body = re.sub(r"[ \t]+", " ", body)
            body = re.sub(r"\n{3,}", "\n\n", body).strip()
            md = (
                f"# {title}\n\n"
                f"- Citation: Foreign Affairs Manual (FAM), U.S. Department of State\n"
                f"- Canonical URL: {url}\n"
                f"- Pulled: {date.today().isoformat()}\n\n"
                f"> Verbatim text reduced from fam.state.gov HTML.\n\n"
                f"{body}\n"
            )
            path.write_text(md, encoding="utf-8")
            wrote_verbatim += 1
            print(f"  wrote VERBATIM {path} ({len(md):,} bytes)", flush=True)
        else:
            if not _file_is_stub(path):
                preserved += 1
                print(f"  preserved existing verbatim {path} (fetch blocked)", flush=True)
                continue
            path.write_text(make_stub(title, url, scope), encoding="utf-8")
            wrote_stub += 1
            print(f"  wrote STUB {path}", flush=True)

    manifest = {
        "version": "0.1.0",
        "last_pulled": date.today().isoformat(),
        "source": FAM_BASE,
        "mode": "stub" if wrote_verbatim == 0 else "mixed",
        "notes": (
            "Pulled by scripts/pull_fam.py. fam.state.gov is bot-gated (503 to "
            "scripted clients); the puller writes pointer stubs when blocked and "
            "verbatim text when reachable. The _file_is_stub guard preserves any "
            "committed verbatim content."
        ),
    }
    (out_dir / "_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(
        f"Done. verbatim={wrote_verbatim} stub={wrote_stub} preserved={preserved}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
