#!/usr/bin/env python3
"""Pull selected New York consolidated-laws articles relevant to civil
practice and consumer-debt / landlord-tenant defense, and convert each
law (or chapter / article slice) to verbatim Markdown.

Output: plugins/ny-court-docs/skills/ny-law-references/references/ny-statutes-debt/
One MD file per (lawId, slice) pair, named `<LawID>-<ShortLabel>.md`
(e.g. `CVP-Article-31-Disclosure.md` for CPLR Article 31).

## Source: NY State Senate Open Legislation API

The NY State Legislature publishes the consolidated laws via the
**Open Legislation** REST/JSON API at `legislation.nysenate.gov`. The
API is the canonical machine-readable source for NY statutes — the
NYS Senate maintains it and the NY State Library cross-references it.
Documentation: https://legislation.nysenate.gov/static/docs/html/

  - Index of laws:                https://legislation.nysenate.gov/api/3/laws
  - Get one law tree:             /api/3/laws/{lawId}
  - Get one section / article:    /api/3/laws/{lawId}/{locationId}

The API requires an API key (free, registration-based). Set the
`NYSENATE_API_KEY` env var to enable the JSON path. When the key is
unset (the default, as in CI without secret wiring) the puller writes
**pointer stubs** mirroring `pull_indiana_statutes.py`'s shape — the
corpus still has the right files and shape, the stubs declare the gap
honestly, and the next refresh with a key will replace them with
verbatim text.

## Target catalog

Selected to cover the **same civil-practice surface** as the WA
(`wa-rcw-debt/`), OR (`or-ors-debt/`), CA (`ca-statutes-debt/`), and
CO (`co-statutes-debt/`) corpora — procedure, evidence, fees,
limitations, exemptions, garnishment, family law, landlord-tenant,
consumer-debt, UCC enactment, debt-collection licensing, vulnerable-
adult protection.

  CPLR (lawId=CVP)         — Civil Practice Law and Rules
    Article 1   — Short title; statutory authority
    Article 2   — Limitations of Time
    Article 3   — Jurisdiction and Service of Papers
    Article 21  — Papers
    Article 22  — Stays, Motions, Orders and Mandates
    Article 23  — Subpoenas, Oaths and Affirmations
    Article 30  — Remedies and Pleadings
    Article 31  — Disclosure
    Article 32  — Accelerated Judgment
    Article 33  — Trial Generally
    Article 50  — General Provisions Relating to Judgments
    Article 51  — Enforcement of Judgments and Orders
    Article 52  — Enforcement of Money Judgments
    Article 53  — Recognition of Foreign Country Money Judgments

  General Obligations (lawId=GOB)
    Title 1     — Short title; obligations generally
    Title 5 §17 — Statute of frauds + interest rates
    Title 17    — Limitation; revival of debts

  General Business (lawId=GBS)
    Article 29-H — Debt collection procedures (NY's Mini-FDCPA)
    Article 22-A — Deceptive acts and practices (§ 349 + § 350)

  Real Property Actions and Proceedings (lawId=RPA, "RPAPL")
    Article 7   — Summary Proceedings to Recover Possession of Real Property
    Article 13  — Foreclosure of Mortgages

  Real Property Law (lawId=RPP)
    Article 7   — Landlord and Tenant

  Uniform Commercial Code — New York enactment (lawId=UCC)
    Article 2   — Sales
    Article 3   — Negotiable Instruments
    Article 9   — Secured Transactions

  Domestic Relations (lawId=DOM)
    Article 9   — Action for Divorce, Separation, or Annulment
    Article 11  — Child Support
    Article 5-B — Uniform Interstate Family Support Act

  Estates, Powers and Trusts (lawId=EPT)
    Article 5   — Family Rights

  Banking (lawId=BNK)
    Article 12-A — Mortgage loan licensing
    Article 12-G — Student-loan servicers

  General Construction (lawId=GCN)
    §§ 19, 24, 25, 25-a — public holidays / weekend roll-over

  Vehicle and Traffic (lawId=VAT)
    Article 7-A — DMV consumer-rights (lemon-law triggers)

Each row in TARGETS below is `(lawId, location_id, short_label, topic)`.

## Dependencies
Python 3.10+ stdlib only (urllib + json + html.parser). No third-party
libs.

## Usage
    python3 scripts/pull_ny_statutes.py \\
        --out plugins/ny-court-docs/skills/ny-law-references/references/ny-statutes-debt \\
        --workers 4

    # Refresh one (law, slice) pair:
    python3 scripts/pull_ny_statutes.py --only CVP-Article-31-Disclosure

    # Force stub mode (skip the API even if NYSENATE_API_KEY is set):
    python3 scripts/pull_ny_statutes.py --stubs-only
"""

from __future__ import annotations

import argparse
import json
import os
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
from typing import Any, Dict, List, Optional, Tuple

USER_AGENT = (
    "claude-legal/1.0 (+https://github.com/codearranger/claude-legal) "
    "ny-statutes-puller"
)

API_BASE = "https://legislation.nysenate.gov/api/3/laws"
JSON_ACCEPT = "application/json,*/*;q=0.8"

DEFAULT_WORKERS = 4
PRE_REQUEST_SLEEP_MIN = 0.4
PRE_REQUEST_SLEEP_MAX = 1.0


# ----------------------------------------------------------------------
# Target catalog.
# ----------------------------------------------------------------------

@dataclass
class StatuteTarget:
    law_id: str          # NY Open-Leg lawId (e.g. "CVP", "GOB")
    location_id: str     # Open-Leg locationId (e.g. "A31"); "" = whole law
    label: str           # filename stem ("CVP-Article-31-Disclosure")
    topic: str           # one-line topic descriptor for stubs / headings
    title: str           # human-readable Markdown H1


def _spec(law_id: str, location_id: str, short: str, topic: str,
          title_prefix: str) -> StatuteTarget:
    """Helper to keep TARGETS table compact."""
    label = f"{law_id}-{short}" if short else law_id
    label = label.replace(" ", "-")
    title = f"{title_prefix} — {topic}" if topic else title_prefix
    return StatuteTarget(law_id, location_id, label, topic, title)


TARGETS: List[StatuteTarget] = [
    # All locationIds below verified against the live Open Legislation
    # API at https://legislation.nysenate.gov/api/3/laws/{lawId}.
    # Article numbers in this corpus are written `A<N>` (no hyphen for
    # plain articles, with hyphen for sub-articles like `A22-A`).

    # --- CPLR (Civil Practice Law and Rules) ---
    _spec("CVP", "A1",    "Article-1",                       "Short Title; Applicability and Definitions", "Civil Practice Law and Rules"),
    _spec("CVP", "A2",    "Article-2-Limitations",           "Limitations of Time",                        "Civil Practice Law and Rules"),
    _spec("CVP", "A3",    "Article-3-Jurisdiction",          "Jurisdiction and Service, Appearance and Choice of Court", "Civil Practice Law and Rules"),
    _spec("CVP", "A21",   "Article-21-Papers",               "Papers",                                     "Civil Practice Law and Rules"),
    _spec("CVP", "A22",   "Article-22-Stays",                "Stay, Motions, Orders and Mandates",         "Civil Practice Law and Rules"),
    _spec("CVP", "A23",   "Article-23-Subpoenas",            "Subpoenas, Oaths and Affirmations",          "Civil Practice Law and Rules"),
    _spec("CVP", "A30",   "Article-30-Pleadings",            "Remedies and Pleading",                      "Civil Practice Law and Rules"),
    _spec("CVP", "A31",   "Article-31-Disclosure",           "Disclosure (Discovery)",                     "Civil Practice Law and Rules"),
    _spec("CVP", "A32",   "Article-32-Accelerated",          "Accelerated Judgment (Summary Judgment, Dismissal Motions)", "Civil Practice Law and Rules"),
    _spec("CVP", "A40",   "Article-40-Trial",                "Trial Generally",                            "Civil Practice Law and Rules"),
    _spec("CVP", "A45",   "Article-45-Evidence",             "Evidence (CPLR codified evidence rules)",    "Civil Practice Law and Rules"),
    _spec("CVP", "A50",   "Article-50-Judgments",            "Judgments Generally",                        "Civil Practice Law and Rules"),
    _spec("CVP", "A51",   "Article-51-Enforcement",          "Enforcement of Judgments and Orders Generally", "Civil Practice Law and Rules"),
    _spec("CVP", "A52",   "Article-52-Money-Judgments",      "Enforcement of Money Judgments (Garnishment, Exemptions, Income Executions)", "Civil Practice Law and Rules"),
    _spec("CVP", "A53",   "Article-53-Foreign",              "Recognition of Foreign-Country Money Judgments", "Civil Practice Law and Rules"),

    # --- General Obligations (GOB) ---
    _spec("GOB", "A5",    "Article-5-Contracts",             "Creation, Definition and Enforcement of Contractual Obligations (statute of frauds, interest rates)", "General Obligations Law"),
    _spec("GOB", "A17",   "Article-17-Revival",              "Revival or Extension; Waiver of Defense or Bar (revival of barred debts)", "General Obligations Law"),

    # --- General Business (GBS) ---
    _spec("GBS", "A22-A", "Article-22-A-Deceptive",          "Consumer Protection From Deceptive Acts and Practices (§§ 349-350 — NY's UDAP statute)", "General Business Law"),
    _spec("GBS", "A29-H", "Article-29-H-Debt-Collection",    "Debt Collection Procedures (§§ 600-602 — NY mini-FDCPA)", "General Business Law"),

    # --- Real Property Actions and Proceedings (RPA / RPAPL) ---
    _spec("RPA", "A7",    "Article-7-Summary-Proceedings",   "Summary Proceedings to Recover Possession of Real Property (Holdover + Nonpayment)", "Real Property Actions and Proceedings Law (RPAPL)"),
    _spec("RPA", "A13",   "Article-13-Foreclosure",          "Action to Foreclose a Mortgage",             "Real Property Actions and Proceedings Law (RPAPL)"),

    # --- Real Property Law (RPP) ---
    _spec("RPP", "A6-A",  "Article-6-A-Good-Cause-Eviction", "Good Cause Eviction Law (2024)",             "Real Property Law"),
    _spec("RPP", "A7",    "Article-7-Landlord-Tenant",       "Landlord and Tenant",                        "Real Property Law"),

    # --- Uniform Commercial Code — NY enactment (UCC) ---
    _spec("UCC", "A2",    "Article-2-Sales",                 "Sales",                                      "Uniform Commercial Code"),
    _spec("UCC", "A3",    "Article-3-Commercial-Paper",      "Commercial Paper (NY-enacted Article 3)",    "Uniform Commercial Code"),
    _spec("UCC", "A9",    "Article-9-Secured",               "Secured Transactions",                       "Uniform Commercial Code"),

    # --- Domestic Relations (DOM) ---
    _spec("DOM", "A9",    "Article-9-Annulment",             "Action to Annul a Marriage or Declare It Void", "Domestic Relations Law"),
    _spec("DOM", "A10",   "Article-10-Divorce",              "Action for Divorce",                          "Domestic Relations Law"),
    _spec("DOM", "A13",   "Article-13-Matrimonial",          "Provisions Applicable to More Than One Type of Matrimonial Action", "Domestic Relations Law"),

    # --- Family Court Act (FCT) — child support + UIFSA ---
    _spec("FCT", "A4",    "Article-4-Child-Support",         "Support of Dependents (child support)",      "Family Court Act"),
    _spec("FCT", "A5-B",  "Article-5-B-UIFSA",               "Uniform Interstate Family Support Act (UIFSA)", "Family Court Act"),

    # --- Estates, Powers and Trusts (EPT) ---
    _spec("EPT", "A5",    "Article-5-Family-Rights",         "Family Rights",                               "Estates, Powers and Trusts Law"),

    # --- General Construction (GCN) — holidays + time computation (whole law) ---
    _spec("GCN", "",      "General-Construction-Holidays",   "Public Holidays; Time Computation; full law", "General Construction Law"),

    # --- Banking (BNK) — debt-collector licensure / mortgage servicing ---
    _spec("BNK", "A12-D", "Article-12-D-Mortgage-Bankers",   "Licensed Mortgage Bankers",                   "Banking Law"),
    _spec("BNK", "A12-E", "Article-12-E-Mortgage-LO",        "Licensed Mortgage Loan Originators",          "Banking Law"),
    _spec("BNK", "A14-A", "Article-14-A-Student-Loan",       "Student Loan Servicers",                      "Banking Law"),
]


# ----------------------------------------------------------------------
# Networking.
# ----------------------------------------------------------------------

def get_api_key() -> Optional[str]:
    """Return the NY Senate Open Legislation API key from env, or None.

    The legislation.nysenate.gov API rejects unauthenticated requests
    with HTTP 401 and the error body
        {"success": false, "errorCode": 701, "message":
         "A valid API key is needed to fulfill this request."}
    Set NYSENATE_API_KEY in the env to enable the API path."""
    key = os.environ.get("NYSENATE_API_KEY", "").strip()
    return key or None


def http_get_json(url: str, *, api_key: Optional[str],
                   retries: int = 4, base_sleep: float = 1.5,
                   timeout: float = 60.0
                   ) -> Tuple[int, Optional[Dict[str, Any]], bytes]:
    """Fetch a JSON URL with retries.

    Returns `(status, parsed_json_or_none, raw_body)`. Status code is
    captured (not raised) for 4xx so the caller can write a stub for a
    missing slice without aborting the leg."""
    time.sleep(random.uniform(PRE_REQUEST_SLEEP_MIN, PRE_REQUEST_SLEEP_MAX))
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": JSON_ACCEPT,
    }
    final_url = url
    if api_key:
        sep = "&" if "?" in url else "?"
        final_url = f"{url}{sep}key={urllib.parse.quote(api_key)}"
    parsed = urllib.parse.urlsplit(final_url)
    safe_path = urllib.parse.quote(parsed.path, safe="/%():'.,")
    safe_url = urllib.parse.urlunsplit(
        (parsed.scheme, parsed.netloc, safe_path, parsed.query,
         parsed.fragment)
    )
    req = urllib.request.Request(safe_url, headers=headers)
    last_exc: Optional[BaseException] = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read()
                try:
                    parsed_json = json.loads(body)
                except json.JSONDecodeError:
                    parsed_json = None
                return resp.status, parsed_json, body
        except urllib.error.HTTPError as exc:
            body = exc.read() if exc.fp else b""
            try:
                parsed_json = json.loads(body)
            except json.JSONDecodeError:
                parsed_json = None
            if 400 <= exc.code < 500:
                return exc.code, parsed_json, body
            last_exc = exc
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            last_exc = exc
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
        sleep_for = base_sleep * (2 ** attempt) * (0.5 + random.random())
        time.sleep(sleep_for)
    assert last_exc is not None
    raise last_exc


# ----------------------------------------------------------------------
# API → Markdown.
# ----------------------------------------------------------------------

def walk_law_tree(node: Dict[str, Any], depth: int = 1
                   ) -> List[Tuple[int, str, str]]:
    """Walk an Open-Leg law tree document and yield
    `(heading_level, locationId, title)` triples for index emission.

    Open Legislation returns law tree shapes like:
        {"result": {"documents": {"docType": "CHAPTER", "title": "...",
                                  "documents": [...children]}}}
    Each child is a `{docType, title, locationId, documents}` node."""
    out: List[Tuple[int, str, str]] = []
    title = node.get("title") or node.get("docType") or ""
    loc = node.get("locationId") or ""
    if title:
        out.append((depth, loc, title))
    children = node.get("documents")
    if isinstance(children, dict):
        children = children.get("items") or []
    if isinstance(children, list):
        for child in children:
            out.extend(walk_law_tree(child, depth + 1))
    return out


def _decode_text(raw: str) -> str:
    """Decode an Open-Leg `text` field into clean Markdown.

    The API delivers section bodies with embedded **literal** `\\n`
    sequences (backslash + n, not JSON-escaped newlines), and the
    first line is the section heading repeating the section number.
    We unescape the literal sequences and squash runs of blank lines.
    """
    out = raw
    # Convert literal `\n` to real newlines, then `\t` to tabs. The
    # `replace` order matters — `\n` is more common; doing it first
    # avoids interleaving issues.
    out = out.replace("\\n", "\n").replace("\\r", "\n").replace("\\t", "\t")
    # Strip carriage returns and trailing spaces on each line.
    out = "\n".join(line.rstrip() for line in out.split("\n"))
    # Collapse 3+ consecutive blank lines down to one blank line.
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out.strip()


def render_section_md(section: Dict[str, Any]) -> str:
    """Render one Open-Leg section JSON to Markdown.

    Each section node carries `{locationId, title, text}` where `text`
    is the rendered statutory body. We emit a `## § <num>. <title>`
    heading followed by the decoded body."""
    title = section.get("title") or section.get("locationId") or ""
    loc = section.get("locationId") or ""
    raw = section.get("text") or ""
    body = _decode_text(raw)
    section_marker = section.get("sectionNo") or loc
    heading = f"## § {section_marker}. {title}".strip()
    if not body:
        return heading + "\n\n_(No text returned by API.)_\n"
    # The API's `text` body usually starts with a redundant
    # "§ 3101. Scope of disclosure. " prefix that duplicates the
    # heading. Strip it if present.
    duplicate_prefix = f"§ {section_marker}. {title}".strip().rstrip(".")
    if body.lstrip().startswith(duplicate_prefix):
        # Find first sentence end and strip.
        stripped = body.lstrip()[len(duplicate_prefix):].lstrip(". \n\t")
        body = stripped
    return f"{heading}\n\n{body}\n"


def collect_sections(node: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Depth-first traversal of a law tree producing the section
    documents in document order."""
    out: List[Dict[str, Any]] = []
    dt = (node.get("docType") or "").upper()
    if dt == "SECTION":
        out.append(node)
    children = node.get("documents")
    if isinstance(children, dict):
        children = children.get("items") or []
    if isinstance(children, list):
        for child in children:
            out.extend(collect_sections(child))
    return out


def find_subtree(root: Dict[str, Any], location_id: str
                  ) -> Optional[Dict[str, Any]]:
    """Find the descendant node whose `locationId` matches `location_id`.

    Returns None if no such node exists. Empty `location_id` returns
    the root itself (used for whole-law targets like GCN).
    """
    if not location_id:
        return root
    if root.get("locationId") == location_id:
        return root
    children = root.get("documents")
    if isinstance(children, dict):
        children = children.get("items") or []
    if isinstance(children, list):
        for child in children:
            r = find_subtree(child, location_id)
            if r is not None:
                return r
    return None


# ----------------------------------------------------------------------
# Rendering.
# ----------------------------------------------------------------------

HEADER_BLOCK = """# {title}

> **Source:** {source}
> **Fetched:** {fetched}
> **Format:** {fmt}

> **NOT LEGAL ADVICE.** Generated content is a drafting aid; verify
> against the current law before filing.

---

"""


def render_md(target: StatuteTarget, source_url: str, fetched: str,
               sections: List[Dict[str, Any]]) -> str:
    header = HEADER_BLOCK.format(
        title=target.title,
        source=source_url,
        fetched=fetched,
        fmt="verbatim conversion of the NY State Senate Open "
            "Legislation API JSON response",
    )
    body_parts: List[str] = []
    for s in sections:
        body_parts.append(render_section_md(s))
    body = "\n".join(body_parts).rstrip() + "\n"
    body = re.sub(r"\n{3,}", "\n\n", body)
    return header + body


def render_stub(target: StatuteTarget, fetched: str, reason: str) -> str:
    canonical_url = (
        f"https://www.nysenate.gov/legislation/laws/"
        f"{target.law_id}"
        + (f"/{target.location_id}" if target.location_id else "")
    )
    api_url = (
        f"{API_BASE}/{target.law_id}"
        + (f"/{target.location_id}" if target.location_id else "")
    )
    return (
        f"# {target.title}\n\n"
        f"> **Source:** {canonical_url}\n"
        f"> **API:** {api_url}\n"
        f"> **Fetched:** {fetched}\n"
        f"> **Status:** _(stub — fetch deferred)_ — {reason}\n"
        f"> **Format:** pointer stub\n\n"
        f"> **NOT LEGAL ADVICE.** This file is a pointer to the\n"
        f"> canonical source; verify against the source itself before\n"
        f"> filing.\n\n"
        f"---\n\n"
        f"## Scope\n\n"
        f"`{target.law_id}`"
        + (f" — `{target.location_id}`" if target.location_id else "")
        + f": {target.topic}.\n\n"
        f"## How to retrieve verbatim text\n\n"
        f"1. **Public HTML mirror** — open the canonical NY State\n"
        f"   Senate URL above in a browser.\n"
        f"2. **Open Legislation JSON API** — request the API URL\n"
        f"   above with `?key=<NYSENATE_API_KEY>` appended. The key is\n"
        f"   free to obtain at\n"
        f"   https://legislation.nysenate.gov/static/docs/html/#api-key-registration\n"
        f"   When the key is wired into the `NYSENATE_API_KEY` env var\n"
        f"   (or the workflow secret of the same name), the next\n"
        f"   quarterly refresh will replace this stub with verbatim\n"
        f"   statutory text.\n\n"
        f"## Why this is a stub\n\n"
        f"The NY Open Legislation API requires a registered API key.\n"
        f"At the time of the most recent refresh the key was not\n"
        f"available to the puller (NYSENATE_API_KEY env var was unset,\n"
        f"or the API returned an error). This stub keeps the corpus's\n"
        f"shape — the next successful refresh with a key will\n"
        f"populate the verbatim text.\n"
    )


# ----------------------------------------------------------------------
# One target → one file.
# ----------------------------------------------------------------------

@dataclass
class WriteResult:
    label: str
    path: Path
    bytes_written: int
    error: Optional[str]
    stub: bool


def _file_is_stub(path: Path) -> bool:
    try:
        head = path.read_text(encoding="utf-8")[:1024]
    except Exception:  # noqa: BLE001
        return True
    return "(stub" in head or "Format:** pointer stub" in head


def fetch_law(law_id: str, api_key: str
               ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Fetch a single NY consolidated law tree (with `?full=true` so
    each SECTION includes its `text` body). Returns `(root_node, err)`.

    `root_node` is the law's top-level document (a CHAPTER node whose
    `documents.items` lists the ARTICLE children). On any failure
    `root_node` is None and `err` is a one-line reason."""
    url = f"{API_BASE}/{law_id}?full=true"
    try:
        status, payload, _ = http_get_json(url, api_key=api_key)
    except Exception as exc:  # noqa: BLE001
        return None, f"{type(exc).__name__}: {exc}"
    if status >= 400 or payload is None or not payload.get("success"):
        msg = "HTTP " + str(status)
        if payload is not None:
            msg = (payload.get("message") or msg)[:200]
        return None, msg
    root = (payload.get("result") or {}).get("documents")
    if not isinstance(root, dict):
        return None, "no result.documents in API response"
    return root, None


def write_one(target: StatuteTarget, out_dir: Path, fetched_iso: str,
               api_key: Optional[str], stubs_only: bool,
               law_cache: Dict[str, Tuple[Optional[Dict[str, Any]],
                                          Optional[str]]]
               ) -> WriteResult:
    """Render one target. If the API path is available and the law has
    already been fetched (or can be fetched on first use), slice the
    cached tree to find the target article and emit its sections."""
    out_path = out_dir / f"{target.label}.md"

    # --- Stubs mode ---
    if stubs_only or api_key is None:
        body = render_stub(
            target,
            fetched_iso,
            "API key unavailable (NYSENATE_API_KEY env var unset)"
            if not stubs_only else "stubs-only mode",
        )
        if out_path.exists() and not _file_is_stub(out_path):
            return WriteResult(target.label, out_path,
                               out_path.stat().st_size, None, stub=False)
        tmp = out_path.with_suffix(".md.tmp")
        tmp.write_text(body, encoding="utf-8")
        tmp.rename(out_path)
        return WriteResult(target.label, out_path, out_path.stat().st_size,
                            None, stub=True)

    # --- API mode: ensure the law tree is cached ---
    if target.law_id not in law_cache:
        law_cache[target.law_id] = fetch_law(target.law_id, api_key)
    root, err = law_cache[target.law_id]

    api_url = f"{API_BASE}/{target.law_id}?full=true"
    if root is None:
        return _write_stub_or_keep(target, out_path, fetched_iso,
                                    f"law fetch failed: {err}")

    # --- Slice the cached tree ---
    subtree = find_subtree(root, target.location_id)
    if subtree is None:
        return _write_stub_or_keep(
            target, out_path, fetched_iso,
            f"locationId {target.location_id!r} not found in {target.law_id} tree",
        )
    sections = collect_sections(subtree)
    if not sections:
        return _write_stub_or_keep(
            target, out_path, fetched_iso,
            "no SECTION documents under that locationId",
        )

    rendered = render_md(target, api_url, fetched_iso, sections)
    tmp = out_path.with_suffix(".md.tmp")
    tmp.write_text(rendered, encoding="utf-8")
    tmp.rename(out_path)
    return WriteResult(target.label, out_path, out_path.stat().st_size,
                       None, stub=False)


def _write_stub_or_keep(target: StatuteTarget, out_path: Path,
                         fetched_iso: str, reason: str) -> WriteResult:
    """If a substantive file already exists for `target`, keep it.
    Otherwise write a fresh stub with `reason`."""
    if out_path.exists() and not _file_is_stub(out_path):
        return WriteResult(target.label, out_path,
                           out_path.stat().st_size,
                           f"{reason} (kept existing file)",
                           stub=False)
    stub_body = render_stub(target, fetched_iso, reason)
    tmp = out_path.with_suffix(".md.tmp")
    tmp.write_text(stub_body, encoding="utf-8")
    tmp.rename(out_path)
    return WriteResult(target.label, out_path,
                       out_path.stat().st_size, reason, stub=True)


# ----------------------------------------------------------------------
# Manifest update.
# ----------------------------------------------------------------------

def update_manifest(out_dir: Path, fetched_iso: str,
                     new_version: str = "0.1.0",
                     mode: str = "stubs") -> Optional[Path]:
    manifest_path = out_dir / "_manifest.json"
    payload = {
        "version": new_version,
        "last_pulled": fetched_iso,
        "source": "https://legislation.nysenate.gov/api/3/laws",
        "mode": mode,
        "notes": (
            "Pulled by scripts/pull_ny_statutes.py. When run with "
            "NYSENATE_API_KEY set, the puller writes verbatim "
            "statutory text from the Open Legislation API. Without "
            "the key, it writes pointer stubs that document the gap."
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
            "plugins/ny-court-docs/skills/ny-law-references/"
            "references/ny-statutes-debt"
        ),
        help="Output directory for the corpus.",
    )
    ap.add_argument(
        "--only",
        nargs="*",
        help="Restrict to these label codes "
             "(e.g. --only CVP-Article-31-Disclosure).",
    )
    ap.add_argument(
        "--workers",
        type=int,
        default=DEFAULT_WORKERS,
        help=f"Concurrent fetches (default {DEFAULT_WORKERS}).",
    )
    ap.add_argument(
        "--manifest-version",
        default="0.1.0",
        help="Version to write into _manifest.json on success.",
    )
    ap.add_argument(
        "--stubs-only",
        action="store_true",
        help="Skip the API entirely and write pointer stubs for every "
             "target. Useful for refreshing the corpus shape without "
             "an API key.",
    )
    args = ap.parse_args()

    out_dir: Path = args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    only = set(args.only) if args.only else None
    targets = [t for t in TARGETS if only is None or t.label in only]
    if not targets:
        print(f"!! no targets match --only {args.only!r}", file=sys.stderr)
        return 2

    api_key = None if args.stubs_only else get_api_key()
    mode = "stubs" if (args.stubs_only or api_key is None) else "api"

    fetched_iso = date.today().isoformat()
    print(f"=== pulling {len(targets)} NY statute target(s) → "
          f"{out_dir} (workers={args.workers}, mode={mode})",
          flush=True)

    # In API mode we fetch one law tree per unique lawId (with
    # `?full=true`) and then slice in-memory for every target. That
    # collapses what used to be N per-target HTTP calls down to ~10.
    # `law_cache` is `{lawId: (root_node_or_None, error_or_None)}`.
    law_cache: Dict[str, Tuple[Optional[Dict[str, Any]], Optional[str]]] = {}

    # If in API mode, prefetch each unique law concurrently so we
    # don't serialize the network round-trips behind the per-target
    # loop. Stub mode skips this entirely.
    if not (args.stubs_only or api_key is None):
        unique_law_ids = sorted({t.law_id for t in targets})
        prefetch_workers = max(1, min(args.workers, len(unique_law_ids)))
        print(f"=== prefetching {len(unique_law_ids)} unique law "
              f"tree(s) (workers={prefetch_workers})", flush=True)
        with ThreadPoolExecutor(max_workers=prefetch_workers) as pool:
            futures = {pool.submit(fetch_law, lid, api_key): lid
                       for lid in unique_law_ids}
            for fut in as_completed(futures):
                lid = futures[fut]
                try:
                    law_cache[lid] = fut.result()
                except Exception as exc:  # noqa: BLE001
                    law_cache[lid] = (None,
                                       f"{type(exc).__name__}: {exc}")
                root, err = law_cache[lid]
                tag = "OK  " if root is not None else "FAIL"
                size = (sum(1 for _ in
                            collect_sections(root)) if root else 0)
                print(f"     [{tag}] {lid} "
                      f"({size:,} sections)"
                      + (f" — {err}" if err else ""), flush=True)

    results: List[WriteResult] = []
    for t in targets:
        results.append(
            write_one(t, out_dir, fetched_iso, api_key,
                      args.stubs_only, law_cache)
        )

    by_label = {r.label: r for r in results}
    ordered = [by_label[t.label] for t in targets if t.label in by_label]
    for t, r in zip(targets, ordered):
        if r.error is None:
            tag = "STUB" if r.stub else "OK  "
        else:
            tag = "FAIL"
        print(f"     [{tag}] {t.label}.md "
              f"({r.bytes_written:,} bytes)"
              + (f" — {r.error}" if r.error else ""),
              flush=True)

    fail = [r for r in ordered if r.error is not None
            and "kept existing file" not in (r.error or "")]
    total_bytes = sum(r.bytes_written for r in ordered)
    print(f"\n=== wrote/kept {len(ordered)} target(s), "
          f"{total_bytes:,} bytes total; {len(fail)} hard-failed",
          flush=True)

    if only is None:
        mp = update_manifest(out_dir, fetched_iso, args.manifest_version,
                              mode)
        if mp is not None:
            print(f"=== updated {mp} → version "
                  f"{args.manifest_version}, last_pulled {fetched_iso}, "
                  f"mode {mode}", flush=True)

    return 0 if not fail else 1


if __name__ == "__main__":
    sys.exit(main())
