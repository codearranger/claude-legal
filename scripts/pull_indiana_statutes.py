#!/usr/bin/env python3
"""Pull selected debt- and civil-practice-relevant Indiana Code articles
from the Indiana General Assembly's authoritative publication site and
convert each (title, article) pair to verbatim Markdown.

Output: plugins/in-court-docs/skills/in-law-references/references/in-statutes-debt/
One MD file per (title, article) pair, named `IC-<title>-<article>.md`
(e.g. `IC-34-11.md` for Title 34 Article 11 — Limitations).

Source URLs:
    https://iga.in.gov/laws/<year>/ic/titles/<NN>/articles/<A>
    https://iga.in.gov/laws/<year>/ic/titles/<NN>/articles/<A>/chapters/<C>
    https://iga.in.gov/laws/<year>/ic/titles/<NN>/articles/<A>/chapters/<C>/sections/<S>

As of May 2026, iga.in.gov runs as a single-page React app served via a
CloudFront distribution that returns the SPA shell (`index.html`) for
every requested path. Section text is only reachable through the
JavaScript runtime, which calls the authenticated `api.iga.in.gov`
back end. The MyIGA Hypermedia API requires a registered key (no
public anonymous endpoint).

This script is built to handle three realities:

  1. **API-key path (preferred).** If the env var `IGA_API_KEY` is
     present, the script hits the JSON API at
     `https://api.iga.in.gov/<year>/codes/ic/<title>/<article>` and
     walks chapters → sections, writing each section verbatim.

  2. **Fallback HTML scrape (when CDN serves real HTML).** Some IGA
     deployments do return server-rendered HTML for the same paths
     (the prompt's verified pattern). If `IGA_API_KEY` is unset, the
     script falls back to HTML scraping with `urllib`.

  3. **Stub path (current state, May 2026).** If neither path
     returns substantive content for an article, the script writes
     a stub MD file with a `STATUS: fetch failed — {reason}` header
     so the corpus is honest about gaps. The next quarterly run
     will replace the stub once access is restored or an
     `IGA_API_KEY` secret is wired into the workflow.

Dependencies: Python 3.10+ stdlib only. No third-party libs.

Usage:
    python3 scripts/pull_indiana_statutes.py \\
        --out plugins/in-court-docs/skills/in-law-references/references/in-statutes-debt \\
        --workers 4

    # Refresh one (title, article) pair:
    python3 scripts/pull_indiana_statutes.py --only IC-34-11

    # Override the source year (defaults to current published edition):
    python3 scripts/pull_indiana_statutes.py --year 2024
"""

from __future__ import annotations

import argparse
import json
import os
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
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Optional, Tuple

USER_AGENT = (
    "claude-legal/1.0 (+https://github.com/codearranger/claude-legal) "
    "indiana-statutes-puller"
)

# Default code year. The IGA site publishes a new "official" edition
# each year; the previous-year edition is the most-cited stable
# snapshot. Override with --year on the command line.
DEFAULT_YEAR = 2024

# Browser-style Accept header. The CloudFront in front of iga.in.gov
# performs Accept-based content negotiation — without an explicit
# Accept of `text/html`, the edge often serves the SPA shell. With
# `Accept: text/html` and a real Referer it sometimes serves the
# server-rendered code page; with `Accept: application/json` and a
# valid API key the api host serves JSON.
HTML_ACCEPT = (
    "text/html,application/xhtml+xml,application/xml;q=0.9,"
    "image/avif,image/webp,*/*;q=0.8"
)
JSON_ACCEPT = "application/json,*/*;q=0.8"

# Polite request pacing. iga.in.gov sits behind a small CloudFront
# distribution; 4 concurrent connections with a 0.4-1.0s pre-request
# sleep keeps us well under their rate limit and avoids the edge's
# "challenge" path.
DEFAULT_WORKERS = 4
PRE_REQUEST_SLEEP_MIN = 0.4
PRE_REQUEST_SLEEP_MAX = 1.0


# ----------------------------------------------------------------------
# Article target catalog.
# ----------------------------------------------------------------------

# Each entry is (title_int, article_str, topic_label). Title and
# article numbers are strings to accommodate decimal articles like
# `24-4.5` and `26-1-9.1`.
TARGETS: List[Tuple[str, str, str]] = [
    ("24", "4.5",  "Uniform Consumer Credit Code (IUCCC)"),
    ("24", "5-0.5", "Deceptive Consumer Sales Act (DCSA — Indiana UDAP analog)"),
    ("26", "1-2",   "Uniform Commercial Code — Article 2 (Sales)"),
    ("26", "1-3",   "Uniform Commercial Code — Article 3 (Negotiable Instruments)"),
    ("26", "1-9.1", "Uniform Commercial Code — Article 9 (Secured Transactions)"),
    ("31", "14",    "Family Law — Paternity (JP case-type chapter)"),
    ("31", "15",    "Dissolution of Marriage; Annulment; Legal Separation"),
    ("31", "16",    "Family Law — Support of Children and Other Dependents"),
    ("31", "17",    "Family Law — Custody and Visitation Rights"),
    ("31", "19",    "Family Law — Adoption"),
    ("31", "21",    "Uniform Child Custody Jurisdiction Act (UCCJEA)"),
    ("31", "25",    "Department of Child Services (DCS)"),
    ("31", "30",    "Juvenile Law — Juvenile Court Jurisdiction"),
    ("31", "32",    "Juvenile Law — Juvenile Court Procedure"),
    ("31", "34",    "Juvenile Law — Children in Need of Services (CHINS)"),
    ("31", "37",    "Juvenile Law — Delinquent and Status Offenders"),
    ("32", "21",    "Conveyance of Real Property"),
    ("32", "29",    "Mortgages"),
    ("32", "30",    "Real Property Liens and Foreclosure"),
    ("32", "31",    "Landlord-Tenant Relations"),
    ("33", "29",    "Indiana Superior Courts"),
    ("34", "11",    "Limitation of Actions"),
    ("34", "26",    "Special Civil Actions; Protective Orders"),
    ("34", "50",    "Indiana Mediation Act / Settlement of Disputes"),
    ("34", "55",    "Property Exempt from Execution"),
    ("34", "57",    "Garnishment Proceedings and Enforcement of Judgments"),
    ("35", "43-5",  "Forgery, Fraud, and Identity Theft"),
]


# ----------------------------------------------------------------------
# Networking.
# ----------------------------------------------------------------------

def http_get(
    url: str,
    *,
    accept: str = HTML_ACCEPT,
    auth: Optional[Tuple[str, str]] = None,
    retries: int = 4,
    base_sleep: float = 1.5,
    timeout: float = 60.0,
    polite_jitter: bool = True,
) -> Tuple[int, bytes, str]:
    """Fetch a URL with jittered exponential-backoff retries.

    Returns `(status_code, body_bytes, content_type)`. Status code is
    captured (not raised) so the caller can distinguish a 404 from a
    transient 5xx and emit a stub instead of aborting the leg.
    """
    if polite_jitter:
        time.sleep(random.uniform(PRE_REQUEST_SLEEP_MIN, PRE_REQUEST_SLEEP_MAX))
    headers: Dict[str, str] = {
        "User-Agent": USER_AGENT,
        "Accept": accept,
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://iga.in.gov/",
    }
    if auth is not None:
        key_hdr, key_val = auth
        headers[key_hdr] = key_val
    parsed = urllib.parse.urlsplit(url)
    safe_path = urllib.parse.quote(parsed.path, safe="/%():'.,")
    safe_url = urllib.parse.urlunsplit(
        (parsed.scheme, parsed.netloc, safe_path, parsed.query, parsed.fragment)
    )
    req = urllib.request.Request(safe_url, headers=headers)
    last_exc: Optional[BaseException] = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read()
                ctype = resp.headers.get("Content-Type", "")
                return resp.status, body, ctype
        except urllib.error.HTTPError as exc:
            # 4xx errors don't benefit from retry; surface them.
            if 400 <= exc.code < 500:
                return exc.code, exc.read() if exc.fp else b"", \
                    exc.headers.get("Content-Type", "") if exc.headers else ""
            last_exc = exc
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            last_exc = exc
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
        sleep_for = base_sleep * (2 ** attempt) * (0.5 + random.random())
        time.sleep(sleep_for)
    assert last_exc is not None
    raise last_exc


def get_api_auth() -> Optional[Tuple[str, str]]:
    """Return ('x-api-key', '<key>') if IGA_API_KEY env var is set,
    else None. The IGA Hypermedia API rejects all requests without a
    registered key (HTTP 403). When unset, the puller falls back to
    HTML scraping."""
    key = os.environ.get("IGA_API_KEY", "").strip()
    if not key:
        return None
    return ("x-api-key", key)


# ----------------------------------------------------------------------
# HTML scrape path (fallback when API key not available).
# ----------------------------------------------------------------------

class _SPADetector(HTMLParser):
    """Detects whether a fetched HTML page is the React SPA shell or
    a real server-rendered code page.

    The SPA shell has:
      - <title>Indiana General Assembly</title>
      - <noscript>You need to enable JavaScript to run this app.</noscript>
      - <div id="root"></div> with no other body content
    Any real page will contain `Section`, `Chapter`, or `IC ` text in
    a substantive paragraph.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.has_noscript_warning = False
        self.has_real_body_text = False
        self._capture = False
        self._buf: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        if tag in ("p", "div", "span", "section", "article"):
            self._capture = True

    def handle_endtag(self, tag: str) -> None:
        if tag in ("p", "div", "span", "section", "article"):
            self._capture = False

    def handle_data(self, data: str) -> None:
        if "enable JavaScript" in data:
            self.has_noscript_warning = True
        if self._capture:
            stripped = data.strip()
            if len(stripped) > 40:
                self._buf.append(stripped)
        # Heuristic: real code pages mention "Section" / "Chapter" /
        # the IC citation prefix in substantive paragraphs.
        if any(s in data for s in ("Sec. ", "IC ", "Chapter ", "Article ")):
            stripped = data.strip()
            if len(stripped) > 60:
                self.has_real_body_text = True

    @property
    def looks_like_spa_shell(self) -> bool:
        # SPA shell = JS warning present + no substantive paragraphs.
        return self.has_noscript_warning and not self.has_real_body_text


def is_spa_shell(html_bytes: bytes) -> bool:
    """Return True if the HTML body is the React SPA fallback shell
    rather than a real Indiana Code page. Used to decide whether to
    emit a stub or parse the content."""
    if len(html_bytes) < 2000:
        # The 691-byte shell observed in May 2026 is the canonical
        # short-circuit; anything under 2KB is suspect.
        return True
    parser = _SPADetector()
    try:
        parser.feed(html_bytes.decode("utf-8", errors="replace"))
    except Exception:
        return False
    return parser.looks_like_spa_shell


# ----------------------------------------------------------------------
# API path (when IGA_API_KEY is set).
# ----------------------------------------------------------------------

API_BASE = "https://api.iga.in.gov"


def fetch_article_via_api(
    year: int, title: str, article: str, auth: Tuple[str, str]
) -> Tuple[List[Dict[str, str]], Optional[str]]:
    """Walk title → article → chapters → sections via the MyIGA
    Hypermedia API. Returns `(sections, error)` — error is None on
    success.

    The API resource tree (per docs.api.iga.in.gov, Codes resource):

        GET /<year>/ic/titles/<title>/articles/<article>
            -> { "chapters": [ { "link": "...", "chapterId": "1" }, ... ] }
        GET <chapter.link>
            -> { "sections": [ { "link": "...", "sectionId": "1" }, ... ] }
        GET <section.link>
            -> { "sectionId": "...", "heading": "...", "citation": "...",
                 "body": "<verbatim text>" }

    The API response envelope may vary by version; this function
    tries a couple of well-known JSON shapes and falls through to
    an explanatory error string if neither matches.
    """
    article_url = (
        f"{API_BASE}/{year}/codes/ic/titles/{title}/articles/{article}"
    )
    status, body, _ctype = http_get(article_url, accept=JSON_ACCEPT, auth=auth)
    if status != 200:
        return [], f"article fetch returned HTTP {status}"
    try:
        article_doc = json.loads(body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        return [], f"article JSON parse failed: {exc}"

    chapters_field = (
        article_doc.get("chapters")
        or article_doc.get("items")
        or article_doc.get("data", {}).get("chapters")
    )
    if not chapters_field:
        return [], "article JSON had no chapters list"

    sections: List[Dict[str, str]] = []
    for chap in chapters_field:
        chap_link = chap.get("link") or chap.get("self") or chap.get("href")
        if not chap_link:
            continue
        if not chap_link.startswith("http"):
            chap_link = f"{API_BASE}{chap_link if chap_link.startswith('/') else '/' + chap_link}"
        status, body, _ = http_get(chap_link, accept=JSON_ACCEPT, auth=auth)
        if status != 200:
            continue
        try:
            chap_doc = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError:
            continue
        secs_field = (
            chap_doc.get("sections")
            or chap_doc.get("items")
            or chap_doc.get("data", {}).get("sections")
        )
        if not secs_field:
            continue
        for sec in secs_field:
            sec_link = sec.get("link") or sec.get("self") or sec.get("href")
            if not sec_link:
                continue
            if not sec_link.startswith("http"):
                sec_link = f"{API_BASE}{sec_link if sec_link.startswith('/') else '/' + sec_link}"
            status, body, _ = http_get(sec_link, accept=JSON_ACCEPT, auth=auth)
            if status != 200:
                continue
            try:
                sec_doc = json.loads(body.decode("utf-8"))
            except json.JSONDecodeError:
                continue
            sections.append({
                "citation": sec_doc.get("citation") or sec_doc.get("sectionId", ""),
                "heading":  sec_doc.get("heading") or sec_doc.get("title", ""),
                "body":     sec_doc.get("body") or sec_doc.get("text", ""),
            })
    if not sections:
        return [], "no sections returned"
    return sections, None


# ----------------------------------------------------------------------
# HTML scrape path (when API key not available).
# ----------------------------------------------------------------------

def fetch_article_via_html(
    year: int, title: str, article: str
) -> Tuple[List[Dict[str, str]], Optional[str]]:
    """Walk the article page → chapter pages → section pages on
    `iga.in.gov` and parse each section's verbatim text out of the
    server-rendered HTML.

    Returns `(sections, error)`. When the upstream returns the SPA
    shell (current behavior as of May 2026), returns
    `([], "iga.in.gov returned SPA shell — content not server-rendered")`.

    The HTML parsing logic is intentionally minimal: when iga.in.gov
    *does* server-render, each section page renders the section body
    inside a `<div class="iga-doc__body">` or `<section class="iga-section">`
    block. This function looks for that block; if it isn't present
    we treat the page as un-renderable and return empty.
    """
    article_url = (
        f"https://iga.in.gov/laws/{year}/ic/titles/{title}/articles/{article}"
    )
    status, body, _ctype = http_get(article_url)
    if status != 200:
        return [], f"article fetch returned HTTP {status}"
    if is_spa_shell(body):
        return [], (
            "iga.in.gov returned SPA shell — content not server-rendered. "
            "Set IGA_API_KEY env var (register at "
            "docs.api.iga.in.gov) for API-path fetch."
        )

    # If we get here, the upstream is serving real HTML. Extract
    # chapter links from the article page, then section links from
    # each chapter, then parse each section page.
    chap_links = _extract_links(body, kind="chapter")
    if not chap_links:
        return [], "no chapter links found on article page"

    sections: List[Dict[str, str]] = []
    for chap_path in chap_links:
        chap_url = urllib.parse.urljoin(article_url, chap_path)
        status, body, _ = http_get(chap_url)
        if status != 200 or is_spa_shell(body):
            continue
        sec_links = _extract_links(body, kind="section")
        for sec_path in sec_links:
            sec_url = urllib.parse.urljoin(chap_url, sec_path)
            status, body, _ = http_get(sec_url)
            if status != 200 or is_spa_shell(body):
                continue
            citation, heading, body_text = _parse_section_html(body)
            if body_text:
                sections.append({
                    "citation": citation,
                    "heading":  heading,
                    "body":     body_text,
                })
    if not sections:
        return [], "HTML scrape returned no sections"
    return sections, None


_LINK_RE = re.compile(
    r'href=["\']([^"\']*?/(?:chapters|sections)/[^"\']*?)["\']',
    re.IGNORECASE,
)


def _extract_links(html_bytes: bytes, *, kind: str) -> List[str]:
    """Pull `/chapters/NN` or `/sections/NN` hrefs out of an HTML
    page. `kind` is "chapter" or "section"."""
    text = html_bytes.decode("utf-8", errors="replace")
    out: List[str] = []
    seen: set = set()
    for m in _LINK_RE.finditer(text):
        href = m.group(1)
        if kind == "chapter" and "/chapters/" not in href:
            continue
        if kind == "section" and "/sections/" not in href:
            continue
        if href in seen:
            continue
        seen.add(href)
        out.append(href)
    return out


_SECTION_BODY_RE = re.compile(
    r'<(?:div|section)[^>]*class=["\'][^"\']*'
    r'(?:iga-(?:doc__body|section)|section-body|content)[^"\']*["\'][^>]*>'
    r'(.*?)</(?:div|section)>',
    re.DOTALL | re.IGNORECASE,
)
_HEADING_RE = re.compile(
    r'<h[1-3][^>]*>(.*?)</h[1-3]>',
    re.DOTALL | re.IGNORECASE,
)
_CITATION_RE = re.compile(r'IC\s+(\d+(?:[\.-]\d+){1,4})')


def _parse_section_html(html_bytes: bytes) -> Tuple[str, str, str]:
    """Best-effort extraction of (citation, heading, body) from a
    section page. When the body container can't be located, returns
    empty strings."""
    text = html_bytes.decode("utf-8", errors="replace")
    citation = ""
    heading = ""
    body_text = ""
    m = _CITATION_RE.search(text)
    if m:
        citation = m.group(1)
    m = _HEADING_RE.search(text)
    if m:
        heading = _strip_html_tags(m.group(1)).strip()
    m = _SECTION_BODY_RE.search(text)
    if m:
        body_text = _strip_html_tags(m.group(1)).strip()
    return citation, heading, body_text


_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"[ \t]+")


def _strip_html_tags(s: str) -> str:
    """Strip HTML tags and collapse whitespace within lines, while
    preserving paragraph breaks (double newline)."""
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.IGNORECASE)
    s = re.sub(r"</p>", "\n\n", s, flags=re.IGNORECASE)
    s = _TAG_RE.sub("", s)
    # Decode HTML entities.
    import html as _html_mod
    s = _html_mod.unescape(s)
    # Collapse runs of spaces / tabs, preserve newlines.
    s = "\n".join(_WS_RE.sub(" ", line).strip() for line in s.splitlines())
    # Collapse 3+ blank lines to 2.
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


# ----------------------------------------------------------------------
# Output writer.
# ----------------------------------------------------------------------

@dataclass
class ArticleResult:
    title: str
    article: str
    label: str
    sections: List[Dict[str, str]]
    error: Optional[str]

    @property
    def filename(self) -> str:
        # Article numbers like "1-9.1" become "1-9-1" in the filename
        # (mirrors the CO convention for decimal-article naming).
        article_slug = self.article.replace(".", "-")
        return f"IC-{self.title}-{article_slug}.md"


def write_article_md(out_dir: Path, year: int, result: ArticleResult) -> Path:
    fpath = out_dir / result.filename
    today = date.today().isoformat()
    article_url = (
        f"https://iga.in.gov/laws/{year}/ic/titles/{result.title}"
        f"/articles/{result.article}"
    )

    lines: List[str] = []
    lines.append(f"# Ind. Code IC {result.title}-{result.article} — {result.label}")
    lines.append("")
    lines.append(f"> **Source:** {article_url}")
    lines.append(f"> **Fetched:** {today}")
    lines.append(
        "> **Format:** verbatim conversion of the Indiana Code "
        f"{year} edition as published by the Indiana General "
        "Assembly (Office of Code Revision)."
    )
    lines.append("")
    lines.append(
        "> **NOT LEGAL ADVICE.** Statute text is reproduced verbatim "
        "as published by the Indiana General Assembly. Verify against "
        "the current official text before citation."
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    if result.error and not result.sections:
        lines.append(f"> **STATUS:** fetch failed — {result.error}")
        lines.append("")
        lines.append(
            "This file is a placeholder. The next quarterly run of "
            "`scripts/pull_indiana_statutes.py` will replace it with "
            "verbatim section text once upstream access is restored "
            "or an `IGA_API_KEY` secret is wired into the refresh "
            "workflow. See "
            "`plugins/in-court-docs/skills/in-law-references/"
            "references/in-statutes-debt/README.md` for the "
            "current corpus status."
        )
    else:
        if result.error:
            lines.append(f"> **PARTIAL:** {result.error}")
            lines.append("")
        for sec in result.sections:
            citation = sec.get("citation", "").strip()
            heading = sec.get("heading", "").strip()
            body = sec.get("body", "").strip()
            if not body:
                continue
            head = f"## IC {citation}".rstrip()
            if heading:
                head = f"{head}. {heading}"
            lines.append(head)
            lines.append("")
            lines.append(body)
            lines.append("")

    text = "\n".join(lines).rstrip() + "\n"
    tmp = fpath.with_suffix(".md.tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.rename(fpath)
    return fpath


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------

def process_one(
    year: int, title: str, article: str, label: str
) -> ArticleResult:
    auth = get_api_auth()
    if auth is not None:
        sections, err = fetch_article_via_api(year, title, article, auth)
        if sections:
            return ArticleResult(title, article, label, sections, None)
        # Fall through to HTML if API path fails (transient, schema
        # drift, etc.).
        api_err = err
    else:
        api_err = "IGA_API_KEY not set"

    sections, err = fetch_article_via_html(year, title, article)
    if sections:
        return ArticleResult(title, article, label, sections, None)

    composite = (
        f"API path: {api_err}; HTML path: {err}"
        if api_err
        else (err or "unknown")
    )
    return ArticleResult(title, article, label, [], composite)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=Path(
        "plugins/in-court-docs/skills/in-law-references/"
        "references/in-statutes-debt"
    ))
    ap.add_argument("--year", type=int, default=DEFAULT_YEAR,
                    help=f"Indiana Code edition year (default {DEFAULT_YEAR}).")
    ap.add_argument("--workers", type=int, default=DEFAULT_WORKERS,
                    help=f"Concurrent article walks (default "
                         f"{DEFAULT_WORKERS}; max 4 recommended).")
    ap.add_argument("--only", nargs="*", default=None,
                    help="Restrict to one or more IC-<T>-<A> slugs "
                         "(e.g. `--only IC-34-11 IC-24-4-5`).")
    args = ap.parse_args()

    out_dir: Path = args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    targets = TARGETS
    if args.only:
        wanted = set(args.only)
        targets = [
            (t, a, lbl) for (t, a, lbl) in TARGETS
            if f"IC-{t}-{a.replace('.', '-')}" in wanted
            or f"IC-{t}-{a}" in wanted
        ]
        if not targets:
            print(f"!! --only matched no targets in TARGETS: {sorted(wanted)}",
                  file=sys.stderr)
            return 2

    print(
        f"[in-statutes] year={args.year} workers={args.workers} "
        f"targets={len(targets)} api_key={'set' if get_api_auth() else 'unset'}",
        flush=True,
    )

    results: List[ArticleResult] = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = {
            ex.submit(process_one, args.year, t, a, lbl): (t, a)
            for (t, a, lbl) in targets
        }
        for fut in as_completed(futures):
            (t, a) = futures[fut]
            try:
                r = fut.result()
            except Exception as exc:  # noqa: BLE001
                r = ArticleResult(t, a, "", [], f"exception: {exc!r}")
            p = write_article_md(out_dir, args.year, r)
            status = "OK" if r.sections else "STUB"
            print(
                f"  [{status}] IC-{t}-{a}: {p.name} "
                f"({p.stat().st_size:,} bytes; sections={len(r.sections)}"
                f"{'; err=' + r.error if r.error else ''})",
                flush=True,
            )
            results.append(r)

    ok = sum(1 for r in results if r.sections)
    stubs = len(results) - ok
    print(
        f"\n=== wrote {len(results)} files: {ok} populated, {stubs} stubs",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
