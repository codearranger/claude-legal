---
name: ar-family-court
description: >
  This skill should be used to choose a venue and handle filing
  mechanics for an Arkansas divorce / domestic-relations or juvenile
  case. Arkansas has no separate family court — domestic-relations
  matters are heard in the Domestic Relations Division of Circuit
  Court, and paternity / dependency-neglect / FINS / termination of
  parental rights are heard in the Juvenile Division of Circuit Court.
  Use it for where to file a divorce in Arkansas, the
  domestic-relations-vs-juvenile routing, residency and venue, intake,
  attorney ad litem and mediation expectations, AOC domestic-relations
  forms, and self-represented divorce. Triggers include "where do I
  file for divorce in Arkansas", "Arkansas divorce venue", "Arkansas
  domestic relations division", "circuit court divorce Arkansas",
  "Arkansas residency divorce 60 days", "Ark. Code Ann. 9-12-307",
  "Arkansas paternity court", "Arkansas juvenile court", "FINS
  Arkansas", "dependency neglect Arkansas", "termination of parental
  rights Arkansas", "attorney ad litem Arkansas", "Arkansas divorce
  forms", "uncontested divorce Arkansas", "pro se divorce Arkansas".
  A venue skill that defers substantive Title 9 law to ar-family-law
  and document form to ar-statewide-format.
version: 0.1.0
---

# Arkansas Family Court — Circuit Court Divisions

> **NOT LEGAL ADVICE.** These notes describe the venue's procedural
> mechanics as a drafting aid, not legal advice. Divorce, custody,
> and juvenile decisions have lasting consequences for property,
> children, and finances. Strongly consider consulting a licensed
> Arkansas family-law attorney even on an agreed or "simple" divorce.
> Local rules and judge-specific practices change; verify with the
> clerk and the current local rules and administrative plan before
> relying on anything here.

Arkansas has **no separate statewide "family court" trial court**.
Since **Amendment 80** (adopted Nov. 2000, effective July 1, 2001)
unified Arkansas's trial courts, divorce and the parenting / support /
property matters incident to a marriage are heard in the
**Domestic Relations Division of Circuit Court**, and paternity,
dependency-neglect, FINS, and termination-of-parental-rights matters
are heard in the **Juvenile Division of Circuit Court**. Both
"divisions" are administrative subject-matter divisions of the single
general-jurisdiction **Circuit Court** — not separate courts — and a
circuit judge may sit in any division.

This skill covers where to file, how the domestic-relations and
juvenile dockets are routed, and the filing mechanics. For the
substantive law (grounds, equitable distribution, child support,
custody, alimony, covenant marriage, protection orders), see
`ar-family-law`. For document form, see `ar-statewide-format`.

## Amendment 80 — one unified Circuit Court

Before Amendment 80, Arkansas divorce was an **equity** matter heard
in the former **Chancery Court**. Amendment 80 **merged Chancery,
Probate, and Circuit Courts into a single Circuit Court** of general
jurisdiction, organized by Supreme Court administrative plan into
five subject-matter divisions: **criminal, civil, probate, domestic
relations, and juvenile**. Practical consequences:

- File a divorce in **Circuit Court**, designating the **Domestic
  Relations Division** in the caption where local practice expects it.
- There is no longer a "chancery" caption or a separate equity clerk;
  the **Circuit Clerk** is the clerk for all divisions.
- Law and equity are unified, so the court may grant both legal and
  equitable relief in the same domestic case.

## What this venue handles

| Matter | Division / forum | Skill |
|---|---|---|
| Divorce (fault or 18-month-separation no-fault) | **Domestic Relations Division**, Circuit Court | this skill + `ar-family-law` |
| Covenant-marriage divorce / separation | Domestic Relations Division | this skill + `ar-family-law` |
| Annulment / legal separation (separate maintenance) | Domestic Relations Division | this skill + `ar-family-law` |
| Equitable distribution of property; alimony | Domestic Relations Division (with the divorce) | `ar-family-law` |
| Custody / support **incident to divorce** or between **married** parents | Domestic Relations Division | `ar-family-law` |
| Post-decree modification (custody, support, alimony) | Domestic Relations Division (the court that entered the decree) | `ar-family-law` |
| Order of protection (Domestic Abuse Act) | Circuit Court | this skill + `ar-family-law` |
| **Paternity** / parentage of a child of **unmarried** parents | **Juvenile Division**, Circuit Court | this skill + `ar-family-law` |
| **Dependency-neglect** | Juvenile Division | this skill |
| **FINS** (Families in Need of Services) | Juvenile Division | this skill |
| **Termination of parental rights (TPR)** | Juvenile Division | this skill |
| Juvenile delinquency | Juvenile Division | this skill |

> Routing rule: divorce and married-parent / divorce-incident
> parenting and support go to the **Domestic Relations Division**.
> Paternity for children of never-married parents, and the
> child-welfare matters (dependency-neglect, FINS, TPR, delinquency)
> under the **Arkansas Juvenile Code (Ark. Code Ann. Title 9,
> ch. 27)**, go to the **Juvenile Division**.

## Residency and venue

Arkansas imposes a **statutory residency requirement** for divorce
keyed to **Ark. Code Ann. § 9-12-307**: a period of residence before
filing and a longer period before the final decree may be entered.
The exact day/month counts are volatile — see
`../ar-family-law/references/dissolution.md`. Confirm the residency
allegation in the complaint and be prepared to **corroborate**
residence (see `ar-family-law`).

- **Venue (county).** Domestic-relations venue is generally proper in
  the county where the plaintiff resides (and, in some configurations,
  where the defendant resides). Confirm the proper county before
  filing; filing in the wrong county can draw a motion to transfer.
- **Jurisdiction over children (UCCJEA).** If there are minor
  children, confirm Arkansas is the child's **home state** under the
  **UCCJEA, Ark. Code Ann. § 9-19-101 et seq.**, and include the
  UCCJEA jurisdictional allegations / affidavit. See
  `../ar-family-law/references/uccjea-uifsa.md`.

## Filing mechanics — domestic relations

### 1. Confirm jurisdiction, residency, and venue

Verify subject-matter jurisdiction (Circuit Court, Domestic Relations
Division), the **§ 9-12-307 residency** allegation, proper county
venue, and UCCJEA home-state jurisdiction over any children.

### 2. Prepare the complaint and required attachments

- **Complaint for Divorce** (or for absolute divorce / divorce from
  bed and board) stating the **ground(s)** under **Ark. Code Ann.
  § 9-12-301** — commonly **general indignities** or the
  **18-month continuous separation** no-fault ground.
- Plan to satisfy the **corroboration-of-grounds-and-residence**
  requirement, which is distinctive to Arkansas (see `ar-family-law`).
- If there is a **minor child**, prepare the **child-support
  calculation** under the income-shares **Administrative Order No. 10**
  Family Support Chart, and any required custody / parenting affidavit.
- For an agreed divorce, a written **property-settlement / separation
  agreement** resolving property, debts, support, and parenting.
- Confirm whether the county's administrative plan or local rule
  requires a **parenting affidavit, financial affidavit/disclosure**,
  or a **mandatory parenting class** in cases with minor children.

Use `ar-statewide-format` for the Ark. R. Civ. P. 10 caption, the
Rule 11 signature, and the **Administrative Order No. 19** redaction /
certificate of compliance. Use `ar-draft-motion` /
`ar-draft-declaration` / `ar-draft-order` for the documents and
`ar-family-law` for the substance.

### 3. File with the Circuit Clerk and pay (or waive) the fee

- File with the **Circuit Clerk** of the proper county.
- Filing fees vary by county; a qualifying self-represented filer may
  seek to proceed **in forma pauperis** (affidavit of indigency).
  Confirm the current form and amount with the clerk.
- **E-filing** is statewide through **eFlex** under **Administrative
  Order No. 21** (the Contexte case-management system); some counties
  mandate it and some accept paper. Confirm the venue's platform with
  `ar-pulaski`, `ar-benton`, `ar-washington`, or `ar-county-courts`.

### 4. Serve the defendant

Serve the summons and complaint under **Ark. R. Civ. P. 4**. The
answer is generally due within a set period after service (longer for
nonresident / out-of-state defendants) — see `ar-first-30-days` and
`ar-deadlines`. For an agreed divorce, the defendant may sign a
**waiver of service** / entry of appearance and the settlement
agreement rather than be formally served; confirm the current
mechanics.

### 5. Observe the waiting period before the decree

Arkansas imposes a **waiting period from filing before a divorce
decree may be entered**. The exact count is volatile — see
`../ar-family-law/references/dissolution.md` — and is computed with
`ar-deadlines`. Even an uncontested divorce cannot be finalized before
the period runs and the grounds and residence are corroborated.

## Filing mechanics — juvenile division (Title 9, ch. 27)

The **Juvenile Division** hears matters under the **Arkansas Juvenile
Code, Ark. Code Ann. Title 9, ch. 27**:

- **Paternity / parentage** of children of unmarried parents
  (establishing the parent-child relationship, then custody and
  support under the same Title 9 substantive framework).
- **Dependency-neglect** — petitions (typically by the Department of
  Human Services) alleging a juvenile is dependent or neglected, with
  a probable-cause hearing, adjudication, disposition, and review /
  permanency hearings.
- **FINS — Families in Need of Services** — petitions addressing
  truancy, runaway, and ungovernable-behavior situations.
- **Termination of parental rights (TPR)** — a separate, high-stakes
  petition with a heightened **clear-and-convincing** burden; an
  **attorney ad litem** for the child is required.
- **Delinquency** — juvenile offenses.

> Juvenile cases are confidential and procedurally distinct from
> domestic-relations divorce practice. Captions, parties (often
> styled **In re** the juvenile, or **Petitioner/Respondent**),
> service, and hearing structure differ. Verify the controlling
> Title 9 ch. 27 provisions and the local juvenile administrative
> plan before filing, and consult counsel — the consequences
> (especially in TPR) are severe and often irreversible.

## Attorney ad litem and the court-appointed advocate

Arkansas family and juvenile practice frequently involves a
court-appointed **attorney ad litem** to represent the **best interest
of a child**:

- In **dependency-neglect and TPR** cases an attorney ad litem for
  the juvenile is **mandatory**.
- In **contested custody** cases, a circuit court **may appoint** an
  attorney ad litem for the child under the Title 9 custody framework
  and the Supreme Court's attorney-ad-litem standards.
- Some courts also use **CASA** (Court Appointed Special Advocate)
  volunteers in child-welfare cases.

Confirm whether the court has appointed (or will appoint) an attorney
ad litem and how fees are allocated; this affects discovery,
disclosures, and the parties' communications with the child.

## Mediation expectations

**Mediation requirements vary by county and judge.** Many Arkansas
circuit courts **order mediation** in contested divorce and custody
cases (often before a final hearing will be set), and the courts
maintain rosters of approved / certified mediators under the Arkansas
Alternative Dispute Resolution Commission. Confirm the venue's
mediation expectation, any required pre-mediation disclosures, and
cost-sharing with the local administrative plan and the relevant venue
skill. Mediation is generally **not** appropriate where there is an
active order of protection or a history of domestic abuse — flag that
to the court.

## Self-represented (pro se) divorce intake

- The Arkansas Judiciary publishes **approved domestic-relations
  forms** through the Administrative Office of the Courts and
  **arcourts.gov** (and the Arkansas Legal Services / ARLegalServices
  self-help portal), including divorce packets and protection-order
  petitions. Confirm the current AOC packet and whether the chosen
  county accepts it.
- Self-represented filers designate themselves clearly in the
  signature block (no Arkansas bar number) — write **"Pro Se"** or
  **"Self-Represented"**; see `ar-pro-se`.
- Clerks and self-help resources can explain **procedure** but cannot
  give legal advice. Encourage consultation with a licensed Arkansas
  family-law attorney, especially where there are minor children,
  retirement assets, real property, a business, a covenant marriage,
  domestic abuse, or any disputed issue.

## Composition

- For the substantive law (grounds, corroboration, property,
  child support, custody, alimony, covenant marriage, UCCJEA/UIFSA,
  protection orders): `ar-family-law`
- For format (Rule 10 caption, Rule 11 signature, Administrative
  Order No. 19 redaction): `ar-statewide-format`
- For the specific county / clerk and e-filing platform:
  `ar-pulaski`, `ar-benton`, `ar-washington`, `ar-county-courts`
- For pro se conventions and AOC forms: `ar-pro-se`
- For the answer and first-30-days response: `ar-first-30-days`
- For the residency / waiting period and other deadlines:
  `ar-deadlines`
- For assembling and preflighting the filing packet: `ar-file-packet`
- For scheduling and hearings: `ar-schedule-hearing`, `ar-hearings`
- For the proposed decree: `ar-draft-order`, `ar-submit-order`

## References

- `../ar-family-law/references/dissolution.md` — residency
  (§ 9-12-307), the waiting period, and corroboration
- `../ar-family-law/references/uccjea-uifsa.md` — UCCJEA home-state
  jurisdiction over children (§ 9-19-101 et seq.)
- `../ar-family-law/references/protection-orders.md` — Domestic Abuse
  Act petitions (§ 9-15-101 et seq.)

Substantive Title 9 references for the matters this venue hears live
under `ar-family-law/references/`.
