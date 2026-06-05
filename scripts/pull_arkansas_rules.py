#!/usr/bin/env python3
"""Pull the Arkansas court rules — Arkansas Rules of Civil Procedure
(Ark. R. Civ. P.), Arkansas Rules of Evidence (Ark. R. Evid.), the
Arkansas District Court Rules, and the Rules of the Supreme Court and
Court of Appeals of Arkansas.

Output: plugins/ar-court-docs/skills/ar-law-references/references/court-rules/

The canonical publisher is the Arkansas Judiciary (arcourts.gov — "Rules
of the Supreme Court and Court of Appeals" / Court Rules). The bare rule
text is a public-domain edict of the Arkansas Supreme Court (only the
West/Lexis annotated compilations are copyrighted), but arcourts.gov does
not expose a clean structured copy a stdlib client can resolve, so this
puller mirrors from **courtrules.net**, a structured free aggregator that
publishes each rule at a stable URL with the verbatim text in a
`rule-text` div — the same "official-source-gated, use the structured
free mirror" pattern the Michigan and Arizona rules pullers use. The
manifest + per-file headers record the mirror as the fetch source and
arcourts.gov as the canonical authority.

Structure on courtrules.net:
  - rule-set index   : /arkansas/<set>
  - section page     : /arkansas/<set>/section/<slug>   (two-level sets)
  - rule page        : /arkansas/<set>/rule-<num>
  - verbatim text    : <div class="rule-text"> ... </div> on each rule page

When the mirror does NOT carry a rule set, or is unreachable, the puller
writes a well-formed pointer stub carrying the canonical arcourts.gov URL
+ a scope description. The `_file_is_stub` regression guard means a
stub-only re-run will NOT clobber verbatim content a prior successful run
committed.

NOTE: Arkansas's Administrative Orders (esp. No. 10 child-support
guidelines, No. 19 access to court records, No. 21 electronic filing) are
published as standalone PDFs on arcourts.gov rather than as numbered
rules on the mirror; they are tracked as canonical-URL pointers in the
ar-law-references corpus, not pulled here.
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
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
STUB_MARKER = "<!-- claude-legal:ar-rules-pointer-stub -->"


@dataclass
class Target:
    slug: str               # output filename (no .md)
    title: str              # H1
    cite: str               # citation label, e.g. "Ark. R. Civ. P."
    set_slug: str           # courtrules.net path segment
    canonical: str          # canonical arcourts.gov URL
    scope: str              # for the stub


TARGETS: list[Target] = [
    Target(
        "ARCP-civil-procedure",
        "Arkansas Rules of Civil Procedure (Ark. R. Civ. P.)",
        "Ark. R. Civ. P.",
        "ar-civil-procedure",
        "https://www.arcourts.gov/content/rules-supreme-court-and-court-appeals-state-arkansas",
        "Ark. R. Civ. P. 1-86 — scope (Rule 1), commencement and service "
        "(Rules 3-4, including the 120-day service period under Rule 4(i)), "
        "pleadings and motions (Rules 7-16, with Arkansas's FACT-PLEADING "
        "standard under Rule 8 and the Rule 12 defenses incl. 12(b)(6)), "
        "parties (Rules 17-25), discovery (Rules 26-37, including "
        "interrogatories under Rule 33), trials (Rules 38-53), judgment "
        "(Rules 54-63, summary judgment under Rule 56, new trial under "
        "Rule 59, and relief from judgment under Rule 60 with its 90-day "
        "Rule 60(a) window), and provisional and final remedies. Time "
        "computation is Rule 6, with the Rule 6(d) 3-day mail add-on.",
    ),
    Target(
        "Ark-R-Evid-evidence",
        "Arkansas Rules of Evidence (Ark. R. Evid.)",
        "Ark. R. Evid.",
        "ar-evidence",
        "https://www.arcourts.gov/content/rules-supreme-court-and-court-appeals-state-arkansas",
        "Ark. R. Evid. 101-1102 — relevance (401-403), hearsay (801-806, "
        "the business-records exception 803(6)), authentication (901-902, "
        "self-authenticating certified business records 902(11)), opinion "
        "and expert testimony (701-706), and privileges.",
    ),
    Target(
        "ADCR-district-court",
        "Arkansas District Court Rules",
        "Ark. Dist. Ct. R.",
        "ar-district-court",
        "https://www.arcourts.gov/content/rules-supreme-court-and-court-appeals-state-arkansas",
        "Arkansas District Court Rules — the streamlined civil procedure "
        "for Arkansas district courts (limited civil jurisdiction and the "
        "small-claims division): commencement, service, answers and "
        "default, limited discovery, trial, judgment, and the 30-day de "
        "novo appeal to circuit court under Rule 9.",
    ),
    Target(
        "Ark-Sup-Ct-Ct-App-rules",
        "Rules of the Supreme Court and Court of Appeals of Arkansas",
        "Ark. Sup. Ct. R.",
        "ar-supreme-court",
        "https://www.arcourts.gov/content/rules-supreme-court-and-court-appeals-state-arkansas",
        "Rules of the Supreme Court and Court of Appeals — including "
        "Rule 5-2 (medium-neutral / public-domain citation: 'YEAR Ark. "
        "NNN' and 'YEAR Ark. App. NNN'), publication and citation of "
        "opinions, and appellate briefing.",
    ),
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


def rule_label(slug: str, cite: str) -> str:
    """rule-12 -> '<cite> 12'; rule-803 -> '<cite> 803';
    rule-appendix-1 -> '<cite> Appendix 1'."""
    m = re.match(r"rule-(\d+)-(\d.*)$", slug)
    if m:
        return f"{cite} {m.group(1)}.{m.group(2).replace('-', '.')}"
    m = re.match(r"rule-(\d.*)$", slug)
    if m:
        return f"{cite} {m.group(1).replace('-', '.')}"
    m = re.match(r"rule-(.+)$", slug)
    if m:
        words = " ".join(w.capitalize() for w in m.group(1).split("-"))
        return f"{cite} {words}"
    return slug


def extract_rule_text(html: str) -> str:
    """Return the verbatim text of the `rule-text` div as Markdown-ish text."""
    i = html.find('class="rule-text"')
    if i == -1:
        return ""
    gt = html.find(">", i)
    region = html[gt + 1:] if gt != -1 else html[i:]
    for marker in ('class="summary-content"', 'class="rule-tabs"',
                   'class="rule-footer"', 'id="disqus', "<footer"):
        j = region.find(marker)
        if j != -1:
            region = region[:j]
    region = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", region)
    region = re.sub(r"(?i)</p>|<br\s*/?>|</li>|</div>", "\n", region)
    text = re.sub(r"(?s)<[^>]+>", " ", region)
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n[ \t]+", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def fetch_rule(set_slug: str, slug: str, cite: str) -> tuple[str, str] | None:
    html = http_get(f"{BASE}/arkansas/{set_slug}/{slug}")
    if not html:
        return None
    body = extract_rule_text(html)
    if len(body) < 30:
        return None
    return rule_label(slug, cite), body


def make_stub(t: Target, reason: str) -> str:
    return (
        f"# {t.title}\n\n{STUB_MARKER}\n\n"
        f"- Citation: {t.cite}\n"
        f"- Canonical: {t.canonical}\n"
        f"- Status: **pointer stub** — verbatim text not retrieved this run\n"
        f"- Pulled: {date.today().isoformat()}\n\n"
        f"> **Why a stub?** {reason} Read the authoritative text at the "
        f"canonical Arkansas Judiciary URL above. Re-run "
        f"`scripts/pull_arkansas_rules.py`; the `_file_is_stub` guard will "
        f"replace this stub with the fetched text.\n\n"
        f"## Scope\n\n{t.scope}\n"
    )


def render(t: Target, rules: list[tuple[str, str]], index_url: str) -> str:
    out = [
        f"# {t.title}", "",
        f"- Citation: {t.cite}",
        f"- Canonical authority: {t.canonical}",
        f"- Fetched from: {index_url} (courtrules.net mirror)",
        f"- Rules: {len(rules)}",
        f"- Pulled: {date.today().isoformat()}", "",
        "> Verbatim rule text mirrored from courtrules.net. The canonical "
        "publisher is the Arkansas Judiciary (arcourts.gov); verify against "
        "the current official text before filing.", "",
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
    return (STUB_MARKER in txt
            or "pointer stub" in txt.lower()
            or "verbatim text not retrieved" in txt.lower())


def discover_slugs(t: Target) -> list[str]:
    idx = http_get(f"{BASE}/arkansas/{t.set_slug}")
    if not idx:
        return []
    seen: set[str] = set()
    slugs: list[str] = []
    rule_re = rf'/arkansas/{re.escape(t.set_slug)}/(rule-[\w-]+)'
    sec_re = rf'/arkansas/{re.escape(t.set_slug)}/(section/[\w-]+)'

    def add(found: list[str]) -> None:
        for s in found:
            if s not in seen:
                seen.add(s)
                slugs.append(s)

    add(re.findall(rule_re, idx))
    subs: list[str] = []
    for sc in re.findall(sec_re, idx):
        if sc not in subs:
            subs.append(sc)
    for sc in subs:
        page = http_get(f"{BASE}/arkansas/{t.set_slug}/{sc}")
        if page:
            add(re.findall(rule_re, page))
    return slugs


def process(t: Target, out_dir: Path, workers: int) -> str:
    """Returns 'verbatim' | 'stub' | 'preserved'."""
    path = out_dir / f"{t.slug}.md"
    index_url = f"{BASE}/arkansas/{t.set_slug}"
    slugs = discover_slugs(t)
    rules: list[tuple[str, str]] = []
    if slugs:
        results: dict[str, tuple[str, str]] = {}
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futs = {ex.submit(fetch_rule, t.set_slug, s, t.cite): s
                    for s in slugs}
            for fut in as_completed(futs):
                r = fut.result()
                if r:
                    results[futs[fut]] = r
        rules = [results[s] for s in slugs if s in results]

    if rules:
        tmp = path.with_suffix(".md.tmp")
        tmp.write_text(render(t, rules, index_url), encoding="utf-8")
        tmp.replace(path)
        print(f"  VERBATIM {t.slug} ({len(rules)}/{len(slugs)} rules)",
              flush=True)
        return "verbatim"
    if not _file_is_stub(path):
        print(f"  preserved existing verbatim {t.slug}", flush=True)
        return "preserved"
    reason = ("The courtrules.net mirror did not carry this rule set or was "
              "unreachable this run.")
    tmp = path.with_suffix(".md.tmp")
    tmp.write_text(make_stub(t, reason), encoding="utf-8")
    tmp.replace(path)
    print(f"  STUB {t.slug} (rules discovered: {len(slugs)})", flush=True)
    return "stub"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out",
        default="plugins/ar-court-docs/skills/ar-law-references/"
                "references/court-rules",
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
        "version": "0.1.0",
        "last_pulled": date.today().isoformat(),
        "source": "courtrules.net (mirror); canonical arcourts.gov",
        "mode": mode,
        "notes": (
            "Pulled by scripts/pull_arkansas_rules.py. Verbatim Ark. R. "
            "Civ. P. + Ark. R. Evid. + Arkansas District Court Rules + "
            "Supreme Court/Court of Appeals Rules mirrored from "
            "courtrules.net (arcourts.gov publishes no clean structured "
            "copy a stdlib client can resolve). Falls back to canonical-URL "
            "pointer stubs when the mirror lacks a set or is unreachable; "
            "the _file_is_stub guard preserves committed verbatim content. "
            "Administrative Orders 10/19/21 are tracked as canonical-URL "
            "pointers in the corpus, not pulled here."
        ),
    }
    (out_dir / "_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Done. {counts} mode={mode}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
