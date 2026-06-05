---
name: ar-benton
description: >
  This skill should be used when the user is drafting or filing in
  Benton County Circuit Court (Bentonville, 19th Judicial Circuit West)
  — the fast-growing Northwest Arkansas trial court. Triggers include
  "Benton County Circuit Court", "Bentonville circuit court", "19th
  Judicial Circuit West", "file in Bentonville", "Benton County
  Courthouse", "04CV docket number", "Benton County division", "eFlex
  Benton County", and questions about the Benton administrative plan,
  division assignment, chambers copies, or working copies. Covers venue
  mechanics, the five subject-matter divisions, the Arkansas county-
  coded case-number format, and e-filing through eFlex/Contexte. Layers
  on top of `ar-statewide-format`.
version: 0.1.0
---

# Benton County Circuit Court (19th Judicial Circuit West, Bentonville)

> **NOT LEGAL ADVICE.** These notes describe the venue's procedural
> mechanics as a drafting aid, not legal advice. Local rules,
> administrative plans, and judge-specific practices change; verify
> with the clerk and the current administrative plan before relying on
> anything here.

Benton County is one of the two large, **fast-growing Northwest
Arkansas** counties (home to the Walmart corporate headquarters) and
its Circuit Court is the **19th Judicial Circuit West**. The court sits
at the **Benton County Courthouse** in **Bentonville**. Its civil and
domestic-relations caseload has risen sharply with the region's growth.
This skill is a venue overlay — apply the `ar-statewide-format` baseline
(caption, numbered paragraphs, Rule 11 signature, line numbering,
footer, Administrative Order No. 19 redaction) and add the Benton
specifics below.

## Court structure and divisions

Under Amendment 80 (effective July 1, 2001), Benton County has a single
**Circuit Court** of general jurisdiction, organized by the Supreme
Court's administrative plan into the **five subject-matter divisions**:
**criminal, civil, probate, domestic relations, and juvenile**. These
are administrative divisions of one court; a circuit judge may be
assigned to any division. The 19th Judicial Circuit is divided into a
**West** subdistrict (Benton County) and an **East** subdistrict
(Carroll County) — Benton County matters are filed in the West. Confirm
the current judge assignments and division structure through the
administrative plan at **arcourts.gov**.

## Case-number format

Benton County filings carry the Arkansas county-coded docket format.
The **county number for Benton is 04**, so a civil case number reads
`04CV-[yy]-[####]` (e.g., `04CV-25-1234`), with `CV` for the civil case
type, `DR` for domestic relations, `PR` for probate, and so on. The
clerk assigns and stamps the number at filing — leave it blank on an
initial complaint and populate it on every subsequent paper. Caption
the court as `IN THE CIRCUIT COURT OF BENTON COUNTY, ARKANSAS` with the
appropriate division line.

## Filing and e-filing

Benton County files through the statewide **eFlex** electronic-filing
system on the **Contexte** case-management platform (Administrative
Order No. 21). Confirm at filing time whether e-filing is mandatory for
your case type, the document-type codes the system expects, and that
each PDF carries the **Administrative Order No. 19** redaction and
certificate of compliance. The Benton County Circuit Clerk's office in
Bentonville is the point of contact for filing and case look-up.

## Chambers copies / working copies and scheduling

Whether a judge requires a **chambers copy** of motion papers, the
format and timing, and how hearings are set are governed by the 19th
Judicial Circuit West administrative plan and individual judges'
practices rather than a statewide rule. **Defer to the assigned judge's
requirements and the circuit administrative plan** — confirm with the
division clerk before relying on a chambers-copy or scheduling
assumption. See `ar-schedule-hearing` and `ar-hearings`.

## Composition

- Format baseline: `ar-statewide-format`
- Limited-jurisdiction / small-claims / eviction matters:
  `ar-district-courts`
- Other counties' Circuit Courts (including Washington County, the
  other large NW Arkansas county): `ar-washington`, `ar-county-courts`
- Subject bundles that compose with this venue: `ar-consumer-debt`,
  `ar-family-law`, `ar-landlord-tenant`, `ar-personal-injury`,
  `ar-employment`, `ar-commercial-disputes`
- Pro se conventions: `ar-pro-se`; pre-filing QC: `ar-quality-check`

## References

- `ar-law-references` — Ark. R. Civ. P., Administrative Orders, and the
  local-rules / administrative-plan directory (confirm the 19th
  Judicial Circuit West plan at arcourts.gov)
