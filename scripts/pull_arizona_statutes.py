#!/usr/bin/env python3
"""Pull a curated, topic-grouped set of Arizona Revised Statutes (A.R.S.)
sections from the official Arizona Legislature website and convert each
section to verbatim Markdown.

Output: plugins/az-court-docs/skills/az-law-references/references/az-statutes-debt/
One MD file per TOPIC GROUP (e.g. `Title12-limitations.md`,
`comparative-fault.md`, `exemptions.md`), each containing the verbatim
text of the curated sections in that group under `## A.R.S. § NN-NNN`
headings.

## Source

The Arizona Legislature publishes the Arizona Revised Statutes section by
section as small, self-contained HTML fragments at:

    https://www.azleg.gov/ars/<title>/<NNNNN>.htm

where `<NNNNN>` is the section number with the integer part zero-padded to
five digits and a decimal suffix rendered with a hyphen — e.g.
`https://www.azleg.gov/ars/12/00548.htm` for A.R.S. § 12-548, and
`https://www.azleg.gov/ars/12/00341-01.htm` for § 12-341.01. (Verified
200 + content, May 2026.) The page is plain server-rendered HTML — no
Cloudflare / bot-fight gate — so stdlib urllib with a browser User-Agent
retrieves it cleanly. (There is also a heavier
`viewdocument/?docName=...` wrapper page that embeds this same fragment
inside the site chrome; the puller uses the lightweight direct `.htm`
fragment instead.)

The fragment layout is:
  - `<TITLE>NN-NNN - Catchline</TITLE>`
  - `<p><font color=GREEN>NN-NNN</font>. <font color=PURPLE><u>Catchline</u></font></p>`
  - a run of `<p>` body paragraphs

## Curation philosophy

This is a BOUNDED, representative corpus — not an attempt to enumerate
every section of the A.R.S. Each topic group pulls a small set (typically
5-15) of the key sections an Arizona civil-practice / consumer-debt /
family-law / landlord-tenant drafter reaches for.

## Behavior on failure

If an individual section fetch fails, that section is recorded inline as a
`_(could not retrieve ...)_` placeholder rather than aborting the run. If
EVERY section in a topic group fails (e.g. the site is down), the group
file is written as a well-formed pointer stub carrying the canonical
per-section URLs. A `_file_is_stub` regression guard prevents a failed run
from clobbering verbatim content committed by an earlier run.

## Usage

    python3 scripts/pull_arizona_statutes.py
    python3 scripts/pull_arizona_statutes.py --only Title12-limitations exemptions
    python3 scripts/pull_arizona_statutes.py --stubs-only

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
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import List, Optional, Tuple

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 "
    "Safari/537.36 claude-legal/1.0"
)

# Per-section URL pattern on the Arizona Legislature site.
SECTION_URL = "https://www.azleg.gov/ars/{title}/{slug}.htm"


# ----------------------------------------------------------------------
# Section-number → URL helpers.
# ----------------------------------------------------------------------

def _section_parts(ars: str) -> Tuple[str, str]:
    """Split an A.R.S. number like '12-341.01' into ('12', '341.01')."""
    title, _, sec = ars.partition("-")
    return title, sec


def _slug(sec: str) -> str:
    """Convert the section part to the URL slug: zero-pad the integer part
    to five digits and render a decimal suffix with a hyphen.
    e.g. '548' -> '00548'; '341.01' -> '00341-01'; '2314.04' -> '02314-04'.
    """
    base, dot, suffix = sec.partition(".")
    out = base.zfill(5)
    if dot:
        out = f"{out}-{suffix}"
    return out


def _url(ars: str) -> str:
    title, sec = _section_parts(ars)
    return SECTION_URL.format(title=title, slug=_slug(sec))


@dataclass
class TopicGroup:
    slug: str            # output filename stem, e.g. "Title12-limitations"
    title: str           # H1 heading / topic label
    blurb: str           # one-line scope descriptor (used in header + stub)
    sections: List[str]  # A.R.S. numbers, e.g. "12-548"
    canonical_act: str = ""


TARGETS: List[TopicGroup] = [
    TopicGroup(
        "Title12-limitations",
        "Title 12 — Periods of Limitation",
        "Statutes of limitation for tort, oral and written contract, and "
        "other civil actions under A.R.S. Title 12, chapter 5.",
        ["12-541", "12-542", "12-543", "12-544", "12-548", "12-550"],
        canonical_act="A.R.S. Title 12 (Courts and Civil Proceedings)",
    ),
    TopicGroup(
        "Title12-procedure-fees",
        "Title 12 — Costs, Attorney Fees & Public-Entity Claims",
        "Costs to the prevailing party, the contested-contract-action "
        "attorney-fee statute, the notice-of-claim and limitations regime "
        "for actions against public entities, and the medical-malpractice "
        "preliminary-expert certification requirement.",
        ["12-341", "12-341.01", "12-821", "12-821.01", "12-2603"],
        canonical_act="A.R.S. Title 12 (Courts and Civil Proceedings)",
    ),
    TopicGroup(
        "comparative-fault",
        "Comparative Fault & Several Liability",
        "Arizona's pure comparative-fault regime (A.R.S. § 12-2505) and the "
        "abolition of joint liability in favor of several liability with "
        "allocation of fault (§ 12-2506).",
        ["12-2505", "12-2506"],
        canonical_act="A.R.S. Title 12, ch. 9, art. 3 (Comparative Fault)",
    ),
    TopicGroup(
        "garnishment-execution",
        "Garnishment & Execution",
        "Writs of garnishment of earnings and of monies/property, the "
        "continuing-lien framework, and execution / judgment-enforcement "
        "provisions under A.R.S. Title 12.",
        ["12-1551", "12-1570", "12-1598", "12-1611", "12-1612"],
        canonical_act="A.R.S. Title 12, ch. 8 (Special Actions and "
                      "Proceedings Relating to Property)",
    ),
    TopicGroup(
        "exemptions",
        "Exemptions — Homestead, Personal Property & Wages",
        "The Arizona homestead exemption and the schedules of personal "
        "property, household goods, and earnings exempt from process under "
        "A.R.S. Title 33, chapter 8.",
        ["33-1101", "33-1121", "33-1123", "33-1126", "33-1131"],
        canonical_act="A.R.S. Title 33, ch. 8 (Homestead and Personal "
                      "Property Exemption)",
    ),
    TopicGroup(
        "landlord-tenant",
        "Landlord-Tenant — Residential & Forcible Detainer",
        "The Arizona Residential Landlord and Tenant Act (A.R.S. Title 33, "
        "ch. 10) — scope, security deposits, nonpayment / noncompliance "
        "termination, the special-detainer remedy — plus the Title 12 "
        "forcible-entry-and-detainer cause of action.",
        ["33-1301", "33-1321", "33-1368", "33-1377", "33-1381", "12-1171"],
        canonical_act="A.R.S. Title 33, ch. 10 (Residential Landlord and "
                      "Tenant Act); A.R.S. Title 12, ch. 8 (FED)",
    ),
    TopicGroup(
        "consumer-fraud-collection",
        "Consumer Fraud & Collection-Agency Regulation",
        "The Arizona Consumer Fraud Act definitions and prohibited "
        "practices (A.R.S. Title 44, ch. 10, art. 7) and the "
        "collection-agency licensing regime under A.R.S. Title 32, "
        "ch. 9.",
        ["44-1521", "44-1522", "32-1001", "32-1021", "32-1055"],
        canonical_act="A.R.S. Title 44, ch. 10 (Consumer Fraud); A.R.S. "
                      "Title 32, ch. 9 (Collection Agencies)",
    ),
    TopicGroup(
        "family-Title25",
        "Title 25 — Marital Dissolution, Custody & Support",
        "Arizona community-property and family-law anchors: the "
        "community-property presumption, dissolution petition / decree "
        "framework, spousal maintenance, division of property, legal "
        "decision-making and parenting time, child support, and the "
        "Uniform Parentage Act.",
        ["25-211", "25-312", "25-318", "25-319", "25-320", "25-329",
         "25-401", "25-403", "25-408", "25-901", "25-903"],
        canonical_act="A.R.S. Title 25 (Marital and Domestic Relations)",
    ),
    TopicGroup(
        "justice-court",
        "Justice Courts — Civil Jurisdiction & Procedure",
        "Justice-court civil jurisdiction (the $10,000 amount-in-"
        "controversy cap), venue, the small-claims division, and "
        "appeal to superior court under A.R.S. Title 22.",
        ["22-201", "22-261", "22-503", "22-519"],
        canonical_act="A.R.S. Title 22 (Justice and Municipal Courts)",
    ),
    TopicGroup(
        "employment",
        "Employment — Wages, Discrimination & Workers' Compensation",
        "Arizona wage-payment and recovery remedies (treble damages for "
        "withheld wages), the workers'-compensation exclusive remedy, the "
        "Employment Protection Act, and the existence of the Arizona Civil "
        "Rights Act employment-discrimination definitions.",
        ["23-355", "23-363", "23-1022", "23-1501", "41-1461"],
        canonical_act="A.R.S. Title 23 (Labor); A.R.S. Title 41, ch. 9, "
                      "art. 4 (Arizona Civil Rights Act)",
    ),
    TopicGroup(
        "commercial",
        "Commercial — UCC, Antitrust, RICO & LLC",
        "Commercial-litigation anchors: the UCC statute of limitations for "
        "contracts of sale, the Arizona Uniform State Antitrust Act, the "
        "civil-RICO private cause of action, and the existence of the "
        "Arizona Limited Liability Company Act.",
        ["44-401", "44-1001", "47-2725", "29-3101", "13-2314.04"],
        canonical_act="A.R.S. Title 44 / Title 47 (UCC) / Title 29 (LLC) / "
                      "Title 13 (RICO)",
    ),
    TopicGroup(
        "holidays",
        "Legal Holidays",
        "Arizona's enumerated legal holidays — used by the case-calendar "
        "deadline arithmetic (A.R.S. § 1-301).",
        ["1-301"],
        canonical_act="A.R.S. Title 1 (General Provisions)",
    ),
]


# ----------------------------------------------------------------------
# HTTP.
# ----------------------------------------------------------------------

def http_get(url: str, *, retries: int = 4, base_sleep: float = 1.0,
             timeout: float = 60.0) -> bytes:
    """Fetch a URL with jittered exponential-backoff retries.

    The Arizona Legislature site serves plain HTML over stdlib urllib with
    a browser User-Agent (no Cloudflare bot-fight gate observed). A
    terminal 401/403/404 is raised immediately so the caller can fall
    through to the per-section placeholder / stub path without waiting on
    retries it can't recover from. Transient errors (5xx, resets, timeouts)
    are retried with jittered backoff."""
    parsed = urllib.parse.urlsplit(url)
    safe_path = urllib.parse.quote(parsed.path, safe="/%():'.,")
    safe_url = urllib.parse.urlunsplit(
        (parsed.scheme, parsed.netloc, safe_path,
         parsed.query, parsed.fragment)
    )
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;"
                  "q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    req = urllib.request.Request(safe_url, headers=headers)
    last_exc: Optional[BaseException] = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            if e.code in (401, 403, 404):
                raise
            last_exc = e
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last_exc = e
        except Exception as e:  # noqa: BLE001
            last_exc = e
        time.sleep(base_sleep * (2 ** attempt) * (0.5 + random.random()))
    assert last_exc is not None
    raise last_exc


# ----------------------------------------------------------------------
# HTML → Markdown for a single A.R.S. section fragment.
# ----------------------------------------------------------------------

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.DOTALL | re.IGNORECASE)
BODY_RE = re.compile(r"<body[^>]*>(.*?)</body>", re.DOTALL | re.IGNORECASE)
# The catchline paragraph: <p>...<font color=GREEN>NN-NNN</font>...</p>
HEAD_P_RE = re.compile(
    r"<p\b[^>]*>\s*<font[^>]*color=?\"?GREEN\"?[^>]*>.*?</p>",
    re.DOTALL | re.IGNORECASE,
)


def _tags_to_text(chunk: str) -> str:
    """Strip HTML tags to plain text, collapsing nbsp and whitespace but
    preserving paragraph breaks (one blank line between <p> blocks)."""
    s = re.sub(r"<script\b[^>]*>.*?</script>", "", chunk,
               flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r"<style\b[^>]*>.*?</style>", "", s,
               flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.IGNORECASE)
    s = re.sub(r"<p\b[^>]*>", "\n\n", s, flags=re.IGNORECASE)
    s = re.sub(r"</p>", "", s, flags=re.IGNORECASE)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    s = s.replace("\xa0", " ")
    lines = []
    for para in re.split(r"\n\s*\n", s):
        para = re.sub(r"[ \t]+", " ", para)
        para = "\n".join(ln.strip() for ln in para.splitlines())
        para = para.strip()
        if para:
            lines.append(para)
    return "\n\n".join(lines)


def parse_section_page(html_text: str, ars: str) -> Tuple[str, str]:
    """Return (catchline, body_md) for one A.R.S. section fragment.

    The catchline comes from the <TITLE> ("NN-NNN - Catchline"); the body
    is every <p> after the leading green/purple catchline paragraph."""
    catchline = ""
    tm = TITLE_RE.search(html_text)
    if tm:
        raw = re.sub(r"\s+", " ",
                     html.unescape(re.sub(r"<[^>]+>", "", tm.group(1)))).strip()
        # Title is "NN-NNN - Catchline"; drop the leading number for a clean
        # catchline (the heading is rebuilt with the number for grep-ability).
        m = re.match(r"^\s*[\d.\-]+\s*-\s*(.*)$", raw)
        catchline = (m.group(1).strip() if m else raw)

    bm = BODY_RE.search(html_text)
    body_src = bm.group(1) if bm else html_text
    # Drop the leading catchline paragraph (green section number + purple
    # underlined catchline) so it isn't duplicated under the heading.
    body_src = HEAD_P_RE.sub("", body_src, count=1)
    body_md = _tags_to_text(body_src)
    # Drop a leading bare repeat of "NN-NNN." if it survived.
    body_md = re.sub(rf"^\s*{re.escape(ars)}\.?\s*\n+", "", body_md)
    return catchline, body_md.strip()


# ----------------------------------------------------------------------
# Render.
# ----------------------------------------------------------------------

HEADER = """# {title} — Arizona Revised Statutes

> **Scope:** {blurb}
> **Title/Act:** {act}
> **Source:** Arizona Legislature — {sample_url}
> **Fetched:** {fetched}
> **Format:** verbatim conversion of the Arizona Legislature per-section
> HTML fragments at `azleg.gov/ars/<title>/<NNNNN>.htm`.

> **NOT LEGAL ADVICE.** Generated content is a drafting aid; verify
> against the current Arizona Revised Statutes before filing.

---

"""


@dataclass
class SectionResult:
    ars: str
    catchline: str = ""
    body: str = ""
    ok: bool = False
    error: str = ""


def render_group_md(group: TopicGroup, fetched_iso: str,
                    results: List[SectionResult]) -> str:
    sample_url = _url(group.sections[0])
    parts: List[str] = [HEADER.format(
        title=group.title, blurb=group.blurb,
        act=group.canonical_act or "(see sections)",
        sample_url=sample_url, fetched=fetched_iso,
    )]
    for r in results:
        heading = f"A.R.S. § {r.ars}"
        if r.catchline:
            heading = f"{heading}. {r.catchline}"
        parts.append(f"## {heading}\n")
        if r.ok:
            parts.append(r.body if r.body else "_(no section body extracted)_")
        else:
            parts.append(f"_(could not retrieve — see {_url(r.ars)} "
                         f"— {r.error})_")
        parts.append("")  # blank line between sections
    out = "\n".join(parts)
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out.rstrip() + "\n"


def render_stub(group: TopicGroup, fetched_iso: str, reason: str) -> str:
    lines = [
        f"# {group.title} — Arizona Revised Statutes\n",
        f"> **Scope:** {group.blurb}",
        f"> **Title/Act:** {group.canonical_act or '(multiple)'}",
        f"> **Canonical source:** Arizona Legislature (`azleg.gov/ars`)",
        f"> **Fetched:** {fetched_iso}",
        f"> **Status:** _(stub — verbatim text not retrieved)_ — {reason}",
        f"> **Format:** pointer stub\n",
        "> **NOT LEGAL ADVICE.** This file is a pointer to the canonical "
        "source; verify against the current Arizona Revised Statutes before "
        "filing.\n",
        "---\n",
        "## Curated sections\n",
        "Re-run `scripts/pull_arizona_statutes.py --only "
        f"{group.slug}` from a network where the Arizona Legislature site "
        "is reachable to fill in verbatim text. The same script replaces "
        "this stub on success.\n",
    ]
    for ars in group.sections:
        lines.append(f"- **A.R.S. § {ars}** — {_url(ars)}")
    return "\n".join(lines) + "\n"


# ----------------------------------------------------------------------
# Regression guard + writing.
# ----------------------------------------------------------------------

def _file_is_stub(path: Path) -> bool:
    try:
        head = path.read_text(encoding="utf-8")[:1024]
    except Exception:  # noqa: BLE001
        return True
    return "Format:** pointer stub" in head or "(stub" in head


@dataclass
class WriteResult:
    slug: str
    path: Path
    bytes_written: int
    ok_sections: int
    total_sections: int
    error: Optional[str]
    stub: bool


def fetch_group(group: TopicGroup, out_dir: Path, fetched_iso: str,
                stubs_only: bool = False) -> WriteResult:
    out_path = out_dir / f"{group.slug}.md"

    if stubs_only:
        rendered = render_stub(group, fetched_iso, "--stubs-only forced")
        tmp = out_path.with_suffix(".md.tmp")
        tmp.write_text(rendered, encoding="utf-8")
        tmp.rename(out_path)
        return WriteResult(group.slug, out_path, out_path.stat().st_size,
                           0, len(group.sections), None, stub=True)

    # Dedup sections, preserving order.
    seen = set()
    sections: List[str] = []
    for ars in group.sections:
        if ars in seen:
            continue
        seen.add(ars)
        sections.append(ars)

    results: List[SectionResult] = []
    for ars in sections:
        r = SectionResult(ars=ars)
        try:
            data = http_get(_url(ars))
            catchline, body = parse_section_page(
                data.decode("utf-8", errors="replace"), ars
            )
            if not body and not catchline:
                r.error = "no content extracted (layout change?)"
            else:
                r.catchline, r.body = catchline, body
                r.ok = True
        except urllib.error.HTTPError as e:
            r.error = f"HTTP {e.code}"
        except Exception as e:  # noqa: BLE001
            r.error = f"{type(e).__name__}: {e}"
        results.append(r)
        time.sleep(0.2 + random.random() * 0.3)

    ok = sum(1 for r in results if r.ok)

    # If NOTHING came back, fall back to a stub (with regression guard).
    if ok == 0:
        if out_path.exists() and not _file_is_stub(out_path):
            return WriteResult(
                group.slug, out_path, out_path.stat().st_size,
                0, len(sections),
                "all sections failed (kept existing verbatim file)",
                stub=False,
            )
        rendered = render_stub(group, fetched_iso,
                               "all curated sections failed to fetch")
        tmp = out_path.with_suffix(".md.tmp")
        tmp.write_text(rendered, encoding="utf-8")
        tmp.rename(out_path)
        return WriteResult(group.slug, out_path, out_path.stat().st_size,
                           0, len(sections),
                           "all sections failed", stub=True)

    rendered = render_group_md(group, fetched_iso, results)
    tmp = out_path.with_suffix(".md.tmp")
    tmp.write_text(rendered, encoding="utf-8")
    tmp.rename(out_path)
    err = None if ok == len(sections) else f"{len(sections) - ok} section(s) failed"
    return WriteResult(group.slug, out_path, out_path.stat().st_size,
                       ok, len(sections), err, stub=False)


# ----------------------------------------------------------------------
# Manifest.
# ----------------------------------------------------------------------

def update_manifest(out_dir: Path, fetched_iso: str, mode: str,
                    version: str = "0.1.0") -> Path:
    manifest_path = out_dir / "_manifest.json"
    payload = {
        "version": version,
        "last_pulled": fetched_iso,
        "mode": mode,
        "source": "https://www.azleg.gov/ars",
        "notes": (
            "Pulled by scripts/pull_arizona_statutes.py. The Arizona "
            "Legislature publishes the Arizona Revised Statutes section by "
            "section as plain HTML fragments at "
            "azleg.gov/ars/<title>/<NNNNN>.htm (integer part zero-padded to "
            "five digits; decimal suffix rendered with a hyphen) — no "
            "Cloudflare bot-fight gate, so stdlib urllib with a browser "
            "User-Agent retrieves it. Each fragment carries the catchline in "
            "<TITLE> and a green/purple catchline <p> followed by the body "
            "<p> run. This is a curated, topic-grouped, BOUNDED corpus (one "
            "MD file per topic, 5-15 representative sections each) rather "
            "than a full enumeration of the A.R.S. Failed sections are "
            "recorded inline; a topic file becomes a well-formed pointer "
            "stub only if every section in it fails. A _file_is_stub "
            "regression guard prevents a failed run from clobbering "
            "committed verbatim content."
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
        "--out", type=Path,
        default=Path(
            "plugins/az-court-docs/skills/az-law-references/"
            "references/az-statutes-debt"
        ),
        help="Output directory for the corpus.",
    )
    ap.add_argument("--only", nargs="*",
                    help="Restrict to these topic-group slugs.")
    ap.add_argument("--workers", type=int, default=4,
                    help="Concurrent topic-group fetches (default 4).")
    ap.add_argument("--stubs-only", action="store_true",
                    help="Write pointer stubs only — no network fetch.")
    ap.add_argument("--manifest-version", default="0.1.0")
    args = ap.parse_args()

    out_dir: Path = args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    only = set(args.only) if args.only else None
    groups = [g for g in TARGETS if only is None or g.slug in only]
    if not groups:
        print(f"!! no targets match --only {args.only!r}", file=sys.stderr)
        return 2

    fetched_iso = date.today().isoformat()
    print(f"=== pulling {len(groups)} AZ topic group(s) → {out_dir} "
          f"(workers={args.workers}, stubs_only={args.stubs_only})",
          flush=True)

    results: List[WriteResult] = []
    workers = max(1, min(args.workers, len(groups)))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(fetch_group, g, out_dir, fetched_iso,
                        args.stubs_only): g
            for g in groups
        }
        for fut in as_completed(futures):
            g = futures[fut]
            try:
                results.append(fut.result())
            except Exception as exc:  # noqa: BLE001
                results.append(WriteResult(
                    g.slug, out_dir / f"{g.slug}.md", 0, 0,
                    len(g.sections), str(exc), stub=True,
                ))

    by_slug = {r.slug: r for r in results}
    ordered = [by_slug[g.slug] for g in groups if g.slug in by_slug]
    for r in ordered:
        tag = ("STUB" if r.stub else
               "OK  " if r.error is None else "PART")
        print(f"     [{tag}] {r.slug}.md ({r.bytes_written:,} bytes, "
              f"{r.ok_sections}/{r.total_sections} sections)"
              + (f" — {r.error}" if r.error else ""), flush=True)

    verbatim = sum(1 for r in ordered if not r.stub)
    stubs = sum(1 for r in ordered if r.stub)
    total_bytes = sum(r.bytes_written for r in ordered)
    total_ok = sum(r.ok_sections for r in ordered)
    print(f"\n=== wrote {len(ordered)} topic file(s): {verbatim} verbatim, "
          f"{stubs} stub; {total_ok} sections OK; {total_bytes:,} bytes",
          flush=True)

    if only is None:
        mode = "stubs" if args.stubs_only else (
            "verbatim" if stubs == 0 else "mixed"
        )
        mp = update_manifest(out_dir, fetched_iso, mode,
                             args.manifest_version)
        print(f"=== updated {mp}", flush=True)

    # Hard-fail only if EVERY group is a stub on a non-stubs-only run.
    if not args.stubs_only and stubs == len(ordered) and len(ordered) > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
