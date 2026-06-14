#!/usr/bin/env python3
"""Pull immigration regulations from the eCFR XML versioner API.

Two regulatory titles carry the bulk of immigration practice:

  - Title 8  (Aliens and Nationality) — DHS/USCIS/CBP/ICE chapter I parts
    (8 CFR 1-499) and the EOIR/DOJ chapter V parts (8 CFR 1001-1337).
  - Title 22 (Foreign Relations) — the State Department visa, passport, and
    exchange-visitor parts that pair with the Foreign Affairs Manual.

This puller curates the most-cited parts (rather than every part in each title)
to keep the corpus bounded and reviewable, mirroring scripts/pull_federal_debt_laws.py.
Add a row to CFR_PARTS to extend coverage.

To refresh: bump ECFR_AS_OF (the eCFR returns the version in force on that date).

Output: plugins/claude-legal-immigration-laws/references/immigration-regulations/
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

USER_AGENT = "claude-legal/1.0 (+https://github.com/codearranger/claude-legal) immigration-cfr-puller"

ECFR_AS_OF = "2026-01-01"
ECFR_BASE = "https://www.ecfr.gov/api/versioner/v1/full"

# Row: (cfr_title, part, out_file, full_title).
CFRRow = tuple[str, str, str, str]
CFR_PARTS: list[CFRRow] = [
    # ----- 8 CFR Chapter I — DHS (USCIS / CBP / ICE) -----
    ("8", "1",    "8CFR-001-definitions",        "8 CFR Part 1 — Definitions"),
    ("8", "103",  "8CFR-103-powers-fees",        "8 CFR Part 103 — Immigration Benefits; Biometrics; Availability of Records; Fees"),
    ("8", "204",  "8CFR-204-immigrant-petitions","8 CFR Part 204 — Immigrant Petitions"),
    ("8", "207",  "8CFR-207-refugees",           "8 CFR Part 207 — Admission of Refugees"),
    ("8", "208",  "8CFR-208-asylum-dhs",         "8 CFR Part 208 — Asylum and Withholding of Removal (DHS)"),
    ("8", "209",  "8CFR-209-adjustment-refugee", "8 CFR Part 209 — Adjustment of Status of Refugees and Asylees"),
    ("8", "211",  "8CFR-211-lpr-documents",      "8 CFR Part 211 — Documentary Requirements: Immigrants; Waivers"),
    ("8", "212",  "8CFR-212-inadmissibility",    "8 CFR Part 212 — Documentary Requirements; Nonimmigrants; Waivers; Admission of Certain Inadmissible Aliens; Parole"),
    ("8", "214",  "8CFR-214-nonimmigrants",      "8 CFR Part 214 — Nonimmigrant Classes"),
    ("8", "216",  "8CFR-216-conditional-residence","8 CFR Part 216 — Conditional Basis of Lawful Permanent Residence"),
    ("8", "217",  "8CFR-217-visa-waiver",        "8 CFR Part 217 — Visa Waiver Program"),
    ("8", "235",  "8CFR-235-inspection",         "8 CFR Part 235 — Inspection of Persons Applying for Admission"),
    ("8", "236",  "8CFR-236-detention-removal",  "8 CFR Part 236 — Apprehension and Detention of Inadmissible and Deportable Aliens"),
    ("8", "240",  "8CFR-240-removal-proceedings","8 CFR Part 240 — Proceedings to Determine Removability (DHS)"),
    ("8", "241",  "8CFR-241-removal-execution",  "8 CFR Part 241 — Apprehension and Detention of Aliens Ordered Removed"),
    ("8", "244",  "8CFR-244-tps",                "8 CFR Part 244 — Temporary Protected Status"),
    ("8", "245",  "8CFR-245-adjustment",         "8 CFR Part 245 — Adjustment of Status to Lawful Permanent Resident"),
    ("8", "245a", "8CFR-245a-legalization",      "8 CFR Part 245a — Adjustment of Status Under Section 245A of the INA"),
    ("8", "248",  "8CFR-248-change-of-status",   "8 CFR Part 248 — Change of Nonimmigrant Classification"),
    ("8", "264",  "8CFR-264-registration",       "8 CFR Part 264 — Registration and Fingerprinting of Aliens"),
    ("8", "274a", "8CFR-274a-employment",        "8 CFR Part 274a — Control of Employment of Aliens"),
    ("8", "287",  "8CFR-287-enforcement",        "8 CFR Part 287 — Field Officers; Powers and Duties"),
    ("8", "292",  "8CFR-292-representation",      "8 CFR Part 292 — Representation and Appearances"),
    # ----- 8 CFR Chapter V — EOIR (DOJ): immigration courts + BIA -----
    ("8", "1001", "8CFR-1001-eoir-definitions",  "8 CFR Part 1001 — Definitions (EOIR)"),
    ("8", "1003", "8CFR-1003-eoir-bia",          "8 CFR Part 1003 — Executive Office for Immigration Review (immigration courts and the Board of Immigration Appeals)"),
    ("8", "1208", "8CFR-1208-asylum-eoir",       "8 CFR Part 1208 — Asylum and Withholding of Removal (EOIR)"),
    ("8", "1240", "8CFR-1240-removal-eoir",      "8 CFR Part 1240 — Proceedings to Determine Removability (EOIR)"),
    ("8", "1003a", None, None),  # placeholder guard removed below
    # ----- 22 CFR — State Department visas / passports / exchange -----
    ("22", "40",  "22CFR-040-visas-general",     "22 CFR Part 40 — Regulations Applicable to Both Nonimmigrants and Immigrants Under the INA"),
    ("22", "41",  "22CFR-041-nonimmigrant-visas","22 CFR Part 41 — Visas: Documentation of Nonimmigrants Under the INA"),
    ("22", "42",  "22CFR-042-immigrant-visas",   "22 CFR Part 42 — Visas: Documentation of Immigrants Under the INA"),
    ("22", "51",  "22CFR-051-passports",         "22 CFR Part 51 — Passports"),
    ("22", "53",  "22CFR-053-entry-departure",   "22 CFR Part 53 — Passport Requirement and Exceptions"),
    ("22", "62",  "22CFR-062-exchange-visitor",  "22 CFR Part 62 — Exchange Visitor Program"),
]
# Drop the placeholder guard row.
CFR_PARTS = [r for r in CFR_PARTS if r[2] is not None]


def localname(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def http_get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


def fetch_cfr_part_xml(cfr_title: str, part: str) -> bytes:
    url = f"{ECFR_BASE}/{ECFR_AS_OF}/title-{cfr_title}.xml?part={part}"
    return http_get(url)


def cfr_text_of(elem: ET.Element) -> str:
    parts: list[str] = []
    if elem.text:
        parts.append(elem.text)
    for child in elem:
        tag = localname(child.tag)
        inner = cfr_text_of(child)
        if tag == "E":
            t = (child.attrib.get("T") or "").strip()
            parts.append(f"***{inner}***" if t == "51" else f"*{inner}*")
        elif tag == "I":
            parts.append(f"*{inner}*")
        elif tag == "B":
            parts.append(f"**{inner}**")
        else:
            parts.append(inner)
        if child.tail:
            parts.append(child.tail)
    return "".join(parts)


def render_cfr_div(elem: ET.Element, depth: int = 0) -> list[str]:
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


def render_cfr_part(part_xml: bytes, cfr_title: str, part: str, full_title: str) -> str:
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
    out.append("> bold (`**`) preserved; tables and footnotes flattened to plain text.")
    out.append("")
    out.extend(render_cfr_div(target))
    text = "\n".join(out).rstrip() + "\n"
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out",
        default="plugins/claude-legal-immigration-laws/references/immigration-regulations",
    )
    ap.add_argument("--only", nargs="*", help="Limit to out-file tokens (e.g., 8CFR-1003-eoir-bia).")
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    only = {s.lower() for s in args.only} if args.only else None

    wrote, failed = 0, 0
    for (cfr_title, part, out_file, full_title) in CFR_PARTS:
        if only and out_file.lower() not in only:
            continue
        print(f"Fetching {cfr_title} CFR {part} ({out_file}) ...", flush=True)
        try:
            xml_bytes = fetch_cfr_part_xml(cfr_title, part)
            md = render_cfr_part(xml_bytes, cfr_title, part, full_title)
        except Exception as e:
            print(f"  ! eCFR fetch/render failed: {e}", flush=True)
            failed += 1
            continue
        path = out_dir / f"{out_file}.md"
        tmp = path.with_suffix(".md.tmp")
        tmp.write_text(md, encoding="utf-8")
        tmp.replace(path)
        wrote += 1
        print(f"  wrote {path} ({len(md):,} bytes)", flush=True)

    manifest = {
        "version": "0.1.0",
        "last_pulled": date.today().isoformat(),
        "source": "https://www.ecfr.gov/api eCFR versioner API",
        "as_of": ECFR_AS_OF,
        "mode": "verbatim",
        "notes": "Pulled by scripts/pull_immigration_cfr.py. Curated 8 CFR (DHS ch I + EOIR ch V) and 22 CFR visa/passport parts.",
    }
    manifest_path = out_dir / "_manifest.json"
    tmp = manifest_path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    tmp.replace(manifest_path)
    print(f"Done. Wrote {wrote} part file(s), {failed} failed.", flush=True)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
