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


def download_pdf(title: int, dest: Path) -> Path:
    """Download one C.R.S. title PDF. Returns the local path."""
    url = PDF_URL.format(tt=title)
    out = dest / f"crs2024-title-{title:02d}.pdf"
    if out.exists() and out.stat().st_size > 0:
        return out
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()
    out.write_bytes(data)
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
    """Write one article as a Markdown file."""
    # File naming: CRS-13-80.md, CRS-13-54-5.md (decimal -> dash).
    suffix = article.replace(".", "-")
    fname = f"CRS-{title}-{suffix}.md"
    fpath = out_dir / fname

    today = date.today().isoformat()
    src_url = PDF_URL.format(tt=title)

    header = [
        f"# C.R.S. Title {title}, Article {article} — {label}",
        "",
        f"> **Source:** {src_url}",
        f"> **Fetched:** {today}",
        "> **Format:** verbatim text extracted from the official "
        "Colorado General Assembly C.R.S. PDF (2024 edition, "
        "\"Uncertified Printout\") via `pdftotext -layout`.",
        "",
        "> **NOT LEGAL ADVICE.** Statute text is reproduced verbatim "
        "as published by the Colorado Office of Legislative Legal "
        "Services. Verify against the current official text before "
        "citation.",
        "",
        "---",
        "",
        "```",
    ]
    footer = ["```", ""]

    body = "\n".join(header + lines + footer) + "\n"
    fpath.write_text(body, encoding="utf-8")
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
