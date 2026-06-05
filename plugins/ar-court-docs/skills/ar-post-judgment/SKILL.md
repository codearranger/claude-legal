---
name: ar-post-judgment
description: >
  Use when navigating post-judgment procedure in an Arkansas civil
  case. Triggers include "Ark. R. Civ. P. 59 new trial", "motion for
  new trial Arkansas", "Ark. R. Civ. P. 60", "set aside default
  judgment Arkansas", "vacate a judgment Arkansas", "Rule 60 90 days",
  "Arkansas garnishment", "wage garnishment exemption Arkansas",
  "claim of exemption", "Arkansas homestead exemption", "Arkansas
  personal property exemption", "writ of execution", "supplemental
  proceedings", "satisfaction of judgment Arkansas", "how long does an
  Arkansas judgment last", "revive a judgment", "scire facias",
  "appeal District Court de novo". Covers Ark. R. Civ. P. 59 (new
  trial) and Rule 60 relief — flagging the distinctive 90-day Rule
  60(a) window versus the narrower Rule 60(c) grounds after 90 days —
  execution and garnishment under Ark. Code Ann. Title 16, the
  constitutional and statutory exemption framework, satisfaction, and
  the 10-year judgment life with scire facias revival.
version: 0.1.0
---

# Arkansas Post-Judgment Procedure

> **NOT LEGAL ADVICE.** This skill addresses procedure once an Arkansas
> judgment has been entered. Verify every step — and every dollar
> figure and day count — against current law before filing or
> responding.

Use this skill alongside `ar-statewide-format` when the case is **past
judgment** — whether you are attacking the judgment, defending against
collection, or collecting on it.

## Two paths after judgment

1. **Attack the judgment** — Ark. R. Civ. P. 59 (new trial / to alter
   or amend), Ark. R. Civ. P. 60 relief from judgment or order, or
   appeal (including the **de novo appeal** from District Court to
   Circuit Court).
2. **Collect or resist collection** — execution and garnishment,
   exemptions, and satisfaction of judgment.

## Attacking the judgment

### Ark. R. Civ. P. 59 — new trial / motion to alter or amend

Rule 59 motions (new trial on the enumerated grounds, or to alter or
amend the judgment) must be filed within a short period after entry —
**confirm the current day count in `ar-deadlines`** and calendar it the
moment judgment is entered. A Rule 59 motion that is not ruled on
within the time the rule allows may be **deemed denied** by operation
of the rule, which starts the appeal clock — watch this trap.

> A timely post-trial motion can affect when the time to appeal begins
> to run. Do **not** assume the appeal deadline is measured only from
> entry of judgment — confirm the interaction in `ar-deadlines` and the
> appellate rules before relying on any date.

### Ark. R. Civ. P. 60 — relief from judgment or order

Arkansas Rule 60 has a **distinctive two-tier structure** that is the
single most important thing to get right:

> ⚠ **The Rule 60(a) 90-day window vs. the narrower Rule 60(c) grounds.**
> Under **Ark. R. Civ. P. 60(a)**, the court has broad power to
> **modify or vacate a judgment, decree, or order to correct errors or
> mistakes or to prevent the miscarriage of justice — but only within
> NINETY (90) DAYS of having it filed/entered of record.** Once that
> 90-day window closes, the court may set aside the judgment **only**
> on the **narrower, enumerated grounds of Ark. R. Civ. P. 60(c)** (for
> example, fraud, a clerical misprision, a void judgment, newly
> discovered evidence the party could not have discovered in time,
> service defects, etc. — verify the exact grounds in
> `ar-law-references`). **Calendar the 90-day line immediately.**

Practical consequences:

- **Within 90 days:** Rule 60(a) gives the court wide latitude to fix
  the judgment. This is the friendliest window — move fast.
- **After 90 days:** you must fit one of the specific Rule 60(c)
  grounds. Generic "the court got it wrong" arguments will not suffice.
- **Setting aside a default judgment** is the most common
  post-judgment use, especially in consumer debt-buyer cases where
  service was defective or the defendant never received notice. Frame
  the motion under the applicable Rule 60 provision (a 60(c) ground
  such as a void judgment / defective service if you are past 90 days)
  and pair it with a **meritorious defense** (chain of title, statute
  of limitations, collection-agency-licensing standing — see
  `ar-consumer-debt`). Default judgments are also governed by **Ark. R.
  Civ. P. 55**, which supplies its own set-aside standard ("good cause
  shown") — confirm which provision controls your facts.

### Appeal — and the District Court de novo route

- **Circuit Court final judgments** are appealed to the **Arkansas
  Court of Appeals** (or Supreme Court) under the **Arkansas Rules of
  Appellate Procedure–Civil**. The notice-of-appeal deadline runs from
  entry of the final judgment (or from disposition of a timely
  post-trial motion). **Verify the current appellate deadline** before
  relying on any number.
- **District Court judgments** are appealed to **Circuit Court for a
  trial de novo** — the case is heard anew under the full Ark. R. Civ.
  P. (so formal discovery becomes available). The appeal window is
  **short**; confirm the current day count and the record-lodging
  mechanics in `ar-deadlines` and `ar-district-courts`, and calendar it
  immediately.

## Collecting / resisting collection

### Writ of execution and garnishment — Ark. Code Ann. Title 16

A money judgment is enforced by a **writ of execution** against
non-exempt property and by **garnishment** of wages or non-wage assets
(bank accounts, etc.). The garnishment statutes, the garnishee's duty
to answer, and the notice-to-the-debtor requirements are found in **Ark.
Code Ann. Title 16** (judgments and their enforcement). **Verify the
current garnishment procedure and the wage-withholding formula** before
relying on any figure — the federal Consumer Credit Protection Act
garnishment cap (15 U.S.C. §§ 1671–1677) sets a floor of protection
that applies in Arkansas.

### Exemptions — constitutional + statutory

A judgment debtor may protect certain property from execution and
garnishment through **exemptions**, which in Arkansas come from **both
the Arkansas Constitution and the statutes**:

- **Homestead exemption** — the Arkansas Constitution protects the
  debtor's homestead (with acreage and value limits that differ for
  urban vs. rural property). The constitutional homestead is a
  cornerstone Arkansas debtor protection.
- **Personal-property exemption** — the Constitution and statutes
  protect specified personal property up to a value cap (and a debtor
  may elect between the state and federal exemption schemes in some
  contexts).
- **Wages / earnings** — protected subject to the federal CCPA floor.
- **Categorically protected funds** — e.g., **Social Security** under
  42 U.S.C. § 407, and certain public benefits and retirement accounts.

> ⚠ **Do not rely on a specific exemption dollar amount or acreage
> figure from memory.** The Arkansas constitutional and statutory
> exemption values (homestead acreage/value, personal-property caps,
> wage protection) are fixed by the Constitution and Code and are the
> kind of figure that drifts. **Look up the current amounts in
> `ar-law-references`** before asserting or relying on them.

**Claiming an exemption** generally requires the debtor to file a
written **claim of exemption** (a schedule of the property claimed
exempt) with the issuing court within the period the garnishment /
execution papers specify, after which the court resolves the claim.
Confirm the current procedure and deadline for the venue, and act
promptly — the window is short.

### Supplemental proceedings (debtor's examination)

A judgment creditor who cannot locate assets may use **supplemental
proceedings** to compel the debtor to appear and answer under oath
about income and property (a "debtor's examination"), and may serve
written discovery in aid of execution. Confirm the current procedure
and the service requirements before invoking it.

### Satisfaction of judgment

When a judgment is paid in full, a **satisfaction** should be entered
of record so the judgment no longer encumbers the debtor.

- The judgment creditor ordinarily files a **Satisfaction of Judgment**
  with the clerk.
- If the creditor refuses after payment, the debtor may move the court
  to enter satisfaction with proof of payment.
- Verify any statutory penalty for a creditor's failure to enter
  satisfaction after demand.

## Judgment life and scire facias revival

An Arkansas money judgment is a **lien** with a statutory life — a
judgment is generally enforceable for **ten (10) years** and may be
**revived** before it expires by **scire facias** (Ark. Code Ann.
§ 16-65-501 / § 16-56-114). Key points:

- The **10-year life** runs from entry (and the lien's effect on real
  property depends on where the judgment is recorded). Confirm the
  current computation and any renewal/re-recording mechanics in
  `ar-law-references`.
- **Scire facias revival** is the mechanism to revive a dormant or
  expiring judgment — it must be sought within the statutory revival
  period. Calendar the expiration if you are a creditor; if you are a
  debtor, a stale, unrevived judgment may no longer be enforceable —
  verify before assuming either way.

## Common pro se post-judgment scenarios

1. **Default judgment in a debt-buyer case** — if within 90 days, Rule
   60(a) gives the court broad power to vacate; if past 90 days, fit a
   Rule 60(c) ground (void judgment / defective service) plus a
   meritorious defense (chain of title, SOL, collection-agency
   licensing). See `ar-consumer-debt`.
2. **District Court judgment you want to challenge** — if within the
   appeal window, the de novo appeal to Circuit Court is usually the
   better route than a post-judgment motion in District Court. See
   `ar-district-courts`.
3. **Bank account garnished that holds Social Security** — assert the
   42 U.S.C. § 407 exemption and any applicable Arkansas exemption;
   file the claim within the window stated on the garnishment papers.
4. **Wage garnishment** — confirm the withholding does not exceed the
   CCPA federal cap and check the current Arkansas wage exemption.
5. **Old judgment resurfacing** — check whether the 10-year life has
   run and whether the creditor revived it by scire facias.

## Composition

- For statewide format: `ar-statewide-format`
- For drafting the motion to set aside / for new trial: `ar-draft-motion`
- For the supporting affidavit / declaration: `ar-draft-declaration`
- For debt-buyer-specific defenses (chain of title, collection-agency
  licensing): `ar-consumer-debt`
- For deadline arithmetic (the Rule 59 window, the Rule 60 90-day line,
  the de novo appeal): `ar-deadlines`
- For the District Court de novo appeal mechanics: `ar-district-courts`

## References

- `ar-law-references` hosts the Ark. R. Civ. P. 59 and 60 text (with
  the 60(a)/60(c) split), the Ark. Code Ann. Title 16 execution /
  garnishment statutes, the constitutional + statutory exemption
  figures (verify current values), the satisfaction procedure, and the
  § 16-65-501 / § 16-56-114 scire facias revival framework.
