#!/usr/bin/env python3
"""Pull selected debt- and civil-practice-relevant Colorado statutory
articles from the official C.R.S. PDFs published by the Colorado
General Assembly's Office of Legislative Legal Services and convert
them to verbatim Markdown.

Output: plugins/co-court-docs/skills/co-law-references/references/co-statutes-debt/
One MD file per (title, article) pair, each section as its own heading.

Source URL pattern (verified May 2026):
    https://content.leg.colorado.gov/sites/default/files/images/olls/crs2024-title-<NN>.pdf
where <NN> is the title number zero-padded to two digits (e.g. "04",
"13", "24").

The PDFs are the official "Uncertified Printout" of the 2024 C.R.S.
They convert cleanly with `pdftotext -layout`. The text format is:

    ARTICLE <N>
        <Article title>
    13-80-101. <Section title>. <body text>
    13-80-102. ...

This script slices each requested article out of the full-title text
and emits one Markdown file per article.

Dependencies: poppler (`brew install poppler`) for `pdftotext`.

Usage:
    python3 scripts/pull_co_statutes.py \\
        --out plugins/co-court-docs/skills/co-law-references/references/co-statutes-debt \\
        --workers 4
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import List, Optional, Tuple

USER_AGENT = (
    "claude-legal/1.0 (+https://github.com/codearranger/claude-legal) "
    "co-statutes-puller"
)
PDF_URL = (
    "https://content.leg.colorado.gov/sites/default/files/images/olls/"
    "crs2024-title-{tt:02d}.pdf"
)

# (title_int, article_str, topic_label) — article is a string because
# Colorado uses decimal article numbers (e.g. "54.5", "10.5").
TARGETS: List[Tuple[int, str, str]] = [
    (4,  "9",    "UCC Article 9 — Secured Transactions"),
    (5,  "1",    "Uniform Consumer Credit Code — General Provisions and Definitions"),
    (5,  "16",   "Colorado Fair Debt Collection Practices Act (CFDCPA)"),
    (6,  "1",    "Colorado Consumer Protection Act (CCPA)"),
    (13, "22",   "Mediation and Alternative Dispute Resolution"),
    (13, "50",   "Joint Rights and Obligations — Judgments"),
    (13, "52",   "Judgments — Enforcement"),
    (13, "54",   "Property Exempt from Execution"),
    (13, "54.5", "Garnishment"),
    (13, "80",   "Limitations — Personal Actions"),
    (13, "90",   "Witnesses"),
    (14, "10",   "Uniform Dissolution of Marriage Act (UDMA)"),
    (14, "13",   "Uniform Child-Custody Jurisdiction and Enforcement Act (UCCJEA)"),
    (24, "4",    "State Administrative Procedure Act"),
]

# Regex for the ARTICLE header line. Allows decimal article numbers.
ARTICLE_RE = re.compile(r"^\s*ARTICLE\s+(\d+(?:\.\d+)?)\s*$")

# Regex for a section start. Section numbers are like 13-80-103.5(1)(a)
# but the heading itself is always TT-AA-NNN(.N)?[a-z]?. (period title space).
# The leading whitespace is variable (typically 8 spaces from pdftotext).
SECTION_RE = re.compile(
    r"^(?P<indent>\s+)(?P<num>\d+-\d+-\d+(?:\.\d+)?[a-z]?)\.\s+(?P<rest>.*)$"
)

# Page-footer noise that pdftotext interleaves on every page break.
PAGE_FOOTER_RE = re.compile(
    r"^Colorado Revised Statutes \d{4}\s+Page \d+ of \d+\s+Uncertified Printout\s*$"
)


@dataclass
class Article:
    title: int
    number: str  # e.g. "9", "54.5"
    label: str
    lines: List[str]


def http_get_bytes(url: str, *, retries: int = 3, sleep: float = 1.5,
                   timeout: float = 120) -> bytes:
    """Fetch a URL with exponential-backoff retries. Mirrors the pattern
    used by pull_wa_rcw.py and pull_ucc.py — leg.colorado.gov can return
    transient 5xx / reset connections on large PDF downloads, and we'd
    rather sleep and retry than abort a quarterly refresh."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    last_exc: Optional[Exception] = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except Exception as exc:  # noqa: BLE001 — any urllib/socket failure should retry
            last_exc = exc
            time.sleep(sleep * (2 ** attempt))
    assert last_exc is not None
    raise last_exc


def download_pdf(title: int, dest: Path) -> Path:
    """Download one C.R.S. title PDF. Returns the local path. Writes
    atomically via a `.part` sidecar then rename, so an interrupted
    download never leaves a half-written PDF that the next run would
    skip-via-cache."""
    url = PDF_URL.format(tt=title)
    out = dest / f"crs2024-title-{title:02d}.pdf"
    if out.exists() and out.stat().st_size > 0:
        return out
    data = http_get_bytes(url)
    tmp = out.with_suffix(out.suffix + ".part")
    tmp.write_bytes(data)
    tmp.rename(out)
    return out


def pdf_to_text(pdf_path: Path) -> Path:
    """Run pdftotext -layout. Returns the resulting .txt path."""
    txt = pdf_path.with_suffix(".txt")
    if not txt.exists():
        subprocess.run(
            ["pdftotext", "-layout", str(pdf_path), str(txt)],
            check=True,
        )
    return txt


def slice_article(text_path: Path, article: str) -> Optional[List[str]]:
    """Return the raw lines of one article from a title text file, or
    None if the article isn't present. The slice spans from the
    matching `ARTICLE <N>` line up to (but not including) the next
    `ARTICLE <M>` line."""
    with text_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    # Find all article header positions.
    headers: List[Tuple[int, str]] = []
    for i, line in enumerate(lines):
        m = ARTICLE_RE.match(line)
        if m:
            headers.append((i, m.group(1)))

    start: Optional[int] = None
    end: Optional[int] = None
    for idx, (lineno, num) in enumerate(headers):
        if num == article:
            start = lineno
            if idx + 1 < len(headers):
                end = headers[idx + 1][0]
            else:
                end = len(lines)
            break
    if start is None:
        return None
    return lines[start:end]


def clean_lines(raw: List[str]) -> List[str]:
    """Drop pdftotext page-footer artifacts and trailing form-feeds.

    Preserves all substantive text and indentation. We only strip:
      - the `Colorado Revised Statutes ... Page X of Y ... Uncertified Printout` footer
      - bare form-feed characters
    """
    out = []
    for raw_line in raw:
        # pdftotext may emit form-feeds for page boundaries.
        line = raw_line.replace("\x0c", "")
        if PAGE_FOOTER_RE.match(line):
            continue
        out.append(line.rstrip("\n"))
    # Collapse runs of >2 blank lines down to 2 (preserve paragraph
    # boundaries but strip excessive page-break gaps).
    cleaned: List[str] = []
    blanks = 0
    for line in out:
        if line.strip() == "":
            blanks += 1
            if blanks <= 2:
                cleaned.append("")
        else:
            blanks = 0
            cleaned.append(line)
    # Trim leading/trailing blank lines.
    while cleaned and cleaned[0].strip() == "":
        cleaned.pop(0)
    while cleaned and cleaned[-1].strip() == "":
        cleaned.pop()
    return cleaned


def write_article(out_dir: Path, title: int, article: str, label: str,
                  lines: List[str]) -> Path:
    """Write one article as a Markdown file.

    Output convention matches the WA / OR state corpora: each statutory
    section gets a `## § NN-N-NNN. Title` heading with the body
    underneath as prose markdown (no fenced wrapping). Any prelude
    content before the first section header (editor's notes, cross-
    references, law-review citations attached to the article as a whole)
    is emitted as plain text under the file's H1.

    Indentation: the pdftotext `-layout` output uses leading whitespace
    to convey the hanging-indent structure of `(1)(a)(I)(A)` nested
    subsections. We keep that whitespace as-is inside each section body
    — markdown renderers treat lines with >=4 leading spaces as an
    indented code block, which actually preserves the visual indentation
    while still leaving the text grep-able and indexable for citation
    scanning downstream skills do."""
    # File naming: CRS-13-80.md, CRS-13-54-5.md (decimal -> dash).
    suffix = article.replace(".", "-")
    fname = f"CRS-{title}-{suffix}.md"
    fpath = out_dir / fname

    today = date.today().isoformat()
    src_url = PDF_URL.format(tt=title)

    out: List[str] = []
    out.append(f"# C.R.S. Title {title}, Article {article} — {label}")
    out.append("")
    out.append(f"> **Source:** {src_url}")
    out.append(f"> **Fetched:** {today}")
    out.append(
        "> **Format:** verbatim text extracted from the official "
        "Colorado General Assembly C.R.S. PDF (2024 edition, "
        '"Uncertified Printout") via `pdftotext -layout`.'
    )
    out.append("")
    out.append(
        "> **NOT LEGAL ADVICE.** Statute text is reproduced verbatim "
        "as published by the Colorado Office of Legislative Legal "
        "Services. Verify against the current official text before "
        "citation."
    )
    out.append("")
    out.append("---")
    out.append("")

    # Split into per-section blocks keyed by SECTION_RE. Anything before
    # the first matching section is the article prelude (editor's notes,
    # etc.) and gets emitted under a "Prelude / editor's notes" heading.
    current_num: Optional[str] = None
    current_label: Optional[str] = None
    current_body: List[str] = []
    prelude: List[str] = []
    saw_first_section = False

    def flush() -> None:
        nonlocal current_num, current_label, current_body
        if current_num is None:
            return
        out.append(f"## § {current_num}. {current_label}".rstrip())
        out.append("")
        # Strip leading/trailing blank lines from the body but keep
        # internal whitespace intact (hanging-indent structure matters).
        body = list(current_body)
        while body and body[0].strip() == "":
            body.pop(0)
        while body and body[-1].strip() == "":
            body.pop()
        out.extend(body)
        out.append("")
        current_num = None
        current_label = None
        current_body = []

    for raw in lines:
        m = SECTION_RE.match(raw)
        if m:
            if not saw_first_section and any(s.strip() for s in prelude):
                out.append("## Prelude / editor's notes")
                out.append("")
                # Trim blank lines around prelude.
                while prelude and prelude[0].strip() == "":
                    prelude.pop(0)
                while prelude and prelude[-1].strip() == "":
                    prelude.pop()
                out.extend(prelude)
                out.append("")
                prelude = []
            saw_first_section = True
            flush()
            current_num = m.group("num")
            # Take the section title as the rest-of-line after `NUM. `,
            # trimmed. If `rest` is empty (title runs onto next line),
            # leave label empty — the heading will just be `## § NUM.`.
            current_label = m.group("rest").strip()
            continue
        if not saw_first_section:
            prelude.append(raw)
        else:
            current_body.append(raw)
    flush()

    # If the article had NO section headers at all (e.g., a fully-
    # repealed stub or a one-section article), emit whatever we
    # accumulated as a single body.
    if not saw_first_section and any(s.strip() for s in prelude):
        out.extend(prelude)
        out.append("")

    body_text = "\n".join(out).rstrip() + "\n"
    # Atomic write: write to .tmp then rename so an interrupted run
    # never leaves a half-written file in the corpus.
    tmp = fpath.with_suffix(".md.tmp")
    tmp.write_text(body_text, encoding="utf-8")
    tmp.rename(fpath)
    return fpath


def process_title(title: int, articles: List[Tuple[str, str]],
                  workdir: Path, out_dir: Path) -> List[Path]:
    """Download + parse one title, write all requested articles."""
    print(f"[title-{title:02d}] downloading PDF ...", flush=True)
    pdf = download_pdf(title, workdir)
    print(f"[title-{title:02d}] converting PDF to text "
          f"({pdf.stat().st_size:,} bytes) ...", flush=True)
    txt = pdf_to_text(pdf)
    written: List[Path] = []
    for article, label in articles:
        raw = slice_article(txt, article)
        if raw is None:
            print(f"[title-{title:02d} art {article}] !! NOT FOUND in PDF",
                  flush=True)
            # Emit a stub note so the corpus is honest about gaps.
            stub_path = out_dir / f"CRS-{title}-{article.replace('.', '-')}.md"
            stub_path.write_text(
                f"# C.R.S. Title {title}, Article {article} — {label}\n\n"
                f"> **STATUS:** fetch failed — article header "
                f"`ARTICLE {article}` not found in "
                f"`crs2024-title-{title:02d}.pdf`.\n",
                encoding="utf-8",
            )
            written.append(stub_path)
            continue
        cleaned = clean_lines(raw)
        p = write_article(out_dir, title, article, label, cleaned)
        print(f"[title-{title:02d} art {article}] wrote "
              f"{p.name} ({p.stat().st_size:,} bytes)",
              flush=True)
        written.append(p)
    return written


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=Path(
        "plugins/co-court-docs/skills/co-law-references/"
        "references/co-statutes-debt"
    ))
    ap.add_argument("--workdir", type=Path, default=None,
                    help="Where to cache downloaded PDFs + text "
                         "(default: a temp dir).")
    ap.add_argument("--workers", type=int, default=4,
                    help="Concurrent title downloads (default 4). "
                         "Each title-PDF download is one network "
                         "request; six titles total.")
    args = ap.parse_args()

    out_dir: Path = args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    cleanup_workdir = False
    if args.workdir is None:
        workdir = Path(tempfile.mkdtemp(prefix="co-crs-"))
        cleanup_workdir = True
    else:
        workdir = args.workdir
        workdir.mkdir(parents=True, exist_ok=True)

    # Group articles by title so we only download + parse each title
    # PDF once.
    by_title: dict[int, List[Tuple[str, str]]] = {}
    for title, article, label in TARGETS:
        by_title.setdefault(title, []).append((article, label))

    all_written: List[Path] = []
    errors: List[str] = []
    try:
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futures = {
                ex.submit(process_title, t, arts, workdir, out_dir): t
                for t, arts in by_title.items()
            }
            for fut in as_completed(futures):
                t = futures[fut]
                try:
                    all_written.extend(fut.result())
                except Exception as exc:
                    errors.append(f"title-{t:02d}: {exc!r}")
                    print(f"[title-{t:02d}] ERROR: {exc!r}", flush=True)
    finally:
        if cleanup_workdir:
            shutil.rmtree(workdir, ignore_errors=True)

    total = sum(p.stat().st_size for p in all_written)
    print(f"\n=== wrote {len(all_written)} files, {total:,} bytes total")
    if errors:
        print("=== errors:")
        for e in errors:
            print(f"  - {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
