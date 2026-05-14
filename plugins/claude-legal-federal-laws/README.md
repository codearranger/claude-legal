# claude-legal-federal-laws

Shared reference corpus for the `claude-legal` marketplace.

## What's in here

- `references/federal-debt-laws/` — verbatim text of U.S. consumer-finance and debt-collection statutes (FDCPA, FCRA, TILA, ECOA) and the CFPB regulations that implement them (Reg B, Reg F, Reg V, Reg Z). Pulled from `uscode.house.gov` USLM XML and the eCFR Versioner API by [`scripts/pull_federal_debt_laws.py`](../../scripts/pull_federal_debt_laws.py).
- `references/ucc-model/` — model Uniform Commercial Code, Articles 1 (General Provisions), 2 (Sales), 3 (Negotiable Instruments), and 9 (Secured Transactions). The *model* text as drafted by ALI/ULC; pulled from Cornell Legal Information Institute (`law.cornell.edu/ucc`) by [`scripts/pull_ucc.py`](../../scripts/pull_ucc.py). State-court matters should cite the enacting state code (e.g., RCW Title 62A for Washington), not the model text — the model is included here for interpreting uniform language across states.

## Why it's a plugin

This is a **data-only plugin** — no skills, no slash commands. It exists so the federal and model-UCC corpora live in one canonical place rather than being copy-pasted into every state plugin (`wa-court-docs`, `or-court-docs`, `ca-court-docs`, `co-court-docs`).

State plugins declare this plugin in their `plugin.json` `dependencies` array. When a user runs `/plugin install <state>-court-docs@claude-legal`, the Claude Code marketplace runtime auto-installs this plugin alongside, dereferences the symlinks each state plugin uses to point into this directory (per the Claude Code plugin spec, symlinks within a marketplace are followed and the target content is copied into the install cache), and the federal/UCC files end up locally available under each state plugin's `references/` tree at runtime.

## Refresh

The quarterly `refresh-references` GitHub Action runs `pull_federal_debt_laws.py` and `pull_ucc.py` against the paths in this plugin, then opens a PR. Federal/UCC content is now updated once per quarter instead of once per state.

## Not legal advice

The text is verbatim from official sources and is provided as a drafting aid. Verify against the current statutes and regulations before relying on any citation in a filing.
