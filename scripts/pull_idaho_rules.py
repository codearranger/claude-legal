#!/usr/bin/env python3
"""Pull verbatim Idaho court-rule text from the Idaho Supreme Court rules
site (isc.idaho.gov) and write one Markdown file per rule SET.

Output (default):
    plugins/id-court-docs/skills/id-law-references/references/court-rules/

The set→file→slug→rule-list map is read from the corpus's own
`_manifest.json`.

## Source

The Idaho Supreme Court publishes a per-rule **print view** that serves
clean, static HTML (the `-new` landing pages are JavaScript-rendered and
are not usable for verbatim extraction). The print URL is:

    https://isc.idaho.gov/rules-procedure/print/<slug>/<rule>

where `<slug>` is the rule-set slug (`ircp`, `ire`, `irfl`, `iar`) and
`<rule>` is the rule number (e.g. `2.2`, `803`, `120`, `14`). Each print
page begins with the set name and the "Rule N. Title" heading, followed
by the verbatim rule body and the adoption/amendment history.

## Curation philosophy

This is a BOUNDED corpus — the rules an Idaho civil-practice /
family-law drafter actually cites — not an enumeration of every rule in
every set. Widen a set by adding rule numbers to its `rules` list in the
manifest.

## Behavior on failure / regression protection

- A rule whose print page is missing or empty is **skipped** (not
  emitted as a gap), so a generous rule list yields clean output.
- A set in which EVERY listed rule fails is written as a well-formed
  pointer stub carrying the canonical URL.
- A `_file_is_stub` guard prevents a failed/offline run from clobbering
  committed verbatim content: a non-stub file is left untouched unless
  `--force` is passed.

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
PRINT_BASE = "https://isc.idaho.gov/rules-procedure/print"
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


def _raw_text(url: str, timeout: int = 30) -> str | None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", "replace")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
        return None
    p = _TextExtractor()
    p.feed(raw)
    return "\n".join(p.chunks)


def fetch_rule(slug: str, rule: str, set_name: str) -> tuple[str, str] | None:
    """Return (heading, body) for a single rule's print page, or None."""
    url = f"{PRINT_BASE}/{slug}/{rule}"
    text = _raw_text(url)
    if not text:
        return None
    lines = text.split("\n")
    if len(lines) < 3:
        return None
    # lines[0] = set name; lines[1] = "Rule N. Title"; lines[2..] = body,
    # which may begin with a redundant "<set name> Rule N. Title." line.
    heading = lines[1].strip()
    if not heading.lower().startswith("rule"):
        # Unexpected shell / 404 page.
        return None
    rest = lines[2:]
    if rest and rest[0].strip().startswith(set_name):
        rest = rest[1:]
    body = "\n".join(rest).strip()
    if len(body) < 60:
        return None
    return heading, body


def render_set(target: dict, rules: list[tuple[str, str]]) -> str:
    name = target.get("name", target.get("set", "Idaho rule set"))
    code = target.get("set", "")
    slug = target.get("slug", "")
    url = target.get("url", "")
    lines = [f"# {name} ({code})", ""]
    lines.append(
        "> **NOT LEGAL ADVICE.** Verbatim rule text fetched from the Idaho "
        "Supreme Court rules site. Verify against the current official text "
        "before relying on any rule."
    )
    lines.append("")
    lines.append(f"Source: {url}")
    lines.append(
        f"Per-rule print pattern: `{PRINT_BASE}/{slug}/<rule>`"
    )
    lines.append("")
    lines.append("---")
    lines.append("")
    for heading, body in rules:
        lines.append(f"## {heading}")
        lines.append("")
        lines.append(body)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_stub(target: dict) -> str:
    name = target.get("name", target.get("set", "Idaho rule set"))
    url = target.get("url", "https://isc.idaho.gov/rules-procedure")
    code = target.get("set", "")
    slug = target.get("slug", "")
    return (
        f"# {name} ({code})\n\n"
        f"{STUB_MARKER}\n\n"
        f"> **NOT LEGAL ADVICE.** Pointer stub. The verbatim text of the "
        f"{name} is published by the Idaho Supreme Court and is populated "
        f"into this file by `scripts/pull_idaho_rules.py`. Until a verbatim "
        f"pull lands, consult the canonical source.\n\n"
        f"## Canonical source\n\n"
        f"- {url}\n"
        f"- Per-rule print view: `{PRINT_BASE}/{slug}/<rule>`\n"
    )


def file_is_stub(path: Path) -> bool:
    if not path.exists():
        return True
    return STUB_MARKER in path.read_text(encoding="utf-8")[:4000]


def main() -> int:
    ap = argparse.ArgumentParser(description="Pull verbatim Idaho court rules")
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

        slug = target.get("slug")
        rule_nums = target.get("rules", [])
        fetched: list[tuple[str, str]] = []
        if not args.stubs_only and slug and rule_nums:
            set_name = target.get("name", "")
            for rn in rule_nums:
                got = fetch_rule(slug, str(rn), set_name)
                if got:
                    fetched.append(got)

        if fetched:
            path.write_text(render_set(target, fetched), encoding="utf-8")
            wrote += 1
            print(f"WROTE {fname} ({len(fetched)}/{len(rule_nums)} rules)")
        else:
            path.write_text(render_stub(target), encoding="utf-8")
            stubbed += 1
            print(f"STUB  {fname}")

    print(f"\nDone: {wrote} fetched, {stubbed} stub, {skipped} skipped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
