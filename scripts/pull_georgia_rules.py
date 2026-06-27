#!/usr/bin/env python3
"""Pull verbatim Georgia court-rule text and write one Markdown file per rule
SET.

Output (default):
    plugins/ga-court-docs/skills/ga-law-references/references/court-rules/

The set->file->source->rule-list map is read from the corpus's own
`_manifest.json`.

## Source

Georgia publishes its uniform court rules and appellate-court rules as open
documents (no paywall, unlike the official O.C.G.A. statute text):

- **Uniform Superior Court Rules (USCR)** and **Uniform Magistrate Court
  Rules** are published as dated-filename PDFs on `assets.georgiacourts.gov`,
  discoverable from the rules landing page at
  `https://georgiacourts.gov/`. Because the OCA re-issues an amended edition
  under a new dated filename, each set's `pdf` field in `_manifest.json`
  records the current one (and `pdf_page` records the landing page to
  re-discover it from).
- **Uniform State Court Rules** largely track the USCR and are published the
  same way.
- **Supreme Court of Georgia rules** — `https://www.gasupreme.us/rules/`.
- **Court of Appeals of Georgia rules** — `https://www.gaappeals.gov/court-rules/`.
- **HTML mirror fallback** — `https://www.courtrules.net/georgia/...` carries
  an HTML copy of many sets; a set's optional `html` field records it.

The puller prefers the PDF (extracted with `pypdf`), falls back to the HTML
mirror when present, and writes a pointer stub when neither yields text.

A USCR/State/Magistrate rule heading reads `Rule 6.2. Time for Response`; the
appellate rules use `Rule 22.` forms. The puller slices each rule's body from
its heading to the next rule heading and discards table-of-contents copies of
each heading (those carry dotted leaders / page numbers).

## Behavior on failure / regression protection

- `pypdf` is an optional dependency. If it is not importable, or a PDF cannot
  be downloaded, or no requested rule is found (and no HTML fallback yields
  text), the set file is written as a well-formed **pointer stub** carrying
  the canonical source URLs — never fabricated text.
- A rule whose body cannot be located is skipped (not emitted as a gap).
- A `_file_is_stub` guard prevents a failed/offline run from clobbering
  committed verbatim content: a non-stub file is left untouched unless
  `--force` is passed.

## Usage

    python3 scripts/pull_georgia_rules.py
    python3 scripts/pull_georgia_rules.py --only uniform-superior-court-rules.md
    python3 scripts/pull_georgia_rules.py --stubs-only
    python3 scripts/pull_georgia_rules.py --force

Install the optional PDF dependency:

    pip3 install --break-system-packages pypdf

## Dependencies

Python 3.10+ stdlib; `pypdf` (optional — stubs are written without it).
"""

from __future__ import annotations

import argparse
import html
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
GEORGIACOURTS = "https://georgiacourts.gov"
RULES_PAGE = "https://georgiacourts.gov/"

DEFAULT_OUT = (
    "plugins/ga-court-docs/skills/ga-law-references/references/court-rules"
)

STUB_MARKER = "<!-- ga-court-rules: pointer-stub -->"
VERBATIM_MARKER = "<!-- ga-court-rules: verbatim -->"


def repo_root() -> Path:
    here = Path(__file__).resolve().parent.parent
    if not (here / "scripts" / "lint-skills.py").exists():
        print("ERROR: cannot locate repo root", file=sys.stderr)
        sys.exit(1)
    return here


def _abs_url(u: str) -> str:
    if not u:
        return u
    if u.startswith("http"):
        return u
    return GEORGIACOURTS + u


def _curl_cffi_get(url: str, timeout: int) -> bytes | None:
    """Fetch bytes with curl_cffi Chrome-TLS impersonation when available.
    The courtrules.net HTML mirror sits behind Cloudflare, which 403s stdlib
    urllib; Chrome impersonation passes where urllib cannot. Returns None if
    the package is absent or the fetch fails (caller falls back to urllib)."""
    try:
        from curl_cffi import requests as creq  # type: ignore
    except Exception:
        return None
    try:
        r = creq.get(url, impersonate="chrome", timeout=timeout)
        if r.status_code == 200 and r.content:
            return r.content
    except Exception:
        return None
    return None


def download_pdf(pdf: str, timeout: int = 90) -> bytes | None:
    url = _abs_url(pdf)
    data = _curl_cffi_get(url, timeout)
    if data is None:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = resp.read()
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
            return None
    if not data or not data.startswith(b"%PDF"):
        return None
    return data


def fetch_html(url: str, timeout: int = 60) -> str | None:
    data = _curl_cffi_get(_abs_url(url), timeout)
    if data is not None:
        return data.decode("utf-8", "replace")
    req = urllib.request.Request(_abs_url(url), headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", "replace")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
        return None


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


def html_to_text(raw: str) -> str | None:
    """Reduce an HTML-mirror page to readable text."""
    s = raw
    s = re.sub(r"(?is)<script\b.*?</script>", " ", s)
    s = re.sub(r"(?is)<style\b.*?</style>", " ", s)
    m = re.search(r"(?is)<body\b[^>]*>(.*?)</body>", s)
    if m:
        s = m.group(1)
    s = re.sub(r"(?i)</p\s*>", "\n", s)
    s = re.sub(r"(?i)<br\s*/?>", "\n", s)
    s = re.sub(r"(?i)</div\s*>", "\n", s)
    s = re.sub(r"(?s)<[^>]+>", "", s)
    s = html.unescape(s).replace("\xa0", " ")
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in s.split("\n")]
    out: list[str] = []
    blank = False
    for ln in lines:
        if ln:
            out.append(ln)
            blank = False
        elif not blank and out:
            out.append("")
            blank = True
    text = "\n".join(out).strip()
    return text or None


# A real (non-TOC) rule heading. Georgia uniform/appellate rules use forms:
#   "Rule 6.2. Time for Response"        (USCR — dotted)
#   "Rule 5. Discovery"                  (USCR — bare)
#   "Rule 22. ..."                       (appellate)
_RULE_HEADING_RE = re.compile(
    r"(?im)^\s*Rule\s+([0-9]+(?:\.[0-9]+)?[A-Za-z]?)\.\s+(.+?)\s*$"
)


def _is_toc_line(title: str, tail: str) -> bool:
    """Table-of-contents copies of a heading carry dotted leaders and/or a
    trailing page number; a '[Reserved]'/'[Repealed]' note is not real body."""
    low = title.lower()
    if low.startswith("reserved") or low.startswith("repealed") or title.endswith("]"):
        return True
    if re.search(r"\.\s?\.\s?\.", title):
        return True
    if re.search(r"\.\s?\.\s?\.", tail[:160]):
        return True
    return False


def _all_real_headings(txt: str) -> list[tuple[str, str, int, int]]:
    """Return [(rule_number, title, start, body_start)] for every real rule
    heading, in document order, sorted by position."""
    found: list[tuple[str, str, int, int]] = []
    for m in _RULE_HEADING_RE.finditer(txt):
        title = m.group(2).strip()
        tail = txt[m.end():m.end() + 200]
        if _is_toc_line(title, tail):
            continue
        found.append((m.group(1), title, m.start(), m.end()))
    found.sort(key=lambda t: t[2])
    return found


def _clean_body(body: str) -> str:
    """Tidy extracted text: join hyphenated line breaks, squeeze blank runs,
    strip trailing whitespace per line. Conservative — does not rewrite
    wording."""
    body = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", body)
    lines = [re.sub(r"[ \t]+", " ", ln).rstrip() for ln in body.split("\n")]
    out: list[str] = []
    blank = False
    for ln in lines:
        s = ln.strip()
        if s:
            out.append(s)
            blank = False
        elif not blank and out:
            out.append("")
            blank = True
    return "\n".join(out).strip()


def extract_rules(txt: str, wanted: list[str]) -> list[tuple[str, str, str]]:
    """Return [(rule_number, title, body)] for each wanted rule found. A rule's
    body runs from its heading to the next rule heading; among duplicate
    occurrences (TOC vs body), keep the one with the most substantive body."""
    headings = _all_real_headings(txt)
    occ: dict[str, list[int]] = {}
    for i, (num, _t, _s, _bs) in enumerate(headings):
        occ.setdefault(num, []).append(i)

    def is_descendant(child: str, parent: str) -> bool:
        return child == parent or child.startswith(parent + ".")

    def body_for(i: int, w: str) -> tuple[str, str]:
        _num, title, _start, body_start = headings[i]
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
    name = target.get("name", target.get("set", "Georgia rule set"))
    code = target.get("set", "")
    pdf_url = _abs_url(target.get("pdf", ""))
    html_url = _abs_url(target.get("html", ""))
    lines = [f"# {name} ({code})", "", VERBATIM_MARKER, ""]
    lines.append(
        "> **NOT LEGAL ADVICE.** Verbatim rule text extracted from the Georgia "
        "court-rule source published on georgiacourts.gov / the appellate "
        "courts. Georgia court rules are amended by order of the promulgating "
        "court; verify against the current official source before relying on "
        "any rule."
    )
    lines.append("")
    if pdf_url:
        lines.append(f"Source PDF: {pdf_url}")
    if html_url:
        lines.append(f"Source (HTML mirror): {html_url}")
    lines.append(f"Rules index: {_abs_url(target.get('pdf_page', RULES_PAGE))}")
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
    name = target.get("name", target.get("set", "Georgia rule set"))
    code = target.get("set", "")
    pdf_url = _abs_url(target.get("pdf", ""))
    html_url = _abs_url(target.get("html", ""))
    page = _abs_url(target.get("pdf_page", RULES_PAGE))
    wanted = ", ".join(str(r) for r in target.get("rules", [])) or "(all)"
    src_lines = []
    if pdf_url:
        src_lines.append(f"- Source PDF: {pdf_url}")
    if html_url:
        src_lines.append(f"- Source (HTML mirror): {html_url}")
    src_lines.append(f"- Rules index: {page}")
    sources = "\n".join(src_lines)
    return (
        f"# {name} ({code})\n\n"
        f"{STUB_MARKER}\n\n"
        f"> **NOT LEGAL ADVICE.** Pointer stub — not verbatim. The verbatim "
        f"text of the {name} is published by the relevant Georgia court "
        f"(uniform rules on georgiacourts.gov; appellate rules on the Supreme "
        f"Court / Court of Appeals sites). This file is populated by "
        f"`scripts/pull_georgia_rules.py` (which needs the optional `pypdf` "
        f"dependency and network access). Until a verbatim pull lands, consult "
        f"the canonical source.\n\n"
        f"_Stub reason: {reason}._\n\n"
        f"## Canonical source\n\n"
        f"{sources}\n\n"
        f"## Rules targeted for this set\n\n"
        f"{wanted}\n\n"
        f"## How to retrieve verbatim text\n\n"
        f"```\n"
        f"pip3 install --break-system-packages pypdf\n"
        f"python3 scripts/pull_georgia_rules.py --only {target.get('file','')} --force\n"
        f"```\n"
    )


def _file_is_stub(path: Path) -> bool:
    """True if the file is absent or carries the pointer-stub marker. A
    committed verbatim file (VERBATIM_MARKER) is NOT a stub and is protected
    from clobbering unless --force is passed."""
    if not path.exists():
        return True
    head = path.read_text(encoding="utf-8")[:4000]
    return STUB_MARKER in head or VERBATIM_MARKER not in head


def main() -> int:
    ap = argparse.ArgumentParser(description="Pull verbatim Georgia court rules")
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

    # Cache extracted text by source URL (a PDF may feed more than one set).
    text_cache: dict[str, str | None] = {}

    def get_text(target: dict) -> str | None:
        pdf = target.get("pdf", "")
        if pdf:
            if pdf not in text_cache:
                data = download_pdf(pdf)
                text_cache[pdf] = extract_pdf_text(data) if data else None
            if text_cache[pdf]:
                return text_cache[pdf]
        # HTML-mirror fallback.
        h = target.get("html", "")
        if h:
            if h not in text_cache:
                raw = fetch_html(h)
                text_cache[h] = html_to_text(raw) if raw else None
            return text_cache[h]
        return None

    wrote, stubbed, skipped = 0, 0, 0
    for target in manifest.get("targets", []):
        fname = target.get("file")
        if not fname:
            continue
        if only and fname not in only:
            continue
        path = out_dir / fname

        if path.exists() and not _file_is_stub(path) and not args.force:
            print(f"SKIP (non-stub) {fname} — pass --force to overwrite")
            skipped += 1
            continue

        wanted = [str(r) for r in target.get("rules", [])]
        rules: list[tuple[str, str, str]] = []
        reason = ""
        if args.stubs_only:
            reason = "--stubs-only requested"
        else:
            txt = get_text(target)
            if txt is None:
                reason = "PDF/HTML download failed or pypdf not installed"
            elif not wanted:
                reason = "no rule list configured for this set"
            else:
                rules = extract_rules(txt, wanted)
                if not rules:
                    reason = "no requested rule found in extracted text"

        if rules:
            path.write_text(render_set(target, rules), encoding="utf-8")
            wrote += 1
            print(f"WROTE {fname} ({len(rules)}/{len(wanted)} rules)")
        else:
            # Never regress committed verbatim content to a stub: a transient
            # upstream failure on a --force refresh keeps the real text.
            if path.exists() and not _file_is_stub(path):
                skipped += 1
                print(f"KEEP (verbatim; fetch failed this run) {fname} — {reason}")
                continue
            path.write_text(render_stub(target, reason), encoding="utf-8")
            stubbed += 1
            print(f"STUB  {fname} — {reason}")

    print(f"\nDone: {wrote} fetched, {stubbed} stub, {skipped} skipped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
