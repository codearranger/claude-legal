#!/usr/bin/env python3
"""Pull a curated, topic-grouped set of Idaho Code sections from the
official Idaho Legislature website and convert each section to Markdown.

Output (default):
    plugins/id-court-docs/skills/id-law-references/references/id-statutes-debt/

One Markdown file per TOPIC GROUP (e.g. `Title5-limitations.md`,
`Title11-exemptions-garnishment.md`), each containing the fetched text of
the curated sections in that group under `## Idaho Code § NN-NNN`
headings. The topic→section map is read from the corpus's own
`_manifest.json`, so adding a section there is enough to widen the pull.

## Source

The Idaho Legislature publishes the Idaho Code section by section as
server-rendered HTML at:

    https://legislature.idaho.gov/statutesrules/idstat/title<T>/t<T>ch<C>/sect<SECTION>/

where `<T>` is the title, `<C>` is the chapter, and `<SECTION>` is the
full section label (e.g. `5-216`). For most sections the chapter is the
hundreds component of the post-hyphen sequence — § 5-216 → Title 5,
Chapter 2 → `title5/t5ch2/sect5-216/`; § 11-605 → `title11/t11ch6/
sect11-605/`. Sections with a second hyphen carry the chapter in the
middle component — § 32-11-101 → Title 32, Chapter 11 → `title32/
t32ch11/sect32-11-101/`. The pages are plain HTML (no bot-fight gate), so
stdlib urllib with a browser User-Agent retrieves them.

## Curation philosophy

This is a BOUNDED, representative corpus — the key sections an Idaho
civil-practice / consumer-debt / family-law drafter reaches for — not an
enumeration of the entire Idaho Code.

## Behavior on failure / regression protection

- An individual section that fails to fetch is recorded inline as a
  `_(could not retrieve ...)_` note rather than aborting the run.
- A topic file in which EVERY section fails is written as a well-formed
  pointer stub carrying the canonical per-section URLs.
- The committed files ship as hand-authored CURATED DIGESTS. By default
  this puller will NOT overwrite an existing file that is not a stub —
  pass `--overwrite-curated` to replace curated digests with fetched
  text. This mirrors the curated-file guard used by the other state
  statute pullers and keeps an offline run from clobbering committed
  content.

## Usage

    python3 scripts/pull_idaho_statutes.py
    python3 scripts/pull_idaho_statutes.py --only Title5-limitations
    python3 scripts/pull_idaho_statutes.py --stubs-only
    python3 scripts/pull_idaho_statutes.py --overwrite-curated

## Dependencies

Python 3.10+ stdlib only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
BASE = "https://legislature.idaho.gov/statutesrules/idstat"

DEFAULT_OUT = (
    "plugins/id-court-docs/skills/id-law-references/references/id-statutes-debt"
)

STUB_MARKER = "<!-- id-statutes-debt: pointer-stub -->"
CURATED_MARKER = "verify current figure"  # appears in the committed digests


def repo_root() -> Path:
    here = Path(__file__).resolve().parent.parent
    if not (here / "scripts" / "lint-skills.py").exists():
        print("ERROR: cannot locate repo root", file=sys.stderr)
        sys.exit(1)
    return here


def section_to_url(section: str) -> str | None:
    """Map an Idaho Code section label like '5-216' or '32-11-101' to its
    legislature.idaho.gov URL. Returns None for non-section entries (e.g.
    a whole-chapter pointer such as 'Title 28, ch. 9')."""
    s = section.replace("I.C.", "").replace("§", "").strip()
    parts = s.split("-")
    if len(parts) == 2:
        title, seq = parts
        if not title.isdigit():
            return None
        seq_num = re.match(r"(\d+)", seq)
        if not seq_num:
            return None
        chapter = int(seq_num.group(1)) // 100
        if chapter == 0:
            chapter = 1
        return f"{BASE}/title{title}/t{title}ch{chapter}/sect{title}-{seq}/"
    if len(parts) == 3:
        title, chapter, _tail = parts
        if not (title.isdigit() and chapter.isdigit()):
            return None
        return f"{BASE}/title{title}/t{title}ch{chapter}/sect{s}/"
    return None


class _TextExtractor(HTMLParser):
    """Collect visible text, skipping script/style/nav chrome."""

    SKIP = {"script", "style", "nav", "header", "footer", "head"}

    def __init__(self) -> None:
        super().__init__()
        self._skip_depth = 0
        self.chunks: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self._skip_depth += 1

    def handle_endtag(self, tag):
        if tag in self.SKIP and self._skip_depth > 0:
            self._skip_depth -= 1

    def handle_data(self, data):
        if self._skip_depth == 0:
            text = data.strip()
            if text:
                self.chunks.append(text)


def fetch_section(url: str, timeout: int = 30) -> str | None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", "replace")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
        return None
    parser = _TextExtractor()
    parser.feed(raw)
    text = "\n".join(parser.chunks)
    # Heuristic: the statute body should mention the section number region.
    if len(text) < 40:
        return None
    return text


def render_topic(title: str, entries: list[tuple[str, str | None, str | None]]) -> str:
    """entries: list of (section_label, url, fetched_text_or_None)."""
    lines = [f"# {title} — Idaho Code", ""]
    lines.append(
        "> **NOT LEGAL ADVICE.** Fetched/curated digest of Idaho Code "
        "sections. Verify against the current official text at "
        "legislature.idaho.gov before relying on any figure or wording."
    )
    lines.append("")
    any_text = False
    for label, url, text in entries:
        lines.append(f"## Idaho Code § {label}")
        lines.append("")
        if url:
            lines.append(f"Source: {url}")
            lines.append("")
        if text:
            any_text = True
            lines.append(text)
        else:
            lines.append(f"_(could not retrieve § {label}; consult the source URL.)_")
        lines.append("")
    if not any_text:
        # Whole file is a stub.
        lines.insert(1, STUB_MARKER)
    return "\n".join(lines).rstrip() + "\n"


def file_is_stub(path: Path) -> bool:
    if not path.exists():
        return True
    head = path.read_text(encoding="utf-8")[:4000]
    return STUB_MARKER in head


def file_is_curated(path: Path) -> bool:
    if not path.exists():
        return False
    body = path.read_text(encoding="utf-8")
    return STUB_MARKER not in body and CURATED_MARKER in body


def main() -> int:
    ap = argparse.ArgumentParser(description="Pull curated Idaho Code digests")
    ap.add_argument("--out", default=None, help="Output dir (default: id-statutes-debt)")
    ap.add_argument("--only", nargs="*", help="Limit to these topic files (stem or filename)")
    ap.add_argument("--workers", type=int, default=4, help="(reserved; fetch is sequential)")
    ap.add_argument("--stubs-only", action="store_true", help="Write pointer stubs; skip network")
    ap.add_argument(
        "--overwrite-curated",
        action="store_true",
        help="Replace committed curated digests with fetched text",
    )
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

    wrote, skipped, stubbed = 0, 0, 0
    for topic in manifest.get("topics", []):
        fname = topic["file"]
        if only and fname not in only:
            continue
        path = out_dir / fname

        if not args.overwrite_curated and file_is_curated(path):
            print(f"SKIP (curated) {fname} — pass --overwrite-curated to replace")
            skipped += 1
            continue

        entries: list[tuple[str, str | None, str | None]] = []
        for label_raw in topic["sections"]:
            label = label_raw.replace("I.C.", "").replace("§", "").strip()
            url = section_to_url(label_raw)
            if args.stubs_only or url is None:
                entries.append((label, url, None))
            else:
                text = fetch_section(url)
                entries.append((label, url, text))

        content = render_topic(topic.get("title", fname), entries)
        path.write_text(content, encoding="utf-8")
        if STUB_MARKER in content:
            stubbed += 1
            print(f"STUB  {fname}")
        else:
            wrote += 1
            print(f"WROTE {fname}")

    print(f"\nDone: {wrote} fetched, {stubbed} stub, {skipped} skipped (curated).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
