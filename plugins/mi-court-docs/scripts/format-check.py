#!/usr/bin/env python3
"""
MCR 1.109 / MCR 2.113 format checker for Michigan court documents.

Unpacks a .docx file, parses the document.xml and styles.xml, and
reports compliance with the MCR 1.109 / MCR 2.113 structural
requirements for documents filed in Michigan courts:

  - Letter paper (8.5" x 11" / 12240 x 15840 DXA)
  - Margins >= 1" on all sides (1440 DXA)
  - Line spacing >= 1.5
  - Body font size >= 12pt (24 half-points)
  - No color text in the body (legible black text expected)
  - No highlighting
  - Footer contains PAGE and NUMPAGES fields

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
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}

# DXA constants
DXA_PER_INCH = 1440
LETTER_WIDTH_DXA = 12240  # 8.5"
LETTER_HEIGHT_DXA = 15840  # 11"
MIN_MARGIN_DXA = 1440  # 1"


@dataclass
class CheckResult:
    name: str
    status: str  # "PASS", "WARN", "FAIL"
    detail: str


def qn(tag: str) -> str:
    """Resolve a namespaced tag."""
    prefix, local = tag.split(":")
    return f"{{{NS[prefix]}}}{local}"


def load_part(zf: zipfile.ZipFile, path: str) -> ET.Element | None:
    """Parse an XML part from the .docx archive."""
    try:
        data = zf.read(path)
    except KeyError:
        return None
    return ET.fromstring(data)


def check_paper_size(root: ET.Element) -> CheckResult:
    pg_sz = root.find(f".//{qn('w:sectPr')}/{qn('w:pgSz')}")
    if pg_sz is None:
        return CheckResult("Paper size", "FAIL", "No <w:pgSz> element found")
    w = int(pg_sz.get(qn("w:w"), 0))
    h = int(pg_sz.get(qn("w:h"), 0))
    if w == LETTER_WIDTH_DXA and h == LETTER_HEIGHT_DXA:
        return CheckResult("Paper size", "PASS", f"Letter ({w} x {h} DXA)")
    if h == LETTER_WIDTH_DXA and w == LETTER_HEIGHT_DXA:
        return CheckResult("Paper size", "WARN", "Letter in landscape orientation")
    return CheckResult(
        "Paper size",
        "FAIL",
        f"Expected 12240 x 15840 DXA (Letter), got {w} x {h}",
    )


def check_margins(root: ET.Element) -> CheckResult:
    pg_mar = root.find(f".//{qn('w:sectPr')}/{qn('w:pgMar')}")
    if pg_mar is None:
        return CheckResult("Margins", "FAIL", "No <w:pgMar> element found")
    sides = {
        "top": int(pg_mar.get(qn("w:top"), 0)),
        "right": int(pg_mar.get(qn("w:right"), 0)),
        "bottom": int(pg_mar.get(qn("w:bottom"), 0)),
        "left": int(pg_mar.get(qn("w:left"), 0)),
    }
    small = {k: v for k, v in sides.items() if v < MIN_MARGIN_DXA}
    if not small:
        in_sides = {k: f"{v/DXA_PER_INCH:.2f}\"" for k, v in sides.items()}
        return CheckResult("Margins", "PASS", f"All >= 1\": {in_sides}")
    in_small = {k: f"{v/DXA_PER_INCH:.2f}\"" for k, v in small.items()}
    return CheckResult(
        "Margins",
        "FAIL",
        f"Margins below 1\" minimum: {in_small}",
    )


def check_line_spacing(root: ET.Element) -> CheckResult:
    """
    Line spacing is expressed as w:spacing with w:line and w:lineRule.
    'auto' rule uses 240ths: 360 = 1.5x, 480 = 2x.

    Some paragraphs (footer, captions, cover pages) are legitimately
    single-spaced. Check the MODE (most common) spacing for body
    paragraphs.
    """
    from collections import Counter

    spacings = root.findall(f".//{qn('w:p')}/{qn('w:pPr')}/{qn('w:spacing')}")
    if not spacings:
        return CheckResult(
            "Line spacing",
            "WARN",
            "No paragraph-level spacing found (check styles.xml manually)",
        )
    values: list[int] = []
    for s in spacings:
        line = s.get(qn("w:line"))
        rule = s.get(qn("w:lineRule"), "auto")
        if line and rule == "auto":
            values.append(int(line))
    if not values:
        return CheckResult(
            "Line spacing",
            "WARN",
            "No 'auto' line spacing found; using default",
        )
    counter = Counter(values)
    mode = counter.most_common(1)[0][0]
    mode_ratio = mode / 240
    min_value = min(values)
    min_ratio = min_value / 240
    if mode >= 360:
        if min_value >= 360:
            return CheckResult(
                "Line spacing",
                "PASS",
                f"Body spacing {mode_ratio:.2f}x (min {min_ratio:.2f}x)",
            )
        return CheckResult(
            "Line spacing",
            "PASS",
            f"Body spacing {mode_ratio:.2f}x (some footer/caption paragraphs at {min_ratio:.2f}x — expected)",
        )
    return CheckResult(
        "Line spacing",
        "FAIL",
        f"Body mode spacing {mode_ratio:.2f}x is below 1.5x",
    )


def check_font_size(root: ET.Element) -> CheckResult:
    """
    Font size lives in <w:rPr><w:sz w:val="X"/> where X is half-points.
    12pt = 24 half-points.
    """
    sizes: list[int] = []
    for sz in root.findall(f".//{qn('w:sz')}"):
        val = sz.get(qn("w:val"))
        if val and val.isdigit():
            sizes.append(int(val))
    if not sizes:
        return CheckResult(
            "Font size",
            "WARN",
            "No explicit <w:sz> found (relying on default)",
        )
    from collections import Counter

    counter = Counter(sizes)
    mode = counter.most_common(1)[0][0]
    min_size = min(sizes)
    if min_size >= 24:
        return CheckResult(
            "Font size",
            "PASS",
            f"All runs >= 12pt (min {min_size/2:.1f}pt; mode {mode/2:.1f}pt)",
        )
    if mode >= 24:
        return CheckResult(
            "Font size",
            "WARN",
            f"Some runs below 12pt (min {min_size/2:.1f}pt) but body mode is {mode/2:.1f}pt",
        )
    return CheckResult(
        "Font size",
        "FAIL",
        f"Body font appears below 12pt (mode {mode/2:.1f}pt)",
    )


def check_font_family(root: ET.Element) -> CheckResult:
    fonts = set()
    for rfonts in root.findall(f".//{qn('w:rFonts')}"):
        for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            v = rfonts.get(qn(attr))
            if v:
                fonts.add(v)
    if not fonts:
        return CheckResult(
            "Font family",
            "WARN",
            "No explicit font family declared",
        )
    acceptable = {
        "Times New Roman",
        "Times",
        "Cambria",
        "Palatino",
        "Palatino Linotype",
        "Garamond",
        "Book Antiqua",
        "Century Schoolbook",
        "Arial",  # MCR practice accepts Arial as well
    }
    used_acceptable = fonts & acceptable
    if used_acceptable:
        return CheckResult(
            "Font family",
            "PASS",
            f"Uses acceptable font(s): {sorted(used_acceptable)}",
        )
    return CheckResult(
        "Font family",
        "WARN",
        f"Non-standard fonts detected: {sorted(fonts)}. MCR 1.109 / 2.113 practice prefers a serif (Times New Roman) or Arial.",
    )


def check_no_color(root: ET.Element) -> CheckResult:
    """
    MCR 1.109 / 2.113: legible black text expected. Check for non-black
    text color and any highlighting.
    """
    violations: list[str] = []
    for color in root.findall(f".//{qn('w:color')}"):
        val = color.get(qn("w:val"), "auto")
        # Allow black, auto, and dark-blue approximations
        if val not in ("auto", "000000", "000080", "00008B"):
            violations.append(f"color={val}")
    for hl in root.findall(f".//{qn('w:highlight')}"):
        val = hl.get(qn("w:val"), "none")
        if val not in ("none",):
            violations.append(f"highlight={val}")
    for shd in root.findall(f".//{qn('w:shd')}"):
        fill = shd.get(qn("w:fill"), "auto")
        if fill not in ("auto", "FFFFFF", "ffffff"):
            violations.append(f"shading={fill}")
    if not violations:
        return CheckResult("No color markings", "PASS", "No color text, highlight, or shading detected")
    unique = sorted(set(violations))
    if len(unique) <= 5:
        return CheckResult(
            "No color markings",
            "WARN",
            f"Color markings found: {unique}. Review — MCR 1.109 / 2.113 permits color only when grayscale would make exhibits illegible.",
        )
    return CheckResult(
        "No color markings",
        "FAIL",
        f"{len(violations)} color markings found. MCR 1.109 / 2.113 expects legible black text in submissions; color permitted only for exhibits that require it.",
    )


def check_footer_pagination(zf: zipfile.ZipFile) -> CheckResult:
    """
    Verify every generated document has the required footer:
      - PAGE field (current page number)
      - NUMPAGES field (total page count, for "of Y")
      - A document title on the left (non-pagination literal text)
    """
    footer_parts = [n for n in zf.namelist() if n.startswith("word/footer") and n.endswith(".xml")]
    if not footer_parts:
        return CheckResult("Footer pagination", "FAIL", "No footer part found")

    has_page = False
    has_numpages = False
    literal_text = ""

    for part in footer_parts:
        root = load_part(zf, part)
        if root is None:
            continue
        # Complex-field run: <w:instrText>PAGE</w:instrText>
        for instr in root.findall(f".//{qn('w:instrText')}"):
            text = (instr.text or "").strip().upper()
            if "NUMPAGES" in text:
                has_numpages = True
            elif "PAGE" in text:
                has_page = True
        # Simple-field: <w:fldSimple w:instr="PAGE"/>
        for fld in root.findall(f".//{qn('w:fldSimple')}"):
            instr = fld.get(qn("w:instr"), "").upper()
            if "NUMPAGES" in instr:
                has_numpages = True
            elif "PAGE" in instr:
                has_page = True
        # Literal text runs
        for t in root.findall(f".//{qn('w:t')}"):
            if t.text:
                literal_text += t.text

    if not has_page:
        return CheckResult(
            "Footer pagination",
            "FAIL",
            "No PAGE field found in any footer — add 'Page X of Y'",
        )
    if not has_numpages:
        return CheckResult(
            "Footer pagination",
            "FAIL",
            "Footer has PAGE but no NUMPAGES field — use 'Page X of Y', not just 'Page X'",
        )
    # Strip the expected pagination literals; anything left should be the title
    stripped = literal_text.replace("Page", "").replace("of", "").strip()
    if not stripped:
        return CheckResult(
            "Footer pagination",
            "FAIL",
            "Footer has 'Page X of Y' but no document title on the left",
        )
    preview = stripped if len(stripped) <= 60 else stripped[:57] + "..."
    return CheckResult(
        "Footer pagination",
        "PASS",
        f"Footer has title + 'Page X of Y' (title: '{preview}')",
    )


def run_checks(docx_path: Path) -> list[CheckResult]:
    if not docx_path.exists():
        return [CheckResult("File", "FAIL", f"File not found: {docx_path}")]
    if docx_path.suffix.lower() != ".docx":
        return [CheckResult("File", "FAIL", f"Not a .docx file: {docx_path}")]

    results: list[CheckResult] = []
    with zipfile.ZipFile(docx_path) as zf:
        doc_root = load_part(zf, "word/document.xml")
        if doc_root is None:
            return [CheckResult("Structure", "FAIL", "Missing word/document.xml")]

        results.append(check_paper_size(doc_root))
        results.append(check_margins(doc_root))
        results.append(check_line_spacing(doc_root))
        results.append(check_font_family(doc_root))
        results.append(check_font_size(doc_root))
        results.append(check_no_color(doc_root))
        results.append(check_footer_pagination(zf))

    return results


def format_report(path: Path, results: list[CheckResult]) -> str:
    icon = {"PASS": "PASS", "WARN": "WARN", "FAIL": "FAIL"}
    lines = [f"MCR 1.109 / 2.113 Format Check: {path.name}", "=" * 60]
    for r in results:
        lines.append(f"  [{icon[r.status]:4}] {r.name}: {r.detail}")
    passes = sum(1 for r in results if r.status == "PASS")
    warns = sum(1 for r in results if r.status == "WARN")
    fails = sum(1 for r in results if r.status == "FAIL")
    lines.append("-" * 60)
    lines.append(f"  Summary: {passes} pass, {warns} warn, {fails} fail")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: format-check.py <path-to-docx>", file=sys.stderr)
        return 2
    path = Path(argv[1]).expanduser().resolve()
    results = run_checks(path)
    report = format_report(path, results)
    print(report)
    fails = sum(1 for r in results if r.status == "FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
