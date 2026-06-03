# wa-court-docs

Draft and format documents for Washington State courts.

## What it does

- Applies **GR 14** formatting to pleadings and papers (US Letter, 3″ top margin on page 1, 1″ elsewhere, no colored markings, proper citation format)
- Builds two-column **pleading captions** with parties on the left and case number / document title on the right
- Scaffolds common document types: **declarations** (with exhibits), **motions + supporting memoranda**, **notes for motion docket**, and **proposed orders**
- Handles **exhibit lists and cover pages** with consistent pagination and footers
- Covers **King County District Court** (including South Division / Burien) local practice
- Supports **pro se** workflows using the pro-se drafting framework
- Guides the **first 30 days** after service — deadline computation, motion-to-dismiss vs. answer triage, affirmative-defense and counterclaim planning
- Provides **discovery procedure** (matter-neutral) and subject-matter request banks (currently debt-buyer)
- Guides **hearing preparation** for in-person and Zoom — oral argument structure, courtroom etiquette, day-of checklist
- Covers **post-judgment** procedure — CR 60 motions to vacate, garnishment response, exemptions, satisfaction of judgment
- Provides canonical **online-sources** catalog for AI-agent verification, and a **fact-check** skill that runs citation, internal-consistency, packet, and sworn-vs.-argued checks before filing
- Ships a **subject-matter bundle for consumer-debt defense** — FDCPA, Reg F, RCW 19.16 Collection Agency Act, Washington CPA, chain-of-title doctrine under UCC Article 9, ten recurring fact patterns, debt-buyer discovery banks, debt-specific key cases, and synthetic example filings

## Architecture

The plugin is organized into two layers:

1. **Matter-neutral procedural skills** — these apply to any Washington civil case regardless of subject matter (civil rules, evidence rules, fees-and-costs, local rules, citation format, online sources, discovery procedure, first-30-days response, hearings, filing packets, post-judgment, fact-check, deadlines, pro se, statewide format, KCDC).
2. **Subject-matter bundles** — self-contained skills supplying the substantive law, fact patterns, request banks, case catalog, and example filings for one subject matter. The procedural skills delegate subject-matter-specific questions to these bundles.

Subject-matter skills currently shipping: `wa-consumer-debt`, `wa-family-law`, `wa-landlord-tenant`, `wa-personal-injury`, `wa-employment`, `wa-commercial-disputes`, and `wa-cema` (Commercial Electronic Mail Act, RCW 19.190 — Washington's anti-spam statute; ships the controlling *Brown v. Old Navy*, No. 102592-1 (Wash. 2025) opinion as a reference). The architecture leaves clean slots for additional subject matter.

## Components

All functionality is exposed as **skills**. There are no slash commands — the agent matches each skill's description against what the user says and invokes it automatically.

### Matter-neutral reference skills

| Skill | Purpose |
|-------|---------|
| `wa-statewide-format` | GR 14 formatting rules, caption structure, signature blocks, exhibit handling, the four document templates |
| `wa-kcdc` | King County District Court specifics — divisions, civil motion docket, filing procedures |
| `wa-pro-se` | pro-se drafting framework for drafting (fact-front-loaded, concise, written to the judge), service protocols, common pro se pitfalls |
| `wa-law-references` | Civil rules (CR/CRLJ), Evidence Rules (ER), fees and costs (RCW 4.84, CR 37), local rules (KCLCR, KCDCLCR), citation format, canonical online sources, general-civil key cases |
| `wa-discovery` | Matter-neutral discovery framework — RFPs, interrogatories, RFAs, meet and confer, motion to compel |
| `wa-hearings` | Courtroom etiquette, oral argument structure, remote hearings, hearing-day checklist |
| `wa-post-judgment` | CR 60 motion to vacate, RCW 6.27 garnishment response, exemptions, supplemental proceedings, satisfaction of judgment |

### Matter-neutral workflow skills

| Skill | Triggers on | Does |
|-------|-------------|------|
| `wa-first-30-days` | "I was just served", "answer deadline", "affirmative defenses" | From-service-through-answer-filed workflow — deadline math, MTD vs. answer triage, general affirmative-defenses checklist, compulsory-counterclaim analysis, evidence preservation, initial discovery plan |
| `wa-draft-motion` | "draft a motion", "motion to compel / dismiss / vacate / strike" | Scaffolds a motion + supporting memorandum (pro-se drafting framework) |
| `wa-draft-declaration` | "draft a declaration", "declaration in support" | Scaffolds a declaration with numbered paragraphs, verification clause, exhibit list |
| `wa-draft-note` | "note for motion docket", "schedule the motion" | Scaffolds the Note for Motion Docket (KCDC variant when applicable) |
| `wa-draft-order` | "proposed order", "order granting" | Scaffolds a proposed order with findings and enforceable relief |
| `wa-quality-check` | "QC this", "is this GR 14 compliant", "review before I file" | Two-pass format + content check; motion-type-specific checklists |
| `wa-fact-check` | "fact check this", "verify citations", "cite-check" | Four-pass verification — citation verification (RED/YELLOW/ORANGE/GREEN), internal consistency, packet consistency, sworn-vs.-argued consistency. Never silently rewrites |
| `wa-deadlines` | "when is my answer due", "compute the deadline" | Computes court- and calendar-day deadlines with RCW 1.16.050 holidays; response, discovery, appeal, and post-judgment windows |
| `wa-schedule-hearing` | "reserve a hearing date", "email CivilMGT" | Drafts the KCDC scheduling email (step 1 of the three-step motion-docket protocol) |
| `wa-file-packet` | "assemble the packet", "I'm ready to file" | Verifies components, caption consistency, and service; enforces a clerk-issued-date preflight for KCDC filings |
| `wa-submit-order` | "submit the order", "the judge granted — prepare the order" | Strips `[PROPOSED]`, applies bench modifications, prepares the transmittal, tracks compliance deadlines |

### Subject-matter bundles

| Bundle | Covers |
|--------|--------|
| `wa-consumer-debt` | Debt-buyer and original-creditor collection cases — FDCPA (15 U.S.C. § 1692 et seq.), Regulation F (12 C.F.R. Part 1006), RCW 19.16 Collection Agency Act, Washington Consumer Protection Act (RCW 19.86, *Hangman Ridge* framework, per se pathway via RCW 19.16.440), Washington statutes of limitations as applied to consumer debt, UCC Article 9 chain-of-title doctrine (RCW 62A.9A), ten recurring debt-buyer fact patterns, debt-specific key cases (*Ziegler*, *Discover Bank v. Bridges*, *Gray v. Suttell*, *Panag*, *CACH v. Kulas*, *Unifund*, *Palisades*, *Midland*, *Rotkiske*, *Heintz*, *Henson*, *Donohue*, *Tourgeman*, etc.), RFPs / IROGs / RFAs / meet-and-confer paragraphs targeting debt-buyer deficiencies, and synthetic example filings (answer, motion to compel, declaration, proposed order, meet-and-confer letter, certificate of service) |

## Composition examples

- A typical debt-buyer defense flow: `wa-first-30-days` composes with `wa-consumer-debt` for subject-matter triage, then with `wa-draft-motion` / `wa-draft-declaration` / `wa-draft-order` for the filings, `wa-law-references` for civil and evidence rules and fee authorities, `wa-pro-se` for voice and the pro-se drafting framework, `wa-statewide-format` for GR 14, `wa-kcdc` for King County District Court specifics, `wa-fact-check` before filing, and `wa-file-packet` for assembly.
- A general civil answer flow without subject-matter specifics: `wa-first-30-days` runs with just the procedural layer — `wa-law-references`, `wa-draft-*`, `wa-fact-check`, `wa-file-packet`.

## Installing

From a marketplace that includes this plugin:

```
/plugin install wa-court-docs
```

## Required tools

The plugin assumes access to standard Claude file tools: Read, Write, Edit, Bash.
For `.docx` generation it expects `node` + the `docx` npm package, and for
format validation a Python 3 interpreter.

## Not legal advice

This plugin is a drafting aid. Review all output carefully against current
court rules and local practice before filing. The author is not an attorney
and nothing in this plugin constitutes legal advice.

## License

MIT.
