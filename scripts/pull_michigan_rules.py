#!/usr/bin/env python3
"""Pull the Michigan Court Rules (MCR) + Michigan Rules of Evidence (MRE).

Output: plugins/mi-court-docs/skills/mi-law-references/references/court-rules/

The canonical publisher is the Michigan Supreme Court / State Court
Administrative Office (courts.michigan.gov), but its rules library serves the
rule text from hash-rotated `/siteassets/...` asset URLs behind a bot gate that
a stdlib client can't resolve. This puller therefore mirrors from
**courtrules.net**, a structured free aggregator that publishes each rule at a
stable URL with the verbatim text in a `rule-text` div — the same
"official-source-gated, use the structured free mirror" pattern the Tennessee
statutes puller uses for Justia. The manifest + per-file headers record the
mirror as the fetch source and courts.michigan.gov as the canonical authority.

Structure on courtrules.net:
  - MCR chapter index : /michigan/michigan-court-rules/part/chapter-N
                        (lists the rule URLs in that chapter)
  - MCR rule page     : /michigan/michigan-court-rules/rule-<ch>-<num>
  - MRE rule index    : /michigan/michigan-rules-of-evidence
  - MRE rule page     : /michigan/michigan-rules-of-evidence/rule-<num>
  - verbatim text     : <div class="rule-text"> ... </div> on each rule page

When the mirror is unreachable the puller writes well-formed pointer stubs
carrying the canonical courts.michigan.gov URL + a chapter scope description.
The `_file_is_stub` regression guard means a stub-only re-run will NOT clobber
verbatim content a prior successful run committed.
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import date
from pathlib import Path

BASE = "https://www.courtrules.net"
CANONICAL = ("https://www.courts.michigan.gov/administration/rules-and-instructions/"
             "court-rules-and-court-administration/")
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
STUB_MARKER = "<!-- claude-legal:mi-rules-pointer-stub -->"


@dataclass
class Target:
    slug: str               # output filename (no .md)
    title: str              # H1
    kind: str               # "mcr-chapter" | "mre"
    index_url: str          # courtrules.net index to discover rule URLs
    rule_re: str            # regex capturing rule path slugs on the index
    scope: str              # for the stub


TARGETS: list[Target] = [
    Target("MCR-chapter-1-general", "Michigan Court Rules — Chapter 1: General Provisions",
           "mcr-chapter", f"{BASE}/michigan/michigan-court-rules/part/chapter-1",
           r'/michigan/michigan-court-rules/(rule-1-[\w-]+)',
           "MCR 1.100-1.111 — applicability, purpose, electronic filing and "
           "signatures (MCR 1.109), time computation (MCR 1.108), and "
           "courtroom interpreters."),
    Target("MCR-chapter-2-civil", "Michigan Court Rules — Chapter 2: Civil Procedure",
           "mcr-chapter", f"{BASE}/michigan/michigan-court-rules/part/chapter-2",
           r'/michigan/michigan-court-rules/(rule-2-[\w-]+)',
           "MCR 2.000-2.640 — commencement, pleadings (MCR 2.111), service "
           "(MCR 2.105), motions (MCR 2.119), discovery (MCR 2.300 et seq.), "
           "summary disposition (MCR 2.116), default (MCR 2.603), judgments and "
           "orders (MCR 2.602)."),
    Target("MCR-chapter-3-special-proceedings",
           "Michigan Court Rules — Chapter 3: Special Proceedings and Actions",
           "mcr-chapter", f"{BASE}/michigan/michigan-court-rules/part/chapter-3",
           r'/michigan/michigan-court-rules/(rule-3-[\w-]+)',
           "MCR 3.000-3.978 — provisional remedies, garnishment (MCR 3.101), "
           "domestic-relations actions (MCR 3.200 et seq.), personal protection "
           "orders (MCR 3.700 et seq.), and juvenile proceedings."),
    Target("MCR-chapter-4-district-court",
           "Michigan Court Rules — Chapter 4: Special Rules for Specific Courts",
           "mcr-chapter", f"{BASE}/michigan/michigan-court-rules/part/chapter-4",
           r'/michigan/michigan-court-rules/(rule-4-[\w-]+)',
           "MCR 4.001-4.401 — district court civil practice, landlord-tenant / "
           "summary proceedings (MCR 4.201), land contract / mortgage "
           "foreclosure, and small claims (MCR 4.301 et seq.)."),
    Target("MRE-evidence", "Michigan Rules of Evidence (MRE)",
           "mre", f"{BASE}/michigan/michigan-rules-of-evidence",
           r'/michigan/michigan-rules-of-evidence/(rule-[\w-]+)',
           "MRE 101-1102 — relevance (401-403), hearsay (801-807, business "
           "records 803(6)), authentication (901-902), opinion and expert "
           "testimony (701-707), and privileges. Restyled effective 2024."),
]


def http_get(url: str, *, retries: int = 4, base_sleep: float = 1.2,
             timeout: float = 30.0) -> str | None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT,
                                               "Accept": "text/html"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
        except Exception:  # noqa: BLE001
            pass
        time.sleep(base_sleep * (2 ** attempt) * (0.5 + random.random()))
    return None


def rule_label(slug: str, kind: str) -> str:
    # rule-2-116 -> "MCR 2.116" ; rule-803 -> "MRE 803"
    m = re.match(r"rule-(\d+)-(.+)$", slug)
    if m:
        return f"MCR {m.group(1)}.{m.group(2).replace('-', '.')}"
    m = re.match(r"rule-(.+)$", slug)
    return f"MRE {m.group(1).replace('-', '.')}" if m else slug


def extract_rule_text(html: str) -> str:
    """Return the verbatim text of the `rule-text` div as Markdown-ish text."""
    i = html.find('class="rule-text"')
    if i == -1:
        return ""
    # Advance past the opening tag's '>' so the tag itself doesn't leak in.
    gt = html.find(">", i)
    region = html[gt + 1:] if gt != -1 else html[i:]
    # Cut at the first sibling block that follows the rule text.
    for marker in ('class="summary-content"', 'class="rule-tabs"',
                   'class="rule-footer"', 'id="disqus', "<footer"):
        j = region.find(marker)
        if j != -1:
            region = region[:j]
    region = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", region)
    # Promote list markers / paragraphs to newlines, then strip tags.
    region = re.sub(r"(?i)</p>|<br\s*/?>|</li>|</div>", "\n", region)
    text = re.sub(r"(?s)<[^>]+>", " ", region)
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n[ \t]+", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def fetch_rule(slug: str, kind: str) -> tuple[str, str] | None:
    base_path = ("/michigan/michigan-rules-of-evidence/" if kind == "mre"
                 else "/michigan/michigan-court-rules/")
    html = http_get(BASE + base_path + slug)
    if not html:
        return None
    body = extract_rule_text(html)
    if len(body) < 30:  # nothing substantive
        return None
    return rule_label(slug, kind), body


def make_stub(t: Target) -> str:
    return (
        f"# {t.title}\n\n{STUB_MARKER}\n\n"
        f"- Citation: Michigan Court Rules / Michigan Rules of Evidence\n"
        f"- Canonical: {CANONICAL}\n"
        f"- Status: **pointer stub** — verbatim text not retrieved this run\n"
        f"- Pulled: {date.today().isoformat()}\n\n"
        f"> **Why a stub?** The verbatim text could not be fetched from the "
        f"courtrules.net mirror this run (origin unreachable), and "
        f"courts.michigan.gov serves the rules from bot-gated, hash-rotated asset "
        f"URLs a stdlib client can't resolve. Read the authoritative text at the "
        f"canonical URL above. Re-run `scripts/pull_michigan_rules.py`; the "
        f"`_file_is_stub` guard will replace this stub with the fetched text.\n\n"
        f"## Scope\n\n{t.scope}\n"
    )


def render(t: Target, rules: list[tuple[str, str]]) -> str:
    out = [
        f"# {t.title}", "",
        f"- Citation: Michigan Court Rules / Michigan Rules of Evidence",
        f"- Canonical authority: {CANONICAL}",
        f"- Fetched from: {t.index_url} (courtrules.net mirror)",
        f"- Rules: {len(rules)}",
        f"- Pulled: {date.today().isoformat()}", "",
        "> Verbatim rule text mirrored from courtrules.net. The canonical "
        "publisher is the Michigan Supreme Court (courts.michigan.gov); verify "
        "against the current official text before filing.", "",
        f"## Scope\n\n{t.scope}", "", "---", "",
    ]
    for label, body in rules:
        out += [f"## {label}", "", body, "", "---", ""]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out).rstrip() + "\n")


def _file_is_stub(p: Path) -> bool:
    if not p.exists():
        return True
    try:
        txt = p.read_text(encoding="utf-8")
    except OSError:
        return True
    # Recognize this puller's marker AND the legacy stub phrasing.
    return (STUB_MARKER in txt
            or "pointer stub" in txt.lower()
            or "verbatim text not retrieved" in txt.lower())


def discover_slugs(t: Target) -> list[str]:
    """Return the ordered, de-duplicated rule slugs for a target.

    MRE lists every rule on one index page. MCR is a two-level tree:
    chapter index -> subchapter pages -> rule pages, so walk both levels.
    """
    idx = http_get(t.index_url)
    if not idx:
        return []
    seen: set[str] = set()
    slugs: list[str] = []

    def add(found: list[str]) -> None:
        for s in found:
            if s not in seen:
                seen.add(s)
                slugs.append(s)

    if t.kind == "mcr-chapter":
        subs: list[str] = []
        for sc in re.findall(r'/michigan/michigan-court-rules/(section/subchapter-[\w-]+)', idx):
            if sc not in subs:
                subs.append(sc)
        for sc in subs:
            page = http_get(f"{BASE}/michigan/michigan-court-rules/{sc}")
            if page:
                add(re.findall(t.rule_re, page))
    else:
        add(re.findall(t.rule_re, idx))
    return slugs


def process(t: Target, out_dir: Path, workers: int) -> str:
    """Returns 'verbatim' | 'stub' | 'preserved'."""
    path = out_dir / f"{t.slug}.md"
    slugs = discover_slugs(t)
    rules: list[tuple[str, str]] = []
    if slugs:
        results: dict[str, tuple[str, str]] = {}
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futs = {ex.submit(fetch_rule, s, t.kind): s for s in slugs}
            for fut in as_completed(futs):
                r = fut.result()
                if r:
                    results[futs[fut]] = r
        rules = [results[s] for s in slugs if s in results]  # preserve order

    if rules:
        tmp = path.with_suffix(".md.tmp")
        tmp.write_text(render(t, rules), encoding="utf-8")
        tmp.replace(path)
        print(f"  VERBATIM {t.slug} ({len(rules)}/{len(slugs)} rules)", flush=True)
        return "verbatim"
    if not _file_is_stub(path):
        print(f"  preserved existing verbatim {t.slug}", flush=True)
        return "preserved"
    tmp = path.with_suffix(".md.tmp")
    tmp.write_text(make_stub(t), encoding="utf-8")
    tmp.replace(path)
    print(f"  STUB {t.slug} (rules discovered: {len(slugs)})", flush=True)
    return "stub"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out",
        default="plugins/mi-court-docs/skills/mi-law-references/references/court-rules",
    )
    ap.add_argument("--only", nargs="*", help="Limit to output slugs.")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    only = set(args.only) if args.only else None
    targets = [t for t in TARGETS if not only or t.slug in only]

    counts = {"verbatim": 0, "stub": 0, "preserved": 0}
    for t in targets:
        print(f"Processing {t.slug} ...", flush=True)
        counts[process(t, out_dir, args.workers)] += 1

    mode = ("verbatim" if counts["stub"] == 0 and counts["verbatim"]
            else "stubs" if counts["verbatim"] == 0 else "mixed")
    manifest = {
        "version": "0.2.0",
        "last_pulled": date.today().isoformat(),
        "source": "courtrules.net (mirror); canonical courts.michigan.gov",
        "mode": mode,
        "notes": (
            "Pulled by scripts/pull_michigan_rules.py. Verbatim MCR (ch. 1-4) + "
            "MRE text mirrored from courtrules.net (the official courts.michigan.gov "
            "rules library is bot-gated with hash-rotated asset URLs). Falls back to "
            "canonical-URL pointer stubs when the mirror is unreachable; the "
            "_file_is_stub guard preserves committed verbatim content."
        ),
    }
    (out_dir / "_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Done. {counts} mode={mode}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
