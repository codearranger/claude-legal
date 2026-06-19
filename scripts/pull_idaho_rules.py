#!/usr/bin/env python3
"""Pull (or stub) the Idaho court-rules corpus from the Idaho Supreme
Court rules site.

Output (default):
    plugins/id-court-docs/skills/id-law-references/references/court-rules/

One Markdown file per rule SET (I.R.C.P., I.R.E., I.R.F.L.P., I.A.R.).
The set→file→URL map is read from the corpus's own `_manifest.json`.

## Source and posture

The Idaho Supreme Court publishes its rules at isc.idaho.gov. The rule
landing pages (e.g. https://isc.idaho.gov/rules-procedure/ircp) and many
per-rule views are JavaScript-rendered, so a plain HTTP fetch does not
reliably yield clean verbatim rule text. There is a per-rule "print"
pattern — https://isc.idaho.gov/rules-procedure/print/ircp/<n> — that
serves more static markup when reachable.

Because verbatim extraction is not reliable without a headless browser,
this corpus ships as **well-formed pointer stubs** (header + canonical
URL + scope note). This puller:

- writes/refreshes a pointer stub for each target in the manifest, and
- if a rule set's print-pattern fetch succeeds and yields substantial
  text, embeds it (best-effort).

## Regression protection

A `_file_is_stub` guard prevents a failed or JS-blocked run from
clobbering any verbatim content a later mechanism may have committed: a
non-stub file is left untouched unless `--force` is passed.

## Usage

    python3 scripts/pull_idaho_rules.py
    python3 scripts/pull_idaho_rules.py --only IRCP-civil-procedure.md
    python3 scripts/pull_idaho_rules.py --stubs-only
    python3 scripts/pull_idaho_rules.py --force

## Dependencies

Python 3.10+ stdlib only.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
DEFAULT_OUT = (
    "plugins/id-court-docs/skills/id-law-references/references/court-rules"
)
STUB_MARKER = "<!-- id-court-rules: pointer-stub -->"


def repo_root() -> Path:
    here = Path(__file__).resolve().parent.parent
    if not (here / "scripts" / "lint-skills.py").exists():
        print("ERROR: cannot locate repo root", file=sys.stderr)
        sys.exit(1)
    return here


class _TextExtractor(HTMLParser):
    SKIP = {"script", "style", "nav", "header", "footer", "head"}

    def __init__(self) -> None:
        super().__init__()
        self._skip = 0
        self.chunks: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in self.SKIP and self._skip > 0:
            self._skip -= 1

    def handle_data(self, data):
        if self._skip == 0:
            t = data.strip()
            if t:
                self.chunks.append(t)


def fetch_text(url: str, timeout: int = 30) -> str | None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", "replace")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
        return None
    p = _TextExtractor()
    p.feed(raw)
    text = "\n".join(p.chunks)
    # JS-rendered shells return little real content; require substance.
    if len(text) < 600:
        return None
    return text


def render_stub(target: dict) -> str:
    name = target.get("name", target.get("set", "Idaho rule set"))
    url = target.get("url", "https://isc.idaho.gov/rules-procedure")
    code = target.get("set", "")
    return (
        f"# {name} ({code})\n\n"
        f"{STUB_MARKER}\n\n"
        f"> **NOT LEGAL ADVICE.** Pointer stub. The verbatim text of the "
        f"{name} is published by the Idaho Supreme Court and is populated "
        f"into this file by `scripts/pull_idaho_rules.py`. Until a verbatim "
        f"pull lands, consult the canonical source.\n\n"
        f"## Canonical source\n\n"
        f"- {url}\n"
        f"- Per-rule print view: `https://isc.idaho.gov/rules-procedure/"
        f"print/{code.lower().replace('.', '').replace(' ', '')}/<n>`\n\n"
        f"## Scope\n\n"
        f"This corpus holds the verbatim {name} most relevant to drafting "
        f"and filing in Idaho's District Courts and their Magistrate "
        f"Divisions. Cite specific rules from the canonical source until "
        f"the verbatim text is pulled.\n"
    )


def render_verbatim(target: dict, text: str) -> str:
    name = target.get("name", target.get("set", "Idaho rule set"))
    url = target.get("url", "")
    code = target.get("set", "")
    return (
        f"# {name} ({code})\n\n"
        f"> **NOT LEGAL ADVICE.** Fetched from the Idaho Supreme Court "
        f"rules site; verify against the current official text before "
        f"relying on any specific rule.\n\n"
        f"Source: {url}\n\n"
        f"---\n\n{text}\n"
    )


def file_is_stub(path: Path) -> bool:
    if not path.exists():
        return True
    return STUB_MARKER in path.read_text(encoding="utf-8")[:4000]


def main() -> int:
    ap = argparse.ArgumentParser(description="Pull/stub the Idaho court-rules corpus")
    ap.add_argument("--out", default=None, help="Output dir (default: court-rules)")
    ap.add_argument("--only", nargs="*", help="Limit to these files (stem or filename)")
    ap.add_argument("--workers", type=int, default=2, help="(reserved; fetch is sequential)")
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
    for target in manifest.get("targets", []):
        fname = target.get("file")
        if not fname:  # e.g. I.R.E.F.S. has no dedicated file
            continue
        if only and fname not in only:
            continue
        path = out_dir / fname

        if path.exists() and not file_is_stub(path) and not args.force:
            print(f"SKIP (non-stub) {fname} — pass --force to overwrite")
            skipped += 1
            continue

        text = None
        if not args.stubs_only:
            text = fetch_text(target.get("url", ""))

        if text:
            path.write_text(render_verbatim(target, text), encoding="utf-8")
            wrote += 1
            print(f"WROTE {fname}")
        else:
            path.write_text(render_stub(target), encoding="utf-8")
            stubbed += 1
            print(f"STUB  {fname}")

    print(f"\nDone: {wrote} fetched, {stubbed} stub, {skipped} skipped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
