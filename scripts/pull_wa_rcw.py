#!/usr/bin/env python3
"""Pull selected debt-related RCW chapters from app.leg.wa.gov and convert to MD.

Output: plugins/wa-court-docs/skills/wa-law-references/references/wa-rcw-debt/
One MD file per chapter, each section as its own heading inside.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path

USER_AGENT = "claude-legal/1.0 (+https://github.com/codearranger/claude-legal) wa-rcw-puller"
BASE = "https://app.leg.wa.gov"
CHAPTER_URL = BASE + "/RCW/default.aspx?cite={chapter}"
SECTION_URL = BASE + "/RCW/default.aspx?cite={cite}"

# (chapter, short-name, description)
CHAPTERS: list[tuple[str, str, str]] = [
    ("4.16",   "4.16",   "Limitation of Actions (statute of limitations)"),
    ("4.28",   "4.28",   "Commencement of Actions / Service of Process"),
    ("4.56",   "4.56",   "Judgments"),
    ("4.84",   "4.84",   "Costs"),
    ("6.01",   "6.01",   "Enforcement of Judgments — General Provisions"),
    ("6.13",   "6.13",   "Homesteads"),
    ("6.15",   "6.15",   "Personal Property Exempt from Execution"),
    ("6.17",   "6.17",   "Executions"),
    ("6.21",   "6.21",   "Sales Under Execution, Order of Sale, or Decree"),
    ("6.25",   "6.25",   "Attachment"),
    ("6.27",   "6.27",   "Garnishment"),
    ("6.32",   "6.32",   "Proceedings Supplemental to Execution"),
    ("6.36",   "6.36",   "Uniform Enforcement of Foreign Judgments Act"),
    ("12.40",  "12.40",  "Small Claims"),
    ("19.16",  "19.16",  "Collection Agencies"),
    ("19.36",  "19.36",  "Contracts (Statute of Frauds)"),
    ("19.52",  "19.52",  "Interest — Usury"),
    ("19.86",  "19.86",  "Unfair Business Practices — Consumer Protection"),
    ("62A.1",  "62A.1",  "UCC — General Provisions"),
    ("62A.3",  "62A.3",  "UCC — Negotiable Instruments"),
    ("62A.9A", "62A.9A", "UCC — Secured Transactions"),
]


def http_get(url: str, *, retries: int = 3, sleep: float = 1.0) -> bytes:
    parsed = urllib.parse.urlsplit(url)
    safe_path = urllib.parse.quote(parsed.path, safe="/%")
    safe_url = urllib.parse.urlunsplit(
        (parsed.scheme, parsed.netloc, safe_path, parsed.query, parsed.fragment)
    )
    req = urllib.request.Request(safe_url, headers={"User-Agent": USER_AGENT})
    last_exc: Exception | None = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:
            last_exc = e
            time.sleep(sleep * (2**attempt))
    assert last_exc is not None
    raise last_exc


# ---- HTML → text ---------------------------------------------------------------------

def html_to_text(s: str) -> str:
    """Convert a chunk of HTML to plain text with paragraph breaks at div/p/br boundaries."""
    # Drop script/style entirely.
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", s, flags=re.IGNORECASE | re.DOTALL)
    # Emphasis first.
    s = re.sub(r"<(em|i)[^>]*>(.*?)</\1>", lambda m: f"*{m.group(2)}*", s, flags=re.IGNORECASE | re.DOTALL)
    s = re.sub(r"<(strong|b)[^>]*>(.*?)</\1>", lambda m: f"**{m.group(2)}**", s, flags=re.IGNORECASE | re.DOTALL)
    # span style="font-weight:bold" — RCW notes use inline span for bold; convert to **
    s = re.sub(
        r"<span[^>]*style=\"[^\"]*font-weight:\s*bold[^\"]*\"[^>]*>(.*?)</span>",
        lambda m: f"**{m.group(1)}**",
        s,
        flags=re.IGNORECASE | re.DOTALL,
    )
    # <br> → block break.
    s = re.sub(r"<br\s*/?>", "\x1e", s, flags=re.IGNORECASE)
    # Block tags → block break markers.
    s = re.sub(r"</(p|div|li|h\d|tr|td|th|blockquote|article|section)\s*>", "\x1e", s, flags=re.IGNORECASE)
    s = re.sub(r"<(p|div|li|h\d|tr|td|th|blockquote|article|section)[^>]*>", "\x1e", s, flags=re.IGNORECASE)
    # Strip remaining tags.
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    blocks: list[str] = []
    for raw in s.split("\x1e"):
        cleaned = re.sub(r"\s+", " ", raw).strip()
        if cleaned:
            blocks.append(cleaned)
    return "\n\n".join(blocks).strip()


# ---- Chapter index parsing -----------------------------------------------------------

def parse_chapter_index(html_text: str, chapter: str) -> tuple[str, list[tuple[str, str]]]:
    """Returns (chapter_caption, [(section_cite, section_caption), ...])."""
    # Caption: <h2><!-- field: CaptionsTitles --><div>...possibly with nested tags...</div><!-- field:
    cap_m = re.search(
        r"<h2[^>]*>\s*<!--\s*field:\s*CaptionsTitles\s*-->\s*(.*?)\s*<!--",
        html_text,
        re.DOTALL,
    )
    chapter_caption = ""
    if cap_m:
        # Strip any tags inside the caption and normalize whitespace.
        chapter_caption = re.sub(r"<[^>]+>", "", cap_m.group(1))
        chapter_caption = html.unescape(chapter_caption)
        chapter_caption = re.sub(r"\s+", " ", chapter_caption).strip()

    # Section rows in the index: <a href="...?cite=X.Y.Z">label</a> ... <td>Caption</td>
    # Section identifiers can use dot or hyphen as separator (e.g., 62A.1-101).
    sections: list[tuple[str, str]] = []
    seen: set[str] = set()
    chapter_pat = re.escape(chapter)
    row_re = re.compile(
        r"<a\s+href=['\"]https?://app\.leg\.wa\.gov/RCW/default\.aspx\?cite="
        + chapter_pat
        + r"([.\-][\d.A-Za-z\-]+)['\"]\s*>\s*[^<]+?\s*</a>\s*</td>\s*"
        r"<td[^>]*>\s*([^<]+?)\s*</td>",
        re.IGNORECASE | re.DOTALL,
    )
    for m in row_re.finditer(html_text):
        sep_and_suffix = m.group(1)  # leading "." or "-" plus the suffix
        cite = f"{chapter}{sep_and_suffix}"
        if cite in seen:
            continue
        seen.add(cite)
        caption = re.sub(r"\s+", " ", m.group(2)).strip().rstrip(".")
        sections.append((cite, caption))
    return chapter_caption, sections


# ---- Section parsing ------------------------------------------------------------------

def parse_section(html_text: str, cite: str) -> tuple[str, str]:
    """Returns (caption, body_md)."""
    cap_m = re.search(
        r"<h2[^>]*>\s*<!--\s*field:\s*CaptionsTitles\s*-->\s*(.*?)\s*<!--",
        html_text,
        re.DOTALL,
    )
    caption = ""
    if cap_m:
        caption = re.sub(r"<[^>]+>", "", cap_m.group(1))
        caption = html.unescape(caption)
        caption = re.sub(r"\s+", " ", caption).strip()

    # Content body — find <div id='contentWrapper' class='section-page'> and read until
    # we hit the panel div that follows.
    start_m = re.search(r"<div\s+id=['\"]contentWrapper['\"][^>]*>", html_text, re.IGNORECASE)
    if not start_m:
        return caption, ""
    body_start = start_m.end()
    # End markers, in priority order.
    end_idx = len(html_text)
    for marker in [
        '<div id="ContentPlaceHolder1_pnlExpanded"',
        "<div id='ContentPlaceHolder1_pnlExpanded'",
        '<div id="ContentPlaceHolder',
        "<div id='ContentPlaceHolder",
        "<footer",
    ]:
        idx = html_text.find(marker, body_start)
        if 0 < idx < end_idx:
            end_idx = idx
    raw_body = html_text[body_start:end_idx]
    body = html_to_text(raw_body)
    return caption, body


def fetch_section(cite: str) -> tuple[str, str, str, str | None]:
    try:
        html_bytes = http_get(SECTION_URL.format(cite=cite))
        caption, body = parse_section(html_bytes.decode("utf-8", errors="replace"), cite)
        return cite, caption, body, None
    except Exception as e:
        return cite, "", "", f"{type(e).__name__}: {e}"


# ---- Render chapter MD ----------------------------------------------------------------

def render_chapter_md(
    chapter: str,
    description: str,
    chapter_caption: str,
    sections: list[tuple[str, str]],
    fetched: dict[str, tuple[str, str, str | None]],
) -> str:
    today = date.today().isoformat()
    out: list[str] = []
    title = chapter_caption or description
    out.append(f"# RCW Chapter {chapter} — {title}")
    out.append("")
    out.append(f"- Citation: RCW Chapter {chapter}")
    out.append(f"- Description: {description}")
    out.append(f"- Source: {CHAPTER_URL.format(chapter=chapter)}")
    out.append(f"- Pulled: {today}")
    out.append(f"- Sections: {len(sections)}")
    out.append("")
    out.append("> Verbatim text from the Washington State Legislature website. Citation")
    out.append("> history (`[ ... ]`) and `Notes:` blocks are preserved as published.")
    out.append("")

    out.append("## Contents")
    out.append("")
    for cite, caption in sections:
        anchor = f"sec-{cite.replace('.', '-')}"
        cap = caption.rstrip(".")
        out.append(f"- [RCW {cite} — {cap}](#{anchor})")
    out.append("")

    for cite, list_caption in sections:
        if cite not in fetched:
            continue
        sec_caption, body, err = fetched[cite]
        caption = sec_caption or list_caption
        anchor = f"sec-{cite.replace('.', '-')}"
        out.append(f'<a id="{anchor}"></a>')
        out.append(f"## RCW {cite} — {caption}")
        out.append("")
        out.append(f"Source: {SECTION_URL.format(cite=cite)}")
        out.append("")
        if err:
            out.append(f"> **Fetch failed:** {err}")
            out.append("")
        elif not body:
            out.append("> _(empty extraction)_")
            out.append("")
        else:
            out.append(body)
            out.append("")
    text = "\n".join(out).rstrip() + "\n"
    return re.sub(r"\n{3,}", "\n\n", text)


# ---- main -----------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="plugins/wa-court-docs/skills/wa-law-references/references/wa-rcw-debt")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--only", nargs="*", help="Optional list of chapter numbers to limit to.")
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    only = set(args.only) if args.only else None
    grand_total = 0
    grand_failed = 0

    for chapter, short, description in CHAPTERS:
        if only and chapter not in only:
            continue
        print(f"\n=== RCW Chapter {chapter} — {description} ===", flush=True)
        try:
            idx_html = http_get(CHAPTER_URL.format(chapter=chapter)).decode("utf-8", errors="replace")
        except Exception as e:
            print(f"  ! chapter index failed: {e}", flush=True)
            continue
        chapter_caption, sections = parse_chapter_index(idx_html, chapter)
        print(f"  caption: {chapter_caption!r}", flush=True)
        print(f"  found {len(sections)} sections", flush=True)
        if not sections:
            (out_dir / f"RCW-{short.replace('.', '_')}.md").write_text(
                f"# RCW Chapter {chapter}\n\n_No sections extracted from the index page._\n",
                encoding="utf-8",
            )
            continue

        fetched: dict[str, tuple[str, str, str | None]] = {}
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = {ex.submit(fetch_section, cite): cite for cite, _cap in sections}
            done = 0
            for fut in as_completed(futs):
                done += 1
                cite, caption, body, err = fut.result()
                fetched[cite] = (caption, body, err)
                if err:
                    print(f"    [{done}/{len(sections)}] {cite} FAIL: {err}", flush=True)
                    grand_failed += 1

        md = render_chapter_md(chapter, description, chapter_caption, sections, fetched)
        out_path = out_dir / f"RCW-{short.replace('.', '_')}.md"
        out_path.write_text(md, encoding="utf-8")
        print(f"  wrote {out_path} ({len(md):,} bytes)", flush=True)
        grand_total += len(sections)

    print(f"\nDone. {grand_total} sections; {grand_failed} fetch errors.", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
