# claude-legal

A Claude Code / Cowork marketplace of plugins for preparing U.S. court documents, organized one plugin per state.

## What's in here

Two plugins today:

- **`wa-court-docs`** — Washington State. Drafts and formats pleadings, declarations, motions, notes for motion docket, and proposed orders for Washington courts. Applies GR 14 formatting; covers King County District Court (all three divisions — East/Redmond, South/Burien, West/Seattle), King County Superior Court (Seattle / Kent — MRJC), and the most-populous counties' roll-up (Pierce, Snohomish, Spokane, Clark, Thurston, Kitsap, Yakima, Whatcom, Benton). Supports pro se workflows. The `wa-consumer-debt` subject-matter bundle covers FDCPA / Reg F / WA CPA debt-defense.
- **`or-court-docs`** — Oregon. Drafts and formats pleadings, declarations, motions, notices of hearing, and proposed orders for Oregon circuit courts. Applies UTCR 2.010 formatting; covers Multnomah County Circuit Court (Portland / Central Courthouse), Washington County Circuit Court (Hillsboro), and the most-populous counties' roll-up (Clackamas, Lane, Marion, Jackson, Deschutes, Linn, Benton, Yamhill, Polk, Douglas). Supports pro se workflows. The `or-consumer-debt` subject-matter bundle covers FDCPA / Reg F / Oregon UTPA (ORS 646.605) / ORS 697 Collection Agency Registration / chain-of-title doctrine.

Both plugins are architected the same way: matter-neutral civil-procedure skills (statewide format, civil rules, evidence rules, fees and costs, local rules, citation format, online sources, discovery, first-30-days response, hearings, filing packets, post-judgment, fact-checking, deadlines) plus subject-matter bundles that plug into the procedural skills (starting with consumer-debt defense in each state).

The marketplace is organized one plugin per state; more state plugins can be added under `plugins/` as it grows.

## Install

Add this marketplace to Claude Code or Cowork, then install the plugins:

```
/plugin marketplace add https://github.com/codearranger/claude-legal
/plugin install wa-court-docs@claude-legal
/plugin install or-court-docs@claude-legal
```

## Repo layout

```
claude-legal/
├── .claude-plugin/
│   └── marketplace.json              # Marketplace manifest
├── plugins/
│   ├── wa-court-docs/                # Washington State plugin (21 skills)
│   │   ├── .claude-plugin/plugin.json
│   │   ├── skills/                   # GR 14, KCDC, KCSC, county roll-up, etc.
│   │   ├── scripts/                  # format-check.py (GR 14), case-calendar.py (CR 6)
│   │   └── evals/
│   └── or-court-docs/                # Oregon plugin (21 skills)
│       ├── .claude-plugin/plugin.json
│       ├── skills/                   # UTCR 2.010, or-multcc, or-wccc, or-county-courts, or-consumer-debt, etc.
│       │   ├── or-statewide-format/  # UTCR 2.010 + statewide drafting
│       │   ├── or-multcc/            # Multnomah Circuit Court (Portland)
│       │   ├── or-wccc/              # Washington Co Circuit Court (Hillsboro)
│       │   ├── or-county-courts/     # Clackamas, Lane, Marion, Jackson, Deschutes, etc.
│       │   ├── or-pro-se/            # Parker framework adapted for Oregon
│       │   ├── or-law-references/    # ORCP, OEC, ORS, citation format, local SLRs
│       │   ├── or-discovery/         # RFPs, RFAs, depositions, ORCP 46 (no interrogatories!)
│       │   ├── or-hearings/          # Oral argument, WebEx, etiquette
│       │   ├── or-post-judgment/     # ORCP 71, ORS 18.600+ garnishment, exemptions
│       │   ├── or-first-30-days/     # Answer, ORCP 21 motions, counterclaims
│       │   ├── or-fact-check/        # Citation verification (Oregon Style Manual)
│       │   ├── or-deadlines/         # ORCP 10 + ORS 187.010 holidays
│       │   ├── or-draft-motion/      # Scaffold motion + memorandum
│       │   ├── or-draft-declaration/ # Scaffold declaration with exhibits
│       │   ├── or-draft-note/        # Scaffold Notice of Hearing
│       │   ├── or-draft-order/       # Scaffold proposed order
│       │   ├── or-quality-check/     # UTCR 2.010 format + content QC
│       │   ├── or-schedule-hearing/  # JA / Civil Division date-request email
│       │   ├── or-file-packet/       # Assemble packet for File and Serve
│       │   ├── or-submit-order/      # Post-hearing signed-order transmittal
│       │   └── or-consumer-debt/     # FDCPA, Reg F, ORS 697, UTPA, chain of title
│       ├── scripts/
│       │   ├── format-check.py       # UTCR 2.010 compliance checker
│       │   └── case-calendar.py      # ORCP 10 deadline arithmetic + ORS 187 holidays
│       └── evals/                    # Drafting, formatting, procedural, subject-matter, integration evals
├── scripts/                          # Shared marketplace scripts
│   ├── lint-skills.py                # Frontmatter + name/dir-match linter
│   ├── hooks/pre-commit              # Symlink target for git hook
│   ├── pull_court_rules.py           # courts.wa.gov → wa court rules
│   ├── pull_federal_debt_laws.py     # Federal law (shared content)
│   ├── pull_ucc.py                   # Model UCC (shared content)
│   └── pull_wa_rcw.py                # app.leg.wa.gov → wa RCW chapters
├── LICENSE
└── README.md
```

## Key differences across states

The WA and OR plugins are intentionally parallel, but they encode the genuine procedural differences between the jurisdictions. A few worth highlighting:

| Concept | Washington | Oregon |
|---------|------------|--------|
| Format rule | GR 14 | UTCR 2.010 |
| Civil rules | CR (superior) + CRLJ (district) | ORCP (unified — no district court) |
| Evidence rules | ER (court rule) | OEC (statutory at ORS Ch. 40) |
| Failure to state | CR 12(b)(6) / CRLJ 12(b)(6) | ORCP 21 A(8) |
| Discovery — interrogatories | CR 33 (available) | **Not available** without court order |
| Discovery — RFPs | CR 34 | ORCP 43 |
| Discovery — RFAs | CR 36 | ORCP 45 |
| Motion to compel | CR 37 / CRLJ 37 | ORCP 46 A |
| Summary judgment | CR 56 | ORCP 47 |
| Vacate judgment | CR 60 | ORCP 71 |
| Time computation | CR 6 | ORCP 10 |
| Statute citation | RCW 19.16.260 (no §) | ORS 697.015 (no §) |
| Case citation | Wn.2d, Wn. App., P.3d (periods) | Or, Or App, P3d (no periods) |
| Parties separator | "vs." | "v." |
| Exhibit labels | Letters (A, B, C) | Numbers (1, 2, 3) |
| Consumer-protection statute | RCW 19.86 (CPA) | ORS 646.605 (UTPA) |
| Collection-agency statute | RCW 19.16 | ORS 697 |
| eFiling system | KCDC/KCSC portals + statewide eFile | OJD File and Serve (Tyler; statewide) |

These differences are captured throughout the skill bodies and reference files — porting a WA template to Oregon (or vice versa) requires more than search-and-replace.

## Disclaimer

Not legal advice. These plugins provide drafting assistance only. Review all generated content and confirm compliance with current court rules and local practice before filing.

## License

MIT. See [LICENSE](LICENSE).
