---
name: ar-pro-se
description: >
  Use when drafting Arkansas court documents for a self-represented
  (pro se) litigant in Circuit or District Court. Covers the pro-se
  drafting framework adapted for Arkansas, the self-represented
  signature block (no bar number; "Pro Se" / "Self-Represented"),
  service of subsequent papers under Ark. R. Civ. P. 5, the
  Administrative Order No. 19 self-redaction duty, and the arcourts.gov
  self-help and court-forms resources. Triggers include "Arkansas pro
  se", "representing myself in Arkansas", "self-represented Arkansas",
  "file without a lawyer Arkansas", "Arkansas pro se signature block",
  "how do I serve a document in Arkansas", "Ark. R. Civ. P. 5",
  "certificate of service Arkansas", "Administrative Order 19
  redaction", "Arkansas court forms", "Arkansas self-help legal", "do I
  need an attorney in Arkansas". Layers under every other ar- skill to
  add the self-represented conventions and the consult-an-attorney
  prompt.
version: 0.1.0
---

# Pro Se Drafting for Arkansas

> **NOT LEGAL ADVICE.** This skill is a drafting aid for
> self-represented litigants, not legal advice and not a substitute
> for counsel. For complex matters, or matters with substantial sums
> at stake, consider consulting a licensed Arkansas attorney. Verify
> every rule, deadline, and citation against current law before
> filing.

This skill carries the **self-represented conventions** that layer on
top of every other Arkansas skill. Use it together with
`ar-statewide-format` (caption + format baseline), `ar-law-references`
(rule and statute lookups), and whichever venue skill governs the
filing court (`ar-pulaski`, `ar-benton`, `ar-washington`,
`ar-district-courts`, `ar-county-courts`).

## You may represent yourself

An individual may appear and act on their own behalf in Arkansas
courts. But:

- A **corporation, LLC, or other entity generally cannot appear pro
  se** — it must be represented by a licensed attorney (with narrow
  exceptions, e.g., the small claims division of District Court).
- One person **cannot** represent another (no representing a spouse,
  child, or friend) — doing so is the unauthorized practice of law.
- A non-lawyer who drafts your documents for a fee, or who tells you
  what to file or how your case will come out, may be engaged in the
  unauthorized practice of law. **This skill produces documents, not
  advice.**

> **Consult an attorney prompt.** Some matters are too consequential to
> handle alone: anything involving a default already entered, a
> deadline that has passed, real property, children's custody, a
> counterclaim exposing you to liability, or a sum you cannot afford to
> lose. Arkansas has a **discretionary attorney-fee statute** for
> contract and other civil actions (Ark. Code Ann. § 16-22-308) — the
> prevailing party (including the other side) may recover fees, so the
> downside of losing can include their lawyer's bill. Weigh getting at
> least a consultation. Legal Aid of Arkansas and the Center for
> Arkansas Legal Services serve eligible low-income litigants; the
> Arkansas Bar Association maintains a lawyer-referral service.

## The self-represented signature block

A pro se litigant signs **for themselves** under **Ark. R. Civ. P.
11**; the signature certifies the Rule 11 representations (the filing
is not for an improper purpose, the legal contentions are warranted,
the factual contentions have evidentiary support). A pro se filer
**omits the Arkansas Bar Number** that an attorney would include
("Ark. Bar No. #####") and instead designates themselves as
**self-represented**:

```
                              Respectfully submitted,


                              _________________________________
                              [Full Legal Name], Pro Se
                              [Mailing Address]
                              [City, AR  ZIP]
                              [Telephone]
                              [Email, if any]
                              Defendant, Self-Represented
```

- Use **"Pro Se"** or **"Self-Represented"** — not "Esq.", not a bar
  number.
- Give a **current mailing address** and contact information; the court
  and the other side serve you there. Update the clerk in writing if it
  changes.
- If you have registered as an e-filer under Administrative Order No.
  21, note that you have consented to **e-service**.

## Caption and format

Follow `ar-statewide-format` for the full caption and layout. In
short, the Circuit Court caption reads `IN THE CIRCUIT COURT OF
[COUNTY] COUNTY, ARKANSAS`, with an optional division line (e.g.,
`CIVIL DIVISION`, `DOMESTIC RELATIONS DIVISION`); the District Court
caption reads `IN THE DISTRICT COURT OF [CITY/DISTRICT], [COUNTY]
COUNTY, ARKANSAS`. Averments go in **numbered paragraphs** (Ark. R.
Civ. P. 10(b)); a written instrument that is an exhibit is part of the
pleading (Rule 10(c)). Arkansas does not mandate a statewide
margin/font/page rule — confirm the venue's local conventions.

## Service of subsequent papers — Ark. R. Civ. P. 5

After the complaint and summons are served (initial service is the
stricter Ark. R. Civ. P. 4 process — see `ar-first-30-days`), **every
later paper** (answer, motion, response, notice, discovery) is served
on the other parties under **Ark. R. Civ. P. 5**:

- Serve every party to the action. If a party is represented, serve
  the **attorney** (not the party).
- Permitted methods include hand delivery, mail to the last known
  address, and **e-service** to registered e-filers under
  Administrative Order No. 21. Confirm the current list of authorized
  methods in `ar-law-references` / `references/civil-rules.md`.
- **Add 3 days** to any deadline that runs from service when service
  was by mail (Ark. R. Civ. P. 6(d)) — verify the current add-on.
- Attach a **certificate of service** to every served paper, stating
  whom you served, when, and how. A sample:

```
                       CERTIFICATE OF SERVICE

I certify that on [DATE] I served a true and correct copy of the
foregoing on the following by [method — e.g., U.S. Mail, postage
prepaid / the court's electronic-filing system]:

   [Name / counsel of record]
   [Address]


                              _________________________________
                              [Full Legal Name], Pro Se
```

Filing with the court and serving the other side are **two separate
steps** — do both.

## Redaction — Administrative Order No. 19

Arkansas court records are presumptively public. **Administrative
Order No. 19** requires the **filer** to redact confidential and
identifying information **before** filing — the clerk does not do it
for you:

- Redact / omit full **Social Security numbers**, financial **account
  numbers**, and identifiers of **minor children** (use initials or
  the role, e.g., "the minor child J.D.").
- Many venues require a **certificate of compliance with Administrative
  Order No. 19** confirming you have redacted.
- If a document genuinely must contain restricted information, follow
  the venue's procedure for filing it under seal or as a confidential
  attachment rather than burying it in the public pleading.

See `ar-statewide-format` and the filing-court venue skill for the
exact redaction/certificate mechanics.

## Arkansas self-help resources

- **arcourts.gov** — the Arkansas Judiciary site publishes **court
  rules**, the **Administrative Orders**, **approved court forms**, and
  **self-help** materials (including domestic-relations and protection-
  order forms). Use the official forms where one exists for your matter.
- **Legal Aid of Arkansas** and the **Center for Arkansas Legal
  Services** — civil legal aid for eligible low-income Arkansans;
  ArkansasLegalServices / ArLawHelp self-help content.
- **County circuit / district clerk** — the clerk can tell you the
  filing fee, the e-filing requirement, and the local form
  conventions, but the clerk **cannot give legal advice**.

## A pro-se drafting checklist

1. **Identify the deadline first.** Compute the answer / response date
   before drafting (see `ar-first-30-days`, `ar-discovery`, and the
   deadline-arithmetic tooling).
2. **Plead facts, not conclusions.** Arkansas is a **fact-pleading**
   state (Ark. R. Civ. P. 8(a)) — a pleading that recites only legal
   conclusions is vulnerable. State who did what, when, and where.
3. **Number every paragraph** (Ark. R. Civ. P. 10(b)); attach exhibits
   (Rule 10(c)).
4. **Redact** under Administrative Order No. 19 before filing.
5. **Sign** with the self-represented block; **omit** any bar number.
6. **Serve** every party under Ark. R. Civ. P. 5 and attach a
   **certificate of service**.
7. **File** with the clerk (eFlex e-filing under Administrative Order
   No. 21 where applicable) — filing and serving are separate steps.
8. **Keep a copy** of everything you file and proof of service.

## Composition

- For caption + format: `ar-statewide-format`
- For rule / statute / case lookups: `ar-law-references`
- For the answer and Rule 12 triage after service: `ar-first-30-days`
- For discovery: `ar-discovery`
- For the filing court's mechanics: `ar-pulaski`, `ar-benton`,
  `ar-washington`, `ar-district-courts`, `ar-county-courts`

## References

- See `ar-law-references/references/civil-rules.md` for Ark. R. Civ. P.
  4 / 5 / 6 / 10 / 11 detail and the current service methods and
  mail add-on.
- See `ar-law-references/references/online-sources.md` for the
  arcourts.gov forms and self-help URLs.
