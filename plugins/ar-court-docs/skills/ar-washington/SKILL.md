---
name: ar-washington
description: >
  This skill should be used when the user is drafting or filing in
  Washington County Circuit Court (Fayetteville / Springdale, 4th
  Judicial Circuit) — the other large Northwest Arkansas trial court,
  home to the University of Arkansas. Triggers include "Washington
  County Circuit Court", "Fayetteville circuit court", "Springdale
  circuit court", "4th Judicial Circuit", "file in Fayetteville",
  "Washington County Courthouse", "72CV docket number", "Washington
  County division", "eFlex Washington County", and questions about the
  Washington County administrative plan, division assignment, chambers
  copies, or working copies. Covers venue mechanics, the five subject-
  matter divisions, the Arkansas county-coded case-number format, and
  e-filing through eFlex/Contexte. Layers on top of `ar-statewide-format`.
version: 0.1.0
---

# Washington County Circuit Court (4th Judicial Circuit, Fayetteville)

> **NOT LEGAL ADVICE.** These notes describe the venue's procedural
> mechanics as a drafting aid, not legal advice. Local rules,
> administrative plans, and judge-specific practices change; verify
> with the clerk and the current administrative plan before relying on
> anything here.

Washington County is the second large, **fast-growing Northwest
Arkansas** county (the **Fayetteville / Springdale** metro, home to the
**University of Arkansas**), and its Circuit Court is the **4th Judicial
Circuit**. The court sits at the **Washington County Courthouse** in
**Fayetteville**. Like its Benton County neighbor, it carries a rising
civil and domestic-relations caseload. This skill is a venue overlay —
apply the `ar-statewide-format` baseline (caption, numbered paragraphs,
Rule 11 signature, line numbering, footer, Administrative Order No. 19
redaction) and add the Washington specifics below.

## Court structure and divisions

Under Amendment 80 (effective July 1, 2001), Washington County has a
single **Circuit Court** of general jurisdiction, organized by the
Supreme Court's administrative plan into the **five subject-matter
divisions**: **criminal, civil, probate, domestic relations, and
juvenile**. These are administrative divisions of one court; a circuit
judge may be assigned to any division. The 4th Judicial Circuit
comprises Washington and Madison Counties — Washington County matters
file at the Fayetteville courthouse. Confirm the current judge
assignments and division structure through the administrative plan at
**arcourts.gov**.

## Case-number format

Washington County filings carry the Arkansas county-coded docket
format. The **county number for Washington is 72**, so a civil case
number reads `72CV-[yy]-[####]` (e.g., `72CV-25-1234`), with `CV` for
the civil case type, `DR` for domestic relations, `PR` for probate, and
so on. The clerk assigns and stamps the number at filing — leave it
blank on an initial complaint and populate it on every subsequent
paper. Caption the court as `IN THE CIRCUIT COURT OF WASHINGTON COUNTY,
ARKANSAS` with the appropriate division line.

## Filing and e-filing

Washington County files through the statewide **eFlex** electronic-
filing system on the **Contexte** case-management platform
(Administrative Order No. 21). Confirm at filing time whether e-filing
is mandatory for your case type, the document-type codes the system
expects, and that each PDF carries the **Administrative Order No. 19**
redaction and certificate of compliance. The Washington County Circuit
Clerk's office in Fayetteville is the point of contact for filing and
case look-up.

## Chambers copies / working copies and scheduling

Whether a judge requires a **chambers copy** of motion papers, its
format and timing, and how hearings are set are governed by the 4th
Judicial Circuit administrative plan and individual judges' practices
rather than a statewide rule. **Defer to the assigned judge's
requirements and the circuit administrative plan** — confirm with the
division clerk before relying on a chambers-copy or scheduling
assumption. See `ar-schedule-hearing` and `ar-hearings`.

## Composition

- Format baseline: `ar-statewide-format`
- Limited-jurisdiction / small-claims / eviction matters:
  `ar-district-courts`
- The other large NW Arkansas county and the broader roll-up:
  `ar-benton`, `ar-county-courts`
- Subject bundles that compose with this venue: `ar-consumer-debt`,
  `ar-family-law`, `ar-landlord-tenant`, `ar-personal-injury`,
  `ar-employment`, `ar-commercial-disputes`
- Pro se conventions: `ar-pro-se`; pre-filing QC: `ar-quality-check`

## References

- `ar-law-references` — Ark. R. Civ. P., Administrative Orders, and the
  local-rules / administrative-plan directory (confirm the 4th Judicial
  Circuit plan at arcourts.gov)
