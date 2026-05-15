#!/usr/bin/env python3
"""Pull selected Ohio Revised Code chapters from the
authoritative `codes.ohio.gov` HTML mirror and convert each
chapter to verbatim Markdown.

Output: plugins/oh-court-docs/skills/oh-law-references/references/oh-statutes-debt/
One MD file per chapter, named `RC-Chapter-<chapter>.md`
(e.g. `RC-Chapter-1345.md` for the Consumer Sales Practices
Act).

## Source

The Ohio Legislative Service Commission publishes the
Revised Code as HTML at `codes.ohio.gov/ohio-revised-code/`.
Chapter pages (`/chapter-<NNNN>`) include the full text of
every section inline within `<section class="laws-body">`
tags. No authentication, no API key, no Cloudflare gate.

## Target catalog

Selected to cover the full civil-practice surface — civil
procedure + evidence + limitations + exemptions +
garnishment + UCC + consumer protection + L&T + family
law + General Construction holidays.

  Chapter 1.14   General Construction Law (holidays)
  Chapter 1301-1310  Uniform Commercial Code (selected
                     subset: 1302 Sales, 1303 Negotiable
                     Instruments, 1309 Secured Transactions)
  Chapter 1345   Consumer Sales Practices Act (CSPA)
  Chapter 2305   Statutes of limitations
  Chapter 2329   Execution of judgments / exemptions
  Chapter 2333   Aid of execution; debtor's exam
  Chapter 3105   Divorce, annulment, alimony
  Chapter 3109   Children — custody / parenting / support
  Chapter 3113   Support enforcement
  Chapter 3119   Child support guidelines
  Chapter 5321   Landlord-tenant (residential)
  Chapter 1923   Forcible entry and detainer (eviction)
  Chapter 2151   Juvenile Court / abuse, neglect, dependency
  Chapter 3127   Uniform Child Custody Jurisdiction and
                 Enforcement Act (UCCJEA)
  Chapter 3115   Uniform Interstate Family Support Act
                 (UIFSA)
  Chapter 1901   Municipal Court Act
  Chapter 1907   County Court Act
  Chapter 1925   Small Claims Division
  Chapter 2305 already above. (Also 2305.06 written K;
                              2305.07 oral K)

## Usage

    python3 scripts/pull_ohio_statutes.py --workers 4

    python3 scripts/pull_ohio_statutes.py \\
        --only RC-Chapter-1345

## Dependencies

Python 3.10+ stdlib only.
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
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional, Tuple

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 "
    "Safari/537.36 claude-legal/1.0"
)

BASE_URL = "https://codes.ohio.gov/ohio-revised-code/chapter-"


# ----------------------------------------------------------------------
# Target catalog.
# ----------------------------------------------------------------------

@dataclass
class ChapterTarget:
    chapter: str             # e.g. "1345"
    label: str               # filename stem ("RC-Chapter-1345")
    topic: str               # one-line topic descriptor
    title: str               # human-readable Markdown H1


TARGETS: List[ChapterTarget] = [
    # --- Definitions (Chapter 1 — contains R.C. 1.14
    #     legal holidays + R.C. 1.45 time computation) ---
    ChapterTarget("1", "RC-Chapter-1",
                  "Definitions — Legal Holidays (R.C. 1.14) + Time Computation",
                  "Ohio Revised Code Chapter 1"),
    # --- Uniform Commercial Code (Articles 2, 3, 9) ---
    ChapterTarget("1302", "RC-Chapter-1302",
                  "Uniform Commercial Code — Sales (Article 2)",
                  "Ohio Revised Code Chapter 1302"),
    ChapterTarget("1303", "RC-Chapter-1303",
                  "Uniform Commercial Code — Negotiable Instruments (Article 3)",
                  "Ohio Revised Code Chapter 1303"),
    ChapterTarget("1309", "RC-Chapter-1309",
                  "Uniform Commercial Code — Secured Transactions (Article 9)",
                  "Ohio Revised Code Chapter 1309"),
    # --- Consumer protection ---
    ChapterTarget("1345", "RC-Chapter-1345",
                  "Consumer Sales Practices Act (CSPA)",
                  "Ohio Revised Code Chapter 1345"),
    # --- Civil procedure / limitations / enforcement ---
    ChapterTarget("2305", "RC-Chapter-2305",
                  "Statutes of Limitations + General Civil Procedure",
                  "Ohio Revised Code Chapter 2305"),
    ChapterTarget("2329", "RC-Chapter-2329",
                  "Execution of Judgments + Exemptions",
                  "Ohio Revised Code Chapter 2329"),
    ChapterTarget("2333", "RC-Chapter-2333",
                  "Aid of Execution; Debtor's Examination",
                  "Ohio Revised Code Chapter 2333"),
    # --- Landlord-tenant + Forcible Entry and Detainer ---
    ChapterTarget("5321", "RC-Chapter-5321",
                  "Residential Landlord-Tenant Act",
                  "Ohio Revised Code Chapter 5321"),
    ChapterTarget("1923", "RC-Chapter-1923",
                  "Forcible Entry and Detainer (Eviction)",
                  "Ohio Revised Code Chapter 1923"),
    # --- Family law ---
    ChapterTarget("3105", "RC-Chapter-3105",
                  "Divorce, Annulment, Legal Separation",
                  "Ohio Revised Code Chapter 3105"),
    ChapterTarget("3109", "RC-Chapter-3109",
                  "Children — Custody, Parenting, Support",
                  "Ohio Revised Code Chapter 3109"),
    ChapterTarget("3113", "RC-Chapter-3113",
                  "Failure to Provide for Family — Support Enforcement",
                  "Ohio Revised Code Chapter 3113"),
    ChapterTarget("3119", "RC-Chapter-3119",
                  "Child Support Guidelines",
                  "Ohio Revised Code Chapter 3119"),
    ChapterTarget("3127", "RC-Chapter-3127",
                  "Uniform Child Custody Jurisdiction and Enforcement Act (UCCJEA)",
                  "Ohio Revised Code Chapter 3127"),
    ChapterTarget("3115", "RC-Chapter-3115",
                  "Uniform Interstate Family Support Act (UIFSA)",
                  "Ohio Revised Code Chapter 3115"),
    # --- Juvenile Court ---
    ChapterTarget("2151", "RC-Chapter-2151",
                  "Juvenile Court — Abuse, Neglect, Dependency",
                  "Ohio Revised Code Chapter 2151"),
    # --- Court-specific procedural codes ---
    ChapterTarget("1901", "RC-Chapter-1901",
                  "Municipal Court Act",
                  "Ohio Revised Code Chapter 1901"),
    ChapterTarget("1907", "RC-Chapter-1907",
                  "County Court Act",
                  "Ohio Revised Code Chapter 1907"),
    ChapterTarget("1925", "RC-Chapter-1925",
                  "Small Claims Division of Municipal and County Courts",
                  "Ohio Revised Code Chapter 1925"),
]


# ----------------------------------------------------------------------
# HTTP.
# ----------------------------------------------------------------------

def http_get(url: str, *, retries: int = 4,
              base_sleep: float = 1.5,
              timeout: float = 60.0) -> bytes:
    """Fetch a URL with jittered exponential-backoff retries."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;"
                   "q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    parsed = urllib.parse.urlsplit(url)
    safe_path = urllib.parse.quote(parsed.path, safe="/%():'.,")
    safe_url = urllib.parse.urlunsplit(
        (parsed.scheme, parsed.netloc, safe_path,
         parsed.query, parsed.fragment)
    )
    req = urllib.request.Request(safe_url, headers=headers)
    last_exc: Optional[BaseException] = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last_exc = e
        except Exception as e:  # noqa: BLE001
            last_exc = e
        sleep_for = base_sleep * (2 ** attempt) * (0.5 + random.random())
        time.sleep(sleep_for)
    assert last_exc is not None
    raise last_exc


# ----------------------------------------------------------------------
# HTML → Markdown.
# ----------------------------------------------------------------------

# Each section on the chapter page is wrapped roughly like:
#   <a ...>{section}.{sub} | {Title}.</a>
#   <div id="content-body-N" class="content-body">
#     <div class="laws-section-info">{Effective, Latest Legislation, PDF}</div>
#     <section class="laws-body">
#       <span><p>...</p>...</span>
#     </section>
#   </div>

SECTION_HEADING_RE = re.compile(
    r"(\d{1,4}\.\d{1,3})\s*<span[^>]*>\|</span>\s*([^<]+?)\s*</a>",
    re.DOTALL,
)

# Find all `<section class="laws-body">...</section>` blocks.
LAWS_BODY_RE = re.compile(
    r'<section\s+class="laws-body"[^>]*>(.*?)</section>',
    re.DOTALL | re.IGNORECASE,
)


def _strip_tags(html_chunk: str) -> str:
    """Convert a snippet of HTML to plain Markdown paragraphs."""
    # Drop scripts/styles defensively.
    s = re.sub(r"<script\b[^>]*>.*?</script>",
               "", html_chunk, flags=re.DOTALL)
    s = re.sub(r"<style\b[^>]*>.*?</style>",
               "", s, flags=re.DOTALL)
    # Convert <p>...</p> to paragraph breaks.
    s = re.sub(r"<p\b[^>]*>", "\n\n", s, flags=re.IGNORECASE)
    s = re.sub(r"</p>", "", s, flags=re.IGNORECASE)
    # Convert <br> to newline.
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.IGNORECASE)
    # Strip remaining tags.
    s = re.sub(r"<[^>]+>", "", s)
    # Decode entities + collapse whitespace per paragraph.
    s = html.unescape(s)
    out_lines = []
    for para in re.split(r"\n\s*\n", s):
        para = re.sub(r"\s+", " ", para).strip()
        if para:
            out_lines.append(para)
    return "\n\n".join(out_lines)


def parse_chapter_html(html_text: str) -> List[Tuple[str, str, str]]:
    """Return a list of `(section_number, section_title, body_md)` tuples.

    Walks the chapter HTML by finding section headings and their
    paired `<section class="laws-body">` blocks. We rely on the
    structural pattern that each section heading is followed by
    exactly one `laws-body` block before the next section heading.
    """
    headings = list(SECTION_HEADING_RE.finditer(html_text))
    bodies = list(LAWS_BODY_RE.finditer(html_text))

    if not headings:
        return []

    out: List[Tuple[str, str, str]] = []
    for i, h in enumerate(headings):
        section_num = h.group(1).strip()
        section_title = h.group(2).strip().rstrip(".")
        # Window in which to find the body for this section.
        win_start = h.end()
        win_end = (headings[i + 1].start()
                   if i + 1 < len(headings)
                   else len(html_text))
        body_match = LAWS_BODY_RE.search(html_text, win_start, win_end)
        body_html = body_match.group(1) if body_match else ""
        body_md = _strip_tags(body_html)
        out.append((section_num, section_title, body_md))
    return out


# ----------------------------------------------------------------------
# Render.
# ----------------------------------------------------------------------

HEADER = """# {title} — {topic}

> **Source:** {source}
> **Fetched:** {fetched}
> **Format:** verbatim conversion of the Ohio LSC HTML
> publication at `codes.ohio.gov`

> **NOT LEGAL ADVICE.** Generated content is a drafting aid;
> verify against the current law before filing.

---

"""


def render_chapter_md(target: ChapterTarget, source: str,
                       fetched: str,
                       sections: List[Tuple[str, str, str]]) -> str:
    body_parts = []
    for num, title, text in sections:
        heading = f"## § {num}. {title}".strip()
        if not text:
            body_parts.append(f"{heading}\n\n_(No text returned by upstream.)_")
        else:
            body_parts.append(f"{heading}\n\n{text}")
    body = "\n\n".join(body_parts).rstrip() + "\n"
    body = re.sub(r"\n{3,}", "\n\n", body)
    return HEADER.format(
        title=target.title, topic=target.topic,
        source=source, fetched=fetched,
    ) + body


def render_stub(target: ChapterTarget, fetched: str, reason: str) -> str:
    source = f"{BASE_URL}{target.chapter}"
    return (
        f"# {target.title} — {target.topic}\n\n"
        f"> **Source:** {source}\n"
        f"> **Fetched:** {fetched}\n"
        f"> **Status:** _(stub — fetch failed)_ — {reason}\n"
        f"> **Format:** pointer stub\n\n"
        f"> **NOT LEGAL ADVICE.** This file is a pointer to "
        f"the canonical source; verify against the source "
        f"itself before filing.\n\n"
        f"---\n\n"
        f"## Scope\n\n"
        f"R.C. Chapter {target.chapter}: {target.topic}.\n\n"
        f"## How to retrieve verbatim text\n\n"
        f"Open the canonical URL above in a browser, or "
        f"re-run `scripts/pull_ohio_statutes.py --only "
        f"{target.label}` to retry. The Ohio LSC publishes "
        f"this chapter at `codes.ohio.gov`; no authentication "
        f"required.\n"
    )


# ----------------------------------------------------------------------
# Output writing.
# ----------------------------------------------------------------------

@dataclass
class WriteResult:
    label: str
    path: Path
    bytes_written: int
    sections: int
    error: Optional[str]
    stub: bool


def _file_is_stub(path: Path) -> bool:
    try:
        head = path.read_text(encoding="utf-8")[:1024]
    except Exception:  # noqa: BLE001
        return True
    return "(stub" in head or "Format:** pointer stub" in head


def write_chapter(target: ChapterTarget, out_dir: Path,
                   fetched_iso: str) -> WriteResult:
    url = f"{BASE_URL}{target.chapter}"
    out_path = out_dir / f"{target.label}.md"
    try:
        data = http_get(url)
        html_text = data.decode("utf-8", errors="replace")
        sections = parse_chapter_html(html_text)
        if not sections:
            raise RuntimeError(
                "no section headings found in chapter HTML "
                "(structure may have changed)"
            )
        rendered = render_chapter_md(target, url, fetched_iso,
                                      sections)
        section_count = len(sections)
    except Exception as exc:  # noqa: BLE001
        if out_path.exists() and not _file_is_stub(out_path):
            return WriteResult(
                target.label, out_path,
                out_path.stat().st_size, 0,
                f"fetch failed (kept existing file): {exc}",
                stub=False,
            )
        rendered = render_stub(target, fetched_iso, f"{exc}")
        tmp = out_path.with_suffix(".md.tmp")
        tmp.write_text(rendered, encoding="utf-8")
        tmp.rename(out_path)
        return WriteResult(target.label, out_path,
                           out_path.stat().st_size, 0,
                           f"{exc}", stub=True)

    tmp = out_path.with_suffix(".md.tmp")
    tmp.write_text(rendered, encoding="utf-8")
    tmp.rename(out_path)
    return WriteResult(target.label, out_path,
                       out_path.stat().st_size, section_count,
                       None, stub=False)


# ----------------------------------------------------------------------
# Manifest.
# ----------------------------------------------------------------------

def update_manifest(out_dir: Path, fetched_iso: str,
                     new_version: str = "0.1.0") -> Optional[Path]:
    manifest_path = out_dir / "_manifest.json"
    payload = {
        "version": new_version,
        "last_pulled": fetched_iso,
        "source": "https://codes.ohio.gov/ohio-revised-code/",
        "notes": (
            "Pulled by scripts/pull_ohio_statutes.py. Ohio LSC "
            "serves the Revised Code as HTML chapter pages with "
            "section bodies inline; no API key or proxy required."
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
        "--out",
        type=Path,
        default=Path(
            "plugins/oh-court-docs/skills/oh-law-references/"
            "references/oh-statutes-debt"
        ),
        help="Output directory for the corpus.",
    )
    ap.add_argument(
        "--only", nargs="*",
        help="Restrict to these chapter labels.",
    )
    ap.add_argument(
        "--workers", type=int, default=4,
        help="Concurrent fetches (default 4).",
    )
    ap.add_argument(
        "--manifest-version", default="0.1.0",
        help="Version to write into _manifest.json on success.",
    )
    args = ap.parse_args()

    out_dir: Path = args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    only = set(args.only) if args.only else None
    targets = [t for t in TARGETS if only is None or t.label in only]
    if not targets:
        print(f"!! no targets match --only {args.only!r}",
              file=sys.stderr)
        return 2

    fetched_iso = date.today().isoformat()
    print(f"=== pulling {len(targets)} OH chapter(s) → "
          f"{out_dir} (workers={args.workers})", flush=True)

    results: List[WriteResult] = []
    workers = max(1, min(args.workers, len(targets)))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(write_chapter, t, out_dir, fetched_iso): t
            for t in targets
        }
        for fut in as_completed(futures):
            t = futures[fut]
            try:
                results.append(fut.result())
            except Exception as exc:  # noqa: BLE001
                results.append(WriteResult(
                    t.label, out_dir / f"{t.label}.md",
                    0, 0, str(exc), stub=True,
                ))

    by_label = {r.label: r for r in results}
    ordered = [by_label[t.label] for t in targets if t.label in by_label]
    for t, r in zip(targets, ordered):
        tag = ("OK  " if r.error is None
               else "STUB" if r.stub else "FAIL")
        sec = f"{r.sections} sec" if r.sections else "0 sec"
        print(f"     [{tag}] {t.label}.md "
              f"({r.bytes_written:,} bytes, {sec})"
              + (f" — {r.error}" if r.error else ""),
              flush=True)

    fail = [r for r in ordered if r.error is not None
            and "kept existing file" not in (r.error or "")]
    total_bytes = sum(r.bytes_written for r in ordered)
    total_sec = sum(r.sections for r in ordered)
    print(f"\n=== wrote {len(ordered)} chapter(s), "
          f"{total_sec:,} sections, {total_bytes:,} bytes; "
          f"{len(fail)} hard-failed", flush=True)

    if only is None:
        mp = update_manifest(out_dir, fetched_iso,
                              args.manifest_version)
        if mp is not None:
            print(f"=== updated {mp}", flush=True)

    return 0 if not fail else 1


if __name__ == "__main__":
    sys.exit(main())
