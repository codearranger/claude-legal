---
name: ar-consumer-debt
description: >
  This skill should be used when defending an Arkansas consumer
  against a debt-collection lawsuit (typically by a debt buyer or
  collection agency, often in District Court for sub-$25,000
  amounts, in Circuit Court above). Triggers include "Arkansas
  debt-buyer lawsuit", "sued by a debt collector in Arkansas",
  "Midland Credit lawsuit Arkansas", "Portfolio Recovery Arkansas",
  "Cavalry SPV Arkansas", "LVNV Funding Arkansas", "Unifin
  Arkansas", "I was sued on a credit card in Arkansas", "Arkansas
  FDCPA", "Arkansas Deceptive Trade Practices Act", "ADTPA debt
  collection", "Ark. Code Ann. 4-88-101", "Arkansas State Board of
  Collection Agencies", "Arkansas collection agency license",
  "unlicensed debt collector Arkansas", "Ark. Code Ann. 17-24-101",
  "Arkansas statute of limitations credit-card debt", "Ark. Code
  Ann. 16-56-111", "Ark. Code Ann. 16-56-105", "written contract 5
  years Arkansas", "open account 3 years Arkansas", "chain of title
  Arkansas debt", "debt-buyer default judgment Arkansas", "sued in
  District Court Arkansas debt", "Arkansas fact pleading". Subject-
  matter bundle covering the federal FDCPA / Regulation F / FCRA
  layer, the Arkansas Deceptive Trade Practices Act (Ark. Code Ann.
  § 4-88-101 et seq.) as narrowed by Act 986 of 2017, the
  collection-agency licensing regime under the Arkansas State Board
  of Collection Agencies (Ark. Code Ann. § 17-24-101 et seq.),
  chain-of-title doctrine under Arkansas UCC Article 9, the Arkansas
  SOL framework (written contract 5 years / oral and open account 3
  years), and the District-vs-Circuit forum split.
version: 0.1.0
---

# Arkansas Consumer-Debt Defense

> **NOT LEGAL ADVICE.** This subject-matter bundle describes a
> procedural and substantive framework for Arkansas consumer-debt
> cases, not legal advice and not strategic advice for any specific
> case. Outcomes are fact-specific; the choice of defenses, claims,
> motions, and discovery belongs to the litigant (and any counsel
> the litigant retains). Statute numbers, dollar thresholds, and day
> counts change — verify every citation against the current Ark.
> Code Ann. and consult a licensed Arkansas attorney about your
> specific case.

Use this subject-matter bundle when an Arkansas consumer has been
sued by a **debt collector** — typically a **debt buyer** (Midland
Credit Management, Portfolio Recovery Associates, Cavalry SPV, LVNV
Funding, Unifin, etc.) or a **collection agency** acting for an
original creditor. The forum is **District Court** for amounts within
its limited civil jurisdiction and **Circuit Court** above that line
(see "Forum" below).

## The Arkansas consumer-debt landscape

Arkansas is distinctive in what it **lacks**: there is **no
comprehensive Arkansas mini-FDCPA statute**. Many states layer a
state debt-collection-practices act over the federal regime; Arkansas
does not. As a result, an Arkansas consumer's collection-abuse claims
and defenses rest on **three** sources working together:

1. the **federal FDCPA** and **Regulation F** — the workhorse for
   debt-collector conduct claims and counterclaims;
2. the **Arkansas Deceptive Trade Practices Act (ADTPA)** — a general
   consumer-protection statute, materially **narrowed** for private
   plaintiffs by **Act 986 of 2017** (read the limits before pleading
   it); and
3. the **collection-agency licensing regime** under the **Arkansas
   State Board of Collection Agencies** (Ark. Code Ann. § 17-24-101
   et seq.) — a real capacity/standing pressure point against an
   unlicensed collector.

Layered on top are the ordinary contract-defense tools: the
**statute of limitations**, **chain-of-title** proof under Arkansas
UCC Article 9, the **business-records evidentiary foundation**, and —
distinctively — Arkansas's **fact-pleading** standard, which is a
stricter pleading bar than federal notice pleading.

### Federal layer

- **FDCPA** (Fair Debt Collection Practices Act), 15 U.S.C.
  §§ 1692–1692p — the primary vehicle for debt-collector-conduct
  claims and counterclaims. See `references/fdcpa.md`.
- **Regulation F**, 12 C.F.R. pt. 1006 — the CFPB rule implementing
  the FDCPA (call-frequency, validation-notice, and time/place
  rules). See `references/reg-f.md`.
- **FCRA** (Fair Credit Reporting Act), 15 U.S.C. §§ 1681 et seq. —
  furnisher / re-aging / dispute issues when the debt is also being
  reported (compose with the federal `consumer-credit-disputes` and
  `consumer-report-accuracy` skills).

### Arkansas layer

- **Arkansas Deceptive Trade Practices Act (ADTPA)** — Ark. Code Ann.
  § 4-88-101 et seq.; private right of action at § 4-88-113(f), as
  narrowed by Act 986 of 2017. See `references/ar-adtpa.md`.
- **Collection-agency licensing** — Ark. Code Ann. § 17-24-101 et
  seq., administered by the **Arkansas State Board of Collection
  Agencies**. See `references/ar-collection-agency-law.md`.
- **Arkansas UCC Article 9** — Ark. Code Ann. § 4-9-101 et seq.;
  governs the assignments that make up a debt buyer's chain of title.
  See `references/chain-of-title.md`.

## Forum — District Court vs. Circuit Court

Arkansas unified its trial courts under **Amendment 80 (2001)**. For
consumer debt, two forums matter:

- **District Court** — the limited-jurisdiction trial court (renamed
  from "Municipal Court" by Amendment 80). It handles civil claims up
  to its statutory cap, with a **small-claims division** for the
  smaller tier. This is the **high-volume consumer-debt forum**.
  District Court practice runs under the **Arkansas District Court
  Rules** layered with the Arkansas Rules of Civil Procedure. See
  `ar-district-courts` for the caps and the rule set; keep the
  current dollar thresholds in `references/` rather than memorizing
  them.
- **Circuit Court** — the general-jurisdiction court, used when the
  amount exceeds the District Court civil cap. Full Arkansas Rules of
  Civil Procedure apply, including formal discovery as of right. See
  `ar-pulaski` / `ar-benton` / `ar-washington` / `ar-county-courts`
  for venue mechanics.

**Strategic consequence — the de novo appeal.** An appeal from a
District Court judgment is taken to **Circuit Court for de novo
review** within the appeal window (a short clock — confirm the exact
day count in `references/ar-statutes-of-limitations.md` and in
`ar-deadlines` / `ar-post-judgment`). On de novo appeal the case is
tried **afresh in Circuit Court under the full Rules of Civil
Procedure**, where formal **discovery** of the chain of title and the
account documentation becomes available as of right — the records a
debt buyer often cannot produce. Calendar that clock immediately; it
is short and non-forgiving.

## Arkansas is a fact-pleading jurisdiction

A defining Arkansas procedural feature: Arkansas requires **fact
pleading**, not notice pleading. Under **Ark. R. Civ. P. 8(a)** a
complaint must state, in ordinary and concise language, the **facts**
showing that the pleader is entitled to relief — mere conclusions
will not do. This is a **stricter** bar than federal notice pleading.

For debt-buyer defense this matters at the **Ark. R. Civ. P.
12(b)(6)** stage: a complaint that recites the elements ("defendant
owes plaintiff $X on an account") without pleading **facts** — the
identity of the original creditor, the chain of assignments to the
plaintiff, the account terms — is vulnerable to a motion to dismiss
for failure to state facts upon which relief can be granted. See
`ar-first-30-days` for how to frame the 12(b)(6) angle; keep the
exact day counts (answer-due, response windows) in
`references/ar-statutes-of-limitations.md` and `ar-deadlines`.

## Statutes of limitations on the debt

Arkansas's limitations periods turn on whether the obligation is a
**written contract** or an **oral/open account** — a distinction that
is frequently dispositive in a credit-card case.

- **Written contract — longer period** (Ark. Code Ann. § 16-56-111).
- **Oral contract / open account — shorter period** (Ark. Code Ann.
  § 16-56-105).
- **Judgments** are subject to a separate, longer period and are
  **revivable** by scire facias.

Exact year counts, the accrual rules (last payment / last activity /
breach), the credit-card written-vs-open-account nuance, and the
judgment-revival mechanics live in
`references/ar-statutes-of-limitations.md` — do not hard-code them
here. The key litigation point: **identify the nature of the
obligation** (signed cardholder agreement → written-contract theory;
no signed agreement → open-account theory) because it selects the
limitations period and can put a stale account past the line.

## The ADTPA and its limits — read this before pleading it

The **Arkansas Deceptive Trade Practices Act**, Ark. Code Ann.
§ 4-88-101 et seq., is the state's general consumer-protection
statute. **Before pleading a private ADTPA claim, read the Act 986 of
2017 limits.** Act 986 amended the private right of action at
§ 4-88-113(f) to require a private plaintiff to prove:

- an **actual financial loss**, and
- that the loss resulted from **reliance** on the deceptive practice;

and Act 986 also **restricts private class actions** under the ADTPA.
The **Attorney General** retains broad enforcement authority that is
not subject to those private-action limits.

Practical consequences for a debt case:

- A private ADTPA claim premised on collection conduct must clear the
  **actual-loss + reliance** elements — it is not a strict-liability
  fee-shifting vehicle the way the FDCPA is.
- For ordinary collection-conduct violations, the **FDCPA** (which
  carries statutory damages, actual damages, and mandatory
  fee-shifting on a prevailing consumer) is generally the stronger
  vehicle; reserve the ADTPA for situations where you can plead and
  prove reliance-based actual loss.

The annotated treatment — what counts as a "deceptive" or
"unconscionable" practice, the AG-vs-private distinction, and the
post-2017 case law — is in `references/ar-adtpa.md`.

## The collection-agency licensing hook

Arkansas licenses and regulates collection agencies through the
**Arkansas State Board of Collection Agencies** under Ark. Code Ann.
§ 17-24-101 et seq. A collection agency operating in Arkansas must be
**licensed and bonded**. Where the plaintiff (or its servicer) is an
**unlicensed** collector, that is a genuine **capacity/standing**
pressure point — raise it as an affirmative defense and probe it in
discovery.

Two cautions, both developed in
`references/ar-collection-agency-law.md`:

1. The statute contains **exemptions** (certain creditors collecting
   their own debts, attorneys, banks, etc.) — confirm the plaintiff
   is actually a covered "collection agency" before asserting the
   defense.
2. Check the **Board's licensee roster** for the plaintiff and its
   servicer at the outset; license status is verifiable.

## Chain of title — Arkansas UCC Article 9

A debt buyer must trace ownership from the original creditor through
every intermediate buyer to itself under Arkansas's enactment of UCC
Article 9 (Ark. Code Ann. § 4-9-101 et seq.), with:

- a **Bill of Sale** for each transfer;
- an **Assignment** specifically identifying **this account** (account
  number / unique identifier); and
- **account-level data** matching this consumer's account.

A bill of sale that references "an attached portfolio" without
attaching it, or that says "all accounts sold on [date]" without
tying to **this** account, is **insufficient** to prove ownership.
See `references/chain-of-title.md`; the RFP bank in
`references/rfp-debt-buyer.md` targets each link.

## Evidence foundation the plaintiff must satisfy

To prove the debt and the assignment, a debt-buyer plaintiff must lay
a business-records foundation:

- **Ark. R. Evid. 803(6)** — business-records hearsay exception
  (records of regularly conducted activity, via a custodian or other
  qualified witness, or a self-authenticating certification).
- **Ark. R. Evid. 902(11)** — self-authentication of certified
  domestic records of regularly conducted activity (the foundation
  for admitting account records without a live custodian).

A common defense theme: the debt buyer's affiant has **no personal
knowledge** of the *original creditor's* record-keeping and cannot lay
an 803(6) foundation for records created by a different entity. Probe
the affiant's basis of knowledge. See
`references/evidence-debt-buyer.md`.

## The five fact patterns

Most Arkansas consumer-debt-buyer cases fall into one of five
patterns; the defense strategy varies by pattern.

### Pattern 1 — Debt-buyer chain-of-title gap

A downstream debt buyer sues but attaches only a generic bill of sale
(or none) and cannot tie **this** account to itself through the chain.

- **Standing / proof of ownership**: demand the Article 9 bills of
  sale and assignments for **every** link, each identifying this
  account number.
- **Fact pleading**: if the complaint does not plead the assignment
  chain as **facts**, raise Ark. R. Civ. P. 12(b)(6).
- **Discovery** (in Circuit, or on de novo appeal): the RFP / RFA /
  interrogatory banks target each transfer.

### Pattern 2 — Time-barred suit

A debt buyer sues on a credit-card or account balance whose last
payment/activity is past the limitations line.

- **Characterize the obligation**: open-account theory triggers the
  shorter period; written-contract theory the longer one (see
  `references/ar-statutes-of-limitations.md`).
- Pin down the **date of last payment / last activity** from the
  account history.
- Plead **statute of limitations** as an affirmative defense; an
  out-of-statute suit can also support an **FDCPA** § 1692e/§ 1692f
  counterclaim for suing on time-barred debt.

### Pattern 3 — Unlicensed collector

The plaintiff or its servicer is collecting in Arkansas without a
license from the Arkansas State Board of Collection Agencies.

- Confirm the plaintiff is a covered "collection agency" (not within
  a statutory exemption) and is in fact **unlicensed** (check the
  Board roster).
- Raise the **capacity/standing** defense and probe license status in
  discovery. See `references/ar-collection-agency-law.md`.

### Pattern 4 — FDCPA violation

Abusive or deceptive collection conduct — illegal call frequency,
false amount, threats, failure to validate, suing on time-barred debt.

- **FDCPA** counterclaim under §§ 1692e (false/misleading), 1692f
  (unfair), 1692g (validation), or 1692c (communications); 1-year SOL
  from the violation; statutory + actual damages + mandatory fees on
  a prevailing consumer.
- **Regulation F** overlay (call-frequency presumption, validation
  notice). See `references/reg-f.md`.
- Consider a **narrow ADTPA** claim only if reliance-based actual loss
  can be pleaded (Act 986).

### Pattern 5 — Identity / standing (wrong defendant or default)

The consumer does not recognize the account (possible identity theft
or misidentification), or a default judgment was entered, often after
defective service.

- **Identity theft**: dispute and FCRA § 605B block; deny the account.
- **Default already entered**: raise relief from judgment (Ark. R.
  Civ. P. 60 — note the distinctive **90-day Rule 60(a)** window to
  modify/vacate for error, with narrower grounds after) and/or the
  de novo appeal from District Court if still in the window. See
  `ar-post-judgment`.
- Pair any set-aside with a **meritorious defense** (SOL, chain of
  title, FDCPA).

## Affirmative-defenses catalog

Plead all that apply in the answer:

1. **Failure to state facts upon which relief can be granted** — Ark.
   R. Civ. P. 12(b)(6); the complaint pleads conclusions, not the
   facts of the assignment chain / account terms (fact-pleading).
2. **Statute of limitations** — written contract (§ 16-56-111) or
   oral/open account (§ 16-56-105), per the obligation's character.
3. **Lack of standing / failure to prove assignment** — plaintiff
   cannot prove it owns **this** account (Article 9).
4. **Lack of capacity to sue** — plaintiff is an unlicensed
   collection agency (§ 17-24-101 et seq.), if covered and unlicensed.
5. **Lack of privity** between plaintiff and defendant.
6. **Account stated** — no agreed accounting between this plaintiff
   and this defendant.
7. **Failure / lack of consideration.**
8. **Payment / accord and satisfaction / settlement / release.**
9. **Identity theft / mistaken identity** (if applicable) — FCRA
   § 605B block.
10. **Discharge in bankruptcy** (if applicable).
11. **FDCPA violation** (pleaded as a counterclaim; note as a defense
    theme — e.g., suit on time-barred debt).

See `references/examples/answer-debt-buyer.md` for a synthetic answer
that assembles these.

## Discovery strategy

- **In District Court**, discovery is more limited; use the District
  Court Rules' available tools, cross-examine at the hearing, and
  preserve the **de novo appeal** to reach full discovery in Circuit.
- **In Circuit Court** (original filing or de novo appeal), the full
  Arkansas Rules of Civil Procedure apply. Arkansas **does** allow
  interrogatories (Ark. R. Civ. P. 33, subject to a presumptive cap —
  see `references/interrogatories-debt-buyer.md`), along with RFPs
  (Rule 34), RFAs (Rule 36), and depositions (Rules 30/31). Sequence:
  1. **First Set of Requests for Admission** (Rule 36) — admissions
     on the elements (no contract, no assignment, no statement of
     account). See `references/rfa-debt-buyer.md`.
  2. **First Set of Interrogatories** (Rule 33) — chain of title,
     custodian identity, account-level data, license status. See
     `references/interrogatories-debt-buyer.md`.
  3. **First Set of Requests for Production** (Rule 34) — bills of
     sale, assignments, original agreement, periodic statements,
     account-level data, electronic records. See
     `references/rfp-debt-buyer.md`.
  4. **Subpoena to the original creditor** verifying the chain.
  5. **Meet-and-confer**, then **Motion to Compel** under Rule 37.

See `ar-discovery` for mechanics.

## Composition

- For statewide format: `ar-statewide-format`
- For the dominant forum and the District-vs-Circuit / de novo
  mechanics: `ar-district-courts`; venue: `ar-pulaski` / `ar-benton`
  / `ar-washington` / `ar-county-courts`
- For pro se conventions and service: `ar-pro-se`
- For drafting the answer / first response and the 12(b)(6) angle:
  `ar-first-30-days`, `ar-draft-motion`
- For the declaration: `ar-draft-declaration`
- For the proposed order: `ar-draft-order`
- For the notice / motion: `ar-draft-note`, `ar-draft-motion`
- For discovery and motion-to-compel mechanics: `ar-discovery`
- For setting aside a default / garnishment / Rule 60 relief:
  `ar-post-judgment`
- For the appeal and other clocks: `ar-deadlines`
- For QC: `ar-quality-check`, `ar-fact-check`

## References

- `references/fdcpa.md` — FDCPA, 15 U.S.C. § 1692 et seq., Arkansas
  framing (cross-refs the verbatim federal text)
- `references/reg-f.md` — Regulation F at 12 C.F.R. pt. 1006
- `references/ar-adtpa.md` — Arkansas Deceptive Trade Practices Act
  (§ 4-88-101 et seq.) + the Act 986 of 2017 private-action narrowing
- `references/ar-collection-agency-law.md` — Ark. Code Ann.
  § 17-24-101 et seq.; the Arkansas State Board of Collection
  Agencies; licensing/bond; exemptions; capacity-to-sue challenge
- `references/chain-of-title.md` — Arkansas UCC Article 9 doctrine
- `references/evidence-debt-buyer.md` — Ark. R. Evid. 803(6) / 902(11)
  foundation
- `references/ar-statutes-of-limitations.md` — § 16-56-111 (written) /
  § 16-56-105 (oral/open) / judgment revival
- `references/fees-consumer-debt.md` — fee mechanics (Ark. Code Ann.
  § 16-22-308; FDCPA fee-shifting)
- `references/rfp-debt-buyer.md` — Request for Production bank
- `references/rfa-debt-buyer.md` — Request for Admission bank
- `references/interrogatories-debt-buyer.md` — Interrogatory bank
- `references/key-cases.md` — Arkansas + federal debt-defense case law
- `references/online-sources.md` — canonical Arkansas URLs
- `references/examples/answer-debt-buyer.md` — SYNTHETIC sample answer
