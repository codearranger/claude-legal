#!/usr/bin/env python3
"""Pull the Foreign Affairs Manual (FAM) — immigration-relevant volumes.

The FAM is the U.S. Department of State's internal guidance, published at
https://fam.state.gov. For immigration practice the relevant volumes are:

  - 9 FAM  — Visas (nonimmigrant + immigrant visa adjudication; the
             Department's interpretation of INA admissibility/ineligibility,
             e.g. 9 FAM 302 ineligibilities, 9 FAM 402 NIV classifications,
             9 FAM 502/504 IV processing). The single most-cited FAM volume
             for immigration lawyers.
  - 8 FAM  — Nationality and Naturalization (acquisition/derivation of U.S.
             citizenship). Only chapter 300 (U.S. Citizenship and Nationality)
             carries substantive public text; the rest of the volume is marked
             "UNAVAILABLE" (SBU/redacted) upstream.
  - 7 FAM  — Consular Affairs (citizen services abroad). Most of the volume is
             consular-protection material tangential to immigration; this
             puller scopes to the overview (000) and the documentation of major
             life events / Consular Reports of Birth Abroad (1400).

## The two things that used to make this corpus "unmirrorable" — both solved

1. **Incomplete TLS chain (missing intermediate).** fam.state.gov serves ONLY
   its leaf certificate and omits the issuing intermediate ("Sectigo Public
   Server Authentication CA OV R36"). A browser repairs this transparently by
   *AIA fetching* — reading the leaf's Authority Information Access "CA Issuers"
   URL and downloading the intermediate. Python's `ssl` does NOT AIA-chase, so a
   default `urlopen` fails with `CERTIFICATE_VERIFY_FAILED` / "unable to get
   local issuer certificate". This is the server's own misconfiguration, NOT a
   proxy or bot-gate — and it is fixable from any machine: `build_ssl_context()`
   below opens an unverified handshake, reads the leaf's AIA URL, fetches the
   intermediate, and adds it to a verify bundle (certifi roots + intermediate).

2. **Stale URL scheme.** The old `/fam/09fam.html` paths are dead (404). The
   site is now an ASP.NET/Kendo app whose table of contents is served as JSON
   from `/api/Tree/GetTreeByVolumeId?Id=<vol>`, and whose per-section content
   lives at `/FAM/<vol>/<sectionId>.html` (note the UPPERCASE `/FAM/`). The
   pages are Word-exported HTML in **windows-1252**, content inside a
   `<div class=WordSection1>` — the same shape `pull_oregon_ors.py` handles.

When the fetch succeeds the puller writes verbatim Markdown; when the network
is genuinely unreachable (e.g. an air-gapped CI runner) it falls back to a
**well-formed pointer stub**. The `_file_is_stub` guard means a stub-only or
blocked re-run will NOT clobber verbatim content a previous successful run
committed.

Output: plugins/claude-legal-immigration-laws/references/foreign-affairs-manual/
"""

from __future__ import annotations

import argparse
import json
import random
import re
import socket
import ssl
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

FAM_BASE = "https://fam.state.gov"
HOST = "fam.state.gov"
TREE_API = FAM_BASE + "/api/Tree/GetTreeByVolumeId?Id={vol}"
VOLUME_DETAILS = FAM_BASE + "/Volumes/Details/{vol}"

# Last-resort intermediate URL if AIA discovery off the live leaf fails.
# (Primary path is to read the AIA "CA Issuers" URL out of the leaf cert.)
FALLBACK_INTERMEDIATE_URL = (
    "http://crt.sectigo.com/SectigoPublicServerAuthenticationCAOVR36.crt"
)

# Row: (out_file, title, volume, id_prefixes, scope).
#   volume       — Kendo volume id for the tree API (e.g. "09FAM").
#   id_prefixes  — tuple of section-id prefixes to include; None = whole volume.
#                  Section ids are zero-padded, so "09FAM0302" selects 9 FAM 302.x,
#                  "09FAM01" selects 9 FAM chapter 100, "08FAM03" selects 8 FAM 300.
FamRow = tuple[str, str, str, "tuple[str, ...] | None", str]
FAM_TARGETS: list[FamRow] = [
    ("09FAM-visas-overview", "9 FAM 100 — Visas (overview)", "09FAM", ("09FAM01",),
     "The Department of State's visa-adjudication manual, introductory chapter: "
     "what a visa is, visa-related roles, definitions, and Visa Office points of "
     "contact."),
    ("09FAM-302-ineligibilities", "9 FAM 302 — Ineligibilities and Waivers", "09FAM",
     ("09FAM0302",),
     "Section-by-section treatment of the INA § 212(a) inadmissibility grounds "
     "(documentation, criminal, security, public charge, misrepresentation, "
     "unlawful presence, etc.) and the corresponding waivers, as applied in visa "
     "adjudication by consular officers."),
    ("09FAM-402-niv-classifications", "9 FAM 402 — Nonimmigrant Visa Classifications",
     "09FAM", ("09FAM0402",),
     "Classification-by-classification guidance for nonimmigrant visa categories "
     "(B, F, H, L, O, P, etc.): eligibility, documentary requirements, and "
     "adjudication standards."),
    ("09FAM-502-504-iv-processing", "9 FAM 502 / 504 — Immigrant Visa Categories and Processing",
     "09FAM", ("09FAM0502", "09FAM0504"),
     "Immigrant visa categories (family-based, employment-based, diversity) and "
     "the National Visa Center / consular immigrant-visa processing workflow."),
    ("08FAM-nationality", "8 FAM 300 — U.S. Citizenship and Nationality", "08FAM",
     ("08FAM03",),
     "Acquisition and derivation of U.S. citizenship as determined by the "
     "Department of State (birth in/out of the U.S., transmission requirements, "
     "derivation, expatriation, Consular Reports of Birth Abroad). The only "
     "substantive public chapter of 8 FAM; the rest is SBU/redacted upstream."),
    # NB: 7 FAM uses a shorter section-id scheme than 8/9 FAM — chapter 000
    # leaves are "07FAM0010".."07FAM0090" and chapter 1400 leaves are
    # "07FAM14NN", so the prefixes are "07FAM00" / "07FAM14" (not "07FAM0000").
    ("07FAM-consular-affairs", "7 FAM 000 / 1400 — Consular Affairs (citizen services)",
     "07FAM", ("07FAM00", "07FAM14"),
     "Consular protection of U.S. nationals abroad (overview) and documentation "
     "of major life events, including Consular Reports of Birth Abroad and "
     "related citizen-services guidance."),
]


# ----------------------------------------------------------------------
# TLS — AIA-chase the missing Sectigo intermediate so the leaf verifies.
# ----------------------------------------------------------------------

def _extract_aia_url(leaf_der: bytes) -> str | None:
    """Find the AIA 'CA Issuers' URL embedded in the leaf certificate.

    The URL appears as a plain IA5String inside the DER and reliably ends in
    .crt/.cer/.p7c, so a byte-regex extracts it without a full X.509 parser
    (stdlib `ssl` exposes no extension parser). Falls back to None."""
    m = re.search(rb"https?://[ -~]+?\.(?:crt|cer|p7c)", leaf_der)
    return m.group(0).decode("ascii") if m else None


def _base_context() -> ssl.SSLContext:
    """A verifying context seeded with the widest available root set: certifi if
    installed (most reliable across platforms), else the system default store."""
    try:
        import certifi  # optional — preferred when present
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:  # noqa: BLE001 — no certifi: fall back to system roots
        return ssl.create_default_context()


def _fetch_intermediate_pem(cache: Path, *, timeout: float) -> str:
    """Return the PEM of the intermediate fam.state.gov omits, fetching it via
    AIA discovery off the live leaf cert (cached under `cache/`)."""
    cache.mkdir(parents=True, exist_ok=True)
    cached = cache / "fam-intermediate.pem"
    if cached.exists() and cached.stat().st_size > 500:
        return cached.read_text(encoding="ascii")

    # Pull the leaf cert via an UNVERIFIED handshake. This is safe: we read ONLY
    # the leaf's bytes (never any response data) to discover its AIA URL. All
    # content is fetched later through the fully-verified context, and
    # build_ssl_context() ends with a verifying handshake — a forged intermediate
    # would fail there, so TLS verification is preserved for everything we mirror.
    unverified = ssl._create_unverified_context()  # noqa: SLF001
    with socket.create_connection((HOST, 443), timeout=timeout) as sock:
        with unverified.wrap_socket(sock, server_hostname=HOST) as tls:
            leaf_der = tls.getpeercert(binary_form=True)

    aia_url = _extract_aia_url(leaf_der) or FALLBACK_INTERMEDIATE_URL
    print(f"  TLS fix: fetching omitted intermediate from {aia_url}", flush=True)
    req = urllib.request.Request(aia_url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        intermediate_pem = ssl.DER_cert_to_PEM_cert(resp.read())
    tmp = cached.with_suffix(".pem.tmp")
    tmp.write_text(intermediate_pem, encoding="ascii")
    tmp.replace(cached)
    return intermediate_pem


def build_ssl_context(cache: Path, *, timeout: float = 30.0) -> ssl.SSLContext:
    """Return an SSLContext that trusts the standard roots PLUS the AIA-fetched
    Sectigo intermediate fam.state.gov omits from its served chain.

    The intermediate is added with `load_verify_locations(cadata=...)`, so it
    augments (never replaces) the root set and no on-disk bundle is assembled.
    """
    ctx = _base_context()
    ctx.load_verify_locations(cadata=_fetch_intermediate_pem(cache, timeout=timeout))
    # Sanity check: the leaf must now verify against roots + intermediate.
    with socket.create_connection((HOST, 443), timeout=timeout) as sock:
        with ctx.wrap_socket(sock, server_hostname=HOST):
            pass
    return ctx


# ----------------------------------------------------------------------
# Networking — jittered exponential backoff (matches pull_oregon_ors.py).
# ----------------------------------------------------------------------

def http_get_bytes(url: str, ctx: ssl.SSLContext, *, retries: int = 4,
                   base_sleep: float = 1.5, timeout: float = 40.0) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    last_exc: BaseException | None = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
                return resp.read()
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            last_exc = exc
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
        sleep_for = base_sleep * (2 ** attempt) * (0.5 + random.random())
        time.sleep(sleep_for)
    assert last_exc is not None
    raise last_exc


# ----------------------------------------------------------------------
# Tree API — enumerate the section leaves of a volume.
# ----------------------------------------------------------------------

def fetch_leaves(vol: str, ctx: ssl.SSLContext) -> list[dict]:
    """Return the flat, in-order list of leaf nodes (id, text, url) for a volume."""
    raw = http_get_bytes(TREE_API.format(vol=vol), ctx)
    tree = json.loads(raw.decode("utf-8", "replace"))
    leaves: list[dict] = []

    def walk(node: dict) -> None:
        items = node.get("items") or []
        if not items:
            leaves.append(node)
        for child in items:
            walk(child)

    for node in tree:
        walk(node)
    return leaves


# ----------------------------------------------------------------------
# HTML -> Markdown — Word-exported windows-1252 page, content in WordSection1.
# ----------------------------------------------------------------------

# A FAM section heading text starts with the section number, e.g.
# "9 FAM 302.1-1(A) (U) Statutory and regulatory authority" or the chapter
# header "9 fam 302 (U) grounds of ineligibility". Headings are CSS-styled
# (class MsoHeadingN), not <b>-wrapped, so we promote by text shape.
FAM_HEADING_RE = re.compile(r"^\d{1,2}\s+FAM\s+\d", re.IGNORECASE)
# Boilerplate that repeats at the top/bottom of every section page.
NOISE_RE = re.compile(r"^\(?U\)?\s*UNCLASSIFIED\s*\(?U?\)?$|^UNCLASSIFIED(\s*\(U\))?$",
                      re.IGNORECASE)


class _FamWalker(HTMLParser):
    """Yield one (is_heading, text) record per block element in WordSection1.

    Treats <p>, <td>, <th> and <li> as block boundaries (FAM lays content out in
    Word paragraphs, sometimes inside layout tables). Tolerant of malformed Word
    HTML; convert_charrefs decodes &nbsp; / &#... automatically."""

    BLOCKS = {"p", "td", "th", "li"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.records: list[tuple[bool, str]] = []
        self._in_block = False
        self._chunks: list[str] = []

    def handle_starttag(self, tag, attrs):  # type: ignore[override]
        tag = tag.lower()
        if tag in self.BLOCKS:
            if self._in_block:
                self._flush()
            self._in_block = True
            self._chunks = []
        elif tag == "br" and self._in_block:
            self._chunks.append(" ")

    def handle_endtag(self, tag):  # type: ignore[override]
        if tag.lower() in self.BLOCKS and self._in_block:
            self._flush()

    def handle_data(self, data):  # type: ignore[override]
        if self._in_block:
            self._chunks.append(data)

    def _flush(self) -> None:
        text = "".join(self._chunks).replace("\xa0", " ").replace("\xad", "")
        text = re.sub(r"\s+", " ", text).strip()
        self._in_block = False
        self._chunks = []
        if not text or NOISE_RE.match(text):
            return
        self.records.append((bool(FAM_HEADING_RE.match(text)), text))


def _slice_wordsection(html: str) -> str:
    """Return the HTML from the WordSection1 container to end-of-body."""
    idx = html.find("WordSection1")
    if idx == -1:
        # Some pages may not use the class; fall back to <body>.
        body = re.search(r"(?is)<body[^>]*>", html)
        idx = body.end() if body else 0
    region = html[idx:]
    end = region.lower().rfind("</body>")
    if end != -1:
        region = region[:end]
    region = re.sub(r"(?is)<style\b[^>]*>.*?</style>", " ", region)
    region = re.sub(r"(?is)<script\b[^>]*>.*?</script>", " ", region)
    region = re.sub(r"(?s)<!--.*?-->", " ", region)
    return region


def page_to_markdown(raw: bytes) -> str:
    """Reduce one FAM section page (windows-1252 Word HTML) to Markdown body."""
    html = raw.decode("windows-1252", errors="replace")
    parser = _FamWalker()
    parser.feed(_slice_wordsection(html))
    if parser._in_block:  # noqa: SLF001 — final flush
        parser._flush()  # noqa: SLF001

    out: list[str] = []
    prev = None
    for is_heading, text in parser.records:
        if text == prev:  # collapse the duplicated header/footer lines
            continue
        prev = text
        if is_heading:
            out.append("")
            out.append(f"#### {text}")
            out.append("")
        else:
            out.append(text)
            out.append("")
    body = "\n".join(out).strip()
    return re.sub(r"\n{3,}", "\n\n", body)


# ----------------------------------------------------------------------
# Stub fallback (preserved for genuinely-unreachable environments).
# ----------------------------------------------------------------------

STUB_MARKER = "<!-- claude-legal:fam-pointer-stub -->"


def _file_is_stub(path: Path) -> bool:
    if not path.exists():
        return True
    try:
        return STUB_MARKER in path.read_text(encoding="utf-8")
    except OSError:
        return True


def make_stub(title: str, vol: str, scope: str, reason: str) -> str:
    today = date.today().isoformat()
    return (
        f"# {title}\n\n"
        f"{STUB_MARKER}\n\n"
        f"- Citation: Foreign Affairs Manual (FAM), U.S. Department of State\n"
        f"- Canonical URL: {VOLUME_DETAILS.format(vol=vol)}\n"
        f"- Status: **pointer stub** — verbatim text not mirrored\n"
        f"- Pulled: {today}\n\n"
        f"> **Why a stub?** This run could not reach fam.state.gov "
        f"({reason}). The puller AIA-chases fam.state.gov's omitted TLS "
        f"intermediate and crawls its JSON table-of-contents API, so a stub "
        f"here means the network itself was unreachable (e.g. an air-gapped "
        f"runner), not a TLS or URL problem. Read the authoritative text at the "
        f"canonical URL above, or re-run `scripts/pull_fam.py` from a host with "
        f"egress to fam.state.gov; the `_file_is_stub` guard will replace this "
        f"stub with the fetched text.\n\n"
        f"## Scope\n\n{scope}\n\n"
        f"## Note on FAM authority\n\n"
        f"The FAM is internal Department of State guidance. It is **not** binding "
        f"law and does not create enforceable rights, but it is highly persuasive "
        f"of the agency's interpretation of the INA and 22 CFR and is routinely "
        f"cited in visa-refusal and consular-processing matters. Always pair a "
        f"FAM cite with the controlling statute (INA / 8 U.S.C.) and regulation "
        f"(8 CFR / 22 CFR).\n"
    )


# ----------------------------------------------------------------------
# Rendering one target file from its selected section leaves.
# ----------------------------------------------------------------------

def render_target(title: str, vol: str, scope: str,
                  sections: list[tuple[dict, str]]) -> str:
    today = date.today().isoformat()
    out: list[str] = [
        f"# {title}",
        "",
        f"- Citation: Foreign Affairs Manual (FAM), U.S. Department of State",
        f"- Volume index: {VOLUME_DETAILS.format(vol=vol)}",
        f"- Sections mirrored: {len(sections)}",
        f"- Pulled: {today}",
        "",
        "> Verbatim text reduced from fam.state.gov Word-exported HTML "
        "(windows-1252). The FAM is agency guidance, not binding law.",
        "",
        "## Scope",
        "",
        scope,
        "",
        "---",
        "",
    ]
    for node, md in sections:
        src = node.get("url") or ""
        src_url = src if src.startswith("http") else FAM_BASE + src
        out.append(f"## {node['text'].strip()}")
        out.append("")
        out.append(f"*Source: {src_url}*")
        out.append("")
        out.append(md if md.strip() else "_(No public text — section marked "
                                         "Unavailable/redacted upstream.)_")
        out.append("")
        out.append("---")
        out.append("")
    text = "\n".join(out).rstrip() + "\n"
    return re.sub(r"\n{3,}", "\n\n", text)


# ----------------------------------------------------------------------
# Main.
# ----------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out",
        default="plugins/claude-legal-immigration-laws/references/foreign-affairs-manual",
    )
    ap.add_argument("--cache", default="/tmp/claude-legal-cache",
                    help="Where to cache the assembled TLS bundle.")
    ap.add_argument("--workers", type=int, default=4,
                    help="Concurrent section-page fetches.")
    ap.add_argument("--stubs-only", action="store_true",
                    help="Skip the network entirely and (re)write pointer stubs.")
    ap.add_argument("--only", nargs="*",
                    help="Limit to out-file tokens (e.g. 09FAM-302-ineligibilities).")
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    only = set(args.only) if args.only else None
    targets = [t for t in FAM_TARGETS if not only or t[0] in only]

    ctx: ssl.SSLContext | None = None
    blocked_reason = ""
    if not args.stubs_only:
        try:
            ctx = build_ssl_context(Path(args.cache))
        except Exception as exc:  # noqa: BLE001
            blocked_reason = f"TLS context build failed: {exc}"
            print(f"  ! {blocked_reason}", flush=True)

    # Fetch each needed volume's tree once.
    trees: dict[str, list[dict]] = {}
    if ctx is not None:
        for vol in {t[2] for t in targets}:
            try:
                trees[vol] = fetch_leaves(vol, ctx)
                print(f"  tree {vol}: {len(trees[vol])} leaves", flush=True)
            except Exception as exc:  # noqa: BLE001
                blocked_reason = f"tree fetch failed for {vol}: {exc}"
                print(f"  ! {blocked_reason}", flush=True)

    wrote_verbatim = wrote_stub = preserved = 0
    for (out_file, title, vol, prefixes, scope) in targets:
        path = out_dir / f"{out_file}.md"
        leaves = trees.get(vol)
        selected = None
        if leaves is not None:
            if prefixes is None:
                selected = list(leaves)
            else:
                selected = [n for n in leaves
                            if any(n["id"].startswith(p) for p in prefixes)]

        if selected:
            def fetch_one(node: dict) -> tuple[dict, str]:
                url = node["url"]
                full = url if url.startswith("http") else FAM_BASE + url
                return node, page_to_markdown(http_get_bytes(full, ctx))  # type: ignore[arg-type]

            results: dict[str, tuple[dict, str]] = {}
            with ThreadPoolExecutor(max_workers=args.workers) as ex:
                futs = {ex.submit(fetch_one, n): n["id"] for n in selected}
                for fut in as_completed(futs):
                    try:
                        node, md = fut.result()
                        results[node["id"]] = (node, md)
                    except Exception as exc:  # noqa: BLE001
                        print(f"  ! section {futs[fut]} failed: {exc}", flush=True)
            ordered = [results[n["id"]] for n in selected if n["id"] in results]
            if ordered:
                md = render_target(title, vol, scope, ordered)
                tmp = path.with_suffix(".md.tmp")
                tmp.write_text(md, encoding="utf-8")
                tmp.replace(path)
                wrote_verbatim += 1
                print(f"  wrote VERBATIM {path} "
                      f"({len(ordered)}/{len(selected)} sections, {len(md):,} bytes)",
                      flush=True)
                continue

        # Could not mirror this target — preserve verbatim or write a stub.
        if not _file_is_stub(path):
            preserved += 1
            print(f"  preserved existing verbatim {path}", flush=True)
            continue
        reason = blocked_reason or "no sections matched / network unreachable"
        tmp = path.with_suffix(".md.tmp")
        tmp.write_text(make_stub(title, vol, scope, reason), encoding="utf-8")
        tmp.replace(path)
        wrote_stub += 1
        print(f"  wrote STUB {path}", flush=True)

    mode = "verbatim" if wrote_stub == 0 and wrote_verbatim else (
        "stub" if wrote_verbatim == 0 else "mixed")
    manifest = {
        "version": "0.2.0",
        "last_pulled": date.today().isoformat(),
        "source": FAM_BASE,
        "mode": mode,
        "notes": (
            "Pulled by scripts/pull_fam.py. The puller AIA-chases the Sectigo "
            "intermediate fam.state.gov omits from its TLS chain, then crawls the "
            "site's JSON table-of-contents API (/api/Tree/GetTreeByVolumeId) and "
            "the per-section /FAM/<vol>/<id>.html pages (windows-1252 Word HTML). "
            "Writes pointer stubs only when the network is unreachable; the "
            "_file_is_stub guard preserves committed verbatim content."
        ),
    }
    (out_dir / "_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Done. verbatim={wrote_verbatim} stub={wrote_stub} "
          f"preserved={preserved} mode={mode}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
