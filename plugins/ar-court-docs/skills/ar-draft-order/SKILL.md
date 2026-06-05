---
name: ar-draft-order
description: >
  This skill should be used to scaffold an Arkansas proposed order for a
  circuit judge's signature. Triggers include "draft an Arkansas
  proposed order", "draft an order in Arkansas", "proposed order
  granting motion to dismiss", "proposed order on summary judgment in
  Arkansas", "default judgment order Arkansas", "draft an order for the
  judge to sign", "order approved as to form", "precedent / proposed
  decree for an Arkansas court". Produces a proposed order with the
  caption replicated, discrete findings, an "IT IS THEREFORE ORDERED"
  decretal block, and the judge-signature line at the foot. Notes that
  only a judge signs an order, the common Arkansas practice of
  circulating the proposed order to opposing counsel for approval as to
  form, and the entry-of-order timing that starts post-judgment clocks.
  Composes with `ar-statewide-format` for the caption, `ar-draft-motion`
  for the underlying motion, and `ar-submit-order` for the transmittal
  workflow.
version: 0.1.0
---

# Draft an Arkansas Proposed Order

> **NOT LEGAL ADVICE.** This skill scaffolds a court document as a
> drafting aid. The user — not the skill — chooses the findings, the
> relief, and the form of the order. Only a judge signs an order; this
> skill prepares the proposed form for the judge's consideration.
> Verify every rule, deadline, and citation against current law before
> filing. Pair with substantive review by counsel where stakes warrant.

Use this skill in addition to `ar-statewide-format` when a motion,
stipulation, or hearing outcome requires a **proposed order** for the
circuit judge's signature. In Arkansas, the prevailing party typically
prepares the proposed order after the court announces its ruling; the
court enters the order, and the **date of entry** (the date the signed
order is filed with the clerk) starts post-judgment clocks — including
the **Rule 60(a) 90-day window** to modify or vacate to correct error
and the time to move for a new trial or to appeal (see
`ar-post-judgment` and `ar-deadlines`).

> **Only a judge signs an order.** This skill prepares a *proposed*
> order. The signature line at the foot is for the court; the
> self-represented party or counsel signs only the "prepared by" /
> "approved as to form" lines, never the order itself.

## Cardinal rule — the order mirrors the ruling

The proposed order's relief should **mirror exactly** what the court
ordered. Two failure modes:

- **Over-reaching**: ordering something the court did not grant —
  judges strike or modify these, and opposing counsel will object on
  approval as to form.
- **Under-reaching**: omitting relief the court actually granted —
  leaves the order incomplete and may require a corrective order.

Cross-check the prayer for relief in the motion (`WHEREFORE...`) and
the court's oral ruling against the order's decretal block (`IT IS
THEREFORE ORDERED...`) one item at a time.

## Standard proposed-order structure

```
                [Caption — exactly matching the motion;
                 see ar-statewide-format]

           [DOCUMENT TITLE: ORDER ON DEFENDANT'S
              MOTION TO DISMISS]

On this day the Court considered Defendant's [Motion Title], filed
[date], the response (if any), the supporting affidavits and exhibits,
the argument of the parties, and the record as a whole. The Court
FINDS:

1. [Finding 1 — stated neutrally.]

2. [Finding 2.]

3. [Finding 3.]

IT IS THEREFORE ORDERED, ADJUDGED, AND DECREED that:

A. [Defendant's Motion to Dismiss is GRANTED / DENIED.]

B. [Specific consequential relief, e.g., "Plaintiff's Complaint is
   dismissed with prejudice."]

C. [Costs are taxed to ____.]

IT IS SO ORDERED.

                                        ____________________________
                                        Honorable [Judge Name]
                                        Circuit Judge, [____] Judicial
                                        Circuit, [____] Division

DATE OF ENTRY: ______________________

PREPARED BY / APPROVED FOR ENTRY:

____________________________            ____________________________
[Counsel / Self-Represented Party       [Opposing counsel / party]
 for Movant; see ar-statewide-format     APPROVED AS TO FORM
 signature block]
```

## Findings vs. decretal language — keep them separate

Arkansas judges expect a clear separation between **findings** (what
the court determined, stated neutrally and numbered) and the
**decretal clause** (the lettered or numbered commands following "IT
IS THEREFORE ORDERED"). Conflating the two makes it harder for the
court to edit a finding without disturbing an order.

## Summary-judgment orders

For a **summary-judgment** order under Ark. R. Civ. P. 56, recite the
basis for the ruling rather than a bare "Motion granted": that there is
no genuine issue of material fact and the movant is entitled to
judgment as a matter of law, and — where granted against the
non-movant — that the non-moving party failed to **"meet proof with
proof"** in response (see `ar-draft-motion`). State which essential
element or undisputed fact carried the ruling so the order is
self-supporting on review.

## Default judgment order

For a default judgment, the proposed order should recite the predicate
findings:

```
On this day the Court considered Plaintiff's Motion for Default
Judgment. The Court FINDS:

1. Defendant was served with the Summons and Complaint on [date] as
   shown by the proof of service filed [date].

2. Defendant has failed to plead or otherwise defend within the time
   allowed by Ark. R. Civ. P. 12.

3. Plaintiff is entitled to judgment in the amount of $______,
   consisting of:
     a. Principal: $______
     b. Pre-judgment interest: $______ (state the rate and basis)
     c. Court costs: $______

IT IS THEREFORE ORDERED that judgment is entered in favor of
Plaintiff and against Defendant in the amount of $______.
```

> **Debt-buyer / assigned-account default judgments.** Where the
> plaintiff is a debt buyer or assignee rather than the original
> creditor, the entitlement to default judgment turns on proving the
> **assignment chain** from original creditor to plaintiff,
> authenticated under Ark. R. Evid. 803(6) / 902(11), and the
> plaintiff's **standing/capacity** — including whether the collector
> is licensed under the Arkansas collection-agency regime. A
> default-judgment order in such a matter should reflect that this
> showing was made. See `ar-consumer-debt`.

## Approval as to form — a common Arkansas practice

It is common Arkansas practice to **circulate the proposed order to
opposing counsel for "approval as to form"** before submitting it to
the court. Opposing counsel signs an "APPROVED AS TO FORM" or
"APPROVED FOR ENTRY" line to confirm the order accurately reflects the
court's ruling — this is **not** an agreement with the result, only
with the form. Some courts and local administrative plans require this
circulation; others permit submission with a certificate that the order
was served on the other side with an opportunity to object. Build the
signature block with an approval line, and verify the filing court's
procedure.

The full transmittal workflow — circulating the proposed order,
collecting form approval, submitting it to the judge, and handling
entry by the clerk — is in `ar-submit-order`.

## Composition

- For format and caption: `ar-statewide-format`
- For the underlying motion: `ar-draft-motion`
- For the supporting affidavit: `ar-draft-declaration`
- For circulating and submitting the signed order: `ar-submit-order`
- For the consumer-debt default-judgment posture: `ar-consumer-debt`
- For family-law decree structure: `ar-family-law`
- For post-judgment timing (Rule 60(a) 90-day window): `ar-post-judgment`,
  `ar-deadlines`
- For the venue overlay: `ar-pulaski`, `ar-benton`, `ar-washington`,
  `ar-county-courts`, `ar-district-courts`

## References

- `references/proposed-order-template.md` — annotated template with
  findings, decretal block, and approval-as-to-form line
- `references/default-judgment-order.md` — default-judgment findings
  and the debt-buyer chain-of-title note
- `references/findings-vs-decretal.md` — separating findings from
  ordering language
