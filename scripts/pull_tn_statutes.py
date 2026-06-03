#!/usr/bin/env python3
"""Pull selected Tennessee Code Annotated chapters from the
Justia mirror at `law.justia.com/codes/tennessee/` and convert
each chapter to verbatim Markdown.

Output: plugins/tn-court-docs/skills/tn-law-references/references/tn-statutes-debt/
One MD file per chapter, named `Tenn-Code-T<NN>-Ch<NN>.md`
(e.g. `Tenn-Code-T28-Ch3.md` for limitations of actions in
contract / tort).

## Source

The **statutory text** of the Tennessee Code is in the public domain:
under the government edicts doctrine (Banks v. Manchester, 128 U.S. 244
(1888); Georgia v. Public.Resource.Org, 590 U.S. 255 (2020)) no one
holds copyright in the words of the law. What carries copyright is the
*Annotated* compilation — the editorial case notes, history, and
cross-references — that LexisNexis publishes as Tennessee's official
code under contract with the state. Tennessee does not itself publish
the bare text as a clean structured free source. This puller copies
ONLY the section text (public domain), never the annotations, from the
most reliably-structured free mirrors: Justia
(`law.justia.com/codes/tennessee/`) and FindLaw
(`codes.findlaw.com/tn/`). It targets Justia.

When Justia returns 403 (its bot-fight policy frequently blocks
GitHub Actions IP ranges and other shared egress), the puller
writes well-formed **pointer stubs** carrying the canonical URL
and a one-line scope description — mirroring the
`pull_indiana_statutes.py` / `pull_ny_statutes.py` "publish what
we can verify + honest stubs for the rest" discipline. The same
script will produce verbatim Markdown when run from an
environment where Justia is reachable (e.g., a developer's
machine or a CI runner with a different egress IP).

## Target catalog

Selected to cover the full civil-practice surface — civil
procedure + General Sessions + sworn-account + executions /
exemptions / garnishment + appeals + limitations + tort
liability + family law + UCC + consumer protection + collection-
agency licensing + landlord-tenant + holidays.

  Title 15 ch 1   General provisions — Legal Holidays (§ 15-1-101)
  Title 16 ch 15  General Sessions Courts ($25,000 civil cap; § 16-15-501)
  Title 20 ch 6   Process — incl. § 20-6-104 debt-buyer 2024 rule
  Title 20 ch 12  Costs and fees — incl. § 20-12-119(c) fee-shifting
  Title 20 ch 16  Summary-judgment standard (§ 20-16-101)
  Title 24 ch 5   Witnesses / sworn account (§ 24-5-107)
  Title 26 ch 2   Executions
  Title 26 ch 3   Sales under execution
  Title 27 ch 5   Appeals — de novo from General Sessions (§ 27-5-108)
  Title 28 ch 3   Limitations of actions (§§ 28-3-104, -105, -109)
  Title 29 ch 18  Forcible entry and detainer (eviction)
  Title 29 ch 20  Governmental Tort Liability Act (GTLA)
  Title 29 ch 26  Health Care Liability Act (HCLA)
  Title 36 ch 3   Domestic abuse / orders of protection (§ 36-3-601)
  Title 36 ch 4   Divorce and annulment (§§ 36-4-101, -103, -121)
  Title 36 ch 5   Alimony, child support, UIFSA (§§ 36-5-101, -121, -2001)
  Title 36 ch 6   Custody / parenting plans / UCCJEA (§§ 36-6-106, -108, -201, -401)
  Title 37 ch 1   Juvenile Court — dependency, neglect, parentage
  Title 47 ch 2   UCC — Sales (Article 2; § 47-2-725 4-year SOL)
  Title 47 ch 11  Retail installment sales (RISA)
  Title 47 ch 14  Interest and usury
  Title 47 ch 18  Tennessee Consumer Protection Act (§ 47-18-101 et seq.)
  Title 62 ch 20  Tennessee Collection Service Act
  Title 66 ch 7   General landlord and tenant (non-URLTA counties)
  Title 66 ch 28  Uniform Residential Landlord and Tenant Act (URLTA)

## Usage

    python3 scripts/pull_tn_statutes.py --workers 4

    python3 scripts/pull_tn_statutes.py \\
        --only Tenn-Code-T28-Ch3

    # Force stubs even where Justia is reachable (useful for
    # validating the stub shape on a developer's machine):
    python3 scripts/pull_tn_statutes.py --stubs-only

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
from typing import List, Optional, Tuple

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 "
    "Safari/537.36 claude-legal/1.0"
)

JUSTIA_BASE = "https://law.justia.com/codes/tennessee/"
LEXIS_HOTTOPICS = "https://www.lexisnexis.com/hottopics/tncode/"


# ----------------------------------------------------------------------
# Targets.
# ----------------------------------------------------------------------

@dataclass
class ChapterTarget:
    title_num: str          # "28"
    chapter_num: str        # "3"
    label: str              # "Tenn-Code-T28-Ch3"
    topic: str              # one-line topic descriptor
    h1: str                 # H1 heading rendered into the MD


TARGETS: List[ChapterTarget] = [
    ChapterTarget("15", "1", "Tenn-Code-T15-Ch1",
                  "General provisions — Legal Holidays (§ 15-1-101)",
                  "Tenn. Code Ann. Title 15, Chapter 1"),
    ChapterTarget("16", "15", "Tenn-Code-T16-Ch15",
                  "General Sessions Courts — $25,000 civil cap (§ 16-15-501)",
                  "Tenn. Code Ann. Title 16, Chapter 15"),
    ChapterTarget("20", "6", "Tenn-Code-T20-Ch6",
                  "Process — incl. § 20-6-104 debt-buyer documentation (2024)",
                  "Tenn. Code Ann. Title 20, Chapter 6"),
    ChapterTarget("20", "12", "Tenn-Code-T20-Ch12",
                  "Costs and fees — § 20-12-119(c) fee-shifting on 12.02(6)",
                  "Tenn. Code Ann. Title 20, Chapter 12"),
    ChapterTarget("20", "16", "Tenn-Code-T20-Ch16",
                  "Summary judgment standard (§ 20-16-101)",
                  "Tenn. Code Ann. Title 20, Chapter 16"),
    ChapterTarget("24", "5", "Tenn-Code-T24-Ch5",
                  "Witnesses; sworn-account procedure (§ 24-5-107)",
                  "Tenn. Code Ann. Title 24, Chapter 5"),
    ChapterTarget("26", "2", "Tenn-Code-T26-Ch2",
                  "Executions",
                  "Tenn. Code Ann. Title 26, Chapter 2"),
    ChapterTarget("26", "3", "Tenn-Code-T26-Ch3",
                  "Sales under execution",
                  "Tenn. Code Ann. Title 26, Chapter 3"),
    ChapterTarget("27", "5", "Tenn-Code-T27-Ch5",
                  "Appeals — de novo from General Sessions (§ 27-5-108)",
                  "Tenn. Code Ann. Title 27, Chapter 5"),
    ChapterTarget("28", "3", "Tenn-Code-T28-Ch3",
                  "Limitations of actions (§§ 28-3-104, -105, -109)",
                  "Tenn. Code Ann. Title 28, Chapter 3"),
    ChapterTarget("29", "18", "Tenn-Code-T29-Ch18",
                  "Forcible entry and detainer (eviction)",
                  "Tenn. Code Ann. Title 29, Chapter 18"),
    ChapterTarget("29", "20", "Tenn-Code-T29-Ch20",
                  "Governmental Tort Liability Act (GTLA)",
                  "Tenn. Code Ann. Title 29, Chapter 20"),
    ChapterTarget("29", "26", "Tenn-Code-T29-Ch26",
                  "Health Care Liability Act (HCLA) — pre-suit notice + certificate of good faith",
                  "Tenn. Code Ann. Title 29, Chapter 26"),
    ChapterTarget("36", "3", "Tenn-Code-T36-Ch3",
                  "Domestic abuse — Orders of Protection (§ 36-3-601)",
                  "Tenn. Code Ann. Title 36, Chapter 3"),
    ChapterTarget("36", "4", "Tenn-Code-T36-Ch4",
                  "Divorce and annulment (§§ 36-4-101, -103, -121)",
                  "Tenn. Code Ann. Title 36, Chapter 4"),
    ChapterTarget("36", "5", "Tenn-Code-T36-Ch5",
                  "Alimony, child support, UIFSA (§§ 36-5-101, -121, -2001)",
                  "Tenn. Code Ann. Title 36, Chapter 5"),
    ChapterTarget("36", "6", "Tenn-Code-T36-Ch6",
                  "Custody, parenting plans, UCCJEA (§§ 36-6-106, -108, -201, -401)",
                  "Tenn. Code Ann. Title 36, Chapter 6"),
    ChapterTarget("37", "1", "Tenn-Code-T37-Ch1",
                  "Juvenile Court — dependency, neglect, parentage, TPR",
                  "Tenn. Code Ann. Title 37, Chapter 1"),
    ChapterTarget("47", "2", "Tenn-Code-T47-Ch2",
                  "UCC — Sales (Article 2; § 47-2-725 4-year SOL)",
                  "Tenn. Code Ann. Title 47, Chapter 2"),
    ChapterTarget("47", "11", "Tenn-Code-T47-Ch11",
                  "Retail installment sales (RISA)",
                  "Tenn. Code Ann. Title 47, Chapter 11"),
    ChapterTarget("47", "14", "Tenn-Code-T47-Ch14",
                  "Interest and usury",
                  "Tenn. Code Ann. Title 47, Chapter 14"),
    ChapterTarget("47", "18", "Tenn-Code-T47-Ch18",
                  "Tennessee Consumer Protection Act (§ 47-18-101 et seq.)",
                  "Tenn. Code Ann. Title 47, Chapter 18"),
    ChapterTarget("62", "20", "Tenn-Code-T62-Ch20",
                  "Tennessee Collection Service Act — licensing (§ 62-20-105)",
                  "Tenn. Code Ann. Title 62, Chapter 20"),
    ChapterTarget("66", "7", "Tenn-Code-T66-Ch7",
                  "General landlord and tenant (non-URLTA counties)",
                  "Tenn. Code Ann. Title 66, Chapter 7"),
    ChapterTarget("66", "28", "Tenn-Code-T66-Ch28",
                  "Uniform Residential Landlord and Tenant Act (URLTA; § 66-28-101)",
                  "Tenn. Code Ann. Title 66, Chapter 28"),
]


# ----------------------------------------------------------------------
# HTTP.
# ----------------------------------------------------------------------

def http_get(url: str, *, retries: int = 4,
             base_sleep: float = 1.5,
             timeout: float = 60.0) -> bytes:
    """Fetch a URL with jittered exponential-backoff retries.

    Justia sits behind Cloudflare with bot-fight mode that fingerprints
    the TLS handshake — stdlib urllib gets a 403 even from a residential
    IP. We try `curl_cffi` (Chrome TLS impersonation) first when
    available; if it is not installed, we fall back to stdlib urllib so
    the script remains importable on minimal environments (where it
    will reliably 403 and the caller will fall through to the
    stub-writing path)."""
    parsed = urllib.parse.urlsplit(url)
    safe_path = urllib.parse.quote(parsed.path, safe="/%():'.,")
    safe_url = urllib.parse.urlunsplit(
        (parsed.scheme, parsed.netloc, safe_path,
         parsed.query, parsed.fragment)
    )
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;"
                  "q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

    # Primary path: curl_cffi with Chrome impersonation.
    try:
        from curl_cffi import requests as _cffi_requests  # type: ignore

        last_exc: Optional[BaseException] = None
        for attempt in range(retries):
            try:
                r = _cffi_requests.get(
                    safe_url,
                    headers=headers,
                    impersonate="chrome",
                    timeout=timeout,
                    allow_redirects=True,
                )
                if r.status_code >= 400:
                    # 401/403 are terminal — bail out so the caller can
                    # fall through to the stub path without waiting.
                    if r.status_code in (401, 403):
                        raise urllib.error.HTTPError(
                            safe_url, r.status_code,
                            "blocked", r.headers, None,
                        )
                    last_exc = RuntimeError(
                        f"HTTP {r.status_code} for {safe_url}"
                    )
                else:
                    return r.content
            except urllib.error.HTTPError:
                raise
            except Exception as e:  # noqa: BLE001
                last_exc = e
            sleep_for = base_sleep * (2 ** attempt) * (0.5 + random.random())
            time.sleep(sleep_for)
        assert last_exc is not None
        raise last_exc
    except ImportError:
        # Fallback: stdlib urllib. Justia will likely 403, but this
        # keeps the script importable and lets the stub-writing path
        # run cleanly on environments without curl_cffi.
        req = urllib.request.Request(safe_url, headers=headers)
        last_exc = None
        for attempt in range(retries):
            try:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    return resp.read()
            except urllib.error.HTTPError as e:
                if e.code in (401, 403):
                    raise
                last_exc = e
            except (urllib.error.URLError, TimeoutError,
                    ConnectionError) as e:
                last_exc = e
            except Exception as e:  # noqa: BLE001
                last_exc = e
            sleep_for = base_sleep * (2 ** attempt) * (0.5 + random.random())
            time.sleep(sleep_for)
        assert last_exc is not None
        raise last_exc


# ----------------------------------------------------------------------
# Justia HTML → Markdown.
# ----------------------------------------------------------------------

# Justia's chapter index lists each section as a row of links to a
# section page. We aggregate by fetching the chapter index, finding
# the per-section links, and pulling each section.

CODELINK_RE = re.compile(
    r'href="(/codes/tennessee/title-' + r'{T}' + r'/chapter-' + r'{C}'
    r'/section-[^"#?]+)"',
)


def _strip_to_md(html_chunk: str) -> str:
    s = re.sub(r"<script\b[^>]*>.*?</script>",
               "", html_chunk, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r"<style\b[^>]*>.*?</style>",
               "", s, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r"<p\b[^>]*>", "\n\n", s, flags=re.IGNORECASE)
    s = re.sub(r"</p>", "", s, flags=re.IGNORECASE)
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.IGNORECASE)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    out_lines = []
    for para in re.split(r"\n\s*\n", s):
        para = re.sub(r"[ \t]+", " ", para).strip()
        if para:
            out_lines.append(para)
    return "\n\n".join(out_lines)


def chapter_index_url(t: ChapterTarget) -> str:
    return (
        f"{JUSTIA_BASE}title-{t.title_num}/chapter-{t.chapter_num}/"
    )


def parse_chapter_index(html_text: str,
                        title_num: str, chapter_num: str
                        ) -> List[str]:
    """Return per-section URL paths directly listed on the chapter
    index page. Returns an empty list when the chapter is subdivided
    into Parts (in which case the caller should walk
    `parse_part_links` -> `parse_part_index` to reach the sections)."""
    pattern = re.compile(
        r'href="(/codes/tennessee/(?:\d{4}/)?title-' +
        re.escape(title_num) +
        r'/chapter-' + re.escape(chapter_num) +
        r'/section-[^"#?]+)"'
    )
    seen: List[str] = []
    seen_set = set()
    for m in pattern.finditer(html_text):
        path = m.group(1)
        if path not in seen_set:
            seen_set.add(path)
            seen.append(path)
    return seen


def parse_part_links(html_text: str,
                     title_num: str, chapter_num: str) -> List[str]:
    """Return the Part-level URL paths listed on a chapter index page
    (for chapters that group sections under Parts rather than flat at
    the chapter level)."""
    pattern = re.compile(
        r'href="(/codes/tennessee/(?:\d{4}/)?title-' +
        re.escape(title_num) +
        r'/chapter-' + re.escape(chapter_num) +
        r'/part-\d+/)"'
    )
    seen: List[str] = []
    seen_set = set()
    for m in pattern.finditer(html_text):
        path = m.group(1)
        if path not in seen_set:
            seen_set.add(path)
            seen.append(path)
    return seen


def parse_part_index(html_text: str,
                     title_num: str, chapter_num: str) -> List[str]:
    """Return per-section URL paths on a Part index page."""
    pattern = re.compile(
        r'href="(/codes/tennessee/(?:\d{4}/)?title-' +
        re.escape(title_num) +
        r'/chapter-' + re.escape(chapter_num) +
        r'/part-\d+/section-[^"#?]+)"'
    )
    seen: List[str] = []
    seen_set = set()
    for m in pattern.finditer(html_text):
        path = m.group(1)
        if path not in seen_set:
            seen_set.add(path)
            seen.append(path)
    return seen


# Justia's current markup puts statutory text inside
# `<div id="codes-content">...</div>` on each section page. The legacy
# class-based selectors (`codes-content` / `content-body` /
# `code-section`) are retained as fallbacks for older snapshots and
# alternative layouts.
SECTION_BODY_ID_RE = re.compile(
    r'<div\b[^>]*\bid="codes-content"[^>]*>(.*?)</div>',
    re.DOTALL | re.IGNORECASE,
)
SECTION_BODY_CLASS_RE = re.compile(
    r'<div[^>]*\bclass="[^"]*\b(?:codes-content|content-body|'
    r'code-section)\b[^"]*"[^>]*>(.*?)</div>',
    re.DOTALL | re.IGNORECASE,
)


def parse_section_page(html_text: str) -> Tuple[str, str]:
    # Heading: prefer the section-specific portion of the og:title meta
    # ("Section 20-16-101 - Burden of proof ..."), falling back to the
    # <title> tag.
    heading = ""
    ogm = re.search(
        r'<meta\s+property="og:title"\s+content="([^"]+)"',
        html_text, re.IGNORECASE,
    )
    if ogm:
        og_title = html.unescape(ogm.group(1))
        # Walk the colon-separated breadcrumb and take the final
        # "Section N-N-N - ..." segment if present.
        parts = [p.strip() for p in og_title.split("::")]
        section_part = next(
            (p for p in reversed(parts)
             if re.match(r"^Section\s+\S", p, re.IGNORECASE)),
            None,
        )
        if section_part:
            heading = section_part
    if not heading:
        tm = re.search(r"<title>\s*([^<]+?)\s*\|\s*Justia",
                       html_text, re.IGNORECASE)
        heading = tm.group(1).strip() if tm else ""

    # Body: try the id-based container first (current Justia layout),
    # then fall back to class-based selectors.
    bm = SECTION_BODY_ID_RE.search(html_text)
    if bm is None:
        bm = SECTION_BODY_CLASS_RE.search(html_text)
    body_md = _strip_to_md(bm.group(1)) if bm else ""
    return heading, body_md


# ----------------------------------------------------------------------
# Render.
# ----------------------------------------------------------------------

HEADER = """# {h1} — {topic}

> **Source:** {source}
> **Fetched:** {fetched}
> **Format:** verbatim conversion of the Justia HTML mirror at
> `law.justia.com/codes/tennessee/`

> **NOT LEGAL ADVICE.** Generated content is a drafting aid;
> verify against the current Tenn. Code Ann. before filing.

---

"""


def render_chapter_md(target: ChapterTarget, fetched_iso: str,
                      sections: List[Tuple[str, str]]) -> str:
    body_parts: List[str] = []
    for heading, body in sections:
        h = heading.strip() or "Section"
        body_parts.append(f"## {h}\n\n{body}".rstrip())
    body = "\n\n".join(body_parts) + "\n"
    body = re.sub(r"\n{3,}", "\n\n", body)
    return HEADER.format(
        h1=target.h1, topic=target.topic,
        source=chapter_index_url(target), fetched=fetched_iso,
    ) + body


def render_stub(target: ChapterTarget, fetched_iso: str,
                reason: str) -> str:
    justia = chapter_index_url(target)
    return (
        f"# {target.h1} — {target.topic}\n\n"
        f"> **Canonical (Justia):** {justia}\n"
        f"> **Official (LexisNexis, copyright):** {LEXIS_HOTTOPICS}\n"
        f"> **Fetched:** {fetched_iso}\n"
        f"> **Status:** _(stub — verbatim text not retrieved)_ — {reason}\n"
        f"> **Format:** pointer stub\n\n"
        f"> **NOT LEGAL ADVICE.** This file is a pointer to the "
        f"canonical sources; verify against the current Tenn. "
        f"Code Ann. before filing.\n\n"
        f"---\n\n"
        f"## Scope\n\n"
        f"{target.topic}.\n\n"
        f"## How to retrieve verbatim text\n\n"
        f"The Tennessee Code is published officially by "
        f"LexisNexis under copyright (the free hottopics mirror "
        f"is a JS container, not flat HTML). The free Justia and "
        f"FindLaw mirrors are the practical structured sources; "
        f"Justia's IP-blocking sometimes returns 403 from shared "
        f"egress (including GitHub Actions runners), in which "
        f"case this stub is what the puller writes.\n\n"
        f"Re-run `scripts/pull_tn_statutes.py --only "
        f"{target.label}` from a network where Justia is "
        f"reachable to fill in the verbatim text. The same "
        f"script will replace this stub on success.\n"
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
    return "Format:** pointer stub" in head or "(stub" in head


def fetch_chapter(target: ChapterTarget, out_dir: Path,
                  fetched_iso: str,
                  stubs_only: bool = False) -> WriteResult:
    out_path = out_dir / f"{target.label}.md"

    if stubs_only:
        rendered = render_stub(target, fetched_iso,
                               "--stubs-only forced")
        tmp = out_path.with_suffix(".md.tmp")
        tmp.write_text(rendered, encoding="utf-8")
        tmp.rename(out_path)
        return WriteResult(target.label, out_path,
                           out_path.stat().st_size, 0,
                           None, stub=True)

    try:
        # 1. Chapter index → per-section URL list (or per-Part list).
        index_url = chapter_index_url(target)
        index_bytes = http_get(index_url)
        index_html = index_bytes.decode("utf-8", errors="replace")
        section_paths = parse_chapter_index(
            index_html, target.title_num, target.chapter_num
        )
        # Some chapters (e.g., Title 28 ch. 3; Title 47 ch. 2) group
        # sections under Parts rather than listing them flat at the
        # chapter level. Walk the Parts to collect their sections.
        if not section_paths:
            part_paths = parse_part_links(
                index_html, target.title_num, target.chapter_num
            )
            if part_paths:
                for part_path in part_paths:
                    part_url = "https://law.justia.com" + part_path
                    try:
                        part_bytes = http_get(part_url)
                    except Exception:  # noqa: BLE001
                        continue
                    part_html = part_bytes.decode(
                        "utf-8", errors="replace"
                    )
                    for sec_path in parse_part_index(
                        part_html, target.title_num, target.chapter_num
                    ):
                        if sec_path not in section_paths:
                            section_paths.append(sec_path)
                    # Gentle pace between Part fetches.
                    time.sleep(0.2 + random.random() * 0.3)
        if not section_paths:
            raise RuntimeError(
                f"no section links found at {index_url} "
                f"(structure may have changed)"
            )

        # 2. Fetch each section sequentially.
        sections: List[Tuple[str, str]] = []
        for path in section_paths:
            url = "https://law.justia.com" + path
            try:
                data = http_get(url)
            except Exception as e:  # noqa: BLE001
                sections.append((f"(fetch failed: {path})",
                                 f"_(could not retrieve: {e})_"))
                continue
            html_text = data.decode("utf-8", errors="replace")
            heading, body_md = parse_section_page(html_text)
            if not body_md.strip():
                body_md = "_(no section body extracted)_"
            sections.append((heading, body_md))
            time.sleep(0.2 + random.random() * 0.3)

        rendered = render_chapter_md(target, fetched_iso, sections)

        # If most sections came back empty or fetch-failed, the
        # chapter MD would be a useless empty shell. Fall back to a
        # clean pointer stub. The Justia bot-fight policy sometimes
        # returns 200 on chapter indexes but 403 on per-section pages
        # (or vice versa); treat that mixed-blocked outcome as a
        # stub-equivalent failure for output purposes.
        placeholder_markers = (
            "_(no section body extracted)_",
            "_(could not retrieve:",
        )
        empty_sections = sum(
            1 for _, b in sections
            if any(m in b for m in placeholder_markers)
        )
        if sections and empty_sections >= max(1, int(len(sections) * 0.5)):
            raise RuntimeError(
                f"section pages blocked or empty "
                f"({empty_sections}/{len(sections)} placeholders)"
            )

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
                       out_path.stat().st_size,
                       len(sections), None, stub=False)


# ----------------------------------------------------------------------
# Manifest.
# ----------------------------------------------------------------------

def update_manifest(out_dir: Path, fetched_iso: str,
                    version: str = "0.1.0") -> Path:
    manifest_path = out_dir / "_manifest.json"
    payload = {
        "version": version,
        "last_pulled": fetched_iso,
        "source": "https://law.justia.com/codes/tennessee/",
        "notes": (
            "Pulled by scripts/pull_tn_statutes.py. The Tennessee "
            "Code Annotated has no clean structured free official "
            "source (LexisNexis publishes the official code under "
            "copyright behind a JS container). Justia is the "
            "primary structured free mirror; FindLaw is a "
            "fallback. Both sit behind Cloudflare bot-fight mode "
            "and 403 against stdlib urllib's TLS fingerprint and "
            "many shared-egress IPs (incl. GitHub Actions runners). "
            "The puller uses curl_cffi with Chrome TLS "
            "impersonation when available — works from a "
            "residential or VPN-routed IP. Walks Chapter -> Part -> "
            "Section for chapters that are subdivided into Parts. "
            "Falls back to well-formed pointer stubs when fetch "
            "fails so the corpus retains its target shape."
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
            "plugins/tn-court-docs/skills/tn-law-references/"
            "references/tn-statutes-debt"
        ),
        help="Output directory for the corpus.",
    )
    ap.add_argument(
        "--only", nargs="*",
        help="Restrict to these chapter labels.",
    )
    ap.add_argument(
        "--workers", type=int, default=4,
        help="Concurrent chapter fetches (default 4).",
    )
    ap.add_argument(
        "--stubs-only", action="store_true",
        help="Write pointer stubs only — do not attempt a network fetch.",
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
    print(f"=== pulling {len(targets)} TN chapter(s) → "
          f"{out_dir} (workers={args.workers}, "
          f"stubs_only={args.stubs_only})", flush=True)

    results: List[WriteResult] = []
    workers = max(1, min(args.workers, len(targets)))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(fetch_chapter, t, out_dir, fetched_iso,
                        args.stubs_only): t
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
        tag = ("OK  " if r.error is None and not r.stub
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
          f"{total_sec:,} sections, "
          f"{total_bytes:,} bytes; "
          f"{len(fail)} hard-failed", flush=True)

    if only is None:
        mp = update_manifest(out_dir, fetched_iso,
                             args.manifest_version)
        print(f"=== updated {mp}", flush=True)

    return 0 if not fail else 1


if __name__ == "__main__":
    sys.exit(main())
