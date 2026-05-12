#!/usr/bin/env python3
"""Pull federal debt-related statutes (USC Title 15) and CFR parts (Title 12) and convert to Markdown.

Statutes from uscode.house.gov USLM XML release point 119-84 (current as of 2026-04-18):
  - FDCPA   = Title 15 ch 41 subchapter V   (15 U.S.C. §§ 1692–1692p)
  - FCRA    = Title 15 ch 41 subchapter III (15 U.S.C. §§ 1681–1681x)
  - TILA    = Title 15 ch 41 subchapter I   (15 U.S.C. §§ 1601–1667f)
  - ECOA    = Title 15 ch 41 subchapter IV  (15 U.S.C. §§ 1691–1691f)

Regulations from ecfr.gov XML versioner API (Title 12):
  - Reg F = Part 1006 (CFPB rules implementing FDCPA)
  - Reg V = Part 1022 (CFPB rules implementing FCRA)
  - Reg Z = Part 1026 (CFPB rules implementing TILA)
  - Reg B = Part 1002 (CFPB rules implementing ECOA)

Output: plugins/wa-court-docs/skills/wa-law-references/references/federal-debt-laws/
"""

from __future__ import annotations

import argparse
import io
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from datetime import date
from pathlib import Path

USER_AGENT = "claude-legal/1.0 (+https://github.com/codearranger/claude-legal) federal-debt-laws-puller"

# USC Title 15 USLM release point. Pinned so output is reproducible; refreshable later.
USC15_RELEASE = "119-84"
USC15_ZIP_URL = f"https://uscode.house.gov/download/releasepoints/us/pl/119/84/xml_usc15@{USC15_RELEASE}.zip"

# eCFR uses an "as-of" date; we pick the most recent fixed date for stable output.
ECFR_AS_OF = "2026-01-01"
ECFR_BASE = "https://www.ecfr.gov/api/versioner/v1/full"

# (subchapter-id, short-name, citation, full-title)
USC_SUBCHAPTERS: list[tuple[str, str, str, str]] = [
    ("schV", "FDCPA", "15 U.S.C. §§ 1692–1692p",
     "Fair Debt Collection Practices Act"),
    ("schIII", "FCRA", "15 U.S.C. §§ 1681–1681x",
     "Fair Credit Reporting Act"),
    ("schI", "TILA", "15 U.S.C. §§ 1601–1667f",
     "Truth in Lending Act"),
    ("schIV", "ECOA", "15 U.S.C. §§ 1691–1691f",
     "Equal Credit Opportunity Act"),
]

# (cfr-part, short-name, full-title)
CFR_PARTS: list[tuple[str, str, str]] = [
    ("1006", "Reg-F", "Regulation F — Debt Collection Practices (FDCPA)"),
    ("1022", "Reg-V", "Regulation V — Fair Credit Reporting"),
    ("1026", "Reg-Z", "Regulation Z — Truth in Lending"),
    ("1002", "Reg-B", "Regulation B — Equal Credit Opportunity"),
]

USLM_NS = "http://xml.house.gov/schemas/uslm/1.0"


def http_get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def get_usc15_xml(cache: Path) -> Path:
    """Download and unzip the USC Title 15 USLM XML if not already cached."""
    cache.mkdir(parents=True, exist_ok=True)
    xml_path = cache / f"usc15@{USC15_RELEASE}.xml"
    if xml_path.exists() and xml_path.stat().st_size > 1_000_000:
        return xml_path
    print(f"  downloading {USC15_ZIP_URL}", flush=True)
    zip_bytes = http_get(USC15_ZIP_URL)
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        # The archive contains usc15.xml at the root.
        names = [n for n in zf.namelist() if n.endswith(".xml")]
        if not names:
            raise RuntimeError(f"no XML inside {USC15_ZIP_URL}")
        with zf.open(names[0]) as src, open(xml_path, "wb") as dst:
            dst.write(src.read())
    return xml_path


# ----- USLM → Markdown -----------------------------------------------------------------

def localname(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def text_of(elem: ET.Element) -> str:
    """Concatenate all text in an element with single spaces; preserve inline structure where useful."""
    parts: list[str] = []
    if elem.text:
        parts.append(elem.text)
    for child in elem:
        ln = localname(child.tag)
        if ln == "ref":
            # Replace cross-references with their visible text.
            parts.append(text_of(child))
        elif ln == "note":
            # Skip notes inside body text — captured separately.
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
        # body
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
        # Build label "(a) Heading"
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
        # nested children
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

    # Fallback: recurse into children.
    for child in elem:
        lines.extend(render_block(child, depth=depth))
    return lines


def render_subchapter(subch: ET.Element, citation: str, full_title: str, short_name: str, source_url: str) -> str:
    today = date.today().isoformat()
    out: list[str] = []
    num = subch.find(f"{{{USLM_NS}}}num")
    heading = subch.find(f"{{{USLM_NS}}}heading")
    sc_label = " ".join(t for t in [(num.text or "").strip() if num is not None else "",
                                    text_of(heading).strip() if heading is not None else ""] if t)
    out.append(f"# {full_title} ({short_name})")
    out.append("")
    out.append(f"- Citation: {citation}")
    out.append(f"- USC Subchapter: {sc_label}")
    out.append(f"- Release point: Public Law {USC15_RELEASE}")
    out.append(f"- Source: {source_url}")
    out.append(f"- Pulled: {today}")
    out.append("")
    out.append("> Verbatim text from the Office of the Law Revision Counsel USLM XML.")
    out.append("> Cross-references and parts/subparts hierarchy preserved.")
    out.append("")

    # Optional chapeau / source credit at subchapter level — usually empty; skip for cleanliness.

    # Iterate through parts (if any) then sections.
    for child in subch:
        ln = localname(child.tag)
        if ln == "part":
            pnum = child.find(f"{{{USLM_NS}}}num")
            phead = child.find(f"{{{USLM_NS}}}heading")
            label = " ".join(t for t in [(pnum.text or "").strip() if pnum is not None else "",
                                         text_of(phead).strip() if phead is not None else ""] if t)
            out.append(f"## {label}")
            out.append("")
            for sub in child:
                if localname(sub.tag) == "section":
                    out.extend(render_block(sub))
        elif ln == "section":
            out.extend(render_block(child))
    text = "\n".join(out).rstrip() + "\n"
    # Clean stray multi-blank-lines.
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def find_subchapter(root: ET.Element, sub_id: str) -> ET.Element | None:
    target_identifier = f"/us/usc/t15/ch41/{sub_id}"
    for sub in root.iter(f"{{{USLM_NS}}}subchapter"):
        if sub.attrib.get("identifier") == target_identifier:
            return sub
    return None


# ----- eCFR XML → Markdown -------------------------------------------------------------

def fetch_cfr_part_xml(part: str) -> bytes:
    url = f"{ECFR_BASE}/{ECFR_AS_OF}/title-12.xml?part={part}"
    return http_get(url)


# eCFR XML structure (CFR-XML 2.0): DIV5 (PART) > DIV6 (SUBPART) > DIV8 (SECTION) > P, etc.
# We render headings from HEAD elements and body paragraphs from P elements.

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
            # T="03" or "04" = italic; T="51" = bold-italic. Default to italic.
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
    div_type = elem.attrib.get("TYPE", "")
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
                # Authority/source/effective notes — emit as italic block-quote.
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
                # quoted block
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
                # Recurse into anything else (tables, footnotes, etc.) and capture text.
                t = cfr_text_of(child).strip()
                if t:
                    lines.append(t)
                    lines.append("")
        return lines

    return lines


def render_cfr_part(part_xml: bytes, part: str, short_name: str, full_title: str) -> str:
    today = date.today().isoformat()
    root = ET.fromstring(part_xml)

    # The full title-12 XML contains many parts; locate the one whose N attribute matches.
    target = None
    for div in root.iter():
        if localname(div.tag) == "DIV5" and div.attrib.get("N") == part and div.attrib.get("TYPE") == "PART":
            target = div
            break
    if target is None:
        # Some responses wrap directly; fall back to scanning for the part number anywhere.
        for div in root.iter():
            if localname(div.tag) == "DIV5" and div.attrib.get("N") == part:
                target = div
                break
    if target is None:
        raise RuntimeError(f"could not locate Part {part} in eCFR XML response")

    out: list[str] = []
    out.append(f"# {full_title}")
    out.append("")
    out.append(f"- Citation: 12 C.F.R. Part {part}")
    out.append(f"- As of: {ECFR_AS_OF}")
    out.append(f"- Source: https://www.ecfr.gov/current/title-12/part-{part}")
    out.append(f"- Pulled: {today}")
    out.append("")
    out.append("> Verbatim text from the eCFR XML versioner API. Inline italics (`*`) and")
    out.append("> bold (`**`) preserved; tables and footnotes flattened to plain text.")
    out.append("")
    out.extend(render_cfr_div(target))
    text = "\n".join(out).rstrip() + "\n"
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


# ----- main ----------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="plugins/wa-court-docs/skills/wa-law-references/references/federal-debt-laws")
    ap.add_argument("--cache", default="/tmp/claude-legal-cache")
    ap.add_argument("--only", nargs="*", help="Optional list of short names to limit to (e.g., FDCPA Reg-F).")
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    cache = Path(args.cache)

    only = {s.lower() for s in args.only} if args.only else None

    # ----- USC -----
    usc_xml_path = get_usc15_xml(cache)
    print(f"Parsing {usc_xml_path} …", flush=True)
    tree = ET.parse(usc_xml_path)
    root = tree.getroot()

    for sub_id, short, citation, full_title in USC_SUBCHAPTERS:
        if only and short.lower() not in only:
            continue
        sub = find_subchapter(root, sub_id)
        if sub is None:
            print(f"  ! could not find {sub_id}", flush=True)
            continue
        # Source URL — uscode.house.gov web view of the subchapter.
        src = f"https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-chapter41-subchapter{sub_id.replace('sch', '').lower()}&edition=prelim"
        md = render_subchapter(sub, citation, full_title, short, src)
        path = out_dir / f"{short}.md"
        path.write_text(md, encoding="utf-8")
        size = len(md)
        print(f"  wrote {path} ({size:,} bytes)", flush=True)

    # ----- CFR -----
    for part, short, full_title in CFR_PARTS:
        if only and short.lower() not in only:
            continue
        print(f"Fetching 12 CFR {part} ({short}) …", flush=True)
        try:
            xml_bytes = fetch_cfr_part_xml(part)
        except Exception as e:
            print(f"  ! eCFR fetch failed: {e}", flush=True)
            continue
        md = render_cfr_part(xml_bytes, part, short, full_title)
        path = out_dir / f"{short}.md"
        path.write_text(md, encoding="utf-8")
        print(f"  wrote {path} ({len(md):,} bytes)", flush=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
