#!/usr/bin/env python3
"""Pull New York court-rule canonical sources and convert each to a
verbatim Markdown file.

Output: plugins/ny-court-docs/skills/ny-law-references/references/court-rules/

Targets:

  202.md                    — 22 NYCRR Part 202 (Uniform Civil Rules for
                              the Supreme Court and the County Court)
  202.70.md                 — 22 NYCRR § 202.70 (Commercial Division
                              Rules of the Supreme Court)
  208.md                    — 22 NYCRR Part 208 (Uniform Civil Rules for
                              the New York City Civil Court)
  210.md                    — 22 NYCRR Part 210 (Uniform Civil Rules for
                              the City Courts outside the City of
                              New York)
  212.md                    — 22 NYCRR Part 212 (Uniform Civil Rules for
                              the District Courts)
  214.md                    — 22 NYCRR Part 214 (Uniform Rules for the
                              Court of Claims)
  130.md                    — 22 NYCRR Part 130 (Costs and sanctions —
                              frivolous conduct)
  Part-1200-Conduct.md      — 22 NYCRR Part 1200 (Rules of Professional
                              Conduct)
  Tanbook.md                — pointer stub for the NY Law Reports Style
                              Manual ("Tanbook") — published by the
                              Reporter of Decisions; not in 22 NYCRR
  NYC-CivilCourt-LR.md      — pointer stub for the NYC Civil Court
                              Directives and Procedures Manual
  Nassau-DC-LR.md           — pointer stub for the Nassau County
                              District Court local rules and Part Rules
  Suffolk-DC-LR.md          — pointer stub for the Suffolk County
                              District Court local rules and Part Rules

Source publication discipline:

  The New York Unified Court System publishes all of Title 22 of the
  NYCRR (the "Rules of the Chief Administrator" / "Rules of the Chief
  Judge" / "Uniform Civil Rules for the Trial Courts") on
  `www.nycourts.gov/rules/trialcourts/`. As of late 2025 / mid-2026 the
  publication site sits behind a Cloudflare managed-challenge gate that
  rejects non-browser user agents with a 403 + JS challenge — the same
  pattern Colorado's courts.coloradojudicial.gov uses on its rule
  index. We therefore:

  1. **Try the canonical URLs.** GitHub Actions runners and many
     enterprise IP ranges aren't always challenged; when the fetch
     succeeds the script writes the verbatim Markdown.

  2. **Fall back to pointer stubs.** When the upstream returns a
     Cloudflare interstitial (403 / "Just a moment..."), we write a
     pointer-stub Markdown with the canonical URL and a one-paragraph
     description of what the rule set governs. The stub remains in
     place until a successful pull replaces it.

  This mirrors `pull_co_court_rules.py`'s "publish what we can verify
  + honest stubs for what's gated" approach. It also mirrors
  `pull_oregon_rules.py`'s pdftotext-layout convention for any PDF
  artifacts encountered, though most NY trial-court rules are
  published as `.shtml` HTML.

Dependencies: Python 3.10+ stdlib only (urllib + html.parser).
Optional: poppler (`brew install poppler`) for PDF fallback if NY ever
republishes its consolidated rules as a single PDF.

Usage:
    python3 scripts/pull_ny_court_rules.py \\
        --out plugins/ny-court-docs/skills/ny-law-references/references/court-rules

    # Refresh one rule set:
    python3 scripts/pull_ny_court_rules.py --only 202
    python3 scripts/pull_ny_court_rules.py --only 202 208 212
"""

from __future__ import annotations

import argparse
import html
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Optional, Tuple

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 "
    "Safari/537.36"
)

# UCS publishes trial-court rules at a per-Part URL slug rather than
# the legacy `/rules/trialcourts/{N}.shtml` pattern. Each RuleSpec
# below carries the absolute URL.
UCS_BASE = "https://www.nycourts.gov"

# Optional HTTP proxy. The www.nycourts.gov host sits behind
# Cloudflare with bot-fight mode that fingerprints TLS handshakes.
# To pull verbatim content we need (a) a Cloudflare-trusted IP and
# (b) a Chrome-mimic TLS fingerprint. The puller satisfies (b) by
# using curl_cffi's chrome impersonation; for (a) the operator may
# point the puller at a Cloudflare-Warp HTTP proxy via the
# NY_RULES_PROXY env var (e.g. http://192.168.8.21:9091). The CI
# refresh workflow runs without the proxy; CI runners often clear
# the upstream gate via their own IP reputation, but if they don't,
# the puller falls back to stubs gracefully.
PROXY_ENV_VAR = "NY_RULES_PROXY"


# ----------------------------------------------------------------------
# Networking — curl_cffi + Chrome TLS fingerprint.
# ----------------------------------------------------------------------

class CloudflareChallenge(Exception):
    """Raised when the upstream returns a Cloudflare 'Just a moment...'
    interstitial in lieu of substantive HTML."""


def _looks_like_cf_challenge(body: bytes) -> bool:
    """Detect a Cloudflare managed-challenge response."""
    head = body[:4096].decode("utf-8", errors="replace").lower()
    if "just a moment" in head:
        return True
    if "cf_chl_opt" in head or "challenge-platform" in head:
        return True
    return False


def _get_proxies() -> Optional[Dict[str, str]]:
    """Return curl_cffi proxies dict from the `NY_RULES_PROXY` env
    var if set; otherwise None (direct fetch)."""
    proxy = os.environ.get(PROXY_ENV_VAR, "").strip()
    if not proxy:
        return None
    return {"http": proxy, "https": proxy}


def http_get_bytes(url: str, *, headers: Optional[Dict[str, str]] = None,
                    retries: int = 3, base_sleep: float = 1.5,
                    timeout: float = 60.0) -> bytes:
    """Fetch a URL with curl_cffi's Chrome TLS impersonation +
    optional warpsocks proxy + jittered exponential-backoff retries.

    Raises `CloudflareChallenge` if the response body looks like a
    CF interstitial — the caller falls back to a stub."""
    try:
        from curl_cffi import requests as _requests  # type: ignore
    except ImportError:
        raise RuntimeError(
            "curl_cffi is required to bypass Cloudflare TLS "
            "fingerprinting on www.nycourts.gov; install with "
            "`pip install --break-system-packages curl_cffi`"
        )

    req_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;"
                   "q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": USER_AGENT,
    }
    if headers:
        req_headers.update(headers)

    proxies = _get_proxies()
    last_exc: Optional[BaseException] = None
    for attempt in range(retries):
        try:
            r = _requests.get(
                url,
                headers=req_headers,
                proxies=proxies,
                impersonate="chrome",
                timeout=timeout,
                allow_redirects=True,
            )
            body = r.content
            if r.status_code >= 400:
                if _looks_like_cf_challenge(body):
                    raise CloudflareChallenge(
                        f"Cloudflare interstitial for {url}"
                    )
                last_exc = RuntimeError(
                    f"HTTP {r.status_code} for {url}"
                )
            else:
                if _looks_like_cf_challenge(body):
                    raise CloudflareChallenge(
                        f"Cloudflare interstitial for {url}"
                    )
                return body
        except CloudflareChallenge:
            raise
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
        sleep_for = base_sleep * (2 ** attempt) * (0.5 + random.random())
        time.sleep(sleep_for)
    assert last_exc is not None
    raise last_exc


# ----------------------------------------------------------------------
# HTML → Markdown.
# ----------------------------------------------------------------------

class RuleHTMLToMD(HTMLParser):
    """Minimal HTML-to-Markdown extractor tuned for nycourts.gov's
    `/rules/trialcourts/*.shtml` template.

    The UCS publication template wraps the rule body in a
    `<div id="main">` or `<div class="content">` and uses simple
    `<p>`, `<h1>`-`<h4>`, `<strong>`, `<em>`, `<a>`, `<ul>`, `<ol>`,
    `<li>`, `<br>` tags. We collect text, treat headings + paragraphs
    as paragraph-level breaks, and emit Markdown headings for the rule
    structure. Tables are linearised (one row per line) since 22 NYCRR
    barely uses tables outside the Commercial Division rules' caption
    examples."""

    BLOCK_TAGS = {
        "p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6",
        "ul", "ol", "table", "section", "article", "header", "footer",
    }
    HEADING_TAGS = {"h1": 1, "h2": 2, "h3": 3, "h4": 4, "h5": 5, "h6": 6}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: List[str] = []
        self._buf: List[str] = []
        self._skip_depth = 0
        self._heading_level: Optional[int] = None
        self._strong_depth = 0
        self._italic_depth = 0
        self._in_li = False
        self._li_marker: List[str] = []  # stack: "ul" or "ol"
        self._ol_counter: List[int] = []
        self._seen_main = False

    def _flush_paragraph(self) -> None:
        text = "".join(self._buf).strip()
        self._buf = []
        if not text:
            return
        text = re.sub(r"\s+", " ", text).strip()
        if self._heading_level is not None:
            prefix = "#" * self._heading_level
            self.out.append(f"\n{prefix} {text}\n")
            self._heading_level = None
        elif self._in_li and self._li_marker:
            kind = self._li_marker[-1]
            if kind == "ol":
                idx = self._ol_counter[-1]
                self.out.append(f"{idx}. {text}\n")
                self._ol_counter[-1] = idx + 1
            else:
                self.out.append(f"- {text}\n")
        else:
            self.out.append(f"{text}\n\n")

    def handle_starttag(self, tag: str, attrs):
        if tag in ("script", "style", "noscript", "head"):
            self._skip_depth += 1
            return
        if self._skip_depth:
            return
        if tag in self.HEADING_TAGS:
            self._flush_paragraph()
            self._heading_level = self.HEADING_TAGS[tag]
        elif tag in ("strong", "b"):
            self._strong_depth += 1
            self._buf.append("**")
        elif tag in ("em", "i"):
            self._italic_depth += 1
            self._buf.append("*")
        elif tag == "li":
            self._flush_paragraph()
            self._in_li = True
        elif tag == "ul":
            self._flush_paragraph()
            self._li_marker.append("ul")
        elif tag == "ol":
            self._flush_paragraph()
            self._li_marker.append("ol")
            self._ol_counter.append(1)
        elif tag == "br":
            self._buf.append("\n")
        elif tag in self.BLOCK_TAGS:
            self._flush_paragraph()

    def handle_endtag(self, tag: str):
        if tag in ("script", "style", "noscript", "head"):
            self._skip_depth = max(0, self._skip_depth - 1)
            return
        if self._skip_depth:
            return
        if tag in self.HEADING_TAGS:
            self._flush_paragraph()
        elif tag in ("strong", "b"):
            self._strong_depth = max(0, self._strong_depth - 1)
            self._buf.append("**")
        elif tag in ("em", "i"):
            self._italic_depth = max(0, self._italic_depth - 1)
            self._buf.append("*")
        elif tag == "li":
            self._flush_paragraph()
            self._in_li = False
        elif tag in ("ul", "ol"):
            self._flush_paragraph()
            if self._li_marker and self._li_marker[-1] == tag:
                self._li_marker.pop()
                if tag == "ol" and self._ol_counter:
                    self._ol_counter.pop()
        elif tag in self.BLOCK_TAGS:
            self._flush_paragraph()

    def handle_data(self, data: str):
        if self._skip_depth:
            return
        self._buf.append(data)

    def to_markdown(self) -> str:
        self._flush_paragraph()
        text = "".join(self.out)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip() + "\n"


def html_to_markdown(html_text: str) -> str:
    parser = RuleHTMLToMD()
    parser.feed(html_text)
    return parser.to_markdown()


# ----------------------------------------------------------------------
# Rendering.
# ----------------------------------------------------------------------

HEADER_BLOCK = """# {title}

> **Source:** {source}
> **Fetched:** {fetched}
> **Format:** {fmt}

> **NOT LEGAL ADVICE.** Generated content is a drafting aid; verify
> against the current rules before filing.

---

"""


def render_md(title: str, source: str, fetched: str, body: str,
              fmt: str = "verbatim conversion of the canonical HTML "
                         "source published by the NY Unified Court "
                         "System") -> str:
    header = HEADER_BLOCK.format(
        title=title, source=source, fetched=fetched, fmt=fmt,
    )
    rendered = header + body.rstrip() + "\n"
    rendered = re.sub(r"\n{3,}", "\n\n", rendered)
    return rendered


def render_stub(spec: "RuleSpec", fetched: str, reason: str) -> str:
    """Pointer-stub MD body for rules we can't currently fetch.

    Used when the upstream returns a Cloudflare interstitial or the
    URL is otherwise gated (e.g. Tanbook publisher PDFs, paid
    publisher hosts). Mirrors `pull_co_court_rules.py` for the
    `_render_paywall_stub` shape."""
    return (
        f"# {spec.title}\n\n"
        f"> **Source:** {spec.url}\n"
        f"> **Fetched:** {fetched}\n"
        f"> **Status:** _(stub — not currently fetched)_ — {reason}\n"
        f"> **Format:** pointer stub\n\n"
        f"> **NOT LEGAL ADVICE.** This file is a pointer to the\n"
        f"> canonical source; verify against the source itself before\n"
        f"> filing.\n\n"
        f"---\n\n"
        f"## What this set governs\n\n"
        f"{spec.description}\n\n"
        f"## How to retrieve verbatim text\n\n"
        f"Open the canonical URL above in a browser. The New York\n"
        f"Unified Court System publishes the full verbatim text of\n"
        f"this rule set on `www.nycourts.gov`. The page is\n"
        f"interactive HTML; no login is required.\n\n"
        f"## Why this is a stub\n\n"
        f"As of the most recent refresh, the upstream publication\n"
        f"host returned a Cloudflare managed-challenge page (or\n"
        f"otherwise rejected automated requests). This stub will be\n"
        f"replaced with verbatim content on the next quarterly\n"
        f"refresh that successfully clears the upstream gate (or\n"
        f"when this script is run from an IP range the upstream\n"
        f"recognizes as low-risk).\n"
    )


# ----------------------------------------------------------------------
# Rule specs.
# ----------------------------------------------------------------------


@dataclass
class RuleSpec:
    code: str            # output filename stem
    title: str           # Markdown H1 + stub heading
    url: str             # canonical source URL
    description: str     # one-paragraph scope description for stubs
    fetchable: bool = True  # False for sets we know are not public HTML


SPECS: List[RuleSpec] = [
    # --- Civil-practice trial-court rule sets (Parts 200-221) ---
    RuleSpec(
        "Part-202-Supreme-County",
        "22 NYCRR Part 202 — Uniform Civil Rules for the Supreme "
        "Court and the County Court",
        f"{UCS_BASE}/rules/part-202-uniform-civil-rules-supreme-court-and-county-court",
        "The core procedural-format rule set for civil practice in "
        "New York State Supreme Court and County Court. Covers caption "
        "format (§ 202.5), e-filing requirements (§ 202.5-b / § 202.5-bb), "
        "the Individual Assignment System (§ 202.3), motion practice "
        "(§§ 202.7-202.8-g), discovery conferral (§ 202.20-f, the 2021 "
        "good-faith rule), preliminary conferences (§ 202.12), note of "
        "issue (§ 202.21), settle-order (§ 202.48 with the 60-day "
        "jurisdictional clock), the default-judgment scrutiny rules "
        "added by the 2022 Consumer Credit Fairness Act (§ 202.27-a / "
        "§ 202.27-b), AND the Commercial Division Rules at § 202.70 "
        "(threshold table, Appendix A — 25-page memo limit, "
        "proportionality, designated counsel, accelerated adjudication).",
    ),
    RuleSpec(
        "Part-205-Family",
        "22 NYCRR Part 205 — Uniform Rules for the Family Court",
        f"{UCS_BASE}/rules/part-205-uniform-rules-family-court",
        "Format and procedural rules for New York Family Court, "
        "covering Articles 3 (juvenile delinquency), 4 (child support "
        "with Support Magistrate process), 5 (paternity), 6 (custody "
        "and visitation), 7 (PINS), 8 (family-offense + Orders of "
        "Protection), and 10 (abuse and neglect).",
    ),
    RuleSpec(
        "Part-206-Court-Claims",
        "22 NYCRR Part 206 — Uniform Rules for the Court of Claims",
        f"{UCS_BASE}/rules/part-206-uniform-rules-court-claims",
        "Format and procedural rules for the Court of Claims — the "
        "statewide trial court handling claims against the State of "
        "New York. Includes the verified-claim requirement and the "
        "90-day notice-of-intention regime.",
    ),
    RuleSpec(
        "Part-207-Surrogates",
        "22 NYCRR Part 207 — Uniform Rules for the Surrogate's Court",
        f"{UCS_BASE}/rules/part-207-uniform-rules-surrogates-court",
        "Format and procedural rules for the Surrogate's Court "
        "handling wills, estates, guardianship, and adoption matters "
        "(one per county, two in some NYC boroughs).",
    ),
    RuleSpec(
        "Part-208-NYC-Civil",
        "22 NYCRR Part 208 — Uniform Civil Rules for the New York "
        "City Civil Court",
        f"{UCS_BASE}/rules/part-208-uniform-civil-rules-new-york-city-civil-court",
        "Format and procedural rules for the Civil Court of the City "
        "of New York — the separate trial court (Civil Court Act) "
        "handling claims up to $50,000 and small-claims matters up to "
        "$10,000 in five boroughs. The primary forum for consumer-"
        "debt collection litigation in NYC. Includes the 2022 CCFA "
        "default-judgment companion rule at § 208.6-a and the Housing "
        "Part overlay at § 208.42.",
    ),
    RuleSpec(
        "Part-210-City-Courts",
        "22 NYCRR Part 210 — Uniform Civil Rules for the City "
        "Courts Outside the City of New York",
        f"{UCS_BASE}/rules/part-210-uniform-civil-rules-city-courts-outside-city-new-york",
        "Format and procedural rules for the ~60 upstate City Courts "
        "(Uniform City Court Act), with civil jurisdiction up to "
        "$15,000.",
    ),
    RuleSpec(
        "Part-212-District-Courts",
        "22 NYCRR Part 212 — Uniform Civil Rules for the District "
        "Courts",
        f"{UCS_BASE}/rules/part-212-uniform-civil-rules-district-courts",
        "Format and procedural rules for the two Long Island District "
        "Courts (Nassau and Suffolk under the Uniform District Court "
        "Act), civil jurisdiction up to $15,000. Also covers the "
        "District Court Housing Parts on Long Island.",
    ),
    RuleSpec(
        "Part-214-Justice-Courts",
        "22 NYCRR Part 214 — Uniform Civil Rules for the Justice "
        "Courts",
        f"{UCS_BASE}/rules/part-214-uniform-civil-rules-justice-courts",
        "Format and procedural rules for the ~1,250 Town and Village "
        "Justice Courts established under the Uniform Justice Court "
        "Act, civil jurisdiction up to $3,000.",
    ),
    RuleSpec(
        "Part-216-Sealing",
        "22 NYCRR Part 216 — Sealing of Court Records in Civil "
        "Actions in the Trial Courts",
        f"{UCS_BASE}/rules/part-216-sealing-court-records-civil-actions-trial-courts",
        "Procedure for sealing court records in civil actions — "
        "balanced against the public's right of access; cross-"
        "referenced in motion practice involving confidential "
        "personal information and trade secrets.",
    ),
    RuleSpec(
        "Part-220-Jury-Selection",
        "22 NYCRR Part 220 — Uniform Rules for Jury Selection and "
        "Deliberation",
        f"{UCS_BASE}/rules/part-220-uniform-rules-jury-selection-and-deliberation-subpart",
        "Statewide uniform procedures for jury voir dire, challenges, "
        "deliberation, and verdict-receiving across the trial courts.",
    ),
    RuleSpec(
        "Part-221-Depositions",
        "22 NYCRR Part 221 — Uniform Rules for the Conduct of "
        "Depositions",
        f"{UCS_BASE}/rules/part-221-uniform-rules-conduct-depositions",
        "Conduct-of-depositions framework including objection rules, "
        "instruction-not-to-answer limits, and conferral with the "
        "deponent during examination. Adopted statewide 2006.",
    ),
    # --- Chief Administrator rule sets (Parts 100-161) ---
    RuleSpec(
        "Part-100-Judicial-Conduct",
        "22 NYCRR Part 100 — Rules Governing Judicial Conduct",
        f"{UCS_BASE}/rules/part-100-judicial-conduct",
        "Rules governing the conduct of New York judges — recusal "
        "standards, ex parte communication restrictions, financial "
        "disclosure requirements. Cross-referenced in motion "
        "practice for judicial-disqualification arguments.",
    ),
    RuleSpec(
        "Part-104-Records-Retention",
        "22 NYCRR Part 104 — Retention and Disposition of Court "
        "Records",
        f"{UCS_BASE}/rules/part-104-retention-and-disposition-court-records",
        "Records-retention schedule for trial-court filings statewide.",
    ),
    RuleSpec(
        "Part-125-Engagement-Counsel",
        "22 NYCRR Part 125 — Uniform Rules for the Engagement of "
        "Counsel",
        f"{UCS_BASE}/rules/part-125-uniform-rules-engagement-counsel",
        "Rules governing attorney engagement in concurrent matters, "
        "scheduling conflicts, and adjournments where counsel are "
        "engaged elsewhere — civility-and-courtesy framework.",
    ),
    RuleSpec(
        "Part-130-Costs-Sanctions",
        "22 NYCRR Part 130 — Costs and Sanctions for Frivolous "
        "Conduct",
        f"{UCS_BASE}/rules/part-130-costs-and-sanctions",
        "Sanctions framework for frivolous conduct in civil practice "
        "— up to $10,000 per occurrence under § 130-1.1. Cross-"
        "referenced in motion practice across all trial-court levels.",
    ),
    # --- Rules of Professional Conduct (22 NYCRR Part 1200) ---
    # Pointer stub: the NY UCS site does not host Part 1200 (the
    # /legal-professional landing pages link out to Cornell LII for
    # the regulatory text). Cornell LII's per-rule pages serve a
    # regulatory-index wrapper but not the verbatim rule body —
    # the authoritative text remains paywalled at West / LexisNexis.
    # We ship a pointer stub with both the official OCA index and
    # the Cornell LII canonical URL so practitioners can navigate
    # interactively.
    RuleSpec(
        "Part-1200-Professional-Conduct",
        "22 NYCRR Part 1200 — Rules of Professional Conduct",
        "https://www.law.cornell.edu/regulations/new-york/title-22/"
        "subtitle-B/chapter-IV/subchapter-E/part-1200",
        "New York's lawyer-conduct rules, adopted by the four "
        "Appellate Divisions and codified at 22 NYCRR Part 1200. "
        "Closely tracks the ABA Model Rules but with NY-specific "
        "differences (advertising rules, advance-fee deposits, "
        "trust-account requirements). The verbatim text is "
        "published in commercial editions by West and LexisNexis; "
        "the Cornell LII URL provides a navigable index but not the "
        "full rule body.",
        fetchable=False,
    ),
    # --- Pointer stubs (no free authoritative HTML source) ---
    RuleSpec(
        "Tanbook",
        "New York Law Reports Style Manual ('Tanbook')",
        "https://www.nycourts.gov/reporter/New-Edition.htm",
        "The official citation manual for New York court papers, "
        "published by the Reporter of Decisions. The 'Tanbook' "
        "controls citation form for New York cases, statutes, and "
        "regulations in trial-court filings. Not part of 22 NYCRR; "
        "downloaded as a PDF from the Reporter's site.",
        fetchable=False,
    ),
    RuleSpec(
        "NYC-CivilCourt-LR",
        "NYC Civil Court — Directives and Procedures Manual + "
        "Part Rules",
        "https://www.nycourts.gov/courts/nyc/civil/directives.shtml",
        "Local-rule overlay for the Civil Court of the City of New "
        "York: directives covering the Consumer Credit Part, the "
        "Housing Part, ex-parte applications, default judgments "
        "(post-CCFA), and individual Part Rules from the Civil Court "
        "judges.",
        fetchable=False,
    ),
    RuleSpec(
        "Nassau-DC-LR",
        "Nassau County District Court — Local Rules and Part Rules",
        "https://ww2.nycourts.gov/courts/10jd/nassau/districtcourt/index.shtml",
        "Local-rule overlay for Nassau District Court: six districts "
        "headquartered at 99 Main Street, Hempstead. Civil Part, "
        "Landlord-Tenant Part, Small Claims Part rules.",
        fetchable=False,
    ),
    RuleSpec(
        "Suffolk-DC-LR",
        "Suffolk County District Court — Local Rules and Part Rules",
        "https://ww2.nycourts.gov/courts/10jd/suffolk/districtcourt/index.shtml",
        "Local-rule overlay for Suffolk District Court: six "
        "districts headquartered at Central Islip. Civil Part, "
        "Landlord-Tenant Part, Small Claims Part rules.",
        fetchable=False,
    ),
]


# ----------------------------------------------------------------------
# Output writing.
# ----------------------------------------------------------------------

@dataclass
class RuleResult:
    code: str
    path: Path
    bytes_written: int
    error: Optional[str]
    stub: bool


def write_rule(spec: RuleSpec, out_dir: Path, fetched_iso: str
                ) -> RuleResult:
    """Fetch + convert + atomically write one rule set to disk.

    On a fetch / conversion failure (including Cloudflare interstitial),
    we fall back to a pointer stub. If a substantive (non-stub) file
    already exists at the target path and this run only produced a
    stub, we **leave the existing file in place** — quarterly refreshes
    should never regress a known-good corpus into a stub."""
    out_path = out_dir / f"{spec.code}.md"

    if not spec.fetchable:
        body = render_stub(spec, fetched_iso, "not published as free HTML")
        tmp = out_path.with_suffix(".md.tmp")
        if out_path.exists() and not _file_is_stub(out_path):
            return RuleResult(spec.code, out_path,
                              out_path.stat().st_size, None, stub=False)
        tmp.write_text(body, encoding="utf-8")
        tmp.rename(out_path)
        return RuleResult(spec.code, out_path, out_path.stat().st_size,
                          None, stub=True)

    try:
        data = http_get_bytes(spec.url)
        text = data.decode("utf-8", errors="replace")
        md = html_to_markdown(text)
        if len(md.strip()) < 200:
            raise RuntimeError(
                f"extracted body suspiciously short ({len(md)} chars) "
                "— likely a navigation page, not the rule text"
            )
        rendered = render_md(spec.title, spec.url, fetched_iso, md)
    except CloudflareChallenge as exc:
        if out_path.exists() and not _file_is_stub(out_path):
            return RuleResult(spec.code, out_path,
                              out_path.stat().st_size,
                              f"cloudflare-blocked (kept existing file)",
                              stub=False)
        rendered = render_stub(spec, fetched_iso,
                               "Cloudflare managed-challenge")
        tmp = out_path.with_suffix(".md.tmp")
        tmp.write_text(rendered, encoding="utf-8")
        tmp.rename(out_path)
        return RuleResult(spec.code, out_path, out_path.stat().st_size,
                          f"cloudflare: {exc}", stub=True)
    except Exception as exc:  # noqa: BLE001
        if out_path.exists() and not _file_is_stub(out_path):
            return RuleResult(spec.code, out_path,
                              out_path.stat().st_size,
                              f"fetch failed (kept existing file): {exc}",
                              stub=False)
        rendered = render_stub(spec, fetched_iso, f"{type(exc).__name__}")
        tmp = out_path.with_suffix(".md.tmp")
        tmp.write_text(rendered, encoding="utf-8")
        tmp.rename(out_path)
        return RuleResult(spec.code, out_path, out_path.stat().st_size,
                          f"{exc}", stub=True)

    tmp = out_path.with_suffix(".md.tmp")
    tmp.write_text(rendered, encoding="utf-8")
    tmp.rename(out_path)
    return RuleResult(spec.code, out_path, out_path.stat().st_size,
                      None, stub=False)


def _file_is_stub(path: Path) -> bool:
    """Detect whether an existing MD file is a pointer-stub.

    Stubs include the `> **Status:** _(stub` marker injected by
    `render_stub`. Anything else is treated as substantive content
    that a quarterly refresh shouldn't overwrite with a stub."""
    try:
        head = path.read_text(encoding="utf-8")[:1024]
    except Exception:  # noqa: BLE001
        return True
    return "(stub" in head or "Format:** pointer stub" in head


# ----------------------------------------------------------------------
# Manifest update.
# ----------------------------------------------------------------------

def update_manifest(out_dir: Path, fetched_iso: str,
                     new_version: str = "0.1.0") -> Optional[Path]:
    manifest_path = out_dir / "_manifest.json"
    if not manifest_path.exists():
        manifest_path.write_text(
            json.dumps(
                {
                    "version": new_version,
                    "last_pulled": fetched_iso,
                    "source": "https://www.nycourts.gov/rules/trialcourts/",
                    "notes": (
                        "Pulled by scripts/pull_ny_court_rules.py. "
                        "Files marked '_(stub' are pointer-stubs "
                        "rendered when the upstream returns a "
                        "Cloudflare interstitial — they will be "
                        "replaced with verbatim content on the next "
                        "successful refresh."
                    ),
                },
                indent=2,
            ) + "\n",
            encoding="utf-8",
        )
        return manifest_path
    try:
        raw = manifest_path.read_text(encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        print(f"  ! could not read {manifest_path}: {exc}", flush=True)
        return None
    updated = re.sub(
        r'("version"\s*:\s*")[^"]*(")',
        lambda m: f'{m.group(1)}{new_version}{m.group(2)}',
        raw, count=1,
    )
    updated = re.sub(
        r'("last_pulled"\s*:\s*")[^"]*(")',
        lambda m: f'{m.group(1)}{fetched_iso}{m.group(2)}',
        updated, count=1,
    )
    try:
        json.loads(updated)
    except Exception as exc:  # noqa: BLE001
        print(f"  ! manifest update produced invalid JSON; "
              f"leaving {manifest_path} untouched: {exc}", flush=True)
        return None
    manifest_path.write_text(updated, encoding="utf-8")
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
            "references/court-rules"
        ),
        help="Output directory for the corpus.",
    )
    ap.add_argument(
        "--only",
        nargs="*",
        help="Restrict to these rule-set codes "
             "(e.g. --only 202 212).",
    )
    ap.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Concurrent fetches (default 4). Each fetch is one "
             "HTML page; values much above 6 risk tripping the "
             "upstream's anti-scrape heuristics.",
    )
    ap.add_argument(
        "--manifest-version",
        default="0.1.0",
        help="Version to write into _manifest.json on success.",
    )
    args = ap.parse_args()

    out_dir: Path = args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    only = set(args.only) if args.only else None
    targets = [s for s in SPECS if only is None or s.code in only]
    if not targets:
        print(f"!! no rule sets match --only {args.only!r}", file=sys.stderr)
        return 2

    fetched_iso = date.today().isoformat()
    print(f"=== pulling {len(targets)} NY rule set(s) → {out_dir} "
          f"(workers={args.workers})", flush=True)

    results: List[RuleResult] = []
    workers = max(1, min(args.workers, len(targets)))
    if workers == 1:
        for spec in targets:
            print(f"  -> {spec.code} ...", flush=True)
            results.append(write_rule(spec, out_dir, fetched_iso))
    else:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {
                pool.submit(write_rule, spec, out_dir, fetched_iso): spec
                for spec in targets
            }
            for fut in as_completed(futures):
                spec = futures[fut]
                try:
                    results.append(fut.result())
                except Exception as exc:  # noqa: BLE001
                    results.append(RuleResult(spec.code,
                                                out_dir / f"{spec.code}.md",
                                                0, str(exc), stub=True))

    by_code = {r.code: r for r in results}
    ordered = [by_code[s.code] for s in targets if s.code in by_code]
    for spec, r in zip(targets, ordered):
        if r.error is None:
            tag = "STUB" if r.stub else "OK  "
        else:
            tag = "FAIL"
        print(f"     [{tag}] {spec.code}.md "
              f"({r.bytes_written:,} bytes)"
              + (f" — {r.error}" if r.error else ""),
              flush=True)

    fail = [r for r in ordered if r.error is not None
            and "kept existing file" not in (r.error or "")
            and "cloudflare:" not in (r.error or "")]
    ok = [r for r in ordered if r.error is None]
    total_bytes = sum(r.bytes_written for r in ordered)
    print(f"\n=== wrote/kept {len(ordered)} rule set(s), "
          f"{total_bytes:,} bytes total; {len(fail)} hard-failed",
          flush=True)

    if only is None:
        mp = update_manifest(out_dir, fetched_iso, args.manifest_version)
        if mp is not None:
            print(f"=== updated {mp} → version "
                  f"{args.manifest_version}, last_pulled {fetched_iso}",
                  flush=True)

    return 0 if not fail else 1


if __name__ == "__main__":
    sys.exit(main())
