---
name: ar-district-courts
description: >
  This skill should be used when the user is filing or defending in an
  Arkansas District Court — the limited-jurisdiction trial court that
  handles civil claims up to the statutory cap, a small-claims
  division, and unlawful-detainer (eviction) actions. It is the
  dominant consumer-debt and eviction forum in Arkansas. Triggers
  include "district court", "Arkansas district court", "small claims",
  "small claims division", "eviction", "unlawful detainer", "failure
  to vacate", "got sued for a debt in district court", "de novo appeal
  to circuit court", "appeal a district court judgment", "state
  district court", "local district court", and "default judgment
  district court". Covers the District Court / small-claims /
  unlawful-detainer jurisdiction, the State vs. Local District Court
  distinction, the Arkansas District Court Rules, and the 30-day de
  novo appeal to Circuit Court. Layers on top of `ar-statewide-format`.
version: 0.1.0
---

# Arkansas District Courts

> **NOT LEGAL ADVICE.** These notes describe the venue's procedural
> mechanics as a drafting aid, not legal advice. Local rules and
> judge-specific practices change; verify with the clerk and the
> current Arkansas District Court Rules before relying on anything here.

The **District Court** is Arkansas's limited-jurisdiction trial court
(renamed from "Municipal Court" by Amendment 80, effective July 1,
2001). It is **the high-volume forum where most consumer-debt suits and
nearly all evictions are filed** — the venue the `ar-consumer-debt` and
`ar-landlord-tenant` bundles compose with most often. This skill is a
venue overlay — apply the `ar-statewide-format` baseline and add the
District Court specifics below.

## Jurisdiction

District Courts exercise **limited civil jurisdiction up to a statutory
dollar cap**, with a separate **small-claims division** capped at a
lower figure, plus a steady docket of **unlawful-detainer / eviction**
matters. They also handle misdemeanors and traffic. (Keep the exact
current dollar caps — the general civil ceiling under Ark. Code Ann.
§ 16-17-704 and the small-claims ceiling — in `ar-law-references`; do
not hard-code the figures here, as the legislature adjusts them.)

- **General civil division** — contract, debt-collection, and other
  civil claims up to the statutory cap. Pleadings follow the Arkansas
  District Court Rules supplemented by Ark. R. Civ. P.; an answer and
  defenses are required to avoid a default.
- **Small-claims division** — a streamlined, lower-cap track designed
  for self-represented litigants. There are restrictions on attorney
  representation and on who may bring claims (for example, limits on
  assignees and certain corporate/collection-entity plaintiffs). The
  small-claims rules are simplified and informal. Confirm the current
  cap and the representation/assignee restrictions in
  `ar-law-references`.
- **Unlawful detainer / eviction** — the civil eviction track runs
  through District Court (see `ar-landlord-tenant` for the substantive
  notice-and-writ framework, including the civil unlawful-detainer
  statute and Arkansas's distinctive criminal failure-to-vacate
  provision). District Court is the eviction forum of first resort.

## State vs. Local District Courts

Arkansas District Courts come in two organizational forms:

- **State District Courts** — district courts staffed by full-time
  state-paid district judges, generally serving larger or consolidated
  districts.
- **Local District Courts** — district courts whose judges are funded
  locally (by the city or county), often part-time, serving smaller
  jurisdictions. Some small cities lacking a district court instead
  have a **City Court**.

The distinction affects staffing, hours, and sometimes scheduling, but
both operate under the same **Arkansas District Court Rules**. Confirm
which form serves the relevant city/county and its filing hours through
the clerk or **arcourts.gov**.

## Governing rules and pleading format

District Court practice is governed by the **Arkansas District Court
Rules** (formerly the Inferior Court Rules) supplemented by the
**Arkansas Rules of Civil Procedure** where the District Court Rules do
not otherwise provide. Caption District Court papers as `IN THE
DISTRICT COURT OF [CITY/DISTRICT], [COUNTY] COUNTY, ARKANSAS`. Apply the
`ar-statewide-format` conventions for numbered paragraphs, the Rule 11
signature block (`Ark. Bar No.` / `Pro Se`), the certificate of
service, and the Administrative Order No. 19 redaction. District Court
procedure is more streamlined than Circuit Court; verify service,
answer, and default specifics in `ar-law-references`.

## De novo appeal to Circuit Court

A party aggrieved by a District Court judgment appeals to **Circuit
Court for a trial de novo** — the Circuit Court hears the matter anew
rather than reviewing the District Court record for error. The appeal
is taken within a **short deadline** (a 30-day window under the
District Court Rules / Ark. R. Civ. P.; confirm the exact day count and
the record-filing mechanics in `ar-law-references`). The de novo
posture is strategically important: it gives a defendant who lost (or
defaulted) below a fresh forum, with full Circuit Court procedure
(including discovery) available on appeal. See `ar-county-courts` and
the flagship venue skills for the receiving Circuit Court, and
`ar-post-judgment` / `ar-first-30-days` for the mechanics.

## Composition

- Format baseline: `ar-statewide-format`
- The Circuit Court that hears de novo appeals: `ar-pulaski`,
  `ar-benton`, `ar-washington`, `ar-county-courts`
- Subject bundles that compose with this high-volume forum:
  `ar-consumer-debt` (debt-collection defense), `ar-landlord-tenant`
  (eviction defense)
- Pro se conventions: `ar-pro-se`; pre-filing QC: `ar-quality-check`

## References

- `ar-law-references` — Arkansas District Court Rules, Ark. R. Civ. P.,
  the civil and small-claims jurisdictional caps (Ark. Code Ann.
  § 16-17-704 and the small-claims provision), and the de novo appeal
  day count
