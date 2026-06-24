#!/usr/bin/env python3
"""Pull a curated, topic-grouped set of Texas statute sections from the
official Texas Constitution and Statutes service and convert each section
to Markdown.

Output (default):
    plugins/tx-court-docs/skills/tx-law-references/references/tx-statutes-debt/

One Markdown file per TOPIC GROUP (e.g. `CPRC-limitations.md`,
`finance-code-debt-collection.md`), each containing the fetched text of
the curated sections in that group under `## Tex. <Code> § N.N` headings.
The topic->section map is read from the corpus's own `_manifest.json`, so
adding a section there is enough to widen the pull.

## Source

statutes.capitol.texas.gov is an Angular single-page app whose
`/Docs/<CODE>/htm/<CODE>.<CHAPTER>.htm` URL serves only the SPA shell.
The verbatim per-CHAPTER HTML actually lives on the legislature's file
server:

    https://tcss.legis.texas.gov/resources/<CODE>/htm/<CODE>.<CHAPTER>.htm

(the same path the SPA's GetStatute API resolves to). That file server
returns static, server-rendered HTML with one bold catchline anchor per
section:

    <a ... href="...#16.004" ...>Sec. 16.004.  FOUR-YEAR LIMITATIONS
    PERIOD.</a>  (a) ... <p ...>...history...</p>

The puller fetches each unique <CODE>.<CHAPTER> page ONCE (cache), slices
the HTML between consecutive section catchline anchors, strips tags, and
writes verbatim Markdown for each requested section.

Code abbreviations used in the manifest's `code` field:
    CP = Civil Practice & Remedies   FI = Finance
    BC = Business & Commerce         PR = Property
    FA = Family                      GV = Government

## Curation philosophy

This is a BOUNDED, representative corpus -- the key sections a Texas
civil-practice / consumer-debt / family-law drafter reaches for -- not an
enumeration of the entire Texas statutes.

## Behavior on failure / regression protection

- An individual section that fails to fetch/slice is recorded inline as a
  `_(could not retrieve ...)_` note rather than aborting the run.
- A topic file in which EVERY section fails is written as a well-formed
  pointer stub carrying the canonical per-chapter URLs.
- A `_file_is_stub` guard prevents a failed/offline run from clobbering
  committed verbatim content: a non-stub file is left untouched unless
  `--force` is passed.

## Usage

    python3 scripts/pull_texas_statutes.py
    python3 scripts/pull_texas_statutes.py --only CPRC-limitations
    python3 scripts/pull_texas_statutes.py --stubs-only
    python3 scripts/pull_texas_statutes.py --force

## Dependencies

Python 3.10+ stdlib only.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
RESOURCE_BASE = "https://tcss.legis.texas.gov/resources"
# Human-facing canonical viewer (what to cite / open in a browser):
VIEWER = "https://statutes.capitol.texas.gov/Docs"

DEFAULT_OUT = (
    "plugins/tx-court-docs/skills/tx-law-references/references/tx-statutes-debt"
)

STUB_MARKER = "<!-- tx-statutes-debt: pointer-stub -->"

# Pretty code label for the `## Tex. <Code> § ...` heading + the file's intro.
CODE_LABEL = {
    "CP": "Civ. Prac. & Rem. Code",
    "FI": "Fin. Code",
    "BC": "Bus. & Com. Code",
    "PR": "Prop. Code",
    "FA": "Fam. Code",
    "GV": "Gov't Code",
}


def repo_root() -> Path:
    here = Path(__file__).resolve().parent.parent
    if not (here / "scripts" / "lint-skills.py").exists():
        print("ERROR: cannot locate repo root", file=sys.stderr)
        sys.exit(1)
    return here


def chapter_url(code: str, chapter: str) -> str:
    return f"{RESOURCE_BASE}/{code}/htm/{code}.{chapter}.htm"


def viewer_url(code: str, chapter: str) -> str:
    return f"{VIEWER}/{code}/htm/{code}.{chapter}.htm"


def section_chapter(section: str) -> str:
    """A Texas section number like '16.004' or '392.101' or '153.131' lives in
    the chapter that is the integer part before the first dot ('16', '392',
    '153')."""
    return section.split(".")[0]


def fetch_chapter_html(code: str, chapter: str, timeout: int = 45) -> str | None:
    url = chapter_url(code, chapter)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", "replace")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
        return None


def _tags_to_text(fragment: str) -> str:
    """Convert a slice of statute HTML to clean, paragraph-broken text."""
    # Drop the inter-section navigation anchors that wrap cross-references;
    # keep their visible text only.
    s = fragment
    # Turn closing block elements into newlines.
    s = re.sub(r"(?i)</p\s*>", "\n", s)
    s = re.sub(r"(?i)<br\s*/?>", "\n", s)
    s = re.sub(r"(?i)</div\s*>", "\n", s)
    # Strip every remaining tag.
    s = re.sub(r"(?s)<[^>]+>", "", s)
    s = html.unescape(s)
    # Normalize whitespace: collapse runs of spaces/tabs, trim each line,
    # squeeze blank-line runs.
    s = s.replace("\xa0", " ")
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in s.split("\n")]
    out: list[str] = []
    blank = False
    for ln in lines:
        if ln:
            out.append(ln)
            blank = False
        else:
            if not blank and out:
                out.append("")
            blank = True
    return "\n".join(out).strip()


# Catchline anchor: <a ... href="...#16.004" ...>Sec. 16.004.  TITLE.</a>
_CATCHLINE_RE = re.compile(
    r'<a\b[^>]*href="[^"]*#([0-9]+(?:\.[0-9A-Za-z]+)*)"[^>]*>\s*'
    r'Sec\.\s*([0-9]+(?:\.[0-9A-Za-z]+)*)\.\s*(.*?)</a>',
    re.IGNORECASE | re.DOTALL,
)


def slice_sections(chapter_html: str) -> dict[str, tuple[str, str]]:
    """Return {section_number: (catchline_title, body_text)} for every
    section catchline anchor found in the chapter HTML.

    Each section body runs from the end of its catchline anchor to the start
    of the next section's catchline anchor (or end of document)."""
    anchors = list(_CATCHLINE_RE.finditer(chapter_html))
    result: dict[str, tuple[str, str]] = {}
    for i, m in enumerate(anchors):
        sec = m.group(2)
        title = re.sub(r"<[^>]+>", "", m.group(3))
        title = html.unescape(title).strip().rstrip(".")
        start = m.end()
        end = anchors[i + 1].start() if i + 1 < len(anchors) else len(chapter_html)
        body = _tags_to_text(chapter_html[start:end])
        # Drop a leading "(a)" run-on with the catchline? No -- the body
        # legitimately begins mid-sentence after the catchline; keep verbatim.
        result[sec] = (title, body)
    return result


def render_topic(
    title: str,
    code: str,
    entries: list[tuple[str, str, str | None, str | None]],
) -> str:
    """entries: (section, viewer_url, catchline_title_or_None, body_or_None)."""
    label = CODE_LABEL.get(code, code)
    lines = [f"# {title} — Tex. {label}", ""]
    lines.append(
        "> **NOT LEGAL ADVICE.** Verbatim Texas statute text fetched from the "
        "Texas Legislature's statutes file server "
        "(tcss.legis.texas.gov / statutes.capitol.texas.gov). The Texas "
        "statutes are amended each regular and special legislative session; "
        "verify currency and check for later amendments against the official "
        "source before relying on any figure or wording."
    )
    lines.append("")
    any_text = False
    for sec, url, ctitle, body in entries:
        heading = f"## Tex. {label} § {sec}"
        if ctitle:
            heading += f". {ctitle}"
        lines.append(heading)
        lines.append("")
        lines.append(f"Source: {url}")
        lines.append("")
        if body:
            any_text = True
            lines.append(body)
        else:
            lines.append(
                f"_(could not retrieve § {sec}; consult the source URL.)_"
            )
        lines.append("")
    if not any_text:
        lines.insert(1, STUB_MARKER)
    return "\n".join(lines).rstrip() + "\n"


def file_is_stub(path: Path) -> bool:
    if not path.exists():
        return True
    return STUB_MARKER in path.read_text(encoding="utf-8")[:4000]


def main() -> int:
    ap = argparse.ArgumentParser(description="Pull curated Texas statute digests")
    ap.add_argument("--out", default=None, help="Output dir (default: tx-statutes-debt)")
    ap.add_argument("--only", nargs="*", help="Limit to these topic files (stem or filename)")
    ap.add_argument("--workers", type=int, default=4, help="(reserved; fetch is sequential + cached)")
    ap.add_argument("--stubs-only", action="store_true", help="Write pointer stubs; skip network")
    ap.add_argument("--force", action="store_true", help="Overwrite non-stub files too")
    args = ap.parse_args()

    root = repo_root()
    out_dir = Path(args.out) if args.out else (root / DEFAULT_OUT)
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = out_dir / "_manifest.json"
    if not manifest_path.exists():
        print(f"ERROR: manifest not found at {manifest_path}", file=sys.stderr)
        return 1
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    only = set()
    for o in args.only or []:
        only.add(o if o.endswith(".md") else f"{o}.md")

    # Cache chapter HTML + sliced sections by (code, chapter).
    chapter_cache: dict[tuple[str, str], dict[str, tuple[str, str]] | None] = {}

    def get_chapter(code: str, chapter: str) -> dict[str, tuple[str, str]] | None:
        key = (code, chapter)
        if key not in chapter_cache:
            if args.stubs_only:
                chapter_cache[key] = None
            else:
                raw = fetch_chapter_html(code, chapter)
                chapter_cache[key] = slice_sections(raw) if raw else None
        return chapter_cache[key]

    wrote, stubbed, skipped = 0, 0, 0
    for topic in manifest.get("topics", []):
        fname = topic["file"]
        if only and fname not in only:
            continue
        path = out_dir / fname

        if path.exists() and not file_is_stub(path) and not args.force:
            print(f"SKIP (non-stub) {fname} — pass --force to overwrite")
            skipped += 1
            continue

        entries: list[tuple[str, str, str | None, str | None]] = []
        # Each section entry is a bare section number; the topic carries its
        # `code` once (a topic file is single-code in this corpus).
        code = topic["code"]
        for sec in topic["sections"]:
            sec = sec.replace("§", "").strip()
            chap = section_chapter(sec)
            url = viewer_url(code, chap)
            sliced = get_chapter(code, chap)
            if sliced and sec in sliced:
                ctitle, body = sliced[sec]
                entries.append((sec, url, ctitle, body))
            else:
                entries.append((sec, url, None, None))

        content = render_topic(topic.get("title", fname), code, entries)
        path.write_text(content, encoding="utf-8")
        if STUB_MARKER in content:
            stubbed += 1
            print(f"STUB  {fname}")
        else:
            got = sum(1 for e in entries if e[3])
            wrote += 1
            print(f"WROTE {fname} ({got}/{len(entries)} sections)")

    print(f"\nDone: {wrote} fetched, {stubbed} stub, {skipped} skipped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
