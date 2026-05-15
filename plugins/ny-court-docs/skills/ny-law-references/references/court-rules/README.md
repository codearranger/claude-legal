# court-rules Corpus — New York

Verbatim text of New York court-rule canonical sources, scoped to the
material most relevant to civil practice.

## Sources

- **22 NYCRR Parts 202 / 208 / 210 / 212 / 214** — Uniform Civil
  Rules for the Supreme + County Courts, the NYC Civil Court, the
  upstate City Courts, the Long Island District Courts, and the
  Court of Claims, respectively. Published by the New York Unified
  Court System at `www.nycourts.gov/rules/trialcourts/`.
- **22 NYCRR § 202.70** — Commercial Division Rules, including the
  county-by-county monetary threshold table.
- **22 NYCRR Part 130** — Costs and sanctions for frivolous conduct.
- **22 NYCRR Part 1200** — Rules of Professional Conduct (adopted by
  the four Appellate Divisions).
- **NY Law Reports Style Manual ("Tanbook")** — citation manual
  published by the Reporter of Decisions; pointer-stub.
- **NYC Civil Court Directives and Procedures Manual** — local-rule
  overlay for the Consumer Credit Part, Housing Part, default-
  judgment scrutiny; pointer-stub.
- **Nassau / Suffolk District Court local rules** — pointer-stubs for
  the two Long Island District Court local rule sets.

## How to refresh

```bash
python3 scripts/pull_ny_court_rules.py --workers 4 \
    --out plugins/ny-court-docs/skills/ny-law-references/references/court-rules
```

The puller:

1. **Tries the canonical UCS URLs first.** When the upstream returns
   substantive HTML, the puller writes verbatim Markdown.
2. **Falls back to pointer stubs** when the upstream returns a
   Cloudflare managed-challenge response (HTTP 403 + "Just a
   moment..." interstitial). The stub records the canonical URL,
   the scope of the rule set, and how to retrieve the verbatim text.
3. **Never regresses substantive content to a stub.** If a previous
   refresh wrote real Markdown and the current refresh would only
   produce a stub, the existing file is kept in place.

## Why some files are stubs

The `www.nycourts.gov` publication host sits behind Cloudflare. Many
IP ranges — including most developer workstations — are challenged
with a JavaScript-required interstitial. GitHub Actions runners are
sometimes (but not always) waved through. When stubs appear in this
corpus, the **canonical URL recorded in the stub remains valid in a
browser**; the stub is just a documentation gap until the puller
clears the upstream gate.

## File index

| File | Rule set | Scope |
|---|---|---|
| `202.md` | 22 NYCRR Part 202 | Uniform Civil Rules — Supreme + County Court |
| `202.70.md` | 22 NYCRR § 202.70 | Commercial Division Rules |
| `208.md` | 22 NYCRR Part 208 | NYC Civil Court |
| `210.md` | 22 NYCRR Part 210 | Upstate City Courts |
| `212.md` | 22 NYCRR Part 212 | Nassau / Suffolk District Courts |
| `214.md` | 22 NYCRR Part 214 | Court of Claims |
| `130.md` | 22 NYCRR Part 130 | Costs and sanctions |
| `Part-1200-Conduct.md` | 22 NYCRR Part 1200 | Rules of Professional Conduct |
| `Tanbook.md` | NY Law Reports Style Manual | Citation format |
| `NYC-CivilCourt-LR.md` | NYC Civil Court Directives | Civil Court local overlay |
| `Nassau-DC-LR.md` | Nassau District Court rules | Long Island District Court |
| `Suffolk-DC-LR.md` | Suffolk District Court rules | Long Island District Court |

> **NOT LEGAL ADVICE.** This corpus is a drafting aid; verify against
> the current canonical text before filing.
