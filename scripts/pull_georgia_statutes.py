#!/usr/bin/env python3
"""Pull a curated, topic-grouped set of Official Code of Georgia Annotated
(O.C.G.A.) sections from open mirrors and convert each section to Markdown.

Output (default):
    plugins/ga-court-docs/skills/ga-law-references/references/ga-statutes-debt/

One Markdown file per TOPIC GROUP (e.g. `title-9-ch-11-civil-practice-act.md`,
`title-9-ch-3-limitations.md`), each containing the fetched text of the curated
sections in that group under `## O.C.G.A. § T-C-S` headings. The topic->section
map is read from the corpus's own `_manifest.json`, so adding a section there
is enough to widen the pull.

> **Slug note:** the output directory keeps the legacy `-debt` suffix for path
> stability (other skills cite into `references/ga-statutes-debt/`), but the
> scope is FULL CIVIL + FAMILY practice, not just debt collection.

## Source

The OFFICIAL O.C.G.A. text (LexisNexis, published for the State of Georgia) is
**paywalled and copyrighted** — it is NOT a target here. The corpus is built
from open mirrors, in priority order:

1. **FindLaw** — `https://codes.findlaw.com/ga/...` — primary open source;
   current and scrapeable. Section URLs look like:
       https://codes.findlaw.com/ga/title-9-civil-practice/ga-code-sect-9-11-56/
   FindLaw serves server-rendered HTML with the section text in the body.
2. **Justia** — `https://law.justia.com/codes/georgia/...` — corroborating
   mirror, but Justia **403s automated fetch**, so it is handled gracefully
   (treated as a failed fetch, never aborting the run) and is really a
   manual/fallback source.
3. **ga.elaws.us** — `https://ga.elaws.us/ocga/<t-c-s>` — last resort; its
   text can lag (a 2013-era snapshot), so it is tried only after FindLaw and
   Justia both fail.

Each section is fetched from the first source that returns usable text. The
fetched HTML is reduced to clean paragraph-broken Markdown.

## Curation philosophy

This is a BOUNDED, representative corpus — the key sections a Georgia
civil-practice / consumer / family-law drafter reaches for — not an
enumeration of the entire Georgia code.

## Behavior on failure / regression protection

- An individual section that fails to fetch from every mirror is recorded
  inline as a `_(could not retrieve ...)_` note rather than aborting the run.
- A topic file in which EVERY section fails is written as a well-formed
  pointer stub carrying the canonical per-section mirror URLs.
- A `_file_is_stub` guard prevents a failed/offline run from clobbering
  committed verbatim content: a non-stub file is left untouched unless
  `--force` is passed.

## Usage

    python3 scripts/pull_georgia_statutes.py
    python3 scripts/pull_georgia_statutes.py --only title-9-ch-11-civil-practice-act
    python3 scripts/pull_georgia_statutes.py --stubs-only
    python3 scripts/pull_georgia_statutes.py --force

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

DEFAULT_OUT = (
    "plugins/ga-court-docs/skills/ga-law-references/references/ga-statutes-debt"
)

STUB_MARKER = "<!-- ga-statutes-debt: pointer-stub -->"
VERBATIM_MARKER = "<!-- ga-statutes-debt: verbatim -->"

# Human-facing canonical viewer (what to cite / open in a browser).
JUSTIA = "https://law.justia.com/codes/georgia"


def repo_root() -> Path:
    here = Path(__file__).resolve().parent.parent
    if not (here / "scripts" / "lint-skills.py").exists():
        print("ERROR: cannot locate repo root", file=sys.stderr)
        sys.exit(1)
    return here


def split_section(section: str) -> tuple[str, str, str]:
    """Split an O.C.G.A. section number like '9-11-56' or '24-8-803' into
    (title, chapter, rest). Georgia section numbers are TITLE-CHAPTER-SECTION;
    a few carry a trailing letter or dotted part (e.g. '9-11-4.1',
    '15-3-3.1') which stays in the 'rest' component."""
    parts = section.split("-", 2)
    if len(parts) < 3:
        # Defensive: pad so callers can always unpack three values.
        parts += [""] * (3 - len(parts))
    return parts[0], parts[1], parts[2]


def findlaw_url(section: str, title_slug: str) -> str:
    """codes.findlaw.com per-section URL. `title_slug` is the FindLaw title
    path component (e.g. 'title-9-civil-practice') carried by the topic."""
    return (
        f"https://codes.findlaw.com/ga/{title_slug}/ga-code-sect-{section}/"
    )


def justia_url(section: str) -> str:
    """A stable Justia landing for the section's title (year-agnostic, points
    at the title index — good enough as a citable pointer in stubs)."""
    title, _chap, _rest = split_section(section)
    return f"{JUSTIA}/title-{title}/"


def elaws_url(section: str) -> str:
    return f"https://ga.elaws.us/ocga/{section}"


def _fetch(url: str, timeout: int = 45) -> str | None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", "replace")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
        return None


def _tags_to_text(fragment: str) -> str:
    """Convert a slice of statute HTML to clean, paragraph-broken text."""
    s = fragment
    # Drop scripts/styles wholesale.
    s = re.sub(r"(?is)<script\b.*?</script>", " ", s)
    s = re.sub(r"(?is)<style\b.*?</style>", " ", s)
    # Turn closing block elements into newlines.
    s = re.sub(r"(?i)</p\s*>", "\n", s)
    s = re.sub(r"(?i)<br\s*/?>", "\n", s)
    s = re.sub(r"(?i)</div\s*>", "\n", s)
    s = re.sub(r"(?i)</li\s*>", "\n", s)
    # Strip every remaining tag.
    s = re.sub(r"(?s)<[^>]+>", "", s)
    s = html.unescape(s)
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


# FindLaw wraps the section body in a content container; the markup has shifted
# over redesigns, so we try a few container patterns and fall back to the
# whole <body>. We then strip obvious chrome (nav, "Read this complete...",
# cookie/marketing boilerplate) heuristically.
_FINDLAW_BODY_RE = re.compile(
    r'(?is)<div[^>]*class="[^"]*(?:codes-text|primary-content|content-block)[^"]*"[^>]*>(.*?)</div>\s*</div>'
)
_BODY_RE = re.compile(r"(?is)<body\b[^>]*>(.*?)</body>")


def _extract_section_text(raw: str) -> str | None:
    """Pull readable section text out of a fetched HTML page. Returns None if
    nothing substantive is found."""
    m = _FINDLAW_BODY_RE.search(raw)
    chunk = m.group(1) if m else None
    if not chunk:
        m = _BODY_RE.search(raw)
        chunk = m.group(1) if m else raw
    text = _tags_to_text(chunk)
    if not text:
        return None
    # Drop common chrome lines that mirrors prepend/append.
    drop_substr = (
        "read this complete",
        "findlaw codes",
        "cookie",
        "advertisement",
        "newsletter",
        "subscribe",
        "javascript",
        "all rights reserved",
    )
    kept = [
        ln
        for ln in text.split("\n")
        if not any(d in ln.lower() for d in drop_substr)
    ]
    text = "\n".join(kept).strip()
    # Require some real heft so a chrome-only / interstitial page is treated as
    # a miss (and the next mirror is tried).
    if len(text) < 60:
        return None
    return text


def fetch_section(section: str, title_slug: str, stubs_only: bool) -> tuple[str, str] | None:
    """Try the mirrors in priority order. Return (source_url, body) for the
    first that yields usable text, else None."""
    if stubs_only:
        return None
    candidates = [
        findlaw_url(section, title_slug),
        justia_url(section),
        elaws_url(section),
    ]
    for url in candidates:
        raw = _fetch(url)
        if not raw:
            continue
        body = _extract_section_text(raw)
        if body:
            return url, body
    return None


def render_topic(topic: dict, results: dict[str, tuple[str, str] | None]) -> str:
    """results: {section: (source_url, body) | None}."""
    title = topic.get("title", topic["file"])
    citelabel = topic.get("cite", "O.C.G.A.")
    lines = [f"# {title} — {citelabel}", ""]
    lines.append(
        "> **NOT LEGAL ADVICE.** Snapshot of Official Code of Georgia "
        "Annotated (O.C.G.A.) section text from open mirrors "
        "(codes.findlaw.com / law.justia.com / ga.elaws.us). The official "
        "annotated O.C.G.A. (LexisNexis) controls and is paywalled; verify "
        "current section text and check for later amendments before relying "
        "on any figure or wording."
    )
    lines.append("")
    any_text = False
    for sec in topic["sections"]:
        sec = sec.replace("§", "").strip()
        heading = f"## O.C.G.A. § {sec}"
        ctitle = topic.get("titles", {}).get(sec)
        if ctitle:
            heading += f". {ctitle}"
        lines.append(heading)
        lines.append("")
        got = results.get(sec)
        if got:
            any_text = True
            src, body = got
            lines.append(f"Source: {src}")
            lines.append("")
            lines.append(body)
        else:
            lines.append(f"Source: {findlaw_url(sec, topic['findlaw_title_slug'])}")
            lines.append("")
            lines.append(
                f"_(could not retrieve § {sec} from any open mirror; "
                f"consult the source URL or the official O.C.G.A.)_"
            )
        lines.append("")
    marker = VERBATIM_MARKER if any_text else STUB_MARKER
    lines.insert(1, marker)
    return "\n".join(lines).rstrip() + "\n"


def _file_is_stub(path: Path) -> bool:
    """True if the file is absent or carries the pointer-stub marker. A
    committed verbatim file (VERBATIM_MARKER) is NOT a stub and is protected
    from clobbering unless --force is passed."""
    if not path.exists():
        return True
    head = path.read_text(encoding="utf-8")[:4000]
    return STUB_MARKER in head or VERBATIM_MARKER not in head


def main() -> int:
    ap = argparse.ArgumentParser(description="Pull curated O.C.G.A. statute digests")
    ap.add_argument("--out", default=None, help="Output dir (default: ga-statutes-debt)")
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

    wrote, stubbed, skipped = 0, 0, 0
    for topic in manifest.get("topics", []):
        fname = topic["file"]
        if only and fname not in only:
            continue
        path = out_dir / fname

        if path.exists() and not _file_is_stub(path) and not args.force:
            print(f"SKIP (non-stub) {fname} — pass --force to overwrite")
            skipped += 1
            continue

        title_slug = topic["findlaw_title_slug"]
        results: dict[str, tuple[str, str] | None] = {}
        for sec in topic["sections"]:
            sec = sec.replace("§", "").strip()
            results[sec] = fetch_section(sec, title_slug, args.stubs_only)

        content = render_topic(topic, results)
        path.write_text(content, encoding="utf-8")
        if STUB_MARKER in content:
            stubbed += 1
            print(f"STUB  {fname}")
        else:
            got = sum(1 for v in results.values() if v)
            wrote += 1
            print(f"WROTE {fname} ({got}/{len(results)} sections)")

    print(f"\nDone: {wrote} fetched, {stubbed} stub, {skipped} skipped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
