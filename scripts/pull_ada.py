#!/usr/bin/env python3
"""Pull the Americans with Disabilities Act statute and its implementing regulations.

This is the ADA companion to ``pull_federal_debt_laws.py``: same USLM-XML and
eCFR-versioner rendering, scoped to the disability-rights corpus served from
https://www.ada.gov/law-and-regs/.

Statute (uscode.house.gov USLM XML, release point Public Law 119-84):
  - ADA = Title 42 Chapter 126 — Equal Opportunity for Individuals with
    Disabilities (42 U.S.C. §§ 12101–12213). Rendered as one file so the
    chapter-level general provisions (§ 12101 findings/purpose, § 12102
    definition of "disability" as amended by the ADA Amendments Act of 2008,
    § 12103 additional definitions) stay with the four titles they govern:
      · Subchapter I  — Employment (Title I; §§ 12111–12117)
      · Subchapter II — Public Services (Title II; §§ 12131–12165)
      · Subchapter III— Public Accommodations (Title III; §§ 12181–12189)
      · Subchapter IV — Miscellaneous Provisions (Title V; §§ 12201–12213)
    (ADA Title IV — telecommunications relay services — amended the
    Communications Act at 47 U.S.C. § 225 and is not part of chapter 126.)

Regulations (ecfr.gov XML versioner API):
  - 29 C.F.R. Part 1630 — EEOC regulation implementing ADA Title I (employment)
  - 28 C.F.R. Part 35   — DOJ regulation implementing ADA Title II (state/local
    government)
  - 28 C.F.R. Part 36   — DOJ regulation implementing ADA Title III (public
    accommodations); its appendices carry the 2010 ADA Standards for Accessible
    Design (figures flatten to text; dimensional specs are preserved)

Output: plugins/claude-legal-federal-laws/references/ada-laws/
"""

from __future__ import annotations

import argparse
import io
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from datetime import date
from pathlib import Path

USER_AGENT = "claude-legal/1.0 (+https://github.com/codearranger/claude-legal) ada-puller"

# USC USLM release point. Every USC title is republished at every release
# point, so one constant suffices. To refresh, browse
# https://uscode.house.gov/download/releasepoints.shtml and bump this.
USC_RELEASE = "119-84"
USC_RELEASE_CONGRESS, USC_RELEASE_PUBLAW = USC_RELEASE.split("-", 1)
USC_ZIP_URL_TMPL = (
    "https://uscode.house.gov/download/releasepoints/us/pl/"
    f"{USC_RELEASE_CONGRESS}/{USC_RELEASE_PUBLAW}/"
    "xml_usc{title}@" + USC_RELEASE + ".zip"
)

# eCFR uses an "as-of" date; we pick the most recent fixed date for stable output.
ECFR_AS_OF = "2026-01-01"
ECFR_BASE = "https://www.ecfr.gov/api/versioner/v1/full"

# Target row: (usc_title, chapter, subchapter_or_None, short_name, citation,
#              full_title). subchapter None means "render the whole chapter".
USCRow = tuple[str, str, str | None, str, str, str]
USC_TARGETS: list[USCRow] = [
    ("42", "ch126", None, "ADA", "42 U.S.C. §§ 12101–12213",
     "Americans with Disabilities Act of 1990"),
]

# Regulation row: (cfr_title, part, short, full_title).
CFRRow = tuple[str, str, str, str]
CFR_PARTS: list[CFRRow] = [
    ("29", "1630", "EEOC-Title-I-29-CFR-1630",
     "EEOC Regulation to Implement the Equal Employment Provisions of the ADA (Title I)"),
    ("28", "35", "DOJ-Title-II-28-CFR-35",
     "DOJ Nondiscrimination on the Basis of Disability in State and Local Government Services (Title II)"),
    ("28", "36", "DOJ-Title-III-28-CFR-36",
     "DOJ Nondiscrimination on the Basis of Disability by Public Accommodations and in Commercial Facilities (Title III) — incl. 2010 ADA Standards for Accessible Design"),
]

USLM_NS = "http://xml.house.gov/schemas/uslm/1.0"


def http_get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def get_usc_xml(title: str, cache: Path) -> Path:
    """Download and unzip the USLM XML for a given USC title if not already cached."""
    cache.mkdir(parents=True, exist_ok=True)
    xml_path = cache / f"usc{title}@{USC_RELEASE}.xml"
    if xml_path.exists() and xml_path.stat().st_size > 100_000:
        return xml_path
    url = USC_ZIP_URL_TMPL.format(title=title)
    print(f"  downloading {url}", flush=True)
    zip_bytes = http_get(url)
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        names = [n for n in zf.namelist() if n.endswith(".xml")]
        if not names:
            raise RuntimeError(f"no XML inside {url}")
        with zf.open(names[0]) as src, open(xml_path, "wb") as dst:
            dst.write(src.read())
    return xml_path


# ----- USLM → Markdown -----------------------------------------------------------------

def localname(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def text_of(elem: ET.Element) -> str:
    """Concatenate all text in an element with single spaces; preserve inline structure."""
    parts: list[str] = []
    if elem.text:
        parts.append(elem.text)
    for child in elem:
        ln = localname(child.tag)
        if ln == "ref":
            parts.append(text_of(child))
        elif ln == "note":
            continue
        else:
            parts.append(text_of(child))
        if child.tail:
            parts.append(child.tail)
    return "".join(parts)


def normalize(s: str) -> str:
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\s*\n\s*", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def render_block(elem: ET.Element, depth: int = 0) -> list[str]:
    """Walk a section/subsection/paragraph/etc. and emit Markdown lines."""
    lines: list[str] = []
    ln = localname(elem.tag)

    if ln in ("section",):
        num = elem.find(f"{{{USLM_NS}}}num")
        heading = elem.find(f"{{{USLM_NS}}}heading")
        num_t = (num.text or "").strip() if num is not None else ""
        head_t = text_of(heading).strip() if heading is not None else ""
        title = " ".join(t for t in [num_t, head_t] if t)
        lines.append(f"### {title}")
        lines.append("")
        for child in elem:
            if localname(child.tag) in ("num", "heading", "sourceCredit", "notes", "note", "editorialNote"):
                continue
            sublines = render_block(child, depth=0)
            if sublines:
                lines.extend(sublines)
                lines.append("")
        return lines

    if ln in ("subsection", "paragraph", "subparagraph", "clause", "subclause", "item", "subitem"):
        num = elem.find(f"{{{USLM_NS}}}num")
        heading = elem.find(f"{{{USLM_NS}}}heading")
        chapeau = elem.find(f"{{{USLM_NS}}}chapeau")
        continuation = elem.find(f"{{{USLM_NS}}}continuation")
        num_t = (num.text or "").strip() if num is not None else ""
        head_t = text_of(heading).strip() if heading is not None else ""
        label_parts = [p for p in [num_t, head_t] if p]
        label = " ".join(label_parts)
        indent = "    " * depth
        lead = ""
        if chapeau is not None:
            lead = normalize(text_of(chapeau))
        if label and lead:
            lines.append(f"{indent}**{label}** {lead}")
        elif label:
            lines.append(f"{indent}**{label}**")
        elif lead:
            lines.append(f"{indent}{lead}")
        for child in elem:
            cln = localname(child.tag)
            if cln in ("num", "heading", "chapeau", "continuation", "sourceCredit", "notes", "note", "editorialNote"):
                continue
            sublines = render_block(child, depth=depth + 1)
            if sublines:
                lines.extend(sublines)
        if continuation is not None:
            lines.append(f"{indent}{normalize(text_of(continuation))}")
        return lines

    if ln in ("content", "p"):
        body = normalize(text_of(elem))
        if body:
            lines.append(("    " * depth) + body)
        return lines

    if ln == "quotedContent":
        body = normalize(text_of(elem))
        if body:
            for line in body.splitlines():
                lines.append(("    " * depth) + "> " + line)
        return lines

    for child in elem:
        lines.extend(render_block(child, depth=depth))
    return lines


def _container_label(elem: ET.Element) -> str:
    num = elem.find(f"{{{USLM_NS}}}num")
    heading = elem.find(f"{{{USLM_NS}}}heading")
    return " ".join(t for t in [
        (num.text or "").strip() if num is not None else "",
        text_of(heading).strip() if heading is not None else "",
    ] if t)


def render_chapter(chapter: ET.Element, citation: str, full_title: str, short_name: str, source_url: str) -> str:
    """Render an entire USC chapter. Chapters may contain chapter-level sections,
    subchapters (which may contain parts which contain sections), or both."""
    today = date.today().isoformat()
    out: list[str] = []
    ch_label = _container_label(chapter)
    out.append(f"# {full_title} ({short_name})")
    out.append("")
    out.append(f"- Citation: {citation}")
    out.append(f"- USC Chapter: {ch_label}")
    out.append(f"- Release point: Public Law {USC_RELEASE}")
    out.append(f"- Source: {source_url}")
    out.append(f"- Pulled: {today}")
    out.append("")
    out.append("> Verbatim text from the Office of the Law Revision Counsel USLM XML.")
    out.append("> Cross-references and parts/subparts hierarchy preserved.")
    out.append("")

    for child in chapter:
        ln = localname(child.tag)
        if ln == "subchapter":
            label = _container_label(child)
            out.append(f"## {label}")
            out.append("")
            for sub in child:
                sln = localname(sub.tag)
                if sln == "part":
                    plabel = _container_label(sub)
                    out.append(f"### {plabel}")
                    out.append("")
                    for sec in sub:
                        if localname(sec.tag) == "section":
                            out.extend(render_block(sec))
                elif sln == "section":
                    out.extend(render_block(sub))
        elif ln == "part":
            label = _container_label(child)
            out.append(f"## {label}")
            out.append("")
            for sub in child:
                if localname(sub.tag) == "section":
                    out.extend(render_block(sub))
        elif ln == "section":
            out.extend(render_block(child))
    text = "\n".join(out).rstrip() + "\n"
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def find_chapter(root: ET.Element, usc_title: str, chapter: str) -> ET.Element | None:
    target_identifier = f"/us/usc/t{usc_title}/{chapter}"
    for ch in root.iter(f"{{{USLM_NS}}}chapter"):
        if ch.attrib.get("identifier") == target_identifier:
            return ch
    return None


# ----- eCFR XML → Markdown -------------------------------------------------------------

def fetch_cfr_part_xml(cfr_title: str, part: str) -> bytes:
    url = f"{ECFR_BASE}/{ECFR_AS_OF}/title-{cfr_title}.xml?part={part}"
    return http_get(url)


def cfr_text_of(elem: ET.Element) -> str:
    """Get text of an element preserving inline E/I/B as Markdown emphasis."""
    parts: list[str] = []
    if elem.text:
        parts.append(elem.text)
    for child in elem:
        tag = localname(child.tag)
        inner = cfr_text_of(child)
        if tag == "E":
            t = (child.attrib.get("T") or "").strip()
            if t == "51":
                parts.append(f"***{inner}***")
            else:
                parts.append(f"*{inner}*")
        elif tag in ("I",):
            parts.append(f"*{inner}*")
        elif tag in ("B",):
            parts.append(f"**{inner}**")
        else:
            parts.append(inner)
        if child.tail:
            parts.append(child.tail)
    return "".join(parts)


def render_cfr_div(elem: ET.Element, depth: int = 0) -> list[str]:
    """Recursively render an eCFR DIV element."""
    lines: list[str] = []
    tag = localname(elem.tag)
    head = None
    for child in elem:
        if localname(child.tag) == "HEAD":
            head = child
            break

    if tag.startswith("DIV"):
        if head is not None:
            head_text = cfr_text_of(head).strip()
            level = {"DIV5": "#", "DIV6": "##", "DIV7": "###", "DIV8": "####", "DIV9": "#####"}.get(tag, "######")
            lines.append(f"{level} {head_text}")
            lines.append("")
        for child in elem:
            ctag = localname(child.tag)
            if ctag == "HEAD":
                continue
            if ctag in ("AUTH", "SOURCE", "EFFDNOT"):
                t = cfr_text_of(child).strip()
                if t:
                    lines.append(f"_{t}_")
                    lines.append("")
            elif ctag.startswith("DIV"):
                lines.extend(render_cfr_div(child, depth=depth + 1))
            elif ctag in ("P", "FP"):
                t = cfr_text_of(child).strip()
                if t:
                    lines.append(t)
                    lines.append("")
            elif ctag == "EXTRACT":
                inner_text = cfr_text_of(child).strip()
                if inner_text:
                    for line in inner_text.splitlines():
                        lines.append(f"> {line}")
                    lines.append("")
            elif ctag == "NOTE":
                t = cfr_text_of(child).strip()
                if t:
                    lines.append(f"> **Note:** {t}")
                    lines.append("")
            else:
                t = cfr_text_of(child).strip()
                if t:
                    lines.append(t)
                    lines.append("")
        return lines

    return lines


def render_cfr_part(part_xml: bytes, cfr_title: str, part: str, short_name: str, full_title: str) -> str:
    today = date.today().isoformat()
    root = ET.fromstring(part_xml)

    target = None
    for div in root.iter():
        if localname(div.tag) == "DIV5" and div.attrib.get("N") == part and div.attrib.get("TYPE") == "PART":
            target = div
            break
    if target is None:
        for div in root.iter():
            if localname(div.tag) == "DIV5" and div.attrib.get("N") == part:
                target = div
                break
    if target is None:
        raise RuntimeError(f"could not locate Part {part} in eCFR XML response for Title {cfr_title}")

    out: list[str] = []
    out.append(f"# {full_title}")
    out.append("")
    out.append(f"- Citation: {cfr_title} C.F.R. Part {part}")
    out.append(f"- As of: {ECFR_AS_OF}")
    out.append(f"- Source: https://www.ecfr.gov/current/title-{cfr_title}/part-{part}")
    out.append(f"- Pulled: {today}")
    out.append("")
    out.append("> Verbatim text from the eCFR XML versioner API. Inline italics (`*`) and")
    out.append("> bold (`**`) preserved; tables, figures, and footnotes flattened to plain text.")
    out.append("")
    out.extend(render_cfr_div(target))
    text = "\n".join(out).rstrip() + "\n"
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


# ----- main ----------------------------------------------------------------------------

def _usc_view_url(usc_title: str, chapter: str) -> str:
    ch_num = chapter.removeprefix("ch")
    return (
        "https://uscode.house.gov/view.xhtml?req=granuleid:"
        f"USC-prelim-title{usc_title}-chapter{ch_num}&edition=prelim"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out",
        default="plugins/claude-legal-federal-laws/references/ada-laws",
        help="Output corpus directory.",
    )
    ap.add_argument("--cache", default="/tmp/claude-legal-cache")
    ap.add_argument("--only", nargs="*", help="Optional list of short names to limit to (e.g., ADA DOJ-Title-II-28-CFR-35).")
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    cache = Path(args.cache)

    only = {s.lower() for s in args.only} if args.only else None

    # ----- USC -----
    usc_roots: dict[str, ET.Element] = {}

    def usc_root(title: str) -> ET.Element:
        if title not in usc_roots:
            xml_path = get_usc_xml(title, cache)
            print(f"Parsing {xml_path} …", flush=True)
            usc_roots[title] = ET.parse(xml_path).getroot()
        return usc_roots[title]

    for (usc_title, chapter, _sub, short, citation, full_title) in USC_TARGETS:
        if only and short.lower() not in only:
            continue
        root = usc_root(usc_title)
        src = _usc_view_url(usc_title, chapter)
        ch = find_chapter(root, usc_title, chapter)
        if ch is None:
            print(f"  ! could not find /us/usc/t{usc_title}/{chapter}", flush=True)
            continue
        md = render_chapter(ch, citation, full_title, short, src)
        path = out_dir / f"{short}.md"
        tmp = path.with_suffix(".md.tmp")
        tmp.write_text(md, encoding="utf-8")
        tmp.replace(path)
        print(f"  wrote {path} ({len(md):,} bytes)", flush=True)

    # ----- CFR -----
    for (cfr_title, part, short, full_title) in CFR_PARTS:
        if only and short.lower() not in only:
            continue
        print(f"Fetching {cfr_title} CFR {part} ({short}) …", flush=True)
        try:
            xml_bytes = fetch_cfr_part_xml(cfr_title, part)
        except Exception as e:
            print(f"  ! eCFR fetch failed: {e}", flush=True)
            continue
        md = render_cfr_part(xml_bytes, cfr_title, part, short, full_title)
        path = out_dir / f"{short}.md"
        tmp = path.with_suffix(".md.tmp")
        tmp.write_text(md, encoding="utf-8")
        tmp.replace(path)
        print(f"  wrote {path} ({len(md):,} bytes)", flush=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
