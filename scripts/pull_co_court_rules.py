#!/usr/bin/env python3
"""Pull Colorado Chief Justice Directives (CJDs) from the Colorado
Judicial Branch website and convert them to verbatim Markdown.

Output: plugins/co-court-docs/skills/co-law-references/references/court-rules/

The script walks the paginated CJD index at
`https://www.coloradojudicial.gov/supreme-court/chief-justice-directives`,
follows each PDF link, downloads the PDF, converts it with
`pdftotext -layout`, and emits one MD file per directive.

CJDs are the only Colorado statewide-rules content the Judicial Branch
publishes free of paywall / Cloudflare protection. The full text of the
**Colorado Rules of Civil Procedure (C.R.C.P.)**, **Colorado Rules of
Evidence (CRE)**, **Colorado Appellate Rules (C.A.R.)**, and the
**Colorado Rules of Professional Conduct** is published commercially by
West / LexisNexis under copyright; coloradojudicial.gov hosts only
amendment orders (`/supreme-court/adopted-proposed-rule-changes`), not
the consolidated rule text. The free-mirror alternatives — Justia,
FindLaw, Casetext — sit behind Cloudflare challenge pages that block
unattended HTTP clients. This script therefore writes **stub files**
for those four rule sets explaining the licensure gap and pointing to
the canonical commercial publisher, alongside the verbatim CJD corpus.

CJD 11-01 (Statewide Electronic Filing Standards) is the most important
deliverable from this corpus — it is the substantive Colorado format
authority cited extensively in `co-statewide-format` alongside
C.R.C.P. 10.

Mirrors the architectural choices of:
  - scripts/pull_co_statutes.py — atomic PDF downloads, pdftotext-layout
    extraction, ThreadPoolExecutor for parallelism, stub fallback when
    a target can't be sourced.
  - scripts/pull_ca_court_rules.py — index-page walk + per-rule fetch,
    one MD per rule-set.
  - scripts/pull_wa_rcw.py — http_get_bytes retry helper.

Dependencies: poppler (`brew install poppler`) for `pdftotext`.

Usage:
    python3 scripts/pull_co_court_rules.py \\
        --out plugins/co-court-docs/skills/co-law-references/references/court-rules \\
        --workers 4
"""

from __future__ import annotations

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional, Tuple

USER_AGENT = (
    "claude-legal/1.0 (+https://github.com/codearranger/claude-legal) "
    "co-court-rules-puller"
)

BASE = "https://www.coloradojudicial.gov"
CJD_INDEX_URL = BASE + "/supreme-court/chief-justice-directives"

# Filename-safe pattern for the CJD number. The Judicial Branch hosts
# files under URL paths like
#   /sites/default/files/2025-12/CJD%2011-01%20Effective%20January%201%202026%20WEB%20A11Y.pdf
# and
#   /sites/default/files/2023-08/11-03.pdf
# Both forms encode the CJD number as `NN-NN` somewhere in the filename;
# this regex tries to extract it.
CJD_NUMBER_RE = re.compile(
    r"(?:CJD[%\s_-]+)?(?P<num>\d{2}-\d{2}(?:\.\d+)?)",
    re.IGNORECASE,
)

# Hostile-character regex for tidying up CJD page-footer artifacts.
# pdftotext interleaves a repeated header on each page of these PDFs.
# We collapse them to a single occurrence at the top of the body.
PAGE_HEADER_RE = re.compile(
    r"^\s*Chief Justice Directive\s+\d{2}-\d{2}.*$",
    re.IGNORECASE,
)
PAGE_HEADER_EFFECTIVE_RE = re.compile(
    r"^\s*Amended,?\s+Effective.*$",
    re.IGNORECASE,
)
PAGE_NUMBER_RE = re.compile(r"^\s*\d+\s*$")


# ---- Rule sets that cannot be auto-sourced ----------------------------------
#
# Each entry: (output_stem, descriptive_title, citation, canonical_url, note).
# These stubs are written ONLY if the file does not already exist, so any
# subsequent hand-authoring under the same filename is preserved on
# re-runs.

STUB_RULES: List[Tuple[str, str, str, str, str]] = [
    (
        "CRCP",
        "Colorado Rules of Civil Procedure (C.R.C.P.)",
        "Colo. R. Civ. P. (citation form: `C.R.C.P. <num>`)",
        "https://www.coloradojudicial.gov/civil-rules-committee",
        "Foundational state-court civil-procedure rules. The Supreme "
        "Court of Colorado adopts and amends the C.R.C.P.; the rules "
        "themselves are published commercially by West (Colorado Court "
        "Rules) and LexisNexis under copyright. The Colorado Judicial "
        "Branch publishes only rule-change orders, not the consolidated "
        "rule text. See the Civil Rules Committee page above for the "
        "current list of pending amendments and the Adopted/Proposed "
        "Rule Changes page for the order history.",
    ),
    (
        "CRE",
        "Colorado Rules of Evidence (CRE)",
        "Colo. R. Evid. (citation form: `CRE <num>`)",
        "https://www.coloradojudicial.gov/supreme-court/adopted-proposed-rule-changes",
        "State-court evidence rules. Published commercially by West and "
        "LexisNexis under copyright; only rule-change orders are hosted "
        "on the Colorado Judicial Branch site.",
    ),
    (
        "CAR",
        "Colorado Appellate Rules (C.A.R.)",
        "Colo. App. R. (citation form: `C.A.R. <num>`)",
        "https://www.coloradojudicial.gov/court-appeals",
        "Appellate-court procedural rules. Published commercially by "
        "West and LexisNexis under copyright; only rule-change orders "
        "are hosted on the Colorado Judicial Branch site.",
    ),
    (
        "Colorado-RPC",
        "Colorado Rules of Professional Conduct",
        "Colo. RPC (citation form: `Colo. RPC <num>`)",
        "https://www.coloradojudicial.gov/rules-professional-conduct-standing-committee",
        "Lawyer-conduct rules adopted by the Supreme Court of Colorado. "
        "Published commercially by West and LexisNexis under copyright; "
        "the Standing Committee page above tracks pending amendments.",
    ),
    (
        "CRCP-Chapter-25-Small-Claims",
        "C.R.C.P. Chapter 25 — Simplified Procedure / Small Claims",
        "Colo. R. Civ. P. 501-521 (citation form: `C.R.C.P. 50X`)",
        "https://www.coloradojudicial.gov/self-help/small-claims",
        "Subset of C.R.C.P. governing small-claims practice (statewide). "
        "Same licensure gap as the full C.R.C.P.; the self-help page "
        "above publishes plain-English summaries and JDF forms.",
    ),
    (
        "CRCP-County-Court-Rules",
        "C.R.C.P. Chapter 18 — County Court Civil Procedure (Rules 301-411)",
        "Colo. R. Civ. P. 301-411 (citation form: `C.R.C.P. 3XX`)",
        "https://www.coloradojudicial.gov/county-courts",
        "Streamlined county-court (limited-jurisdiction, ≤$25k) civil-"
        "procedure rules. Same licensure gap as the full C.R.C.P.",
    ),
]


# ---- HTTP helpers ----------------------------------------------------------

def http_get_bytes(url: str, *, retries: int = 3, sleep: float = 1.5,
                   timeout: float = 120) -> bytes:
    """Fetch a URL with exponential-backoff retries. Mirrors the pattern
    used by pull_co_statutes.py / pull_wa_rcw.py — coloradojudicial.gov
    occasionally serves transient 5xx from its Pantheon/Drupal cache
    layer, and we'd rather sleep and retry than abort a quarterly
    refresh."""
    parsed = urllib.parse.urlsplit(url)
    safe_path = urllib.parse.quote(parsed.path, safe="/%")
    safe_url = urllib.parse.urlunsplit(
        (parsed.scheme, parsed.netloc, safe_path, parsed.query, parsed.fragment)
    )
    req = urllib.request.Request(safe_url, headers={"User-Agent": USER_AGENT})
    last_exc: Optional[Exception] = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except Exception as exc:  # noqa: BLE001 — retry on any urllib failure
            last_exc = exc
            time.sleep(sleep * (2 ** attempt))
    assert last_exc is not None
    raise last_exc


# ---- CJD index walker ------------------------------------------------------

@dataclass
class CJD:
    """One Chief Justice Directive PDF discovered on the index pages."""
    url: str
    filename: str          # the URL-decoded basename (e.g. "CJD 11-01 ... .pdf")
    number: str            # e.g. "11-01", "23-04"; "" if the regex misses
    listing_text: str = "" # the link's anchor text from the index page


HREF_RE = re.compile(
    r'href="(?P<url>https?://[^"]*\.pdf)"',
    re.IGNORECASE,
)
# Anchor text — best-effort. The index entries are inside long <article>
# blocks; the anchor text inside the <a href=...pdf> may be a tag or a
# short label. We use a softer regex that's tolerant of nested markup.
ANCHOR_RE = re.compile(
    r'<a\s+[^>]*href="(?P<url>https?://[^"]*\.pdf)"[^>]*>\s*(?P<text>.*?)\s*</a>',
    re.IGNORECASE | re.DOTALL,
)


def parse_index_page(html_text: str) -> List[CJD]:
    """Parse one page of the CJD index. Returns the CJDs in document
    order, deduplicated by URL."""
    seen: Dict[str, CJD] = {}
    # Pass 1: anchor-with-text — preferred so we capture the listing copy.
    for m in ANCHOR_RE.finditer(html_text):
        url = m.group("url")
        if url in seen:
            continue
        raw_text = m.group("text") or ""
        text = re.sub(r"<[^>]+>", " ", raw_text)
        text = html.unescape(text).strip()
        text = re.sub(r"\s+", " ", text)
        filename = urllib.parse.unquote(url.rsplit("/", 1)[-1])
        num_m = CJD_NUMBER_RE.search(filename)
        if not num_m:
            num_m = CJD_NUMBER_RE.search(text)
        number = num_m.group("num") if num_m else ""
        seen[url] = CJD(url=url, filename=filename, number=number, listing_text=text)
    # Pass 2: bare href in case some PDFs were nested in non-<a> markup.
    for m in HREF_RE.finditer(html_text):
        url = m.group("url")
        if url in seen:
            continue
        filename = urllib.parse.unquote(url.rsplit("/", 1)[-1])
        num_m = CJD_NUMBER_RE.search(filename)
        number = num_m.group("num") if num_m else ""
        seen[url] = CJD(url=url, filename=filename, number=number, listing_text="")
    return list(seen.values())


def discover_cjds(*, max_pages: int = 20) -> List[CJD]:
    """Walk all paginated index pages. Stops when a page yields 0 PDFs
    or HTTP fails (signal of past-the-end)."""
    out: Dict[str, CJD] = {}
    for page in range(max_pages):
        url = CJD_INDEX_URL if page == 0 else f"{CJD_INDEX_URL}?page={page}"
        try:
            body = http_get_bytes(url).decode("utf-8", errors="replace")
        except Exception as exc:
            print(f"[cjd-index page={page}] HTTP error: {exc!r}", flush=True)
            break
        page_cjds = parse_index_page(body)
        new = 0
        for c in page_cjds:
            if c.url not in out:
                out[c.url] = c
                new += 1
        print(f"[cjd-index page={page}] found {len(page_cjds)} PDFs "
              f"({new} new)", flush=True)
        if new == 0 and page > 0:
            break
    return list(out.values())


# ---- PDF download + text extraction ---------------------------------------

def download_pdf(cjd: CJD, dest: Path) -> Path:
    """Download one CJD PDF. Returns the local path. Writes atomically
    via a `.part` sidecar then rename, so an interrupted download never
    leaves a half-written PDF that the next run would skip-via-cache.
    Filename slug is the CJD number + a sanitized version of the URL
    basename, so multiple amendments of the same CJD coexist on disk
    even though the corpus only keeps the latest version (the index
    page is curated to one effective version per CJD).
    """
    # Local cache name: CJD-NN-NN.pdf if we have a number, else the
    # url-derived basename.
    if cjd.number:
        local = f"CJD-{cjd.number}.pdf"
    else:
        local = re.sub(r"[^A-Za-z0-9._-]", "_", cjd.filename)
    out = dest / local
    if out.exists() and out.stat().st_size > 0:
        return out
    data = http_get_bytes(cjd.url)
    tmp = out.with_suffix(out.suffix + ".part")
    tmp.write_bytes(data)
    tmp.rename(out)
    return out


def pdf_to_text(pdf_path: Path) -> Path:
    """Run pdftotext -layout. Returns the resulting .txt path. Cached
    against the source PDF mtime so re-runs skip the conversion."""
    txt = pdf_path.with_suffix(".txt")
    if txt.exists() and txt.stat().st_mtime >= pdf_path.stat().st_mtime:
        return txt
    subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), str(txt)],
        check=True,
    )
    return txt


def clean_cjd_text(raw: str) -> Tuple[str, str]:
    """Strip pdftotext page-header / page-number noise from a CJD text
    extraction. Returns (title, body).

    The Colorado CJD PDF layout is:
        [running page header — repeated every page]
        Chief Justice Directive NN-NN
        Amended, Effective <date>

        SUPREME COURT OF COLORADO
        OFFICE OF THE CHIEF JUSTICE

        Directive Concerning <title>
        Chief Justice Directive NN-NN
        <body…>
                                <page number>

    We dedupe the running page header, drop bare page-number lines, and
    extract the "Directive Concerning ..." line as the title.
    """
    lines = raw.replace("\x0c", "\n").splitlines()
    body_lines: List[str] = []
    title: str = ""
    seen_first_header = False

    for line in lines:
        stripped = line.rstrip()
        # Drop bare page numbers (typically right-aligned on their own line).
        if PAGE_NUMBER_RE.match(stripped):
            continue
        # Page-header lines: "Chief Justice Directive 11-01" repeating.
        # Keep the first occurrence (it's the document title) and drop
        # the rest.
        if PAGE_HEADER_RE.match(stripped) or PAGE_HEADER_EFFECTIVE_RE.match(stripped):
            if not seen_first_header:
                seen_first_header = True
                body_lines.append(stripped.strip())
                continue
            # Subsequent occurrences are page-running-headers.
            continue
        body_lines.append(stripped)

    # Title extraction: look for a "Directive Concerning ..." line in
    # the first 30 non-blank lines.
    non_blank_idx = 0
    for line in body_lines:
        if not line.strip():
            continue
        non_blank_idx += 1
        if non_blank_idx > 30:
            break
        m = re.match(r"\s*Directive Concerning\s+(?P<t>.+)$", line, re.IGNORECASE)
        if m:
            title = m.group("t").strip().rstrip(".")
            break

    # Collapse runs of >2 blank lines.
    cleaned: List[str] = []
    blanks = 0
    for line in body_lines:
        if line.strip() == "":
            blanks += 1
            if blanks <= 2:
                cleaned.append("")
        else:
            blanks = 0
            cleaned.append(line)
    while cleaned and cleaned[0].strip() == "":
        cleaned.pop(0)
    while cleaned and cleaned[-1].strip() == "":
        cleaned.pop()

    return title, "\n".join(cleaned)


# ---- Markdown rendering ----------------------------------------------------

def write_cjd_md(out_dir: Path, cjd: CJD, title: str, body: str) -> Path:
    """Write one CJD as a Markdown file."""
    today = date.today().isoformat()
    if cjd.number:
        stem = f"CJD-{cjd.number}"
        heading_lead = f"CJD {cjd.number}"
    else:
        stem = re.sub(r"\.pdf$", "", cjd.filename, flags=re.IGNORECASE)
        stem = re.sub(r"[^A-Za-z0-9._-]", "-", stem)
        heading_lead = stem
    fname = f"{stem}.md"
    fpath = out_dir / fname

    h1 = heading_lead
    if title:
        h1 = f"{heading_lead} — {title}"

    out: List[str] = []
    out.append(f"# {h1}")
    out.append("")
    out.append(f"- Citation: Colo. Chief Justice Directive {cjd.number or '(unknown)'}")
    out.append(f"- Source: {cjd.url}")
    out.append(f"- Fetched: {today}")
    out.append(
        "- Format: verbatim text extracted from the official Colorado "
        "Supreme Court Office of the Chief Justice PDF via "
        "`pdftotext -layout`."
    )
    if cjd.listing_text:
        out.append(f"- Index entry: {cjd.listing_text}")
    out.append("")
    out.append(
        "> **NOT LEGAL ADVICE.** Directive text is reproduced verbatim "
        "as published by the Colorado Supreme Court. Chief Justice "
        "Directives are administrative directives binding on Colorado "
        "courts; verify against the current effective version before "
        "citation."
    )
    out.append("")
    out.append("---")
    out.append("")
    if body:
        out.append(body)
    else:
        out.append("> _(empty extraction — re-check the source PDF.)_")
    text = "\n".join(out).rstrip() + "\n"

    tmp = fpath.with_suffix(".md.tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.rename(fpath)
    return fpath


def write_stub_rule_md(out_dir: Path, stem: str, descriptive_title: str,
                       citation: str, canonical_url: str, note: str,
                       *, overwrite: bool = False) -> Optional[Path]:
    """Write a stub MD pointer for a rule-set that cannot be auto-
    sourced (full text behind paywall / Cloudflare). Returns the path
    if a file was written, or None if an existing file was preserved.
    """
    fpath = out_dir / f"{stem}.md"
    if fpath.exists() and not overwrite:
        return None
    today = date.today().isoformat()
    out: List[str] = []
    out.append(f"# {descriptive_title}")
    out.append("")
    out.append(f"- Citation: {citation}")
    out.append(f"- Canonical Colorado source: {canonical_url}")
    out.append(f"- Stub written: {today}")
    out.append("")
    out.append(
        f"> **STATUS:** Full verbatim text of the **{descriptive_title}** "
        f"is not published on a free Colorado-government website. "
        f"The Supreme Court of Colorado adopts and amends the rule "
        f"set, but the consolidated rule text is published commercially "
        f"by West (Colorado Court Rules) and LexisNexis under "
        f"copyright. Free third-party mirrors (Justia, FindLaw, "
        f"Casetext) sit behind Cloudflare challenge pages that block "
        f"automated retrieval."
    )
    out.append("")
    out.append(f"> **Refresh fallback:** when this content needs to "
               f"be cited verbatim in a SKILL.md body or eval, copy "
               f"the rule text from the canonical source above (or "
               f"the LexisNexis/West subscription publication) and "
               f"replace this stub. The `pull_co_court_rules.py` "
               f"refresh job does not overwrite a hand-authored MD; "
               f"it only writes this stub when no file is present.")
    out.append("")
    out.append("## Why no automated pull?")
    out.append("")
    out.append(note)
    out.append("")
    out.append("## What is available automatically")
    out.append("")
    out.append(
        "Chief Justice Directives (CJDs) — including **CJD 11-01 "
        "Statewide Electronic Filing Standards** which together with "
        "C.R.C.P. 10 defines the Colorado document-format rule — "
        "**are** auto-pulled in this same corpus. See `CJD-11-01.md` "
        "and the rest of the `CJD-*.md` files in this directory for "
        "the verbatim text of every effective CJD."
    )
    out.append("")
    text = "\n".join(out).rstrip() + "\n"
    tmp = fpath.with_suffix(".md.tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.rename(fpath)
    return fpath


def write_corpus_readme(out_dir: Path, cjd_count: int, stub_count: int,
                        total_bytes: int) -> Path:
    """Refresh the corpus README with an inventory."""
    today = date.today().isoformat()
    fpath = out_dir / "README.md"
    out: List[str] = []
    out.append("# court-rules Corpus — Colorado")
    out.append("")
    out.append(f"- Last refreshed: {today}")
    out.append(f"- Chief Justice Directives (verbatim): {cjd_count}")
    out.append(f"- Rule-set stubs (full text paywalled): {stub_count}")
    out.append(f"- Total corpus size: {total_bytes:,} bytes")
    out.append("")
    out.append(
        "This corpus holds the Colorado court-rules content most "
        "relevant to civil practice. The Colorado-specific situation: "
        "**Chief Justice Directives (CJDs)** are published as free PDFs "
        "on `coloradojudicial.gov`; the rule sets themselves — "
        "**C.R.C.P., CRE, C.A.R., Colorado RPC** — are published "
        "commercially by West (Colorado Court Rules) and LexisNexis "
        "under copyright, and free-mirror alternatives (Justia, "
        "FindLaw, Casetext) sit behind Cloudflare. The `STUB-*.md` "
        "entries explain the licensure gap and point to the canonical "
        "subscription publication. Substantive citations in the "
        "Colorado plugin's SKILL.md files reference the rule numbers "
        "and verbatim short excerpts, not the full rule text."
    )
    out.append("")
    out.append("## Inventory")
    out.append("")
    out.append("### Chief Justice Directives (auto-pulled, verbatim)")
    out.append("")
    cjd_files = sorted(p for p in out_dir.glob("CJD-*.md"))
    for p in cjd_files:
        out.append(f"- `{p.name}`")
    out.append("")
    out.append("### Rule-set stubs (refresh manually from West / Lexis)")
    out.append("")
    for stem, descriptive_title, citation, *_ in STUB_RULES:
        candidate = out_dir / f"{stem}.md"
        if candidate.exists():
            out.append(f"- `{candidate.name}` — {descriptive_title} ({citation})")
    out.append("")
    out.append("## Re-pull")
    out.append("")
    out.append("```")
    out.append(
        "python3 scripts/pull_co_court_rules.py \\"
    )
    out.append(
        "  --out plugins/co-court-docs/skills/co-law-references/references/court-rules \\"
    )
    out.append("  --workers 4")
    out.append("```")
    out.append("")
    out.append(
        "Re-running is idempotent: existing CJD MD files are "
        "rewritten with fresh metadata; existing stubs (and any hand-"
        "authored MD files in this directory) are preserved untouched "
        "unless `--overwrite-stubs` is passed."
    )
    out.append("")
    text = "\n".join(out).rstrip() + "\n"
    tmp = fpath.with_suffix(".md.tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.rename(fpath)
    return fpath


# ---- Per-CJD processing ----------------------------------------------------

def process_cjd(cjd: CJD, workdir: Path, out_dir: Path) -> Tuple[Path, int]:
    """Download, convert, and write one CJD. Returns (output_md_path, bytes)."""
    pdf = download_pdf(cjd, workdir)
    txt = pdf_to_text(pdf)
    raw = txt.read_text(encoding="utf-8", errors="replace")
    title, body = clean_cjd_text(raw)
    p = write_cjd_md(out_dir, cjd, title, body)
    return p, p.stat().st_size


# ---- Main ------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--out",
        type=Path,
        default=Path(
            "plugins/co-court-docs/skills/co-law-references/"
            "references/court-rules"
        ),
        help="Output directory (default: the canonical CO court-rules corpus).",
    )
    ap.add_argument(
        "--workdir",
        type=Path,
        default=None,
        help="Where to cache downloaded PDFs + text (default: a temp dir).",
    )
    ap.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Concurrent CJD downloads (default 4). ~80 PDFs total; "
             "each is small (typically 200KB-2MB).",
    )
    ap.add_argument(
        "--only",
        nargs="*",
        help="Optional list of rule-set stem(s) to limit to (e.g. CRCP, "
             "or `CJD-11-01`). When set, the CJD index walk is skipped "
             "unless one of the requested values starts with `CJD-`.",
    )
    ap.add_argument(
        "--max-cjd-pages",
        type=int,
        default=20,
        help="Maximum index pages to walk for CJDs (default 20; the "
             "site currently has 6).",
    )
    ap.add_argument(
        "--overwrite-stubs",
        action="store_true",
        help="Rewrite stub files for paywalled rule sets even if a "
             "file already exists at the target path. Off by default "
             "so hand-authored content is preserved.",
    )
    args = ap.parse_args()

    out_dir: Path = args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    cleanup_workdir = False
    if args.workdir is None:
        workdir = Path(tempfile.mkdtemp(prefix="co-cjd-"))
        cleanup_workdir = True
    else:
        workdir = args.workdir
        workdir.mkdir(parents=True, exist_ok=True)

    only = set(args.only) if args.only else None
    want_cjds = only is None or any(s.startswith("CJD") for s in only)
    want_stubs = only is None or any(not s.startswith("CJD") for s in only)

    cjd_written: List[Path] = []
    stub_written: List[Path] = []
    errors: List[str] = []

    try:
        # ---- CJDs ----
        if want_cjds:
            print(f"=== Discovering CJDs at {CJD_INDEX_URL}", flush=True)
            cjds = discover_cjds(max_pages=args.max_cjd_pages)
            if only:
                filt = {s for s in only if s.startswith("CJD")}
                cjds = [
                    c for c in cjds
                    if (c.number and f"CJD-{c.number}" in filt) or "CJD" in filt
                ]
            print(f"=== Discovered {len(cjds)} CJDs to process", flush=True)

            with ThreadPoolExecutor(max_workers=args.workers) as ex:
                futs = {
                    ex.submit(process_cjd, c, workdir, out_dir): c
                    for c in cjds
                }
                done = 0
                for fut in as_completed(futs):
                    c = futs[fut]
                    done += 1
                    try:
                        path, size = fut.result()
                        cjd_written.append(path)
                        print(f"  [{done}/{len(cjds)}] wrote "
                              f"{path.name} ({size:,} bytes)", flush=True)
                    except Exception as exc:
                        errors.append(f"CJD {c.number or c.filename}: {exc!r}")
                        print(f"  [{done}/{len(cjds)}] ERROR for "
                              f"{c.number or c.filename}: {exc!r}",
                              flush=True)

        # ---- Stubs for paywalled rule sets ----
        if want_stubs:
            print("\n=== Writing stub pointers for paywalled rule sets",
                  flush=True)
            for stem, descriptive_title, citation, canonical_url, note in STUB_RULES:
                if only and stem not in only:
                    continue
                p = write_stub_rule_md(
                    out_dir,
                    stem,
                    descriptive_title,
                    citation,
                    canonical_url,
                    note,
                    overwrite=args.overwrite_stubs,
                )
                if p:
                    stub_written.append(p)
                    print(f"  wrote {p.name}", flush=True)
                else:
                    print(f"  skip (existing): {stem}.md", flush=True)

        # ---- README ----
        total = sum(p.stat().st_size for p in cjd_written + stub_written)
        total += sum(
            p.stat().st_size for p in out_dir.glob("*.md")
            if p not in cjd_written and p not in stub_written
            and p.name != "README.md"
        )
        write_corpus_readme(
            out_dir,
            cjd_count=len(list(out_dir.glob("CJD-*.md"))),
            stub_count=sum(
                1 for stem, *_ in STUB_RULES
                if (out_dir / f"{stem}.md").exists()
            ),
            total_bytes=total,
        )
        print(f"\n=== wrote {len(cjd_written)} CJD MDs + "
              f"{len(stub_written)} stub MDs to {out_dir}",
              flush=True)
        if errors:
            print("=== errors:")
            for e in errors:
                print(f"  - {e}")
            return 1
        return 0
    finally:
        if cleanup_workdir:
            shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
