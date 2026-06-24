#!/usr/bin/env python3
"""Pull verbatim Texas court-rule text from the consolidated rule PDFs the
Office of Court Administration publishes at txcourts.gov, and write one
Markdown file per rule SET.

Output (default):
    plugins/tx-court-docs/skills/tx-law-references/references/court-rules/

The set->file->pdf->rule-list map is read from the corpus's own
`_manifest.json`.

## Source

The Supreme Court of Texas promulgates the Texas Rules of Civil Procedure
(TRCP), the Texas Rules of Evidence (TRE), and the Texas Rules of
Appellate Procedure (TRAP). The Office of Court Administration publishes
each as a single consolidated PDF on the "Rules & Standards" page:

    https://www.txcourts.gov/rules-forms/rules-standards/

Each set's `pdf` field in `_manifest.json` is the path under
`https://www.txcourts.gov` (the media path changes when the OCA re-issues
an amended edition, so the manifest records the current one). The puller
downloads the PDF, extracts its text with `pypdf`, locates each rule's
heading, and slices the body from one rule heading to the next.

A rule heading in these PDFs reads `RULE 169. EXPEDITED ACTIONS`; the
justice-court rules use dotted numbers (`RULE 500.3. ...`); a handful of
sub-rules appear without the `RULE` prefix (e.g. `193.7 Production of
Documents Self-Authenticating`). The puller handles all three forms and
discards the table-of-contents copies of each heading (those carry dotted
leaders / page numbers).

## Behavior on failure / regression protection

- `pypdf` is an optional dependency. If it is not importable, or a PDF
  cannot be downloaded, or no requested rule is found, the set file is
  written as a well-formed **pointer stub** carrying the canonical PDF URL
  — never fabricated text.
- A rule whose body cannot be located is skipped (not emitted as a gap).
- A `_file_is_stub` guard prevents a failed/offline run from clobbering
  committed verbatim content: a non-stub file is left untouched unless
  `--force` is passed.

## Usage

    python3 scripts/pull_texas_rules.py
    python3 scripts/pull_texas_rules.py --only TRCP-civil-procedure.md
    python3 scripts/pull_texas_rules.py --stubs-only
    python3 scripts/pull_texas_rules.py --force

Install the optional PDF dependency:

    pip3 install --break-system-packages pypdf

## Dependencies

Python 3.10+ stdlib; `pypdf` (optional — stubs are written without it).
"""

from __future__ import annotations

import argparse
import io
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
TXCOURTS = "https://www.txcourts.gov"
RULES_PAGE = "https://www.txcourts.gov/rules-forms/rules-standards/"

DEFAULT_OUT = (
    "plugins/tx-court-docs/skills/tx-law-references/references/court-rules"
)

STUB_MARKER = "<!-- tx-court-rules: pointer-stub -->"


def repo_root() -> Path:
    here = Path(__file__).resolve().parent.parent
    if not (here / "scripts" / "lint-skills.py").exists():
        print("ERROR: cannot locate repo root", file=sys.stderr)
        sys.exit(1)
    return here


def _pdf_url(pdf: str) -> str:
    if pdf.startswith("http"):
        return pdf
    return TXCOURTS + pdf


def download_pdf(pdf: str, timeout: int = 90) -> bytes | None:
    url = _pdf_url(pdf)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
        return None
    if not data.startswith(b"%PDF"):
        return None
    return data


def extract_pdf_text(data: bytes) -> str | None:
    try:
        from pypdf import PdfReader
    except Exception:
        return None
    try:
        reader = PdfReader(io.BytesIO(data))
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    except Exception:
        return None


# A real (non-TOC) rule heading. Forms seen across the three PDFs:
#   "RULE 169. EXPEDITED ACTIONS"            (TRCP — all caps prefix)
#   "RULE 500.3.  ..." / "RULE 21a. ..."     (TRCP — dotted / lettered)
#   "Rule 401.  Test for Relevant Evidence"  (TRE / TRAP — mixed case)
#   "Rule 26.1. ..."                         (TRAP — dotted)
# plus a sub-rule fallback without the prefix:
#   "193.7 Production of Documents Self-Authenticating"
_RULE_HEADING_RE = re.compile(
    r"(?im)^RULE\s+([0-9]+[A-Za-z]?(?:\.[0-9]+[A-Za-z]?)?)\.\s+(.+?)\s*$"
)
_SUBRULE_HEADING_RE = re.compile(
    r"(?m)^\s*([0-9]+\.[0-9]+[A-Za-z]?)\.?\s+([A-Z][A-Za-z].+?)\s*$"
)


def _is_toc_line(title: str, tail: str) -> bool:
    """Table-of-contents copies of a heading carry dotted leaders and/or a
    trailing page number; a bracketed '[RULE N. Repealed ...]' note is not a
    real heading either."""
    if title.lower().startswith("repealed") or title.endswith("]"):
        return True
    if re.search(r"\bRepealed\b", title) and "effective" in title.lower():
        return True
    if re.search(r"\.\s?\.\s?\.", title):
        return True
    if re.search(r"\.\s?\.\s?\.", tail[:160]):
        return True
    return False


def _all_real_headings(txt: str) -> list[tuple[str, str, int, int]]:
    """Return [(rule_number, title, start, body_start)] for every real rule
    heading, in document order, de-duplicated by position."""
    found: list[tuple[str, str, int, int]] = []
    for m in _RULE_HEADING_RE.finditer(txt):
        title = m.group(2).strip()
        tail = txt[m.end():m.end() + 200]
        if _is_toc_line(title, tail):
            continue
        found.append((m.group(1), title, m.start(), m.end()))
    for m in _SUBRULE_HEADING_RE.finditer(txt):
        title = m.group(2).strip()
        tail = txt[m.end():m.end() + 200]
        if _is_toc_line(title, tail):
            continue
        # Avoid double-counting a position already captured by the prefixed
        # pattern.
        if any(abs(m.start() - s) < 5 for _, _, s, _ in found):
            continue
        found.append((m.group(1), title, m.start(), m.end()))
    found.sort(key=lambda t: t[2])
    return found


def _clean_body(body: str) -> str:
    """Tidy extracted PDF text: collapse intra-word spacing artifacts the
    extractor leaves (e.g. "$ 250,000"), squeeze blank runs, strip trailing
    whitespace per line. Conservative — does not rewrite wording."""
    # Join hyphenated line breaks: "pen-\n alties" -> "penalties"
    body = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", body)
    lines = [re.sub(r"[ \t]+", " ", ln).rstrip() for ln in body.split("\n")]
    out: list[str] = []
    blank = False
    for ln in lines:
        s = ln.strip()
        if s:
            out.append(s)
            blank = False
        else:
            if not blank and out:
                out.append("")
            blank = True
    text = "\n".join(out).strip()
    text = re.sub(r"\$\s+(\d)", r"$\1", text)
    return text


def extract_rules(txt: str, wanted: list[str]) -> list[tuple[str, str, str]]:
    """Return [(rule_number, title, body)] for each wanted rule found.

    Most rules' bodies run from their heading to the next rule heading. But
    several Texas rules are UMBRELLA headings whose substance lives entirely
    in dotted sub-rules (e.g. RULE 510. EVICTION CASES is immediately
    followed by RULE 510.1, 510.2, ...). For such a rule the inter-heading
    slice is empty, so we instead capture the parent heading plus every
    sub-rule of that parent, up to the next heading that is NOT a descendant
    of the requested rule."""
    headings = _all_real_headings(txt)
    # All occurrence indices per rule number, in document order. A rule's
    # heading typically appears twice: once in the table of contents (where
    # the next heading immediately follows, leaving an empty body) and once
    # at the real body. We try every occurrence and keep the one whose body
    # window is substantive.
    occ: dict[str, list[int]] = {}
    for i, (num, _title, _s, _bs) in enumerate(headings):
        occ.setdefault(num, []).append(i)

    def is_descendant(child: str, parent: str) -> bool:
        return child == parent or child.startswith(parent + ".")

    def body_for(i: int, w: str) -> tuple[str, str]:
        num, title, _start, body_start = headings[i]
        # Extend the body window across any descendant sub-rule headings so
        # an umbrella rule (e.g. RULE 510. EVICTION CASES) pulls in its
        # sub-rule text verbatim.
        j = i + 1
        while j < len(headings) and is_descendant(headings[j][0], w):
            j += 1
        end = headings[j][2] if j < len(headings) else len(txt)
        return title, _clean_body(txt[body_start:end])

    out: list[tuple[str, str, str]] = []
    for w in wanted:
        best: tuple[str, str] | None = None
        for i in occ.get(w, []):
            title, body = body_for(i, w)
            if best is None or len(body) > len(best[1]):
                best = (title, body)
        if best and len(best[1]) >= 40:
            out.append((w, best[0], best[1]))
    return out


def render_set(target: dict, rules: list[tuple[str, str, str]]) -> str:
    name = target.get("name", target.get("set", "Texas rule set"))
    code = target.get("set", "")
    url = _pdf_url(target.get("pdf", ""))
    lines = [f"# {name} ({code})", ""]
    lines.append(
        "> **NOT LEGAL ADVICE.** Verbatim rule text extracted from the "
        "consolidated rule PDF the Texas Office of Court Administration "
        "publishes at txcourts.gov. Texas court rules are amended by order "
        "of the Supreme Court of Texas; verify against the current official "
        "PDF before relying on any rule."
    )
    lines.append("")
    lines.append(f"Source PDF: {url}")
    lines.append(f"Rules index: {RULES_PAGE}")
    lines.append("")
    lines.append("---")
    lines.append("")
    for num, title, body in rules:
        lines.append(f"## Rule {num}. {title}")
        lines.append("")
        lines.append(body)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_stub(target: dict, reason: str) -> str:
    name = target.get("name", target.get("set", "Texas rule set"))
    code = target.get("set", "")
    url = _pdf_url(target.get("pdf", ""))
    wanted = ", ".join(str(r) for r in target.get("rules", []))
    return (
        f"# {name} ({code})\n\n"
        f"{STUB_MARKER}\n\n"
        f"> **NOT LEGAL ADVICE.** Pointer stub — not verbatim. The verbatim "
        f"text of the {name} is published by the Supreme Court of Texas / "
        f"Office of Court Administration as a consolidated PDF. This file is "
        f"populated by `scripts/pull_texas_rules.py` (which needs the "
        f"optional `pypdf` dependency and network access to txcourts.gov). "
        f"Until a verbatim pull lands, consult the canonical source.\n\n"
        f"_Stub reason: {reason}._\n\n"
        f"## Canonical source\n\n"
        f"- Source PDF: {url}\n"
        f"- Rules index: {RULES_PAGE}\n\n"
        f"## Rules targeted for this set\n\n"
        f"{wanted}\n\n"
        f"## How to retrieve verbatim text\n\n"
        f"```\n"
        f"pip3 install --break-system-packages pypdf\n"
        f"python3 scripts/pull_texas_rules.py --only {target.get('file','')} --force\n"
        f"```\n"
    )


def file_is_stub(path: Path) -> bool:
    if not path.exists():
        return True
    return STUB_MARKER in path.read_text(encoding="utf-8")[:4000]


def main() -> int:
    ap = argparse.ArgumentParser(description="Pull verbatim Texas court rules")
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

    # Cache extracted PDF text by pdf path (TRCP file feeds two set files).
    text_cache: dict[str, str | None] = {}

    def get_text(pdf: str) -> str | None:
        if pdf not in text_cache:
            data = download_pdf(pdf)
            text_cache[pdf] = extract_pdf_text(data) if data else None
        return text_cache[pdf]

    wrote, stubbed, skipped = 0, 0, 0
    for target in manifest.get("targets", []):
        fname = target.get("file")
        if not fname:
            continue
        if only and fname not in only:
            continue
        path = out_dir / fname

        if path.exists() and not file_is_stub(path) and not args.force:
            print(f"SKIP (non-stub) {fname} — pass --force to overwrite")
            skipped += 1
            continue

        wanted = [str(r) for r in target.get("rules", [])]
        rules: list[tuple[str, str, str]] = []
        reason = ""
        if args.stubs_only:
            reason = "--stubs-only requested"
        else:
            pdf = target.get("pdf", "")
            txt = get_text(pdf)
            if txt is None:
                reason = "PDF download failed or pypdf not installed"
            else:
                rules = extract_rules(txt, wanted)
                if not rules:
                    reason = "no requested rule found in extracted PDF text"

        if rules:
            path.write_text(render_set(target, rules), encoding="utf-8")
            wrote += 1
            print(f"WROTE {fname} ({len(rules)}/{len(wanted)} rules)")
        else:
            path.write_text(render_stub(target, reason), encoding="utf-8")
            stubbed += 1
            print(f"STUB  {fname} — {reason}")

    print(f"\nDone: {wrote} fetched, {stubbed} stub, {skipped} skipped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
