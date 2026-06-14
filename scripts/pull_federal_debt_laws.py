#!/usr/bin/env python3
"""Pull federal debt-related statutes (multiple USC titles) and CFR parts (multiple CFR titles).

Statutes from uscode.house.gov USLM XML, release point Public Law 119-84
(current as of 2026-04-21). All five USC titles below are available at the
same 119-84 release point. To refresh: visit
https://uscode.house.gov/download/releasepoints.shtml, find the latest
public-law release point, and bump USC_RELEASE — every USC title is
republished at every release point, so a single constant is sufficient.

USC sources (federal-debt-laws/):
  - TILA          = Title 15 ch 41 subchapter I    (15 U.S.C. §§ 1601–1667f)
  - Garnishment   = Title 15 ch 41 subchapter II   (15 U.S.C. §§ 1671–1677)
  - FCRA          = Title 15 ch 41 subchapter III  (15 U.S.C. §§ 1681–1681x)
  - ECOA          = Title 15 ch 41 subchapter IV   (15 U.S.C. §§ 1691–1691f)
  - FDCPA         = Title 15 ch 41 subchapter V    (15 U.S.C. §§ 1692–1692p)
  - EFTA          = Title 15 ch 41 subchapter VI   (15 U.S.C. §§ 1693–1693r)
  - RESPA         = Title 12 ch 27                 (12 U.S.C. §§ 2601–2617)
  - SCRA          = Title 50 ch 50                 (50 U.S.C. §§ 3901–4043)
  - FHA           = Title 42 ch 45 subchapter I    (42 U.S.C. §§ 3601–3619)

USC sources (federal-bankruptcy/):
  - Bankruptcy Code chapters 1, 3, 5, 7, 11, 12, 13, 15 — all of 11 U.S.C.

Regulations from ecfr.gov XML versioner API:
  - Reg F = 12 C.F.R. Part 1006  (CFPB rules implementing FDCPA)
  - Reg V = 12 C.F.R. Part 1022  (CFPB rules implementing FCRA)
  - Reg Z = 12 C.F.R. Part 1026  (CFPB rules implementing TILA)
  - Reg B = 12 C.F.R. Part 1002  (CFPB rules implementing ECOA)
  - Reg E = 12 C.F.R. Part 1005  (CFPB rules implementing EFTA)
  - Reg M = 12 C.F.R. Part 1013  (Consumer Leasing Act)
  - Reg N = 12 C.F.R. Part 1014  (Mortgage Acts and Practices)
  - Reg P = 12 C.F.R. Part 1016  (Gramm-Leach-Bliley financial privacy)
  - Reg X = 12 C.F.R. Part 1024  (RESPA implementing regs)
  - Reg DD = 12 C.F.R. Part 1030 (Truth in Savings Act)
  - TSR   = 16 C.F.R. Part 310   (FTC Telemarketing Sales Rule)

Output: plugins/claude-legal-federal-laws/references/{federal-debt-laws,federal-bankruptcy}/
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
#              full_title, corpus_dir).
# - subchapter_or_None: "schI", "schII", ... when the act is one subchapter
#   of a chapter; None means "render the whole chapter".
# - corpus_dir: which output corpus the file is written into.
USCRow = tuple[str, str, str | None, str, str, str, str]
USC_TARGETS: list[USCRow] = [
    # 15 U.S.C. Chapter 41 — Consumer Credit Protection Act
    ("15", "ch41", "schI",   "TILA",        "15 U.S.C. §§ 1601–1667f",
     "Truth in Lending Act",                                   "federal-debt-laws"),
    ("15", "ch41", "schII",  "Garnishment", "15 U.S.C. §§ 1671–1677",
     "Restrictions on Garnishment (CCPA Title III)",           "federal-debt-laws"),
    ("15", "ch41", "schIII", "FCRA",        "15 U.S.C. §§ 1681–1681x",
     "Fair Credit Reporting Act",                              "federal-debt-laws"),
    ("15", "ch41", "schIV",  "ECOA",        "15 U.S.C. §§ 1691–1691f",
     "Equal Credit Opportunity Act",                           "federal-debt-laws"),
    ("15", "ch41", "schV",   "FDCPA",       "15 U.S.C. §§ 1692–1692p",
     "Fair Debt Collection Practices Act",                     "federal-debt-laws"),
    ("15", "ch41", "schVI",  "EFTA",        "15 U.S.C. §§ 1693–1693r",
     "Electronic Fund Transfer Act",                           "federal-debt-laws"),
    # 12 U.S.C. Chapter 27 — RESPA statute
    ("12", "ch27", None,     "RESPA",       "12 U.S.C. §§ 2601–2617",
     "Real Estate Settlement Procedures Act",                  "federal-debt-laws"),
    # 50 U.S.C. Chapter 50 — SCRA
    ("50", "ch50", None,     "SCRA",        "50 U.S.C. §§ 3901–4043",
     "Servicemembers Civil Relief Act",                        "federal-debt-laws"),
    # 42 U.S.C. Chapter 45 Subchapter I — Fair Housing Act
    ("42", "ch45", "schI",   "FHA",         "42 U.S.C. §§ 3601–3619",
     "Fair Housing Act",                                       "federal-debt-laws"),
    # 11 U.S.C. — Bankruptcy Code; one file per chapter into its own corpus.
    ("11", "ch1",  None,     "Chapter-1",   "11 U.S.C. §§ 101–112",
     "Bankruptcy Code — Chapter 1 (General Provisions)",       "federal-bankruptcy"),
    ("11", "ch3",  None,     "Chapter-3",   "11 U.S.C. §§ 301–366",
     "Bankruptcy Code — Chapter 3 (Case Administration)",      "federal-bankruptcy"),
    ("11", "ch5",  None,     "Chapter-5",   "11 U.S.C. §§ 501–562",
     "Bankruptcy Code — Chapter 5 (Creditors, the Debtor, and the Estate)",
                                                                "federal-bankruptcy"),
    ("11", "ch7",  None,     "Chapter-7",   "11 U.S.C. §§ 701–784",
     "Bankruptcy Code — Chapter 7 (Liquidation)",              "federal-bankruptcy"),
    ("11", "ch11", None,     "Chapter-11",  "11 U.S.C. §§ 1101–1195",
     "Bankruptcy Code — Chapter 11 (Reorganization)",          "federal-bankruptcy"),
    ("11", "ch12", None,     "Chapter-12",  "11 U.S.C. §§ 1201–1232",
     "Bankruptcy Code — Chapter 12 (Family Farmer/Fisherman)", "federal-bankruptcy"),
    ("11", "ch13", None,     "Chapter-13",  "11 U.S.C. §§ 1301–1330",
     "Bankruptcy Code — Chapter 13 (Adjustment of Debts of an Individual with Regular Income)",
                                                                "federal-bankruptcy"),
    ("11", "ch15", None,     "Chapter-15",  "11 U.S.C. §§ 1501–1532",
     "Bankruptcy Code — Chapter 15 (Ancillary and Other Cross-Border Cases)",
                                                                "federal-bankruptcy"),
]

# Regulation row: (cfr_title, part, short, full_title, corpus_dir).
CFRRow = tuple[str, str, str, str, str]
CFR_PARTS: list[CFRRow] = [
    ("12", "1002", "Reg-B",  "Regulation B — Equal Credit Opportunity",                           "federal-debt-laws"),
    ("12", "1005", "Reg-E",  "Regulation E — Electronic Fund Transfers (EFTA)",                   "federal-debt-laws"),
    ("12", "1006", "Reg-F",  "Regulation F — Debt Collection Practices (FDCPA)",                  "federal-debt-laws"),
    ("12", "1013", "Reg-M",  "Regulation M — Consumer Leasing",                                   "federal-debt-laws"),
    ("12", "1014", "Reg-N",  "Regulation N — Mortgage Acts and Practices (MAP Rule)",             "federal-debt-laws"),
    ("12", "1016", "Reg-P",  "Regulation P — Privacy of Consumer Financial Information",          "federal-debt-laws"),
    ("12", "1022", "Reg-V",  "Regulation V — Fair Credit Reporting",                              "federal-debt-laws"),
    ("12", "1024", "Reg-X",  "Regulation X — Real Estate Settlement Procedures (RESPA)",          "federal-debt-laws"),
    ("12", "1026", "Reg-Z",  "Regulation Z — Truth in Lending",                                   "federal-debt-laws"),
    ("12", "1030", "Reg-DD", "Regulation DD — Truth in Savings",                                  "federal-debt-laws"),
    ("16", "310",  "TSR",    "Telemarketing Sales Rule (FTC)",                                    "federal-debt-laws"),
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


def _container_label(elem: ET.Element) -> str:
    num = elem.find(f"{{{USLM_NS}}}num")
    heading = elem.find(f"{{{USLM_NS}}}heading")
    return " ".join(t for t in [
        (num.text or "").strip() if num is not None else "",
        text_of(heading).strip() if heading is not None else "",
    ] if t)


def render_subchapter(subch: ET.Element, citation: str, full_title: str, short_name: str, source_url: str) -> str:
    today = date.today().isoformat()
    out: list[str] = []
    sc_label = _container_label(subch)
    out.append(f"# {full_title} ({short_name})")
    out.append("")
    out.append(f"- Citation: {citation}")
    out.append(f"- USC Subchapter: {sc_label}")
    out.append(f"- Release point: Public Law {USC_RELEASE}")
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
            label = _container_label(child)
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


def render_chapter(chapter: ET.Element, citation: str, full_title: str, short_name: str, source_url: str) -> str:
    """Render an entire USC chapter (used when the act is a whole chapter, e.g. RESPA, SCRA,
    and Bankruptcy chapters). Chapters may contain subchapters which contain sections, or may
    contain sections directly."""
    today = date.today().isoformat()
    out: list[str] = []
    ch_label = _container_label(chapter)
    # Suppress the "(short_name)" suffix when the short is just a file-name token
    # like "Chapter-7" that adds no information beyond the full title.
    if short_name.startswith("Chapter-"):
        out.append(f"# {full_title}")
    else:
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


def find_subchapter(root: ET.Element, usc_title: str, chapter: str, sub_id: str) -> ET.Element | None:
    target_identifier = f"/us/usc/t{usc_title}/{chapter}/{sub_id}"
    for sub in root.iter(f"{{{USLM_NS}}}subchapter"):
        if sub.attrib.get("identifier") == target_identifier:
            return sub
    return None


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


def render_cfr_part(part_xml: bytes, cfr_title: str, part: str, short_name: str, full_title: str) -> str:
    today = date.today().isoformat()
    root = ET.fromstring(part_xml)

    # The full title XML contains many parts; locate the one whose N attribute matches.
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
    out.append("> bold (`**`) preserved; tables and footnotes flattened to plain text.")
    out.append("")
    out.extend(render_cfr_div(target))
    text = "\n".join(out).rstrip() + "\n"
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


# ----- main ----------------------------------------------------------------------------

def _usc_view_url(usc_title: str, chapter: str, sub_id: str | None) -> str:
    """Build the human-readable uscode.house.gov URL for a chapter or subchapter."""
    ch_num = chapter.removeprefix("ch")
    if sub_id is None:
        return (
            "https://uscode.house.gov/view.xhtml?req=granuleid:"
            f"USC-prelim-title{usc_title}-chapter{ch_num}&edition=prelim"
        )
    sub_letters = sub_id.removeprefix("sch").lower()
    return (
        "https://uscode.house.gov/view.xhtml?req=granuleid:"
        f"USC-prelim-title{usc_title}-chapter{ch_num}-subchapter{sub_letters}&edition=prelim"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out-root",
        default="plugins/claude-legal-federal-laws/references",
        help="Root references/ dir; per-target corpus subdirs are written inside it.",
    )
    ap.add_argument("--cache", default="/tmp/claude-legal-cache")
    ap.add_argument("--only", nargs="*", help="Optional list of short names to limit to (e.g., FDCPA Reg-F TSR).")
    args = ap.parse_args()

    out_root = Path(args.out_root)
    out_root.mkdir(parents=True, exist_ok=True)
    cache = Path(args.cache)

    only = {s.lower() for s in args.only} if args.only else None

    # ----- USC -----
    # Parse each USC title we need only once (lazy load).
    usc_roots: dict[str, ET.Element] = {}

    def usc_root(title: str) -> ET.Element:
        if title not in usc_roots:
            xml_path = get_usc_xml(title, cache)
            print(f"Parsing {xml_path} …", flush=True)
            usc_roots[title] = ET.parse(xml_path).getroot()
        return usc_roots[title]

    for (usc_title, chapter, sub_id, short, citation, full_title, corpus) in USC_TARGETS:
        if only and short.lower() not in only:
            continue
        root = usc_root(usc_title)
        src = _usc_view_url(usc_title, chapter, sub_id)
        if sub_id is None:
            ch = find_chapter(root, usc_title, chapter)
            if ch is None:
                print(f"  ! could not find /us/usc/t{usc_title}/{chapter}", flush=True)
                continue
            md = render_chapter(ch, citation, full_title, short, src)
        else:
            sub = find_subchapter(root, usc_title, chapter, sub_id)
            if sub is None:
                print(f"  ! could not find /us/usc/t{usc_title}/{chapter}/{sub_id}", flush=True)
                continue
            md = render_subchapter(sub, citation, full_title, short, src)
        out_dir = out_root / corpus
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / f"{short}.md"
        tmp = path.with_suffix(".md.tmp")
        tmp.write_text(md, encoding="utf-8")
        tmp.replace(path)
        print(f"  wrote {path} ({len(md):,} bytes)", flush=True)

    # ----- CFR -----
    for (cfr_title, part, short, full_title, corpus) in CFR_PARTS:
        if only and short.lower() not in only:
            continue
        print(f"Fetching {cfr_title} CFR {part} ({short}) …", flush=True)
        try:
            xml_bytes = fetch_cfr_part_xml(cfr_title, part)
        except Exception as e:
            print(f"  ! eCFR fetch failed: {e}", flush=True)
            continue
        md = render_cfr_part(xml_bytes, cfr_title, part, short, full_title)
        out_dir = out_root / corpus
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / f"{short}.md"
        tmp = path.with_suffix(".md.tmp")
        tmp.write_text(md, encoding="utf-8")
        tmp.replace(path)
        print(f"  wrote {path} ({len(md):,} bytes)", flush=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
