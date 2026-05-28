#!/usr/bin/env python3
"""
Ohio Civ. R. 10 format checker for Ohio court documents.

Unpacks a .docx file, parses the document.xml, and reports
compliance with Ohio Civ. R. 10's structural requirements
plus the common local-rule conventions adopted by most
Ohio Courts of Common Pleas + Municipal Courts:

  - Letter paper (8.5 x 11 / 12240 x 15840 DXA)
  - Margins >= 1 inch sides + bottom; 1.5 inch top on
    page one for caption (Civ. R. 10(A))
  - Body font: 12-point minimum
  - Line spacing: double-spaced body (most Ohio local rules)
  - Black text on white
  - Footer with page number

Ohio does NOT have a statewide pleading-format rule
analogous to CRC 2.100 or GR 14. Format requirements
live in Civ. R. 10 + each court's local rules. This
script enforces the common-denominator baseline.

Usage:
    python3 format-check.py <path-to-docx>

Output: human-readable pass/warn/fail report.
Exit code: 0 if all pass, 1 if any fail.
"""

from __future__ import annotations

import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET


# WordprocessingML namespaces
NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
}

# DXA constants
DXA_PER_INCH = 1440
LETTER_WIDTH_DXA = 12240    # 8.5 inches
LETTER_HEIGHT_DXA = 15840   # 11 inches
MIN_MARGIN_SIDES_DXA = 1440         # 1 inch sides + bottom
MIN_MARGIN_TOP_FIRST_DXA = 2160     # 1.5 inches top first page

MIN_BODY_HALF_POINTS = 24   # 12 points
DOUBLE_SPACING_MIN = 480    # half-points; ~2x


@dataclass
class CheckResult:
    name: str
    status: str  # "PASS", "WARN", "FAIL"
    detail: str


def _check_page_size(sect_pr: ET.Element) -> CheckResult:
    pg = sect_pr.find("w:pgSz", NS)
    if pg is None:
        return CheckResult("Page size", "WARN",
                           "no <w:pgSz> element found")
    w = int(pg.get(f"{{{NS['w']}}}w") or 0)
    h = int(pg.get(f"{{{NS['w']}}}h") or 0)
    if w == LETTER_WIDTH_DXA and h == LETTER_HEIGHT_DXA:
        return CheckResult("Page size", "PASS",
                           "Letter (8.5 x 11)")
    return CheckResult(
        "Page size", "FAIL",
        f"expected Letter ({LETTER_WIDTH_DXA}x"
        f"{LETTER_HEIGHT_DXA}); got {w}x{h} DXA",
    )


def _check_margins(sect_pr: ET.Element) -> list[CheckResult]:
    mar = sect_pr.find("w:pgMar", NS)
    if mar is None:
        return [CheckResult("Margins", "WARN",
                            "no <w:pgMar>")]
    top = int(mar.get(f"{{{NS['w']}}}top") or 0)
    bottom = int(mar.get(f"{{{NS['w']}}}bottom") or 0)
    left = int(mar.get(f"{{{NS['w']}}}left") or 0)
    right = int(mar.get(f"{{{NS['w']}}}right") or 0)

    out: list[CheckResult] = []
    if top >= MIN_MARGIN_SIDES_DXA:
        out.append(CheckResult(
            "Top margin", "PASS",
            f"{top/DXA_PER_INCH:.2f} in "
            f"({'>=1.5 in if page-1 caption block' if top >= MIN_MARGIN_TOP_FIRST_DXA else '>=1 in'})",
        ))
    else:
        out.append(CheckResult(
            "Top margin", "FAIL",
            f"{top/DXA_PER_INCH:.2f} in (need >=1 in; "
            f"1.5 in for page-1 caption per Civ. R. 10(A))",
        ))
    for label, val in [("Bottom", bottom),
                        ("Left", left),
                        ("Right", right)]:
        if val >= MIN_MARGIN_SIDES_DXA:
            out.append(CheckResult(
                f"{label} margin", "PASS",
                f"{val/DXA_PER_INCH:.2f} in",
            ))
        else:
            out.append(CheckResult(
                f"{label} margin", "FAIL",
                f"{val/DXA_PER_INCH:.2f} in (need >=1 in)",
            ))
    return out


def _check_fonts(doc_root: ET.Element) -> CheckResult:
    """Check body font is >= 12pt (24 half-points)."""
    bad = 0
    seen = 0
    for r in doc_root.iter(f"{{{NS['w']}}}r"):
        rpr = r.find("w:rPr", NS)
        if rpr is None:
            continue
        sz = rpr.find("w:sz", NS)
        if sz is None:
            continue
        try:
            v = int(sz.get(f"{{{NS['w']}}}val") or 0)
        except ValueError:
            continue
        seen += 1
        if v < MIN_BODY_HALF_POINTS:
            bad += 1
    if seen == 0:
        return CheckResult("Body font size", "WARN",
                           "no explicit font sizes found "
                           "(template default may apply)")
    if bad == 0:
        return CheckResult("Body font size", "PASS",
                           f"all {seen} runs >= 12pt")
    return CheckResult("Body font size", "FAIL",
                       f"{bad} of {seen} runs below 12pt")


def _check_line_spacing(doc_root: ET.Element) -> CheckResult:
    """Check body paragraphs are double-spaced (most Ohio
    local rules require it; some allow 1.5x)."""
    bad = 0
    seen = 0
    for p in doc_root.iter(f"{{{NS['w']}}}p"):
        ppr = p.find("w:pPr", NS)
        if ppr is None:
            continue
        spacing = ppr.find("w:spacing", NS)
        if spacing is None:
            continue
        line = spacing.get(f"{{{NS['w']}}}line")
        if line is None:
            continue
        try:
            v = int(line)
        except ValueError:
            continue
        seen += 1
        if v < DOUBLE_SPACING_MIN:
            bad += 1
    if seen == 0:
        return CheckResult("Line spacing", "WARN",
                           "no explicit spacing found "
                           "(template default may apply)")
    if bad == 0:
        return CheckResult("Line spacing", "PASS",
                           f"all {seen} paragraphs >= 2x")
    return CheckResult("Line spacing", "WARN",
                       f"{bad} of {seen} paragraphs < 2x "
                       "(some Ohio local rules allow 1.5x)")


def _check_footer_page_number(zf: zipfile.ZipFile) -> CheckResult:
    """Detect a footer with a PAGE field for pagination."""
    footers = [n for n in zf.namelist()
                if "footer" in n.lower() and n.endswith(".xml")]
    if not footers:
        return CheckResult("Footer pagination", "WARN",
                           "no footer XML found")
    for fn in footers:
        body = zf.read(fn).decode("utf-8", errors="replace")
        if "PAGE" in body.upper():
            return CheckResult("Footer pagination", "PASS",
                               f"PAGE field in {fn}")
    return CheckResult("Footer pagination", "WARN",
                       "footer present but no PAGE field "
                       "found (most Ohio local rules "
                       "require page numbering)")


def check_docx(path: Path) -> tuple[int, list[CheckResult]]:
    if not path.exists():
        return 1, [CheckResult(
            "File", "FAIL",
            f"{path} does not exist",
        )]
    results: list[CheckResult] = []
    try:
        with zipfile.ZipFile(path) as zf:
            try:
                doc_xml = zf.read("word/document.xml")
            except KeyError:
                return 1, [CheckResult(
                    "Document", "FAIL",
                    "word/document.xml not found",
                )]
            doc_root = ET.fromstring(doc_xml)
            sect_pr = doc_root.find(".//w:sectPr", NS)
            if sect_pr is None:
                results.append(CheckResult(
                    "Section properties", "FAIL",
                    "no <w:sectPr>",
                ))
            else:
                results.append(_check_page_size(sect_pr))
                results.extend(_check_margins(sect_pr))
            results.append(_check_fonts(doc_root))
            results.append(_check_line_spacing(doc_root))
            results.append(_check_footer_page_number(zf))
    except (zipfile.BadZipFile, ET.ParseError) as e:
        return 1, [CheckResult(
            "Document", "FAIL",
            f"could not parse .docx: {type(e).__name__}: {e}",
        )]
    return 0, results


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: format-check.py <path-to-docx>",
              file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    rc, results = check_docx(path)

    print(f"Ohio Civ. R. 10 Format Check: {path.name}")
    print("=" * 60)
    fail = 0
    for r in results:
        bullet = {"PASS": "✓", "WARN": "?", "FAIL": "✗"}.get(
            r.status, "?")
        print(f"  {bullet} [{r.status:<4}] {r.name}: {r.detail}")
        if r.status == "FAIL":
            fail += 1
    print("=" * 60)
    print(f"{fail} failure(s); "
          f"{sum(1 for r in results if r.status == 'WARN')} "
          f"warning(s); "
          f"{sum(1 for r in results if r.status == 'PASS')} pass(es).")
    return 1 if fail or rc else 0


if __name__ == "__main__":
    sys.exit(main())
