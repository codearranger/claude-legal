---
name: ar-file-packet
description: >
  Use when assembling and filing a complete motion or pleading packet in
  an Arkansas court. Triggers include "how do I file this in Arkansas",
  "assemble my filing packet", "eFlex Arkansas e-filing", "how do I
  e-file in Arkansas circuit court", "Administrative Order 21 e-filing",
  "what do I need to redact before filing", "certificate of compliance
  Administrative Order 19", "document type to select when e-filing",
  "preflight my Arkansas filing", "what goes in my filing packet". Walks
  through assembling every required component, redacting per
  Administrative Order No. 19 (with the certificate of compliance),
  e-filing via eFlex under Administrative Order No. 21, selecting the
  right document type, and preflighting with the plugin scripts.
version: 0.1.0
---

# Assemble an Arkansas Court Filing Packet

> **NOT LEGAL ADVICE.** This skill is a procedural and drafting aid,
> not legal advice. Verify current rules, deadlines, and venue-specific
> filing practices before filing. Pair with substantive review by
> counsel where stakes warrant.

Use this skill to take a set of drafted documents and turn them into a
**filing-ready packet** for an Arkansas court — assembled, redacted,
preflighted, and ready for the clerk or the e-filing portal. For the
content / consistency check, pair with `ar-quality-check` and
`ar-fact-check`; this skill is about **assembly and submission**.

## What goes in the packet

A typical contested-motion packet contains, in order:

1. **The motion** (Ark. R. Civ. P. 10 caption; numbered paragraphs) —
   see `ar-draft-motion`.
2. **A supporting brief / memorandum** (if the motion or local rule
   calls for one).
3. **Supporting affidavit(s) / declaration(s)** and **exhibits**
   (a written instrument attached as an exhibit is part of the
   pleading, Ark. R. Civ. P. 10(c)) — see `ar-draft-declaration`.
4. **A Notice of Hearing** if a hearing has been coordinated — see
   `ar-schedule-hearing` / `ar-draft-note`.
5. **A proposed order** where the court expects one — see
   `ar-draft-order` and `ar-submit-order`.
6. **A certificate of service** (Ark. R. Civ. P. 5) and a
   **certificate of compliance with Administrative Order No. 19**.

Confirm any **venue-specific** add-ons (cover sheet, chambers copy,
page-limit certification) through `ar-law-references` and the venue
skills — these are local-rule matters.

## Redaction — Administrative Order No. 19

> ⚠ **Before anything is filed, redact under Administrative Order No.
> 19** (Access to Court Records). Confidential / identifying
> information must be removed or partially redacted, typically
> including **Social Security numbers, financial-account numbers, and
> minors' identifiers** (and other categories the order specifies —
> verify the current list in `ar-law-references`).
> - Redact in the **actual PDF content**, not with a black box that can
>   be deleted to reveal the text underneath.
> - Attach (or include) a **certificate of compliance with
>   Administrative Order No. 19** stating the filing complies.
> - If a document must contain sensitive data in full, use the
>   confidential-information procedure the order prescribes rather than
>   filing it in the public record.

## E-filing — eFlex / Administrative Order No. 21

Statewide electronic filing in Arkansas runs through **eFlex** (the
Contexte Case Management System portal), under **Administrative Order
No. 21**. Key points:

- **Registered e-filers consent to e-service** — once you e-file, other
  registered parties are served electronically, which affects the
  mail-add-on analysis (see `ar-deadlines`).
- **Select the correct document type** in eFlex (e.g., "Motion,"
  "Brief," "Affidavit," "Notice of Hearing," "Proposed Order") — the
  document-type code routes the filing and affects how the clerk and
  judge see it. Choosing the wrong type can delay or misroute the
  filing.
- **Lead document vs. attachments** — file the motion as the lead
  document with the brief / affidavit / exhibits as attachments or
  separate filings as the portal and local practice require.
- **PDF assembly** — text-searchable PDFs, bookmarked where helpful,
  with exhibits clearly labeled and paginated.
- Confirm whether your court / case type is **mandatory e-filing** or
  permits paper filing — practice varies by court and case type; verify
  through the venue skills and `ar-law-references`.

## Preflight — run the scripts

Before submitting, preflight the assembled documents:

```
python3 scripts/format-check.py <path-to-docx-or-pdf>
```

This checks the marketplace common-practice defaults against the Ark.
R. Civ. P. 10/11 caption + signature, and **WARNs** where typography is
a **local-rule** matter (Arkansas has no statewide format rule — see
`ar-quality-check`). Then run the consistency passes in
`ar-quality-check` and `ar-fact-check`.

## Filing checklist

- [ ] Every required component present and in order (motion, brief,
      affidavit/exhibits, notice, proposed order, certificates).
- [ ] **Caption** identical on every paper (Ark. R. Civ. P. 10(a)).
- [ ] **Signature block** correct (Ark. Bar No. for an attorney; "Pro
      Se," no bar number, for a self-represented filer).
- [ ] **Administrative Order No. 19 redaction** done in the actual PDF
      + **certificate of compliance** included.
- [ ] **Certificate of service** (Ark. R. Civ. P. 5) included.
- [ ] **Correct document type(s)** selected in eFlex.
- [ ] **Deadlines** confirmed (filing window, response window, any
      hearing date) — see `ar-deadlines`.
- [ ] Preflight scripts + `ar-quality-check` + `ar-fact-check` run
      clean (or every WARNING understood).

## Composition

- For drafting each component: `ar-draft-motion`, `ar-draft-declaration`,
  `ar-draft-note`, `ar-draft-order`
- For the format / content QC before submission: `ar-quality-check`
- For the deep citation + consistency check: `ar-fact-check`
- For getting a hearing date to put in the Notice: `ar-schedule-hearing`
- For the post-hearing proposed order: `ar-submit-order`
- For deadline math: `ar-deadlines`
- For venue-specific e-filing / local rules: `ar-pulaski`, `ar-benton`,
  `ar-washington`, `ar-district-courts`, `ar-county-courts`

## References

- `ar-law-references` hosts Administrative Order No. 19 (redaction +
  certificate of compliance), Administrative Order No. 21 (e-filing via
  eFlex), the Ark. R. Civ. P. 5 / 10 / 11 text, and the venue local
  rules governing packet add-ons and mandatory-e-filing scope.
