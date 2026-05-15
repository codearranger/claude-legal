#!/usr/bin/env python3
"""Pull Ohio court-rule canonical sources and convert each to a
verbatim Markdown file.

Output: plugins/oh-court-docs/skills/oh-law-references/references/court-rules/

## Targets (all consolidated PDFs at supremecourt.ohio.gov)

  CivilProcedure.md     — Ohio Rules of Civil Procedure (Civ. R.)
  Evidence.md           — Ohio Rules of Evidence (Evid. R.)
  AppellateProcedure.md — Ohio Rules of Appellate Procedure (App. R.)
  CriminalProcedure.md  — Ohio Rules of Criminal Procedure (Crim. R.)
  JuvenileProcedure.md  — Ohio Rules of Juvenile Procedure (Juv. R.)
  Traffic.md            — Ohio Traffic Rules
  Superintendence.md    — Ohio Rules of Superintendence
                          (Sup. R. — chambers practice + reporting
                           requirements + case-management standards)
  RulesOfPractice.md    — Ohio Rules of Practice of the Supreme Court
                          (Sup. Ct. Prac. R.)
  ProfessionalConduct.md — Ohio Rules of Professional Conduct
                            (Prof. Cond. R.)
  JudicialConduct.md    — Ohio Code of Judicial Conduct
                          (Code of Jud. Cond.)
  GovBar.md             — Rules for the Government of the Bar of Ohio
                          (Gov. Bar R.)
  GovJud.md             — Rules for the Government of the Judiciary
                          of Ohio (Gov. Jud. R.)
  Reporting.md          — Rules of Reporting (Rep. R.)
  CourtOfClaims.md      — Court of Claims local rules

Source PDFs published by the Supreme Court of Ohio at
`https://www.supremecourt.ohio.gov/docs/LegalResources/Rules/`
and (for Court of Claims local rules) at
`https://ohiocourtofclaims.gov`. No authentication, no
Cloudflare gate.

Conversion: `pdftotext -layout` and emit the resulting text
under a standard Markdown header block.

## Dependencies
- Python 3.10+ stdlib
- `pdftotext` from poppler (`brew install poppler` /
  `apt-get install -y poppler-utils`)

## Usage
    python3 scripts/pull_ohio_court_rules.py --workers 4
    python3 scripts/pull_ohio_court_rules.py --only CivilProcedure
"""

from __future__ import annotations

import argparse
import json
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional

USER_AGENT = (
    "claude-legal/1.0 (+https://github.com/codearranger/claude-legal) "
    "oh-court-rules-puller"
)

SC_BASE = "https://www.supremecourt.ohio.gov/docs/LegalResources/Rules"


# ----------------------------------------------------------------------
# Networking.
# ----------------------------------------------------------------------

def http_get_bytes(url: str, *, retries: int = 4,
                    base_sleep: float = 1.5,
                    timeout: float = 60.0) -> bytes:
    """Fetch a URL with jittered exponential-backoff retries."""
    req_headers = {"User-Agent": USER_AGENT}
    parsed = urllib.parse.urlsplit(url)
    safe_path = urllib.parse.quote(parsed.path, safe="/%()'")
    safe_url = urllib.parse.urlunsplit(
        (parsed.scheme, parsed.netloc, safe_path,
         parsed.query, parsed.fragment)
    )
    req = urllib.request.Request(safe_url, headers=req_headers)
    last_exc: Optional[BaseException] = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except (urllib.error.URLError, TimeoutError,
                ConnectionError) as exc:
            last_exc = exc
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
        sleep_for = base_sleep * (2 ** attempt) * (0.5 + random.random())
        time.sleep(sleep_for)
    assert last_exc is not None
    raise last_exc


# ----------------------------------------------------------------------
# PDF → text.
# ----------------------------------------------------------------------

def pdf_bytes_to_layout_text(pdf_bytes: bytes) -> str:
    """Run `pdftotext -layout <stdin> -` and return the text."""
    with tempfile.TemporaryDirectory(prefix="oh-rules-pdf-") as td:
        pdf_path = Path(td) / "source.pdf"
        pdf_path.write_bytes(pdf_bytes)
        proc = subprocess.run(
            ["pdftotext", "-layout", str(pdf_path), "-"],
            check=True, capture_output=True,
        )
        return proc.stdout.decode("utf-8", errors="replace")


def strip_form_feeds(text: str) -> str:
    """Replace form-feed characters with blank lines."""
    return text.replace("\x0c", "\n")


# ----------------------------------------------------------------------
# Rendering.
# ----------------------------------------------------------------------

HEADER_BLOCK = """# {title}

> **Source:** {source}
> **Fetched:** {fetched}
> **Format:** verbatim conversion of the official PDF source

> **NOT LEGAL ADVICE.** Generated content is a drafting aid;
> verify against the current rules before filing.

---

"""


def render_md(title: str, source: str, fetched: str,
              body: str) -> str:
    header = HEADER_BLOCK.format(title=title, source=source,
                                  fetched=fetched)
    rendered = header + body.rstrip() + "\n"
    rendered = re.sub(r"\n{3,}", "\n\n", rendered)
    return rendered


# ----------------------------------------------------------------------
# Rule specs.
# ----------------------------------------------------------------------

@dataclass
class RuleSpec:
    code: str       # output filename stem ("CivilProcedure")
    title: str      # Markdown H1
    url: str        # source PDF URL


SPECS: List[RuleSpec] = [
    RuleSpec("CivilProcedure",
             "Ohio Rules of Civil Procedure (Civ. R.)",
             f"{SC_BASE}/civil/CivilProcedure.pdf"),
    RuleSpec("Evidence",
             "Ohio Rules of Evidence (Evid. R.)",
             f"{SC_BASE}/evidence/evidence.pdf"),
    RuleSpec("AppellateProcedure",
             "Ohio Rules of Appellate Procedure (App. R.)",
             f"{SC_BASE}/appellate/AppellateProcedure.pdf"),
    RuleSpec("CriminalProcedure",
             "Ohio Rules of Criminal Procedure (Crim. R.)",
             f"{SC_BASE}/criminal/CriminalProcedure.pdf"),
    RuleSpec("JuvenileProcedure",
             "Ohio Rules of Juvenile Procedure (Juv. R.)",
             f"{SC_BASE}/juvenile/JuvenileProcedure.pdf"),
    RuleSpec("Traffic",
             "Ohio Traffic Rules (Traf. R.)",
             f"{SC_BASE}/traffic/Traffic.pdf"),
    RuleSpec("Superintendence",
             "Ohio Rules of Superintendence (Sup. R.)",
             f"{SC_BASE}/superintendence/Superintendence.pdf"),
    RuleSpec("RulesOfPractice",
             "Ohio Rules of Practice of the Supreme Court (Sup. Ct. Prac. R.)",
             f"{SC_BASE}/practice/rulesofpractice.pdf"),
    RuleSpec("ProfessionalConduct",
             "Ohio Rules of Professional Conduct (Prof. Cond. R.)",
             f"{SC_BASE}/professional/professional.pdf"),
    RuleSpec("JudicialConduct",
             "Ohio Code of Judicial Conduct (Code of Jud. Cond.)",
             f"{SC_BASE}/conduct/judcond0309.pdf"),
    RuleSpec("GovBar",
             "Rules for the Government of the Bar of Ohio (Gov. Bar R.)",
             f"{SC_BASE}/govbar/govbar.pdf"),
    RuleSpec("GovJud",
             "Rules for the Government of the Judiciary of Ohio (Gov. Jud. R.)",
             f"{SC_BASE}/government/GOVJUD.pdf"),
    RuleSpec("Reporting",
             "Ohio Rules of Reporting (Rep. R.)",
             f"{SC_BASE}/reporting/Report.pdf"),
    RuleSpec("CourtOfClaims",
             "Ohio Court of Claims Local Rules",
             "https://ohiocourtofclaims.gov/wp-content/uploads/2021/10/local-rules-2019.pdf"),
]


# ----------------------------------------------------------------------
# Output.
# ----------------------------------------------------------------------

@dataclass
class RuleResult:
    code: str
    path: Path
    bytes_written: int
    error: Optional[str]


def write_rule(spec: RuleSpec, out_dir: Path,
                fetched_iso: str) -> RuleResult:
    """Fetch + convert + atomically write one rule set."""
    out_path = out_dir / f"{spec.code}.md"
    try:
        data = http_get_bytes(spec.url)
        text = strip_form_feeds(pdf_bytes_to_layout_text(data))
        rendered = render_md(spec.title, spec.url, fetched_iso, text)
    except Exception as exc:  # noqa: BLE001
        if not out_path.exists():
            stub = (
                f"# {spec.title}\n\n"
                f"> **Source:** {spec.url}\n"
                f"> **Fetched:** {fetched_iso}\n"
                f"> **Status:** _(fetch failed)_ — "
                f"{type(exc).__name__}: {exc}\n"
            )
            tmp = out_path.with_suffix(".md.tmp")
            tmp.write_text(stub, encoding="utf-8")
            tmp.rename(out_path)
        return RuleResult(spec.code, out_path,
                           out_path.stat().st_size
                           if out_path.exists() else 0,
                           f"{exc}")
    tmp = out_path.with_suffix(".md.tmp")
    tmp.write_text(rendered, encoding="utf-8")
    tmp.rename(out_path)
    return RuleResult(spec.code, out_path,
                       out_path.stat().st_size, None)


# ----------------------------------------------------------------------
# Manifest.
# ----------------------------------------------------------------------

def update_manifest(out_dir: Path, fetched_iso: str,
                     new_version: str = "0.1.0") -> Optional[Path]:
    manifest_path = out_dir / "_manifest.json"
    payload = {
        "version": new_version,
        "last_pulled": fetched_iso,
        "source": "https://www.supremecourt.ohio.gov/docs/LegalResources/Rules/",
        "notes": (
            "Pulled by scripts/pull_ohio_court_rules.py. "
            "Supreme Court of Ohio publishes all rules of "
            "court as consolidated PDFs; no API key or proxy "
            "required."
        ),
    }
    manifest_path.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    return manifest_path


# ----------------------------------------------------------------------
# CLI.
# ----------------------------------------------------------------------

def _verify_pdftotext_available() -> None:
    if shutil.which("pdftotext") is None:
        print(
            "!! pdftotext not on PATH — install poppler "
            "(brew install poppler / apt-get install -y poppler-utils).",
            file=sys.stderr,
        )
        sys.exit(2)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--out",
        type=Path,
        default=Path(
            "plugins/oh-court-docs/skills/oh-law-references/"
            "references/court-rules"
        ),
        help="Output directory for the corpus.",
    )
    ap.add_argument(
        "--only", nargs="*",
        help="Restrict to these rule-set codes.",
    )
    ap.add_argument(
        "--workers", type=int, default=3,
        help="Concurrent PDF fetches (default 3).",
    )
    ap.add_argument(
        "--manifest-version", default="0.1.0",
        help="Version to write into _manifest.json on success.",
    )
    args = ap.parse_args()

    _verify_pdftotext_available()

    out_dir: Path = args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    only = set(args.only) if args.only else None
    targets = [s for s in SPECS if only is None or s.code in only]
    if not targets:
        print(f"!! no rule sets match --only {args.only!r}",
              file=sys.stderr)
        return 2

    fetched_iso = date.today().isoformat()
    print(f"=== pulling {len(targets)} OH rule set(s) → "
          f"{out_dir} (workers={args.workers})", flush=True)

    results: List[RuleResult] = []
    workers = max(1, min(args.workers, len(targets)))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(write_rule, spec, out_dir, fetched_iso): spec
            for spec in targets
        }
        for fut in as_completed(futures):
            spec = futures[fut]
            try:
                results.append(fut.result())
            except Exception as exc:  # noqa: BLE001
                results.append(RuleResult(
                    spec.code, out_dir / f"{spec.code}.md",
                    0, str(exc),
                ))

    by_code = {r.code: r for r in results}
    ordered = [by_code[s.code] for s in targets if s.code in by_code]
    for spec, r in zip(targets, ordered):
        tag = "OK  " if r.error is None else "FAIL"
        print(f"     [{tag}] {spec.code}.md "
              f"({r.bytes_written:,} bytes)"
              + (f" — {r.error}" if r.error else ""),
              flush=True)

    fail = [r for r in ordered if r.error is not None]
    total_bytes = sum(r.bytes_written for r in ordered
                       if r.error is None)
    print(f"\n=== wrote {len(ordered) - len(fail)} rule set(s), "
          f"{total_bytes:,} bytes; {len(fail)} failed",
          flush=True)

    if only is None and not fail:
        mp = update_manifest(out_dir, fetched_iso,
                              args.manifest_version)
        if mp is not None:
            print(f"=== updated {mp}", flush=True)

    return 0 if not fail else 1


if __name__ == "__main__":
    sys.exit(main())
