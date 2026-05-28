---
name: consumer-credit-monitoring
description: >
  Use this skill to help a consumer apply the proactive, ongoing
  strategy that generates proof of harm and propagates corrections —
  the strategic-application and monitoring layer of a Fair Credit
  Reporting Act (FCRA) matter. Triggers include "should I apply for
  credit", "generate a denial letter", "I need an adverse action
  letter", "apply to create proof of harm", "send corrected report to
  everyone", "notify everyone who pulled my credit", "who pulled my
  credit report", "soft vs hard inquiry", "re-notify after dispute",
  "1681i(d)", "annual report review", "review on my birthday",
  "specialty report review", "check report after data breach",
  "data breach class action", "convert denial into approval".
  Covers applying for credit within the last 3-6 months (even with a
  low score) to generate adverse-action letters that establish harm
  and standing, demanding the CRA re-send the corrected report to
  everyone who received it (15 U.S.C. § 1681i(d) — 6-month window for
  most uses, 2-year for employment), monitoring soft and hard
  inquiries so every relevant party gets corrected data, re-pulling
  reports after data-breach notifications, a fixed-date annual review
  (e.g., birthday) of all Big-3 and specialty reports (insurance,
  utility, medical, prescription), and the rising-data-breach
  litigation context. Produces § 1681i(d) re-notification demand
  letters, annual-review calendars/checklists, and post-breach action
  checklists. Composes with consumer-report-ordering,
  consumer-credit-disputes, consumer-report-accuracy,
  consumer-harm-documentation, the state *-consumer-debt bundles, and
  the state *-pro-se skills.
version: 0.1.1
---

# Consumer Credit Monitoring & Strategy

> **NOT LEGAL ADVICE.** This skill produces drafting aids and checklists. It is not legal advice
> and does not create an attorney-client relationship. Verify every deadline, dollar threshold,
> and statutory citation against current law before relying on or filing anything.

## Purpose

Two forward-looking moves: (1) **generate the proof of harm** that gives a claim teeth, and
(2) once errors are corrected, **propagate the corrections** so prior denials turn into approvals
and every party that saw the bad data sees the good data. Then keep watching.

Statutory text: [`../../references/federal-debt-laws/FCRA.md`](../../references/federal-debt-laws/FCRA.md).

## Generate proof of harm — recent credit applications (optional)

A consumer who hasn't applied for credit recently has no fresh **adverse-action letter** — and the
adverse-action letter is among the cleanest forms of proof of **harm and standing**. If the
consumer chooses to generate this proof:

- If the consumer hasn't applied in a while, one option is to apply within the last 3–6 months so
  a current denial (or worse-terms) letter exists.
- **An application can be informative even with a low score.** The function isn't approval — it's
  to receive the **denial letter** that documents the consequence of the inaccurate report. Route
  any denial to `consumer-report-ordering` (free post-adverse-action report) and
  `consumer-harm-documentation` (damages record).
- Whether to apply for credit at all is a personal-finance decision for the consumer; this skill
  describes only what happens if the consumer chooses to.

## Propagate corrections — re-notify everyone who pulled the report

After a successful dispute/correction, don't stop at the consumer's own copy:

- **Demand the CRA send the corrected report to everyone who received it.** Under 15 U.S.C.
  § 1681i(d), on the consumer's request the CRA must furnish notification of a correction/deletion
  to persons who received the report — **within the prior 6 months** for most purposes (**2 years**
  for employment purposes). The source guidance frames this as "everyone who pulled it in the past
  year"; apply the **statutory 6-month / 2-year windows** when drafting.
- **Monitor soft and hard inquiries** to identify exactly who pulled the file, so each relevant
  party gets the corrected data.
- **Convert denials into approvals.** A corrected report sent back to a creditor/insurer/landlord
  who previously denied the consumer can reopen the decision on better terms.

## Ongoing monitoring cadence

- **Fixed-date annual review.** Pick a memorable date (e.g., the consumer's **birthday**) and
  review **all** reports each year — Big-3 **and** specialty (insurance, utility, medical,
  prescription). Accurate reports need no action; errors trigger a dispute to prevent overpaying or
  future denials.
- **After any data-breach notice,** pull reports **immediately** to catch fraud early and minimize
  damage — and preserve the breach notice (it is itself a free-report trigger and potential claim).
- **Context:** data-breach **class actions** and private FCRA suits are rising as consumers grow
  more vigilant; clear, contemporaneous harm documentation is what maximizes recovery.

## Artifacts this skill drafts

- **§ 1681i(d) re-notification demand** — requests the CRA furnish the corrected/deleted-information
  notice to all recipients within the 6-month (2-year employment) window.
- **Annual-review calendar / checklist** — the fixed-date list of every Big-3 and specialty report
  to pull, with an errors-found → dispute routing column.
- **Post-breach action checklist** — immediate steps after a data-breach notice (pull reports,
  preserve the notice, consider fraud alert/freeze, diary follow-up).

Each artifact ends with the `NOT LEGAL ADVICE` disclaimer.

## Related federal authority

- **ECOA § 1691(d) + Reg B § 1002.9** —
  [`../../references/federal-debt-laws/ECOA.md`](../../references/federal-debt-laws/ECOA.md) /
  [`../../references/federal-debt-laws/Reg-B.md`](../../references/federal-debt-laws/Reg-B.md).
  Applying for credit to generate an **adverse-action (denial) letter** invokes the ECOA / Reg B
  notice regime as well as FCRA § 1681m — both govern the letter you are trying to generate.
- **Reg V §§ 1022.70–1022.75 (12 CFR Part 1022)** —
  [`../../references/federal-debt-laws/Reg-V.md`](../../references/federal-debt-laws/Reg-V.md).
  The **risk-based-pricing notice** is triggered when a report leads to worse terms — relevant when
  a corrected report should convert prior worse-terms offers into better ones.

## Composition

- Order the reports (incl. the post-adverse-action free report) → **`consumer-report-ordering`**.
- File the dispute that produces the correction → **`consumer-credit-disputes`**.
- Confirm the corrected data + dispute marks → **`consumer-report-accuracy`**.
- Turn denials and breach notices into a damages record → **`consumer-harm-documentation`**.
- Underlying debt defense → the state **`*-consumer-debt`** bundle; pro-se mechanics → the state
  **`*-pro-se`** skill.
