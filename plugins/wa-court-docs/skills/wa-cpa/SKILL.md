---
name: wa-cpa
description: >
  Use this skill for Washington Consumer Protection Act (CPA / UDAP)
  claims and defenses — the general unfair-or-deceptive-acts statute,
  RCW 19.86, applicable to any consumer or business matter (not just
  debt or B2B). This is the matter-neutral CPA home that the
  subject-matter bundles compose with. Triggers include "Consumer
  Protection Act", "Washington CPA", "RCW 19.86", "19.86.020",
  "19.86.090", "19.86.093", "UDAP", "unfair or deceptive act or
  practice", "unfair business practice", "deceptive practice",
  "consumer fraud", "Hangman Ridge", "five elements", "public interest
  element", "per se CPA violation", "capacity to deceive", "treble
  damages", "$25,000 cap", "attorney fees CPA", "trade or commerce",
  "injury to business or property", "Panag", "Klem", "Indoor
  Billboard", "Michael v. Mosquera-Lacy", "Short v. Demopolis",
  "Nordstrom v. Tampourlos", "regulated industry exemption", "19.86.170",
  "serve the attorney general", "19.86.095", "CPA statute of
  limitations", "19.86.120", "CPA counterclaim". Covers the five
  Hangman Ridge elements, the unfair-vs-deceptive distinction (Klem),
  the codified public-interest factors (RCW 19.86.093), per se
  pathways, remedies (actual + treble capped at $25,000 + mandatory
  attorney fees + injunction), the 4-year SOL, the regulated-industry
  exemption, and AG service. Composes with wa-consumer-debt (RCW 19.16
  per se), wa-commercial-disputes (B2B CPA), wa-cema (RCW 19.190 per
  se), wa-first-30-days, wa-discovery, wa-draft-motion / -declaration,
  wa-law-references, wa-statewide-format, and wa-pro-se.
version: 0.1.0
---

# Washington Consumer Protection Act (CPA / UDAP) — RCW 19.86

The matter-neutral subject-matter skill for Washington's general
**unfair-or-deceptive-acts** statute, the Consumer Protection Act,
**RCW 19.86**. It supplies the CPA elements, standards, per se
pathways, remedies, and limits that apply to **any** UDAP claim —
consumer or business — and is the canonical CPA home that the
narrower bundles (`wa-consumer-debt`, `wa-commercial-disputes`,
`wa-cema`, landlord-tenant) compose with for their per se hooks.

> **NOT LEGAL ADVICE.** These notes are drafting aids, not legal
> advice. Verify every statute and case citation against current
> authority before filing. See `wa-fact-check` and
> `wa-law-references/references/online-sources.md`.

## How this skill is organized

This is a **subject-matter skill**. It sits alongside the procedural
skills (`wa-first-30-days`, `wa-discovery`, `wa-law-references`, the
`wa-draft-*` scaffolders) and supplies the CPA-specific content they
delegate to.

```
wa-cpa/
├── SKILL.md                  ← you are here
└── references/
    ├── cpa-framework.md       the RCW 19.86 elements, standards,
                               remedies, SOL, exemption, AG service
    └── key-cases.md           the CPA case catalog
```

The verbatim statute is in the corpus at
`wa-law-references/references/wa-rcw-debt/RCW-19_86.md` — cite that for
current text (thin-skill convention).

## The claim in one screen

A private CPA claim has **five *Hangman Ridge* elements** (105 Wn.2d
778 (1986)):

1. **Unfair OR deceptive** act or practice (independent prongs — *Klem*).
2. In **trade or commerce** (RCW 19.86.010(2)).
3. **Public interest** impact (codified at RCW 19.86.093).
4. **Injury** to plaintiff's **business or property** (not personal
   injury alone; can be modest — *Panag*).
5. **Causation** — proximate link (*Indoor Billboard*).

**Two ways to satisfy element 1 + shortcut elements 2–3:**

- **Per se:** the predicate statute declares a violation to be a per se
  CPA violation (CEMA RCW 19.190.030; Collection Agency Act RCW
  19.16.440; etc.). Establishes the unfair/deceptive act and supplies
  the public interest via RCW 19.86.093(1). The plaintiff then proves
  only **injury + causation**.
- **Independent (non-per-se):** prove **deception** (capacity to deceive
  a substantial portion of the public — no intent required, *Panag*) **or
  unfairness** (FTC standard — substantial injury, not reasonably
  avoidable, not outweighed by benefits — *Klem*), plus the
  capacity-to-injure-others public interest (RCW 19.86.093(3)).

See `references/cpa-framework.md` for each element in depth.

## Remedies (RCW 19.86.090)

- Actual damages + injunctive relief.
- **Mandatory** costs and reasonable attorney's fees to a prevailing
  plaintiff (*Nordstrom v. Tampourlos*).
- **Discretionary treble damages, capped at $25,000** for a § .020
  violation; available to pro se plaintiffs.
- District-court option (actual damages to the RCW 3.66.020 limit, same
  treble cap).
- **4-year SOL** (RCW 19.86.120). **Serve the Attorney General** with the
  initial pleading whenever injunctive relief is requested (RCW 19.86.095).

## When to reach for this skill vs. a bundle

- **Reach for `wa-cpa`** when the matter is a **standalone UDAP claim** —
  deceptive advertising, a misrepresented consumer transaction, an unfair
  business practice — that does **not** sit inside one of the existing
  bundles, or when you need the **general CPA framework** (elements,
  public interest, remedies) regardless of subject matter.
- **Compose with a bundle** for its per se hook and subject-specific law:
  - `wa-consumer-debt` — RCW 19.16 Collection Agency Act per se (RCW 19.16.440).
  - `wa-cema` — RCW 19.190 anti-spam per se (RCW 19.190.030).
  - `wa-commercial-disputes` — B2B CPA, including the public-interest
    analysis for essentially private commercial disputes.
  - `wa-landlord-tenant` — RLTA-based deceptive/unfair practices.

## Defense checklist (if you represent the defendant)

- **Public interest:** is this an essentially **private dispute** with no
  capacity to injure others (RCW 19.86.093(3) / *Hangman Ridge* /
  *Michael v. Mosquera-Lacy* factors)?
- **Injury / causation:** is the claimed injury to **business or
  property** (not personal/emotional alone), and is it **proximately
  caused** by the challenged act (*Indoor Billboard*)?
- **Trade or commerce:** for a professional defendant, does the claim go
  to **competence/strategy** (outside the CPA) rather than the
  **entrepreneurial** aspects (*Short v. Demopolis*)?
- **Regulated-industry exemption** (RCW 19.86.170) — is the specific
  challenged action actually required/permitted by a regulator (narrow)?
- **SOL** — outside the 4-year window (RCW 19.86.120)?

## Composition

- **`wa-first-30-days`** — pleading the CPA claim or counterclaim;
  answer posture and affirmative defenses if defending.
- **`wa-discovery`** — targeting the pattern/other-customer evidence
  that proves public interest, the deceptive materials, and causation.
- **`wa-draft-motion` / `wa-draft-declaration`** — scaffolders.
- **`wa-law-references`** — civil rules, evidence (capacity-to-deceive
  is an objective question; pattern evidence under ER 404(b) limits),
  fees, online sources; the verbatim RCW 19.86 chapter.
- **`wa-statewide-format`** — GR 14; **`wa-fact-check`** — citation +
  good-law verification before filing.
