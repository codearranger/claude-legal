#!/usr/bin/env python3
"""Pull the Immigration and Nationality Act (INA) — 8 U.S.C. Chapter 12.

The INA is codified at Title 8 of the U.S. Code, Chapter 12 ("Immigration and
Nationality"), 8 U.S.C. §§ 1101 et seq. Practitioners cite it by INA section
number (e.g., "INA § 212(a)(6)(C)(i)") while the codified text is numbered by
U.S.C. section (8 U.S.C. § 1182). This puller writes the verbatim U.S.C. text
(one Markdown file per subchapter) from the Office of the Law Revision Counsel
USLM XML and records the INA-section <-> 8 U.S.C.-section correspondence in the
corpus README (authored separately).

Subchapters of 8 U.S.C. Chapter 12:
  - schI   = General Provisions               8 U.S.C. §§ 1101-1107   (INA §§ 101-106)
  - schII  = Immigration                      8 U.S.C. §§ 1151-1381   (INA §§ 201-294)
  - schIII = Nationality and Naturalization   8 U.S.C. §§ 1401-1504   (INA §§ 301-360)
  - schIV  = Refugee Assistance               8 U.S.C. §§ 1521-1525   (INA §§ 411-414)
  - schV   = Alien Terrorist Removal Procedures 8 U.S.C. §§ 1531-1537 (INA §§ 501-507)

To refresh: visit https://uscode.house.gov/download/releasepoints.shtml, find
the latest public-law release point, and bump USC_RELEASE below.

Output: plugins/claude-legal-immigration-laws/references/immigration-statutes/
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from datetime import date
from pathlib import Path

USER_AGENT = "claude-legal/1.0 (+https://github.com/codearranger/claude-legal) ina-puller"

# USC USLM release point. Every USC title is republished at every release point.
# To refresh, browse https://uscode.house.gov/download/releasepoints.shtml and
# bump this constant.
USC_RELEASE = "119-93"
USC_RELEASE_CONGRESS, USC_RELEASE_PUBLAW = USC_RELEASE.split("-", 1)
# The OLRC zero-pads the title number to two digits in the filename
# (xml_usc08@..., not xml_usc8@...). {title} is formatted padded below.
USC_ZIP_URL_TMPL = (
    "https://uscode.house.gov/download/releasepoints/us/pl/"
    f"{USC_RELEASE_CONGRESS}/{USC_RELEASE_PUBLAW}/"
    "xml_usc{title}@" + USC_RELEASE + ".zip"
)

USLM_NS = "http://xml.house.gov/schemas/uslm/1.0"

# Target row: (subchapter_id, out_file, short_name, citation, full_title, ina_range).
SubRow = tuple[str, str, str, str, str, str]
SUBCHAPTERS: list[SubRow] = [
    ("schI",   "INA-I-general-provisions",          "INA Subchapter I",
     "8 U.S.C. §§ 1101-1107",  "Immigration and Nationality Act — Subchapter I (General Provisions)",
     "INA §§ 101-106"),
    ("schII",  "INA-II-immigration",                "INA Subchapter II",
     "8 U.S.C. §§ 1151-1381",  "Immigration and Nationality Act — Subchapter II (Immigration)",
     "INA §§ 201-294"),
    ("schIII", "INA-III-nationality",               "INA Subchapter III",
     "8 U.S.C. §§ 1401-1504",  "Immigration and Nationality Act — Subchapter III (Nationality and Naturalization)",
     "INA §§ 301-360"),
    ("schIV",  "INA-IV-refugee-assistance",         "INA Subchapter IV",
     "8 U.S.C. §§ 1521-1525",  "Immigration and Nationality Act — Subchapter IV (Refugee Assistance)",
     "INA §§ 411-414"),
    ("schV",   "INA-V-alien-terrorist-removal",     "INA Subchapter V",
     "8 U.S.C. §§ 1531-1537",  "Immigration and Nationality Act — Subchapter V (Alien Terrorist Removal Procedures)",
     "INA §§ 501-507"),
]

USC_TITLE = "8"
USC_CHAPTER = "ch12"


def http_get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


def get_usc_xml(title: str, cache: Path) -> Path:
    cache.mkdir(parents=True, exist_ok=True)
    xml_path = cache / f"usc{title}@{USC_RELEASE}.xml"
    if xml_path.exists() and xml_path.stat().st_size > 100_000:
        return xml_path
    url = USC_ZIP_URL_TMPL.format(title=f"{int(title):02d}")
    print(f"  downloading {url}", flush=True)
    zip_bytes = http_get(url)
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        names = [n for n in zf.namelist() if n.endswith(".xml")]
        if not names:
            raise RuntimeError(f"no XML inside {url}")
        with zf.open(names[0]) as src, open(xml_path, "wb") as dst:
            dst.write(src.read())
    return xml_path


# ----- USLM -> Markdown ----------------------------------------------------------------

def localname(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def text_of(elem: ET.Element) -> str:
    parts: list[str] = []
    if elem.text:
        parts.append(elem.text)
    for child in elem:
        ln = localname(child.tag)
        if ln == "note":
            continue
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
    lines: list[str] = []
    ln = localname(elem.tag)

    if ln == "section":
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
        label = " ".join(p for p in [num_t, head_t] if p)
        indent = "    " * depth
        lead = normalize(text_of(chapeau)) if chapeau is not None else ""
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


def render_subchapter(subch: ET.Element, citation: str, full_title: str,
                      ina_range: str, source_url: str) -> str:
    today = date.today().isoformat()
    out: list[str] = []
    sc_label = _container_label(subch)
    out.append(f"# {full_title}")
    out.append("")
    out.append(f"- Citation: {citation}")
    out.append(f"- INA sections: {ina_range}")
    out.append(f"- USC Subchapter: {sc_label}")
    out.append(f"- Release point: Public Law {USC_RELEASE}")
    out.append(f"- Source: {source_url}")
    out.append(f"- Pulled: {today}")
    out.append("")
    out.append("> Verbatim text from the Office of the Law Revision Counsel USLM XML.")
    out.append("> Codified U.S.C. section numbers shown; see the corpus README for the")
    out.append("> INA-section <-> 8 U.S.C.-section crosswalk practitioners cite by.")
    out.append("")

    for child in subch:
        ln = localname(child.tag)
        if ln == "part":
            out.append(f"## {_container_label(child)}")
            out.append("")
            for sub in child:
                sln = localname(sub.tag)
                if sln == "subpart":
                    out.append(f"### {_container_label(sub)}")
                    out.append("")
                    for sec in sub:
                        if localname(sec.tag) == "section":
                            out.extend(render_block(sec))
                elif sln == "section":
                    out.extend(render_block(sub))
        elif ln == "section":
            out.extend(render_block(child))
    text = "\n".join(out).rstrip() + "\n"
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def find_subchapter(root: ET.Element, sub_id: str) -> ET.Element | None:
    target = f"/us/usc/t{USC_TITLE}/{USC_CHAPTER}/{sub_id}"
    for sub in root.iter(f"{{{USLM_NS}}}subchapter"):
        if sub.attrib.get("identifier") == target:
            return sub
    return None


def _usc_view_url(sub_id: str) -> str:
    sub_letters = sub_id.removeprefix("sch").lower()
    return (
        "https://uscode.house.gov/view.xhtml?req=granuleid:"
        f"USC-prelim-title{USC_TITLE}-chapter12-subchapter{sub_letters}&edition=prelim"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out",
        default="plugins/claude-legal-immigration-laws/references/immigration-statutes",
    )
    ap.add_argument("--cache", default="/tmp/claude-legal-cache")
    ap.add_argument("--only", nargs="*", help="Limit to subchapter ids (e.g., schII schIII).")
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    only = {s.lower() for s in args.only} if args.only else None

    xml_path = get_usc_xml(USC_TITLE, Path(args.cache))
    print(f"Parsing {xml_path} ...", flush=True)
    root = ET.parse(xml_path).getroot()

    wrote = 0
    for (sub_id, out_file, short, citation, full_title, ina_range) in SUBCHAPTERS:
        if only and sub_id.lower() not in only:
            continue
        sub = find_subchapter(root, sub_id)
        if sub is None:
            print(f"  ! could not find /us/usc/t{USC_TITLE}/{USC_CHAPTER}/{sub_id}", flush=True)
            continue
        md = render_subchapter(sub, citation, full_title, ina_range, _usc_view_url(sub_id))
        path = out_dir / f"{out_file}.md"
        tmp = path.with_suffix(".md.tmp")
        tmp.write_text(md, encoding="utf-8")
        tmp.replace(path)
        wrote += 1
        print(f"  wrote {path} ({len(md):,} bytes)", flush=True)

    manifest = {
        "version": "0.1.0",
        "last_pulled": date.today().isoformat(),
        "source": "https://uscode.house.gov USLM XML",
        "release_point": f"Public Law {USC_RELEASE}",
        "mode": "verbatim",
        "notes": "Pulled by scripts/pull_ina.py. Title 8 U.S.C. Chapter 12, one file per subchapter.",
    }
    manifest_path = out_dir / "_manifest.json"
    tmp = manifest_path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    tmp.replace(manifest_path)
    print(f"Done. Wrote {wrote} subchapter file(s) + _manifest.json", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
