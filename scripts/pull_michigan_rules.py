#!/usr/bin/env python3
"""Pull the Michigan Court Rules (MCR) and Michigan Rules of Evidence
(MRE) into the mi-court-docs reference corpus.

Output: plugins/mi-court-docs/skills/mi-law-references/references/court-rules/
One MD file per target (MCR chapters 1-4 + the MRE).

## Source

The Michigan Supreme Court publishes the Michigan Court Rules and the
Michigan Rules of Evidence at `courts.michigan.gov`. The canonical "One
Court of Justice" rules library is the authoritative free source; the
community mirror at `michigancourtrules.org` is a fallback.

In practice the `courts.michigan.gov` rules assets are served from
opaque, hash-prefixed `/siteassets/...` paths discovered through the live
rules-library index (the stable deep-link paths rotate as the court
republishes the rules book), and the `michigancourtrules.org` mirror has
been observed returning HTTP 522 (origin down). When the configured
candidate URLs are unreachable, this puller writes **well-formed pointer
stubs** carrying the canonical URLs and a per-chapter scope description —
the same "publish what we can verify + honest stubs for the rest"
discipline used by `pull_co_court_rules.py` and `pull_ny_court_rules.py`.

When a candidate URL IS reachable (HTML or PDF), the puller converts it
to verbatim Markdown (PDF via `pdftotext -layout` when poppler is
installed). A `_file_is_stub` regression guard prevents a failed run from
clobbering verbatim content committed by an earlier run.

## Targets

  MCR-chapter-1-general.md            MCR ch. 1 — General Provisions
  MCR-chapter-2-civil.md              MCR ch. 2 — Civil Procedure
  MCR-chapter-3-special-proceedings.md MCR ch. 3 — Special Proceedings & Actions
  MCR-chapter-4-district-court.md     MCR ch. 4 — Special Rules: Specific Courts
  MRE-evidence.md                     Michigan Rules of Evidence

## Usage

    python3 scripts/pull_michigan_rules.py
    python3 scripts/pull_michigan_rules.py --only MRE-evidence
    python3 scripts/pull_michigan_rules.py --stubs-only

## Dependencies

Python 3.10+ stdlib. `poppler` (`brew install poppler`) only needed if a
reachable target is a PDF.
"""

from __future__ import annotations

import argparse
import html
import json
import random
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import List, Optional

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 "
    "Safari/537.36 claude-legal/1.0"
)

# Canonical human-facing entry points (used in stubs).
MCR_LIBRARY = (
    "https://www.courts.michigan.gov/administration/rules-and-instructions/"
    "court-rules-and-court-administration/"
)
MCR_MIRROR = "https://www.michigancourtrules.org/"


@dataclass
class RuleTarget:
    slug: str           # output filename stem
    title: str          # H1 / topic label
    scope: str          # one-line scope descriptor
    # Ordered list of candidate content URLs to try (HTML or PDF). The
    # first that returns substantive content wins; if all fail, a stub
    # is written. Candidate paths intentionally left empty by default
    # because the courts.michigan.gov asset paths are hash-prefixed and
    # rotate — an operator refreshing locally can populate these from
    # the live rules-library index, or the mirror can be re-probed when
    # its origin is back up.
    candidates: List[str] = field(default_factory=list)
    canonical: str = MCR_LIBRARY


TARGETS: List[RuleTarget] = [
    RuleTarget(
        "MCR-chapter-1-general",
        "Michigan Court Rules — Chapter 1: General Provisions",
        "MCR 1.101-1.110 — applicability, construction, definitions, "
        "computation and extension of time (MCR 1.108), and electronic "
        "filing provisions that govern every civil matter.",
        candidates=[],
        canonical=MCR_LIBRARY,
    ),
    RuleTarget(
        "MCR-chapter-2-civil",
        "Michigan Court Rules — Chapter 2: Civil Procedure",
        "MCR 2.000-2.640 — commencement of action, pleadings (MCR 2.111), "
        "service of process (MCR 2.105), motions (MCR 2.119), discovery "
        "(MCR 2.300 et seq.), summary disposition (MCR 2.116), default "
        "and default judgment (MCR 2.603), and judgments/orders.",
        candidates=[],
        canonical=MCR_LIBRARY,
    ),
    RuleTarget(
        "MCR-chapter-3-special-proceedings",
        "Michigan Court Rules — Chapter 3: Special Proceedings and Actions",
        "MCR 3.000-3.999 — provisional/post-judgment remedies including "
        "garnishment (MCR 3.101) and other writs, plus domestic-relations "
        "actions (MCR 3.201 et seq.) and other special civil proceedings.",
        candidates=[],
        canonical=MCR_LIBRARY,
    ),
    RuleTarget(
        "MCR-chapter-4-district-court",
        "Michigan Court Rules — Chapter 4: Special Rules for Specific Courts",
        "MCR 4.001-4.306 — rules specific to the district court, including "
        "summary proceedings to recover possession of premises "
        "(MCR 4.201, eviction), land contract / mortgage forfeiture "
        "(MCR 4.202), and the small claims division (MCR 4.301 et seq.).",
        candidates=[],
        canonical=MCR_LIBRARY,
    ),
    RuleTarget(
        "MRE-evidence",
        "Michigan Rules of Evidence (MRE)",
        "The Michigan Rules of Evidence (MRE 101-1102) — relevance, "
        "hearsay and its exceptions, authentication, the business-records "
        "exception, and judicial notice, as restyled effective Jan. 1, "
        "2024.",
        candidates=[],
        canonical=MCR_LIBRARY,
    ),
]


# ----------------------------------------------------------------------
# HTTP.
# ----------------------------------------------------------------------

def http_get(url: str, *, retries: int = 4, base_sleep: float = 1.0,
             timeout: float = 90.0) -> bytes:
    """Fetch a URL with jittered exponential-backoff retries. Terminal
    4xx (401/403/404) and the 522 origin-down status raise immediately so
    the caller falls through to the stub path without burning retries."""
    parsed = urllib.parse.urlsplit(url)
    safe_path = urllib.parse.quote(parsed.path, safe="/%():'.,")
    safe_url = urllib.parse.urlunsplit(
        (parsed.scheme, parsed.netloc, safe_path,
         parsed.query, parsed.fragment)
    )
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/pdf,"
                  "application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    req = urllib.request.Request(safe_url, headers=headers)
    last_exc: Optional[BaseException] = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            if e.code in (401, 403, 404, 410, 522):
                raise
            last_exc = e
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last_exc = e
        except Exception as e:  # noqa: BLE001
            last_exc = e
        time.sleep(base_sleep * (2 ** attempt) * (0.5 + random.random()))
    assert last_exc is not None
    raise last_exc


# ----------------------------------------------------------------------
# Content conversion.
# ----------------------------------------------------------------------

def _looks_like_pdf(data: bytes) -> bool:
    return data[:5] == b"%PDF-"


def pdf_to_markdown(data: bytes) -> str:
    """Convert PDF bytes to layout-preserving text via pdftotext."""
    with tempfile.TemporaryDirectory(prefix="mi-rules-") as td:
        pdf_path = Path(td) / "in.pdf"
        txt_path = Path(td) / "out.txt"
        pdf_path.write_bytes(data)
        subprocess.run(["pdftotext", "-layout", str(pdf_path),
                        str(txt_path)], check=True)
        text = txt_path.read_text(encoding="utf-8", errors="replace")
    text = text.replace("\x0c", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def html_to_markdown(data: bytes) -> str:
    s = data.decode("utf-8", errors="replace")
    # Try to isolate a main-content container; otherwise use the body.
    m = re.search(
        r'<(?:main|article)\b[^>]*>(.*?)</(?:main|article)>',
        s, re.DOTALL | re.IGNORECASE,
    )
    chunk = m.group(1) if m else s
    chunk = re.sub(r"<script\b[^>]*>.*?</script>", "", chunk,
                   flags=re.DOTALL | re.IGNORECASE)
    chunk = re.sub(r"<style\b[^>]*>.*?</style>", "", chunk,
                   flags=re.DOTALL | re.IGNORECASE)
    chunk = re.sub(r"<(?:nav|header|footer|aside)\b[^>]*>.*?"
                   r"</(?:nav|header|footer|aside)>", "", chunk,
                   flags=re.DOTALL | re.IGNORECASE)
    chunk = re.sub(r"<br\s*/?>", "\n", chunk, flags=re.IGNORECASE)
    chunk = re.sub(r"</(?:p|div|li|h[1-6]|tr)>", "\n\n", chunk,
                   flags=re.IGNORECASE)
    chunk = re.sub(r"<[^>]+>", "", chunk)
    chunk = html.unescape(chunk).replace("\xa0", " ")
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in chunk.splitlines()]
    out, blanks = [], 0
    for ln in lines:
        if not ln:
            blanks += 1
            if blanks <= 1:
                out.append("")
        else:
            blanks = 0
            out.append(ln)
    return "\n".join(out).strip()


# ----------------------------------------------------------------------
# Render.
# ----------------------------------------------------------------------

def render_verbatim(target: RuleTarget, fetched_iso: str,
                    source_url: str, body: str) -> str:
    return (
        f"# {target.title}\n\n"
        f"> **Scope:** {target.scope}\n"
        f"> **Source:** {source_url}\n"
        f"> **Canonical:** {target.canonical}\n"
        f"> **Fetched:** {fetched_iso}\n"
        f"> **Format:** verbatim conversion of the published Michigan "
        f"Supreme Court rules.\n\n"
        f"> **NOT LEGAL ADVICE.** Generated content is a drafting aid; "
        f"verify against the current Michigan Court Rules / Michigan Rules "
        f"of Evidence before filing.\n\n"
        f"---\n\n"
        f"{body}\n"
    )


def render_stub(target: RuleTarget, fetched_iso: str, reason: str) -> str:
    return (
        f"# {target.title}\n\n"
        f"> **Scope:** {target.scope}\n"
        f"> **Canonical (courts.michigan.gov rules library):** "
        f"{target.canonical}\n"
        f"> **Mirror (community):** {MCR_MIRROR}\n"
        f"> **Fetched:** {fetched_iso}\n"
        f"> **Status:** _(stub — verbatim text not retrieved)_ — {reason}\n"
        f"> **Format:** pointer stub\n\n"
        f"> **NOT LEGAL ADVICE.** This file is a pointer to the canonical "
        f"sources; verify against the current Michigan Court Rules / "
        f"Michigan Rules of Evidence before filing.\n\n"
        f"---\n\n"
        f"## Scope\n\n{target.scope}\n\n"
        f"## How to retrieve verbatim text\n\n"
        f"The Michigan Supreme Court publishes the Michigan Court Rules "
        f"and Michigan Rules of Evidence through the One Court of Justice "
        f"rules library. The rules assets are served from hash-prefixed "
        f"`courts.michigan.gov/siteassets/...` paths that rotate as the "
        f"rules book is republished, and the community mirror at "
        f"`michigancourtrules.org` has been observed returning HTTP 522 "
        f"(origin down). To fill in verbatim text, populate the "
        f"`candidates` URL list for `{target.slug}` in "
        f"`scripts/pull_michigan_rules.py` with the current deep-link "
        f"discovered from the rules library, then re-run "
        f"`scripts/pull_michigan_rules.py --only {target.slug}`. The "
        f"script replaces this stub on success.\n"
    )


# ----------------------------------------------------------------------
# Regression guard + writing.
# ----------------------------------------------------------------------

def _file_is_stub(path: Path) -> bool:
    try:
        head = path.read_text(encoding="utf-8")[:1024]
    except Exception:  # noqa: BLE001
        return True
    return "Format:** pointer stub" in head or "(stub" in head


@dataclass
class WriteResult:
    slug: str
    path: Path
    bytes_written: int
    source_url: Optional[str]
    error: Optional[str]
    stub: bool


def fetch_target(target: RuleTarget, out_dir: Path, fetched_iso: str,
                 stubs_only: bool = False) -> WriteResult:
    out_path = out_dir / f"{target.slug}.md"

    if not stubs_only:
        for url in target.candidates:
            try:
                data = http_get(url)
            except Exception:  # noqa: BLE001
                continue
            try:
                body = (pdf_to_markdown(data) if _looks_like_pdf(data)
                        else html_to_markdown(data))
            except Exception:  # noqa: BLE001
                continue
            if len(body.strip()) < 500:
                # Too little content to be the real rule text.
                continue
            rendered = render_verbatim(target, fetched_iso, url, body)
            tmp = out_path.with_suffix(".md.tmp")
            tmp.write_text(rendered, encoding="utf-8")
            tmp.rename(out_path)
            return WriteResult(target.slug, out_path,
                               out_path.stat().st_size, url, None,
                               stub=False)

    # Fell through (no candidate worked, no candidates configured, or
    # stubs-only). Regression guard: keep existing verbatim content.
    reason = ("--stubs-only forced" if stubs_only else
              "no reachable candidate URL (courts.michigan.gov assets "
              "hash-rotated / mirror origin down)")
    if not stubs_only and out_path.exists() and not _file_is_stub(out_path):
        return WriteResult(target.slug, out_path,
                           out_path.stat().st_size, None,
                           f"{reason} (kept existing verbatim file)",
                           stub=False)
    rendered = render_stub(target, fetched_iso, reason)
    tmp = out_path.with_suffix(".md.tmp")
    tmp.write_text(rendered, encoding="utf-8")
    tmp.rename(out_path)
    return WriteResult(target.slug, out_path, out_path.stat().st_size,
                       None, reason, stub=True)


# ----------------------------------------------------------------------
# Manifest.
# ----------------------------------------------------------------------

def update_manifest(out_dir: Path, fetched_iso: str, mode: str,
                    version: str = "0.1.0") -> Path:
    manifest_path = out_dir / "_manifest.json"
    payload = {
        "version": version,
        "last_pulled": fetched_iso,
        "mode": mode,
        "source": MCR_LIBRARY,
        "mirror": MCR_MIRROR,
        "notes": (
            "Pulled by scripts/pull_michigan_rules.py. The Michigan "
            "Supreme Court publishes the Michigan Court Rules (MCR) and "
            "Michigan Rules of Evidence (MRE) through the One Court of "
            "Justice rules library at courts.michigan.gov. The rules "
            "assets are served from hash-prefixed /siteassets/... paths "
            "that rotate as the rules book is republished, and the "
            "community mirror at michigancourtrules.org has been observed "
            "returning HTTP 522 (origin down). When no candidate URL is "
            "reachable the puller writes well-formed pointer stubs "
            "carrying the canonical URLs + a per-chapter scope "
            "description (mirroring the pull_co_court_rules.py / "
            "pull_ny_court_rules.py discipline). Populate the per-target "
            "`candidates` list with a current deep-link from the rules "
            "library and re-run with --only to fill in verbatim text; a "
            "_file_is_stub regression guard prevents clobbering committed "
            "verbatim content."
        ),
    }
    manifest_path.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    return manifest_path


# ----------------------------------------------------------------------
# CLI.
# ----------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--out", type=Path,
        default=Path(
            "plugins/mi-court-docs/skills/mi-law-references/"
            "references/court-rules"
        ),
        help="Output directory for the corpus.",
    )
    ap.add_argument("--only", nargs="*",
                    help="Restrict to these target slugs.")
    ap.add_argument("--workers", type=int, default=4,
                    help="Concurrent target fetches (default 4).")
    ap.add_argument("--stubs-only", action="store_true",
                    help="Write pointer stubs only — no network fetch.")
    ap.add_argument("--manifest-version", default="0.1.0")
    args = ap.parse_args()

    out_dir: Path = args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    only = set(args.only) if args.only else None
    targets = [t for t in TARGETS if only is None or t.slug in only]
    if not targets:
        print(f"!! no targets match --only {args.only!r}", file=sys.stderr)
        return 2

    fetched_iso = date.today().isoformat()
    print(f"=== pulling {len(targets)} MI court-rule target(s) → {out_dir} "
          f"(workers={args.workers}, stubs_only={args.stubs_only})",
          flush=True)

    results: List[WriteResult] = []
    workers = max(1, min(args.workers, len(targets)))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(fetch_target, t, out_dir, fetched_iso,
                        args.stubs_only): t
            for t in targets
        }
        for fut in as_completed(futures):
            t = futures[fut]
            try:
                results.append(fut.result())
            except Exception as exc:  # noqa: BLE001
                results.append(WriteResult(
                    t.slug, out_dir / f"{t.slug}.md", 0, None,
                    str(exc), stub=True,
                ))

    by_slug = {r.slug: r for r in results}
    ordered = [by_slug[t.slug] for t in targets if t.slug in by_slug]
    for r in ordered:
        tag = "STUB" if r.stub else "OK  "
        print(f"     [{tag}] {r.slug}.md ({r.bytes_written:,} bytes)"
              + (f" — {r.error}" if r.error else "")
              + (f" [{r.source_url}]" if r.source_url else ""),
              flush=True)

    verbatim = sum(1 for r in ordered if not r.stub)
    stubs = sum(1 for r in ordered if r.stub)
    total_bytes = sum(r.bytes_written for r in ordered)
    print(f"\n=== wrote {len(ordered)} target(s): {verbatim} verbatim, "
          f"{stubs} stub; {total_bytes:,} bytes", flush=True)

    if only is None:
        mode = "stubs" if args.stubs_only else (
            "verbatim" if stubs == 0 else
            "mixed" if verbatim else "stubs"
        )
        mp = update_manifest(out_dir, fetched_iso, mode,
                             args.manifest_version)
        print(f"=== updated {mp}", flush=True)

    # Stubbing is an expected outcome here, not a hard failure.
    return 0


if __name__ == "__main__":
    sys.exit(main())
