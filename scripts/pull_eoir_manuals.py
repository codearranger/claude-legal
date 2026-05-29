#!/usr/bin/env python3
"""Pull the EOIR practice manuals — the procedural "court rules" of the
immigration courts and the Board of Immigration Appeals.

Immigration-court practice has two layers of procedural authority:

  1. **Binding regulations** — 8 CFR Part 1003 (EOIR organization, the BIA,
     and immigration-judge proceedings), Part 1240 (removal proceedings), and
     Part 1208 (asylum/withholding before EOIR). These are LAW and are already
     mirrored verbatim in ../immigration-regulations/ (8CFR-1003-eoir-bia.md,
     8CFR-1240-removal-eoir.md, 8CFR-1208-asylum-eoir.md). Cite THESE for
     anything jurisdictional or substantive.

  2. **Practice manuals** — the **Immigration Court Practice Manual (ICPM)** and
     the **Board of Immigration Appeals Practice Manual (BIAPM)**, published by
     EOIR at justice.gov. These are procedural guidance (filing format, page
     limits, deadlines, e-filing via ECAS), not regulations, but courts expect
     compliance. This puller targets these two manuals.

## Why pointer stubs (for now)

EOIR moved the manuals to a **JavaScript-rendered** web manual at
`justice.gov/eoir/reference-materials/ic/chapter-N` (ICPM) and `.../bia/chapter-N`
(BIAPM). The substantive chapter text is **not present in the static HTML** (the
page ships only chrome; the body is hydrated client-side), and justice.gov's
Akamai edge **403s most chapter URLs** from a plain client even when paced. So a
stdlib fetch cannot mirror verbatim text from here. This puller therefore writes
**well-formed pointer stubs** carrying the canonical URLs + chapter enumeration +
scope, exactly as scripts/pull_ny_court_rules.py and scripts/pull_co_court_rules.py
do for JS-rendered / gated official sources. The `_file_is_stub` guard means a
later verbatim run (headless browser or an un-gated egress) will NOT clobber
content already committed.

For the binding rules, no stub is needed — they are in ../immigration-regulations/.

Output: plugins/claude-legal-immigration-laws/references/court-rules/
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

EOIR_BASE = "https://www.justice.gov/eoir/reference-materials"

# Row: (out_file, title, url_slug, chapter_url_tmpl, chapters, scope).
#   chapters — list of (number, title) for the canonical chapter enumeration.
ManualRow = tuple[str, str, str, str, list[tuple[str, str]], str]

ICPM_CHAPTERS = [
    ("1", "The Immigration Court"),
    ("2", "Appearances Before the Immigration Court"),
    ("3", "Filing with the Immigration Court"),
    ("4", "Hearings Before Immigration Judges"),
    ("5", "Motions Before the Immigration Court"),
    ("6", "Appeals of Immigration Judge Decisions"),
    ("7", "Other Proceedings Before Immigration Judges"),
    ("8", "Stays"),
    ("9", "Detention and Bond"),
    ("10", "Discipline of Practitioners"),
    ("11", "Forms"),
    ("12", "Freedom of Information Act (FOIA)"),
    ("13", "Other Information"),
]

BIAPM_CHAPTERS = [
    ("1", "The Board of Immigration Appeals"),
    ("2", "Appearances Before the Board"),
    ("3", "Filing with the Board"),
    ("4", "Appeals of Immigration Judge Decisions"),
    ("5", "Motions Before the Board"),
    ("6", "Stays and Expedite Requests"),
    ("7", "Other Information"),
    ("8", "Discipline of Practitioners"),
]

MANUALS: list[ManualRow] = [
    ("Immigration-Court-Practice-Manual",
     "Immigration Court Practice Manual (ICPM)",
     "ic",
     EOIR_BASE + "/ic/chapter-{n}",
     ICPM_CHAPTERS,
     "EOIR's procedural manual for practice before the immigration courts: "
     "appearances (Form EOIR-28), filing requirements and format, the master- "
     "and individual-calendar hearing structure, motions practice, deadlines, "
     "and e-filing through ECAS. Procedural guidance — for binding rules cite "
     "8 CFR Part 1003 / 1240 / 1208 in ../immigration-regulations/."),
    ("BIA-Practice-Manual",
     "Board of Immigration Appeals Practice Manual (BIAPM)",
     "bia",
     EOIR_BASE + "/bia/chapter-{n}",
     BIAPM_CHAPTERS,
     "EOIR's procedural manual for appeals to the Board of Immigration Appeals: "
     "the Notice of Appeal (Form EOIR-26), the briefing schedule, page limits, "
     "motions to reopen/reconsider before the Board, and stays. Procedural "
     "guidance — for binding rules cite 8 CFR § 1003.1–§ 1003.8 in "
     "../immigration-regulations/8CFR-1003-eoir-bia.md."),
]

STUB_MARKER = "<!-- claude-legal:eoir-manual-pointer-stub -->"


def _file_is_stub(path: Path) -> bool:
    if not path.exists():
        return True
    try:
        return STUB_MARKER in path.read_text(encoding="utf-8")
    except OSError:
        return True


def http_status(url: str, *, timeout: float = 25.0) -> tuple[int | str, bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT,
                                               "Accept": "text/html"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception:  # noqa: BLE001
        return "ERR", b""


# Heuristic: a verbatim chapter would carry section markers like "1.2" plus
# substantive prose in the STATIC HTML. The current JS-rendered pages do not,
# so this returns False today — but keeps the door open for a headless future.
def _looks_verbatim(html: bytes, chapter_no: str) -> bool:
    if len(html) < 8000:
        return False
    text = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", html.decode("utf-8", "replace"))
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return f"{chapter_no}.1" in text and "jurisdiction" in text.lower()


def make_stub(title: str, slug: str, chapter_tmpl: str,
              chapters: list[tuple[str, str]], scope: str, probe: str) -> str:
    today = date.today().isoformat()
    rows = "\n".join(
        f"| {n} | {ct} | {chapter_tmpl.format(n=n)} |" for n, ct in chapters
    )
    return (
        f"# {title}\n\n"
        f"{STUB_MARKER}\n\n"
        f"- Publisher: Executive Office for Immigration Review (EOIR), U.S. Department of Justice\n"
        f"- Canonical landing: {EOIR_BASE}/{slug}\n"
        f"- Status: **pointer stub** — verbatim text not mirrored\n"
        f"- Pulled: {today}\n\n"
        f"> **Why a stub?** EOIR serves this manual as a **JavaScript-rendered** "
        f"web manual (the chapter body is hydrated client-side and is absent from "
        f"the static HTML), and justice.gov's Akamai edge **403s** most chapter "
        f"URLs from a plain client. So `scripts/pull_eoir_manuals.py` cannot mirror "
        f"verbatim text from here ({probe}). Read the authoritative manual at the "
        f"chapter URLs below. A future headless or un-gated run will replace this "
        f"stub; the `_file_is_stub` guard protects committed verbatim content.\n\n"
        f"## Chapters\n\n"
        f"| # | Chapter | URL |\n|---|---|---|\n{rows}\n\n"
        f"## Authority note — manual vs. binding rule\n\n"
        f"This manual is **procedural guidance**, not law. The **binding** rules for "
        f"immigration-court and BIA practice are the regulations at **8 CFR Part 1003** "
        f"(EOIR / immigration judges / the Board), **Part 1240** (removal proceedings), "
        f"and **Part 1208** (asylum before EOIR) — mirrored verbatim in "
        f"[`../immigration-regulations/`](../immigration-regulations/) "
        f"(`8CFR-1003-eoir-bia.md`, `8CFR-1240-removal-eoir.md`, `8CFR-1208-asylum-eoir.md`). "
        f"Always cite the regulation for anything jurisdictional or substantive and use the "
        f"manual only for filing format, page limits, and procedural mechanics.\n\n"
        f"## Scope\n\n{scope}\n"
    )


def make_verbatim(title: str, slug: str, sections: list[tuple[str, str, str]]) -> str:
    today = date.today().isoformat()
    out = [
        f"# {title}", "",
        f"- Publisher: Executive Office for Immigration Review (EOIR), U.S. Department of Justice",
        f"- Canonical landing: {EOIR_BASE}/{slug}",
        f"- Pulled: {today}", "",
        "> Verbatim text reduced from the EOIR web manual. Procedural guidance, "
        "not binding law — pair with 8 CFR Part 1003 / 1240 / 1208.", "",
    ]
    for n, ct, body in sections:
        out += [f"## Chapter {n} — {ct}", "", f"*Source: {EOIR_BASE}/{slug}/chapter-{n}*", "", body, "", "---", ""]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out).rstrip() + "\n")


def html_to_md(html: bytes) -> str:
    text = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", html.decode("utf-8", "replace"))
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return re.sub(r"\n{3,}", "\n\n", re.sub(r"[ \t]+", " ", text)).strip()


def write_readme(out_dir: Path) -> None:
    today = date.today().isoformat()
    (out_dir / "README.md").write_text(
        "# Immigration court rules — EOIR\n\n"
        "Procedural authority for practice before the **immigration courts** and the "
        "**Board of Immigration Appeals (BIA)** comes in two layers:\n\n"
        "## 1. Binding regulations (LAW) — mirrored verbatim elsewhere\n\n"
        "The enforceable rules live in **8 CFR**, already mirrored verbatim under "
        "[`../immigration-regulations/`](../immigration-regulations/):\n\n"
        "- **Part 1003** — EOIR; the Board of Immigration Appeals; immigration-judge "
        "proceedings; motions before the Board and the IJ (`8CFR-1003-eoir-bia.md`)\n"
        "- **Part 1240** — removal proceedings before EOIR (`8CFR-1240-removal-eoir.md`)\n"
        "- **Part 1208** — asylum and withholding before EOIR (`8CFR-1208-asylum-eoir.md`)\n\n"
        "Cite these for anything jurisdictional or substantive.\n\n"
        "## 2. Practice manuals (procedural guidance) — pointer stubs here\n\n"
        "EOIR publishes two procedural manuals at justice.gov. They are guidance, not "
        "law, but courts expect compliance with their filing-format and deadline rules:\n\n"
        "| File | Manual | Canonical |\n|---|---|---|\n"
        "| [Immigration-Court-Practice-Manual.md](Immigration-Court-Practice-Manual.md) | ICPM | "
        f"<{EOIR_BASE}/ic> |\n"
        "| [BIA-Practice-Manual.md](BIA-Practice-Manual.md) | BIAPM | "
        f"<{EOIR_BASE}/bia> |\n\n"
        "These ship as **pointer stubs** because EOIR renders the manuals client-side "
        "(JavaScript) and Akamai-gates the chapter URLs, so verbatim text can't be "
        "mirrored from a stdlib client. Each stub carries the canonical chapter URLs "
        "and a cross-reference to the binding 8 CFR rules. Refresh with "
        "`scripts/pull_eoir_manuals.py`; the `_file_is_stub` guard preserves any "
        "verbatim content a future headless/un-gated run commits.\n\n"
        f"- Pulled by: `scripts/pull_eoir_manuals.py`\n- Last updated: {today}\n\n"
        "> **NOT LEGAL ADVICE.** Verify the current manual text and the controlling "
        "8 CFR provision before filing.\n",
        encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out",
        default="plugins/claude-legal-immigration-laws/references/court-rules",
    )
    ap.add_argument("--stubs-only", action="store_true",
                    help="Skip the network probe and (re)write pointer stubs.")
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    wrote_verbatim = wrote_stub = preserved = 0
    for (out_file, title, slug, tmpl, chapters, scope) in MANUALS:
        path = out_dir / f"{out_file}.md"
        sections: list[tuple[str, str, str]] = []
        probe = "stubs-only mode" if args.stubs_only else ""

        if not args.stubs_only:
            for (n, ct) in chapters:
                status, html = http_status(tmpl.format(n=n))
                if isinstance(status, int) and status == 200 and _looks_verbatim(html, n):
                    sections.append((n, ct, html_to_md(html)))
                elif not probe:
                    probe = f"chapter-{n} returned {status}"

        if sections:
            path.write_text(make_verbatim(title, slug, sections), encoding="utf-8")
            wrote_verbatim += 1
            print(f"  wrote VERBATIM {path} ({len(sections)}/{len(chapters)} chapters)", flush=True)
            continue

        if not _file_is_stub(path):
            preserved += 1
            print(f"  preserved existing verbatim {path}", flush=True)
            continue
        path.write_text(make_stub(title, slug, tmpl, chapters, scope,
                                  probe or "fetch blocked"), encoding="utf-8")
        wrote_stub += 1
        print(f"  wrote STUB {path}", flush=True)

    write_readme(out_dir)
    mode = "verbatim" if wrote_stub == 0 and wrote_verbatim else (
        "stub" if wrote_verbatim == 0 else "mixed")
    manifest = {
        "version": "0.1.0",
        "last_pulled": date.today().isoformat(),
        "source": EOIR_BASE,
        "mode": mode,
        "notes": (
            "Pulled by scripts/pull_eoir_manuals.py. The EOIR practice manuals "
            "(ICPM + BIA Practice Manual) are JS-rendered and Akamai-gated, so they "
            "ship as pointer stubs with canonical URLs + chapter enumeration; the "
            "binding rules are 8 CFR Part 1003/1240/1208 in ../immigration-regulations/. "
            "The _file_is_stub guard preserves any verbatim content a future "
            "headless/un-gated run commits."
        ),
    }
    (out_dir / "_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Done. verbatim={wrote_verbatim} stub={wrote_stub} "
          f"preserved={preserved} mode={mode}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
