#!/usr/bin/env python3
"""Pull a curated, topic-grouped set of Michigan Compiled Laws (MCL)
sections from the official Michigan Legislature website and convert
each section to verbatim Markdown.

Output: plugins/mi-court-docs/skills/mi-law-references/references/mi-statutes-debt/
One MD file per TOPIC GROUP (e.g. `RJA-limitations.md`,
`RCPA-collection-practices.md`, `MCPA.md`, `garnishment-exemptions.md`),
each containing the verbatim text of the curated sections in that group
under `## MCL 600.XXXX` headings.

## Source

The Michigan Legislature publishes the Michigan Compiled Laws section by
section at:

    https://www.legislature.mi.gov/Laws/MCL?objectName=mcl-<act>-<sec>

e.g. `mcl-600-5701` for MCL 600.5701. (Verified 200 + content, May 2026.)
The page is plain server-rendered HTML — no Cloudflare / bot-fight gate —
so stdlib urllib with a browser User-Agent retrieves it cleanly. The
statute text lives inside `<div class="sectionWrapper">`: an act-name
header in `<div class="excerpt">`, the section number + catchline in an
`<h1 class="h4">`, the body in a run of `<p>` elements, and the amendment
history in a trailing `<div class="editorials">`.

## Curation philosophy

This is a BOUNDED, representative corpus — not an attempt to enumerate
every section of the MCL. Each topic group pulls a small set (typically
5-15) of the key sections a Michigan civil-practice / consumer-debt /
family-law / landlord-tenant drafter reaches for. Where an act is large
(e.g. the Revised Judicature Act, the Elliott-Larsen Civil Rights Act),
the group pulls a representative SAMPLE of anchor sections, not the whole
act.

## Behavior on failure

If an individual section fetch fails, that section is recorded inline as
a `_(could not retrieve ...)_` placeholder rather than aborting the run.
If EVERY section in a topic group fails (e.g. the site is down), the
group file is written as a well-formed pointer stub carrying the
canonical per-section URLs. A `_file_is_stub` regression guard prevents a
failed run from clobbering verbatim content committed by an earlier run.

## Usage

    python3 scripts/pull_michigan_statutes.py
    python3 scripts/pull_michigan_statutes.py --only RJA-limitations MCPA
    python3 scripts/pull_michigan_statutes.py --stubs-only

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

# Per-section URL pattern on the Michigan Legislature site.
SECTION_URL = "https://www.legislature.mi.gov/Laws/MCL?objectName=mcl-{obj}"


# ----------------------------------------------------------------------
# Target catalog — one TopicGroup per output file.
# Each "section" is a (mcl_number, object_slug) pair, where the object
# slug is the `objectName` query value (e.g. "600-5701" for MCL 600.5701,
# "445-251" for MCL 445.251, "37-2101" for MCL 37.2101).
# ----------------------------------------------------------------------

@dataclass
class TopicGroup:
    slug: str            # output filename stem, e.g. "RJA-limitations"
    title: str           # H1 heading / topic label
    blurb: str           # one-line scope descriptor (used in header + stub)
    sections: List[Tuple[str, str]]  # (mcl_number, object_slug)
    canonical_act: str = ""          # act name for the header


def _obj(mcl: str) -> str:
    """Convert an MCL number like '600.5701' to its objectName slug
    '600-5701'."""
    return mcl.replace(".", "-")


def _grp(mcl_numbers: List[str]) -> List[Tuple[str, str]]:
    return [(n, _obj(n)) for n in mcl_numbers]


TARGETS: List[TopicGroup] = [
    TopicGroup(
        "RJA-limitations",
        "Revised Judicature Act — Periods of Limitation",
        "Statutes of limitation for contract, tort, and other civil "
        "actions under the Revised Judicature Act of 1961 (MCL ch. 600).",
        _grp([
            "600.5805",   # injuries to persons/property; tort SOL
            "600.5807",   # contract / specialty SOL (incl. 6-yr written K)
            "600.5809",   # judgments / instruments under seal
            "600.5813",   # residual / personal-actions 6-year catch-all
            "600.5827",   # accrual — general
            "600.5833",   # accrual — payment of money/installment contracts
            "600.5838",   # accrual — malpractice
            "600.5839",   # improvements to real property repose
        ]),
        canonical_act="Revised Judicature Act of 1961 (Act 236 of 1961)",
    ),
    TopicGroup(
        "RJA-summary-proceedings",
        "Revised Judicature Act — Summary Proceedings (Eviction)",
        "Summary proceedings to recover possession of premises — the "
        "Michigan eviction statute under RJA chapter 57 (MCL 600.5701 "
        "et seq.).",
        _grp([
            "600.5701",   # definitions
            "600.5714",   # when person entitled to possession may recover
            "600.5716",   # judgment for possession
            "600.5718",   # writ of restitution
            "600.5720",   # limits/conditions on issuance of writ
            "600.5728",   # money judgment in summary proceedings
            "600.5739",   # appeal
        ]),
        canonical_act="Revised Judicature Act of 1961 (Act 236 of 1961)",
    ),
    TopicGroup(
        "RJA-district-court-jurisdiction",
        "Revised Judicature Act — District Court Jurisdiction",
        "Civil jurisdiction and the $25,000 amount-in-controversy cap of "
        "the Michigan district court (MCL 600.8301), plus small-claims "
        "division provisions.",
        _grp([
            "600.8301",   # civil jurisdiction; $25,000 cap
            "600.8302",   # equitable jurisdiction / ancillary
            "600.8401",   # small claims division — establishment
            "600.8408",   # small claims jurisdictional amount
        ]),
        canonical_act="Revised Judicature Act of 1961 (Act 236 of 1961)",
    ),
    TopicGroup(
        "garnishment-exemptions",
        "Garnishment, Execution & Exemptions",
        "Garnishment procedure, execution against property, and the "
        "schedule of property exempt from levy and sale under the "
        "Revised Judicature Act.",
        _grp([
            "600.4011",   # garnishment — subject property / jurisdiction
            "600.4012",   # periodic garnishment; duration
            "600.4031",   # garnishment procedure
            "600.6023",   # property exempt from levy and sale
            "600.6023a",  # homestead/principal-residence exemption interplay
            "600.6027",   # earnings — exempt portion / federal floor
            "600.6051",   # execution — issuance
        ]),
        canonical_act="Revised Judicature Act of 1961 (Act 236 of 1961)",
    ),
    TopicGroup(
        "comparative-fault",
        "Comparative Fault & Tort Liability",
        "Michigan's modified comparative-fault regime and allocation of "
        "fault in tort actions (MCL 600.2957 - 600.2959).",
        _grp([
            "600.2957",   # allocation of fault among persons
            "600.2958",   # comparative negligence — economic/noneconomic
            "600.2959",   # reduction of damages by comparative fault; >50% bar on noneconomic
        ]),
        canonical_act="Revised Judicature Act of 1961 (Act 236 of 1961)",
    ),
    TopicGroup(
        "RCPA-collection-practices",
        "Regulation of Collection Practices Act (RCPA)",
        "Michigan's mini-FDCPA — the Regulation of Collection Practices "
        "Act (MCL 445.251 et seq.), which reaches first-party creditors "
        "in addition to third-party collectors.",
        _grp([
            "445.251",   # definitions
            "445.252",   # prohibited methods/practices
            "445.253",   # licensee/regulated-person prohibitions
            "445.254",   # rules
            "445.255",   # enforcement / administration
            "445.257",   # remedies; private right of action; treble/statutory damages
        ]),
        canonical_act="Regulation of Collection Practices Act (Act 360 of 1976)",
    ),
    TopicGroup(
        "MCPA",
        "Michigan Consumer Protection Act (MCPA)",
        "A representative sample of the Michigan Consumer Protection Act "
        "(MCL 445.901 et seq.) — definitions, the catalog of prohibited "
        "unfair/deceptive acts, and the private remedy.",
        _grp([
            "445.901",   # short title
            "445.902",   # definitions
            "445.903",   # prohibited unfair/unconscionable/deceptive acts
            "445.911",   # private remedies; class actions; damages
        ]),
        canonical_act="Michigan Consumer Protection Act (Act 331 of 1976)",
    ),
    TopicGroup(
        "ELCRA",
        "Elliott-Larsen Civil Rights Act (ELCRA) — sample",
        "A representative sample of the Elliott-Larsen Civil Rights Act "
        "(MCL 37.2101 et seq.) — Michigan's employment / public-"
        "accommodation antidiscrimination statute.",
        _grp([
            "37.2101",   # short title
            "37.2102",   # recognition of civil right; scope
            "37.2103",   # definitions
            "37.2202",   # employment — prohibited practices
            "37.2801",   # civil action; remedies; damages; attorney fees
        ]),
        canonical_act="Elliott-Larsen Civil Rights Act (Act 453 of 1976)",
    ),
    TopicGroup(
        "UCC-article-9",
        "Uniform Commercial Code — Article 9 (sample)",
        "A representative sample of Michigan's enactment of UCC Article 9 "
        "(Secured Transactions, MCL 440.9101 et seq.) — the chain-of-title "
        "anchor for assigned consumer debt.",
        _grp([
            "440.9101",   # short title
            "440.9102",   # definitions
            "440.9203",   # attachment / enforceability of security interest
            "440.9203",   # (anchor; dup tolerated — dedup below)
            "440.9210",   # request for accounting
            "440.9607",   # collection / enforcement by secured party
        ]),
        canonical_act="Uniform Commercial Code (Act 174 of 1962)",
    ),
    TopicGroup(
        "family-divorce",
        "Divorce — Grounds, Residency & Property",
        "Michigan divorce: no-fault grounds, residency requirement, and "
        "the framework for division of property (MCL 552.6 et seq.).",
        _grp([
            "552.6",     # complaint for divorce; no-fault grounds
            "552.7",     # residency requirement
            "552.9",     # grounds — breakdown of marriage relationship
            "552.9f",    # judgment; division of property
            "552.19",    # division of real and personal estate
            "552.23",    # award from estate of either party; spousal support
        ]),
        canonical_act="Divorce statute (Act 259 of 1909 / RS 1846 ch. 84)",
    ),
    TopicGroup(
        "child-custody-support",
        "Child Custody, Parenting Time & Support",
        "The Child Custody Act best-interest factors (MCL 722.23) and "
        "related custody / parenting-time / support provisions.",
        _grp([
            "722.23",    # "best interests of the child" defined — the 12 factors
            "722.25",    # presumption / burden as between parent and third party
            "722.27",    # custody orders; modification
            "722.27a",   # parenting time
            "722.3",     # (support obligation anchor; dedup if absent)
        ]),
        canonical_act="Child Custody Act of 1970 (Act 91 of 1970)",
    ),
    TopicGroup(
        "landlord-tenant",
        "Landlord-Tenant — Security Deposits & Tenancies",
        "Michigan landlord-tenant statutes — security-deposit handling, "
        "the covenant of fitness/repair, and termination of tenancies "
        "(MCL 554.601 et seq. and MCL 554.134).",
        _grp([
            "554.602",   # security deposit — maximum amount
            "554.603",   # security deposit — notice of forwarding address
            "554.604",   # security deposit — separate accounting / bond
            "554.609",   # itemized list of damages
            "554.611",   # tenant remedy for retained deposit
            "554.613",   # damages; double-deposit penalty
            "554.139",   # covenant of fitness / reasonable repair
            "554.134",   # termination of estate at will / notice to quit
        ]),
        canonical_act="Landlord-Tenant Relationships (Act 348 of 1972) / "
                      "RS 1846 ch. 66",
    ),
    TopicGroup(
        "holidays",
        "Legal Holidays",
        "Michigan's public-holiday statute — used by the case-calendar "
        "deadline arithmetic (MCL 435.101 et seq.).",
        _grp([
            "435.101",   # public holidays — bills, checks, notes; courts
            "435.102",   # designation of holidays
        ]),
        canonical_act="Public Holidays (Act 261 of 1865 et al.)",
    ),
]


# ----------------------------------------------------------------------
# HTTP.
# ----------------------------------------------------------------------

def http_get(url: str, *, retries: int = 4, base_sleep: float = 1.0,
             timeout: float = 60.0) -> bytes:
    """Fetch a URL with jittered exponential-backoff retries.

    The Michigan Legislature site serves plain HTML over stdlib urllib
    with a browser User-Agent (no Cloudflare bot-fight gate observed).
    A terminal 401/403/404 is raised immediately so the caller can fall
    through to the per-section placeholder / stub path without waiting on
    retries it can't recover from. Transient errors (5xx, resets,
    timeouts) are retried with jittered backoff."""
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
# HTML → Markdown for a single MCL section page.
# ----------------------------------------------------------------------

SECTION_WRAPPER_RE = re.compile(
    r'<div\b[^>]*\bclass="sectionWrapper"[^>]*>(.*)',
    re.DOTALL | re.IGNORECASE,
)
H4_RE = re.compile(
    r'<h1\b[^>]*\bclass="h4"[^>]*>(.*?)</h1>',
    re.DOTALL | re.IGNORECASE,
)
EDITORIALS_RE = re.compile(
    r'<div\b[^>]*\bclass="editorials[^"]*"[^>]*>(.*?)</div>',
    re.DOTALL | re.IGNORECASE,
)
EXCERPT_RE = re.compile(
    r'<div\b[^>]*\bclass="excerpt"[^>]*>(.*?)</div>',
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
        # Keep leading subsection markers like "(a)"; just trim the edges.
        para = "\n".join(ln.strip() for ln in para.splitlines())
        para = para.strip()
        if para:
            lines.append(para)
    return "\n\n".join(lines)


def parse_section_page(html_text: str) -> Tuple[str, str, str, str]:
    """Return (catchline, body_md, history, act_name) for one section
    page. Any field may be '' if not present."""
    wm = SECTION_WRAPPER_RE.search(html_text)
    wrapper = wm.group(1) if wm else html_text
    # SECTION_WRAPPER_RE captures greedily to end-of-document, so the
    # page footer (Acceptable Use Policy / Privacy Policy / Site Map /
    # the Legislative Service Bureau disclaimer) trails the real statute
    # text. Truncate at the first post-content sentinel so chrome never
    # leaks into the last section. `</main>` is the reliable boundary;
    # the footer link block is a defensive secondary cut.
    for sentinel in ("</main>", "<footer", "Acceptable Use Policy"):
        idx = wrapper.find(sentinel)
        if idx != -1:
            wrapper = wrapper[:idx]
            break

    # Act name (from the excerpt header), e.g. "REVISED JUDICATURE ACT
    # OF 1961 (EXCERPT) / Act 236 of 1961".
    act_name = ""
    em = EXCERPT_RE.search(wrapper)
    if em:
        act_name = re.sub(r"\s+", " ", _tags_to_text(em.group(1))).strip()

    # Catchline: the h4 (e.g. "600.5701 Definitions.").
    catchline = ""
    hm = H4_RE.search(wrapper)
    if hm:
        catchline = re.sub(r"\s+", " ",
                           html.unescape(re.sub(r"<[^>]+>", "",
                                                hm.group(1)))).strip()

    # History (editorials div) — capture before stripping it from body.
    history = ""
    edm = EDITORIALS_RE.search(wrapper)
    if edm:
        history = re.sub(r"\s+", " ", _tags_to_text(edm.group(1))).strip()
        # The editorials block already opens with a bold "History:"
        # label; strip it so the rendered "*History:* ..." prefix isn't
        # doubled ("*History:* History: ...").
        history = re.sub(r"^History:\s*", "", history)

    # Body: everything in the wrapper minus the excerpt header, the h4,
    # and the editorials block.
    body_src = wrapper
    if em:
        body_src = body_src.replace(em.group(0), "", 1)
    if hm:
        body_src = body_src.replace(hm.group(0), "", 1)
    if edm:
        body_src = body_src.replace(edm.group(0), "", 1)
    body_md = _tags_to_text(body_src)
    # Drop a leading bare "Sec. NNNN." line — it's redundant with the
    # catchline heading.
    body_md = re.sub(r"^\s*Sec\.\s*[\w.]+\.\s*\n+", "", body_md)
    return catchline, body_md.strip(), history, act_name


# ----------------------------------------------------------------------
# Render.
# ----------------------------------------------------------------------

HEADER = """# {title} — Michigan Compiled Laws

> **Scope:** {blurb}
> **Act:** {act}
> **Source:** Michigan Legislature — {sample_url}
> **Fetched:** {fetched}
> **Format:** verbatim conversion of the Michigan Legislature per-section
> HTML at `legislature.mi.gov/Laws/MCL?objectName=mcl-<act>-<sec>`.

> **NOT LEGAL ADVICE.** Generated content is a drafting aid; verify
> against the current Michigan Compiled Laws before filing.

---

"""


@dataclass
class SectionResult:
    mcl: str
    obj: str
    catchline: str = ""
    body: str = ""
    history: str = ""
    act: str = ""
    ok: bool = False
    error: str = ""


def render_group_md(group: TopicGroup, fetched_iso: str,
                    results: List[SectionResult]) -> str:
    act = group.canonical_act or next(
        (r.act for r in results if r.ok and r.act), ""
    )
    sample_url = SECTION_URL.format(obj=group.sections[0][1])
    parts: List[str] = [HEADER.format(
        title=group.title, blurb=group.blurb, act=act or "(see sections)",
        sample_url=sample_url, fetched=fetched_iso,
    )]
    for r in results:
        heading = r.catchline.strip() or r.mcl
        # Ensure the heading starts with the MCL number for grep-ability.
        if not heading.startswith(r.mcl.split(".")[0]):
            heading = f"{r.mcl} {heading}"
        parts.append(f"## MCL {heading}\n")
        if r.ok:
            parts.append(r.body if r.body else "_(no section body extracted)_")
            if r.history:
                parts.append(f"\n*History:* {r.history}")
        else:
            url = SECTION_URL.format(obj=r.obj)
            parts.append(f"_(could not retrieve — see {url} — {r.error})_")
        parts.append("")  # blank line between sections
    out = "\n".join(parts)
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out.rstrip() + "\n"


def render_stub(group: TopicGroup, fetched_iso: str, reason: str) -> str:
    lines = [
        f"# {group.title} — Michigan Compiled Laws\n",
        f"> **Scope:** {group.blurb}",
        f"> **Act:** {group.canonical_act or '(multiple)'}",
        f"> **Canonical source:** Michigan Legislature "
        f"(`legislature.mi.gov/Laws/MCL`)",
        f"> **Fetched:** {fetched_iso}",
        f"> **Status:** _(stub — verbatim text not retrieved)_ — {reason}",
        f"> **Format:** pointer stub\n",
        "> **NOT LEGAL ADVICE.** This file is a pointer to the canonical "
        "source; verify against the current Michigan Compiled Laws before "
        "filing.\n",
        "---\n",
        "## Curated sections\n",
        "Re-run `scripts/pull_michigan_statutes.py --only "
        f"{group.slug}` from a network where the Michigan Legislature "
        "site is reachable to fill in verbatim text. The same script "
        "replaces this stub on success.\n",
    ]
    for mcl, obj in group.sections:
        url = SECTION_URL.format(obj=obj)
        lines.append(f"- **MCL {mcl}** — {url}")
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

    # Dedup sections (the catalog tolerates accidental dups for clarity).
    seen = set()
    sections: List[Tuple[str, str]] = []
    for mcl, obj in group.sections:
        if obj in seen:
            continue
        seen.add(obj)
        sections.append((mcl, obj))

    results: List[SectionResult] = []
    for mcl, obj in sections:
        url = SECTION_URL.format(obj=obj)
        r = SectionResult(mcl=mcl, obj=obj)
        try:
            data = http_get(url)
            catchline, body, history, act = parse_section_page(
                data.decode("utf-8", errors="replace")
            )
            if not body and not catchline:
                r.error = "no content extracted (layout change?)"
            else:
                r.catchline, r.body, r.history, r.act = (
                    catchline, body, history, act
                )
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
        "source": "https://www.legislature.mi.gov/Laws/MCL",
        "notes": (
            "Pulled by scripts/pull_michigan_statutes.py. The Michigan "
            "Legislature publishes the Michigan Compiled Laws section by "
            "section as plain HTML at "
            "legislature.mi.gov/Laws/MCL?objectName=mcl-<act>-<sec> — no "
            "Cloudflare bot-fight gate, so stdlib urllib with a browser "
            "User-Agent retrieves it. Statute text lives inside "
            "<div class=\"sectionWrapper\"> (excerpt act-name header, an "
            "<h1 class=\"h4\"> catchline, <p> body, and an editorials "
            "History block). This is a curated, topic-grouped, BOUNDED "
            "corpus (one MD file per topic, 5-15 representative sections "
            "each) rather than a full enumeration of the MCL. Failed "
            "sections are recorded inline; a topic file becomes a "
            "well-formed pointer stub only if every section in it fails. "
            "A _file_is_stub regression guard prevents a failed run from "
            "clobbering committed verbatim content."
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
            "plugins/mi-court-docs/skills/mi-law-references/"
            "references/mi-statutes-debt"
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
    print(f"=== pulling {len(groups)} MI topic group(s) → {out_dir} "
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

    # Hard-fail only if EVERY group is a stub on a non-stubs-only run
    # (i.e. the site is fully unreachable) — partial failures are fine.
    if not args.stubs_only and stubs == len(ordered) and len(ordered) > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
