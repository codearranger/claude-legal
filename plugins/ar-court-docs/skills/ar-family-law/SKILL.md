---
name: ar-family-law
description: >
  This skill should be used for any Arkansas family-law /
  domestic-relations matter: divorce, annulment, separate maintenance,
  covenant marriage, child custody and the joint-custody presumption,
  child support, alimony, equitable distribution of property,
  paternity, relocation, UCCJEA / UIFSA, and orders of protection.
  Triggers include "divorce in Arkansas", "Arkansas divorce grounds",
  "general indignities Arkansas", "18 month separation divorce
  Arkansas", "Ark. Code Ann. 9-12-301", "Arkansas corroboration
  divorce", "Arkansas residency divorce", "Ark. Code Ann. 9-12-307",
  "covenant marriage Arkansas", "Ark. Code Ann. 9-11-801", "equitable
  distribution Arkansas", "one-half presumption Arkansas",
  "Ark. Code Ann. 9-12-315", "Arkansas child support", "income shares
  Arkansas", "Administrative Order No. 10", "Arkansas family support
  chart", "joint custody presumption Arkansas", "Act 604 Arkansas",
  "Ark. Code Ann. 9-13-101", "best interest Arkansas child", "Arkansas
  alimony", "Ark. Code Ann. 9-12-312", "Arkansas relocation parent",
  "Arkansas paternity", "Arkansas UCCJEA", "Ark. Code Ann. 9-19-101",
  "Arkansas UIFSA", "Ark. Code Ann. 9-17-101", "order of protection
  Arkansas", "domestic abuse act Arkansas", "Ark. Code Ann. 9-15-101",
  "common-law marriage Arkansas". A subject-matter bundle covering
  Title 9 of the Arkansas Code: divorce grounds and procedure
  (§ 9-12-301, § 9-12-307), covenant marriage (§ 9-11-801),
  equitable distribution with the one-half presumption (§ 9-12-315),
  the income-shares child-support model (Administrative Order No. 10),
  the Act 604 joint-custody presumption (§ 9-13-101), alimony
  (§ 9-12-312), UCCJEA (§ 9-19-101), UIFSA (§ 9-17-101), and the
  Domestic Abuse Act (§ 9-15-101).
version: 0.1.0
---

# Arkansas Family Law — Title 9

> **NOT LEGAL ADVICE.** This subject-matter bundle describes a
> procedural and substantive framework for Arkansas family-law cases,
> not legal advice and not strategic advice for any specific case.
> Family-law cases carry long-term consequences for property,
> children, and finances; outcomes are fact-specific. Strongly
> consider consulting a licensed Arkansas family-law attorney even on
> a "simple" or "agreed" divorce. The choice of grounds, claims,
> defenses, and parenting proposals belongs to the litigant (and any
> counsel the litigant retains). Verify every rule, deadline, dollar
> figure, and citation against current law before filing.

This subject-matter bundle covers the substantive Arkansas
domestic-relations law of **Title 9** of the Arkansas Code:
**divorce**, **annulment**, **separate maintenance**, **covenant
marriage**, **equitable distribution**, **child support**,
**custody and parenting**, **alimony**, **paternity**, **relocation**,
**UCCJEA / UIFSA**, and **orders of protection**. It supplies the law;
the venue mechanics live in `ar-family-court` (Domestic Relations and
Juvenile Divisions of Circuit Court) and document format lives in
`ar-statewide-format`.

## Snapshot — distinctive Arkansas family-law features

- **Divorce always requires grounds — including "no-fault."** Arkansas
  has **no pure no-fault divorce**. The closest thing is the
  **18-month continuous separation** ground; otherwise the plaintiff
  must plead and prove a **fault ground** (general indignities,
  adultery, cruelty, etc.) listed at **Ark. Code Ann. § 9-12-301**.
- **Corroboration of grounds AND residence is required.** Arkansas is
  distinctive in still requiring **third-party corroboration** of the
  ground for divorce and of residence — even in many **uncontested**
  cases. A bare admission by the defendant is not enough.
- **Residency and a waiting period.** Arkansas requires a statutory
  period of residence (a period before filing and a longer period
  before the decree) under **§ 9-12-307**, plus a **waiting period
  from filing before the decree may be entered**. Exact counts live
  in `references/dissolution.md`.
- **Covenant marriage.** Arkansas is **one of only three states** that
  offer **covenant marriage** (**§ 9-11-801 et seq.**) — a more
  binding marriage with **mandatory premarital counseling** and a
  **restricted set of divorce grounds**.
- **Equitable distribution with a one-half presumption.** Marital
  property is presumptively divided **one-half to each spouse** under
  **§ 9-12-315**; the court may vary that split only after weighing
  the statutory factors and explaining why an equal division would be
  inequitable. Non-marital property is returned to its owner.
- **Income-shares child support since July 1, 2020.** Arkansas
  switched from the old percentage-of-payor model to an
  **income-shares** model adopted by **Administrative Order No. 10**,
  combining both parents' incomes against the **Family Support Chart**.
- **Rebuttable joint-custody presumption (Act 604 of 2021).** In
  original custody determinations, **joint custody is presumed to be
  in the best interest of the child** under **§ 9-13-101**; the
  presumption is rebutted **only by clear and convincing evidence**
  (or by the parties' agreement or one party not seeking custody).
- **Alimony is discretionary.** Spousal support under **§ 9-12-312**
  has **no statutory formula** — it is committed to the circuit
  court's discretion under qualitative factors.
- **No common-law marriage.** Arkansas does **not** recognize
  common-law marriages contracted in Arkansas (but recognizes a
  common-law marriage valid where contracted elsewhere).

## Filing path — where a family case goes

Arkansas has **no separate family court**. Since **Amendment 80**
(2001) unified the trial courts, family matters are heard in
**Circuit Court** divisions:

| Matter | Division | Skill |
|---|---|---|
| Divorce, annulment, separate maintenance | **Domestic Relations Division** | `ar-family-court` |
| Custody / support **incident to divorce** or between **married** parents | Domestic Relations Division | `ar-family-court` |
| Covenant-marriage divorce | Domestic Relations Division | `ar-family-court` |
| Alimony; equitable distribution | Domestic Relations Division | `ar-family-court` |
| Order of protection (Domestic Abuse Act) | Circuit Court | this skill + `ar-family-court` |
| **Paternity** (children of unmarried parents) | **Juvenile Division** | `ar-family-court` |
| Dependency-neglect; FINS; termination of parental rights | Juvenile Division | `ar-family-court` |

See `ar-family-court` for the venue mechanics, residency, intake,
attorney ad litem, and the Title 9 ch. 27 juvenile matters.

## Divorce — grounds (§ 9-12-301)

Arkansas divorce grounds are enumerated at **Ark. Code Ann.
§ 9-12-301**. There is **no pure no-fault divorce** in Arkansas; the
plaintiff must plead and prove a statutory ground.

### Fault grounds

The fault grounds include, among others:

- **General indignities** — conduct rendering the complaining spouse's
  condition intolerable (the most commonly pleaded fault ground)
- **Adultery**
- **Cruel and barbarous treatment** endangering life
- **Habitual drunkenness** for one year
- **Conviction of a felony or other infamous crime**
- **Willful failure to provide** the common necessaries of life
- **Impotence**
- Indignities and other enumerated grounds

> Verify the **exact subsection numbering and the precise wording** of
> any ground at the current text of § 9-12-301 before pleading it; the
> list is periodically amended. Detail lives in
> `references/dissolution.md`.

### The 18-month-separation "no-fault" ground

Arkansas's closest analog to no-fault divorce is the ground of
**living separate and apart without cohabitation for 18 continuous
months** (**§ 9-12-301(b)**). Even on this ground, the **residence**
and the **fact of separation** generally must be **corroborated**.

## Divorce — procedure, residency, corroboration, and the waiting period

The mechanics are at **§ 9-12-307** (residency) and the surrounding
Title 9, ch. 12 provisions. Key Arkansas-distinctive points:

1. **Residency (§ 9-12-307).** Arkansas requires a statutory period of
   residence **before filing** and a longer period **before the final
   decree**. The exact day/month counts are volatile — see
   `references/dissolution.md` — and the residence must be
   **corroborated**.
2. **Corroboration of grounds and residence.** Arkansas still requires
   **independent third-party corroboration** of the ground for divorce
   and of residence. This requirement persists even in many
   **uncontested** divorces (a limited statutory relaxation may apply
   where the parties have lived separate and apart and there is no
   collusion — verify the current rule). Plan for a corroborating
   witness or affidavit. See `references/dissolution.md`.
3. **Waiting period.** A decree may not be entered until a statutory
   **waiting period from filing** has run. Compute it with
   `ar-deadlines`; the count lives in `references/dissolution.md`.
4. **Default vs. contested.** Even when the defendant defaults or
   agrees, the plaintiff must still **prove (and corroborate) grounds
   and residence** to obtain the decree — Arkansas does not grant
   divorce on the pleadings alone.

## Covenant marriage (§ 9-11-801 et seq.)

Arkansas is **one of only three covenant-marriage states**. A
**covenant marriage** under **Ark. Code Ann. § 9-11-801 et seq.** is
an opt-in, more durable form of marriage:

- The couple signs a **Declaration of Intent** to contract a covenant
  marriage and completes **premarital counseling**.
- A covenant-married couple agrees to a **restricted set of grounds**
  for divorce or separation and to **mandatory counseling** before
  seeking dissolution.
- Existing married couples may **convert** an ordinary marriage to a
  covenant marriage.

If a client is in a covenant marriage, the ordinary § 9-12-301 grounds
do **not** all apply — the available grounds are the narrower covenant
set, and the counseling prerequisite must be satisfied. See
`references/covenant-marriage.md`.

## Annulment and separate maintenance

- **Annulment** treats a marriage as **void or voidable from the
  outset** (e.g., lack of capacity, certain incurable conditions,
  fraud or force going to the essence of the marriage). It is **rare**
  and the grounds are narrow; most "I want an annulment" requests are
  actually divorces. Research the specific basis and verify the
  governing Title 9 provision before pleading annulment.
- **Separate maintenance / divorce from bed and board** lets a spouse
  obtain support and resolve issues while **remaining married**.
  Confirm the current Title 9, ch. 12 provisions.

## Equitable distribution — property (§ 9-12-315)

Arkansas is an **equitable-distribution** state, **not** a
community-property state, governed by **§ 9-12-315**. The court
follows a two-step process.

### Step 1 — Classify

Each asset and debt is classified as **marital** or **non-marital
(separate)**. Non-marital property generally includes property owned
before the marriage, gifts and inheritances to one spouse, and
property excluded by a valid agreement; it is **returned to its
owner** and not divided (though it can inform an alimony award).

### Step 2 — Divide marital property — the one-half presumption

Marital property is **presumptively divided one-half to each spouse**.
The court may make an **unequal** division **only** if it finds an
equal division would be **inequitable** after weighing the statutory
factors, and it must **state its reasons** in writing. The factors
(length of the marriage; age, health, and station of the parties;
occupation, income, and employability; estate, needs, and
contribution of each party; and others) live in
`references/property-distribution.md`.

## Child support — income-shares (Administrative Order No. 10)

Since **July 1, 2020**, Arkansas uses the **income-shares model**
adopted by the Arkansas Supreme Court's **Administrative Order
No. 10**. Both parents' incomes are combined, the **Family Support
Chart** assigns a basic support obligation for the number of children,
and that obligation is apportioned between the parents in proportion
to their incomes and adjusted for parenting time.

- **Inputs** typically include each parent's **gross income** (with
  adjustments), the **number of overnights / parenting time**,
  **work-related child-care** costs, the **health-insurance** premium
  for the child, and recurring **uninsured medical** expenses.
- A court may **deviate** from the presumptive chart amount with
  written findings of why the deviation is in the child's best
  interest.

> The chart figures, the worksheet, and the deviation criteria are set
> by **Administrative Order No. 10** and are amended periodically —
> always run the **current** official worksheet rather than relying on
> stale numbers. See `references/child-support.md`.

## Custody and parenting — the Act 604 joint-custody presumption (§ 9-13-101)

Custody is governed by **Ark. Code Ann. § 9-13-101** under the
overarching **best-interest-of-the-child** standard. The defining
modern feature is **Act 604 of 2021**:

- In an **original** custody determination there is a **rebuttable
  presumption that joint custody is in the best interest of the
  child**.
- The presumption is **rebutted only by clear and convincing
  evidence** that joint custody is **not** in the child's best
  interest (or by the parties' agreement, or where one party does not
  seek custody).
- **"Joint custody"** means an **approximate and reasonable equal
  division of time** with the child between the parents.

The court still applies the **best-interest** factors (the child's
relationship with each parent, stability and continuity, each parent's
fitness and willingness to foster the other's relationship, evidence
of domestic abuse, and the child's reasonable preference where of
sufficient maturity). **Relocation** of a custodial parent is analyzed
under Arkansas case law and the best-interest standard. Detail —
including the joint-custody presumption, the best-interest factors,
relocation, and visitation — lives in
`references/custody-and-parenting.md`.

## Alimony / spousal support (§ 9-12-312)

Spousal support is governed by **§ 9-12-312** and is **discretionary**
— Arkansas has **no alimony formula**. The court weighs qualitative
factors (the financial need of one spouse and the ability of the other
to pay; the parties' earning capacity, health, and station; the length
of the marriage; the property division; and the standard of living
during the marriage). Alimony may be **temporary (pendente lite)** or
permanent, and is generally **modifiable** on a material change of
circumstances and **terminates** on the recipient's remarriage or
either party's death (and may terminate on cohabitation — verify).
See `references/maintenance.md`.

## Paternity / parentage

Establishing **paternity** for a child of **unmarried** parents is a
**Juvenile Division** matter under the **Arkansas Juvenile Code
(Title 9, ch. 27)** — see `ar-family-court`. Paternity may be
established by acknowledgment, genetic testing, or adjudication. Once
parentage is established, **custody and support** follow the same
Title 9 substantive framework (income-shares support under
Administrative Order No. 10; best-interest custody under § 9-13-101).

## Common-law marriage

Arkansas **does not recognize common-law marriage contracted within
Arkansas**. Cohabitation and reputation, however long, do **not**
create a valid marriage in Arkansas. However, a common-law marriage
that was **validly contracted in another jurisdiction** that
recognizes it will generally be **recognized in Arkansas by comity**.
If a party asserts an out-of-jurisdiction common-law marriage, plead
and prepare to prove its validity under the law of the place where it
was formed.

## Jurisdiction over children and interstate cases

- **UCCJEA — § 9-19-101 et seq.** governs subject-matter jurisdiction
  over **custody / parenting** determinations. The child's **home
  state** generally controls. Plead the UCCJEA jurisdictional
  allegations (and any required affidavit of the child's residences)
  in the petition. See `references/uccjea-uifsa.md`.
- **UIFSA — § 9-17-101 et seq.** governs interstate **child-support**
  establishment, modification, and enforcement, including registration
  of out-of-state orders. See `references/uccjea-uifsa.md`.

## Orders of protection / Domestic Abuse Act (§ 9-15-101 et seq.)

Civil **orders of protection** for domestic abuse are governed by the
**Arkansas Domestic Abuse Act**, **Ark. Code Ann. § 9-15-101 et seq.**
A petition may be filed (often without a filing fee at the outset) by a
person in a **qualifying relationship** with the respondent; the court
may enter an **ex parte temporary order** followed by a hearing on a
**final order of protection** of statutory duration, and a final order
generally triggers a **firearm-possession prohibition / surrender**
consistent with state and federal law. Orders of protection frequently
run parallel to a divorce or paternity case; coordinate the parenting
and possession provisions across the cases. See
`references/protection-orders.md`.

## Drafting checklist

- [ ] Forum chosen correctly (Domestic Relations vs. Juvenile
      Division) per the filing-path table — see `ar-family-court`
- [ ] Ground(s) pleaded under § 9-12-301 (general indignities or the
      18-month-separation ground), **with a plan to corroborate** the
      ground and residence
- [ ] Residency alleged under § 9-12-307 and the waiting period
      calculated from filing — verify with `ar-deadlines`
- [ ] Covenant marriage screened for (restricted grounds + counseling
      if applicable) — `references/covenant-marriage.md`
- [ ] Property classified (marital vs. non-marital) before proposing a
      division; the **one-half presumption** under § 9-12-315 applied,
      with written reasons for any unequal split
- [ ] Child support run on the **current** Administrative Order No. 10
      income-shares worksheet / Family Support Chart
- [ ] Custody proposal built on the **Act 604 joint-custody
      presumption** (§ 9-13-101) and best-interest factors
- [ ] Alimony request supported by the § 9-12-312 discretionary factors
- [ ] UCCJEA / UIFSA allegations included where there is an interstate
      element
- [ ] Order-of-protection coordination handled where there is domestic
      abuse — `references/protection-orders.md`

## Composition

- For format and the Rule 10 caption: `ar-statewide-format`
- For the divorce / juvenile venue, intake, attorney ad litem, and
  AOC forms: `ar-family-court`
- For drafting the complaint / petition / motion: `ar-draft-motion`
- For sworn declarations / affidavits: `ar-draft-declaration`
- For a proposed decree / order: `ar-draft-order`, `ar-submit-order`
- For pro se conventions and self-represented intake: `ar-pro-se`
- For the residency / waiting period and other deadlines:
  `ar-deadlines`
- For hearings and oral argument: `ar-hearings`
- For citation verification: `ar-fact-check`
- For canonical Title 9 text: `ar-law-references`

## References

- `references/dissolution.md` — divorce mechanics: grounds,
  corroboration, § 9-12-307 residency, the waiting period, default vs.
  contested
- `references/property-distribution.md` — § 9-12-315 equitable
  distribution, the one-half presumption, factors, marital vs.
  non-marital
- `references/child-support.md` — Administrative Order No. 10
  income-shares model, Family Support Chart, deviation, modification
- `references/custody-and-parenting.md` — § 9-13-101 Act 604
  joint-custody presumption, best interest, relocation, visitation
- `references/maintenance.md` — § 9-12-312 alimony factors,
  modification, termination
- `references/covenant-marriage.md` — § 9-11-801 et seq. formation,
  limited divorce grounds, counseling
- `references/protection-orders.md` — § 9-15-101 et seq. Domestic
  Abuse Act: qualifying relationships, ex parte, duration, firearms
- `references/uccjea-uifsa.md` — § 9-19-101 UCCJEA home-state analysis
  + § 9-17-101 UIFSA
