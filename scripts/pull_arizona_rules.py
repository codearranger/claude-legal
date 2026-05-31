#!/usr/bin/env python3
"""Pull the Arizona court rules — Arizona Rules of Civil Procedure
(Ariz. R. Civ. P.), Arizona Rules of Evidence (Ariz. R. Evid.), Arizona
Rules of Family Law Procedure (ARFLP), and the Justice Court Rules of
Civil Procedure (JCRCP).

Output: plugins/az-court-docs/skills/az-law-references/references/court-rules/

The canonical publisher is the Arizona Supreme Court (azcourts.gov /
govt.westlaw.com Arizona Court Rules), but that library is Cloudflare-
gated and a stdlib client can't resolve it. This puller therefore mirrors
from **courtrules.net**, a structured free aggregator that publishes each
rule at a stable URL with the verbatim text in a `rule-text` div — the
same "official-source-gated, use the structured free mirror" pattern the
Michigan rules puller uses. The manifest + per-file headers record the
mirror as the fetch source and azcourts.gov as the canonical authority.

Structure on courtrules.net (verified May 2026):
  - rule-set index   : /arizona/<set>
  - section page     : /arizona/<set>/section/<slug>   (two-level sets)
  - rule page        : /arizona/<set>/rule-<num>
  - verbatim text    : <div class="rule-text"> ... </div> on each rule page

Some sets (Evidence, Justice Court Civil) list every rule directly on the
index page (one level); others (Civil Procedure, Family Law) interpose a
layer of `section/` pages. This puller collects rule slugs from BOTH the
index and any discovered section pages, so it handles either shape.

When the mirror does NOT carry a rule set, or is unreachable, the puller
writes a well-formed pointer stub carrying the canonical azcourts.gov URL
+ a scope description. The `_file_is_stub` regression guard means a
stub-only re-run will NOT clobber verbatim content a prior successful run
committed.
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
STUB_MARKER = "<!-- claude-legal:az-rules-pointer-stub -->"


@dataclass
class Target:
    slug: str               # output filename (no .md)
    title: str              # H1
    cite: str               # citation label, e.g. "Ariz. R. Civ. P."
    set_slug: str           # courtrules.net path segment, e.g. "az-civil-procedure"
    canonical: str          # canonical azcourts.gov URL
    scope: str              # for the stub


TARGETS: list[Target] = [
    Target(
        "ARCP-civil-procedure",
        "Arizona Rules of Civil Procedure (Ariz. R. Civ. P.)",
        "Ariz. R. Civ. P.",
        "az-civil-procedure",
        "https://www.azcourts.gov/rules/Recent-Amendments/"
        "Rules-of-Civil-Procedure",
        "Ariz. R. Civ. P. 1-86 — scope and one form of action, "
        "commencement and service (Rules 3-4.2), pleadings and motions "
        "(Rules 7-16), parties (Rules 17-25), disclosure and discovery "
        "(Rules 26-37, including the Arizona mandatory-initial-disclosure "
        "regime under Rule 26.1), trials (Rules 38-53), judgment "
        "(Rules 54-63, summary judgment under Rule 56, relief from "
        "judgment under Rule 60), provisional and final remedies, "
        "compulsory arbitration (Rules 72-77), and general provisions.",
    ),
    Target(
        "Ariz-R-Evid-evidence",
        "Arizona Rules of Evidence (Ariz. R. Evid.)",
        "Ariz. R. Evid.",
        "az-evidence",
        "https://www.azcourts.gov/rules/Recent-Amendments/"
        "Rules-of-Evidence",
        "Ariz. R. Evid. 101-1103 — relevance (401-403), hearsay "
        "(801-807, business-records exception 803(6)), authentication "
        "(901-902), opinion and expert testimony (701-706), and "
        "privileges.",
    ),
    Target(
        "ARFLP-family-law-procedure",
        "Arizona Rules of Family Law Procedure (ARFLP)",
        "Ariz. R. Fam. Law P.",
        "az-family-law",
        "https://www.azcourts.gov/rules/Recent-Amendments/"
        "Rules-of-Family-Law-Procedure",
        "Arizona Rules of Family Law Procedure — scope and definitions, "
        "commencement and service, pleadings and motions, the mandatory "
        "disclosure regime (Rule 49), temporary orders, alternative "
        "dispute resolution, trial and post-decree procedure for "
        "dissolution, legal decision-making, parenting time, and support "
        "matters.",
    ),
    Target(
        "JCRCP-justice-court",
        "Justice Court Rules of Civil Procedure (JCRCP)",
        "Ariz. JCRCP",
        "az-justice-court-civil",
        "https://www.azcourts.gov/rules/Recent-Amendments/"
        "Justice-Court-Rules-of-Civil-Procedure",
        "Justice Court Rules of Civil Procedure — the streamlined civil "
        "procedure for Arizona justice courts (civil jurisdiction up to "
        "$10,000): commencement, service, answers and default, "
        "limited discovery, motions, trial, judgment and post-judgment "
        "enforcement, and the small-claims division.",
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
    """rule-2-116 -> '<cite> 2.116'; rule-803 -> '<cite> 803';
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
    """Return the verbatim text of the `rule-text` div as Markdown-ish
    text. (Same slice used by the Michigan rules puller.)"""
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


def fetch_rule(set_slug: str, slug: str, cite: str) -> tuple[str, str] | None:
    html = http_get(f"{BASE}/arizona/{set_slug}/{slug}")
    if not html:
        return None
    body = extract_rule_text(html)
    if len(body) < 30:  # nothing substantive
        return None
    return rule_label(slug, cite), body


def make_stub(t: Target, reason: str) -> str:
    return (
        f"# {t.title}\n\n{STUB_MARKER}\n\n"
        f"- Citation: {t.cite}\n"
        f"- Canonical: {t.canonical}\n"
        f"- Status: **pointer stub** — verbatim text not retrieved this run\n"
        f"- Pulled: {date.today().isoformat()}\n\n"
        f"> **Why a stub?** {reason} The canonical publisher "
        f"(azcourts.gov / Arizona Court Rules) is Cloudflare-gated and a "
        f"stdlib client can't resolve it. Read the authoritative text at "
        f"the canonical URL above. Re-run `scripts/pull_arizona_rules.py`; "
        f"the `_file_is_stub` guard will replace this stub with the fetched "
        f"text.\n\n"
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
        "publisher is the Arizona Supreme Court (azcourts.gov); verify "
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
    return (STUB_MARKER in txt
            or "pointer stub" in txt.lower()
            or "verbatim text not retrieved" in txt.lower())


def discover_slugs(t: Target) -> list[str]:
    """Return the ordered, de-duplicated rule slugs for a target.

    Some sets list rules directly on the index page; others interpose a
    layer of `section/` pages. Collect rule slugs from the index AND from
    any discovered section pages, so either shape is handled.
    """
    idx = http_get(f"{BASE}/arizona/{t.set_slug}")
    if not idx:
        return []
    seen: set[str] = set()
    slugs: list[str] = []
    rule_re = rf'/arizona/{re.escape(t.set_slug)}/(rule-[\w-]+)'
    sec_re = rf'/arizona/{re.escape(t.set_slug)}/(section/[\w-]+)'

    def add(found: list[str]) -> None:
        for s in found:
            if s not in seen:
                seen.add(s)
                slugs.append(s)

    # Rules listed directly on the index (one-level sets like Evidence).
    add(re.findall(rule_re, idx))

    # Section pages (two-level sets like Civil Procedure / Family Law).
    subs: list[str] = []
    for sc in re.findall(sec_re, idx):
        if sc not in subs:
            subs.append(sc)
    for sc in subs:
        page = http_get(f"{BASE}/arizona/{t.set_slug}/{sc}")
        if page:
            add(re.findall(rule_re, page))
    return slugs


def process(t: Target, out_dir: Path, workers: int) -> str:
    """Returns 'verbatim' | 'stub' | 'preserved'."""
    path = out_dir / f"{t.slug}.md"
    index_url = f"{BASE}/arizona/{t.set_slug}"
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
        rules = [results[s] for s in slugs if s in results]  # preserve order

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
        default="plugins/az-court-docs/skills/az-law-references/"
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
        "source": "courtrules.net (mirror); canonical azcourts.gov",
        "mode": mode,
        "notes": (
            "Pulled by scripts/pull_arizona_rules.py. Verbatim Ariz. R. "
            "Civ. P. + Ariz. R. Evid. + ARFLP + JCRCP text mirrored from "
            "courtrules.net (the official azcourts.gov / Arizona Court "
            "Rules library is Cloudflare-gated). Handles both one-level "
            "index sets and two-level section-page sets. Falls back to "
            "canonical-URL pointer stubs when the mirror lacks a set or is "
            "unreachable; the _file_is_stub guard preserves committed "
            "verbatim content."
        ),
    }
    (out_dir / "_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Done. {counts} mode={mode}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
