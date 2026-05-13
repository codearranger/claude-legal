#!/usr/bin/env python3
"""Pull selected debt-relevant California statutory chapters from
leginfo.legislature.ca.gov and convert to MD.

Output: plugins/ca-court-docs/skills/ca-law-references/references/ca-statutes-debt/
One MD file per topic, each section as its own heading inside.

Modeled on scripts/pull_wa_rcw.py. The CA target is the
California Legislative Information bulk codes view at
leginfo.legislature.ca.gov.

URL patterns used:

  - Expanded branch (chapter / article TOC):
    https://leginfo.legislature.ca.gov/faces/codes_displayexpandedbranch.xhtml?tocCode=<CODE>&division=...&title=...&part=...&chapter=...&article=...

  - Single section:
    https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=<CODE>&sectionNum=<NUM>.

Codes referenced here:

  - CCP  — Code of Civil Procedure
  - CIV  — Civil Code
  - BPC  — Business and Professions Code
  - FIN  — Financial Code
  - COM  — Commercial Code

NOTE: leginfo's HTML is JSF (JavaServer Faces) with view-state
tokens. This puller uses the public displaySection endpoint which
serves a stable HTML body for each section. If the site changes
its URL or HTML scheme, update the SECTION_URL / parser below.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path

USER_AGENT = (
    "claude-legal/1.0 (+https://github.com/codearranger/claude-legal) "
    "ca-statutes-puller"
)
BASE = "https://leginfo.legislature.ca.gov"
SECTION_URL = (
    BASE
    + "/faces/codes_displaySection.xhtml?lawCode={code}&sectionNum={section}."
)
RANGE_URL = (
    BASE
    + "/faces/codes_displayText.xhtml?lawCode={code}&division=&title="
    "&part=&chapter=&article=&sectionNum={section}."
)


# ---- Configuration: which sections to pull, grouped by output file ------------
#
# Each entry maps an OUTPUT FILE in ca-statutes-debt/ to a list of sections
# to fetch. Sections are tuples of (code, section_number, label).
#
# Section numbers must exactly match the lookup format on leginfo. For
# California, many codes have section numbers with embedded dots (e.g.,
# "1788.30" for Cal. Civ. Code § 1788.30); preserve them as strings.
#
# To add coverage:
#   1. Append a new (code, section, label) tuple to the relevant FILE entry,
#      OR add a new FILE entry mapping output filename → section list
#   2. Re-run the puller
#
# These groupings mirror the topic-organized files already authored in
# ca-statutes-debt/, so the puller will incrementally enrich them with
# verbatim text from leginfo.

CCP_SOL = [
    ("CCP", "312",   "General SOL rule"),
    ("CCP", "313",   "Acquired rights"),
    ("CCP", "318",   "Real property — 5 years"),
    ("CCP", "335.1", "Personal injury — 2 years"),
    ("CCP", "337",   "Written contract / book account — 4 years"),
    ("CCP", "338",   "3-year actions; fraud/mistake discovery rule"),
    ("CCP", "339",   "Oral contract — 2 years"),
    ("CCP", "340",   "1-year actions"),
    ("CCP", "343",   "Catch-all — 4 years"),
    ("CCP", "360",   "Revival by acknowledgment / partial payment"),
    ("CCP", "361",   "Borrowing statute"),
    ("CCP", "366.2", "Action against decedent"),
]

CCP_TIME = [
    ("CCP", "12",    "Time computation — general rule"),
    ("CCP", "12a",   "Holidays — extension of period"),
    ("CCP", "12b",   "Half-holidays"),
    ("CCP", "12c",   "Court day defined"),
    ("CCP", "13",    "Single-day computation"),
    ("CCP", "135",   "Judicial holidays"),
]

CCP_SERVICE = [
    ("CCP", "412.10",  "Manner of service"),
    ("CCP", "412.20",  "Form of summons; 30-day answer"),
    ("CCP", "415.10",  "Personal service"),
    ("CCP", "415.20",  "Substituted service"),
    ("CCP", "415.30",  "Service by mail with NORF"),
    ("CCP", "415.40",  "Out-of-state service"),
    ("CCP", "415.50",  "Service by publication"),
    ("CCP", "416.10",  "Service on corporation"),
    ("CCP", "416.20",  "Service on partnership"),
    ("CCP", "417.10",  "Proof of service"),
    ("CCP", "417.20",  "Proof — service on entity"),
]

CCP_PLEADINGS = [
    ("CCP", "425.10",  "Required contents of complaint"),
    ("CCP", "425.11",  "Personal-injury statement of damages"),
    ("CCP", "425.16",  "Anti-SLAPP"),
    ("CCP", "426.10",  "Cross-complaints — definitions"),
    ("CCP", "426.30",  "Compulsory cross-complaint"),
    ("CCP", "428.10",  "Permissive cross-complaint"),
    ("CCP", "430.10",  "Grounds for demurrer"),
    ("CCP", "430.20",  "Grounds for demurrer to answer"),
    ("CCP", "430.30",  "Face-of-pleading rule"),
    ("CCP", "430.40",  "Time for demurrer"),
    ("CCP", "430.41",  "Meet-and-confer for demurrer"),
    ("CCP", "430.50",  "Demurrer to part of cause of action"),
    ("CCP", "431.30",  "Form of answer; verification"),
    ("CCP", "431.40",  "Verification by entity attorney"),
    ("CCP", "431.70",  "Setoff"),
    ("CCP", "435",     "Notice of motion to strike"),
    ("CCP", "435.5",   "Meet-and-confer for motion to strike"),
    ("CCP", "436",     "Authority of court to strike"),
    ("CCP", "437",     "Court rules and orders"),
    ("CCP", "437c",    "Summary judgment"),
    ("CCP", "438",     "Motion for judgment on pleadings"),
]

CCP_MOTIONS = [
    ("CCP", "1005",    "Motion notice / service / time"),
    ("CCP", "1010",    "Notice of motion — contents"),
    ("CCP", "1010.6",  "Electronic service"),
    ("CCP", "1011",    "Personal service of papers"),
    ("CCP", "1012",    "Service by mail"),
    ("CCP", "1013",    "Mail service extension"),
    ("CCP", "1013a",   "Proof of service by mail"),
    ("CCP", "1014",    "Appearance defined"),
    ("CCP", "1015",    "Other notices"),
    ("CCP", "1019",    "Filing of papers"),
    ("CCP", "1020",    "Service / filing acknowledgments"),
]

CCP_DISCOVERY = [
    ("CCP", "2017.010", "Scope of discovery"),
    ("CCP", "2023.030", "Sanctions"),
    ("CCP", "2024.020", "Trial-date cutoffs"),
    ("CCP", "2025.270", "Deposition notice — time"),
    ("CCP", "2025.450", "Motion to compel attendance"),
    ("CCP", "2030.010", "Right to propound interrogatories"),
    ("CCP", "2030.030", "35-special-interrogatory cap"),
    ("CCP", "2030.040", "Declaration of necessity for additional"),
    ("CCP", "2030.050", "Required declaration of necessity"),
    ("CCP", "2030.060", "Form of interrogatories"),
    ("CCP", "2030.260", "Time to respond"),
    ("CCP", "2030.300", "Motion to compel further (rogs)"),
    ("CCP", "2031.010", "Right to demand inspection"),
    ("CCP", "2031.260", "Time to respond to RFP"),
    ("CCP", "2031.310", "Motion to compel further (RFPs)"),
    ("CCP", "2031.320", "Failure to comply with compel order"),
    ("CCP", "2033.010", "Right to request admission"),
    ("CCP", "2033.030", "35-RFA cap (non-genuineness)"),
    ("CCP", "2033.250", "Time to respond to RFA"),
    ("CCP", "2033.280", "Failure to respond — deemed admitted"),
    ("CCP", "2033.290", "Motion to compel further (RFAs)"),
]

CCP_RELIEF = [
    ("CCP", "473",   "Relief from default — discretionary + mandatory"),
    ("CCP", "473.5", "Set aside default when no actual notice"),
]

CCP_ENFORCEMENT = [
    ("CCP", "683.020",  "10-year judgment life"),
    ("CCP", "683.110",  "Renewal of judgment"),
    ("CCP", "683.130",  "Renewal procedure"),
    ("CCP", "683.140",  "Effect of renewal"),
    ("CCP", "685.010",  "Post-judgment costs"),
    ("CCP", "685.030",  "Post-judgment costs added to judgment"),
    ("CCP", "697.310",  "Judgment lien on real property"),
    ("CCP", "697.510",  "Judgment lien on personal property"),
    ("CCP", "697.060",  "Duration of lien"),
    ("CCP", "699.510",  "Writ of execution"),
    ("CCP", "700.010",  "Levying officer"),
    ("CCP", "700.140",  "Levy on deposit accounts"),
    ("CCP", "706.010",  "Wage garnishment — application"),
    ("CCP", "706.022",  "Earnings withholding order"),
    ("CCP", "706.029",  "Priority"),
    ("CCP", "706.050",  "Withholding amount"),
    ("CCP", "706.105",  "Claim of exemption procedure"),
    ("CCP", "708.110",  "Judgment debtor exam"),
    ("CCP", "708.120",  "Third-party exam"),
    ("CCP", "708.170",  "Failure to appear"),
    ("CCP", "708.205",  "Turnover order"),
    ("CCP", "708.510",  "Assignment of rights to payment"),
    ("CCP", "708.610",  "Appointment of receiver"),
    ("CCP", "724.010",  "Acknowledgment of satisfaction"),
    ("CCP", "724.030",  "Filing acknowledgment"),
    ("CCP", "724.050",  "Demand for acknowledgment"),
    ("CCP", "724.080",  "Penalty for failure"),
    ("CCP", "724.110",  "Demand for acknowledgment with payment"),
    ("CCP", "918",      "Stay pending appeal"),
]

CCP_EXEMPTIONS = [
    ("CCP", "703.140", "Bankruptcy-style exemptions"),
    ("CCP", "703.520", "Claim of exemption — notice"),
    ("CCP", "703.530", "Levying officer's response"),
    ("CCP", "703.550", "Judgment creditor's response"),
    ("CCP", "703.580", "Hearing"),
    ("CCP", "704.010", "Motor vehicle"),
    ("CCP", "704.020", "Household goods"),
    ("CCP", "704.030", "Jewelry, heirlooms, art"),
    ("CCP", "704.040", "Health and safety items"),
    ("CCP", "704.060", "Tools of trade"),
    ("CCP", "704.070", "Paid earnings"),
    ("CCP", "704.080", "Deposit account"),
    ("CCP", "704.090", "Public benefits"),
    ("CCP", "704.100", "Life insurance"),
    ("CCP", "704.110", "Retirement"),
    ("CCP", "704.115", "Self-settled IRAs"),
    ("CCP", "704.140", "Personal injury recoveries"),
    ("CCP", "704.170", "Cemetery property"),
    ("CCP", "704.180", "Crime-victim compensation"),
    ("CCP", "704.710", "Homestead — definitions"),
    ("CCP", "704.720", "Automatic homestead exemption"),
    ("CCP", "704.730", "Homestead amount (AB 1885)"),
    ("CCP", "704.780", "Declaration of homestead"),
]

CIV_ROSENTHAL = [
    ("CIV", "1788",      "Title"),
    ("CIV", "1788.1",    "Findings"),
    ("CIV", "1788.2",    "Definitions"),
    ("CIV", "1788.10",   "Threats and use of force"),
    ("CIV", "1788.11",   "Communication frequency / pretense"),
    ("CIV", "1788.12",   "Communication with workplace / others"),
    ("CIV", "1788.13",   "False or misleading representations"),
    ("CIV", "1788.14",   "Specific abusive practices"),
    ("CIV", "1788.15",   "Litigation against debtor"),
    ("CIV", "1788.16",   "Postdated checks"),
    ("CIV", "1788.17",   "FDCPA incorporation"),
    ("CIV", "1788.18",   "Identity theft"),
    ("CIV", "1788.30",   "Remedies and damages"),
    ("CIV", "1788.32",   "Cumulative remedies"),
    ("CIV", "1788.33",   "Severability"),
]

CIV_FDBPA = [
    ("CIV", "1788.50",  "Definitions"),
    ("CIV", "1788.52",  "Pre-collection requirements"),
    ("CIV", "1788.58",  "Complaint requirements"),
    ("CIV", "1788.59",  "Requests for documentation"),
    ("CIV", "1788.60",  "Default judgment requirements"),
    ("CIV", "1788.61",  "Notice of sale of debt"),
    ("CIV", "1788.62",  "Remedies and damages"),
    ("CIV", "1788.63",  "Cumulative remedies"),
    ("CIV", "1788.65",  "Severability"),
    ("CIV", "1788.66",  "Effective date"),
]

CIV_CLRA = [
    ("CIV", "1750",   "Title and purpose"),
    ("CIV", "1761",   "Definitions"),
    ("CIV", "1770",   "Prohibited practices (24 enumerated)"),
    ("CIV", "1780",   "Remedies"),
    ("CIV", "1781",   "Class actions"),
    ("CIV", "1782",   "Pre-suit notice"),
    ("CIV", "1783",   "Statute of limitations"),
    ("CIV", "1784",   "Effect on existing rights"),
]

CIV_ATTY_FEES = [
    ("CIV", "1717",   "Reciprocal attorney's fees"),
    ("CIV", "1717.5", "Pleading requirements"),
]

BPC_UCL = [
    ("BPC", "17200",   "Unfair competition defined"),
    ("BPC", "17201",   "Person defined"),
    ("BPC", "17203",   "Remedies"),
    ("BPC", "17204",   "Standing"),
    ("BPC", "17205",   "Cumulative remedies"),
    ("BPC", "17206",   "Civil penalties (AG)"),
    ("BPC", "17208",   "Statute of limitations"),
    ("BPC", "17500",   "False advertising — prohibition"),
]

FIN_CDCLA = [
    ("FIN", "100000",  "Title"),
    ("FIN", "100001",  "Definitions"),
    ("FIN", "100002",  "License requirement"),
    ("FIN", "100003",  "Exemptions"),
    ("FIN", "100005",  "License application"),
    ("FIN", "100007",  "Surety bond"),
    ("FIN", "100008",  "Denial / suspension / revocation"),
    ("FIN", "100010",  "Renewal"),
    ("FIN", "100012",  "Continuing education"),
    ("FIN", "100015",  "Examination and supervision"),
    ("FIN", "100018",  "Rosenthal Act incorporation"),
    ("FIN", "100020",  "Enforcement"),
    ("FIN", "100027",  "Effective date"),
]

COM_ART2 = [
    ("COM", "2102",   "Scope"),
    ("COM", "2105",   "Definitions — goods"),
    ("COM", "2201",   "Statute of frauds"),
    ("COM", "2204",   "Formation in general"),
    ("COM", "2207",   "Battle of the forms"),
    ("COM", "2313",   "Express warranties"),
    ("COM", "2314",   "Implied warranty: merchantability"),
    ("COM", "2315",   "Implied warranty: fitness for purpose"),
    ("COM", "2316",   "Exclusion / modification of warranties"),
    ("COM", "2503",   "Tender of delivery"),
    ("COM", "2601",   "Buyer's rights upon nonconforming tender"),
    ("COM", "2607",   "Notice of breach"),
    ("COM", "2703",   "Seller's remedies"),
    ("COM", "2711",   "Buyer's remedies"),
    ("COM", "2715",   "Incidental and consequential damages"),
    ("COM", "2719",   "Contractual modification / limitation"),
    ("COM", "2725",   "Statute of limitations — 4 years"),
]

COM_ART3 = [
    ("COM", "3102",   "Scope"),
    ("COM", "3104",   "Negotiable instrument defined"),
    ("COM", "3301",   "Person entitled to enforce"),
    ("COM", "3302",   "Holder in due course"),
    ("COM", "3305",   "Defenses against person entitled to enforce"),
    ("COM", "3308",   "Proof of signatures / status"),
    ("COM", "3309",   "Lost / destroyed / stolen instrument"),
    ("COM", "3118",   "Statute of limitations"),
]

COM_ART9 = [
    ("COM", "9101",   "Short title"),
    ("COM", "9102",   "Definitions"),
    ("COM", "9203",   "Attachment"),
    ("COM", "9310",   "Perfection by filing"),
    ("COM", "9404",   "Rights acquired by assignee"),
    ("COM", "9406",   "Discharge of account debtor"),
    ("COM", "9601",   "Rights after default"),
    ("COM", "9610",   "Disposition of collateral"),
    ("COM", "9611",   "Notification before disposition"),
    ("COM", "9615",   "Application of proceeds"),
    ("COM", "9626",   "Burden of proof — commercial reasonableness"),
]


# (output_file_stem, description, sections) — drives main() iteration
FILES: list[tuple[str, str, list[tuple[str, str, str]]]] = [
    ("CCP-Time-Computation",       "Time computation (CCP §§ 12-13)",                  CCP_TIME),
    ("CCP-SOL",                    "Statutes of limitation (CCP §§ 312-366)",          CCP_SOL),
    ("CCP-Service",                "Service of summons (CCP §§ 412.10-417.40)",        CCP_SERVICE),
    ("CCP-Pleadings",              "Pleadings, demurrer, MSJ (CCP §§ 425.10-440)",     CCP_PLEADINGS),
    ("CCP-Motions-1005-to-1020",   "Motion practice (CCP §§ 1005-1020)",               CCP_MOTIONS),
    ("CCP-Discovery",              "Civil Discovery Act (CCP §§ 2016.010-2036.050)",   CCP_DISCOVERY),
    ("CCP-Relief-473",             "Relief from default (CCP §§ 473-473.5)",           CCP_RELIEF),
    ("CCP-Enforcement",            "Enforcement of judgments (CCP §§ 683-708)",        CCP_ENFORCEMENT),
    ("CCP-Exemptions",             "Exemptions (CCP §§ 703.140 + 704.010-995)",        CCP_EXEMPTIONS),
    ("CivCode-Rosenthal",          "Rosenthal Act (Civ. Code §§ 1788-1788.33)",        CIV_ROSENTHAL),
    ("CivCode-FDBPA",              "FDBPA (Civ. Code §§ 1788.50-1788.66)",             CIV_FDBPA),
    ("CivCode-CLRA",               "CLRA (Civ. Code §§ 1750-1784)",                    CIV_CLRA),
    ("CivCode-Atty-Fees",          "Reciprocal fees (Civ. Code § 1717)",               CIV_ATTY_FEES),
    ("BPC-UCL",                    "UCL + FAL (B&P §§ 17200-17210, § 17500)",          BPC_UCL),
    ("FinCode-CDCLA",              "CDCLA (Fin. Code §§ 100000-100027)",               FIN_CDCLA),
    ("CommCode-Art-2-Sales",       "UCC Art. 2 (Cal. Comm. Code §§ 2101-2725)",        COM_ART2),
    ("CommCode-Art-3-Negotiable",  "UCC Art. 3 (Cal. Comm. Code §§ 3101-3605)",        COM_ART3),
    ("CommCode-Art-9-Secured",     "UCC Art. 9 (Cal. Comm. Code §§ 9101-9809)",        COM_ART9),
]


# ---- Networking ---------------------------------------------------------------

def http_get(url: str, *, retries: int = 3, sleep: float = 1.5) -> bytes:
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


# ---- HTML → text --------------------------------------------------------------

def html_to_text(s: str) -> str:
    """Convert HTML fragment to plain text with paragraph breaks at
    div/p/br boundaries. Mirrors the WA puller's approach."""
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", s, flags=re.IGNORECASE | re.DOTALL)
    s = re.sub(r"<(em|i)[^>]*>(.*?)</\1>", lambda m: f"*{m.group(2)}*", s, flags=re.IGNORECASE | re.DOTALL)
    s = re.sub(r"<(strong|b)[^>]*>(.*?)</\1>", lambda m: f"**{m.group(2)}**", s, flags=re.IGNORECASE | re.DOTALL)
    s = re.sub(
        r"<span[^>]*style=\"[^\"]*font-weight:\s*bold[^\"]*\"[^>]*>(.*?)</span>",
        lambda m: f"**{m.group(1)}**",
        s,
        flags=re.IGNORECASE | re.DOTALL,
    )
    s = re.sub(r"<br\s*/?>", "\x1e", s, flags=re.IGNORECASE)
    s = re.sub(r"</(p|div|li|h\d|tr|td|th|blockquote|article|section)\s*>", "\x1e", s, flags=re.IGNORECASE)
    s = re.sub(r"<(p|div|li|h\d|tr|td|th|blockquote|article|section)[^>]*>", "\x1e", s, flags=re.IGNORECASE)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    blocks: list[str] = []
    for raw in s.split("\x1e"):
        cleaned = re.sub(r"\s+", " ", raw).strip()
        if cleaned:
            blocks.append(cleaned)
    return "\n\n".join(blocks).strip()


# ---- Section parsing ----------------------------------------------------------

def parse_section(html_text: str, code: str, section: str) -> tuple[str, str]:
    """Returns (caption, body_md). Leginfo's section page wraps the
    text in <div id="manylawsections"> with the section number and
    body inline. The fallback path captures whatever main content
    block is present.
    """
    caption = ""
    body = ""

    # Caption: typically appears as "<h6>1788.30.</h6>" or similar
    cap_m = re.search(
        r"<h\d[^>]*>\s*" + re.escape(section) + r"\.?\s*</h\d>",
        html_text,
        re.IGNORECASE,
    )

    # Heuristic: find a div with id starting with manylawsections, otherwise
    # fall back to the section's surrounding content.
    body_re = re.compile(
        r"<div\s+id=['\"]manylawsections['\"][^>]*>(.*?)</div>\s*<div\s+id=['\"]hist['\"]",
        re.IGNORECASE | re.DOTALL,
    )
    body_m = body_re.search(html_text)
    if not body_m:
        # Fallback: content area without explicit history div
        body_re2 = re.compile(
            r"<div\s+id=['\"]manylawsections['\"][^>]*>(.*?)(?:</div>\s*<div\s+id=|<footer)",
            re.IGNORECASE | re.DOTALL,
        )
        body_m = body_re2.search(html_text)

    if body_m:
        body = html_to_text(body_m.group(1))

    # Use the body's first line as the caption if no heading found
    if cap_m and not caption:
        caption = section
    elif not caption and body:
        first = body.split("\n", 1)[0]
        if len(first) <= 200:
            caption = first

    return caption, body


def fetch_section(code: str, section: str) -> tuple[str, str, str, str, str | None]:
    """Returns (code, section, caption, body, error|None)."""
    url = SECTION_URL.format(code=code, section=section)
    try:
        html_bytes = http_get(url)
        caption, body = parse_section(html_bytes.decode("utf-8", errors="replace"), code, section)
        return code, section, caption, body, None
    except Exception as e:
        return code, section, "", "", f"{type(e).__name__}: {e}"


# ---- Render -------------------------------------------------------------------

CODE_DISPLAY = {
    "CCP": "Cal. Code Civ. Proc.",
    "CIV": "Cal. Civ. Code",
    "BPC": "Cal. Bus. & Prof. Code",
    "FIN": "Cal. Fin. Code",
    "COM": "Cal. Comm. Code",
    "EVID": "Cal. Evid. Code",
}


def render_file_md(
    stem: str,
    description: str,
    sections: list[tuple[str, str, str]],
    fetched: dict[tuple[str, str], tuple[str, str, str | None]],
) -> str:
    today = date.today().isoformat()
    out: list[str] = []
    out.append(f"# {description}")
    out.append("")
    out.append(f"- Description: {description}")
    out.append(f"- Source: {BASE}/faces/codes.xhtml")
    out.append(f"- Pulled: {today}")
    out.append(f"- Sections: {len(sections)}")
    out.append("")
    out.append("> Verbatim text from the California Legislative Information website.")
    out.append("> Citation history and notes are preserved as published.")
    out.append("")

    out.append("## Contents")
    out.append("")
    for code, section, label in sections:
        cite_disp = f"{CODE_DISPLAY.get(code, code)} § {section}"
        anchor = f"sec-{code.lower()}-{section.replace('.', '-')}"
        out.append(f"- [{cite_disp} — {label}](#{anchor})")
    out.append("")

    for code, section, label in sections:
        key = (code, section)
        caption, body, err = fetched.get(key, ("", "", "missing"))
        cite_disp = f"{CODE_DISPLAY.get(code, code)} § {section}"
        anchor = f"sec-{code.lower()}-{section.replace('.', '-')}"
        out.append(f'<a id="{anchor}"></a>')
        out.append(f"## {cite_disp} — {label}")
        out.append("")
        out.append(f"Source: {SECTION_URL.format(code=code, section=section)}")
        out.append("")
        if err:
            out.append(f"> **Fetch failed:** {err}")
            out.append("")
        elif not body:
            out.append("> _(empty extraction)_")
            out.append("")
        else:
            out.append(body)
            out.append("")
    text = "\n".join(out).rstrip() + "\n"
    return re.sub(r"\n{3,}", "\n\n", text)


# ---- Main --------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out",
        default="plugins/ca-court-docs/skills/ca-law-references/references/ca-statutes-debt",
    )
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument(
        "--only",
        nargs="*",
        help="Optional list of output-file stems to limit to (e.g. CCP-SOL CivCode-Rosenthal).",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Print URLs without fetching.",
    )
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    only = set(args.only) if args.only else None

    if args.dry_run:
        for stem, desc, sections in FILES:
            if only and stem not in only:
                continue
            print(f"\n=== {stem} — {desc} ({len(sections)} sections) ===")
            for code, section, label in sections:
                print(f"  {SECTION_URL.format(code=code, section=section)}")
        return 0

    grand_total = 0
    grand_failed = 0

    for stem, description, sections in FILES:
        if only and stem not in only:
            continue
        print(f"\n=== {stem} — {description} ===", flush=True)
        print(f"  {len(sections)} sections", flush=True)

        fetched: dict[tuple[str, str], tuple[str, str, str | None]] = {}
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = {
                ex.submit(fetch_section, code, section): (code, section)
                for code, section, _label in sections
            }
            done = 0
            for fut in as_completed(futs):
                done += 1
                code, section, caption, body, err = fut.result()
                fetched[(code, section)] = (caption, body, err)
                if err:
                    print(
                        f"    [{done}/{len(sections)}] {code} § {section} FAIL: {err}",
                        flush=True,
                    )
                    grand_failed += 1

        md = render_file_md(stem, description, sections, fetched)
        out_path = out_dir / f"{stem}.md"
        out_path.write_text(md, encoding="utf-8")
        print(f"  wrote {out_path} ({len(md):,} bytes)", flush=True)
        grand_total += len(sections)

    print(
        f"\nDone. {grand_total} sections; {grand_failed} fetch errors.",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
