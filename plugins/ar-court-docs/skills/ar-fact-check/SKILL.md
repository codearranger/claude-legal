---
name: ar-fact-check
description: >
  Use to fact-check an Arkansas court filing before it goes out the
  door. Triggers include "check my citations Arkansas", "is this Ark.
  Code Ann. cite right", "Arkansas citation format", "2015 Ark. 100
  citation", "Ark. App. citation", "medium-neutral citation Arkansas",
  "Ark. Sup. Ct. R. 5-2", "do my exhibits match my motion", "is my
  affidavit consistent with my brief", "verify quotes against the
  source", "proofread my Arkansas filing for accuracy". Runs four
  verification passes — citation verification (medium-neutral and Ark.
  Code Ann. / Ark. R. Civ. P. / Ark. R. Evid. format), internal
  consistency, packet consistency, and sworn-vs-argued consistency —
  so nothing in the filing contradicts itself or misstates authority.
version: 0.1.0
---

# Fact-Check Arkansas Court Filings

> **NOT LEGAL ADVICE.** Formatting and quality checks verify the
> surface — they don't tell the user whether the underlying legal
> position is sound. Verify current rules and case law before filing;
> pair with substantive review by counsel where stakes warrant.

Use this skill to run a disciplined verification sweep over an Arkansas
filing **before** it is filed. It is a four-pass framework: citation
verification, internal consistency, packet consistency, and
sworn-vs-argued consistency. For the format / typography QC pass, use
`ar-quality-check`; this skill is about whether the **content** is
accurate and self-consistent.

## Pass 1 — Citation verification

Check every authority cited and confirm both the **form** of the
citation and that the cited source **says what the filing claims**.

### Arkansas citation form (Ark. Sup. Ct. R. 5-2)

- **Medium-neutral / public-domain citation (since July 1, 2009).**
  Arkansas appellate opinions are cited by a court-assigned
  medium-neutral cite under **Ark. Sup. Ct. R. 5-2**:
  - **Arkansas Supreme Court**: `Smith v. Jones, 2015 Ark. 100` —
    the format is `[YEAR] Ark. [opinion number]`.
  - **Arkansas Court of Appeals**: `Smith v. Jones, 2015 Ark. App.
    200` — the format is `[YEAR] Ark. App. [opinion number]`.
  - A parallel **S.W.3d** reporter cite may be appended when available.
  - **Pre-July-1-2009 cases** cite to the **Arkansas Reports** (Ark.)
    and the South Western Reporter (e.g., `294 Ark. 239`, with the
    `S.W.2d`/`S.W.3d` parallel). Do not retrofit a medium-neutral cite
    onto a pre-2009 case.
- **Pinpoint citations** to medium-neutral opinions are by **paragraph
  number** (the opinions are paragraph-numbered), not page number.
- **Statutes**: `Ark. Code Ann. § 16-56-111` (use the section symbol;
  the Code is cited by title-chapter-section).
- **Rules**: `Ark. R. Civ. P. 12`; `Ark. R. Evid. 803(6)`; appellate
  rules as `Ark. R. App. P.–Civ.` / `Ark. Sup. Ct. R.`; administrative
  orders as `Administrative Order No. 19`.
- Arkansas has **no separate state style manual** — Rule 5-2 governs
  case citation and the Bluebook fills gaps; do not invent a house style.

### Verification steps

1. **Pull each cited source** from `ar-law-references` (or the official
   source) and confirm the statute / rule / case actually stands for the
   proposition asserted.
2. **Quote-to-source check.** Every quotation must match the source
   **verbatim** — check ellipses, brackets, and emphasis.
3. **Currency.** Confirm the statute or rule has not been amended or
   repealed and the case has not been overruled or superseded. Several
   Arkansas tort-reform provisions were **struck down by the Arkansas
   Supreme Court** (for example, the nonparty-fault allocation
   provision and the punitive-damages cap of the Civil Justice Reform
   Act of 2003) — do not cite a statute that has been held
   unconstitutional as if it were good law. When in doubt, verify the
   case's treatment.
4. **Subsection accuracy.** Confirm the exact subsection (e.g.,
   `§ 4-88-113(f)` for the ADTPA private-action element) — pinpoint
   subsections drift across amendments.

## Pass 2 — Internal consistency

Within a single document, confirm:

- **Party names, dates, dollar amounts, and account numbers** are
  identical every time they appear.
- **Defined terms** are used consistently (if "the Agreement" is
  defined once, it is not later called "the Contract").
- **Cross-references** inside the document point to the right
  paragraph / exhibit.
- The **relief requested** in the prayer matches the relief argued in
  the body.

## Pass 3 — Packet consistency

Across every document in the filing packet (motion, brief, affidavit,
exhibits, proposed order):

- The **caption** (court, county, division, case number, party
  designations) is identical on every paper — see `ar-statewide-format`
  for the Ark. R. Civ. P. 10(a) caption shape.
- **Exhibit references** in the brief match the **exhibit labels**
  actually attached, and each referenced exhibit is present.
- The **facts asserted in the brief** are supported by the **affidavit
  / declaration** and the exhibits — no argued fact lacks a sworn or
  documentary source.
- The **proposed order** grants exactly what the motion requests — no
  more, no less. See `ar-submit-order`.

## Pass 4 — Sworn-vs-argued consistency

This is the pass that catches the dangerous mismatch:

- Anything stated as **fact** in an affidavit or verified pleading must
  be **within the affiant's personal knowledge** and must **not
  contradict** what is argued in the brief.
- Argument in the brief must not **assert facts that no one swore to**.
- If the affidavit hedges ("on information and belief") but the brief
  states the same point as established fact, reconcile them.
- Remember Arkansas is a **fact-pleading** jurisdiction (Ark. R. Civ.
  P. 8(a)) — the complaint must plead **facts**, not conclusions, so a
  fact-check should confirm the pleaded facts are actually there and
  are supported, not merely labeled.

## Composition

- For format / typography QC: `ar-quality-check`
- For the caption and signature baseline: `ar-statewide-format`
- For drafting the documents being checked: `ar-draft-motion`,
  `ar-draft-declaration`, `ar-draft-order`
- For the proposed order it is checked against: `ar-submit-order`
- For the authorities being verified: `ar-law-references`

## References

- `ar-law-references` hosts the Ark. Sup. Ct. R. 5-2 citation rule, the
  Ark. Code Ann. statutes, the Ark. R. Civ. P. / Ark. R. Evid. text,
  and the key-cases list used to verify currency and treatment.
