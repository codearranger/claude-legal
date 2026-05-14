#!/usr/bin/env python3
"""Pull the model Uniform Commercial Code (Articles 1, 2, 3, 9) from Cornell LII and convert to MD.

Each article gets one MD file with all sections, headings preserved.

Source: https://www.law.cornell.edu/ucc/

Note: Cornell LII publishes the *model* UCC text. The version actually in force
in Washington is in RCW Title 62A (pulled separately). The model text is useful
because comments and uniformity references are anchored to it.
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

USER_AGENT = "claude-legal/1.0 (+https://github.com/codearranger/claude-legal) ucc-puller"
BASE = "https://www.law.cornell.edu/ucc"

ARTICLES: list[tuple[str, str]] = [
    ("1", "General Provisions"),
    ("2", "Sales"),
    ("3", "Negotiable Instruments"),
    ("9", "Secured Transactions"),
]


def http_get(url: str, *, retries: int = 3, sleep: float = 1.0) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
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


def fetch_section_list(article: str) -> list[str]:
    html_text = http_get(f"{BASE}/{article}").decode("utf-8", errors="replace")
    sections = sorted(set(re.findall(rf"/ucc/{article}/({article}-\d+(?:[A-Z])?)", html_text)),
                      key=lambda s: tuple(int(p) if p.isdigit() else p for p in re.split(r"(\d+)", s) if p))
    return sections


# ---- HTML → Markdown for a single section -------------------------------------------

TAG_RE = re.compile(r"<(/?)([a-zA-Z0-9]+)([^>]*)>", re.DOTALL)


def html_to_text(s: str) -> str:
    """Strip HTML tags but preserve paragraph breaks, list items, emphasis, and link text.

    Strategy: split into block segments (one per <p>/<li>/<h*>/<div>), then collapse
    all whitespace within each block to single spaces, then re-join with blank lines.
    """
    # Emphasis tags first (before stripping others).
    s = re.sub(r"<(em|i)[^>]*>(.*?)</\1>", lambda m: f"*{m.group(2)}*", s, flags=re.IGNORECASE | re.DOTALL)
    s = re.sub(r"<(strong|b)[^>]*>(.*?)</\1>", lambda m: f"**{m.group(2)}**", s, flags=re.IGNORECASE | re.DOTALL)
    # <br> → block separator marker.
    s = re.sub(r"<br\s*/?>", "\n\n\x1e", s, flags=re.IGNORECASE)
    # Mark block boundaries with a control char (\x1e = record separator).
    s = re.sub(r"</(p|div|li|h\d|tr|td|th|blockquote|article|section)\s*>", "\x1e", s, flags=re.IGNORECASE)
    s = re.sub(r"<(p|div|li|h\d|tr|td|th|blockquote|article|section)[^>]*>", "\x1e", s, flags=re.IGNORECASE)
    # Strip remaining tags.
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    # Split on block markers, normalize each block's internal whitespace, drop empties.
    blocks: list[str] = []
    for raw in s.split("\x1e"):
        cleaned = re.sub(r"\s+", " ", raw).strip()
        if cleaned:
            blocks.append(cleaned)
    return "\n\n".join(blocks).strip()


def parse_section(html_text: str, section_id: str) -> tuple[str, str]:
    """Returns (heading, body_md) for one section page."""
    h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", html_text, re.DOTALL)
    raw_heading = h1_match.group(1) if h1_match else section_id
    heading = re.sub(r"\s+", " ", html_to_text(raw_heading)).strip()
    if not heading or heading == section_id:
        heading = f"§ {section_id}"

    art_match = re.search(r"<article[^>]*>(.*?)</article>", html_text, re.DOTALL)
    if not art_match:
        return heading, ""
    art_html = art_match.group(1)
    # Strip the prev/up/next navigation block.
    art_html = re.sub(r"<nav[^>]*>.*?</nav>", "", art_html, flags=re.DOTALL | re.IGNORECASE)
    body = html_to_text(art_html)
    return heading, body


def fetch_section(article: str, section_id: str) -> tuple[str, str, str, str | None]:
    url = f"{BASE}/{article}/{section_id}"
    try:
        html_bytes = http_get(url)
        heading, body = parse_section(html_bytes.decode("utf-8", errors="replace"), section_id)
        return section_id, heading, body, None
    except Exception as e:
        return section_id, f"§ {section_id}", "", f"{type(e).__name__}: {e}"


def render_article_md(article: str, title: str, sections: list[tuple[str, str, str, str | None]]) -> str:
    today = date.today().isoformat()
    out: list[str] = []
    out.append(f"# UCC Article {article} — {title}")
    out.append("")
    out.append(f"- Citation: U.C.C. art. {article} (model text)")
    out.append(f"- Source: {BASE}/{article}")
    out.append(f"- Pulled: {today}")
    out.append(f"- Sections: {len(sections)}")
    out.append("")
    out.append("> Verbatim text from Cornell Legal Information Institute. The *model* UCC")
    out.append("> as drafted by ALI/ULC; the version in force in Washington is in")
    out.append("> [RCW Title 62A](../wa-rcw-debt/). Cite the RCW for state-court matters and")
    out.append("> reference the model + comments only when interpreting uniform language.")
    out.append("")

    out.append("## Contents")
    out.append("")
    for sid, heading, _body, _err in sections:
        anchor = f"sec-{sid.lower()}"
        out.append(f"- [{heading}](#{anchor})")
    out.append("")

    for sid, heading, body, err in sections:
        anchor = f"sec-{sid.lower()}"
        out.append(f'<a id="{anchor}"></a>')
        out.append(f"## {heading}")
        out.append("")
        out.append(f"Source: {BASE}/{article}/{sid}")
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
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="plugins/claude-legal-federal-laws/references/ucc-model")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--only", nargs="*", help="Optional list of article numbers to limit to.")
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    only = set(args.only) if args.only else None

    for article, title in ARTICLES:
        if only and article not in only:
            continue
        print(f"\n=== UCC Article {article} — {title} ===", flush=True)
        section_ids = fetch_section_list(article)
        print(f"  found {len(section_ids)} sections", flush=True)

        results: dict[str, tuple[str, str, str, str | None]] = {}
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = {ex.submit(fetch_section, article, sid): sid for sid in section_ids}
            done = 0
            for fut in as_completed(futs):
                done += 1
                sid, heading, body, err = fut.result()
                results[sid] = (sid, heading, body, err)
                if err:
                    print(f"    [{done}/{len(section_ids)}] {sid} FAIL: {err}", flush=True)

        # Preserve original ordering.
        ordered = [results[s] for s in section_ids if s in results]
        md = render_article_md(article, title, ordered)
        path = out_dir / f"Article-{article}.md"
        path.write_text(md, encoding="utf-8")
        print(f"  wrote {path} ({len(md):,} bytes)", flush=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
