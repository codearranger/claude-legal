---
name: ar-schedule-hearing
description: >
  Use when the user needs to get a motion or matter set for hearing in
  an Arkansas court. Triggers include "how do I get a hearing date in
  Arkansas", "schedule a hearing on my motion", "how do I get my motion
  heard in circuit court", "do I call the judge's office", "Notice of
  Hearing Arkansas", "set a hearing in Pulaski County", "coordinate a
  hearing date", "District Court return date", "when is my court date".
  Explains how a litigant coordinates a setting with the division /
  judge's office, the per-county and per-judge variation, drafts the
  Notice of Hearing, and flags District Court return-date practice
  (where the date comes on the summons, not by self-scheduling).
version: 0.1.0
---

# Reserve a Hearing Date (Arkansas)

> **NOT LEGAL ADVICE.** This skill is a procedural and drafting aid,
> not legal advice. Verify current rules, deadlines, and venue-specific
> scheduling practices before relying on a date. Pair with substantive
> review by counsel where stakes warrant.

Use this skill to get a motion or matter **set for hearing** in an
Arkansas court. There is **no single statewide self-scheduling system** —
how a setting happens depends on the **court (Circuit vs. District)**,
the **judicial circuit's administrative plan**, and the **individual
judge's chambers practice**. Confirm the procedure for your specific
division before relying on the general framework below.

## Circuit Court — coordinate, then notice

In **Circuit Court**, the usual sequence is:

1. **File the motion** (and brief / supporting papers) — see
   `ar-draft-motion`. Some judges will not set a hearing until the
   motion and the response period have run; confirm the division's
   practice.
2. **Coordinate a date** with the **judge's office / trial court
   assistant (TCA) or court coordinator** — most Arkansas circuit
   judges set their own dockets, so you (or both parties) contact
   chambers to obtain an available date. Some divisions have a
   published motion day; some require you to email proposed dates;
   some issue a setting on their own (a **Notice of Hearing** or
   **scheduling order** from the court).
3. **Serve and file a Notice of Hearing** once a date is obtained,
   notifying all parties of the date, time, place, and the motion to be
   heard — unless the **court itself** issues the setting (in which case
   the court's notice controls).
4. **Confirm the format** (in person / Zoom / phone) — remote-appearance
   practice is local-rule and judge-dependent; see `ar-hearings`.

> Because chambers practice varies judge-by-judge, **call or email the
> division's coordinator** and ask exactly how that judge wants a
> hearing requested. Do not assume a published motion day exists.

## District Court — watch the return-date practice

> ⚠ **District Court is different.** In the limited-jurisdiction
> **District Court** (the high-volume eviction / small-claims /
> consumer-debt forum), the appearance/return **date is frequently set
> on the summons or by the clerk** when the case is filed — the
> defendant is told **when to appear** rather than self-scheduling a
> motion hearing. If you are a **defendant**, read the summons / notice
> for the **return date** and appear (or respond) by it. If you need a
> different setting or a continuance, contact the **District Court
> clerk's office**. See `ar-district-courts`.

## Notice of Hearing — template

When you supply the notice (Circuit Court, after coordinating a date),
use the Ark. R. Civ. P. 10(a) caption (see `ar-statewide-format`) and a
body along these lines:

```
                         NOTICE OF HEARING

   PLEASE TAKE NOTICE that the [moving party]'s [title of motion],
   filed [date], will be heard before the Honorable [Judge], [Division]
   Division of the Circuit Court of [County] County, Arkansas, on
   [day, date] at [time], at [courthouse address / remote link if
   applicable], or as soon thereafter as the matter may be heard.

   [Signature block — Ark. Bar No. ##### for an attorney; "Pro Se"
   with no bar number for a self-represented filer]

                      CERTIFICATE OF SERVICE
   [served on all parties per Ark. R. Civ. P. 5 / e-service under
   Administrative Order No. 21]
```

Adapt the caption (Circuit vs. District; the correct division line) and
fill in the date only **after** you have actually coordinated it with
chambers.

## Before you notice a date — checklist

- [ ] Motion (and brief) **filed**; response period status known.
- [ ] **Date confirmed** with the judge's coordinator (Circuit) or
      clerk (District) — never notice a date you have not cleared.
- [ ] **Format** confirmed (in person / Zoom / phone).
- [ ] Notice of Hearing **served on all parties** and filed, with a
      certificate of service — unless the court issues the setting.
- [ ] Deadline math checked so the hearing leaves room for the response
      / reply windows — see `ar-deadlines`.

## Composition

- For preparing the motion to be heard: `ar-draft-motion`,
  `ar-draft-note` (the Notice)
- For the hearing itself (argument, etiquette, remote practice):
  `ar-hearings`
- For deadline arithmetic around the setting: `ar-deadlines`
- For the caption + signature baseline: `ar-statewide-format`
- For venue-specific scheduling practice: `ar-pulaski`, `ar-benton`,
  `ar-washington`, `ar-district-courts`, `ar-county-courts`

## References

- `ar-law-references` hosts the Ark. R. Civ. P. 78 motion-practice text,
  the circuit administrative plans / local rules that govern
  scheduling, and the District Court Rules' return-date practice.
