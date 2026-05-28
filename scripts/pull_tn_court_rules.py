#!/usr/bin/env python3
"""Pull selected Tennessee statewide rule sets from the
authoritative `tncourts.gov` HTML mirror and convert each rule
set to a verbatim Markdown corpus file.

Output: plugins/tn-court-docs/skills/tn-law-references/references/court-rules/
One MD file per rule set, named after the rule set.

## Source

The Tennessee Administrative Office of the Courts publishes the
statewide rule sets as Drupal HTML at `tncourts.gov`. Each rule
set has a landing page that links out to one HTML sub-page per
rule (sometimes 288+ pages per rule set). The body of each sub-
page sits inside `<div class="field--name-field-rules-rule-content"
...>` and contains only the rule text proper (no navigation
chrome). No authentication, no API key, no Cloudflare gate.

## Target catalog

Statewide rule sets covering the civil-practice surface:

  - Tennessee Rules of Civil Procedure (Tenn. R. Civ. P.)
  - Tennessee Rules of Evidence (Tenn. R. Evid.)
  - Tennessee Rules of Appellate Procedure (Tenn. R. App. P.)
  - Tennessee Supreme Court Rules (including Tenn. Sup. Ct. R. 4
    on citation of unpublished opinions)

The four-flagship-county and other local-rule sets are county-by-
county and live behind individual clerk sites; they are written
as pointer stubs in this corpus (developers can extend the
TARGETS list as new sources come online).

## Usage

    python3 scripts/pull_tn_court_rules.py --workers 4

    python3 scripts/pull_tn_court_rules.py \\
        --only Tenn-Rules-Civil-Procedure

## Dependencies

Python 3.10+ stdlib only.
"""

from __future__ import annotations

import argparse
import html
import json
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import List, Optional, Tuple

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 "
    "Safari/537.36 claude-legal/1.0"
)

BASE = "https://www.tncourts.gov"


# ----------------------------------------------------------------------
# Targets.
# ----------------------------------------------------------------------

@dataclass
class RuleSetTarget:
    label: str          # filename stem
    title: str          # H1 in the rendered MD
    topic: str          # one-line topic descriptor
    landing: str        # landing page URL under BASE (absolute)
    # The sub-page path prefix used to discover per-rule URLs from
    # the landing page (relative to BASE).
    rule_path_prefix: str
    # Optional: a pointer-only target with no fetch path (for sets
    # we do not have a verbatim source for — county local rules).
    stub_only: bool = False
    stub_note: str = ""


TARGETS: List[RuleSetTarget] = [
    RuleSetTarget(
        label="Tenn-Rules-Civil-Procedure",
        title="Tennessee Rules of Civil Procedure",
        topic="Civil procedure in Tennessee's circuit and chancery courts",
        landing=BASE + "/courts/supreme-court/rules/rules-civil-procedure",
        rule_path_prefix="/courts/rules-civil-procedure/rules/rules-civil-procedure-rules/",
    ),
    RuleSetTarget(
        label="Tenn-Rules-Evidence",
        title="Tennessee Rules of Evidence",
        topic="Evidence in Tennessee's trial courts",
        landing=BASE + "/courts/supreme-court/rules/rules-evidence",
        rule_path_prefix="/courts/rules-evidence/",
    ),
    RuleSetTarget(
        label="Tenn-Rules-Appellate-Procedure",
        title="Tennessee Rules of Appellate Procedure",
        topic="Appellate practice (Supreme Court, Court of Appeals, "
              "Court of Criminal Appeals)",
        landing=BASE + "/courts/supreme-court/rules/rules-appellate-procedure",
        rule_path_prefix="/courts/rules-appellate-procedure/",
    ),
    RuleSetTarget(
        label="Tenn-Supreme-Court-Rules",
        title="Tennessee Supreme Court Rules",
        topic="Supreme Court Rules (incl. Tenn. Sup. Ct. R. 4 on "
              "citation; Rule 9 on disciplinary enforcement; etc.)",
        landing=BASE + "/courts/supreme-court/rules/supreme-court-rules",
        rule_path_prefix="/courts/supreme-court/rules/supreme-court-rules/",
    ),
    # Pointer-only — county-by-county local rules indexed at the AOC.
    RuleSetTarget(
        label="Tenn-Local-Rules-Practice",
        title="Tennessee Local Rules of Practice (per-county index)",
        topic="Per-county local rules — typography, page limits, "
              "chambers copies, motion-docket scheduling",
        landing=BASE + "/courts/court-rules2/local-rules-practice",
        rule_path_prefix="",
        stub_only=True,
        stub_note=(
            "Local rules are published one set per county by each "
            "clerk and are indexed at the AOC 'Local Rules of "
            "Practice' page. They are not aggregated into a single "
            "rule-set page that this puller can walk. Confirm the "
            "specific county's current local rules at the AOC "
            "index and fetch the PDF for the filing court."
        ),
    ),
]


# ----------------------------------------------------------------------
# HTTP.
# ----------------------------------------------------------------------

def http_get(url: str, *, retries: int = 4,
             base_sleep: float = 1.5,
             timeout: float = 60.0) -> bytes:
    """Fetch a URL with jittered exponential-backoff retries."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;"
                  "q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    parsed = urllib.parse.urlsplit(url)
    safe_path = urllib.parse.quote(parsed.path, safe="/%():'.,")
    safe_url = urllib.parse.urlunsplit(
        (parsed.scheme, parsed.netloc, safe_path,
         parsed.query, parsed.fragment)
    )
    req = urllib.request.Request(safe_url, headers=headers)
    last_exc: Optional[BaseException] = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last_exc = e
        except Exception as e:  # noqa: BLE001
            last_exc = e
        sleep_for = base_sleep * (2 ** attempt) * (0.5 + random.random())
        time.sleep(sleep_for)
    assert last_exc is not None
    raise last_exc


# ----------------------------------------------------------------------
# HTML extraction.
# ----------------------------------------------------------------------

RULE_BODY_RE = re.compile(
    r'<div\s+class="field field--name-field-rules-rule-content[^"]*"'
    r'[^>]*>(.*?)</div>\s*</section>',
    re.DOTALL | re.IGNORECASE,
)

RULE_TITLE_RE = re.compile(
    r'<title>\s*([^<]+?)\s*\|\s*Tennessee',
    re.DOTALL | re.IGNORECASE,
)


def _strip_to_md(html_chunk: str) -> str:
    """Convert a snippet of HTML to plain Markdown paragraphs."""
    s = re.sub(r"<script\b[^>]*>.*?</script>",
               "", html_chunk, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r"<style\b[^>]*>.*?</style>",
               "", s, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r"<p\b[^>]*>", "\n\n", s, flags=re.IGNORECASE)
    s = re.sub(r"</p>", "", s, flags=re.IGNORECASE)
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.IGNORECASE)
    s = re.sub(r"<li\b[^>]*>", "\n- ", s, flags=re.IGNORECASE)
    s = re.sub(r"</li>", "", s, flags=re.IGNORECASE)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    out_lines = []
    for para in re.split(r"\n\s*\n", s):
        para = re.sub(r"[ \t]+", " ", para).strip()
        if para:
            out_lines.append(para)
    return "\n\n".join(out_lines)


def parse_rule_subpage(html_text: str) -> Tuple[str, str]:
    """Return (heading, body_md) for one rule sub-page.

    `heading` is the rule number + title from the <title> tag
    (e.g., "Rule 10.01: Caption — Names of Parties."). `body_md`
    is the contents of the field-rules-rule-content div.
    """
    tm = RULE_TITLE_RE.search(html_text)
    heading = tm.group(1).strip() if tm else ""

    bm = RULE_BODY_RE.search(html_text)
    body_md = _strip_to_md(bm.group(1)) if bm else ""

    return heading, body_md


# ----------------------------------------------------------------------
# Landing-page → sub-page discovery.
# ----------------------------------------------------------------------

def discover_subpages(landing_html: str, prefix: str) -> List[str]:
    """Return a sorted list of unique sub-page paths (relative to
    BASE) found in the landing page that begin with `prefix`."""
    if not prefix:
        return []
    pattern = re.compile(
        r'href="(' + re.escape(prefix) + r'[^"#?]+)"'
    )
    seen: List[str] = []
    seen_set = set()
    for m in pattern.finditer(landing_html):
        path = m.group(1)
        if path == prefix or path == prefix.rstrip("/"):
            continue
        if path not in seen_set:
            seen_set.add(path)
            seen.append(path)
    return seen


# ----------------------------------------------------------------------
# Render.
# ----------------------------------------------------------------------

HEADER = """# {title} — {topic}

> **Source:** {source}
> **Fetched:** {fetched}
> **Format:** verbatim conversion of the Tennessee AOC HTML
> publication at `tncourts.gov`

> **NOT LEGAL ADVICE.** Generated content is a drafting aid;
> verify against the current rule before filing.

---

"""


def render_rule_set_md(
    target: RuleSetTarget, fetched_iso: str,
    sections: List[Tuple[str, str]],
) -> str:
    """Render one MD file aggregating all rule sub-pages of a set."""
    body_parts: List[str] = []
    for heading, body in sections:
        h = heading.strip() or "Rule"
        # Promote the rule number/title to an H2.
        body_parts.append(f"## {h}\n\n{body}".rstrip())
    body = "\n\n".join(body_parts) + "\n"
    body = re.sub(r"\n{3,}", "\n\n", body)
    return HEADER.format(
        title=target.title, topic=target.topic,
        source=target.landing, fetched=fetched_iso,
    ) + body


def render_stub(target: RuleSetTarget, fetched_iso: str,
                reason: str) -> str:
    note = target.stub_note or reason
    return (
        f"# {target.title} — {target.topic}\n\n"
        f"> **Source:** {target.landing}\n"
        f"> **Fetched:** {fetched_iso}\n"
        f"> **Status:** _(stub — verbatim text not retrieved)_ — {reason}\n"
        f"> **Format:** pointer stub\n\n"
        f"> **NOT LEGAL ADVICE.** This file is a pointer to the "
        f"canonical source; verify against the source itself "
        f"before filing.\n\n"
        f"---\n\n"
        f"## Scope\n\n"
        f"{target.topic}.\n\n"
        f"## How to retrieve verbatim text\n\n"
        f"Open the canonical URL above in a browser, or re-run "
        f"`scripts/pull_tn_court_rules.py --only {target.label}` "
        f"to retry. The Tennessee AOC publishes this rule set at "
        f"`tncourts.gov`; no authentication is required.\n\n"
        f"## Notes\n\n"
        f"{note}\n"
    )


# ----------------------------------------------------------------------
# Output writing.
# ----------------------------------------------------------------------

@dataclass
class WriteResult:
    label: str
    path: Path
    bytes_written: int
    rules: int
    error: Optional[str]
    stub: bool


def _file_is_stub(path: Path) -> bool:
    try:
        head = path.read_text(encoding="utf-8")[:1024]
    except Exception:  # noqa: BLE001
        return True
    return "Format:** pointer stub" in head or "(stub" in head


def fetch_rule_set(target: RuleSetTarget, out_dir: Path,
                   fetched_iso: str,
                   max_rules: Optional[int] = None) -> WriteResult:
    out_path = out_dir / f"{target.label}.md"

    if target.stub_only:
        rendered = render_stub(target, fetched_iso,
                               "stub-only target (no per-rule HTML index)")
        tmp = out_path.with_suffix(".md.tmp")
        tmp.write_text(rendered, encoding="utf-8")
        tmp.rename(out_path)
        return WriteResult(target.label, out_path,
                           out_path.stat().st_size, 0,
                           None, stub=True)

    try:
        # 1. Fetch the landing page and discover sub-page URLs.
        landing_bytes = http_get(target.landing)
        landing_html = landing_bytes.decode("utf-8", errors="replace")
        subpages = discover_subpages(landing_html, target.rule_path_prefix)
        if not subpages:
            raise RuntimeError(
                f"no sub-pages found under {target.rule_path_prefix} "
                f"(landing layout may have changed)"
            )
        if max_rules is not None:
            subpages = subpages[:max_rules]

        # 2. Fetch each sub-page sequentially with a short pause
        #    (be polite to the upstream).
        sections: List[Tuple[str, str]] = []
        for i, path in enumerate(subpages):
            url = BASE + path
            try:
                data = http_get(url)
            except Exception as e:  # noqa: BLE001
                sections.append((f"(fetch failed: {path})",
                                 f"_(could not retrieve: {e})_"))
                continue
            html_text = data.decode("utf-8", errors="replace")
            heading, body_md = parse_rule_subpage(html_text)
            if not body_md.strip():
                # Some sub-pages may be section dividers with no body.
                body_md = "_(no rule text in field-rules-rule-content; " \
                          "may be a section divider)_"
            sections.append((heading, body_md))
            # Light pacing: small random sleep to spread requests.
            time.sleep(0.15 + random.random() * 0.2)

        rendered = render_rule_set_md(target, fetched_iso, sections)
    except Exception as exc:  # noqa: BLE001
        if out_path.exists() and not _file_is_stub(out_path):
            return WriteResult(
                target.label, out_path,
                out_path.stat().st_size, 0,
                f"fetch failed (kept existing file): {exc}",
                stub=False,
            )
        rendered = render_stub(target, fetched_iso, f"{exc}")
        tmp = out_path.with_suffix(".md.tmp")
        tmp.write_text(rendered, encoding="utf-8")
        tmp.rename(out_path)
        return WriteResult(target.label, out_path,
                           out_path.stat().st_size, 0,
                           f"{exc}", stub=True)

    tmp = out_path.with_suffix(".md.tmp")
    tmp.write_text(rendered, encoding="utf-8")
    tmp.rename(out_path)
    return WriteResult(target.label, out_path,
                       out_path.stat().st_size,
                       len(sections), None, stub=False)


# ----------------------------------------------------------------------
# Manifest.
# ----------------------------------------------------------------------

def update_manifest(out_dir: Path, fetched_iso: str,
                    version: str = "0.1.0") -> Path:
    manifest_path = out_dir / "_manifest.json"
    payload = {
        "version": version,
        "last_pulled": fetched_iso,
        "source": "https://www.tncourts.gov/",
        "notes": (
            "Pulled by scripts/pull_tn_court_rules.py. Tennessee "
            "AOC publishes the statewide rule sets as Drupal HTML "
            "with one sub-page per rule. The puller walks each rule "
            "set's landing page, discovers sub-page URLs by path "
            "prefix, and extracts the rule body from the "
            "`field--name-field-rules-rule-content` div. County-by-"
            "county local rules are pointer stubs (no aggregated "
            "HTML index)."
        ),
    }
    manifest_path.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    return manifest_path


# ----------------------------------------------------------------------
# CLI.
# ----------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--out",
        type=Path,
        default=Path(
            "plugins/tn-court-docs/skills/tn-law-references/"
            "references/court-rules"
        ),
        help="Output directory for the corpus.",
    )
    ap.add_argument(
        "--only", nargs="*",
        help="Restrict to these rule-set labels.",
    )
    ap.add_argument(
        "--workers", type=int, default=2,
        help="Concurrent rule-set fetches (default 2). Each rule "
             "set walks many sub-pages serially within its worker.",
    )
    ap.add_argument(
        "--max-rules-per-set", type=int, default=None,
        help="Cap sub-pages fetched per rule set (debug).",
    )
    ap.add_argument(
        "--manifest-version", default="0.1.0",
        help="Version to write into _manifest.json on success.",
    )
    args = ap.parse_args()

    out_dir: Path = args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    only = set(args.only) if args.only else None
    targets = [t for t in TARGETS if only is None or t.label in only]
    if not targets:
        print(f"!! no targets match --only {args.only!r}",
              file=sys.stderr)
        return 2

    fetched_iso = date.today().isoformat()
    print(f"=== pulling {len(targets)} TN rule set(s) → "
          f"{out_dir} (workers={args.workers})", flush=True)

    results: List[WriteResult] = []
    workers = max(1, min(args.workers, len(targets)))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(fetch_rule_set, t, out_dir, fetched_iso,
                        args.max_rules_per_set): t
            for t in targets
        }
        for fut in as_completed(futures):
            t = futures[fut]
            try:
                results.append(fut.result())
            except Exception as exc:  # noqa: BLE001
                results.append(WriteResult(
                    t.label, out_dir / f"{t.label}.md",
                    0, 0, str(exc), stub=True,
                ))

    by_label = {r.label: r for r in results}
    ordered = [by_label[t.label] for t in targets if t.label in by_label]
    for t, r in zip(targets, ordered):
        tag = ("OK  " if r.error is None and not r.stub
               else "STUB" if r.stub else "FAIL")
        rules = f"{r.rules} rules" if r.rules else "0 rules"
        print(f"     [{tag}] {t.label}.md "
              f"({r.bytes_written:,} bytes, {rules})"
              + (f" — {r.error}" if r.error else ""),
              flush=True)

    fail = [r for r in ordered if r.error is not None
            and "kept existing file" not in (r.error or "")]
    total_bytes = sum(r.bytes_written for r in ordered)
    total_rules = sum(r.rules for r in ordered)
    print(f"\n=== wrote {len(ordered)} rule set(s), "
          f"{total_rules:,} rule sub-pages, "
          f"{total_bytes:,} bytes; "
          f"{len(fail)} hard-failed", flush=True)

    if only is None:
        mp = update_manifest(out_dir, fetched_iso,
                             args.manifest_version)
        print(f"=== updated {mp}", flush=True)

    return 0 if not fail else 1


if __name__ == "__main__":
    sys.exit(main())
