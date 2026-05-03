#!/usr/bin/env python3
"""Pull all Washington State court rules and convert them to per-rule-set Markdown files.

Source index: https://www.courts.wa.gov/court_rules/
Each rule set's list page links out to per-rule PDFs. We fetch each list page,
extract (rule_num, title, pdf_url) tuples, download every PDF, run pdftotext,
and concatenate the results into a single MD file per rule set.

Output: plugins/wa-court-docs/skills/wa-law-references/references/court-rules/<SET>.md
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path

BASE = "https://www.courts.wa.gov"
LIST_URL = BASE + "/court_rules/?fa=court_rules.list&group={group}&set={set}"
USER_AGENT = "wa-court-docs-marketplace/1.0 (+https://github.com/) court-rules-puller"

# (group, set, full_title) — taken from the rule-set index pages
RULE_SETS: list[tuple[str, str, str]] = [
    # General Application
    ("ga", "GR", "General Rules"),
    ("ga", "CJC", "Code of Judicial Conduct"),
    ("ga", "DRJ", "Discipline Rules for Judges"),
    ("ga", "BJAR", "Board for Judicial Administration Rules"),
    ("ga", "APR", "Admission and Practice Rules"),
    ("ga", "RPC", "Rules of Professional Conduct"),
    ("ga", "LPORPC", "Limited Practice Officer Rules of Professional Conduct"),
    ("ga", "LLLT RPC", "Limited License Legal Technician Rules of Professional Conduct"),
    ("ga", "ELC", "Rules for Enforcement of Lawyer Conduct"),
    ("ga", "ELPOC", "Rules for Enforcement of Limited Practice Officer Conduct"),
    ("ga", "ELLLTC", "Rules for Enforcement of Limited License Legal Technician Conduct"),
    ("ga", "JISCR", "Judicial Information System Committee Rules"),
    ("ga", "ER", "Rules of Evidence"),
    # Superior Court
    ("sup", "AR", "Superior Court Administrative Rules"),
    ("sup", "CCR", "Superior Court Civil Commitment Rules"),
    ("sup", "CR", "Superior Court Civil Rules"),
    ("sup", "SCCAR", "Superior Court Civil Arbitration Rules"),
    ("sup", "SPR", "Superior Court Special Proceedings"),
    ("sup", "GALR", "Superior Court Guardian ad Litem Rules"),
    ("sup", "CrR", "Superior Court Criminal Rules"),
    ("sup", "SPRC", "Superior Court Special Proceedings Rules -- Criminal"),
    ("sup", "JuCR", "Juvenile Court Rules"),
    # Courts of Limited Jurisdiction
    ("clj", "ARLJ", "Administrative Rules for Courts of Limited Jurisdiction"),
    ("clj", "RALJ", "Rules for Appeal of Decisions of Courts of Limited Jurisdiction"),
    ("clj", "CRLJ", "Civil Rules for Courts of Limited Jurisdiction"),
    ("clj", "CrRLJ", "Criminal Rules for Courts of Limited Jurisdiction"),
    ("clj", "IRLJ", "Infraction Rules for Courts of Limited Jurisdiction"),
    # Appellate
    ("app", "RAP", "Rules of Appellate Procedure"),
    # Appellate Court Administration
    ("aca", "SAR", "Supreme Court Administrative Rules"),
    ("aca", "CAR", "Court of Appeals Administrative Rules"),
    ("aca", "SCAR", "Supplemental Court of Appeals Administrative Rule"),
    # Additional Matter
    ("am", "ATJ", "Access to Justice"),
    ("am", "BBP", "Bench-Bar-Press Committee Statement of Principles"),
    ("am", "BJA", "Advisory Case Processing Time Standards"),
    ("am", "Table", "Table of Adoptions and Amendments"),
]


def http_get(url: str, *, retries: int = 3, sleep: float = 1.0) -> bytes:
    # Quote any spaces / control chars in the path so urllib.request accepts the URL.
    parsed = urllib.parse.urlsplit(url)
    safe_path = urllib.parse.quote(parsed.path, safe="/%")
    safe_url = urllib.parse.urlunsplit(
        (parsed.scheme, parsed.netloc, safe_path, parsed.query, parsed.fragment)
    )
    req = urllib.request.Request(safe_url, headers={"User-Agent": USER_AGENT})
    last_exc: Exception | None = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:
            last_exc = e
            time.sleep(sleep * (2**attempt))
    assert last_exc is not None
    raise last_exc


# Two HTML row shapes to capture:
#   <td valign="top">RULE_NUM</td>  ...  <a href="...pdf"> TITLE </a></td>
# Section headers (between groups of rules) we ignore for now; we just want the rules.
ROW_RE = re.compile(
    r"<td[^>]*>\s*(?P<num>[^<\s][^<]*?)\s*</td>\s*"
    r"<td[^>]*>\s*<a[^>]+href=\"(?P<href>[^\"]*?\.pdf)\"[^>]*>\s*(?P<title>.*?)\s*</a>",
    re.IGNORECASE | re.DOTALL,
)
# Section-header rows look like: <td colspan=2 ...><a name="..."></a><br><b>1 Scope of Rules</b></td>
SECTION_RE = re.compile(
    r"<td[^>]*colspan=2[^>]*>\s*(?:<a[^>]*></a>\s*)?(?:<br[^>]*>\s*)?<b>\s*(?P<header>[^<]+?)\s*</b>",
    re.IGNORECASE | re.DOTALL,
)


def parse_list_page(group: str, set_id: str, html_bytes: bytes) -> list[dict]:
    """Walk the list page in document order, attaching the most recent section header to each rule."""
    text = html_bytes.decode("utf-8", errors="replace")
    # Trim to the main body to avoid matching nav/footer.
    body_start = text.find('class="mainPage"')
    if body_start != -1:
        text = text[body_start:]
    footer_start = text.find('<div class="footerOuter">')
    if footer_start != -1:
        text = text[:footer_start]

    rules: list[dict] = []
    current_section: str | None = None
    pos = 0
    while pos < len(text):
        m_section = SECTION_RE.search(text, pos)
        m_row = ROW_RE.search(text, pos)
        if not m_row and not m_section:
            break
        # Whichever comes first
        if m_section and (not m_row or m_section.start() < m_row.start()):
            current_section = html.unescape(m_section.group("header")).strip()
            pos = m_section.end()
            continue
        assert m_row is not None
        num_raw = html.unescape(m_row.group("num")).strip()
        title_raw = m_row.group("title")
        # Title may contain inline <br> and other tags; strip tags and normalize whitespace.
        title = re.sub(r"<[^>]+>", " ", title_raw)
        title = html.unescape(title)
        title = re.sub(r"\s+", " ", title).strip(" -")
        href = m_row.group("href")
        # Any row with a PDF link is a rule entry; section headers don't have PDF links.
        if num_raw and href:
            pdf_url = urllib.parse.urljoin(BASE + "/court_rules/", href)
            rules.append(
                {
                    "set": set_id,
                    "group": group,
                    "num": num_raw,
                    "title": title,
                    "section": current_section,
                    "pdf_url": pdf_url,
                }
            )
        pos = m_row.end()

    # Fallback: pages with a single PDF in a colspan=2 row, or prose pages with PDFs in <p> tags.
    if not rules:
        anchor_re = re.compile(
            r"<a[^>]+href=\"(?P<href>[^\"]*?\.pdf)\"[^>]*>\s*(?P<title>.*?)\s*</a>",
            re.IGNORECASE | re.DOTALL,
        )
        for i, m in enumerate(anchor_re.finditer(text), start=1):
            href = m.group("href")
            title_raw = m.group("title")
            title = re.sub(r"<[^>]+>", " ", title_raw)
            title = html.unescape(title)
            title = re.sub(r"\s+", " ", title).strip(" -")
            # If multiple PDFs (e.g., ATJ), number them; if single, use set_id as the num.
            num = set_id if i == 1 else f"{set_id}-{i}"
            pdf_url = urllib.parse.urljoin(BASE + "/court_rules/", href)
            # If link text was a URL (some pages quote the link as href text), derive a title from the filename.
            if not title or title.lower().startswith(("http://", "https://", "www.")):
                stem = pdf_url.rsplit("/", 1)[-1].removesuffix(".pdf")
                title = re.sub(r"^[A-Z]+_[A-Z]+_", "", stem).replace("_", " ").strip() or full_title_for(set_id)
            rules.append(
                {
                    "set": set_id,
                    "group": group,
                    "num": num,
                    "title": title,
                    "section": current_section,
                    "pdf_url": pdf_url,
                }
            )
        # If a page with multiple PDFs got the first one named just `set_id`, that's fine —
        # we'll still see e.g. ATJ, ATJ-2 in the output.

    return rules


def full_title_for(set_id: str) -> str:
    for _g, s, t in RULE_SETS:
        if s == set_id:
            return t
    return set_id


def pdftotext(pdf_bytes: bytes) -> str:
    """Run pdftotext -layout on bytes; return UTF-8 text."""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as fp:
        fp.write(pdf_bytes)
        pdf_path = fp.name
    try:
        # -layout preserves columns/indentation; -nopgbrk drops form-feed page breaks.
        result = subprocess.run(
            ["pdftotext", "-layout", "-nopgbrk", "-enc", "UTF-8", pdf_path, "-"],
            capture_output=True,
            check=True,
        )
        return result.stdout.decode("utf-8", errors="replace")
    finally:
        Path(pdf_path).unlink(missing_ok=True)


def clean_text(text: str) -> str:
    # Collapse 3+ blank lines to 2.
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Strip trailing whitespace per line.
    text = "\n".join(line.rstrip() for line in text.splitlines())
    return text.strip()


def fetch_pdf_text(rule: dict) -> tuple[dict, str | None, str | None]:
    """Returns (rule, text, error)."""
    try:
        pdf_bytes = http_get(rule["pdf_url"])
        text = clean_text(pdftotext(pdf_bytes))
        return rule, text, None
    except Exception as e:
        return rule, None, f"{type(e).__name__}: {e}"


def render_set_md(set_id: str, group: str, full_title: str, rules: list[dict], texts: dict[str, str], errors: dict[str, str]) -> str:
    today = date.today().isoformat()
    list_url = LIST_URL.format(group=group, set=urllib.parse.quote(set_id))
    lines: list[str] = []
    lines.append(f"# {full_title} ({set_id})")
    lines.append("")
    lines.append(f"- Source: {list_url}")
    lines.append(f"- Pulled: {today}")
    lines.append(f"- Rules: {len(rules)}")
    lines.append("")
    lines.append("> Verbatim text extracted from the official PDFs published by the Washington")
    lines.append("> Administrative Office of the Courts. PDF layout extraction is imperfect; cite")
    lines.append("> the original PDF (linked under each rule) when accuracy matters.")
    lines.append("")

    # Table of contents
    lines.append("## Contents")
    lines.append("")
    last_section: str | None = None
    for r in rules:
        if r.get("section") and r["section"] != last_section:
            lines.append(f"- **{r['section']}**")
            last_section = r["section"]
        anchor = f"{set_id.lower().replace(' ', '-')}-{r['num'].lower().replace('.', '-').replace(' ', '-')}"
        lines.append(f"  - [{set_id} {r['num']} — {r['title']}](#{anchor})")
    lines.append("")

    # Rule bodies
    last_section = None
    for r in rules:
        if r.get("section") and r["section"] != last_section:
            lines.append(f"## {r['section']}")
            lines.append("")
            last_section = r["section"]
        anchor = f"{set_id.lower().replace(' ', '-')}-{r['num'].lower().replace('.', '-').replace(' ', '-')}"
        lines.append(f'<a id="{anchor}"></a>')
        lines.append(f"### {set_id} {r['num']} — {r['title']}")
        lines.append("")
        lines.append(f"Source: {r['pdf_url']}")
        lines.append("")
        if r["num"] in errors:
            lines.append(f"> **Extraction failed:** {errors[r['num']]}")
            lines.append("")
            continue
        body = texts.get(r["num"], "").strip()
        if not body:
            lines.append("> _(empty extraction)_")
            lines.append("")
            continue
        lines.append("```")
        lines.append(body)
        lines.append("```")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out",
        default="plugins/wa-court-docs/skills/wa-law-references/references/court-rules",
        help="Output directory (relative to repo root or absolute).",
    )
    ap.add_argument("--workers", type=int, default=8, help="Parallel PDF fetch workers.")
    ap.add_argument("--only", nargs="*", help="Optional list of set IDs to limit to (debugging).")
    ap.add_argument("--manifest", default=None, help="Optional path to write a JSON manifest of all rules.")
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest: dict = {"pulled": date.today().isoformat(), "sets": []}

    sets_to_process = RULE_SETS
    if args.only:
        only = {s.lower() for s in args.only}
        sets_to_process = [t for t in RULE_SETS if t[1].lower() in only]

    grand_total = 0
    grand_failed = 0

    for group, set_id, full_title in sets_to_process:
        print(f"\n=== {set_id} ({full_title}) [group={group}] ===", flush=True)
        list_url = LIST_URL.format(group=group, set=urllib.parse.quote(set_id))
        try:
            list_html = http_get(list_url)
        except Exception as e:
            print(f"  ! list page failed: {e}", flush=True)
            continue
        rules = parse_list_page(group, set_id, list_html)
        print(f"  found {len(rules)} rules", flush=True)
        if not rules:
            # Write a placeholder noting the empty set so the index is complete.
            md = (
                f"# {full_title} ({set_id})\n\n"
                f"- Source: {list_url}\n- Pulled: {date.today().isoformat()}\n\n"
                f"_No individual rules extracted from the list page._\n"
            )
            (out_dir / f"{set_id.replace(' ', '_')}.md").write_text(md, encoding="utf-8")
            continue

        texts: dict[str, str] = {}
        errors: dict[str, str] = {}
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = {ex.submit(fetch_pdf_text, r): r for r in rules}
            done = 0
            for fut in as_completed(futs):
                done += 1
                r, text, err = fut.result()
                if err:
                    errors[r["num"]] = err
                    print(f"    [{done}/{len(rules)}] {set_id} {r['num']} FAIL: {err}", flush=True)
                else:
                    texts[r["num"]] = text or ""

        md = render_set_md(set_id, group, full_title, rules, texts, errors)
        out_path = out_dir / f"{set_id.replace(' ', '_')}.md"
        out_path.write_text(md, encoding="utf-8")
        print(f"  wrote {out_path} ({len(rules)} rules, {len(errors)} errors)", flush=True)
        grand_total += len(rules)
        grand_failed += len(errors)
        manifest["sets"].append(
            {
                "set": set_id,
                "group": group,
                "title": full_title,
                "list_url": list_url,
                "file": out_path.name,
                "rules": rules,
                "errors": errors,
            }
        )

    if args.manifest:
        Path(args.manifest).write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        print(f"\nmanifest -> {args.manifest}", flush=True)

    print(f"\nDone. {grand_total} rules across {len(manifest['sets'])} sets, {grand_failed} extraction errors.", flush=True)
    return 0 if grand_failed == 0 else 0  # don't fail on per-PDF errors; they're recorded in the MD


if __name__ == "__main__":
    sys.exit(main())
