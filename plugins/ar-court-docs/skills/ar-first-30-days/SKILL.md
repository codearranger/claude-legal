---
name: ar-first-30-days
description: >
  Use when an Arkansas defendant has just been served with a civil
  complaint and summons. Covers the matter-neutral response window:
  the answer deadline under Ark. R. Civ. P. 12 (30 days for a resident;
  a longer period for a nonresident / out-of-state defendant — see
  references), the Rule 12(b) motion-to-dismiss triage including the
  Rule 12(b)(6) "failure to state facts upon which relief can be
  granted" motion under Arkansas's FACT-PLEADING standard, affirmative
  defenses under Rule 8(c), counterclaims under Rule 13, and default
  under Rule 55. Triggers include "I was served in Arkansas", "Arkansas
  answer deadline", "how long do I have to answer in Arkansas", "30 days
  to answer Arkansas", "motion to dismiss Arkansas", "Ark. R. Civ. P.
  12(b)(6)", "failure to state a claim Arkansas", "fact pleading
  Arkansas", "affirmative defenses Arkansas", "counterclaim Arkansas",
  "default judgment against me Arkansas", "I got sued by a debt
  collector in Arkansas". Routes to ar-discovery, ar-pro-se, and the
  subject bundles.
version: 0.1.0
---

# Arkansas — First 30 Days After Service

> **NOT LEGAL ADVICE.** This skill is a procedural and drafting aid,
> not legal advice. Deadlines are jurisdictional — missing the answer
> date can cost you the case by default. Verify the current Ark. R.
> Civ. P. day counts and the venue's local rules immediately, and
> consider consulting a licensed Arkansas attorney where stakes
> warrant.

You have been served with a complaint and summons. Act on the
**deadline first**, then decide **how** to respond. Use this skill with
`ar-law-references` (rule lookups), `ar-pro-se` (self-represented
conventions + service), `ar-discovery` (developing the facts), and the
subject bundle that fits the case (e.g., `ar-consumer-debt`,
`ar-landlord-tenant`, `ar-family-law`).

## Step 1 — Pin the answer deadline (Ark. R. Civ. P. 12)

A defendant must serve a response within the time set by **Ark. R.
Civ. P. 12**:

- A **resident** defendant served in Arkansas generally has **30 days**
  after service of the summons and complaint.
- A **nonresident / out-of-state** defendant has a **longer** period
  (and service on certain governmental and other defendants has its
  own count). **Verify the exact day counts** in `ar-law-references` /
  `references/civil-rules.md` — do not assume 30 days applies.
- Add the **Ark. R. Civ. P. 6(d) mail add-on** where a deadline runs
  from service by mail; compute weekends and Arkansas holidays under
  Ark. R. Civ. P. 6(a). Use the deadline-arithmetic tooling /
  `ar-deadlines`.

> **Initial service is Ark. R. Civ. P. 4, not Rule 5.** The complaint
> and summons must have been served under the stricter **Rule 4**
> process. If service was defective (wrong method, wrong person,
> outside the service window), that is itself a Rule 12(b) defense —
> see Step 3. Subsequent papers are served under Rule 5 (see
> `ar-pro-se`).

Filing **something** by the deadline — an answer or a proper Rule 12
motion — is what stops a default.

## Step 2 — The fork: answer, or move under Rule 12(b)

You respond either by **answering** the complaint or by filing a
**Rule 12(b) motion** that raises one or more threshold defenses. A
proper Rule 12 motion filed within the answer period **suspends** the
time to answer until the court rules (verify the post-ruling answer
window in `references/civil-rules.md`).

### The answer (Ark. R. Civ. P. 8)

- **Admit, deny, or state lack of knowledge** as to each numbered
  paragraph of the complaint. An averment not denied may be **deemed
  admitted** — answer every paragraph.
- Plead your **affirmative defenses** (Step 4).
- Assert any **counterclaims** (Step 5).
- Follow the caption + numbered-paragraph format (`ar-statewide-format`)
  and the self-represented signature + certificate-of-service
  conventions (`ar-pro-se`).

## Step 3 — Rule 12(b) motion triage

**Ark. R. Civ. P. 12(b)** lists the defenses that may be raised by
motion. Triage the complaint against each:

| Rule 12(b) ground | When it applies |
|---|---|
| Lack of subject-matter jurisdiction | Wrong court for the kind of case (e.g., a claim that belongs before the Workers' Compensation Commission or the State Claims Commission) |
| Lack of personal jurisdiction | No constitutional / long-arm basis to haul this defendant into an Arkansas court |
| Improper venue | Filed in the wrong county / circuit |
| Insufficiency of process / of service of process | The summons or the Rule 4 service was defective |
| **Failure to state facts upon which relief can be granted (12(b)(6))** | The complaint, taken as true, still does not state a claim — see the fact-pleading note below |
| Failure to join a necessary party | A required party under Rule 19 is missing |

Some Rule 12(b) defenses are **waived** if not raised in the first
response (personal jurisdiction, venue, process, and service of
process); subject-matter jurisdiction and failure to state a claim are
treated differently. Confirm the current waiver and consolidation rules
in `references/civil-rules.md` before omitting a defense.

> **ARKANSAS IS A FACT-PLEADING STATE — this drives Rule 12(b)(6).**
> Ark. R. Civ. P. 8(a) requires "a statement in ordinary and concise
> language of **facts** showing that the pleader is entitled to
> relief." Arkansas does **not** follow federal notice pleading — a
> complaint that recites only **legal conclusions** (e.g., "Defendant
> owes Plaintiff $X on an account") **without pleading the underlying
> facts** is vulnerable to a Rule 12(b)(6) motion. On a 12(b)(6)
> motion the court treats the facts pleaded as true but **disregards
> mere conclusions**, and looks only at the complaint and its attached
> exhibits. This is the single most important Arkansas-specific point
> in the first 30 days: in a debt-buyer or other documentary case, test
> whether the complaint actually pleads the **facts** of the contract,
> the assignment chain, and the amount due — or just asserts the
> conclusion.

> **The 12(b)(6) → summary-judgment conversion.** If a Rule 12(b)(6)
> motion (or the response to it) presents matters **outside the
> pleadings** and the court does not exclude them, the motion is
> **treated as a Rule 56 summary-judgment motion** and all parties get
> a reasonable opportunity to present Rule 56 material. Under Arkansas's
> summary-judgment standard, once the movant makes a prima facie
> showing the non-movant must **"meet proof with proof"** and show a
> genuine issue of material fact (*Wallace v. Broyles*; *Flentje v.
> First Nat'l Bank of Wynne*). Don't accidentally convert your motion
> by attaching outside evidence unless you mean to. See
> `references/key-cases.md`.

## Step 4 — Affirmative defenses (Ark. R. Civ. P. 8(c))

Affirmative defenses must be **pleaded affirmatively** in the answer or
they may be **waived**. The catalog includes (non-exhaustive):

- **Statute of limitations** — the most common debt-defense; the
  written-contract, oral-contract / open-account, and tort limitations
  periods differ. Look up the applicable period and the accrual rule in
  `ar-law-references` (Ark. Code Ann. Title 16, ch. 56).
- Payment, release, accord and satisfaction, discharge in bankruptcy.
- Failure of consideration, fraud, illegality, estoppel, waiver.
- **Lack of capacity / standing** — in a debt-buyer case, that the
  plaintiff has not proven the **chain of title** from the original
  creditor, or that an unlicensed collection agency lacks capacity (the
  Arkansas State Board of Collection Agencies licensing regime, Ark.
  Code Ann. § 17-24-101 et seq.). See `ar-consumer-debt`.
- Statute of frauds; arbitration / forum-selection.

Plead the **facts** supporting each defense — Arkansas's fact-pleading
posture applies to your answer too.

## Step 5 — Counterclaims (Ark. R. Civ. P. 13)

- **Compulsory counterclaims** (Rule 13(a)) — a claim you have against
  the opposing party that **arises out of the same transaction or
  occurrence** must be pleaded now or it is **lost**. Identify any such
  claim before you file.
- **Permissive counterclaims** (Rule 13(b)) — unrelated claims you may,
  but need not, bring.
- A counterclaim can flip a consumer-debt case: e.g., an **FDCPA**
  counterclaim (15 U.S.C. § 1692) for abusive collection conduct. See
  `ar-consumer-debt`.

## Step 6 — If a default is looming or entered (Ark. R. Civ. P. 55)

- A defendant who does not respond within the time allowed risks a
  **default judgment** under **Ark. R. Civ. P. 55**.
- If a default has been **entered but not reduced to judgment**, or a
  default **judgment** has been entered, Rule 55 provides for **setting
  it aside** for good cause / the enumerated grounds. Act fast — and
  note the **90-day Rule 60(a)** window in which a circuit court may
  modify or vacate a judgment to correct error (after 90 days, only the
  narrower Rule 60(c) grounds apply). See `ar-law-references` /
  `references/civil-rules.md` and `ar-post-judgment`.

## The first-30-days checklist

1. **Calendar the answer deadline** today (Rule 12; resident vs.
   nonresident counts; Rule 6 add-ons).
2. **Read the complaint paragraph by paragraph** and the attached
   exhibits (Rule 10(c)).
3. **Triage Rule 12(b)** — is there a jurisdiction / venue / service /
   **12(b)(6) fact-pleading** defense?
4. **List affirmative defenses** (Rule 8(c)) — limitations first.
5. **Identify compulsory counterclaims** (Rule 13(a)) — use them or
   lose them.
6. **Draft** the answer or Rule 12 motion (`ar-statewide-format`,
   `ar-draft-motion`, `ar-pro-se`).
7. **Redact** under Administrative Order No. 19; **serve** under Rule
   5 with a certificate of service; **file** with the clerk.

## Composition

- For rule / statute / case lookups: `ar-law-references`
- For caption + format: `ar-statewide-format`
- For self-represented conventions, service, and redaction: `ar-pro-se`
- For drafting the motion or answer: `ar-draft-motion`,
  `ar-draft-declaration`
- For developing the facts after you respond: `ar-discovery`
- For deadline arithmetic: `ar-deadlines`
- For setting aside a default / post-judgment relief: `ar-post-judgment`
- For the matter-specific defense: `ar-consumer-debt`,
  `ar-landlord-tenant`, `ar-family-law`, and the other subject bundles

## References

- See `ar-law-references/references/civil-rules.md` for the Ark. R.
  Civ. P. 8 / 12 / 13 / 55 / 56 / 60 detail, the answer-deadline day
  counts, and the 12(b) waiver/consolidation rules.
- See `ar-law-references/references/key-cases.md` for the fact-pleading
  and summary-judgment ("meet proof with proof") authorities.
