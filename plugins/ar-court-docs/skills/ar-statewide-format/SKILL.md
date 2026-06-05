---
name: ar-statewide-format
description: >
  This skill should be used when the user asks to "draft a pleading",
  "format an Arkansas court document", "apply Ark. R. Civ. P. 10",
  "build an Arkansas caption", "format a complaint", "format a
  motion", "draft a declaration or affidavit", "draft a proposed
  order", or "format a filing" for any Arkansas state court — Circuit
  Court or District Court. Triggers include "Arkansas caption", "Ark.
  R. Civ. P. 10", "Rule 10 caption", "numbered paragraphs", "Rule 11
  signature", "Arkansas Bar Number", "Ark. Bar No.", "certificate of
  service Rule 5", "Circuit Court of Pulaski County", "District Court
  of", "Case No.", "CV-__-____ docket number", "Administrative Order
  19 redaction", "certificate of compliance", "Administrative Order 21
  e-filing", "eFlex", "how do I format an Arkansas complaint", "what
  margins does an Arkansas court require", and "2015 Ark. 100 medium-
  neutral citation". Covers Ark. R. Civ. P. 10 form-of-pleadings
  requirements, the Arkansas Circuit Court and District Court captions,
  numbered paragraphs, attaching written instruments under Rule 10(c),
  the Rule 11 signature block with the attorney's Arkansas Bar Number,
  certificate of service under Rule 5, Administrative Order No. 19
  redaction + certificate of compliance, Administrative Order No. 21
  eFlex e-filing, line-numbered pleading-paper conventions, and
  Arkansas medium-neutral citation (2015 Ark. 100 / 2015 Ark. App.
  200, Ark. Sup. Ct. R. 5-2). It is the canonical home for the
  marketplace layout conventions and the key point that Arkansas has
  no statewide page/margin/font rule — typography and page limits come
  from each court's LOCAL RULES and circuit administrative plan.
version: 0.1.0
---

# Arkansas Statewide Court Document Formatting

> **NOT LEGAL ADVICE.** This skill assists with drafting and
> formatting only. Verify against the current Arkansas Rules of Civil
> Procedure, the Administrative Orders of the Arkansas Supreme Court,
> and the local rules / administrative plan of the filing court before
> submitting any document.

Use these conventions whenever drafting a paper to be filed in an
Arkansas state trial court. The form of an Arkansas pleading is
governed by **Ark. R. Civ. P. 10** (form of pleadings) and **Ark. R.
Civ. P. 11** (signing of pleadings), supplemented by **Ark. R. Civ. P.
5** (service and filing of subsequent papers), the Arkansas Supreme
Court's **Administrative Order No. 19** (access to court records /
redaction), and **Administrative Order No. 21** (electronic filing).

## Key architectural point: there is NO statewide page/margin/font rule

Arkansas does **not** publish a single statewide rule prescribing paper
size, margins, font, line spacing, or page limits for trial-court
pleadings. The form of a pleading is set by:

- **Ark. R. Civ. P. 10** — the caption (name of court, title of the
  action, docket number, designation of the paper) and averments in
  **numbered paragraphs** (content/structure, not typography);
- **Ark. R. Civ. P. 11** — the signature and its representations;
- **Administrative Order No. 19** — redaction of confidential/
  identifying information and a **certificate of compliance**;
- **Administrative Order No. 21** — statewide electronic filing
  through **eFlex**; and
- the **LOCAL RULES / circuit administrative plan of the filing court**
  — each judicial circuit publishes an administrative plan and many
  courts publish local rules covering margins, page limits, chambers
  copies, proposed-order conventions, and division-specific mechanics.
  These are indexed at **arcourts.gov**.

So this skill states the **common-practice defaults** for typography
and **defers page limits / margins / font specifics to local rules and
the circuit administrative plan**. Always confirm the controlling
court's requirements before relying on any page limit or margin figure.
(Pulaski, Benton, and Washington Counties each have an overlay skill —
see Composition.)

Note: **appellate** briefs filed in the Arkansas Supreme Court and
Court of Appeals DO have a strict format under **Ark. Sup. Ct. R. 4-1 /
4-2**, and e-filing is mandatory in the appellate courts — but that is
appellate, not trial-court, practice.

## Common-practice typographic defaults (verify against local rules)

These are the customary defaults Arkansas practitioners use absent a
contrary local rule or administrative-plan provision. They are
conventions, not a statewide mandate — confirm against the filing
court's requirements.

| Item | Common-practice default |
|------|--------------------------|
| Paper size | US Letter, 8½ × 11 inches |
| Margins | 1 inch on all four sides |
| Body font | 12 point, serif (Times New Roman or Century Schoolbook) |
| Line spacing | Double-spaced body text; single-spaced block quotes, captions, and signature blocks |
| Ink | Black |
| Page numbers | Each page numbered; `Page X of Y` in the footer |

`scripts/format-check.py` validates a generated `.docx` against these
common-practice defaults and flags departures so they can be checked
against the controlling local rule or administrative plan.

## Line numbering (pleading paper) — applied BY DEFAULT

Apply continuous line numbering down the left margin of every generated
Arkansas pleading. Line numbers count every body line and **restart on
each page**.

Ark. R. Civ. P. 10 does **not** require line numbering, and an Arkansas
pleading filed without line numbers is rule-compliant. But
line-numbered pleading paper is universal practice across the
`claude-legal` marketplace: it lets the court and opposing counsel cite
an exact location ("page 4, lines 12-15") and never harms an Arkansas
filing. Apply it **by default** to every motion, memorandum brief,
declaration, affidavit, notice, and proposed order. Exhibits and
attachments are exempt.

For programmatically generated `.docx` documents, apply line numbering
through the section's `lineNumbers` property:

```javascript
import { LineNumberRestartFormat } from "docx";

sections: [{
  properties: {
    page: { /* size + margins */ },
    lineNumbers: {
      countBy: 1,                                // number every line
      restart: LineNumberRestartFormat.NEW_PAGE, // restart 1.. each page
    },
  },
  // ...
}]
```

This emits `<w:lnNumType w:countBy="1" w:restart="newPage"/>` into the
section's `<w:sectPr>`. The numbers render in the left margin and do
not shift the 1-inch text margin.

**Do NOT set `start` explicitly.** An explicit `start: 1` renders off
by one in LibreOffice (the first body line shows "2"). Omit `start` —
it defaults to 1 in OOXML.

## Required footer (mandatory on every generated document)

Every generated document MUST carry a running footer on every page:

- **Left**: a short document identifier — typically
  `[Document title] — Case No. [docket number]` (e.g., `Answer —
  Case No. 60CV-25-1234`). Keep it to a single line so it never wraps.
- **Right**: `Page X of Y`, where `X` is the current page number and
  `Y` is the total page count. Use Word's `PAGE` and `NUMPAGES` fields
  — never a static number.
- **Font**: 10 pt; matches body font family.
- **Alignment**: a right-aligned tab stop at 9,360 DXA (6.5") places
  the page counter flush right while the title stays flush left.

The footer runs continuously from page 1 through the last exhibit page
— do not restart or suppress pagination anywhere.

## Two-section page-1 pattern

If a venue local rule or administrative plan ever sets a larger top
margin on page 1 (for the clerk's file stamp), generate the document in
**two sections**: a first section covering page 1 with the larger top
margin, and a second section for the balance with the standard margin.
Apply the same `lineNumbers` and footer settings to both sections so
numbering and pagination stay continuous. Absent such a local rule,
a single section with uniform margins is fine.

## Caption structure (Ark. R. Civ. P. 10(a))

Rule 10(a) requires every pleading to contain a caption stating the
**name of the court**, the **title of the action** (the parties), the
**docket (case) number**, and a **designation** of the paper. The
Arkansas caption stacks the court line, the party block, the
case-number line, and the document title:

```
            IN THE CIRCUIT COURT OF PULASKI COUNTY, ARKANSAS
                          CIVIL DIVISION

JOHN DOE,                                  )
        Plaintiff,                         )
                                           )
v.                                         )   Case No. ____________
                                           )
MIDLAND CREDIT MANAGEMENT, INC.,           )
        Defendant.                         )

                              ANSWER
```

### The four caption elements in order

1. **Court identifier line** (centered, ALL CAPS).
   - Circuit Court: `IN THE CIRCUIT COURT OF [COUNTY] COUNTY, ARKANSAS`
     (some clerks render it `IN THE CIRCUIT COURT OF [COUNTY] COUNTY`).
     An optional division line follows — e.g., `CIVIL DIVISION`,
     `DOMESTIC RELATIONS DIVISION`, `PROBATE DIVISION`. The five
     subject-matter divisions (criminal, civil, probate, domestic
     relations, juvenile) are administrative divisions of one Circuit
     Court, not separate courts.
   - District Court: `IN THE DISTRICT COURT OF [CITY/DISTRICT],
     [COUNTY] COUNTY, ARKANSAS`. See `ar-district-courts`.
2. **Party block.** On the left, the parties stacked with their
   designations, separated by a centered `v.`; on the right, a column
   of right parentheses `)` closing into the case-number line.
   - **Plaintiff / Defendant** for civil actions (including Arkansas
     divorce, which uses Plaintiff/Defendant rather than
     Petitioner/Respondent — though "Petitioner" appears in some
     paternity and guardianship matters).
   - `IN RE` for in-rem captions.
3. **Case-number line.** Commonly `Case No. ____________` or the
   structured Arkansas docket format `No. [county code]CV-[yy]-[####]`
   (e.g., `60CV-25-1234`, where the leading digits are the county
   number, `CV` is the civil case type, and the balance is the
   year-sequence). The filer leaves it blank on an initial pleading —
   the clerk assigns and stamps the number on filing — and populates it
   on every subsequent paper.
4. **Document title** (centered, ALL CAPS) immediately below the
   caption: e.g., `COMPLAINT`, `ANSWER`, `MOTION TO DISMISS`,
   `MOTION FOR SUMMARY JUDGMENT`.

## Numbered paragraphs (Ark. R. Civ. P. 10(b))

Under Rule 10(b), all averments of claim or defense are made in
**numbered paragraphs**, the contents of each limited as far as
practicable to a **single set of circumstances**. Number with an Arabic
numeral, a period, and a tab: `1.\tThe Defendant is a resident of
Pulaski County, Arkansas.` Claims founded on separate transactions
should be stated in separate counts when separation aids clarity.

Keep in mind that Arkansas is a **fact-pleading** jurisdiction — the
complaint must state **facts**, not bare legal conclusions (Ark. R.
Civ. P. 8(a) requires a statement of the facts in ordinary and concise
language). Drafting averments with concrete factual content is a form
requirement with substantive teeth; see `ar-first-30-days` for the
Rule 12(b)(6) fact-pleading standard.

## Attaching written instruments (Ark. R. Civ. P. 10(c))

Under Rule 10(c), a copy of a **written instrument** that is an exhibit
to a pleading (a contract, note, lease, assignment, etc.) is a **part
of the pleading for all purposes**. When a claim or defense is founded
on a written instrument, attach a copy and reference it by letter in
the body ("a true and correct copy of the [instrument] is attached as
**Exhibit A**"). Attach the copies after the signature block and
certificate of service. In debt-buyer cases this is where the
assignment / chain-of-title documents live — see `ar-consumer-debt`.

## Signature block (Ark. R. Civ. P. 11)

Under Rule 11, every pleading, motion, or other paper must be **signed
by at least one attorney of record** in the attorney's individual name,
or, **if the party is not represented, by the party**. The signature
certifies the Rule 11 representations (the paper is not interposed for
delay, claims are warranted by law, factual contentions have
evidentiary support, etc.).

An attorney's signature block must include the attorney's **Arkansas
Bar Number**:

```
Respectfully submitted,


                                   ____________________________
                                   [Name]
                                   Ark. Bar No. #####
                                   [Firm name]
                                   [Street address]
                                   [City, AR ZIP]
                                   Phone: (###) ###-####
                                   Email: name@example.com
                                   Attorney for [Party]
```

**Pro se filers omit the bar number** and identify themselves as
self-represented:

```
                                   ____________________________
                                   [Name]
                                   [Street address]
                                   [City, AR ZIP]
                                   Phone: (###) ###-####
                                   Email: name@example.com
                                   Pro Se / Self-Represented
```

See `ar-pro-se` for the full self-represented drafting framework.

## Verification / declaration language

Many Arkansas filings use a traditional **notarized affidavit** with a
jurat; some filings may use an **unsworn declaration**. For a sworn
affidavit, use the jurat ("Subscribed and sworn to before me this ___
day of ____, 20__") with the notary block. For a declaration, close the
body with:

```
I declare under penalty of perjury that the foregoing is true and
correct.

Executed on [date] at [city], Arkansas.

                                   ____________________________
                                   [Declarant name]
```

Verify whether a particular filing must be **sworn (notarized)** rather
than declared (verified pleadings, certain affidavits, and probate
filings frequently require a notarized jurat). Default to a notarized
affidavit where the rule or the filing type calls for sworn testimony.

## Certificate of service (Ark. R. Civ. P. 5)

Every paper required to be served must carry a certificate of service
under Rule 5. Place it at the foot of the document:

```
                    CERTIFICATE OF SERVICE

I certify that on [date] a true and correct copy of the foregoing
[Document Title] was served on:

  [Opposing party / counsel name]
  [Address]
  via [the court's electronic-filing system (eFlex) / U.S. Mail,
       postage prepaid / hand delivery / email per Ark. R. Civ. P. 5].

                                   ____________________________
                                   [Signer name]
```

Registered e-filers under Administrative Order No. 21 consent to
electronic service through eFlex. Initial process (the summons) is
served under **Ark. R. Civ. P. 4**, not Rule 5; verify the current
Rule 4 service period in `ar-law-references`.

## Administrative Order No. 19 — redaction + certificate of compliance

Under **Administrative Order No. 19**, filers must **redact
confidential / identifying information** from documents that become
part of the public court record — Social Security numbers, financial
account numbers, and identifiers of minors, among others. A filed
document should carry a **certificate of compliance with Administrative
Order No. 19** confirming the filer has redacted the required
information (or that an exception applies). Treat the redaction pass and
the certificate as part of the standard pre-filing workflow; see
`ar-quality-check` and `ar-file-packet`.

## Exhibits

Attach exhibits after the signature block and certificate of service:

1. An **Exhibit List** page, centered title, each entry like
   `Exhibit A:    [one-line description]`.
2. One **cover page per exhibit**: `EXHIBIT A` centered and bold,
   followed by an italic caption, then the exhibit content.
3. Footer pagination continues through the exhibits — do not restart
   the page counter.

A written instrument attached under Rule 10(c) is itself an exhibit and
is part of the pleading for all purposes.

## Citation format

Since **July 1, 2009**, Arkansas uses a **medium-neutral / public-
domain citation** for its appellate opinions, governed by **Ark. Sup.
Ct. R. 5-2**. There is no separate Arkansas style manual; citation
otherwise follows Bluebook as modified by Rule 5-2.

- Arkansas Supreme Court (post-2009): `Smith v. Jones, 2015 Ark. 100`
  (parallel `S.W.3d` cite where available).
- Arkansas Court of Appeals (post-2009): `Smith v. Jones, 2015 Ark.
  App. 200`.
- Pre-2009 opinions cite to the Arkansas Reports + the South Western
  Reporter: `Sterling Drug, Inc. v. Oxford, 294 Ark. 239, 743 S.W.2d
  380 (1988)`.
- Statutes: `Ark. Code Ann. § 16-56-111`.
- Rules: `Ark. R. Civ. P. 12`; `Ark. R. Evid. 803(6)`; administrative
  orders: `Ark. Sup. Ct. Admin. Order No. 19`.

See `ar-fact-check` for citation verification.

## Producing documents programmatically

For `.docx` generation, use the `docx` npm package. Key points:

- Set page size explicitly to US Letter (12,240 × 15,840 DXA) —
  `docx-js` defaults to A4.
- Use Times New Roman at `size: 24` (half-points = 12 pt).
- Apply uniform 1,440 DXA margins to all four sides on every section
  (a common-practice default — confirm against local rules).
- Build the footer with a right-aligned tab stop at 9,360 DXA and use
  `PageNumber.CURRENT` / `PageNumber.TOTAL_PAGES` for "Page X of Y".
- Apply the `lineNumbers` section property above (omit `start`).

Run `scripts/format-check.py` on the generated `.docx` to validate the
common-practice defaults.

## Filing mechanics: paper vs. e-filing

Arkansas operates a statewide e-filing system, **eFlex**, under
**Administrative Order No. 21**; the trial courts run on the **Contexte**
case-management system. Whether e-filing is mandatory or available, and
the document-type codes used at filing, vary by court — confirm the
venue's posture (and the Administrative Order No. 19 redaction +
certificate requirement) before assembling a packet. The appellate
courts use mandatory e-filing. See the venue skills and
`ar-file-packet`.

## Composition

- For Pulaski County (Little Rock, 6th Judicial Circuit): `ar-pulaski`
- For Benton County (Bentonville, 19th Judicial Circuit West):
  `ar-benton`
- For Washington County (Fayetteville/Springdale, 4th Judicial
  Circuit): `ar-washington`
- For limited-jurisdiction / small-claims / eviction practice:
  `ar-district-courts`
- For other counties' Circuit Courts: `ar-county-courts`
- For drafting specific document types: `ar-draft-motion`,
  `ar-draft-declaration`, `ar-draft-note`, `ar-draft-order`
- For pro se conventions: `ar-pro-se`
- For pre-filing QC: `ar-quality-check`
- For citation verification: `ar-fact-check`

## References

- `ar-law-references` — canonical Ark. R. Civ. P., Ark. R. Evid., Ark.
  Code Ann., Administrative Orders, and local-rules corpus
- `scripts/format-check.py` — common-practice format validation
