#!/usr/bin/env python3
"""Pull selected Oregon Revised Statutes (ORS) chapters from the
official Oregon Legislative Assembly website and convert each chapter
to verbatim Markdown.

Output: plugins/or-court-docs/skills/or-law-references/references/or-ors-debt/
One MD file per chapter (e.g. ORS-12.md, ORS-79A.md).

Source URL pattern (verified May 2026):
    https://www.oregonlegislature.gov/bills_laws/ors/ors{NNN}.html
where {NNN} is the zero-padded chapter number, optionally followed by
an alphabetic suffix (lowercase in the URL, but the upstream server
serves the same content for either case — e.g. ors079A.html and
ors079a.html resolve to the same payload).

The pages are Microsoft Word "filtered HTML" exports in windows-1252.
Each chapter page consists of a long stream of <p class=MsoNormal>
paragraphs. Two paragraph shapes matter:

  (1) Table-of-contents lines: a span containing "NN.NNN<nbsp>title".
      No surrounding <b>. These get rendered as plain text paragraphs.

  (2) Section starts: a span wrapped in <b>...</b> containing
      "NN.NNN Title." followed by an unbolded body span with the
      verbatim section text and (often) a bracketed legislative-history
      citation like "[Amended by 1979 c.284 §43]". These get rendered
      as `## NN.NNN Title. body...` headings.

All other paragraphs (chapter title block, division/series headings
like "GENERAL PROVISIONS", legislative notes, etc.) come through as
plain-text paragraphs. The conversion preserves text verbatim.

This intentionally avoids any external HTML library so the script
runs unattended in CI with only the Python stdlib.

Dependencies: Python 3.10+ stdlib only (urllib, html.parser, re, etc.).

Usage:
    python3 scripts/pull_oregon_ors.py \\
        --out plugins/or-court-docs/skills/or-law-references/references/or-ors-debt \\
        --workers 4

    # Refresh one chapter:
    python3 scripts/pull_oregon_ors.py --only 36 --out /tmp/or-test
    python3 scripts/pull_oregon_ors.py --only 79A
"""

from __future__ import annotations

import argparse
import html
import json
import random
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from typing import List, Optional, Tuple, Union

USER_AGENT = (
    "claude-legal/1.0 (+https://github.com/codearranger/claude-legal) "
    "oregon-ors-puller"
)
BASE_URL = "https://www.oregonlegislature.gov/bills_laws/ors/ors{slug}.html"

# Default chapter list mirrors the manifest. Each entry is
# (chapter_id, subject). The chapter_id is the string used in URLs
# and filenames — e.g. "12", "79A", "659A". Alphabetic suffixes are
# preserved in the canonical (uppercase) form.
DEFAULT_CHAPTERS: List[Tuple[str, str]] = [
    ("12",   "Limitations of actions"),
    ("14",   "Jurisdiction; venue"),
    ("18",   "Judgments; execution; garnishment"),
    ("19",   "Appeals"),
    ("20",   "Fees and costs"),
    ("21",   "Court fees"),
    ("32",   "Injunctions (former provisions; entirely repealed 1981)"),
    ("33",   "Contempt"),
    ("36",   "Mandatory arbitration"),
    ("40",   "Evidence Code (OEC)"),
    ("41",   "Evidence — general procedure framework"),
    ("71",   "UCC Article 1 (general)"),
    ("72",   "UCC Article 2 (sales)"),
    ("73",   "UCC Article 3 (negotiable instruments)"),
    ("79",   "UCC Article 9 (pre-2025 renumbering snapshot)"),
    ("79A",  "UCC Article 9 (renumbered from 79 in 2025; current authoritative)"),
    ("82",   "Interest; usury"),
    ("86",   "Mortgages and trust deeds"),
    ("87",   "Liens — statutory"),
    ("88",   "Foreclosure of liens"),
    ("90",   "Residential landlord and tenant"),
    ("100",  "Condominiums"),
    ("105",  "Property rights; FED"),
    ("107",  "Marital dissolution; annulment; separation; family abuse prevention"),
    ("109",  "Parent and child rights and duties"),
    ("116",  "Probate — procedure"),
    ("124",  "Abuse prevention — vulnerable persons"),
    ("165",  "Forgery, theft, fraud (civil-fraud parallels)"),
    ("174",  "Construction of statutes"),
    ("187",  "Holidays"),
    ("192",  "Public records and meetings"),
    ("646",  "Trade practices; UTPA"),
    ("657",  "Unemployment insurance"),
    ("659A", "Unlawful discrimination — employment, public accommodations, real property"),
    ("697",  "Collection agencies"),
]


# ----------------------------------------------------------------------
# Networking — jittered exponential backoff matching pull_co_statutes.py.
# ----------------------------------------------------------------------

def http_get_bytes(url: str, *, retries: int = 4, base_sleep: float = 1.5,
                    timeout: float = 30.0) -> bytes:
    """Fetch a URL with jittered exponential-backoff retries.

    Pattern mirrors pull_co_statutes.py / pull_wa_rcw.py. oregon
    legislature is a SharePoint front-end and occasionally returns
    transient 5xx / connection resets on bulk fetches; we'd rather
    sleep + retry than abort the quarterly refresh."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    last_exc: Optional[BaseException] = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            last_exc = exc
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
        # Jittered exponential backoff: base * 2^attempt +/- 50%.
        sleep_for = base_sleep * (2 ** attempt)
        sleep_for *= 0.5 + random.random()
        time.sleep(sleep_for)
    assert last_exc is not None
    raise last_exc


# ----------------------------------------------------------------------
# HTML parsing — stdlib html.parser walker.
# ----------------------------------------------------------------------

# Bold section-start pattern: matches either "NN.NNN Title..." OR
# just "NN.NNN" alone (the bare-repealed form, e.g. <b>12.030</b>
# followed by an unbolded "[Repealed by ...]" run in the same <p>).
# Leading whitespace / nbsp tolerated.
SECTION_BOLD_RE = re.compile(
    r"^\s*([0-9]+[A-Za-z]?\.[0-9]+)\b",
)

# Pattern for a paragraph that starts with an unbolded section
# reference. The TOC lines use this shape. We DON'T promote these to
# headings — they're already covered by the bold-pattern detector,
# and demoting TOC entries to plain text matches the hand-authored
# corpus shape produced in PR #6.
SECTION_PLAIN_RE = re.compile(
    r"^([0-9]+[A-Za-z]?\.[0-9]+)\s+",
)


class _ParaWalker(HTMLParser):
    """Walk a Word-exported HTML document and yield one record per <p>.

    Each record is (kind, text) where:
      - kind == "heading" — the <p> contained a <b> wrap whose visible
        text matches `NN.NNN Title.`. `text` is the full paragraph text
        with the bold portion at the front and the unbolded body
        following.
      - kind == "para" — everything else.

    The walker is intentionally tolerant of malformed HTML — Microsoft
    Word's filtered-HTML export is full of mismatched tags. It uses
    `convert_charrefs=True` so &nbsp;/&amp;/&#... are decoded
    automatically into the corresponding characters.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.records: List[Tuple[str, str]] = []
        # State while inside a <p>
        self._in_p = False
        self._p_chunks: List[str] = []
        self._bold_depth = 0
        # Track whether any text inside the <p> appeared inside a <b>.
        # We capture the bold text itself separately so we can apply
        # SECTION_BOLD_RE only to bold text (TOC entries are not bold,
        # but their plain text may coincidentally look like a section
        # reference).
        self._bold_text_chunks: List[str] = []

    # -- start tags --
    def handle_starttag(self, tag: str, attrs):  # type: ignore[override]
        tag = tag.lower()
        if tag == "p":
            # Some Word exports nest paragraphs; treat a new <p> as a
            # paragraph boundary regardless of whether the previous one
            # closed cleanly.
            if self._in_p:
                self._flush_paragraph()
            self._in_p = True
            self._p_chunks = []
            self._bold_depth = 0
            self._bold_text_chunks = []
        elif tag == "b" or tag == "strong":
            if self._in_p:
                self._bold_depth += 1
        elif tag == "br":
            if self._in_p:
                self._p_chunks.append(" ")
        # span / div / font / etc. don't carry semantic info worth tracking.

    # -- end tags --
    def handle_endtag(self, tag: str):  # type: ignore[override]
        tag = tag.lower()
        if tag == "p":
            if self._in_p:
                self._flush_paragraph()
        elif tag == "b" or tag == "strong":
            if self._in_p and self._bold_depth > 0:
                self._bold_depth -= 1

    # -- text --
    def handle_data(self, data: str):  # type: ignore[override]
        if not self._in_p:
            return
        self._p_chunks.append(data)
        if self._bold_depth > 0:
            self._bold_text_chunks.append(data)

    # -- internals --
    def _flush_paragraph(self) -> None:
        text = "".join(self._p_chunks)
        # Normalize whitespace — collapse runs of whitespace (including
        # non-breaking space) to a single ASCII space. This matches the
        # PR #6 conversion that produced ORS-12.md / ORS-32.md.
        text = text.replace("\xa0", " ")
        text = re.sub(r"\s+", " ", text).strip()
        bold_text = "".join(self._bold_text_chunks)
        bold_text = bold_text.replace("\xa0", " ")
        bold_text = re.sub(r"\s+", " ", bold_text).strip()
        # Reset state
        self._in_p = False
        self._p_chunks = []
        self._bold_depth = 0
        self._bold_text_chunks = []
        if not text:
            return
        if bold_text and SECTION_BOLD_RE.match(bold_text):
            self.records.append(("heading", text))
        else:
            self.records.append(("para", text))


def parse_chapter_html(html_bytes: bytes) -> List[Tuple[str, str]]:
    """Decode windows-1252 HTML and return a list of (kind, text) tuples."""
    text = html_bytes.decode("windows-1252", errors="replace")
    # Strip <style>, <script>, and HTML comments — they pollute the
    # paragraph text otherwise (Word emits long inline <style> blocks).
    text = re.sub(r"<style\b[^>]*>.*?</style>", "", text,
                  flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<script\b[^>]*>.*?</script>", "", text,
                  flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    parser = _ParaWalker()
    parser.feed(text)
    if parser._in_p:  # noqa: SLF001 — final flush
        parser._flush_paragraph()  # noqa: SLF001
    return parser.records


# ----------------------------------------------------------------------
# Rendering.
# ----------------------------------------------------------------------

def render_chapter(chapter: str, subject: str,
                    records: List[Tuple[str, str]],
                    fetched_iso: str, source_url: str) -> str:
    """Render parsed records as the canonical chapter Markdown."""
    out: List[str] = []
    out.append(f"# ORS Chapter {chapter} — {subject}")
    out.append("")
    out.append(f"> **Source:** {source_url}")
    out.append(f"> **Fetched:** {fetched_iso}")
    out.append("> **Format:** verbatim conversion of the official HTML source")
    out.append("")
    out.append("---")
    out.append("")
    for kind, text in records:
        if kind == "heading":
            out.append(f"## {text}")
        else:
            out.append(text)
        out.append("")
    # Collapse trailing whitespace runs.
    body = "\n".join(out).rstrip() + "\n"
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body


# ----------------------------------------------------------------------
# Per-chapter pipeline.
# ----------------------------------------------------------------------

def _padded_slug(chapter: str) -> str:
    """Return the URL slug for a chapter id.

    Numeric prefix zero-padded to 3 digits; alphabetic suffix preserved
    in the original case. The upstream server is case-insensitive about
    the suffix, but we keep the canonical-form (uppercase) suffix in
    output filenames.
    """
    m = re.match(r"^(\d+)([A-Za-z]?)$", chapter)
    if not m:
        raise ValueError(f"unrecognized chapter id: {chapter!r}")
    num = int(m.group(1))
    suffix = m.group(2)
    return f"{num:03d}{suffix}"


@dataclass
class ChapterResult:
    chapter: str
    subject: str
    path: Path
    bytes_written: int
    error: Optional[str]


def fetch_and_write_chapter(chapter: str, subject: str, out_dir: Path,
                              fetched_iso: str) -> ChapterResult:
    slug = _padded_slug(chapter)
    url = BASE_URL.format(slug=slug)
    out_path = out_dir / f"ORS-{chapter}.md"
    try:
        data = http_get_bytes(url)
        records = parse_chapter_html(data)
        if not records:
            raise RuntimeError("no paragraphs extracted")
        body = render_chapter(chapter, subject, records, fetched_iso, url)
    except Exception as exc:  # noqa: BLE001
        # Write a stub note so the corpus is honest about the gap, but
        # only if no existing file is present — we don't want a one-off
        # fetch failure to wipe a previously-good corpus entry.
        if not out_path.exists():
            stub = (
                f"# ORS Chapter {chapter} — {subject}\n\n"
                f"> **Source:** {url}\n"
                f"> **Fetched:** {fetched_iso}\n"
                f"> **Status:** _(fetch failed)_ — {type(exc).__name__}: {exc}\n"
            )
            tmp = out_path.with_suffix(".md.tmp")
            tmp.write_text(stub, encoding="utf-8")
            tmp.rename(out_path)
            return ChapterResult(chapter, subject, out_path,
                                   out_path.stat().st_size, f"{exc}")
        return ChapterResult(chapter, subject, out_path,
                              out_path.stat().st_size, f"{exc}")
    tmp = out_path.with_suffix(".md.tmp")
    tmp.write_text(body, encoding="utf-8")
    tmp.rename(out_path)
    return ChapterResult(chapter, subject, out_path,
                          out_path.stat().st_size, None)


# ----------------------------------------------------------------------
# Manifest update.
# ----------------------------------------------------------------------

def update_manifest(out_dir: Path, fetched_iso: str,
                     new_version: str = "0.3.0") -> Optional[Path]:
    """If a `_manifest.json` exists, bump its version + last_pulled.

    Updates the two scalar fields in place via regex so the existing
    formatting (custom indentation, ordering, compact per-chapter
    one-line objects, and the unicode em-dash in `_note`) is preserved.
    """
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
    # Sanity check — parses as JSON after edit.
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

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--out",
        type=Path,
        default=Path(
            "plugins/or-court-docs/skills/or-law-references/"
            "references/or-ors-debt"
        ),
        help="Output directory for the corpus (default matches the "
             "canonical OR plugin location).",
    )
    ap.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Concurrent chapter downloads (default 4). The OR site "
             "tolerates modest parallelism; we cap low to be polite.",
    )
    ap.add_argument(
        "--only",
        nargs="*",
        help="Restrict to these chapter ids (e.g. --only 36 79A). "
             "Useful for smoke-testing a single chapter.",
    )
    ap.add_argument(
        "--manifest-version",
        default="0.3.0",
        help="Version to write into _manifest.json on success "
             "(default 0.3.0).",
    )
    args = ap.parse_args()

    out_dir: Path = args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    only = set(args.only) if args.only else None
    targets = [
        (c, s) for c, s in DEFAULT_CHAPTERS if only is None or c in only
    ]
    if not targets:
        print(f"!! no chapters match --only {args.only!r}", file=sys.stderr)
        return 2

    fetched_iso = date.today().isoformat()
    print(f"=== pulling {len(targets)} ORS chapter(s) → {out_dir}",
          flush=True)

    results: List[ChapterResult] = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {
            ex.submit(fetch_and_write_chapter, c, s, out_dir, fetched_iso): c
            for c, s in targets
        }
        for fut in as_completed(futs):
            r = fut.result()
            results.append(r)
            tag = "OK " if r.error is None else "FAIL"
            print(f"  [{tag}] ORS-{r.chapter}.md "
                  f"({r.bytes_written:,} bytes)"
                  + (f" — {r.error}" if r.error else ""),
                  flush=True)

    ok = [r for r in results if r.error is None]
    fail = [r for r in results if r.error is not None]
    total_bytes = sum(r.bytes_written for r in ok)
    print(f"\n=== wrote {len(ok)} chapters, "
          f"{total_bytes:,} bytes; {len(fail)} failed", flush=True)
    if fail:
        for r in fail:
            print(f"  - ORS-{r.chapter}: {r.error}", flush=True)

    # Bump manifest only when running a full pull AND nothing failed.
    if only is None and not fail:
        mp = update_manifest(out_dir, fetched_iso, args.manifest_version)
        if mp is not None:
            print(f"=== updated {mp} → version "
                  f"{args.manifest_version}, last_pulled {fetched_iso}",
                  flush=True)

    return 0 if not fail else 1


if __name__ == "__main__":
    sys.exit(main())
