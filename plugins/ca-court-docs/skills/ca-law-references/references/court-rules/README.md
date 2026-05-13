# California Court Rules Corpus

This directory holds verbatim text of the California court
rules most relevant to civil practice, extracted from
authoritative sources.

## Rules covered (when fully populated)

| Rules | File | Source | Update cycle |
|-------|------|--------|--------------|
| California Rules of Court (CRC) — Title 2 (format) | `CRC-Title-2.md` | courts.ca.gov/cms/rules | Annual (Jan 1) |
| California Rules of Court (CRC) — Title 3 (civil) | `CRC-Title-3.md` | courts.ca.gov/cms/rules | Annual (Jan 1) + interim |
| California Rules of Court (CRC) — Title 8 (appellate) | `CRC-Title-8.md` | courts.ca.gov/cms/rules | Annual |
| LASC Local Rules | `LASC-Local-Rules.md` | lacourt.org | Annual + as amended |
| SFSC Local Rules | `SFSC-Local-Rules.md` | sfsuperiorcourt.org | Annual + as amended |
| OCSC Local Rules | `OCSC-Local-Rules.md` | occourts.org | Annual + as amended |
| San Diego Superior Court Local Rules | `SDSC-Local-Rules.md` | sdcourt.ca.gov | Annual + as amended |
| Santa Clara Superior Court Local Rules | `SCSC-Local-Rules.md` | scscourt.org | Annual + as amended |

## About the California Rules of Court (CRC)

The California Rules of Court are promulgated by the Judicial
Council of California under the authority of California
Constitution, article VI, section 6. The Judicial Council
has rulemaking authority over practice and procedure in
California courts. CRC amendments are effective January 1
annually; emergency amendments may be effective at any time.

The CRC is organized in numbered Titles:

- **Title 1** — General provisions and definitions
- **Title 2** — Trial court rules (format, filing, service,
  e-filing, exhibits)
- **Title 3** — Civil rules (case management, law and motion,
  discovery, ADR, complex litigation, coordination)
- **Title 4** — Criminal rules
- **Title 5** — Family and juvenile rules
- **Title 6** — Small claims rules
- **Title 7** — Probate rules
- **Title 8** — Appellate rules (CRC 8.1115 on unpublished
  opinions is critical to California civil practice)
- **Title 9** — Rules on law practice, attorneys, judges
- **Title 10** — Judicial administration rules (includes the
  California Style Manual as Appendix B)

### Most critical CRC provisions for civil practice

**Format (CRC Title 2, Division 1)**:
- Rules 2.100-2.119 — paper size, margins, font, line spacing,
  line numbers, caption requirements. Every filed document
  must comply. See `ca-statewide-format` for the complete
  checklist.

**Case management (CRC Title 3, Division 7)**:
- Rules 3.700-3.740 — case management conference, CMC
  statement (Form CM-110), trial-setting procedure
- Rule 3.714 — civil case cover sheet (Form CM-010) required
  at filing
- Rule 3.722 — CMC at 180 days from filing; parties file
  CMC statement 15 days before

**Complex litigation (CRC Title 3, Division 9)**:
- Rules 3.400-3.403 — complex case designation; assigned to
  a single judge from filing through trial

**Law and motion (CRC Title 3, Division 11)**:
- Rules 3.1100-3.1390 — the core motion rules governing
  notice periods, opposition, reply, oral argument, tentative
  rulings (rule 3.1308), demurrers (rule 3.1320), summary
  judgment (rule 3.1350)

**Discovery (CRC Title 3, Division 19)**:
- Rules 3.1000-3.1020 — discovery motions; IDC (Informal
  Discovery Conference) requirements

**ADR (CRC Title 3, Divisions 8-9)**:
- Rules 3.850-3.898 — court-connected ADR; mediation
  confidentiality (Cal. Evid. Code §§ 1115-1128)

**Appellate practice (CRC Title 8)**:
- Rule 8.1115 — unpublished opinion prohibition
- Rule 8.204 — appellate brief format

## About California local rules

Each of California's 58 Superior Courts adopts local rules
under CRC rule 3.20, which limits local rules to matters
not covered by the CRC. When a local rule conflicts with
the CRC or a statute, the CRC/statute controls.

Local rules are the most variable element of California
civil practice — what applies in LASC may differ significantly
from SFSC, OCSC, or any other court. Always pull the current
local rules from the court's website before drafting a motion.

### Los Angeles Superior Court (LASC)

LASC is the nation's largest trial court, with 31 courthouses
and dozens of civil departments. LASC local rules are
published at:

**https://www.lacourt.org/division/civil/CI0078.aspx**

Key provisions:
- Department-specific courtroom rules (posted on each
  department's page at lacourt.org/newsmedia/courtrooms/)
- Tentative ruling system: https://www.lacourt.org/tentativeRulingNet/
- eFiling mandatory for most civil filings
- Ex parte practice in the assigned department; notice by
  10:00 a.m. the day before

### San Francisco Superior Court (SFSC)

SFSC local rules are published at:

**https://www.sfsuperiorcourt.org/divisions/civil/local-rules**

Key provisions:
- Law and motion in Departments 501-502
- Online reservation system for hearing dates
- Tentative rulings posted by 3:00 p.m. day before hearing
- Fast Track civil case management

### Orange County Superior Court (OCSC)

OCSC local rules are published at:

**https://www.occourts.org/general-public/local-rules/**

Key provisions:
- Informal Discovery Conference (IDC) required before
  discovery motions in most departments
- Tentative rulings posted by 1:30 p.m. day before
- Complex litigation assigned to dedicated departments

## Citation tables

When citing in a filing, use these forms (per the California
Style Manual):

| Source | Cite form |
|--------|-----------|
| CRC | `Cal. Rules of Court, rule 3.1308` |
| LASC Local Rules | `LASC Local Rules, rule 3.3` |
| SFSC Local Rules | `SFSC Local Rules, rule 10.6` |
| OCSC Local Rules | `OCSC Local Rules, rule 354` |

After first full citation, abbreviate: `Rule 3.1308` or
`LASC rule 3.3`.

## How to re-pull

A future `scripts/pull_ca_court_rules.py` script will handle
bulk extraction. To run (once created):

```bash
python3 scripts/pull_ca_court_rules.py \
  --workers 8 \
  --manifest plugins/ca-court-docs/skills/ca-law-references/references/court-rules/_manifest.json
```

The script should:
1. Fetch the CRC consolidated PDF from courts.ca.gov
2. Extract text using `pdfplumber`
3. Segment by Title and Rule number
4. Write individual markdown files
5. For local rules, fetch from each court's website and
   convert PDF to markdown

For ad hoc extraction without the script, use WebFetch against
the canonical URLs in `../online-sources.md`.

## Status

This corpus is **empty in the initial PR** — only this README.
The first pull-script run will populate the verbatim rule
files. The quarterly agent routine (once configured for
California) will keep it fresh.

## Cross-references

- `../online-sources.md` — canonical URLs
- `../legal-data-apis.md` — programmatic access
- `../civil-rules.md` — agent-facing summary of CCP
- `../../ca-statewide-format/` — CRC 2.100-2.119 format
  checklist
