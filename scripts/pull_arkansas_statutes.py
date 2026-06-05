#!/usr/bin/env python3
"""Pull selected Arkansas Code Annotated chapters from the Justia mirror
at `law.justia.com/codes/arkansas/` and convert each chapter to verbatim
Markdown.

Output: plugins/ar-court-docs/skills/ar-law-references/references/ar-statutes-debt/
One MD file per chapter, named `Ark-Code-T<NN>-Ch<NN>.md`
(e.g. `Ark-Code-T16-Ch56.md` for limitations of actions). The directory
slug retains the legacy `debt` name for path stability; scope covers the
full civil + family + consumer practice surface.

## Source

The **statutory text** of the Arkansas Code is in the public domain:
under the government edicts doctrine (Banks v. Manchester, 128 U.S. 244
(1888); Georgia v. Public.Resource.Org, 590 U.S. 255 (2020)) no one
holds copyright in the words of the law. What carries copyright is the
*Annotated* compilation that LexisNexis publishes as Arkansas's official
code. This puller copies ONLY the section text (public domain), never the
annotations, from the most reliably-structured free mirror: Justia
(`law.justia.com/codes/arkansas/`).

Arkansas's code nests Title → Subtitle → Chapter → Subchapter → Section,
so this puller does NOT construct section URLs directly. It DISCOVERS
them by walking links: title index → chapter index (under any subtitle)
→ subchapter indexes → section pages. Section slugs encode the citation
(`section-16-56-105`), so the puller matches links by the
`section-<title>-<chapter>-` prefix regardless of the intervening
subtitle/subchapter path segments.

When Justia returns 403 (its bot-fight policy frequently blocks shared
egress, incl. GitHub Actions IP ranges), the puller writes well-formed
**pointer stubs** carrying the canonical URL and a one-line scope
description — the "publish what we can verify + honest stubs for the
rest" discipline. It uses `curl_cffi` with Chrome TLS impersonation when
available (works from a residential or VPN-routed IP); the `_file_is_stub`
guard preserves committed verbatim content across stub-only re-runs.

## Usage

    python3 scripts/pull_arkansas_statutes.py --workers 4
    python3 scripts/pull_arkansas_statutes.py --only Ark-Code-T16-Ch56
    python3 scripts/pull_arkansas_statutes.py --stubs-only

## Dependencies

Python 3.10+ stdlib; optional `curl_cffi` for the verbatim path.
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
JUSTIA_BASE = "https://law.justia.com/codes/arkansas/"


@dataclass
class ChapterTarget:
    title_num: str   # "16"
    chapter_num: str  # "56"
    label: str       # "Ark-Code-T16-Ch56"
    topic: str       # one-line topic descriptor
    h1: str          # H1 heading rendered into the MD


TARGETS: List[ChapterTarget] = [
    ChapterTarget("1", "5", "Ark-Code-T1-Ch5",
                  "Holidays and observances — official holidays (§ 1-5-101)",
                  "Ark. Code Ann. Title 1, Chapter 5"),
    # Title 4 — UCC + business entities + consumer / commercial
    ChapterTarget("4", "2", "Ark-Code-T4-Ch2",
                  "UCC Article 2 — Sales", "Ark. Code Ann. Title 4, Chapter 2"),
    ChapterTarget("4", "3", "Ark-Code-T4-Ch3",
                  "UCC Article 3 — Negotiable Instruments",
                  "Ark. Code Ann. Title 4, Chapter 3"),
    ChapterTarget("4", "9", "Ark-Code-T4-Ch9",
                  "UCC Article 9 — Secured Transactions",
                  "Ark. Code Ann. Title 4, Chapter 9"),
    ChapterTarget("4", "27", "Ark-Code-T4-Ch27",
                  "Arkansas Business Corporation Act of 1987",
                  "Ark. Code Ann. Title 4, Chapter 27"),
    ChapterTarget("4", "38", "Ark-Code-T4-Ch38",
                  "Arkansas Uniform Limited Liability Company Act (Act 1041 of 2021)",
                  "Ark. Code Ann. Title 4, Chapter 38"),
    ChapterTarget("4", "59", "Ark-Code-T4-Ch59",
                  "Arkansas Uniform Fraudulent Transfer Act",
                  "Ark. Code Ann. Title 4, Chapter 59"),
    ChapterTarget("4", "75", "Ark-Code-T4-Ch75",
                  "Trade practices — Trade Secrets Act (§ 4-75-601) + covenants not to compete (§ 4-75-101)",
                  "Ark. Code Ann. Title 4, Chapter 75"),
    ChapterTarget("4", "88", "Ark-Code-T4-Ch88",
                  "Arkansas Deceptive Trade Practices Act (§ 4-88-101 et seq.)",
                  "Ark. Code Ann. Title 4, Chapter 88"),
    # Title 9 — family law
    ChapterTarget("9", "11", "Ark-Code-T9-Ch11",
                  "Marriage — incl. covenant marriage (§ 9-11-801 et seq.)",
                  "Ark. Code Ann. Title 9, Chapter 11"),
    ChapterTarget("9", "12", "Ark-Code-T9-Ch12",
                  "Divorce and annulment — grounds (§ 9-12-301), property (§ 9-12-315), alimony (§ 9-12-312)",
                  "Ark. Code Ann. Title 9, Chapter 12"),
    ChapterTarget("9", "13", "Ark-Code-T9-Ch13",
                  "Custody — joint-custody presumption (§ 9-13-101; Act 604 of 2021)",
                  "Ark. Code Ann. Title 9, Chapter 13"),
    ChapterTarget("9", "15", "Ark-Code-T9-Ch15",
                  "Domestic Abuse Act — orders of protection (§ 9-15-101 et seq.)",
                  "Ark. Code Ann. Title 9, Chapter 15"),
    ChapterTarget("9", "17", "Ark-Code-T9-Ch17",
                  "Uniform Interstate Family Support Act (UIFSA; § 9-17-101 et seq.)",
                  "Ark. Code Ann. Title 9, Chapter 17"),
    ChapterTarget("9", "19", "Ark-Code-T9-Ch19",
                  "Uniform Child Custody Jurisdiction and Enforcement Act (UCCJEA; § 9-19-101 et seq.)",
                  "Ark. Code Ann. Title 9, Chapter 19"),
    ChapterTarget("9", "27", "Ark-Code-T9-Ch27",
                  "Arkansas Juvenile Code — dependency-neglect, FINS, paternity, TPR",
                  "Ark. Code Ann. Title 9, Chapter 27"),
    # Title 11 — employment
    ChapterTarget("11", "3", "Ark-Code-T11-Ch3",
                  "Right to work and labor relations (§ 11-3-301 et seq.)",
                  "Ark. Code Ann. Title 11, Chapter 3"),
    ChapterTarget("11", "4", "Ark-Code-T11-Ch4",
                  "Arkansas Minimum Wage Act (§ 11-4-201 et seq.)",
                  "Ark. Code Ann. Title 11, Chapter 4"),
    ChapterTarget("11", "9", "Ark-Code-T11-Ch9",
                  "Workers' compensation — exclusive remedy (§ 11-9-101 et seq.)",
                  "Ark. Code Ann. Title 11, Chapter 9"),
    # Title 16 — practice, procedure, courts
    ChapterTarget("16", "17", "Ark-Code-T16-Ch17",
                  "District Courts — jurisdiction and civil cap (§ 16-17-704)",
                  "Ark. Code Ann. Title 16, Chapter 17"),
    ChapterTarget("16", "22", "Ark-Code-T16-Ch22",
                  "Attorneys at law — fee-shifting in civil actions (§ 16-22-308)",
                  "Ark. Code Ann. Title 16, Chapter 22"),
    ChapterTarget("16", "55", "Ark-Code-T16-Ch55",
                  "Civil Justice Reform Act of 2003 — several liability (§§ 16-55-201 to -208)",
                  "Ark. Code Ann. Title 16, Chapter 55"),
    ChapterTarget("16", "56", "Ark-Code-T16-Ch56",
                  "Limitations of actions (§ 16-56-105 (3yr); § 16-56-111 (5yr written))",
                  "Ark. Code Ann. Title 16, Chapter 56"),
    ChapterTarget("16", "62", "Ark-Code-T16-Ch62",
                  "Wrongful death and survival (§ 16-62-102)",
                  "Ark. Code Ann. Title 16, Chapter 62"),
    ChapterTarget("16", "64", "Ark-Code-T16-Ch64",
                  "Trial — modified comparative fault (§ 16-64-122)",
                  "Ark. Code Ann. Title 16, Chapter 64"),
    ChapterTarget("16", "65", "Ark-Code-T16-Ch65",
                  "Judgments — enforcement, revival, liens (§ 16-65-501)",
                  "Ark. Code Ann. Title 16, Chapter 65"),
    ChapterTarget("16", "108", "Ark-Code-T16-Ch108",
                  "Arkansas Uniform Arbitration Act (§ 16-108-201 et seq.)",
                  "Ark. Code Ann. Title 16, Chapter 108"),
    ChapterTarget("16", "114", "Ark-Code-T16-Ch114",
                  "Medical Malpractice Act — 2-year SOL (§ 16-114-203)",
                  "Ark. Code Ann. Title 16, Chapter 114"),
    ChapterTarget("16", "123", "Ark-Code-T16-Ch123",
                  "Arkansas Civil Rights Act of 1993 (§ 16-123-101 et seq.)",
                  "Ark. Code Ann. Title 16, Chapter 123"),
    # Title 17 — collection agencies
    ChapterTarget("17", "24", "Ark-Code-T17-Ch24",
                  "Collection agencies — State Board of Collection Agencies (§ 17-24-101 et seq.)",
                  "Ark. Code Ann. Title 17, Chapter 24"),
    # Title 18 — property / landlord-tenant
    ChapterTarget("18", "16", "Ark-Code-T18-Ch16",
                  "Landlord and tenant — failure to vacate (§ 18-16-101); security deposits (§ 18-16-301)",
                  "Ark. Code Ann. Title 18, Chapter 16"),
    ChapterTarget("18", "17", "Ark-Code-T18-Ch17",
                  "Residential Landlord-Tenant Act of 2007 + habitability (Act 1052 of 2021; § 18-17-501)",
                  "Ark. Code Ann. Title 18, Chapter 17"),
    ChapterTarget("18", "60", "Ark-Code-T18-Ch60",
                  "Unlawful detainer and other civil possession actions (§ 18-60-301 et seq.)",
                  "Ark. Code Ann. Title 18, Chapter 60"),
    # Title 19 — claims against the state
    ChapterTarget("19", "10", "Ark-Code-T19-Ch10",
                  "Arkansas State Claims Commission (§ 19-10-201 et seq.)",
                  "Ark. Code Ann. Title 19, Chapter 10"),
    # Title 21 — public officers / employees
    ChapterTarget("21", "1", "Ark-Code-T21-Ch1",
                  "Arkansas Whistle-Blower Act (§ 21-1-601 et seq.)",
                  "Ark. Code Ann. Title 21, Chapter 1"),
    ChapterTarget("21", "9", "Ark-Code-T21-Ch9",
                  "Immunity of political subdivisions from tort liability (§ 21-9-301)",
                  "Ark. Code Ann. Title 21, Chapter 9"),
]


# ----------------------------------------------------------------------
# HTTP.
# ----------------------------------------------------------------------

def http_get(url: str, *, retries: int = 4, base_sleep: float = 1.5,
             timeout: float = 60.0) -> bytes:
    """Fetch a URL with jittered exponential-backoff retries. Tries
    curl_cffi (Chrome TLS impersonation) first; falls back to stdlib
    urllib (which Justia will likely 403, sending the caller to the
    stub path)."""
    parsed = urllib.parse.urlsplit(url)
    safe_path = urllib.parse.quote(parsed.path, safe="/%():'.,")
    safe_url = urllib.parse.urlunsplit(
        (parsed.scheme, parsed.netloc, safe_path, parsed.query, parsed.fragment)
    )
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        from curl_cffi import requests as _cffi_requests  # type: ignore

        last_exc: Optional[BaseException] = None
        for attempt in range(retries):
            try:
                r = _cffi_requests.get(
                    safe_url, headers=headers, impersonate="chrome",
                    timeout=timeout, allow_redirects=True,
                )
                if r.status_code >= 400:
                    if r.status_code in (401, 403):
                        raise urllib.error.HTTPError(
                            safe_url, r.status_code, "blocked", r.headers, None)
                    last_exc = RuntimeError(f"HTTP {r.status_code} for {safe_url}")
                else:
                    return r.content
            except urllib.error.HTTPError:
                raise
            except Exception as e:  # noqa: BLE001
                last_exc = e
            time.sleep(base_sleep * (2 ** attempt) * (0.5 + random.random()))
        assert last_exc is not None
        raise last_exc
    except ImportError:
        req = urllib.request.Request(safe_url, headers=headers)
        last_exc = None
        for attempt in range(retries):
            try:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    return resp.read()
            except urllib.error.HTTPError as e:
                if e.code in (401, 403):
                    raise
                last_exc = e
            except Exception as e:  # noqa: BLE001
                last_exc = e
            time.sleep(base_sleep * (2 ** attempt) * (0.5 + random.random()))
        assert last_exc is not None
        raise last_exc


def get_text(url: str) -> str:
    return http_get(url).decode("utf-8", "replace")


# ----------------------------------------------------------------------
# Discovery walk (Title -> Chapter -> Subchapter -> Section).
# ----------------------------------------------------------------------

def _find(pattern: str, text: str) -> List[str]:
    seen: set[str] = set()
    out: List[str] = []
    for m in re.finditer(pattern, text):
        p = m.group(1)
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def discover_section_paths(t: ChapterTarget) -> List[str]:
    """Return ordered Justia URL paths for each section of the target
    chapter, discovered by link-walking (subtitle/subchapter-agnostic)."""
    T, C = re.escape(t.title_num), re.escape(t.chapter_num)
    # 1. Title index → chapter index path (under any subtitle).
    try:
        title_html = get_text(f"{JUSTIA_BASE}title-{t.title_num}/")
    except Exception:  # noqa: BLE001
        return []
    chapter_paths = _find(
        rf'href="(/codes/arkansas/(?:\d{{4}}/)?title-{T}/'
        rf'(?:subtitle-[^"/]+/)?chapter-{C}/)"',
        title_html,
    )
    if not chapter_paths:
        # Fall back to the conventional no-subtitle path.
        chapter_paths = [f"/codes/arkansas/title-{t.title_num}/chapter-{t.chapter_num}/"]

    section_re = (
        rf'href="(/codes/arkansas/(?:\d{{4}}/)?title-{T}/[^"]*'
        rf'section-{T}-{C}-[^"#?]+)"'
    )
    subchapter_re = (
        rf'href="(/codes/arkansas/(?:\d{{4}}/)?title-{T}/[^"]*'
        rf'chapter-{C}/(?:subtitle-[^"/]+/)?subchapter-[^"/]+/)"'
    )

    sections: List[str] = []
    seen: set[str] = set()

    def collect(paths: List[str]) -> None:
        for p in paths:
            if p not in seen:
                seen.add(p)
                sections.append(p)

    for cpath in chapter_paths:
        try:
            chap_html = get_text(f"https://law.justia.com{cpath}")
        except Exception:  # noqa: BLE001
            continue
        collect(_find(section_re, chap_html))
        # Chapters subdivided into subchapters: walk each.
        for sub in _find(subchapter_re, chap_html):
            try:
                sub_html = get_text(f"https://law.justia.com{sub}")
            except Exception:  # noqa: BLE001
                continue
            collect(_find(section_re, sub_html))
    return sections


# ----------------------------------------------------------------------
# Justia section HTML → Markdown.
# ----------------------------------------------------------------------

SECTION_BODY_ID_RE = re.compile(
    r'<div\b[^>]*\bid="codes-content"[^>]*>(.*?)</div>',
    re.DOTALL | re.IGNORECASE)
SECTION_BODY_CLASS_RE = re.compile(
    r'<div[^>]*\bclass="[^"]*\b(?:codes-content|content-body|code-section)\b'
    r'[^"]*"[^>]*>(.*?)</div>', re.DOTALL | re.IGNORECASE)


def _strip_to_md(chunk: str) -> str:
    s = re.sub(r"<script\b[^>]*>.*?</script>", "", chunk, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r"<style\b[^>]*>.*?</style>", "", s, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r"<p\b[^>]*>", "\n\n", s, flags=re.IGNORECASE)
    s = re.sub(r"</p>", "", s, flags=re.IGNORECASE)
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.IGNORECASE)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    out: List[str] = []
    for para in re.split(r"\n\s*\n", s):
        para = re.sub(r"[ \t]+", " ", para).strip()
        if para:
            out.append(para)
    return "\n\n".join(out)


def parse_section_page(html_text: str) -> Tuple[str, str]:
    heading = ""
    ogm = re.search(r'<meta\s+property="og:title"\s+content="([^"]+)"',
                    html_text, re.IGNORECASE)
    if ogm:
        parts = [p.strip() for p in html.unescape(ogm.group(1)).split("::")]
        section_part = next(
            (p for p in reversed(parts) if re.match(r"^Section\s+\S", p, re.IGNORECASE)),
            None)
        if section_part:
            heading = section_part
    if not heading:
        tm = re.search(r"<title>\s*([^<]+?)\s*\|\s*Justia", html_text, re.IGNORECASE)
        heading = tm.group(1).strip() if tm else "Section"
    bm = SECTION_BODY_ID_RE.search(html_text) or SECTION_BODY_CLASS_RE.search(html_text)
    body_md = _strip_to_md(bm.group(1)) if bm else ""
    return heading, body_md


# ----------------------------------------------------------------------
# Render.
# ----------------------------------------------------------------------

HEADER = """# {h1} — {topic}

> **Source:** {source}
> **Fetched:** {fetched}
> **Format:** verbatim conversion of the Justia HTML mirror at
> `law.justia.com/codes/arkansas/`

> **NOT LEGAL ADVICE.** Generated content is a drafting aid; verify
> against the current Ark. Code Ann. before filing.

---

"""

STUB_MARKER = "<!-- claude-legal:ar-statutes-pointer-stub -->"


def render_chapter_md(t: ChapterTarget, fetched_iso: str,
                      sections: List[Tuple[str, str]]) -> str:
    parts = [f"## {h.strip() or 'Section'}\n\n{b}".rstrip() for h, b in sections]
    body = re.sub(r"\n{3,}", "\n\n", "\n\n".join(parts) + "\n")
    return HEADER.format(
        h1=t.h1, topic=t.topic,
        source=f"{JUSTIA_BASE}title-{t.title_num}/", fetched=fetched_iso,
    ) + body


def render_stub(t: ChapterTarget, fetched_iso: str, reason: str) -> str:
    return (
        f"# {t.h1} — {t.topic}\n\n{STUB_MARKER}\n\n"
        f"> **Status:** pointer stub — verbatim text not retrieved this run.\n"
        f"> **Reason:** {reason}\n"
        f"> **Canonical:** {JUSTIA_BASE}title-{t.title_num}/ "
        f"(walk to Chapter {t.chapter_num})\n"
        f"> **Fetched:** {fetched_iso}\n\n"
        f"> **NOT LEGAL ADVICE.** Read the authoritative text at the "
        f"canonical Justia URL (or the official LexisNexis Arkansas Code). "
        f"Re-run `scripts/pull_arkansas_statutes.py` from an environment "
        f"where Justia is reachable; the `_file_is_stub` guard will replace "
        f"this stub with the fetched text.\n\n"
        f"## Scope\n\n{t.topic}\n"
    )


def _file_is_stub(p: Path) -> bool:
    if not p.exists():
        return True
    try:
        txt = p.read_text(encoding="utf-8")
    except OSError:
        return True
    return (STUB_MARKER in txt or "pointer stub" in txt.lower()
            or "verbatim text not retrieved" in txt.lower())


@dataclass
class WriteResult:
    label: str
    sections: int
    stub: bool
    error: Optional[str]


def fetch_chapter(t: ChapterTarget, out_dir: Path, fetched_iso: str,
                  stubs_only: bool) -> WriteResult:
    out_path = out_dir / f"{t.label}.md"

    def write(text: str) -> None:
        tmp = out_path.with_suffix(".md.tmp")
        tmp.write_text(text, encoding="utf-8")
        tmp.replace(out_path)

    if stubs_only:
        if not _file_is_stub(out_path):
            return WriteResult(t.label, 0, False, "kept existing verbatim file")
        write(render_stub(t, fetched_iso, "stubs-only run"))
        return WriteResult(t.label, 0, True, "stubs-only")

    try:
        paths = discover_section_paths(t)
        if not paths:
            raise RuntimeError("no section links discovered (blocked or empty index)")
        sections: List[Tuple[str, str]] = []
        for p in paths:
            try:
                heading, body = parse_section_page(get_text(f"https://law.justia.com{p}"))
            except Exception as e:  # noqa: BLE001
                heading, body = ("Section", f"_(could not retrieve: {e})_")
            sections.append((heading, body))
            time.sleep(0.2 + random.random() * 0.3)
        empty = sum(1 for _, b in sections if "could not retrieve" in b or not b.strip())
        if empty >= max(1, int(len(sections) * 0.5)):
            raise RuntimeError(f"section pages blocked or empty ({empty}/{len(sections)})")
        write(render_chapter_md(t, fetched_iso, sections))
        return WriteResult(t.label, len(sections), False, None)
    except Exception as exc:  # noqa: BLE001
        if out_path.exists() and not _file_is_stub(out_path):
            return WriteResult(t.label, 0, False, f"fetch failed (kept existing file): {exc}")
        write(render_stub(t, fetched_iso, str(exc)))
        return WriteResult(t.label, 0, True, str(exc))


def update_manifest(out_dir: Path, fetched_iso: str, version: str = "0.1.0") -> Path:
    mp = out_dir / "_manifest.json"
    mp.write_text(json.dumps({
        "version": version,
        "last_pulled": fetched_iso,
        "source": "https://law.justia.com/codes/arkansas/",
        "notes": (
            "Pulled by scripts/pull_arkansas_statutes.py. The Arkansas Code "
            "Annotated has no clean structured free official source "
            "(LexisNexis publishes the official annotated code under "
            "copyright). Justia is the primary structured free mirror for "
            "the public-domain section text. The puller discovers section "
            "URLs by walking Title -> Chapter -> Subchapter -> Section links "
            "(subtitle/subchapter-agnostic) rather than constructing them. "
            "Justia sits behind Cloudflare bot-fight mode and 403s against "
            "stdlib urllib and many shared-egress IPs; the puller uses "
            "curl_cffi with Chrome TLS impersonation when available and "
            "falls back to well-formed pointer stubs when fetch fails. The "
            "_file_is_stub guard preserves committed verbatim content."
        ),
    }, indent=2) + "\n", encoding="utf-8")
    return mp


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=Path(
        "plugins/ar-court-docs/skills/ar-law-references/references/ar-statutes-debt"))
    ap.add_argument("--only", nargs="*", help="Restrict to these chapter labels.")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--stubs-only", action="store_true",
                    help="Write pointer stubs only — no network fetch.")
    ap.add_argument("--manifest-version", default="0.1.0")
    args = ap.parse_args()

    out_dir: Path = args.out
    out_dir.mkdir(parents=True, exist_ok=True)
    only = set(args.only) if args.only else None
    targets = [t for t in TARGETS if only is None or t.label in only]
    if not targets:
        print(f"!! no targets match --only {args.only!r}", file=sys.stderr)
        return 2

    fetched_iso = date.today().isoformat()
    print(f"=== pulling {len(targets)} AR chapter(s) → {out_dir} "
          f"(workers={args.workers}, stubs_only={args.stubs_only})", flush=True)

    results: List[WriteResult] = []
    workers = max(1, min(args.workers, len(targets)))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futs = {pool.submit(fetch_chapter, t, out_dir, fetched_iso, args.stubs_only): t
                for t in targets}
        for fut in as_completed(futs):
            t = futs[fut]
            try:
                results.append(fut.result())
            except Exception as exc:  # noqa: BLE001
                results.append(WriteResult(t.label, 0, True, str(exc)))

    by_label = {r.label: r for r in results}
    fail = 0
    for t in targets:
        r = by_label.get(t.label)
        if r is None:
            continue
        tag = "OK  " if (r.error is None and not r.stub) else ("STUB" if r.stub else "FAIL")
        if r.stub and "kept existing" not in (r.error or ""):
            pass
        print(f"     [{tag}] {t.label}.md ({r.sections} sec)"
              + (f" — {r.error}" if r.error else ""), flush=True)
        if r.error and "kept existing" not in r.error and not r.stub:
            fail += 1

    if only is None:
        mp = update_manifest(out_dir, fetched_iso, args.manifest_version)
        print(f"=== updated {mp}", flush=True)
    return 0 if not fail else 1


if __name__ == "__main__":
    sys.exit(main())
