# claude-legal

A Claude Code / Cowork marketplace of plugins for preparing U.S. court documents. The first plugin covers Washington State courts; the structure leaves clean slots for additional states.

## What's in here

One plugin today:

- **wa-court-docs** — Drafts and formats pleadings, declarations, motions, notes for motion docket, and proposed orders for Washington courts. Applies GR 14 formatting, covers King County District Court (all three divisions — East/Redmond, South/Burien, West/Seattle), and supports pro se workflows. Architected as matter-neutral civil-procedure skills plus subject-matter bundles (starting with `wa-consumer-debt` for FDCPA / Reg F / WA CPA debt-defense).

The marketplace is organized one plugin per state; more state plugins can be added under `plugins/` as it grows.

## Install

Add this marketplace to Claude Code or Cowork, then install `wa-court-docs`:

```
/plugin marketplace add https://github.com/codearranger/claude-legal
/plugin install wa-court-docs@claude-legal
```

## Repo layout

```
claude-legal/
├── .claude-plugin/
│   └── marketplace.json              # Marketplace manifest
├── plugins/
│   └── wa-court-docs/
│       ├── .claude-plugin/plugin.json
│       ├── README.md
│       ├── LICENSE
│       ├── skills/                   # All workflows are skills, auto-invoked by description
│       │   ├── wa-statewide-format/  # GR 14 + statewide drafting conventions
│       │   ├── wa-kcdc/              # King County District Court specifics
│       │   ├── wa-pro-se/            # Parker framework, service, pro se drafting
│       │   ├── wa-law-references/    # Civil rules, evidence rules, citation format, fees, local rules
│       │   ├── wa-discovery/         # RFPs, interrogatories, RFAs, meet and confer, motion to compel
│       │   ├── wa-hearings/          # Oral argument, Zoom, courtroom etiquette, hearing day
│       │   ├── wa-post-judgment/     # CR 60, garnishment, exemptions, supplemental proceedings
│       │   ├── wa-first-30-days/     # Answer, defenses, counterclaims after service
│       │   ├── wa-fact-check/        # Citation verification, quote-to-source checking
│       │   ├── wa-deadlines/         # CR/CRLJ 6 deadline computation with RCW 1.16.050 holidays
│       │   ├── wa-draft-motion/      # Scaffold motion + supporting memorandum
│       │   ├── wa-draft-declaration/ # Scaffold declaration with numbered paragraphs + exhibits
│       │   ├── wa-draft-note/        # Scaffold Note for Motion Docket
│       │   ├── wa-draft-order/       # Scaffold proposed order for judge signature
│       │   ├── wa-quality-check/     # Format + content QC before filing
│       │   ├── wa-schedule-hearing/  # KCDC CivilMGT date-request email
│       │   ├── wa-file-packet/       # Assemble and preflight the full filing packet
│       │   ├── wa-submit-order/      # Post-hearing: signed-order preparation and transmittal
│       │   └── wa-consumer-debt/     # Subject-matter bundle: FDCPA, Reg F, RCW 19.16, CPA, chain of title
│       ├── scripts/
│       │   ├── format-check.py       # GR 14 compliance checker (paper/margins/fonts/color/footer)
│       │   └── case-calendar.py      # Deadline arithmetic helper for wa-deadlines
│       └── evals/                    # Drafting, formatting, procedural, subject-matter, and integration evals
├── LICENSE
└── README.md
```

## Disclaimer

Not legal advice. This plugin provides drafting assistance only. Review all
generated content and confirm compliance with current court rules and local
practice before filing.

## License

MIT. See [LICENSE](LICENSE).
