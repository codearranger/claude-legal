---
name: ar-draft-note
description: >
  This skill should be used to scaffold the scheduling document that
  places an Arkansas motion or matter on the court's calendar — in
  Arkansas practice this is the NOTICE OF HEARING. Triggers include
  "draft a notice of hearing in Arkansas", "how do I set my Arkansas
  motion for a hearing", "draft an Arkansas notice of hearing for my
  motion to compel", "notice of hearing for summary judgment Arkansas",
  "schedule my motion in Pulaski County Circuit Court", "get a hearing
  date for my Arkansas motion", "notice the other side of my hearing
  date". Produces a Notice of Hearing in Arkansas format identifying
  the motion, the date/time/place (or division/judge), and the manner
  of appearance, with a certificate of service. Composes with
  `ar-statewide-format` for the caption and signature, `ar-draft-motion`
  for the underlying motion, and `ar-schedule-hearing` for coordinating
  the date with the division or assigned judge.
version: 0.1.0
---

# Draft an Arkansas Notice of Hearing

> **NOT LEGAL ADVICE.** This skill scaffolds a court document as a
> drafting aid. The user — not the skill — chooses the motion type,
> theory of relief, and strategy. Verify every rule, deadline, and
> citation against current law before filing. Pair with substantive
> review by counsel where stakes warrant.

Use this skill to produce the **Notice of Hearing** — the scheduling
document that tells the court and the opposing party when and where a
motion or matter will be heard. In Arkansas Circuit Court practice, a
motion is generally not heard until it is **set** for a hearing and the
opposing party is **noticed**. The hearing date is coordinated with the
assigned division or judge (see `ar-schedule-hearing`); the Notice of
Hearing then memorializes that date and is served on all parties. The
caption, signature, and certificate of service follow
`ar-statewide-format`.

## Coordinate the date first, then notice it

In Arkansas there is **no single statewide self-scheduling rule** — how
a hearing date is obtained varies by circuit, division, and judge.
Common patterns:

- **Coordinate with chambers / the division clerk** for an available
  date and time, then file and serve the Notice of Hearing for that
  date.
- Some circuits and divisions use **motion dockets / law-and-motion
  days** on a recurring calendar; the Notice sets the matter for the
  next available docket.
- The **assigned judge's standing order or administrative plan** may
  prescribe the exact mechanism, required lead time, and whether the
  hearing is in person or remote.

Use `ar-schedule-hearing` to obtain the date by the correct mechanism
for the filing court; use this skill to draft the document once you
have a date. Confirm the **minimum notice period** the local rule or
judge requires between service of the Notice and the hearing, and
compute it with `ar-deadlines` (Rule 6(a) computation; Rule 6(d) adds
3 days for service by mail).

## Notice of Hearing structure

```
                    [Caption — see ar-statewide-format]

                       NOTICE OF HEARING

TO: [Opposing party / counsel of record], and all parties of record:

PLEASE TAKE NOTICE that [Movant]'s [exact title of the motion],
filed [date], will be brought on for hearing before the Honorable
[Judge Name], [Circuit] Judicial Circuit, [____] Division, on:

        DATE:   [day of week], [month] [day], 20[__]
        TIME:   [__:__] [a.m./p.m.]
        PLACE:  [Courtroom / Division], [County] County Courthouse,
                [address], [city], Arkansas
                [or: by remote appearance — see instructions below]

[If remote: appearance instructions / video link / call-in
information per the division's standing order.]

                                        [Signature block —
                                         see ar-statewide-format]

                       CERTIFICATE OF SERVICE
[Date, method, recipients — per ar-statewide-format and Rule 5]
```

## Drafting points

1. **Identify the motion exactly.** Use the same title as the filed
   motion (`ar-draft-motion`) so the clerk and court can match them.
2. **State date, time, and place** — or the division/judge and the
   remote-appearance instructions where the matter is heard remotely.
3. **Name the assigned judge and division** consistent with the
   circuit's case-assignment plan (see the venue overlay).
4. **Serve every party** and complete the certificate of service under
   Rule 5; registered e-filers are served through eFlex under
   Administrative Order No. 21.
5. **Respect the minimum notice period** so the opposing party has the
   time the local rule or judge requires to respond and appear.

## Composition

- For format, caption, and signature block: `ar-statewide-format`
- For coordinating the date: `ar-schedule-hearing`
- For the underlying motion: `ar-draft-motion`
- For the proposed order to bring to the hearing: `ar-draft-order`
- For computing the minimum notice period: `ar-deadlines`
- For the venue overlay (division/judge mechanics): `ar-pulaski`,
  `ar-benton`, `ar-washington`, `ar-county-courts`, `ar-district-courts`
- For hearing-day conduct: `ar-hearings`
- For pre-filing QC: `ar-quality-check`, `ar-fact-check`
- For pro se conventions: `ar-pro-se`

## References

- `references/notice-of-hearing-template.md` — annotated Notice of
  Hearing template
- `references/scheduling-mechanics.md` — coordinate-then-notice
  workflow and minimum-notice considerations by circuit/division
