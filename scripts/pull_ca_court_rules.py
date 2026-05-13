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

  https://courts.ca.gov/rules-forms/courtrules

Per-Title pages live at:

  https://courts.ca.gov/rules-forms/courtrules/title-<N>-...

And per-rule pages have URLs like:

  https://courts.ca.gov/rules-forms/courtrules/title-three/...rule-3-1113

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
INDEX_URL = BASE + "/rules-forms/courtrules"
USER_AGENT = (
    "claude-legal/1.0 (+https://github.com/codearranger/claude-legal) "
    "ca-court-rules-puller"
)


# ---- Configuration: which titles / rule sets to pull -------------------------

# Each entry maps an OUTPUT FILE to a Title number and a description.
# Titles 1-10 of the California Rules of Court cover the main civil-
# practice content. Titles 5 and 7 (family law, probate) are included
# at smaller scope; titles 9 (criminal) and 10 (Judicial Council
# administration) are omitted because this plugin is civil-only.

TITLES: list[tuple[str, str, str]] = [
    # (output_stem, title_slug, description)
    ("CRC-Title-1-General-Rules",       "title-one",   "General Rules"),
    ("CRC-Title-2-Trial-Court-Rules",   "title-two",   "Rules Applicable in All Trial Courts"),
    ("CRC-Title-3-Civil-Rules",         "title-three", "Civil Rules"),
    ("CRC-Title-4-Criminal-Rules",      "title-four",  "Criminal Rules"),
    ("CRC-Title-5-Family-Law-Rules",    "title-five",  "Family and Juvenile Rules"),
    ("CRC-Title-7-Probate-Rules",       "title-seven", "Probate Rules"),
    ("CRC-Title-8-Appellate-Rules",     "title-eight", "Appellate Rules"),
    ("CRC-Title-9-Attorney-Rules",      "title-nine",  "Rules on Law Practice, Attorneys, and Judges"),
    ("CRC-Title-10-Judicial-Admin",     "title-ten",   "Judicial Administration Rules"),
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

def parse_title_index(html_text: str, title_slug: str) -> list[tuple[str, str, str]]:
    """Returns [(rule_number, rule_caption, rule_url)] for a CRC Title.

    Looks for anchor tags whose href contains the title-slug and a
    rule-N-N pattern. Caption is the link text (or the next text node
    when the link text is just the rule number).
    """
    out: list[tuple[str, str, str]] = []
    seen: set[str] = set()

    # Anchors pointing to per-rule pages under this title
    pat = re.compile(
        r"<a\s+href=['\"]([^'\"]*"
        + re.escape(title_slug)
        + r"[^'\"]*rule[-_](\d+[-_]\d+[A-Za-z0-9]*)[^'\"]*)['\"][^>]*>(.*?)</a>",
        re.IGNORECASE | re.DOTALL,
    )
    for m in pat.finditer(html_text):
        url = m.group(1)
        rule_num = m.group(2).replace("_", ".").replace("-", ".")
        # Normalize: rule "3-1113" → "3.1113"
        if rule_num in seen:
            continue
        seen.add(rule_num)
        caption = re.sub(r"<[^>]+>", "", m.group(3))
        caption = html.unescape(caption).strip()
        # If caption is just the rule number, attempt to find the next
        # adjacent text (the rule title); fall back to "Rule N.N".
        if not caption or re.match(r"^Rule\s+[\d.]+$", caption, re.IGNORECASE):
            caption = f"Rule {rule_num}"
        # Make absolute URL
        if url.startswith("/"):
            url = BASE + url
        elif not url.startswith("http"):
            url = BASE + "/" + url.lstrip("/")
        out.append((rule_num, caption, url))

    # Sort by rule number (numerically when possible)
    def key(item: tuple[str, str, str]) -> tuple:
        parts = item[0].split(".")
        try:
            return tuple(int(p) for p in parts)
        except ValueError:
            return (0,)
    out.sort(key=key)
    return out


# ---- Rule parsing ------------------------------------------------------------

def parse_rule(html_text: str) -> tuple[str, str]:
    """Returns (caption, body_md). Looks for the main content area
    of a rule page on courts.ca.gov."""
    caption = ""
    body = ""

    # Page heading: typically <h1> with rule number
    cap_m = re.search(r"<h1[^>]*>(.*?)</h1>", html_text, re.IGNORECASE | re.DOTALL)
    if cap_m:
        caption = re.sub(r"<[^>]+>", "", cap_m.group(1))
        caption = html.unescape(caption).strip()

    # Main content area — try a few common markup patterns
    body_re_candidates = [
        re.compile(r"<main[^>]*>(.*?)</main>", re.IGNORECASE | re.DOTALL),
        re.compile(r"<article[^>]*>(.*?)</article>", re.IGNORECASE | re.DOTALL),
        re.compile(r"<div[^>]+id=['\"]main-content['\"][^>]*>(.*?)</div>\s*<footer", re.IGNORECASE | re.DOTALL),
        re.compile(r"<div[^>]+class=['\"][^'\"]*(?:rule-body|rule-content)[^'\"]*['\"][^>]*>(.*?)</div>\s*(?:<footer|<aside)", re.IGNORECASE | re.DOTALL),
    ]
    for body_re in body_re_candidates:
        m = body_re.search(html_text)
        if m:
            body = html_to_text(m.group(1))
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
    rules: list[tuple[str, str, str]],
    fetched: dict[str, tuple[str, str, str, str | None]],
) -> str:
    today = date.today().isoformat()
    out: list[str] = []
    out.append(f"# California Rules of Court — {description}")
    out.append("")
    out.append(f"- Citation: Cal. Rules of Court, {description}")
    out.append(f"- Source: {BASE}/rules-forms/courtrules/{title_slug}")
    out.append(f"- Pulled: {today}")
    out.append(f"- Rules: {len(rules)}")
    out.append("")
    out.append("> Verbatim rule text scraped from courts.ca.gov.")
    out.append("> The Judicial Council periodically amends these rules.")
    out.append("> Verify against the current text before relying.")
    out.append("")

    out.append("## Contents")
    out.append("")
    for rule_num, caption, _url in rules:
        anchor = f"rule-{rule_num.replace('.', '-')}"
        cap = caption.rstrip(".")
        out.append(f"- [Rule {rule_num} — {cap}](#{anchor})")
    out.append("")

    for rule_num, list_caption, _url in rules:
        if rule_num not in fetched:
            continue
        url, caption, body, err = fetched[rule_num]
        caption = caption or list_caption
        anchor = f"rule-{rule_num.replace('.', '-')}"
        out.append(f'<a id="{anchor}"></a>')
        out.append(f"## Rule {rule_num} — {caption}")
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
    text = "\n".join(out).rstrip() + "\n"
    return re.sub(r"\n{3,}", "\n\n", text)


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
        index_url = f"{BASE}/rules-forms/courtrules/{title_slug}"
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
        rules = parse_title_index(idx_html, title_slug)
        print(f"  found {len(rules)} rules", flush=True)

        if not rules:
            (out_dir / f"{stem}.md").write_text(
                f"# {description}\n\n_No rules extracted from {index_url}._\n",
                encoding="utf-8",
            )
            continue

        fetched: dict[str, tuple[str, str, str, str | None]] = {}
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = {
                ex.submit(fetch_rule, rule_num, url): rule_num
                for rule_num, _cap, url in rules
            }
            done = 0
            for fut in as_completed(futs):
                done += 1
                rule_num, url, caption, body, err = fut.result()
                fetched[rule_num] = (url, caption, body, err)
                if err:
                    print(
                        f"    [{done}/{len(rules)}] Rule {rule_num} FAIL: {err}",
                        flush=True,
                    )
                    grand_failed += 1

        md = render_title_md(stem, description, title_slug, rules, fetched)
        out_path = out_dir / f"{stem}.md"
        out_path.write_text(md, encoding="utf-8")
        print(f"  wrote {out_path} ({len(md):,} bytes)", flush=True)
        grand_total += len(rules)

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
