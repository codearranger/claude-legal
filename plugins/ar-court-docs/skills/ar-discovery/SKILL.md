---
name: ar-discovery
description: >
  Use when drafting, responding to, or compelling discovery in an
  Arkansas civil case in Circuit Court. Covers the Ark. R. Civ. P.
  26–37 framework: interrogatories under Rule 33 (Arkansas DOES allow
  interrogatories, subject to a presumptive numeric cap), requests for
  production under Rule 34, requests for admission under Rule 36,
  depositions under Rule 30/31, the good-faith meet-and-confer
  requirement, and the Rule 37 motion-to-compel / sanctions workflow.
  Triggers include "Arkansas discovery", "Ark. R. Civ. P. 26",
  "interrogatories under Rule 33", "how many interrogatories can I serve
  in Arkansas", "Request for Production Arkansas", "Rule 34 Arkansas",
  "Request for Admission Rule 36", "deposition Rule 30 Arkansas",
  "motion to compel Arkansas", "Rule 37 sanctions Arkansas", "discovery
  response deadline Arkansas", "meet and confer Arkansas", "discovery
  dispute Arkansas", "privilege log Arkansas". Covers the response
  window, the interrogatory cap, the deemed-admitted trap on RFAs, and
  the conferral-then-compel sequence.
version: 0.1.0
---

# Arkansas Discovery

> **NOT LEGAL ADVICE.** This skill helps draft and respond to
> discovery. Verify against the current Ark. R. Civ. P. and the
> venue's local rules and any case-management order before serving or
> filing.

Use this skill alongside `ar-statewide-format`, `ar-law-references`,
`ar-pro-se`, and (where applicable) `ar-first-30-days`. The Arkansas
discovery framework lives in **Ark. R. Civ. P. 26–37** and applies in
**Circuit Court**.

> **Arkansas is a fact-pleading jurisdiction.** Because Ark. R. Civ. P.
> 8(a) requires the complaint to plead **facts** (not conclusions),
> discovery is where you develop and pin down those facts — and where a
> consumer-debt or other documentary defendant tests whether the
> plaintiff can actually prove the elements it pleaded (e.g., the chain
> of title and the business-records foundation under Ark. R. Evid.
> 803(6) / 902(11)). See `ar-first-30-days` and `ar-law-references`.

> **District Court is a limited-jurisdiction forum.** Discovery
> practice in District Court (and especially the small claims
> division) is constrained — confirm what is available before serving
> a full discovery set there. See `ar-district-courts`. The full Ark.
> R. Civ. P. 26–37 toolkit described here is Circuit Court practice.

## Snapshot — Arkansas written-discovery clock

| Discovery device | Rule | Response due |
|---|---|---|
| Interrogatories | Ark. R. Civ. P. 33 | the rule's response window after service |
| Requests for Production | Ark. R. Civ. P. 34 | the rule's response window after service |
| Requests for Admission | Ark. R. Civ. P. 36 | the rule's response window after service |

Frame these as the **current** day counts — verify the exact response
window (and any shorter period for requests served with the summons or
a longer one for a defendant served before answering) against Ark. R.
Civ. P. 33 / 34 / 36 in `ar-law-references` /
`references/civil-rules.md`. Add the **Ark. R. Civ. P. 6(d) mail
add-on** when service was by mail.

## Scope — Ark. R. Civ. P. 26

Discovery scope is broad: a party may obtain discovery of any matter,
**not privileged**, that is **relevant** to the subject matter of the
pending action and reasonably calculated to lead to the discovery of
admissible evidence, subject to the protective-order and limitation
provisions of Rule 26. Privileged matter must be **withheld with a
privilege log** that describes the withheld material so the requesting
party can assess the claim. See `references/privilege-log.md`.

## Interrogatories — Ark. R. Civ. P. 33

**Arkansas allows written interrogatories.** Rule 33 imposes a
**presumptive numeric cap** on the number of interrogatories
(**including discrete subparts**) a party may serve without leave of
court or a stipulation.

> **Verify the cap.** Look up the current presumptive limit in
> `ar-law-references` / `references/civil-rules.md` before serving — it
> is a fixed number (counting subparts), and exceeding it without leave
> or stipulation invites an objection. A venue's local rules or a
> case-management order may also adjust limits.

- Each interrogatory is answered **separately and fully, in writing,
  under oath**; any objection is stated with specificity in lieu of an
  answer.
- Service: after commencement of the action, subject to any
  case-management order.

```
INTERROGATORIES

Pursuant to Ark. R. Civ. P. 33, [Defendant] requests that [Plaintiff]
answer the following Interrogatories separately and fully in writing
under oath, and serve the answers on the undersigned within the time
allowed by the Rule.

INTERROGATORY NO. 1: State the name, address, and telephone number of
each person known to you to have knowledge of the facts alleged in the
Complaint, and describe the subject of that knowledge.

ANSWER:
[Response]

INTERROGATORY NO. 2: [...]
```

## Requests for Production — Ark. R. Civ. P. 34

- Service: after commencement of the action.
- The responding party must produce documents as they are **kept in
  the usual course of business**, or organized and labeled to
  correspond to the categories in the request.
- **ESI**: produce in a reasonably usable form; preserve metadata
  unless the parties agree otherwise.
- In a documentary case, RFPs are how you demand the **underlying
  account documents and assignment chain** — the original agreement,
  the account statements, and each bill of sale / assignment in the
  chain of title — rather than a summary affidavit.

## Requests for Admission — Ark. R. Civ. P. 36

- Service: after commencement of the action.
- **Critical deemed-admitted trap**: a matter is **deemed admitted**
  unless the party **timely** serves a written answer or objection.
  Calendar RFA deadlines carefully — a missed deadline can concede
  dispositive facts (e.g., the validity of a signature, the existence
  of an account).
- A party may move to **withdraw or amend** an admission when doing so
  would serve the presentation of the merits and the requesting party
  is not prejudiced.

## Depositions — Ark. R. Civ. P. 30 / 31

- **Rule 30** — oral depositions; **Rule 31** — depositions on written
  questions.
- Notice: serve **reasonable** written notice stating the time, place,
  and deponent. For an entity deposition, describe the matters for
  examination so the entity can designate a witness to testify on its
  behalf.
- Non-party documents and attendance: a deposition notice may be
  accompanied by a **subpoena** under Ark. R. Civ. P. 45.
- Remote / video depositions are permitted by stipulation or court
  order; confirm the recording method in advance.

## Meet-and-confer

Before filing a discovery motion, **confer** with the opposing party
(or counsel) to attempt informal resolution, and **document** the
attempt. Arkansas practice — and many venues' local rules and case
plans — expect a **good-faith conferral** before a motion to compel.
Confirm the venue's requirement in `ar-law-references`.

```
Subject: Conferral re: Discovery Responses — [Case Short Title],
         No. [CV-__-____]

[Name / counsel],

This message is my good-faith effort to confer before I file a Motion
to Compel under Ark. R. Civ. P. 37.

Your responses to my [Interrogatories / Requests for Production],
served on [DATE], are deficient as follows:

  1. Interrogatory No. 3 — Boilerplate objection ("vague, overly
     broad, unduly burdensome") without specifying which terms are
     vague or quantifying the burden.

  2. RFP No. 7 — No documents produced; the response states none
     exist, yet the Complaint references documents within this request.

  [...]

Please supplement by [date 7-10 days out]. If I do not hear from you, I
will proceed with a Motion to Compel and seek expenses under Ark. R.
Civ. P. 37.

[Name], Pro Se
```

## Motion to compel — Ark. R. Civ. P. 37

If conferral fails, move to compel under **Ark. R. Civ. P. 37**. The
motion should:

1. **Identify the specific deficiencies** (which interrogatory / RFP /
   RFA, and why the response is inadequate).
2. **Attach** the requests and the responses as exhibits.
3. **Document the conferral attempt** (a certificate of good-faith
   conferral, if the venue requires one).
4. **Address each objection** with specificity.
5. **Request specific relief**: an order compelling responses by a date
   certain, and an award of expenses.

### Sanctions

- **Ark. R. Civ. P. 37** authorizes, on a successful motion to compel,
  an award of the reasonable expenses (including attorney's fees)
  caused by the failure, unless the opposing position was
  substantially justified.
- For **disobedience of a discovery order**, Rule 37 authorizes
  stronger sanctions — up to striking pleadings, dismissal, or default
  judgment.
- Rule 37 also reaches failures to admit and failures to supplement.

Verify the current subpart lettering and the precise sanctions
catalog in the verbatim rule text (`references/court-rules/`).

## Composition

- For drafting the motion to compel: `ar-draft-motion`
- For the supporting declaration / affidavit: `ar-draft-declaration`
- For statewide format: `ar-statewide-format`
- For service and self-represented conventions: `ar-pro-se`
- For consumer-debt RFP / RFA banks and debt-buyer discovery strategy:
  `ar-consumer-debt`
- For deadline arithmetic: `ar-deadlines`
- For rule / statute / case lookups: `ar-law-references`

## References

- See `ar-law-references/references/civil-rules.md` for the Ark. R.
  Civ. P. 26–37 detail, the Rule 33 interrogatory cap, and the
  response windows.
- See `ar-law-references/references/evidence-rules.md` for the Ark. R.
  Evid. 803(6) / 902(11) foundation that discovery in a documentary
  case is built around.
