#!/usr/bin/env python3
"""Pull Oregon court-rule canonical sources and convert each to a
verbatim Markdown file.

Output: plugins/or-court-docs/skills/or-law-references/references/court-rules/

Seven outputs total, mirroring the existing hand-authored corpus:

  ORCP.md           — Oregon Rules of Civil Procedure
                      Source: HTML at oregonlegislature.gov/bills_laws/SiteAssets/ORCP.html
                      (the Council on Court Procedures' canonical link)
  UTCR.md           — Uniform Trial Court Rules
                      Source: monolithic annual-edition PDF in the OJD SharePoint
                      asset library (list 'UTCR'); script picks the highest-Id
                      list item whose Title is "2025 UTCR (PDF)" or similar.
  ORAP.md           — Oregon Rules of Appellate Procedure
                      Source: SharePoint list 'ORAP'; script picks the highest-Id
                      list item whose Title is "Oregon Rules of Appellate Procedure".
  OEC.md            — Oregon Evidence Code (ORS Chapter 40)
                      Source: HTML at oregonlegislature.gov (same as the ORS puller).
  ORPC.md           — Oregon Rules of Professional Conduct
                      Source: PDF at osbar.org/_docs/rulesregs/orpc.pdf.
  Multnomah-SLR.md  — Multnomah County SLR
                      Source: SharePoint list 'LCR'; script picks the highest-Id
                      item whose File.Name begins with "Multnomah_SLR".
  Washington-SLR.md — Washington County (OR) SLR
                      Source: SharePoint list 'LCR'; script picks the highest-Id
                      item whose File.Name begins with "Washington_SLR".

Conversion approach:
  - HTML sources (ORCP, OEC): paragraph-walk the Microsoft Word "filtered
    HTML" output and emit each <p> as one Markdown paragraph, matching
    the format produced by PR #6.
  - PDF sources (UTCR, ORAP, ORPC, Multnomah-SLR, Washington-SLR):
    `pdftotext -layout` and emit the result verbatim under a standard
    Markdown header block. The layout-mode output preserves the
    document's column structure, which matters for rule numbering and
    indentation.

Dependencies: poppler (`brew install poppler` / `apt-get install -y
poppler-utils`) for `pdftotext`. Stdlib for everything else.

Usage:
    python3 scripts/pull_oregon_rules.py \\
        --out plugins/or-court-docs/skills/or-law-references/references/court-rules

    # Refresh one rule set:
    python3 scripts/pull_oregon_rules.py --only OEC --out /tmp/or-rules-test
    python3 scripts/pull_oregon_rules.py --only UTCR ORAP
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
from dataclasses import dataclass
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

USER_AGENT = (
    "claude-legal/1.0 (+https://github.com/codearranger/claude-legal) "
    "oregon-rules-puller"
)

# Direct URLs for the non-SharePoint sources.
ORCP_URL = "https://www.oregonlegislature.gov/bills_laws/SiteAssets/ORCP.html"
OEC_URL = "https://www.oregonlegislature.gov/bills_laws/ors/ors040.html"
ORPC_URL = "https://www.osbar.org/_docs/rulesregs/orpc.pdf"

# SharePoint list endpoint template. The OR Judicial Department site
# stores rule PDFs in the SharePoint asset library under
# https://www.courts.oregon.gov/rules/. Each rule set is its own list
# ('UTCR', 'ORAP', 'LCR', etc.). Items expose a File subobject with
# Name + ServerRelativeUrl.
SP_BASE = "https://www.courts.oregon.gov/rules"
SP_LIST_URL = (
    SP_BASE
    + "/_api/web/lists/getbytitle('{list_title}')/items"
    + "?$top=500&$expand=File&$orderby=Id%20desc"
    + "&$select=Id,Title,Category,File/Name,File/ServerRelativeUrl"
)


# ----------------------------------------------------------------------
# Networking.
# ----------------------------------------------------------------------

def http_get_bytes(url: str, *, headers: Optional[Dict[str, str]] = None,
                    retries: int = 4, base_sleep: float = 1.5,
                    timeout: float = 30.0) -> bytes:
    """Fetch a URL with jittered exponential-backoff retries.

    Same pattern as pull_co_statutes.py — leg/SharePoint endpoints
    occasionally return transient 5xx or connection-resets on bulk
    fetches, and we'd rather sleep and retry than abort a quarterly
    refresh."""
    req_headers = {"User-Agent": USER_AGENT}
    if headers:
        req_headers.update(headers)
    # Quote any spaces / unsafe chars in path; preserve query as-is.
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
# SharePoint REST helpers.
# ----------------------------------------------------------------------

@dataclass
class SPItem:
    item_id: int
    title: str
    category: Optional[str]
    file_name: str
    server_relative_url: str

    @property
    def absolute_url(self) -> str:
        # ServerRelativeUrl is host-relative, e.g. "/rules/UTCR/foo.pdf"
        return "https://www.courts.oregon.gov" + self.server_relative_url


def sp_list_items(list_title: str) -> List[SPItem]:
    """Fetch the items of a SharePoint list under courts.oregon.gov/rules.

    Returns a list ordered newest-first (highest Id first).
    """
    url = SP_LIST_URL.format(list_title=list_title)
    raw = http_get_bytes(url, headers={
        "Accept": "application/json;odata=nometadata",
    })
    data = json.loads(raw.decode("utf-8"))
    items: List[SPItem] = []
    for entry in data.get("value", []):
        f = entry.get("File") or {}
        name = f.get("Name") or ""
        rel = f.get("ServerRelativeUrl") or ""
        if not name or not rel:
            continue
        items.append(SPItem(
            item_id=int(entry.get("Id", 0)),
            title=entry.get("Title") or "",
            category=entry.get("Category"),
            file_name=name,
            server_relative_url=rel,
        ))
    return items


def pick_sp_item(items: List[SPItem],
                  predicate: Callable[[SPItem], bool]) -> Optional[SPItem]:
    """Return the highest-Id SPItem matching predicate, or None."""
    matches = [it for it in items if predicate(it)]
    if not matches:
        return None
    matches.sort(key=lambda it: it.item_id, reverse=True)
    return matches[0]


# ----------------------------------------------------------------------
# HTML → paragraphs (shared with pull_oregon_ors.py shape).
# ----------------------------------------------------------------------

class _ParaWalker(HTMLParser):
    """Walk a Word-exported HTML document and yield one record per <p>.

    Behaves identically to the walker in pull_oregon_ors.py but kept
    inline here to avoid coupling the two scripts."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.paragraphs: List[str] = []
        self._in_p = False
        self._chunks: List[str] = []

    def handle_starttag(self, tag, attrs):  # type: ignore[override]
        tag = tag.lower()
        if tag == "p":
            if self._in_p:
                self._flush()
            self._in_p = True
            self._chunks = []
        elif tag == "br":
            if self._in_p:
                self._chunks.append(" ")

    def handle_endtag(self, tag):  # type: ignore[override]
        if tag.lower() == "p" and self._in_p:
            self._flush()

    def handle_data(self, data):  # type: ignore[override]
        if self._in_p:
            self._chunks.append(data)

    def _flush(self) -> None:
        text = "".join(self._chunks)
        text = text.replace("\xa0", " ")
        text = re.sub(r"\s+", " ", text).strip()
        self._in_p = False
        self._chunks = []
        if text:
            self.paragraphs.append(text)


def parse_html_paragraphs(html_bytes: bytes,
                            encoding: str = "windows-1252") -> List[str]:
    text = html_bytes.decode(encoding, errors="replace")
    text = re.sub(r"<style\b[^>]*>.*?</style>", "", text,
                  flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<script\b[^>]*>.*?</script>", "", text,
                  flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    p = _ParaWalker()
    p.feed(text)
    if p._in_p:  # noqa: SLF001
        p._flush()  # noqa: SLF001
    return p.paragraphs


# ----------------------------------------------------------------------
# PDF → text.
# ----------------------------------------------------------------------

def pdf_bytes_to_layout_text(pdf_bytes: bytes) -> str:
    """Run `pdftotext -layout <stdin> -` and return the resulting text.

    `pdftotext` accepts `-` as either the input or output path for
    stdin/stdout. We write to a temp file rather than streaming because
    poppler's stdin handling is finicky with large PDFs; the temp-file
    detour costs us nothing and matches pull_co_statutes.py's pattern.
    """
    with tempfile.TemporaryDirectory(prefix="or-rules-pdf-") as td:
        td_path = Path(td)
        pdf_path = td_path / "source.pdf"
        pdf_path.write_bytes(pdf_bytes)
        proc = subprocess.run(
            ["pdftotext", "-layout", str(pdf_path), "-"],
            check=True,
            capture_output=True,
        )
        # pdftotext emits UTF-8 by default.
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
> **Format:** verbatim conversion of the official {fmt} source

---

"""


def render_md(title: str, source: str, fetched: str, fmt: str,
              body: str) -> str:
    """Wrap a body string with the canonical Markdown header block."""
    header = HEADER_BLOCK.format(
        title=title, source=source, fetched=fetched, fmt=fmt,
    )
    rendered = header + body.rstrip() + "\n"
    rendered = re.sub(r"\n{3,}", "\n\n", rendered)
    return rendered


# ----------------------------------------------------------------------
# Per-rule pullers.
# ----------------------------------------------------------------------

@dataclass
class RuleSpec:
    code: str           # output filename stem ("ORCP", "UTCR", ...)
    title: str          # Markdown H1
    fmt: str            # "HTML" or "PDF"
    fetcher: Callable[["RuleSpec"], Tuple[str, str]]
    # fetcher returns (source_url, body_text). title/format come from
    # the spec; the header block is applied centrally.


def fetch_html_paragraphs(url: str) -> str:
    """Fetch a Word-exported HTML page and return paragraphs joined by
    blank lines."""
    data = http_get_bytes(url)
    paras = parse_html_paragraphs(data)
    if not paras:
        raise RuntimeError(f"no paragraphs extracted from {url}")
    return "\n\n".join(paras)


def fetch_orcp(_spec: "RuleSpec") -> Tuple[str, str]:
    body = fetch_html_paragraphs(ORCP_URL)
    return ORCP_URL, body


def fetch_oec(_spec: "RuleSpec") -> Tuple[str, str]:
    body = fetch_html_paragraphs(OEC_URL)
    return OEC_URL, body


def fetch_orpc(_spec: "RuleSpec") -> Tuple[str, str]:
    data = http_get_bytes(ORPC_URL)
    text = strip_form_feeds(pdf_bytes_to_layout_text(data))
    return ORPC_URL, text


def _pick_or_raise(items: List[SPItem], predicate: Callable[[SPItem], bool],
                    description: str) -> SPItem:
    item = pick_sp_item(items, predicate)
    if item is None:
        raise RuntimeError(f"no SharePoint item matched: {description}")
    return item


def fetch_utcr(_spec: "RuleSpec") -> Tuple[str, str]:
    items = sp_list_items("UTCR")
    # Match the canonical monolithic publication. Recent file names
    # follow "<YEAR>_UTCR_including_amendments_effective_<DATE>.pdf".
    # We pick the highest-Id item whose Title starts with "<YEAR> UTCR"
    # and File.Name starts with "<YEAR>_UTCR_including_amendments".
    item = _pick_or_raise(
        items,
        lambda it: (
            it.file_name.lower().endswith(".pdf")
            and "including_amendments" in it.file_name.lower()
            and "_utcr_" in it.file_name.lower()
            and "_ch" not in it.file_name.lower()  # skip per-chapter PDFs
            and "_toc" not in it.file_name.lower()  # skip ToC PDFs
        ),
        "UTCR full annual-edition PDF "
        "('YYYY_UTCR_including_amendments_effective_*.pdf')",
    )
    data = http_get_bytes(item.absolute_url)
    text = strip_form_feeds(pdf_bytes_to_layout_text(data))
    return item.absolute_url, text


def fetch_orap(_spec: "RuleSpec") -> Tuple[str, str]:
    items = sp_list_items("ORAP")
    # Pick the most recent ORAP full-edition PDF. Title is "Oregon Rules
    # of Appellate Procedure"; filenames look like
    # "ORAP-2026-FullPermanentTempAmendments.pdf" or
    # "ORAP 2026 Full Permanent and Temp Amendments Eff 01-01-2026.pdf".
    item = _pick_or_raise(
        items,
        lambda it: (
            it.title.lower().startswith("oregon rules of appellate procedure")
            and it.file_name.lower().endswith(".pdf")
        ),
        "ORAP full-edition PDF",
    )
    data = http_get_bytes(item.absolute_url)
    text = strip_form_feeds(pdf_bytes_to_layout_text(data))
    return item.absolute_url, text


def _slr_picker(prefix: str, description: str
                ) -> Callable[["RuleSpec"], Tuple[str, str]]:
    """Build an SLR fetcher closure (Multnomah / Washington share shape)."""
    def fetch(_spec: "RuleSpec") -> Tuple[str, str]:
        items = sp_list_items("LCR")
        item = _pick_or_raise(
            items,
            lambda it: (
                it.file_name.lower().startswith(prefix.lower())
                and (it.category or "").upper() == "SLR"
                and it.file_name.lower().endswith(".pdf")
            ),
            description,
        )
        data = http_get_bytes(item.absolute_url)
        text = strip_form_feeds(pdf_bytes_to_layout_text(data))
        return item.absolute_url, text
    return fetch


fetch_multnomah_slr = _slr_picker(
    "Multnomah_SLR",
    "Multnomah County SLR PDF ('Multnomah_SLR_YYYY.pdf')",
)
fetch_washington_slr = _slr_picker(
    "Washington_SLR",
    "Washington County (OR) SLR PDF ('Washington_SLR_YYYY.pdf')",
)


SPECS: List[RuleSpec] = [
    RuleSpec("ORCP",           "ORCP — Oregon Rules of Civil Procedure",
             "HTML", fetch_orcp),
    RuleSpec("UTCR",           "UTCR — Uniform Trial Court Rules",
             "PDF",  fetch_utcr),
    RuleSpec("ORAP",           "ORAP — Oregon Rules of Appellate Procedure",
             "PDF",  fetch_orap),
    RuleSpec("OEC",            "OEC — Oregon Evidence Code (ORS Chapter 40)",
             "HTML", fetch_oec),
    RuleSpec("ORPC",           "ORPC — Oregon Rules of Professional Conduct",
             "PDF",  fetch_orpc),
    RuleSpec("Multnomah-SLR",
             "Multnomah-SLR — Multnomah County Supplementary Local Court Rules",
             "PDF",  fetch_multnomah_slr),
    RuleSpec("Washington-SLR",
             "Washington-SLR — Washington County (Oregon) Supplementary "
             "Local Court Rules",
             "PDF",  fetch_washington_slr),
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
    out_path = out_dir / f"{spec.code}.md"
    try:
        source_url, body = spec.fetcher(spec)
        rendered = render_md(spec.title, source_url, fetched_iso,
                              spec.fmt, body)
    except Exception as exc:  # noqa: BLE001
        # Don't clobber an existing good file with a fetch-failure stub.
        if not out_path.exists():
            stub = (
                f"# {spec.title}\n\n"
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
# Manifest update.
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
            "plugins/or-court-docs/skills/or-law-references/"
            "references/court-rules"
        ),
        help="Output directory for the corpus (default matches the "
             "canonical OR plugin location).",
    )
    ap.add_argument(
        "--only",
        nargs="*",
        help="Restrict to these rule-set codes (e.g. --only OEC ORCP).",
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
    print(f"=== pulling {len(targets)} OR rule set(s) → {out_dir}",
          flush=True)

    # Pulled sequentially (rather than in a thread pool) because:
    #   (a) only 7 items, and pdftotext invocations bind CPU per call;
    #   (b) the SharePoint REST API is rate-shy.
    results: List[RuleResult] = []
    for spec in targets:
        print(f"  -> {spec.code} ({spec.fmt}) ...", flush=True)
        r = write_rule(spec, out_dir, fetched_iso)
        results.append(r)
        tag = "OK " if r.error is None else "FAIL"
        print(f"     [{tag}] {spec.code}.md "
              f"({r.bytes_written:,} bytes)"
              + (f" — {r.error}" if r.error else ""),
              flush=True)

    ok = [r for r in results if r.error is None]
    fail = [r for r in results if r.error is not None]
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
