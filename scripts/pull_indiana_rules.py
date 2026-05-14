#!/usr/bin/env python3
"""Pull Indiana court-rule canonical sources and convert each to a
verbatim Markdown file.

Output: plugins/in-court-docs/skills/in-law-references/references/court-rules/

Seven outputs total:

  Trial-Rules.md          — Indiana Rules of Trial Procedure (Ind. Trial R.)
                            Source: consolidated PDF at rules.incourts.gov
  Evidence-Rules.md       — Indiana Rules of Evidence (Ind. Evid. R.)
                            Source: consolidated PDF at rules.incourts.gov
  Appellate-Rules.md      — Indiana Rules of Appellate Procedure (Ind. App. R.)
                            Source: consolidated PDF at rules.incourts.gov
  Professional-Conduct.md — Indiana Rules of Professional Conduct
                            (Ind. R. Prof. Cond.)
                            Source: consolidated PDF at rules.incourts.gov
  Admin-Rules.md          — Indiana Rules for Administrative and Original
                            Actions / Administrative Rules (Ind. Admin. R.)
                            Source: consolidated PDF at rules.incourts.gov
  Marion-Local-Rules.md   — Marion County Local Court Rules (LR49)
                            Source: PDF at in.gov/courts/files/
  Lake-Local-Rules.md     — Lake County Local Court Rules (LR45)
                            Source: PDF at in.gov/courts/files/

Conversion approach: `pdftotext -layout` and emit the result verbatim
under a standard Markdown header block. The layout-mode output preserves
the document's column structure, which matters for rule numbering and
indentation.

The Indiana Supreme Court publishes all five state-wide rule sets as
consolidated PDFs on the publication site `rules.incourts.gov`. Local
rules for each county are published as PDFs under
`in.gov/courts/files/<county>-local-rules.pdf` by the Indiana Judicial
Branch (the per-county clerk's pages on indy.gov / lakecountyin.org link
to the same canonical PDFs). The script tracks the
state-publication-system URLs only, so no per-clerk URL discovery is
needed at refresh time.

Dependencies: poppler (`brew install poppler` / `apt-get install -y
poppler-utils`) for `pdftotext`. Stdlib for everything else.

Usage:
    python3 scripts/pull_indiana_rules.py \\
        --out plugins/in-court-docs/skills/in-law-references/references/court-rules

    # Refresh one rule set:
    python3 scripts/pull_indiana_rules.py --only Evidence-Rules
    python3 scripts/pull_indiana_rules.py --only Trial-Rules Appellate-Rules
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
    "indiana-rules-puller"
)


# ----------------------------------------------------------------------
# Networking.
# ----------------------------------------------------------------------

def http_get_bytes(url: str, *, headers: Optional[Dict[str, str]] = None,
                    retries: int = 4, base_sleep: float = 1.5,
                    timeout: float = 60.0) -> bytes:
    """Fetch a URL with jittered exponential-backoff retries.

    Same pattern as pull_oregon_rules.py / pull_co_statutes.py — the
    upstream nginx (rules.incourts.gov via volt-adc) occasionally drops
    long-lived connections under bulk fetch, and we'd rather sleep and
    retry than abort a quarterly refresh."""
    req_headers = {"User-Agent": USER_AGENT}
    if headers:
        req_headers.update(headers)
    # Quote any spaces / unsafe chars in path; preserve query as-is.
    # The IN PDF paths contain literal spaces ("PDF - Trial/trial.pdf").
    parsed = urllib.parse.urlsplit(url)
    safe_path = urllib.parse.quote(parsed.path, safe="/%()'")
    safe_url = urllib.parse.urlunsplit(
        (parsed.scheme, parsed.netloc, safe_path, parsed.query, parsed.fragment)
    )
    req = urllib.request.Request(safe_url, headers=req_headers)
    last_exc: Optional[BaseException] = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
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
    """Run `pdftotext -layout <stdin> -` and return the resulting text.

    `pdftotext` accepts `-` as either the input or output path for
    stdin/stdout. We write to a temp file rather than streaming because
    poppler's stdin handling is finicky with large PDFs; the temp-file
    detour costs us nothing and matches pull_oregon_rules.py's pattern.
    """
    with tempfile.TemporaryDirectory(prefix="in-rules-pdf-") as td:
        td_path = Path(td)
        pdf_path = td_path / "source.pdf"
        pdf_path.write_bytes(pdf_bytes)
        proc = subprocess.run(
            ["pdftotext", "-layout", str(pdf_path), "-"],
            check=True,
            capture_output=True,
        )
        return proc.stdout.decode("utf-8", errors="replace")


def strip_form_feeds(text: str) -> str:
    """Replace form-feed characters with a blank line for readability."""
    return text.replace("\x0c", "\n")


# ----------------------------------------------------------------------
# Rendering.
# ----------------------------------------------------------------------

HEADER_BLOCK = """# {title}

> **Source:** {source}
> **Fetched:** {fetched}
> **Format:** verbatim conversion of the official PDF source

> **NOT LEGAL ADVICE.** Generated content is a drafting aid; verify
> against the current rules before filing.

---

"""


def render_md(title: str, source: str, fetched: str, body: str) -> str:
    """Wrap a body string with the canonical Markdown header block."""
    header = HEADER_BLOCK.format(title=title, source=source, fetched=fetched)
    rendered = header + body.rstrip() + "\n"
    rendered = re.sub(r"\n{3,}", "\n\n", rendered)
    return rendered


# ----------------------------------------------------------------------
# Rule specs.
# ----------------------------------------------------------------------

# Five state-wide rule sets are published as consolidated PDFs on the
# Indiana Supreme Court's rule-publication site (rules.incourts.gov).
# Local-rule PDFs are served by the Indiana Judicial Branch's main
# www.in.gov asset host. Both hosts return content-disposition: pdf and
# the URLs are stable across publication-cycle updates (the PDF body
# changes; the URL does not).
RULES_HOST = "https://rules.incourts.gov"
IN_GOV_FILES = "https://www.in.gov/courts/files"


@dataclass
class RuleSpec:
    code: str           # output filename stem ("Trial-Rules", ...)
    title: str          # Markdown H1
    url: str            # source PDF URL


SPECS: List[RuleSpec] = [
    RuleSpec(
        "Trial-Rules",
        "Indiana Rules of Trial Procedure (Ind. Trial R.)",
        f"{RULES_HOST}/pdf/PDF - Trial/trial.pdf",
    ),
    RuleSpec(
        "Evidence-Rules",
        "Indiana Rules of Evidence (Ind. Evid. R.)",
        f"{RULES_HOST}/pdf/PDF - Evidence/evidence.pdf",
    ),
    RuleSpec(
        "Appellate-Rules",
        "Indiana Rules of Appellate Procedure (Ind. App. R.)",
        f"{RULES_HOST}/pdf/PDF - Appellate/appellate.pdf",
    ),
    RuleSpec(
        "Professional-Conduct",
        "Indiana Rules of Professional Conduct (Ind. R. Prof. Cond.)",
        f"{RULES_HOST}/pdf/PDF - Professional Conduct/professional-conduct.pdf",
    ),
    RuleSpec(
        "Admin-Rules",
        "Indiana Administrative Rules (Ind. Admin. R.)",
        f"{RULES_HOST}/pdf/PDF - Admin/admin.pdf",
    ),
    RuleSpec(
        "Marion-Local-Rules",
        "Marion County Local Court Rules (LR49)",
        f"{IN_GOV_FILES}/marion-local-rules.pdf",
    ),
    RuleSpec(
        "Lake-Local-Rules",
        "Lake County Local Court Rules (LR45)",
        f"{IN_GOV_FILES}/lake-local-rules.pdf",
    ),
]


# ----------------------------------------------------------------------
# Output writing.
# ----------------------------------------------------------------------

@dataclass
class RuleResult:
    code: str
    path: Path
    bytes_written: int
    error: Optional[str]


def write_rule(spec: RuleSpec, out_dir: Path, fetched_iso: str
                ) -> RuleResult:
    """Fetch + convert + atomically write one rule set to disk.

    On a fetch / conversion failure, we leave any existing file in place
    untouched (and only write a placeholder stub if nothing's already
    there). This means a transient upstream blip during a quarterly
    refresh won't clobber a previously-good corpus."""
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
                          out_path.stat().st_size if out_path.exists() else 0,
                          f"{exc}")
    tmp = out_path.with_suffix(".md.tmp")
    tmp.write_text(rendered, encoding="utf-8")
    tmp.rename(out_path)
    return RuleResult(spec.code, out_path, out_path.stat().st_size, None)


# ----------------------------------------------------------------------
# Manifest update (best-effort; the IN corpus may not have one yet).
# ----------------------------------------------------------------------

def update_manifest(out_dir: Path, fetched_iso: str,
                     new_version: str = "0.2.0") -> Optional[Path]:
    """Bump version + last_pulled in place via regex, preserving the
    existing JSON formatting (indentation, key order, unicode chars)."""
    manifest_path = out_dir / "_manifest.json"
    if not manifest_path.exists():
        return None
    try:
        raw = manifest_path.read_text(encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        print(f"  ! could not read {manifest_path}: {exc}", flush=True)
        return None
    updated = re.sub(
        r'("version"\s*:\s*")[^"]*(")',
        lambda m: f'{m.group(1)}{new_version}{m.group(2)}',
        raw, count=1,
    )
    updated = re.sub(
        r'("last_pulled"\s*:\s*")[^"]*(")',
        lambda m: f'{m.group(1)}{fetched_iso}{m.group(2)}',
        updated, count=1,
    )
    try:
        json.loads(updated)
    except Exception as exc:  # noqa: BLE001
        print(f"  ! manifest update produced invalid JSON; "
              f"leaving {manifest_path} untouched: {exc}", flush=True)
        return None
    manifest_path.write_text(updated, encoding="utf-8")
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
            "plugins/in-court-docs/skills/in-law-references/"
            "references/court-rules"
        ),
        help="Output directory for the corpus (default matches the "
             "canonical IN plugin location).",
    )
    ap.add_argument(
        "--only",
        nargs="*",
        help="Restrict to these rule-set codes "
             "(e.g. --only Evidence-Rules Trial-Rules).",
    )
    ap.add_argument(
        "--workers",
        type=int,
        default=3,
        help="Concurrent PDF fetches (default 3; each fetch is one "
             "PDF, and pdftotext is CPU-bound, so values much above 4 "
             "rarely help).",
    )
    ap.add_argument(
        "--manifest-version",
        default="0.2.0",
        help="Version to write into _manifest.json on success "
             "(default 0.2.0).",
    )
    args = ap.parse_args()

    _verify_pdftotext_available()

    out_dir: Path = args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    only = set(args.only) if args.only else None
    targets = [s for s in SPECS if only is None or s.code in only]
    if not targets:
        print(f"!! no rule sets match --only {args.only!r}", file=sys.stderr)
        return 2

    fetched_iso = date.today().isoformat()
    print(f"=== pulling {len(targets)} IN rule set(s) → {out_dir} "
          f"(workers={args.workers})", flush=True)

    results: List[RuleResult] = []
    workers = max(1, min(args.workers, len(targets)))
    if workers == 1:
        for spec in targets:
            print(f"  -> {spec.code} ...", flush=True)
            results.append(write_rule(spec, out_dir, fetched_iso))
    else:
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
                    results.append(RuleResult(spec.code,
                                                out_dir / f"{spec.code}.md",
                                                0, str(exc)))

    # Stable per-spec order for the summary log.
    by_code = {r.code: r for r in results}
    ordered = [by_code[s.code] for s in targets if s.code in by_code]
    for spec, r in zip(targets, ordered):
        tag = "OK " if r.error is None else "FAIL"
        print(f"     [{tag}] {spec.code}.md "
              f"({r.bytes_written:,} bytes)"
              + (f" — {r.error}" if r.error else ""),
              flush=True)

    ok = [r for r in ordered if r.error is None]
    fail = [r for r in ordered if r.error is not None]
    total_bytes = sum(r.bytes_written for r in ok)
    print(f"\n=== wrote {len(ok)} rule set(s), "
          f"{total_bytes:,} bytes; {len(fail)} failed", flush=True)
    if fail:
        for r in fail:
            print(f"  - {r.code}: {r.error}", flush=True)

    if only is None and not fail:
        mp = update_manifest(out_dir, fetched_iso, args.manifest_version)
        if mp is not None:
            print(f"=== updated {mp} → version "
                  f"{args.manifest_version}, last_pulled {fetched_iso}",
                  flush=True)

    return 0 if not fail else 1


if __name__ == "__main__":
    sys.exit(main())
