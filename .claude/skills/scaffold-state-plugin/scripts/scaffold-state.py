#!/usr/bin/env python3
"""
scaffold-state.py — Scaffold a new state plugin for claude-legal.

Generates the directory tree + lint-clean stub SKILL.md files +
plugin.json + scripts (copied from or-court-docs with parameters
substituted) + eval directories + reference-corpus READMEs/manifests.
After the script runs, the agent (or a human) authors substantive
content into each stub.

The script does NOT author substantive law. That's the next step.
This script handles the mechanical scaffolding only.

Usage:
    scaffold-state.py --state <abbr> --name <full> \\
        --primary-court "<slug>:<display>" \\
        [--secondary-court "<slug>:<display>"] \\
        [--format-rule "<rule code>"] \\
        [--civil-rules "<code>"] \\
        [--evidence "<code>"] \\
        [--statute "<code>"] \\
        [--style-manual "<name>"] \\
        [--dry-run]

Example:
    scaffold-state.py --state ca --name California \\
        --primary-court "lasc:Los Angeles Superior Court" \\
        --secondary-court "sfsc:San Francisco Superior Court" \\
        --format-rule "California Rules of Court 2.100-2.119" \\
        --civil-rules CCP \\
        --evidence CEC \\
        --statute "Cal. Civ. Code" \\
        --style-manual "California Style Manual"

Exit codes:
    0  success (all files created)
    1  validation error in arguments
    2  plugin already exists (use --force to overwrite)
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


# ---- Skill names and roles ---------------------------------------

SKILL_ROLES = [
    "statewide-format",
    "{primary_court}",
    "{secondary_court}",
    "county-courts",
    "pro-se",
    "law-references",
    "discovery",
    "hearings",
    "post-judgment",
    "first-30-days",
    "fact-check",
    "deadlines",
    "draft-motion",
    "draft-declaration",
    "draft-note",
    "draft-order",
    "quality-check",
    "schedule-hearing",
    "file-packet",
    "submit-order",
    "family-court",   # baseline venue: family court
    "consumer-debt",  # baseline subject bundle: consumer-debt defense
    "family-law",     # baseline subject bundle: family-law substance
]


@dataclass
class StateConfig:
    """All the metadata needed to scaffold a state plugin."""

    abbr: str  # "ca"
    name: str  # "California"
    primary_court_slug: str  # "lasc"
    primary_court_display: str  # "Los Angeles Superior Court"
    secondary_court_slug: str  # "sfsc"
    secondary_court_display: str  # "San Francisco Superior Court"
    format_rule: str  # "California Rules of Court 2.100-2.119"
    civil_rules: str  # "CCP"
    evidence: str  # "CEC"
    statute: str  # "Cal. Civ. Code"
    style_manual: str  # "California Style Manual"


# ---- Category-specific disclaimer blocks ------------------------
#
# Every scaffolded SKILL.md ships with a category-appropriate
# "NOT LEGAL ADVICE" blockquote. The text is chosen by skill role:
# drafting scaffolders explicitly identify the user as decision-
# maker; declaration scaffolders identify the user as declarant;
# order scaffolders flag that only a judge signs; venue skills
# defer to current local rules; pro-se skills add the consult-an-
# attorney prompt; subject-matter bundles flag fact-specificity.
# Authors expanding a stub MUST preserve the disclaimer block.

DRAFTING_DISCLAIMER = (
    "> **NOT LEGAL ADVICE.** This skill scaffolds a court document\n"
    "> as a drafting aid. The user — not the skill — chooses the\n"
    "> motion type, theory of relief, and strategy. Verify every\n"
    "> rule, deadline, and citation against current law before\n"
    "> filing. Pair with substantive review by counsel where stakes\n"
    "> warrant."
)

DRAFTING_DECLARATION_DISCLAIMER = (
    "> **NOT LEGAL ADVICE.** This skill scaffolds a court document\n"
    "> as a drafting aid. The user — not the skill — is the\n"
    "> declarant, chooses what facts to swear to, and signs the\n"
    "> declaration. Verify every rule, deadline, and citation\n"
    "> against current law before filing. Pair with substantive\n"
    "> review by counsel where stakes warrant."
)

DRAFTING_ORDER_DISCLAIMER = (
    "> **NOT LEGAL ADVICE.** This skill scaffolds a court document\n"
    "> as a drafting aid. The user — not the skill — chooses the\n"
    "> findings, the relief, and the form of the order. Only a\n"
    "> judge signs an order; this skill prepares the proposed form\n"
    "> for the judge's consideration. Verify every rule, deadline,\n"
    "> and citation against current law before filing. Pair with\n"
    "> substantive review by counsel where stakes warrant."
)

VENUE_DISCLAIMER = (
    "> **NOT LEGAL ADVICE.** These notes describe the venue's\n"
    "> procedural mechanics as a drafting aid, not legal advice.\n"
    "> Local rules and judge-specific practices change; verify\n"
    "> with the clerk and the current local rules before relying\n"
    "> on anything here."
)

FORMAT_QC_DISCLAIMER = (
    "> **NOT LEGAL ADVICE.** Formatting and quality checks verify\n"
    "> the surface — they don't tell the user whether the\n"
    "> underlying legal position is sound. Verify current rules\n"
    "> before filing; pair with substantive review by counsel\n"
    "> where stakes warrant."
)

WORKFLOW_DISCLAIMER = (
    "> **NOT LEGAL ADVICE.** This skill is a procedural and\n"
    "> drafting aid, not legal advice. Verify current rules,\n"
    "> deadlines, and venue-specific practices before filing.\n"
    "> Pair with substantive review by counsel where stakes\n"
    "> warrant."
)

PRO_SE_DISCLAIMER = (
    "> **NOT LEGAL ADVICE.** This skill is a drafting aid for\n"
    "> self-represented litigants, not legal advice and not a\n"
    "> substitute for counsel. For complex matters, or matters\n"
    "> with substantial sums at stake, consider consulting a\n"
    "> licensed {state} attorney. Verify every rule, deadline,\n"
    "> and citation against current law before filing."
)

SUBJECT_BUNDLE_DISCLAIMER = (
    "> **NOT LEGAL ADVICE.** This subject-matter bundle describes\n"
    "> a procedural and substantive framework for {state} cases in\n"
    "> this area, not legal advice and not strategic advice for\n"
    "> any specific case. Outcomes are fact-specific; the choice\n"
    "> of defenses, claims, motions, and discovery belongs to the\n"
    "> litigant (and any counsel the litigant retains). Verify\n"
    "> every rule, deadline, and citation against current law\n"
    "> before filing."
)

GENERIC_DISCLAIMER = (
    "> **NOT LEGAL ADVICE.** This skill is a procedural and\n"
    "> reference aid, not legal advice. Verify current rules,\n"
    "> deadlines, and citations against the authoritative source\n"
    "> before relying on anything here. Pair with substantive\n"
    "> review by counsel where stakes warrant."
)

DISCLAIMER_BY_ROLE = {
    # Drafting scaffolders — user picks motion / declaration / order
    "draft-motion": DRAFTING_DISCLAIMER,
    "draft-note": DRAFTING_DISCLAIMER,
    "draft-declaration": DRAFTING_DECLARATION_DISCLAIMER,
    "draft-order": DRAFTING_ORDER_DISCLAIMER,
    # Venue skills — defer to current local rules
    "{primary_court}": VENUE_DISCLAIMER,
    "{secondary_court}": VENUE_DISCLAIMER,
    "county-courts": VENUE_DISCLAIMER,
    "family-court": VENUE_DISCLAIMER,
    # Format / QC / fact-check — surface only
    "statewide-format": FORMAT_QC_DISCLAIMER,
    "quality-check": FORMAT_QC_DISCLAIMER,
    "fact-check": FORMAT_QC_DISCLAIMER,
    # Workflow procedural skills
    "discovery": WORKFLOW_DISCLAIMER,
    "hearings": WORKFLOW_DISCLAIMER,
    "post-judgment": WORKFLOW_DISCLAIMER,
    "first-30-days": WORKFLOW_DISCLAIMER,
    "schedule-hearing": WORKFLOW_DISCLAIMER,
    "file-packet": WORKFLOW_DISCLAIMER,
    "submit-order": WORKFLOW_DISCLAIMER,
    # Pro-se — adds consult-an-attorney prompt
    "pro-se": PRO_SE_DISCLAIMER,
    # Reference / deadline aids
    "law-references": GENERIC_DISCLAIMER,
    "deadlines": GENERIC_DISCLAIMER,
    # Subject-matter bundles — fact-specific outcomes
    "consumer-debt": SUBJECT_BUNDLE_DISCLAIMER,
    "family-law": SUBJECT_BUNDLE_DISCLAIMER,
}


def disclaimer_for_skill(role: str, cfg: "StateConfig") -> str:
    """Return the category-appropriate disclaimer blockquote
    for a skill role, with placeholders substituted."""
    key = role
    if role == cfg.primary_court_slug:
        key = "{primary_court}"
    elif role == cfg.secondary_court_slug:
        key = "{secondary_court}"
    template = DISCLAIMER_BY_ROLE.get(key, GENERIC_DISCLAIMER)
    return template.format(state=cfg.name)


# ---- Skill stub templates ---------------------------------------

SKILL_STUB_TEMPLATE = """---
name: {abbr}-{role}
description: >
  {description}
version: 0.1.0
---

# {title}

> **TODO**: Author substantive content. This is a scaffolded
> stub. Research the {state} analog from authoritative sources
> before writing — do not search-and-replace from another
> state plugin.

{disclaimer}

## State context

- **State**: {state}
- **Format rule**: {format_rule}
- **Civil rules**: {civil_rules}
- **Evidence rules**: {evidence}
- **Style manual**: {style_manual}

## What to author

1. Description: replace the placeholder with realistic trigger
   phrases for how a {state} pro se filer would ask about this
2. Body: substantive content matching the role
3. Composition notes: which other {abbr}- skills this layers
   with
4. References: the supporting `references/*.md` files

## References to author

- Research the {state} analog from authoritative sources
  before authoring; do NOT search-and-replace from another
  state plugin

## Cross-references

- `{abbr}-statewide-format` for format baseline
- `{abbr}-{primary_court_slug}` / `{abbr}-{secondary_court_slug}` / `{abbr}-county-courts` for venue
- `{abbr}-pro-se` for pro se conventions
"""

# Role-specific description seed phrases (filled in to the
# `description:` block). Authors should expand these.
ROLE_DESCRIPTIONS = {
    "statewide-format": (
        "Use when the user asks to draft or format a court document"
        " for any {state} court. Triggers include 'draft a pleading',"
        " 'format a {state} document', 'apply {format_rule}',"
        " 'build a caption'. Covers {format_rule} page formatting,"
        " caption requirements, document titles, and citation format"
        " per the {style_manual}."
    ),
    "{primary_court}": (
        "Use when drafting or filing in {primary_court_display}."
        " Triggers include the court name, its case number format,"
        " and local-rule references. Layers on top of"
        " `{abbr}-statewide-format`."
    ),
    "{secondary_court}": (
        "Use when drafting or filing in {secondary_court_display}."
        " Triggers include the court name, its case number format,"
        " and local-rule references. Layers on top of"
        " `{abbr}-statewide-format`."
    ),
    "county-courts": (
        "Use when filing in a {state} court other than"
        " {primary_court_display} or {secondary_court_display}."
        " Covers the most-populous counties' civil courts plus a"
        " statewide directory of all counties."
    ),
    "pro-se": (
        "Use when drafting {state} court documents for a"
        " self-represented (pro se) litigant. Covers the Parker"
        " framework adapted for {state}, service protocols, and"
        " state-specific pro se conventions."
    ),
    "law-references": (
        "Matter-neutral reference catalog for {state} civil"
        " practice: {civil_rules} civil rules, {evidence} evidence"
        " rules, statute citations, fees-and-costs, local rules,"
        " key cases, and the canonical online-sources catalog."
    ),
    "discovery": (
        "Use when drafting, responding to, or compelling discovery"
        " in a {state} civil case. Covers RFPs, RFAs, depositions,"
        " interrogatories (if available under state rules),"
        " meet-and-confer mechanics, and motion to compel."
    ),
    "hearings": (
        "Prepare for and conduct hearings in {state} courts. Use"
        " for oral argument, remote-hearing protocol, courtroom"
        " etiquette, and hearing-day checklist."
    ),
    "post-judgment": (
        "Navigate post-judgment procedure in {state}: motion to"
        " vacate, garnishment response, exemption claims,"
        " supplemental proceedings, satisfaction of judgment."
    ),
    "first-30-days": (
        "Use when a {state} defendant has just been served with a"
        " civil complaint. Covers the matter-neutral response"
        " window: answer deadline, motion-to-dismiss triage,"
        " affirmative defenses, and counterclaim mechanics."
    ),
    "fact-check": (
        "Use to fact-check a {state} court filing before filing."
        " Runs citation verification, internal consistency,"
        " packet consistency, and sworn-vs.-argued consistency"
        " passes."
    ),
    "deadlines": (
        "Use when the user asks about timing or deadlines in a"
        " {state} civil case. Computes calendar-day and court-day"
        " deadlines using state holidays and the state's rules of"
        " time computation."
    ),
    "draft-motion": (
        "Scaffold a motion + supporting memorandum for a {state}"
        " court. Applies the pro-se drafting framework adapted to {state}."
    ),
    "draft-declaration": (
        "Scaffold a declaration (or affidavit, per {state}"
        " conventions) for a {state} court filing."
    ),
    "draft-note": (
        "Scaffold the scheduling document that places a motion on"
        " the {state} court's calendar (terminology varies by"
        " state — Notice of Hearing, Note for Motion Docket,"
        " Notice of Motion, etc.)."
    ),
    "draft-order": (
        "Scaffold a proposed order for a {state} court."
    ),
    "quality-check": (
        "Use to QC, review, or validate a {state} court document"
        " before filing. Runs a two-pass format + content check."
    ),
    "schedule-hearing": (
        "Use when the user needs to reserve a motion hearing date"
        " in a {state} court. Drafts the contact email or call log"
        " per the court's scheduling protocol."
    ),
    "file-packet": (
        "Use when assembling and filing a complete {state} court"
        " motion packet. Verifies every required component,"
        " enforces cross-document consistency, and produces filing"
        " instructions."
    ),
    "submit-order": (
        "Use after a hearing, when the judge has ruled and the"
        " prevailing party needs to submit the proposed order for"
        " signature."
    ),
    "consumer-debt": (
        "Subject-matter bundle for {state} consumer-debt defense:"
        " FDCPA, Regulation F, the {state} consumer-protection"
        " statute, the {state} collection-agency regime (if any),"
        " chain of title, and synthetic example filings."
    ),
    "family-court": (
        "Use when drafting or filing in {state}'s family court —"
        " custody / support / family offense / paternity / abuse"
        " and neglect. Even when {state} hears family matters"
        " inside a Family Division of the general-jurisdiction"
        " trial court (rather than a separate Family Court),"
        " this skill covers the division's rules, intake, and"
        " pro-se forms."
    ),
    "family-law": (
        "Subject-matter bundle for {state} family-law substance:"
        " divorce / annulment / legal separation / custody /"
        " child support / parenting plan / property distribution"
        " / maintenance. Substantive law of {state}'s family"
        " code."
    ),
}


# ---- Generation logic --------------------------------------------

def expand_role(role: str, cfg: StateConfig) -> str:
    """Resolve a role placeholder (e.g., '{primary_court}') to
    its actual skill name component."""
    if role == "{primary_court}":
        return cfg.primary_court_slug
    if role == "{secondary_court}":
        return cfg.secondary_court_slug
    return role


def get_resolved_roles(cfg: StateConfig) -> list[str]:
    """Return the 21 skill name components for this state."""
    return [expand_role(r, cfg) for r in SKILL_ROLES]


def title_for_skill(role: str, cfg: StateConfig) -> str:
    """Human-readable title for the skill body H1."""
    titles = {
        "statewide-format": f"{cfg.name} Statewide Format",
        cfg.primary_court_slug: cfg.primary_court_display,
        cfg.secondary_court_slug: cfg.secondary_court_display,
        "county-courts": f"{cfg.name} County Courts",
        "pro-se": f"Pro Se Drafting for {cfg.name}",
        "law-references": f"{cfg.name} Law References",
        "discovery": f"{cfg.name} Discovery",
        "hearings": f"{cfg.name} Hearings",
        "post-judgment": f"{cfg.name} Post-Judgment Procedure",
        "first-30-days": f"{cfg.name} — First 30 Days After Service",
        "fact-check": f"Fact-Check {cfg.name} Court Filings",
        "deadlines": f"{cfg.name} Case Deadlines",
        "draft-motion": f"Draft a {cfg.name} Motion",
        "draft-declaration": f"Draft a {cfg.name} Declaration",
        "draft-note": f"Draft a {cfg.name} Notice/Note",
        "draft-order": f"Draft a {cfg.name} Proposed Order",
        "quality-check": f"Quality Check ({cfg.name})",
        "schedule-hearing": f"Reserve a Hearing Date ({cfg.name})",
        "file-packet": f"Assemble a {cfg.name} Court Filing Packet",
        "submit-order": f"Post-Hearing Order Submission ({cfg.name})",
        "consumer-debt": f"{cfg.name} Consumer-Debt Defense",
        "family-court": f"{cfg.name} Family Court",
        "family-law": f"{cfg.name} Family Law",
    }
    return titles.get(role, role.replace("-", " ").title())


def description_for_skill(role: str, cfg: StateConfig) -> str:
    """Render the description block for a skill, substituting
    state-specific placeholders. The author should expand this
    with state-specific trigger phrases."""
    # role lookup uses the original SKILL_ROLES key (with
    # placeholder), not the resolved name. Map back.
    key = role
    if role == cfg.primary_court_slug:
        key = "{primary_court}"
    elif role == cfg.secondary_court_slug:
        key = "{secondary_court}"

    template = ROLE_DESCRIPTIONS.get(
        key, "Use this skill when [TODO]. Triggers include [TODO]."
    )
    return template.format(
        state=cfg.name,
        abbr=cfg.abbr,
        primary_court_slug=cfg.primary_court_slug,
        primary_court_display=cfg.primary_court_display,
        secondary_court_slug=cfg.secondary_court_slug,
        secondary_court_display=cfg.secondary_court_display,
        format_rule=cfg.format_rule,
        civil_rules=cfg.civil_rules,
        evidence=cfg.evidence,
        statute=cfg.statute,
        style_manual=cfg.style_manual,
    )


def render_skill_stub(role: str, cfg: StateConfig) -> str:
    """Render the full SKILL.md stub for a skill role."""
    return SKILL_STUB_TEMPLATE.format(
        abbr=cfg.abbr,
        role=role,
        description=description_for_skill(role, cfg),
        title=title_for_skill(role, cfg),
        disclaimer=disclaimer_for_skill(role, cfg),
        state=cfg.name,
        format_rule=cfg.format_rule,
        civil_rules=cfg.civil_rules,
        evidence=cfg.evidence,
        style_manual=cfg.style_manual,
        primary_court_slug=cfg.primary_court_slug,
        secondary_court_slug=cfg.secondary_court_slug,
    )


def render_plugin_json(cfg: StateConfig) -> str:
    """Render the plugin.json file."""
    return json.dumps(
        {
            "name": f"us-{cfg.abbr}-court-docs",
            "version": "0.1.0",
            # State plugins depend on the shared federal-laws plugin
            # rather than embedding federal-debt-laws / ucc-model
            # content. The marketplace runtime auto-installs the
            # dependency and dereferences the in-tree symlinks at
            # install time. See ../../symlink wiring in
            # create_state_plugin() below.
            "dependencies": ["claude-legal-federal-laws"],
            "description": (
                f"Draft and format pleadings, declarations, motions,"
                f" notices, and proposed orders for {cfg.name} courts."
                f" Applies {cfg.format_rule} statewide formatting;"
                f" includes {cfg.primary_court_display} and"
                f" {cfg.secondary_court_display} specifics plus a"
                f" county-courts roll-up; supports pro se workflows."
                f" Architected as matter-neutral civil-procedure"
                f" skills ({cfg.civil_rules} civil rules,"
                f" {cfg.evidence} evidence rules, fees and costs,"
                f" local rules, citation format per the"
                f" {cfg.style_manual}) plus subject-matter bundles."
                f" The first subject-matter bundle, {cfg.abbr}-"
                f"consumer-debt, covers FDCPA / Reg F / state UTPA-"
                f"equivalent / chain-of-title doctrine. All workflows"
                f" are skills (no slash commands) so the agent"
                f" invokes them automatically from natural-language"
                f" requests."
            ),
            "author": {
                "name": "codearranger",
                "url": "https://github.com/codearranger",
            },
            "homepage": "https://github.com/codearranger/claude-legal",
            "repository": "https://github.com/codearranger/claude-legal",
            "license": "MIT",
            "keywords": [
                cfg.name.lower().replace(" ", "-"),
                "legal",
                "pleadings",
                "pro-se",
                cfg.civil_rules.lower(),
                cfg.evidence.lower(),
                "civil-rules",
                "evidence-rules",
                "discovery",
                "hearings",
                "post-judgment",
                "fact-check",
                "fdcpa",
                "consumer-protection",
                "debt-collection",
            ],
        },
        indent=2,
    ) + "\n"


def render_plugin_readme(cfg: StateConfig) -> str:
    """Render the top-level plugins/us-<abbr>-court-docs/README.md — the
    canonical human-facing plugin detail (the marketplace standard). The
    root README.md links here; marketplace.json carries only a short blurb."""
    return (
        f"# us-{cfg.abbr}-court-docs — {cfg.name}\n\n"
        f"Draft and format pleadings, declarations, motions, and proposed "
        f"orders for {cfg.name} courts.\n\n"
        f"> **NOT LEGAL ADVICE.** Output is a drafting aid; verify every "
        f"rule, deadline, and citation against current law before filing.\n\n"
        f"## What it covers\n\n"
        f"Applies **{cfg.format_rule}** formatting; covers "
        f"{cfg.primary_court_display}, {cfg.secondary_court_display}, and a "
        f"county-courts roll-up. Architected as matter-neutral civil-procedure "
        f"skills ({cfg.civil_rules} civil rules, {cfg.evidence} evidence rules, "
        f"fees and costs, local rules, citation per the {cfg.style_manual}, "
        f"discovery, first-30-days, hearings, filing, post-judgment, "
        f"fact-check, deadlines, drafting scaffolders) plus subject-matter "
        f"bundles (starting with `{cfg.abbr}-consumer-debt`).\n\n"
        f"<!-- TODO: expand coverage — venues, subject bundles, statute / "
        f"court-rule corpus sizes, SKILL.md count, and any procedural quirks "
        f"worth flagging. -->\n\n"
        f"## Reference corpora\n\n"
        f"Under `skills/{cfg.abbr}-law-references/references/` (each corpus dir "
        f"has its own README): `{cfg.abbr}-statutes-debt/`, `court-rules/`, plus "
        f"the shared `federal-debt-laws/` / `federal-bankruptcy/` / `ucc-model/` "
        f"symlinks into `claude-legal-federal-laws`.\n\n"
        f"## Refresh\n\n"
        f"Plugin scripts: `format-check.py` ({cfg.format_rule}) · "
        f"`case-calendar.py`.\n\n"
        f"---\n"
        f"Part of the [claude-legal](../../README.md) marketplace. Skills are "
        f"indexed in [CLAUDE.md](../../CLAUDE.md).\n"
    )


def render_corpus_readme(corpus: str, cfg: StateConfig) -> str:
    """Render a README for a reference-corpus directory."""
    return (
        f"# {corpus} Corpus — {cfg.name}\n\n"
        f"> **TODO**: Populate by future pull script.\n\n"
        f"This corpus holds verbatim text of {corpus} content"
        f" most relevant to {cfg.name} civil practice. Source:"
        f" the state's authoritative publisher.\n\n"
        f"## How to populate\n\n"
        f"Author a `scripts/pull_{cfg.abbr}_{corpus.replace('-', '_')}"
        f".py` script that fetches from the state's authoritative"
        f" source.\n"
    )


def render_eval_readme(cfg: StateConfig) -> str:
    """Render the evals/README.md."""
    return f"""# Evals — Skill Regression Tests ({cfg.name})

This folder contains prompt-based regression tests for each
skill in the `us-{cfg.abbr}-court-docs` plugin.

> **TODO**: Author evals across the five categories
> (drafting, formatting, procedural, subject-matter,
> integration). Aim for at least 20 evals across the five
> categories.

## Folder layout

- `procedural/` — matter-neutral civil-procedure evals
- `drafting/` — drafting-skill evals
- `formatting/` — format and local-rule evals
- `subject-matter/` — subject bundle evals
- `integration/` — end-to-end multi-skill evals
"""


# ---- Filesystem operations ---------------------------------------

def create_state_plugin(cfg: StateConfig, root: Path, force: bool, dry_run: bool) -> None:
    """Generate the full plugin directory tree."""
    plugin_dir = root / "plugins" / f"us-{cfg.abbr}-court-docs"

    if plugin_dir.exists() and not force:
        print(
            f"ERROR: {plugin_dir} already exists. Use --force to overwrite.",
            file=sys.stderr,
        )
        sys.exit(2)

    if dry_run:
        print(f"[DRY RUN] Would create {plugin_dir}")

    def write(path: Path, content: str) -> None:
        if dry_run:
            print(f"  CREATE {path.relative_to(root)}")
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    # plugin.json
    write(
        plugin_dir / ".claude-plugin" / "plugin.json",
        render_plugin_json(cfg),
    )

    # plugin-level README.md — the canonical human-facing plugin detail
    # (marketplace standard). The root README.md links here as a one-row
    # table entry, and marketplace.json carries only a short blurb.
    write(plugin_dir / "README.md", render_plugin_readme(cfg))

    # 21 SKILL.md stubs
    roles = get_resolved_roles(cfg)
    for role in roles:
        skill_dir = plugin_dir / "skills" / f"{cfg.abbr}-{role}"
        write(skill_dir / "SKILL.md", render_skill_stub(role, cfg))
        # Most skills have a references/ subdir
        if role not in {
            "first-30-days",
            "fact-check",
            "deadlines",
            "draft-motion",
            "draft-declaration",
            "draft-note",
            "draft-order",
            "quality-check",
            "schedule-hearing",
            "file-packet",
            "submit-order",
        }:
            (skill_dir / "references").mkdir(parents=True, exist_ok=True)

    # statewide-format gets a templates/ subdir
    (plugin_dir / "skills" / f"{cfg.abbr}-statewide-format" /
     "references" / "templates").mkdir(parents=True, exist_ok=True)

    # law-references corpora — state-specific only. federal-debt-laws
    # and ucc-model are NOT state-specific; they live in the shared
    # claude-legal-federal-laws plugin and are reached via symlinks
    # laid down further below.
    corpora_root = plugin_dir / "skills" / f"{cfg.abbr}-law-references" / "references"
    for corpus in ["court-rules", f"{cfg.abbr}-statutes-debt"]:
        corpus_dir = corpora_root / corpus
        corpus_dir.mkdir(parents=True, exist_ok=True)
        write(corpus_dir / "README.md", render_corpus_readme(corpus, cfg))

    # Symlinks into the shared claude-legal-federal-laws plugin.
    # Relative path from corpora_root (5 levels deep under repo root)
    # back up to plugins/ then down into the shared plugin.
    if not dry_run:
        corpora_root.mkdir(parents=True, exist_ok=True)
    shared_target_prefix = Path("../../../../claude-legal-federal-laws/references")
    for corpus in ["federal-debt-laws", "federal-bankruptcy", "ucc-model"]:
        link_path = corpora_root / corpus
        target = shared_target_prefix / corpus
        if dry_run:
            print(f"  SYMLINK {link_path.relative_to(root)} -> {target}")
        else:
            # Remove a pre-existing dir/file if present (idempotent rerun).
            if link_path.is_symlink() or link_path.exists():
                if link_path.is_symlink() or link_path.is_file():
                    link_path.unlink()
                else:
                    shutil.rmtree(link_path)
            link_path.symlink_to(target)

    # Subject-bundle examples/ dirs
    (plugin_dir / "skills" / f"{cfg.abbr}-consumer-debt" /
     "references" / "examples").mkdir(parents=True, exist_ok=True)
    (plugin_dir / "skills" / f"{cfg.abbr}-family-law" /
     "references" / "examples").mkdir(parents=True, exist_ok=True)

    # Scripts (copy from or-court-docs as starting point)
    or_scripts = root / "plugins" / "or-court-docs" / "scripts"
    new_scripts = plugin_dir / "scripts"
    if not dry_run:
        new_scripts.mkdir(parents=True, exist_ok=True)
    for script_name in ["format-check.py", "case-calendar.py"]:
        src = or_scripts / script_name
        dst = new_scripts / script_name
        if src.exists():
            if dry_run:
                print(f"  COPY  {src.relative_to(root)} -> {dst.relative_to(root)}")
            else:
                shutil.copy2(src, dst)
                # TODO marker prepended so the agent knows to
                # adapt. The copied source is a working baseline
                # that the agent must rewrite for the new state.
                existing = dst.read_text()
                dst.write_text(
                    f"# TODO: Adapt this script for {cfg.name}.\n"
                    f"# Update format-rule references, holidays,"
                    f" and named rules for {cfg.name}.\n\n"
                    f"{existing}"
                )

    # Evals
    evals_root = plugin_dir / "evals"
    for sub in ["drafting", "formatting", "procedural",
                "subject-matter", "integration"]:
        (evals_root / sub).mkdir(parents=True, exist_ok=True)
    write(evals_root / "README.md", render_eval_readme(cfg))

    print(f"\nScaffolded plugin at {plugin_dir.relative_to(root)}\n")
    print("Next steps:")
    print("  1. Author substantive content into each SKILL.md")
    print("  2. Build the references/*.md files")
    print(f"  3. Adapt scripts/format-check.py and case-calendar.py"
          f" for {cfg.name}")
    print("  4. Add 18+ evals across the five categories")
    print(f"  5. Flesh out the plugin README at"
          f" plugins/us-{cfg.abbr}-court-docs/README.md (the canonical detail;"
          " a starter was written — fill in the TODO)")
    print(f"  6. Register us-{cfg.abbr}-court-docs in"
          " .claude-plugin/marketplace.json (short blurb ending"
          " \"Full detail in the plugin README.\")")
    print(f"  7. Add a one-row link to plugins/us-{cfg.abbr}-court-docs/README.md"
          " in the root README.md table; update CLAUDE.md")
    print("  8. Run `python3 scripts/lint-skills.py`")


# ---- CLI ---------------------------------------------------------

def parse_court_arg(arg: str) -> tuple[str, str]:
    """Parse '<slug>:<display>' into (slug, display)."""
    if ":" not in arg:
        print(
            f"ERROR: court argument '{arg}' must be in"
            " '<slug>:<display>' format",
            file=sys.stderr,
        )
        sys.exit(1)
    slug, display = arg.split(":", 1)
    return slug.strip(), display.strip()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold a new state plugin for claude-legal"
    )
    parser.add_argument(
        "--state",
        required=True,
        help="Two-letter state abbreviation (e.g., 'ca')",
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Full state name (e.g., 'California')",
    )
    parser.add_argument(
        "--primary-court",
        required=True,
        help="Primary high-volume court '<slug>:<display>'"
        " (e.g., 'lasc:Los Angeles Superior Court')",
    )
    parser.add_argument(
        "--secondary-court",
        default="county-courts:County Courts Roll-up",
        help="Secondary high-volume court (optional)",
    )
    parser.add_argument(
        "--format-rule",
        default="[STATE FORMAT RULE]",
        help="State's pleading-format rule (e.g., 'CRC 2.100')",
    )
    parser.add_argument(
        "--civil-rules",
        default="[CIVIL RULES]",
        help="State's civil rules code (e.g., 'CCP')",
    )
    parser.add_argument(
        "--evidence",
        default="[EVIDENCE RULES]",
        help="State's evidence rules code (e.g., 'CEC')",
    )
    parser.add_argument(
        "--statute",
        default="[STATUTE CODE]",
        help="State's statute code prefix (e.g., 'Cal. Civ. Code')",
    )
    parser.add_argument(
        "--style-manual",
        default="[STYLE MANUAL]",
        help="State's citation style manual",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Repo root (default: current dir)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing plugin dir",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without writing",
    )
    args = parser.parse_args()

    # Validate state abbr
    abbr = args.state.lower().strip()
    if not abbr.isalpha() or len(abbr) != 2:
        print(
            f"ERROR: --state must be a two-letter abbreviation,"
            f" got '{args.state}'",
            file=sys.stderr,
        )
        return 1

    primary_slug, primary_display = parse_court_arg(args.primary_court)
    secondary_slug, secondary_display = parse_court_arg(args.secondary_court)

    cfg = StateConfig(
        abbr=abbr,
        name=args.name,
        primary_court_slug=primary_slug,
        primary_court_display=primary_display,
        secondary_court_slug=secondary_slug,
        secondary_court_display=secondary_display,
        format_rule=args.format_rule,
        civil_rules=args.civil_rules,
        evidence=args.evidence,
        statute=args.statute,
        style_manual=args.style_manual,
    )

    root = Path(args.root).resolve()
    if not (root / "scripts" / "lint-skills.py").exists():
        print(
            f"ERROR: --root '{root}' does not look like the"
            " claude-legal repo (scripts/lint-skills.py not found)",
            file=sys.stderr,
        )
        return 1

    create_state_plugin(cfg, root, args.force, args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
