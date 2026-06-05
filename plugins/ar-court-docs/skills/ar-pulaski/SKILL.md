---
name: ar-pulaski
description: >
  This skill should be used when the user is drafting or filing in
  Pulaski County Circuit Court (Little Rock, 6th Judicial Circuit) —
  the state's largest and highest-volume trial court. Triggers include
  "Pulaski County Circuit Court", "Pulaski County Courthouse", "6th
  Judicial Circuit", "Little Rock circuit court", "file in Little
  Rock", "60CV docket number", "Pulaski division assignment", "Pulaski
  domestic relations division", "Pulaski civil division", "eFlex
  Pulaski", and questions about chambers copies, working copies, or the
  Pulaski administrative plan. Covers venue mechanics, the five
  subject-matter divisions, the Arkansas county-coded case-number
  format, e-filing through eFlex/Contexte, and chambers/working-copy
  practice. Layers on top of `ar-statewide-format`.
version: 0.1.0
---

# Pulaski County Circuit Court (6th Judicial Circuit, Little Rock)

> **NOT LEGAL ADVICE.** These notes describe the venue's procedural
> mechanics as a drafting aid, not legal advice. Local rules,
> administrative plans, and judge-specific practices change; verify
> with the clerk and the current administrative plan before relying on
> anything here.

Pulaski County Circuit Court is the **largest trial court in
Arkansas** and the **6th Judicial Circuit**. Sitting at the **Pulaski
County Courthouse** in **Little Rock** (the state capital), it carries
the highest civil and domestic-relations caseload in the state. This
skill is a venue overlay — apply the `ar-statewide-format` baseline
(caption, numbered paragraphs, Rule 11 signature, line numbering,
footer, Administrative Order No. 19 redaction) and add the Pulaski
specifics below.

## Court structure and divisions

Under Amendment 80 (effective July 1, 2001), Pulaski County has a
single **Circuit Court** of general jurisdiction, organized by the
Supreme Court's administrative plan into the **five subject-matter
divisions**: **criminal, civil, probate, domestic relations, and
juvenile**. These are administrative divisions of one court — a circuit
judge may be assigned to sit in any of them. The 6th Judicial Circuit
seats a large bench of circuit judges, each assigned to a division
under the circuit's administrative plan.

- **Civil division** — consumer-debt suits, contract and tort actions,
  commercial disputes, and limited-jurisdiction appeals from District
  Court tried de novo.
- **Domestic relations division** — divorce, custody, support, and
  protection orders (Pulaski's domestic-relations volume is among the
  highest in the state).
- Probate, juvenile, and criminal divisions handle their respective
  dockets.

Pulaski County also includes the separate **Perry County** seat in some
historical groupings; confirm the current circuit composition and judge
assignments through the administrative plan at **arcourts.gov**.

## Case-number format

Pulaski County filings carry the Arkansas county-coded docket format.
The **county number for Pulaski is 60**, so a civil case number reads
`60CV-[yy]-[####]` (e.g., `60CV-25-1234`), where `CV` designates the
civil case type. Domestic-relations matters use the `DR` type code
(`60DR-[yy]-[####]`), probate uses `PR`, and so on. The clerk assigns
and stamps the number at filing; leave it blank on an initial complaint
and populate it on every subsequent paper. Caption the court as `IN THE
CIRCUIT COURT OF PULASKI COUNTY, ARKANSAS` with the appropriate division
line (e.g., `CIVIL DIVISION`).

## Filing and e-filing

Pulaski County files through the statewide **eFlex** electronic-filing
system on the **Contexte** case-management platform (Administrative
Order No. 21). Confirm at filing time whether e-filing is mandatory for
your case type and document, the document-type codes the system
expects, and that each PDF carries the **Administrative Order No. 19**
redaction and certificate of compliance. The Pulaski County Circuit
Clerk's office is the point of contact for filing questions and case
look-up.

## Chambers copies / working copies

Whether a judge requires a **chambers copy** (a courtesy paper or
electronic copy of motion papers delivered to the assigned division),
and the format and timing for it, is set by the circuit's
administrative plan and individual judges' practices rather than a
statewide rule. **Defer to the assigned judge's requirements and the
6th Judicial Circuit administrative plan** — do not assume a chambers
copy is or is not required. Confirm with the division clerk before a
motion hearing. See `ar-schedule-hearing` and `ar-hearings`.

## Hearings and scheduling

Hearing-setting practice (whether the court sets matters on its own
motion, whether parties request settings through the division clerk or
a court coordinator, and remote-appearance availability) is
division-specific. Coordinate through the assigned division and confirm
the current administrative-plan procedure. See `ar-hearings` and
`ar-schedule-hearing`.

## Composition

- Format baseline: `ar-statewide-format`
- Limited-jurisdiction / small-claims / eviction matters that would
  instead be filed in (or appealed from) District Court:
  `ar-district-courts`
- Other counties' Circuit Courts: `ar-county-courts`
- Subject bundles that compose with this venue: `ar-consumer-debt`,
  `ar-family-law`, `ar-landlord-tenant`, `ar-personal-injury`,
  `ar-employment`, `ar-commercial-disputes`
- Pro se conventions: `ar-pro-se`; pre-filing QC: `ar-quality-check`

## References

- `ar-law-references` — Ark. R. Civ. P., Administrative Orders, and the
  local-rules / administrative-plan directory (confirm the 6th Judicial
  Circuit plan at arcourts.gov)
