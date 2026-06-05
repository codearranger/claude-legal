---
name: ar-draft-declaration
description: >
  This skill should be used to scaffold the sworn-facts document that
  supports an Arkansas filing — in Arkansas practice this is most often
  a NOTARIZED AFFIDAVIT (with a jurat), and where authorized an unsworn
  declaration under penalty of perjury. Triggers include "draft an
  affidavit in Arkansas", "draft an Arkansas affidavit in support of a
  motion", "draft a sworn statement for an Arkansas court", "do I need
  a notary for my Arkansas affidavit", "draft a declaration under
  penalty of perjury in Arkansas", "affidavit in support of summary
  judgment Arkansas", "affidavit of service / affidavit of account".
  Produces a sworn affidavit (default) or unsworn declaration in
  Arkansas format, with personal-knowledge averments in numbered
  paragraphs and the correct jurat or penalty-of-perjury closing.
  Composes with `ar-statewide-format` for the caption and signature and
  with `ar-draft-motion` for the motion the affidavit supports.
version: 0.1.0
---

# Draft an Arkansas Affidavit or Declaration

> **NOT LEGAL ADVICE.** This skill scaffolds a court document as a
> drafting aid. The user — not the skill — is the declarant, chooses
> what facts to swear to, and signs the declaration. Verify every rule,
> deadline, and citation against current law before filing. Pair with
> substantive review by counsel where stakes warrant.

Use this skill to produce the sworn-facts document that carries the
evidence behind a motion, a default-judgment package, or a contested
hearing in Arkansas. **The Arkansas default is a notarized AFFIDAVIT**
— a written statement of facts sworn before a notary public or other
officer authorized to administer oaths, closed with a **jurat**
("Subscribed and sworn to before me..."). Where a sworn affidavit is
expressly required, use the affidavit form. Where an unsworn writing is
permitted, an unsworn **declaration under penalty of perjury** may
substitute. The caption, signature, and certificate of service follow
`ar-statewide-format`.

## Affidavit (default) vs. unsworn declaration

| Form | When to use | Closing |
|---|---|---|
| **Notarized affidavit** (default) | Rule 56 summary-judgment support; default-judgment proof; verifications; any filing where a rule or local practice requires a **sworn** statement | **Jurat** before a notary: "Subscribed and sworn to before me this ___ day of ____, 20__." |
| **Unsworn declaration under penalty of perjury** | Where the rule or local practice authorizes an unsworn writing in lieu of an affidavit | Penalty-of-perjury attestation dated and signed by the declarant, no notary |

> **Default to the affidavit and flag when sworn is required.** When in
> doubt, use the notarized affidavit form — it satisfies every
> requirement an unsworn declaration would and avoids a rejected
> filing. **Ark. R. Civ. P. 56** affidavits in particular must be made
> on **personal knowledge**, set out facts that would be **admissible
> in evidence**, and show the affiant is **competent to testify** to
> the matters stated; verifications and default-judgment proof are also
> commonly required to be sworn. Verify whether the specific filing
> requires a sworn affidavit in `references/` and the local rules of
> the filing court.

## Affidavit structure (default form)

```
                    [Caption — see ar-statewide-format]

           AFFIDAVIT OF [NAME] IN SUPPORT OF
           [MOTION / DEFENSE]

STATE OF ARKANSAS    )
                     )  ss.
COUNTY OF __________  )

I, [Full Name], being first duly sworn upon oath, state as follows:

1. I am over the age of eighteen (18) and competent to testify to the
   matters stated herein. I make this Affidavit upon my personal
   knowledge.

2. [Fact — one fact per numbered paragraph. Stick to what the affiant
   personally knows, saw, did, or received. Attach and identify any
   exhibit: "A true and correct copy of [document] is attached as
   Exhibit __."]

3. [Fact.]

FURTHER AFFIANT SAYETH NAUGHT.

                                        ____________________________
                                        [Affiant Name]

                              JURAT

SUBSCRIBED AND SWORN TO before me this ___ day of __________, 20__.

                                        ____________________________
                                        Notary Public
My commission expires: __________
```

## Unsworn declaration (where authorized)

```
                    [Caption — see ar-statewide-format]

           DECLARATION OF [NAME]

1. I am over the age of eighteen (18) and have personal knowledge of
   the facts stated below.

2. [Fact.]

I declare under penalty of perjury under the laws of the State of
Arkansas that the foregoing is true and correct.

Executed on [date], at [city, state].

                                        ____________________________
                                        [Declarant Name]
```

## Drafting rules for sworn facts

1. **Personal knowledge only.** The affiant swears to what they
   personally know, did, saw, or received — not to argument, opinion,
   or hearsay. Phrases like "I am informed and believe" weaken an
   affidavit and may be stricken on a Rule 56 motion.
2. **One fact per paragraph, numbered** (consistent with Rule 10(b)).
3. **Lay the foundation for exhibits.** Attach each document as a
   labeled exhibit and identify it in the paragraph that relies on it;
   business records may be authenticated under Ark. R. Evid. 803(6) /
   902(11) (see `ar-consumer-debt` for the debt-buyer account-records
   chain-of-title posture).
4. **No legal conclusions.** Save the argument for the motion or brief
   (`ar-draft-motion`); the affidavit supplies the facts that the
   argument applies the law to.
5. **Match the motion.** Every record citation in the motion's
   statement of facts should trace to a paragraph of a filed affidavit.
6. **Redact** under Administrative Order No. 19 before filing (SSNs,
   account numbers, minors' identifiers); attach the certificate of
   compliance (see `ar-file-packet`).

## Common Arkansas affidavits

| Affidavit | Use |
|---|---|
| Affidavit in support of summary judgment | Rule 56 personal-knowledge proof of undisputed facts |
| Affidavit in support of default judgment | Proof of the debt/claim amount and entitlement (see `ar-post-judgment`, `ar-consumer-debt`) |
| Affidavit of service | Proof of how and when a paper was served |
| Verification / verified pleading | Sworn confirmation that pleading averments are true |
| Affidavit of account | Sworn statement of an account balance with attached records |
| Affidavit of indigency | Supporting a request to proceed without prepayment of fees |

## Composition

- For format, caption, and signature block: `ar-statewide-format`
- For the motion the affidavit supports: `ar-draft-motion`
- For the proposed order: `ar-draft-order`
- For default-judgment proof: `ar-post-judgment`, `ar-consumer-debt`
- For the venue overlay: `ar-pulaski`, `ar-benton`, `ar-washington`,
  `ar-county-courts`, `ar-district-courts`
- For pre-filing QC: `ar-quality-check`, `ar-fact-check`
- For pro se conventions: `ar-pro-se`

## References

- `references/affidavit-template.md` — annotated notarized-affidavit
  template with the Arkansas jurat
- `references/declaration-template.md` — unsworn penalty-of-perjury
  declaration template and when it is authorized
- `references/personal-knowledge.md` — drafting rules for admissible
  sworn facts under Ark. R. Civ. P. 56 and the Arkansas Rules of Evidence
