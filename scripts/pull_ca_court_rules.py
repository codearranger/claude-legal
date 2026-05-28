#!/usr/bin/env python3
"""Pull California Rules of Court (CRC) and selected local-rule
indexes from courts.ca.gov and convert them to per-Title Markdown
files.

Output: plugins/ca-court-docs/skills/ca-law-references/references/court-rules/

The script fetches the rule-set index pages, extracts per-rule
links, downloads the HTML for each rule, and concatenates the
results into one MD file per Title (e.g., `CRC-Title-2.md`).

Modeled on scripts/pull_court_rules.py (the WA puller). The WA
version downloads per-rule PDFs and runs pdftotext; this CA
version uses the HTML rule pages because courts.ca.gov serves the
rules as static HTML rather than per-rule PDFs.

NOTE: courts.ca.gov has undergone a site redesign in recent years.
The URL patterns and HTML structure may evolve. If parsing fails,
update the BASE / INDEX_URL / parser below. The site presents the
California Rules of Court at:

  https://courts.ca.gov/forms-rules/rules-court

Per-Title indexes live at:

  https://courts.ca.gov/cms/rules/index/<word>      (one, two, three, ...)

And per-rule pages have URLs like:

  https://courts.ca.gov/cms/rules/index/three/rule3_1113

Each Title index contains a nested list with Division/Chapter
headings (each a `<li class="list__item paragraph--type--rule-section--default">`
containing a `<div>Division N. ...</div>` or `<div>Chapter N. ...</div>`)
and rule links (`<li class="list__item"><a href="...rule3_X">Rule N.M. Caption</a></li>`).

Each rule page wraps the verbatim rule body inside
`<div class="container jcc-rulesformatting stack">` inside
`<div class="box roc__rule__content">` inside `<article class="roc__rule">`.

This script is intentionally conservative — it caches the
discovered URLs and prints them in dry-run mode for verification.
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

BASE = "https://courts.ca.gov"
INDEX_URL = BASE + "/forms-rules/rules-court"
TITLE_INDEX_FMT = BASE + "/cms/rules/index/{slug}"
USER_AGENT = (
    "claude-legal/1.0 (+https://github.com/codearranger/claude-legal) "
    "ca-court-rules-puller"
)


# ---- Configuration: which titles / rule sets to pull -------------------------

# Each entry maps an OUTPUT FILE to a Title number and a description.
# Titles 1-10 of the California Rules of Court cover the main civil-
# practice content. All 9 published titles (1-5, 7-10 — Title 6 is
# reserved by the Judicial Council) are pulled so the corpus is
# complete; the consumer-debt skill cites mostly Titles 2-3 and 8,
# but Titles 1, 4, 9, 10 are present for cross-reference.

TITLES: list[tuple[str, str, str]] = [
    # (output_stem, title_slug, description)
    # The slug is the URL-path word the site uses for the title — bare
    # ordinals ("one", "two", ...), not "title-one". Title 6 is reserved.
    ("CRC-Title-1-General-Rules",       "one",   "General Rules"),
    ("CRC-Title-2-Trial-Court-Rules",   "two",   "Rules Applicable in All Trial Courts"),
    ("CRC-Title-3-Civil-Rules",         "three", "Civil Rules"),
    ("CRC-Title-4-Criminal-Rules",      "four",  "Criminal Rules"),
    ("CRC-Title-5-Family-Law-Rules",    "five",  "Family and Juvenile Rules"),
    ("CRC-Title-7-Probate-Rules",       "seven", "Probate Rules"),
    ("CRC-Title-8-Appellate-Rules",     "eight", "Appellate Rules"),
    ("CRC-Title-9-Attorney-Rules",      "nine",  "Rules on Law Practice, Attorneys, and Judges"),
    ("CRC-Title-10-Judicial-Admin",     "ten",   "Judicial Administration Rules"),
]


# Local-rule URL pointers — one MD per court. The HTML structure
# varies wildly across counties; the script writes a stub with the
# discovered URL so a human can fill in the specific local-rule
# numbers. This is the limitation of authoring without per-court
# scraping logic.

LOCAL_RULE_COURTS: list[tuple[str, str, str]] = [
    # (output_stem, court name, local-rules URL)
    ("LASC-Local-Rules",         "Los Angeles Superior Court",      "https://lacourt.org/division/civil/civil-local-rules"),
    ("SFSC-Local-Rules",         "San Francisco Superior Court",    "https://sfsuperiorcourt.org/divisions/civil/local-rules"),
    ("OCSC-Local-Rules",         "Orange County Superior Court",    "https://occourts.org/general-public/local-rules-of-court"),
    ("Other-County-Local-Rules", "Other most-populous counties",    "https://courts.ca.gov/courts/superior-courts"),
]


# ---- Networking --------------------------------------------------------------

def http_get(url: str, *, retries: int = 3, sleep: float = 1.5) -> bytes:
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


# ---- HTML → text -------------------------------------------------------------

def html_to_text(s: str) -> str:
    """Convert HTML fragment to plain text with paragraph breaks at
    div/p/br boundaries. Same approach as the WA puller."""
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", s, flags=re.IGNORECASE | re.DOTALL)
    s = re.sub(r"<(em|i)[^>]*>(.*?)</\1>", lambda m: f"*{m.group(2)}*", s, flags=re.IGNORECASE | re.DOTALL)
    s = re.sub(r"<(strong|b)[^>]*>(.*?)</\1>", lambda m: f"**{m.group(2)}**", s, flags=re.IGNORECASE | re.DOTALL)
    s = re.sub(r"<br\s*/?>", "\x1e", s, flags=re.IGNORECASE)
    s = re.sub(r"</(p|div|li|h\d|tr|td|th|blockquote|article|section)\s*>", "\x1e", s, flags=re.IGNORECASE)
    s = re.sub(r"<(p|div|li|h\d|tr|td|th|blockquote|article|section)[^>]*>", "\x1e", s, flags=re.IGNORECASE)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    blocks: list[str] = []
    for raw in s.split("\x1e"):
        cleaned = re.sub(r"\s+", " ", raw).strip()
        if cleaned:
            blocks.append(cleaned)
    return "\n\n".join(blocks).strip()


# ---- Index parsing -----------------------------------------------------------

# Each entry in the parsed index is one of:
#   ("rule",     rule_num, caption, url)
#   ("division", "",       heading, "")
#   ("chapter",  "",       heading, "")
# The order preserves the natural document ordering of the Title.
IndexEntry = tuple[str, str, str, str]


def parse_title_index(html_text: str, title_slug: str) -> list[IndexEntry]:
    """Returns an ordered list of index entries for a CRC Title.

    The site renders each Title index as a nested list:

        <li class="list__item paragraph--type--rule-section--default">
          <div>Division N. Caption</div>
          <ul ...>
            <li class="list__item paragraph--type--rule-section--default">
              <div>Chapter N. Caption</div>
              <ul ...>
                <li class="list__item">
                  <a href="/cms/rules/index/<slug>/rule3_1113">Rule 3.1113. Memorandum</a>
                </li>
                ...
              </ul>
            </li>
            ...
          </ul>
        </li>

    This walker emits a flat ordered sequence of (kind, num, text, url)
    tuples so the renderer can faithfully reproduce the Division /
    Chapter / Rule structure.
    """
    out: list[IndexEntry] = []
    seen_rules: set[str] = set()

    # Pattern matching either:
    #   (A) a "rule-section" <li> (Division or Chapter) with its <div> caption, OR
    #   (B) a "list__item" <li> with a rule anchor inside.
    # We iterate over the union, preserving document order.
    href_prefix = f"/cms/rules/index/{title_slug}/rule"

    section_re = re.compile(
        r'<li\s+class="list__item\s+paragraph--type--rule-section--default">\s*'
        r'\s*<div>([^<]+)</div>',
        re.IGNORECASE,
    )
    rule_re = re.compile(
        r'<a\s+href="(' + re.escape(href_prefix) + r'(\d+[A-Za-z0-9_]*))"\s*'
        r'[^>]*>\s*(.*?)\s*</a>',
        re.IGNORECASE | re.DOTALL,
    )

    # Run both patterns and merge by position in the document
    section_hits = [(m.start(), "section", m) for m in section_re.finditer(html_text)]
    rule_hits = [(m.start(), "rule", m) for m in rule_re.finditer(html_text)]
    hits = sorted(section_hits + rule_hits, key=lambda t: t[0])

    for _pos, kind, m in hits:
        if kind == "section":
            heading = html.unescape(m.group(1)).strip()
            low = heading.lower()
            if low.startswith("division"):
                out.append(("division", "", heading, ""))
            elif low.startswith("chapter"):
                out.append(("chapter", "", heading, ""))
            elif low.startswith("part"):
                out.append(("chapter", "", heading, ""))
            else:
                # Generic section heading (e.g., "Standards", "Appendix") — keep
                out.append(("division", "", heading, ""))
        else:  # rule
            href = m.group(1)
            raw = m.group(2)  # e.g., "3_1113" or "3_1113a"
            # Normalize: rule "3_1113" → "3.1113"; "3_1113a" → "3.1113a"
            rule_num = raw.replace("_", ".")
            if rule_num in seen_rules:
                continue
            seen_rules.add(rule_num)
            caption = re.sub(r"<[^>]+>", "", m.group(3))
            caption = html.unescape(caption).strip()
            # Strip a leading "Rule N.M. " prefix if present in the anchor text
            caption = re.sub(
                r"^Rule\s+" + re.escape(rule_num) + r"\.?\s*",
                "",
                caption,
                flags=re.IGNORECASE,
            ).strip()
            if not caption:
                caption = f"Rule {rule_num}"
            url = BASE + href
            out.append(("rule", rule_num, caption, url))

    return out


# ---- Rule parsing ------------------------------------------------------------

def parse_rule(html_text: str) -> tuple[str, str]:
    """Returns (caption, body_md). Looks for the main content area
    of a rule page on courts.ca.gov.

    Each rule page has the verbatim text inside:
        <div class="container jcc-rulesformatting stack">...</div>
    sitting inside:
        <div class="box roc__rule__content">...</div>
    The page title is rendered as:
        <h1 class="hangover__title ..."><span>Rule N.M. Caption</span></h1>
    """
    caption = ""
    body = ""

    # Page heading: <h1 class="hangover__title ..."><span>Rule N.M. Caption</span></h1>
    cap_m = re.search(
        r'<h1[^>]*class="[^"]*hangover__title[^"]*"[^>]*>\s*(?:<span[^>]*>)?\s*(.*?)\s*(?:</span>)?\s*</h1>',
        html_text,
        re.IGNORECASE | re.DOTALL,
    )
    if cap_m:
        caption = re.sub(r"<[^>]+>", "", cap_m.group(1))
        caption = html.unescape(caption).strip()
    if not caption:
        # Fallback to a generic <h1>
        cap_m = re.search(r"<h1[^>]*>(.*?)</h1>", html_text, re.IGNORECASE | re.DOTALL)
        if cap_m:
            caption = re.sub(r"<[^>]+>", "", cap_m.group(1))
            caption = html.unescape(caption).strip()

    # Main rule body — primary selector first, then progressively looser fallbacks.
    body_re_candidates = [
        # Innermost container that holds only the rule body markup
        re.compile(
            r'<div\s+class="container\s+jcc-rulesformatting\s+stack"[^>]*>(.*)',
            re.IGNORECASE | re.DOTALL,
        ),
        # Slight variation: classes in different order
        re.compile(
            r'<div\s+class="[^"]*jcc-rulesformatting[^"]*"[^>]*>(.*)',
            re.IGNORECASE | re.DOTALL,
        ),
        # Outer wrapper if the inner div is missing
        re.compile(
            r'<div\s+class="[^"]*roc__rule__content[^"]*"[^>]*>(.*)',
            re.IGNORECASE | re.DOTALL,
        ),
        re.compile(r"<article[^>]*>(.*?)</article>", re.IGNORECASE | re.DOTALL),
    ]
    for body_re in body_re_candidates:
        m = body_re.search(html_text)
        if not m:
            continue
        frag = m.group(1)
        # Close at the next </article> or </main>, whichever comes first
        close = re.search(r"</article>|</main>", frag, re.IGNORECASE)
        if close:
            frag = frag[: close.start()]
        body = html_to_text(frag)
        if body:
            break

    return caption, body


def fetch_rule(rule_num: str, url: str) -> tuple[str, str, str, str, str | None]:
    """Returns (rule_num, url, caption, body, error|None)."""
    try:
        html_bytes = http_get(url)
        caption, body = parse_rule(html_bytes.decode("utf-8", errors="replace"))
        return rule_num, url, caption, body, None
    except Exception as e:
        return rule_num, url, "", "", f"{type(e).__name__}: {e}"


# ---- Render Title MD ---------------------------------------------------------

def render_title_md(
    stem: str,
    description: str,
    title_slug: str,
    entries: list[IndexEntry],
    fetched: dict[str, tuple[str, str, str, str | None]],
) -> str:
    today = date.today().isoformat()
    rule_count = sum(1 for kind, *_ in entries if kind == "rule")

    out: list[str] = []
    out.append(f"# California Rules of Court — {description}")
    out.append("")
    out.append(f"- Citation: Cal. Rules of Court, {description}")
    out.append(f"- Source: {TITLE_INDEX_FMT.format(slug=title_slug)}")
    out.append(f"- Pulled: {today}")
    out.append(f"- Rules: {rule_count}")
    out.append("")
    out.append("> Verbatim rule text scraped from courts.ca.gov.")
    out.append("> The Judicial Council periodically amends these rules.")
    out.append("> Verify against the current text before relying.")
    out.append("")

    # Table of contents — preserves Division / Chapter hierarchy.
    out.append("## Contents")
    out.append("")
    for kind, rule_num, text, _url in entries:
        if kind == "division":
            out.append("")
            out.append(f"**{text}**")
            out.append("")
        elif kind == "chapter":
            out.append(f"- *{text}*")
        else:  # rule
            anchor = f"rule-{rule_num.replace('.', '-')}"
            cap = text.rstrip(".")
            out.append(f"  - [Rule {rule_num} — {cap}](#{anchor})")
    out.append("")

    # Rule bodies in order, with Division / Chapter section headings.
    for kind, rule_num, text, _url in entries:
        if kind == "division":
            out.append(f"## {text}")
            out.append("")
            continue
        if kind == "chapter":
            out.append(f"### {text}")
            out.append("")
            continue
        # kind == "rule"
        if rule_num not in fetched:
            continue
        url, caption, body, err = fetched[rule_num]
        caption = caption or text
        # Strip a redundant "Rule N.M." prefix from caption if present
        caption = re.sub(
            r"^Rule\s+" + re.escape(rule_num) + r"\.?\s*",
            "",
            caption,
            flags=re.IGNORECASE,
        ).strip()
        anchor = f"rule-{rule_num.replace('.', '-')}"
        out.append(f'<a id="{anchor}"></a>')
        out.append(f"#### Rule {rule_num}. {caption}")
        out.append("")
        out.append(f"Source: {url}")
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
    text_out = "\n".join(out).rstrip() + "\n"
    return re.sub(r"\n{3,}", "\n\n", text_out)


def render_local_rules_pointer(
    stem: str,
    court_name: str,
    url: str,
) -> str:
    today = date.today().isoformat()
    out: list[str] = []
    out.append(f"# {court_name} — Local Rules")
    out.append("")
    out.append(f"- Court: {court_name}")
    out.append(f"- Source: {url}")
    out.append(f"- Pulled: {today}")
    out.append("")
    out.append(
        "> Per-court local-rule HTML varies widely across California "
        "Superior Courts. This file is a pointer to the court's local-"
        "rules index. The substantive content for this corpus is "
        "authored in the same-named MD file (see the existing CRC "
        "court-rules corpus); the puller writes only this stub when "
        "an automated scrape is not feasible."
    )
    out.append("")
    out.append("## Re-pull")
    out.append("")
    out.append(
        "Adjust `LOCAL_RULE_COURTS` in `scripts/pull_ca_court_rules.py` "
        "and (if needed) add per-court HTML parsing in `parse_local_rule`."
    )
    out.append("")
    return "\n".join(out) + "\n"


# ---- Main --------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out",
        default="plugins/ca-court-docs/skills/ca-law-references/references/court-rules",
    )
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument(
        "--only",
        nargs="*",
        help="Optional list of output-file stems to limit to (e.g. CRC-Title-3-Civil-Rules).",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Print URLs without fetching.",
    )
    ap.add_argument(
        "--skip-local",
        action="store_true",
        help="Skip the local-rules stubs (only fetch CRC Titles).",
    )
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    only = set(args.only) if args.only else None
    grand_total = 0
    grand_failed = 0

    for stem, title_slug, description in TITLES:
        if only and stem not in only:
            continue
        index_url = TITLE_INDEX_FMT.format(slug=title_slug)
        print(f"\n=== {stem} — {description} ===", flush=True)
        print(f"  index: {index_url}", flush=True)

        if args.dry_run:
            print(f"  (dry-run) would fetch {index_url}")
            continue

        try:
            idx_html = http_get(index_url).decode("utf-8", errors="replace")
        except Exception as e:
            print(f"  ! index failed: {e}", flush=True)
            continue
        entries = parse_title_index(idx_html, title_slug)
        rule_entries = [e for e in entries if e[0] == "rule"]
        print(
            f"  found {len(rule_entries)} rules "
            f"({sum(1 for e in entries if e[0] == 'division')} divisions, "
            f"{sum(1 for e in entries if e[0] == 'chapter')} chapters)",
            flush=True,
        )

        if not rule_entries:
            (out_dir / f"{stem}.md").write_text(
                f"# {description}\n\n_No rules extracted from {index_url}._\n",
                encoding="utf-8",
            )
            continue

        fetched: dict[str, tuple[str, str, str, str | None]] = {}
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = {
                ex.submit(fetch_rule, rule_num, url): rule_num
                for _kind, rule_num, _cap, url in rule_entries
            }
            done = 0
            for fut in as_completed(futs):
                done += 1
                rule_num, url, caption, body, err = fut.result()
                fetched[rule_num] = (url, caption, body, err)
                if err:
                    print(
                        f"    [{done}/{len(rule_entries)}] Rule {rule_num} FAIL: {err}",
                        flush=True,
                    )
                    grand_failed += 1

        md = render_title_md(stem, description, title_slug, entries, fetched)
        out_path = out_dir / f"{stem}.md"
        out_path.write_text(md, encoding="utf-8")
        print(f"  wrote {out_path} ({len(md):,} bytes)", flush=True)
        grand_total += len(rule_entries)

    if not args.skip_local:
        for stem, court_name, url in LOCAL_RULE_COURTS:
            if only and stem not in only:
                continue
            print(f"\n=== {stem} — {court_name} ===", flush=True)
            print(f"  pointer: {url}", flush=True)
            if args.dry_run:
                continue
            # Local-rule HTML varies per court; the puller writes a
            # pointer stub. Substantive content stays in the human-
            # authored MD file in the same directory.
            target = out_dir / f"{stem}.md"
            if target.exists():
                print(f"  skip (file already authored): {target}", flush=True)
                continue
            md = render_local_rules_pointer(stem, court_name, url)
            target.write_text(md, encoding="utf-8")
            print(f"  wrote {target}", flush=True)

    print(
        f"\nDone. {grand_total} rules; {grand_failed} fetch errors.",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
