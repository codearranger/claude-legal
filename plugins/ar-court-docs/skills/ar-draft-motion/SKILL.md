---
name: ar-draft-motion
description: >
  This skill should be used to scaffold an Arkansas civil motion with
  its supporting brief or memorandum of law. Triggers include "draft a
  motion in Arkansas", "draft an Arkansas motion to compel", "draft an
  Ark. R. Civ. P. 12(b)(6) motion to dismiss", "Arkansas motion for
  summary judgment", "draft a Rule 56 motion in Arkansas", "draft a
  motion for new trial under Rule 59", "draft a Rule 60 motion to set
  aside", "draft an Arkansas motion in limine", "draft a brief in
  support of an Arkansas motion". Produces a motion plus a supporting
  brief in the Arkansas statewide format, applying the pro-se drafting
  framework (state the relief, cite the rule or statute, state the
  supporting facts, conclude with signature and certificate of
  service). Composes with `ar-statewide-format` for the caption and
  signature, `ar-draft-declaration` for sworn facts, `ar-draft-order`
  for the proposed order, `ar-draft-note` for the Notice of Hearing,
  and the relevant venue overlay.
version: 0.1.0
---

# Draft an Arkansas Motion

> **NOT LEGAL ADVICE.** This skill scaffolds a court document as a
> drafting aid. The user — not the skill — chooses the motion type,
> theory of relief, and strategy. Verify every rule, deadline, and
> citation against current law before filing. Pair with substantive
> review by counsel where stakes warrant.

Use this skill to produce a motion + supporting brief or memorandum of
law in Arkansas format. Arkansas motion practice follows the
**Arkansas Rules of Civil Procedure (ARCP)** — state the grounds and
the relief sought, plus the specific rule under which the motion is
filed (Rule 12, Rule 56, Rule 37, Rule 59, Rule 60, etc.). The
caption, numbered paragraphs, signature block, and certificate of
service follow `ar-statewide-format`.

These conventions apply in **Circuit Court** (the unified
general-jurisdiction trial court, where the ARCP govern). In the
limited-jurisdiction **District Court** forum the **Arkansas District
Court Rules** govern and practice is more informal — do not assume
full ARCP written-motion practice there (see `ar-district-courts`).

## Page limits and typography

Arkansas has **no single statewide page-limit, margin, or font rule**
for trial-court pleadings. Form of pleadings is governed by **Ark. R.
Civ. P. 10** (caption naming the court, title and parties, "Civil No."
docket designation; averments in **numbered paragraphs** under Rule
10(b); written instruments attached as exhibits under Rule 10(c)) and
**Ark. R. Civ. P. 11** (signing — the signature certifies the Rule 11
representations; an attorney signs with the Arkansas Bar Number, a pro
se party signs for self). **Page limits, margins, chambers-copy
requirements, and proposed-order conventions are set by per-circuit
LOCAL RULES and the assigned judge's administrative plan** — check the
local rules of the filing court (indexed on arcourts.gov) and the
judge's standing orders before finalizing. See `ar-statewide-format`.

Filed PDFs must carry a **certificate of compliance with Administrative
Order No. 19** (redaction of confidential/identifying information), and
e-filing flows through **eFlex** under Administrative Order No. 21. See
`ar-file-packet`.

## Motion + brief structure

Arkansas practice commonly pairs a short **motion** (stating the relief
and grounds) with a separate or appended **brief in support** (the
legal argument). Some courts permit a combined document; many local
rules expect a discrete brief. Verify the local rule of the filing
court.

```
                    [Caption — see ar-statewide-format]

           [DOCUMENT TITLE IN ALL CAPS, e.g.,
       DEFENDANT'S MOTION TO DISMISS PURSUANT TO
       ARK. R. CIV. P. 12(b)(6)]

[Movant], [Plaintiff / Defendant], pursuant to Ark. R. Civ. P.
[rule], respectfully moves the Court for [specific relief], and in
support states:

1. [Ground one — short, particular statement of fact.]

2. [Ground two.]

WHEREFORE, [Movant] respectfully requests that the Court [grant the
relief sought] and enter the accompanying proposed Order, and for all
other proper relief.

                                        [Signature block —
                                         see ar-statewide-format]

                       CERTIFICATE OF SERVICE
[Date, method, recipients — per ar-statewide-format and Rule 5]
```

> **Fact-pleading reminder.** Arkansas is a **fact-pleading**
> jurisdiction (Ark. R. Civ. P. 8(a) requires a statement of *facts*,
> not mere conclusions). When the motion turns on the sufficiency of a
> pleading, frame the argument around whether the opposing pleading
> states *facts* on each element — not the federal notice-pleading
> standard. See `ar-first-30-days`.

### Supporting brief in support

```
                    [Caption — see ar-statewide-format]

       BRIEF IN SUPPORT OF DEFENDANT'S MOTION TO DISMISS

                       I. INTRODUCTION

[1-2 paragraph summary of the case, the relief sought, and the
reasons in headline form.]

                  II. STATEMENT OF FACTS

[Numbered factual paragraphs. Each material fact gets a record
citation — Affidavit ¶ X, Complaint ¶ X, Exhibit X, or admission in
the pleadings. Sworn facts belong in an affidavit; see
ar-draft-declaration.]

                  III. STANDARD OF REVIEW

[State the governing standard for this motion type — e.g., the Rule
12(b)(6) fact-pleading standard, or the Rule 56 "meet proof with
proof" summary-judgment standard described below.]

                       IV. ARGUMENT

A. [Headline of first argument.]

[Lead with the rule or statute citation; state the controlling
standard; apply it to the facts; cite controlling Arkansas
authority.]

B. [Headline of second argument.]

                       V. CONCLUSION

For the foregoing reasons, [Movant] respectfully requests that the
Court [grant the motion] and enter the accompanying proposed Order.

                                        [Signature block]

                       CERTIFICATE OF SERVICE
[Per ar-statewide-format and Rule 5]
```

## Summary judgment — Rule 56 and the "meet proof with proof" standard

A motion for summary judgment is governed by **Ark. R. Civ. P. 56**.
Once the moving party makes a **prima facie showing** that there is no
genuine issue of material fact and it is entitled to judgment as a
matter of law, the burden shifts: the non-moving party must **"meet
proof with proof"** and demonstrate a genuine issue of material fact by
affidavit or other Rule 56 materials — it cannot rest on the
allegations or denials of its pleadings (*Wallace v. Broyles*;
*Flentje v. First Nat'l Bank of Wynne*). The court views the evidence
in the light most favorable to the non-moving party and resolves all
doubts and inferences against the movant.

> A Rule 56 motion is typically accompanied by supporting affidavits
> made on personal knowledge (see `ar-draft-declaration`) and any
> exhibits authenticated under the Arkansas Rules of Evidence. Verify
> the response period and hearing-notice timing for the filing court
> in `references/` and use `ar-deadlines` to compute the dates; serve
> the motion with enough lead time for the non-movant's response.

## Motion to dismiss — Rule 12(b)(6) and fact pleading

A motion to dismiss for failure to state facts upon which relief can be
granted is brought under **Ark. R. Civ. P. 12(b)(6)**. Because Arkansas
is a fact-pleading state, the motion tests whether the complaint pleads
**facts** — not conclusions — sufficient to state a claim. If matters
outside the pleadings are presented and not excluded by the court, the
motion is **treated as one for summary judgment under Rule 56** and the
parties get a reasonable opportunity to present Rule 56 materials. The
**answer is due within 30 days** of service (longer for nonresident or
out-of-state defendants — verify the exact counts in `references/` and
with `ar-deadlines`); a Rule 12 motion alters the time to answer (see
`ar-first-30-days`).

## Common motion types

| Motion | Rule | Notes |
|---|---|---|
| Motion to Dismiss | Ark. R. Civ. P. 12(b)(6) | Fact-pleading test; converts to Rule 56 if outside matter considered |
| Motion for Summary Judgment | Ark. R. Civ. P. 56 | Prima facie showing → non-movant must "meet proof with proof"; evidence viewed for the non-movant |
| Motion to Compel | Ark. R. Civ. P. 37 | Attach the deficient responses; satisfy the good-faith meet-and-confer requirement first (see `ar-discovery`) |
| Motion for New Trial | Ark. R. Civ. P. 59 | Enumerated grounds; strict timing — verify in `references/` and `ar-deadlines` |
| Motion to Set Aside / Relief from Judgment | Ark. R. Civ. P. 60 | **Rule 60(a)** lets the court modify/vacate within **90 days** of filing to correct error; after 90 days only the narrower **Rule 60(c)** grounds apply (see `ar-post-judgment`) |
| Motion in Limine | (inherent / Ark. R. Evid.) | Pre-trial; anticipated evidentiary disputes |
| Motion for Extension of Time | Ark. R. Civ. P. 6 | Compute under Rule 6(a); Rule 6(d) adds 3 days for service by mail |

## The pro-se drafting framework — applied to motions

Self-represented filers should follow the **pro-se drafting framework**
(see `ar-pro-se`):

1. **State the relief clearly** in the opening sentence.
2. **Cite the rule or statute** (Ark. R. Civ. P. ____ / Ark. Code Ann.
   § ____) that grants the court power to award that relief.
3. **State the facts** that satisfy each element of the standard, with
   record citations to a supporting affidavit.
4. **Apply the controlling Arkansas authority** to those facts (cite
   per Ark. Sup. Ct. R. 5-2 — e.g., medium-neutral `2015 Ark. 100`).
5. **Conclude** with the specific order sought, and attach a proposed
   Order (see `ar-draft-order`).

## Filing checklist

- [ ] Caption matches the assigned court (Circuit / District) and county
- [ ] Title in ALL CAPS centered below the caption
- [ ] Grounds and relief stated, averments in numbered paragraphs (Rule 10(b))
- [ ] All cited rules and statutes correct (run `ar-fact-check`)
- [ ] For Rule 56: supporting affidavit(s); response/hearing timing computed
- [ ] Within any applicable local-rule page limit
- [ ] Proposed Order drafted as a **separate** document (`ar-draft-order`)
- [ ] Supporting affidavit(s) drafted (`ar-draft-declaration`)
- [ ] Notice of Hearing prepared if required (`ar-draft-note`, `ar-schedule-hearing`)
- [ ] Certificate of Service complete (Rule 5)
- [ ] Administrative Order No. 19 redaction + certificate of compliance
- [ ] Format check passes (`scripts/format-check.py`)

## Composition

- For format, caption, and signature block: `ar-statewide-format`
- For the supporting affidavit: `ar-draft-declaration`
- For the proposed order: `ar-draft-order`
- For setting the hearing: `ar-draft-note`, `ar-schedule-hearing`
- For the venue overlay: `ar-pulaski`, `ar-benton`, `ar-washington`,
  `ar-county-courts`, `ar-district-courts`
- For pre-filing QC: `ar-quality-check`, `ar-fact-check`
- For deadline math: `ar-deadlines`
- For pro se conventions: `ar-pro-se`

## References

- `references/motion-template.md` — annotated motion + brief template
- `references/rule-56-standard.md` — the "meet proof with proof"
  summary-judgment standard and Rule 56 timing
- `references/argument-structure.md` — pro-se drafting framework applied
