---
name: wa-kcsc
description: >
  This skill should be used when drafting or filing civil documents in the
  King County Superior Court (KCSC) — the general-jurisdiction trial court
  for King County, sitting at the King County Courthouse in Seattle and
  the Maleng Regional Justice Center (MRJC) in Kent. Triggers include
  "King County Superior Court", "KCSC", "MRJC" / "Maleng Regional Justice
  Center", "Seattle case assignment area" / "Kent case assignment area",
  "case schedule" / "case information cover sheet" / "case assignment
  designation", "working copies to the judge", "note for civil motion
  calendar in King County Superior Court", "Ex Parte via the Clerk", or a
  King County superior-court cause number (e.g., "25-2-#####-# SEA" /
  "... KNT"). For the King County *District* Court (limited jurisdiction,
  ≤ $100k) use the `wa-kcdc` skill; for other counties' superior/district
  courts use `wa-county-courts`. Layer this on top of
  `wa-statewide-format`, and consult `wa-law-references` for the King
  County LCR text and the statewide CR / ER.
version: 0.1.0
---

# King County Superior Court

Use this skill in addition to `wa-statewide-format` when a civil matter is
in the **King County Superior Court** (KCSC) — the court of general
jurisdiction for King County. KCSC hears the larger civil matters
(including debt-collection actions over the $100,000 district-court
ceiling, and any matter filed in superior court by choice), supplemental
proceedings, CR 60 motions, and appeals from the district court (RALJ).

For the King County **District** Court (limited jurisdiction, up to
$100,000) use `wa-kcdc`. For superior or district courts in other
counties use `wa-county-courts`.

> **NOT LEGAL ADVICE.** This is a drafting and procedure aid. Court
> locations, e-filing systems, working-copy submission tools, civil
> motion calendars, case-schedule deadlines, and the King County local
> rules all change without notice — verify each against the court's own
> pages and the current King County LCR before relying on it. Do not
> cache KCSC-specific values across sessions.

## Two facilities — and the case assignment area decides which

KCSC sits at two locations:

- **King County Courthouse**, 516 Third Ave, Seattle, WA 98104
  (**Seattle** case assignment area).
- **Maleng Regional Justice Center (MRJC)**, 401 Fourth Ave N, Kent, WA
  98032 (**Kent** case assignment area).

**LCR 82** governs the case assignment area. Roughly: the **Seattle**
area is King County north of I-90 (plus the cities of Seattle, Mercer
Island, Bellevue, Issaquah, North Bend, and Vashon/Maury Islands); the
**Kent** area is King County south of I-90 except the Seattle-area
cities. Verify the current boundary text in LCR 82(e) before designating.

Two consequences for every filing:

1. **Cause-number suffix.** The case number carries the assignment-area
   code (commonly shown as `SEA` or `KNT`) after the cause number. Per
   LCR 82, the Clerk **may reject** a pleading or document that doesn't
   carry the code. Copy the exact code from the case caption / the
   Clerk's confirmation — don't construct it.
2. **Case Assignment Designation.** A **Case Information Cover Sheet and
   Case Assignment Designation** form (the "CICS") is filed with the
   initial pleading certifying which area the case belongs in under
   LCR 82(e). Pull the current CICS form (civil vs. family-law versions
   exist) from the King County Superior Court Clerk's forms page.

## Caption — KCSC variant

```
   IN THE SUPERIOR COURT OF THE STATE OF WASHINGTON
            IN AND FOR THE COUNTY OF KING
```

Cause number on the right side below "No.", **including the assignment
code** (e.g., `No. 25-2-#####-# SEA`). Format follows GR 14 plus the
King County LCR — see the `wa-statewide-format` skill and LCR 7/10.

## Authoritative sources — pull current forms, calendars, and rules

These are the canonical starting points; treat anything hardcoded here as
a pointer, not ground truth:

- **King County Superior Court** —
  `https://kingcounty.gov/en/court/superior-court` — calendars,
  locations, and operations.
- **King County Superior Court Clerk (Dept. of Judicial Administration)**
  — `https://kingcounty.gov/en/dept/dja` — the **E-Filing** application,
  eRecords (case viewing), the **Submit Working Copies** tool, fee
  schedule, and current forms (including the CICS / Case Assignment
  Designation). E-filing landing:
  `https://kingcounty.gov/en/dept/dja/courts-jails-legal-system/court-forms-document-filing/filing`.
- **King County Local Civil Rules (LCR)** — on the county site
  (`https://kingcounty.gov/en/dept/dja/courts-jails-legal-system/superior-court-local-rules/local-civil-rules`)
  and at `https://www.courts.wa.gov/court_rules/` ("Superior Court Rules"
  → King County). The King County LCR is amended roughly annually
  (current set effective Sept. 1, 2025 at time of writing) — check the
  effective date. Note: the in-repo `wa-law-references/references/court-rules/`
  corpus carries the **statewide** CR / ER / etc., not the King County
  LCR; pull the LCR live.
- **King County Law Library motions guide** — `https://kcll.org/motions/`
  — practical walkthrough of noting and confirming civil motions.

**Agent behavior**: before you draft a case schedule, a note for a civil
motion, an ex parte presentation, or a working-copy cover sheet, fetch
the current form, calendar, and LCR text from the sources above.

## Case schedule — issued at filing (LCR 4)

For most civil cases, the Clerk issues an **Order Setting Civil Case
Schedule** when the case is filed. It fixes a string of deadlines —
confirmation of joinder/claims/defenses, disclosure of witnesses,
discovery cutoff, dispositive-motion cutoff, trial date, and more — keyed
to the filing date. Treat the Case Schedule as controlling alongside the
CR/CRLJ time rules; compute every date with the `wa-deadlines` skill
(and `plugins/wa-court-docs/scripts/case-calendar.py`), applying RCW
1.16.050 holidays. Some case types (e.g., certain unlawful detainer,
domestic, or probate matters) are exempt or follow a different track —
check LCR 4 for the case-type list.

## Civil motions — how they're heard

KCSC does **not** run a single county-wide "motion docket" the way the
district court does. Instead:

- **Motions in a case with an assigned judge** are noted to that judge —
  typically scheduled with the **bailiff** of the assigned department,
  on that department's motion calendar, per LCR 7 and the judge's
  posted procedures. Some categories go to the **Chief Civil**
  department.
- **Ex Parte and "without oral argument" matters** (agreed orders, many
  procedural orders, certain default and supplemental-proceeding
  matters) go through the **Ex Parte and Probate Department / Ex Parte
  via the Clerk** — submit through the Clerk's e-filing/ex parte
  process; check the current Ex Parte procedures on the DJA site.
- **Notice.** Note the motion with the notice period LCR 7 / CR 6
  require (commonly at least **9 court days** before the hearing for a
  noted civil motion served in person — confirm the current LCR 7
  timing, including the longer/shorter variants for response and reply,
  and any electronic-service adjustment).
- **Confirmation.** The moving party generally must **confirm** the
  motion (and identify whether oral argument is requested) by the
  deadline in LCR 7; an unconfirmed motion is typically **struck**.
  Confirm through the method the assigned department / the LCR
  specifies.

## Working copies are required (LCR 7)

Unlike most district courts, KCSC **requires working copies** — a
courtesy/bench copy of the motion materials delivered to the assigned
judge's department (or to Ex Parte) by the LCR 7 deadline. The Clerk
offers an electronic **"Submit Working Copies"** tool; some departments
also accept or prefer paper. Working copies must carry the working-copy
designation/coversheet and be delivered separately from the filed
documents. Pull the current working-copy instructions from the DJA site
before each motion.

## E-filing

- E-file through the **King County Superior Court Clerk's E-Filing
  application** (linked from the DJA filing page above). When an initial
  pleading is e-filed, the Clerk returns an electronic conformed copy to
  the filer.
- The **CICS / Case Assignment Designation** travels with the initial
  pleading; the **Confirmation of Service** / proof of service travels
  with anything served.
- View case documents through **eRecords**.
- Serve under **CR 5** the same day, by an authorized method, and attach
  a Declaration/Certificate of Service.

## Document set for a noted civil motion

1. **Motion** (and **Memorandum** if not self-contained)
2. **Declaration(s)** with authenticated exhibits
3. **Proposed Order**
4. **Note for Civil Motion Calendar** (assigned department) **or** the
   Ex Parte presentation materials, as applicable
5. **Working copies** of all of the above, with the working-copy
   coversheet, delivered per LCR 7
6. **Declaration/Certificate of Service**

E-file each as a separate PDF; deliver working copies through the Submit
Working Copies tool (or as the department directs).

## Appeals from the district court (RALJ)

A party appealing a King County District Court judgment goes to KCSC
under the **RALJ** (Rules for Appeal of Decisions of Courts of Limited
Jurisdiction). The notice of appeal, the RALJ deadlines, and the record
designation are governed by the RALJ (text in
`wa-law-references/references/court-rules/RALJ.md`) plus the King County
LCR's RALJ provisions — not by the RAP. Use `wa-deadlines` for the
timing.

## References

- `references/case-assignment-and-locations.md` — Seattle vs. Kent area
  boundaries (LCR 82), the two facilities, the CICS form, and the
  cause-number code
- `references/efiling-working-copies-motions.md` — e-filing through the
  Clerk, the Submit Working Copies tool, the LCR 4 case schedule, and
  LCR 7 motion noting/confirmation
