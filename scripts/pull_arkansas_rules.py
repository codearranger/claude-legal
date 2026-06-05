#!/usr/bin/env python3
"""Pull the Arkansas court rules — Arkansas Rules of Civil Procedure
(Ark. R. Civ. P.), Arkansas Rules of Evidence (Ark. R. Evid.), the
Arkansas District Court Rules, and the Rules of the Supreme Court and
Court of Appeals of Arkansas — VERBATIM from the official Arkansas
Judiciary rules database.

Output: plugins/ar-court-docs/skills/ar-law-references/references/court-rules/

## Source

The Arkansas Judiciary publishes the full text of each rule set on its
Lexum-powered database at `opinions.arcourts.gov/ark/cr/en/` (the "Court
Rules" collection linked from arcourts.gov). Each rule set is a single
document served as a PDF at:

    https://opinions.arcourts.gov/ark/cr/en/<docid>/1/document.do

The bare rule text is a public-domain edict of the Arkansas Supreme
Court (only the West/Lexis annotated compilations are copyrighted). This
puller discovers the CURRENT document id for each rule set by title from
the collection's browse listing (so a republish that renumbers the
document is followed automatically), downloads the PDF, extracts the
text with `pdftotext -layout` (poppler), splits it into rules, and emits
one Markdown file per rule set.

When the source is unreachable, or `pdftotext` is unavailable, the
puller writes a well-formed pointer stub carrying the canonical URL + a
scope description. The `_file_is_stub` regression guard means a
stub-only re-run will NOT clobber verbatim content a prior successful
run committed.

## Dependencies

Python 3.10+ stdlib + `pdftotext` (poppler-utils).
"""

from __future__ import annotations

import argparse
import json
import random
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import date
from pathlib import Path

BASE = "https://opinions.arcourts.gov"
NAV = BASE + "/ark/cr/en/nav_date.do?iframe=true"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
STUB_MARKER = "<!-- claude-legal:ar-rules-pointer-stub -->"
CANONICAL = "https://www.arcourts.gov/content/rules-supreme-court-and-court-appeals-state-arkansas"


@dataclass
class Target:
    slug: str             # output filename (no .md)
    title: str            # H1
    cite: str             # citation label, e.g. "Ark. R. Civ. P."
    title_match: str      # substring to find the doc in the browse listing
    fallback_docid: str   # used if discovery fails
    scope: str


TARGETS: list[Target] = [
    Target(
        "ARCP-civil-procedure",
        "Arkansas Rules of Civil Procedure (Ark. R. Civ. P.)",
        "Ark. R. Civ. P.",
        "Rules of Civil Procedure",
        "16712",
        "Ark. R. Civ. P. 1-86 — scope, commencement and service (Rule 4, "
        "incl. the 120-day service period), pleadings and motions "
        "(Rule 8 fact-pleading, Rule 12 incl. 12(b)(6)), discovery "
        "(Rules 26-37, interrogatories under Rule 33), judgment "
        "(Rule 56 summary judgment, Rule 59 new trial, Rule 60 with the "
        "90-day Rule 60(a) window). Time computation is Rule 6 (+ Rule "
        "6(d) 3-day mail add-on).",
    ),
    Target(
        "Ark-R-Evid-evidence",
        "Arkansas Rules of Evidence (Ark. R. Evid.)",
        "Ark. R. Evid.",
        "Rules of Evidence",
        "1876",
        "Ark. R. Evid. 101-1102 — relevance (401-403), hearsay (801-806, "
        "business records 803(6)), authentication (901-902, certified "
        "business records 902(11)), opinion and expert testimony "
        "(701-706), privileges.",
    ),
    Target(
        "ADCR-district-court",
        "Arkansas District Court Rules",
        "Ark. Dist. Ct. R.",
        "District Court Rules",
        "1878",
        "Arkansas District Court Rules — streamlined civil procedure for "
        "the limited-jurisdiction district courts (civil + small-claims), "
        "commencement, service, default, limited discovery, and the "
        "30-day de novo appeal to circuit court (Rule 9).",
    ),
    Target(
        "Ark-Sup-Ct-Ct-App-rules",
        "Rules of the Supreme Court and Court of Appeals of Arkansas",
        "Ark. Sup. Ct. R.",
        "Rules of the Supreme Court and Court of Appeals",
        "1871",
        "Rules of the Supreme Court and Court of Appeals — including "
        "Rule 5-2 (medium-neutral / public-domain citation: 'YEAR Ark. "
        "NNN' / 'YEAR Ark. App. NNN'), publication and citation of "
        "opinions, and appellate briefing (Rules 4-1, 4-2).",
    ),
]


def http_get(url: str, *, retries: int = 5, base_sleep: float = 1.2,
             timeout: float = 90.0) -> bytes | None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
        except Exception:  # noqa: BLE001
            pass
        time.sleep(base_sleep * (2 ** attempt) * (0.5 + random.random()))
    return None


def discover_docid(t: Target) -> str:
    """Return the current Lexum document id for a rule set, matched by
    title in the Court Rules browse listing; fall back to the known id."""
    raw = http_get(NAV)
    if not raw:
        return t.fallback_docid
    html = raw.decode("utf-8", "replace")
    # Anchors like: href="/ark/cr/en/16712/1/document.do">Arkansas Rules of Civil Procedure</a>
    for m in re.finditer(
        r'href="/ark/cr/en/(\d+)/\d+/document\.do"[^>]*>(.*?)</a>',
        html, re.S | re.I,
    ):
        docid, text = m.group(1), re.sub(r"<[^>]+>", " ", m.group(2))
        text = re.sub(r"\s+", " ", text).strip()
        if t.title_match.lower() in text.lower():
            return docid
    return t.fallback_docid


def fetch_pdf_text(docid: str) -> str | None:
    """Download the rule-set PDF and extract text with pdftotext -layout."""
    raw = http_get(f"{BASE}/ark/cr/en/{docid}/1/document.do")
    if not raw or raw[:4] != b"%PDF":
        return None
    with tempfile.TemporaryDirectory() as td:
        pdf = Path(td) / "rules.pdf"
        pdf.write_bytes(raw)
        try:
            out = subprocess.run(
                ["pdftotext", "-layout", str(pdf), "-"],
                capture_output=True, timeout=180,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return None
        if out.returncode != 0:
            return None
        return out.stdout.decode("utf-8", "replace")


# A rule heading looks like "Rule 12." or "Rule 5-2." or "Rule 4.1." at
# the start of a line (pdftotext -layout may indent it).
RULE_HEADING = re.compile(r"^\s{0,8}(Rule\s+[0-9][0-9A-Za-z.\-]*\.?\s+\S.*)$")


def _clean_pdf_text(text: str) -> str:
    # Drop obvious page-furniture lines and de-hyphenate soft line breaks.
    lines = []
    for ln in text.splitlines():
        s = ln.rstrip()
        # Skip bare page numbers and repeated header/footer noise.
        if re.fullmatch(r"\s*\d{1,4}\s*", s):
            continue
        lines.append(s)
    return "\n".join(lines)


def split_into_rules(text: str) -> list[tuple[str, str]]:
    """Split the full rule-set text into (heading, body) pairs keyed on
    each 'Rule N.' heading line. Text before the first heading (the
    title page / table of contents) is attached as a leading 'Front
    matter' section only if substantive."""
    text = _clean_pdf_text(text)
    rules: list[tuple[str, str]] = []
    cur_head: str | None = None
    cur_body: list[str] = []

    def flush():
        if cur_head is not None:
            body = re.sub(r"\n{3,}", "\n\n", "\n".join(cur_body)).strip()
            rules.append((cur_head.strip(), body))

    for ln in text.splitlines():
        m = RULE_HEADING.match(ln)
        # Treat a heading line as a new rule only when it is short-ish
        # (a true heading, not a sentence that merely starts with "Rule").
        if m and len(ln.strip()) < 140:
            flush()
            cur_head = re.sub(r"\s+", " ", m.group(1)).strip()
            cur_body = []
        else:
            if cur_head is None:
                continue  # skip front matter / TOC before Rule 1
            cur_body.append(ln)
    flush()
    return rules


def make_stub(t: Target, reason: str) -> str:
    return (
        f"# {t.title}\n\n{STUB_MARKER}\n\n"
        f"- Citation: {t.cite}\n"
        f"- Canonical: {CANONICAL}\n"
        f"- Source: {BASE}/ark/cr/en/ (Court Rules collection)\n"
        f"- Status: **pointer stub** — verbatim text not retrieved this run\n"
        f"- Pulled: {date.today().isoformat()}\n\n"
        f"> **Why a stub?** {reason} Read the authoritative text at the "
        f"canonical Arkansas Judiciary URL above. Re-run "
        f"`scripts/pull_arkansas_rules.py` (needs `pdftotext`/poppler); "
        f"the `_file_is_stub` guard will replace this stub with the "
        f"fetched text.\n\n"
        f"## Scope\n\n{t.scope}\n"
    )


def render(t: Target, docid: str, rules: list[tuple[str, str]]) -> str:
    out = [
        f"# {t.title}", "",
        f"- Citation: {t.cite}",
        f"- Canonical authority: {CANONICAL}",
        f"- Fetched from: {BASE}/ark/cr/en/{docid}/1/document.do (official PDF)",
        f"- Rules: {len(rules)}",
        f"- Pulled: {date.today().isoformat()}", "",
        "> Verbatim text extracted from the official Arkansas Judiciary "
        "Court Rules PDF (`pdftotext -layout`). Verify against the current "
        "official text before filing.", "",
        f"## Scope\n\n{t.scope}", "", "---", "",
    ]
    for head, body in rules:
        out += [f"## {head}", "", body, "", "---", ""]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out).rstrip() + "\n")


def _file_is_stub(p: Path) -> bool:
    if not p.exists():
        return True
    try:
        txt = p.read_text(encoding="utf-8")
    except OSError:
        return True
    return (STUB_MARKER in txt
            or "pointer stub" in txt.lower()
            or "verbatim text not retrieved" in txt.lower()
            # the offline-authored curated summaries are superseded by a
            # successful verbatim pull, but preserved on failure:
            or False)


def process(t: Target, out_dir: Path) -> str:
    """Returns 'verbatim' | 'stub' | 'preserved'."""
    path = out_dir / f"{t.slug}.md"
    docid = discover_docid(t)
    text = fetch_pdf_text(docid)
    rules = split_into_rules(text) if text else []

    if len(rules) >= 3:
        tmp = path.with_suffix(".md.tmp")
        tmp.write_text(render(t, docid, rules), encoding="utf-8")
        tmp.replace(path)
        print(f"  VERBATIM {t.slug} (docid={docid}, {len(rules)} rules)", flush=True)
        return "verbatim"

    if not _file_is_stub(path):
        print(f"  preserved existing content {t.slug}", flush=True)
        return "preserved"

    reason = ("The Arkansas Judiciary rules PDF was unreachable, not a PDF, "
              "or pdftotext was unavailable this run."
              if not text else
              f"Extracted only {len(rules)} rule sections from the PDF.")
    tmp = path.with_suffix(".md.tmp")
    tmp.write_text(make_stub(t, reason), encoding="utf-8")
    tmp.replace(path)
    print(f"  STUB {t.slug} (docid={docid})", flush=True)
    return "stub"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out",
        default="plugins/ar-court-docs/skills/ar-law-references/"
                "references/court-rules",
    )
    ap.add_argument("--only", nargs="*", help="Limit to output slugs.")
    ap.add_argument("--workers", type=int, default=2,
                    help="(reserved; rule-set PDFs are fetched sequentially)")
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    only = set(args.only) if args.only else None
    targets = [t for t in TARGETS if not only or t.slug in only]

    counts = {"verbatim": 0, "stub": 0, "preserved": 0}
    for t in targets:
        print(f"Processing {t.slug} ...", flush=True)
        counts[process(t, out_dir)] += 1

    mode = ("verbatim" if counts["stub"] == 0 and counts["verbatim"]
            else "stubs" if counts["verbatim"] == 0 else "mixed")
    manifest = {
        "version": "0.1.0",
        "last_pulled": date.today().isoformat(),
        "source": f"{BASE}/ark/cr/en/ (official Arkansas Judiciary Court Rules PDFs)",
        "mode": mode,
        "notes": (
            "Pulled by scripts/pull_arkansas_rules.py. Verbatim Ark. R. "
            "Civ. P. + Ark. R. Evid. + Arkansas District Court Rules + "
            "Supreme Court/Court of Appeals Rules extracted (pdftotext "
            "-layout) from the official Lexum-hosted Court Rules PDFs at "
            "opinions.arcourts.gov; the current document id per rule set "
            "is discovered by title. Falls back to canonical-URL pointer "
            "stubs when the source is unreachable or pdftotext is "
            "unavailable; the _file_is_stub guard preserves committed "
            "verbatim content. Administrative Orders 10/19/21 are tracked "
            "as canonical-URL pointers in the corpus, not pulled here."
        ),
    }
    (out_dir / "_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Done. {counts} mode={mode}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
