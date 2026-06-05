---
name: ar-quality-check
description: >
  Use to QC, review, or validate an Arkansas court document before
  filing. Triggers include "check my Arkansas filing", "is my motion
  formatted right for Arkansas", "review my pleading before I file",
  "does my caption meet Ark. R. Civ. P. 10", "did I sign this right",
  "Administrative Order 19 redaction", "do I need to redact my SSN",
  "certificate of compliance Arkansas", "preflight my filing",
  "pre-filing checklist Arkansas". Runs a two-pass check — a format
  pass against the Ark. R. Civ. P. 10/11 caption + signature and
  Administrative Order No. 19 redaction (via scripts/format-check.py),
  and a content pass for consistency — and WARNs where typography is a
  local-rule matter because Arkansas has no statewide format rule.
version: 0.1.0
---

# Quality Check (Arkansas)

> **NOT LEGAL ADVICE.** Formatting and quality checks verify the
> surface — they don't tell the user whether the underlying legal
> position is sound. Verify current rules before filing; pair with
> substantive review by counsel where stakes warrant.

Use this skill as the **last gate before filing**. It runs two passes:
a **format pass** (does the document meet the Ark. R. Civ. P. 10/11
caption + signature requirements and Administrative Order No. 19
redaction) and a **content pass** (is the document internally and
cross-document consistent). For deep citation / sworn-vs-argued
checking, hand off to `ar-fact-check`; this skill is the format-plus-
surface gate.

## The Arkansas format posture — what we can and cannot check

> ⚠ **Arkansas has NO single statewide rule prescribing paper size,
> margins, font, or page limits for trial-court pleadings.** Typography
> is governed by the **local rules and administrative plan of each
> judicial circuit / division**. So the format check **WARNs** (does
> not hard-fail) on typographic items — it applies the
> marketplace-universal common-practice defaults and flags anything
> off, but the authoritative typography rule is the venue's local rule.
> Confirm margins / page limits / chambers-copy conventions through
> `ar-law-references` and the venue skills before relying on a default.

What **is** governed by statewide rule and therefore checked firmly:

- **Caption** — Ark. R. Civ. P. 10(a): name of the court, the title /
  parties, the docket ("Civil No." / "Case No.") line, and the
  designation of the paper. See `ar-statewide-format` for the
  caption shape (Circuit Court vs. District Court).
- **Numbered paragraphs** — Ark. R. Civ. P. 10(b): averments in
  numbered paragraphs.
- **Attached instruments** — Ark. R. Civ. P. 10(c): a copy of a written
  instrument that is an exhibit is a part of the pleading.
- **Signature** — Ark. R. Civ. P. 11: the signing party / attorney
  signs and thereby makes the Rule 11 representations. An attorney signs
  with the **Arkansas Bar Number** ("Ark. Bar No. #####"); a
  self-represented filer **omits the bar number** and signs as "Pro Se"
  / "Self-Represented." See `ar-pro-se`.
- **Redaction + certificate** — **Administrative Order No. 19** (Access
  to Court Records): confidential / identifying information (SSNs,
  financial-account numbers, minors' identifiers) must be **redacted**,
  and filed PDFs should carry a **certificate of compliance with
  Administrative Order No. 19**.

## Pass 1 — Format (run the script)

Run the format checker on the assembled document:

```
python3 scripts/format-check.py <path-to-docx-or-pdf>
```

It checks the marketplace common-practice defaults (US Letter, 1"
margins, readable serif body, line-numbered pleading paper, a
doc-title + Page X of Y footer) against the Ark. R. Civ. P. 10/11
caption + signature requirements, and **WARNs** where an item is a
**local-rule** matter (the typographic items) rather than a statewide
requirement. Read the WARNINGS — they are pointers to confirm the
venue's local rule, not failures.

Manual format items the script cannot fully judge:

- [ ] **Caption** matches Ark. R. Civ. P. 10(a) and the correct court /
      county / division.
- [ ] **Signature block** is correct (bar number for an attorney; "Pro
      Se" with no bar number for a self-represented filer).
- [ ] **Administrative Order No. 19 redaction** done and the
      **certificate of compliance** attached.
- [ ] If e-filing, the document meets **Administrative Order No. 21**
      assembly requirements — see `ar-file-packet`.

## Pass 2 — Content (consistency)

A fast surface-consistency sweep (for the deep version, use
`ar-fact-check`):

- [ ] The **caption** is identical on every paper in the packet.
- [ ] **Party names, dates, and dollar figures** match throughout.
- [ ] **Exhibit references** match the exhibits actually attached.
- [ ] The **prayer for relief** matches what is argued, and the
      **proposed order** (if any) grants exactly that — see
      `ar-submit-order`.
- [ ] Nothing **sworn** in an affidavit contradicts what is **argued**
      in the brief.
- [ ] As a **fact-pleading** jurisdiction, the pleading states **facts**
      (Ark. R. Civ. P. 8(a)), not bare conclusions.

## Composition

- For the caption / signature / format baseline: `ar-statewide-format`
- For the deep citation + sworn-vs-argued passes: `ar-fact-check`
- For packet assembly + e-filing under Admin Orders 19/21:
  `ar-file-packet`
- For the proposed order it is checked against: `ar-submit-order`
- For self-represented signature conventions: `ar-pro-se`
- For venue-specific local format rules: `ar-pulaski`, `ar-benton`,
  `ar-washington`, `ar-district-courts`, `ar-county-courts`

## References

- `ar-law-references` hosts the Ark. R. Civ. P. 10/11 text,
  Administrative Order No. 19 (redaction) and No. 21 (e-filing), and the
  circuit local rules that govern trial-court typography.
