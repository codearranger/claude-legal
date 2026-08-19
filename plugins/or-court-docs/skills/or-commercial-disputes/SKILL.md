---
name: or-commercial-disputes
description: >
  Subject-matter bundle for Oregon commercial-litigation matters —
  breach of contract (Oregon contract law, ORS 72 UCC Sales), Oregon
  Unlawful Trade Practices Act (UTPA, ORS 646.605), Oregon LLC Act
  (ORS Chapter 63), Oregon Business Corporation Act (ORS Chapter 60),
  breach of fiduciary duty, fraud, trade secrets (Oregon UTSA, ORS
  93.100), mandatory arbitration under ORAM (ORS 36.400), and
  commercial-lease disputes. Triggers include "Oregon commercial
  dispute", "breach of contract Oregon", "ORS 72 UCC Oregon",
  "Oregon UTPA business", "ORS 646.605 business", "Oregon LLC
  ORS 63", "Oregon corporation ORS 60", "trade secrets Oregon",
  "ORAM mandatory arbitration Oregon", "commercial lease Oregon".
  Composes with or-statewide-format, or-multcc / or-wccc /
  or-county-courts, or-discovery, or-deadlines.
version: 0.1.0
---

# Oregon Commercial Disputes — Subject-Matter Bundle

> **NOT LEGAL ADVICE.** Oregon's commercial law is largely
> harmonized with the UCC and Uniform Acts but has state-specific
> nuances in the LLC Act, corporations, and the UTPA. Verify all
> cites against current ORS. For complex commercial disputes,
> consult a licensed Oregon business attorney.

## At a glance

- **Contract law**: Oregon common law + ORS Chapter 72 (UCC Article 2
  Sales) + ORS Chapter 79A (UCC Article 9 Secured Transactions)
- **Business entities**: ORS Chapter 60 (Oregon Business Corporation
  Act, OBCA) + ORS Chapter 63 (Oregon LLC Act, OLLCA)
- **Unfair competition**: Oregon UTPA (ORS 646.605) applies to
  business-to-business transactions as well as consumer transactions
- **Trade secrets**: Oregon Uniform Trade Secrets Act (ORS 93.100-93.180,
  but check — ORS is not the typical Oregon chapter for UTSA; verify
  the current ORS chapter for the Oregon UTSA)
- **Arbitration**: Oregon Revised Uniform Arbitration Act (ORUAA,
  ORS 36.600-36.740); Oregon Mandatory Arbitration (ORAM, ORS 36.400
  et seq. — for cases at or below the jurisdictional cap in Circuit Court)

## Contract litigation

### Formation and enforceability

Oregon applies objective-theory contract formation. Key statutes:
- **ORS 72 (UCC Article 2)**: governs contracts for the sale of goods
  (movables); statute of frauds at ORS 72.2010 (contracts > $500
  must be written, or fall within exceptions)
- **Oregon statute of frauds** for non-goods contracts: ORS 41.580
  (contracts not to be performed within 1 year; conveyances of real
  property; guaranty; etc.)

### Breach and damages

Oregon applies the expectation-damages rule. Consequential damages
are recoverable if foreseeable at time of contracting (*Hadley v.
Baxendale* principle). The non-breaching party has a duty to mitigate.

**Attorney's fees in contract cases**: Oregon follows the American
Rule (each party pays their own fees) UNLESS a statute or the contract
itself provides for fees. See ORS 20.083 (reciprocal-fee provision:
if a contract provides fees to one party, fees are available to the
prevailing party regardless of which party prevails).

### UCC Article 2 (Sales) — ORS Chapter 72

Key provisions:
- **Perfect tender rule** (ORS 72.6010): buyer may reject for any
  non-conformity, but cure right arises (ORS 72.5080)
- **Warranty of merchantability** (ORS 72.3140) and **fitness for
  particular purpose** (ORS 72.3150)
- **4-year SOL** from breach (ORS 72.7250) — longer than the 6-year
  contract SOL for non-goods contracts

## Oregon Unlawful Trade Practices Act (UTPA) — ORS 646.605-646.656

The Oregon UTPA is a powerful tool in commercial disputes:
- Applies to **any person** engaged in trade or commerce (not limited
  to consumers) — B2B claims are available
- Broad list of prohibited practices at ORS 646.607-608
- Private right of action: actual damages + attorney's fees (mandatory
  to prevailing plaintiff) + injunctive relief; punitive available for
  malicious conduct
- **1-year SOL** from discovery; **6-year repose** (ORS 646.638(6))

**Mandatory demand letter prerequisite** (ORS 646.638(2)): before
filing a private UTPA action, the plaintiff must give the defendant
written notice of the alleged violation and demand for relief. If
the defendant cures within a reasonable time, no suit may be brought.
This is a **substantive precondition** to suit — not merely a
procedural requirement.

## Oregon LLC Act (OLLCA) — ORS Chapter 63

Oregon LLCs are governed by ORS Chapter 63. Key features:
- **Default = member-managed** (ORS 63.130); management may be vested
  in managers by operating agreement
- **Fiduciary duties** of members/managers: duty of loyalty (ORS
  63.155) + duty of care (ORS 63.160); operating agreement can
  adjust (within limits)
- **Dissolution**: voluntary (ORS 63.621); judicial dissolution for
  deadlock or oppression (ORS 63.661) — the primary commercial remedy
  for LLC disputes
- **Member withdrawal**: governed by operating agreement; dissociation
  and buyout rights under ORS 63.205-63.220

## Oregon Business Corporation Act (OBCA) — ORS Chapter 60

Key provisions for commercial disputes:
- **Shareholder oppression**: derivative suit (ORS 60.261) and direct
  suit (ORS 60.261) rights
- **Judicial dissolution** (ORS 60.661): available for deadlock,
  waste, oppression of minority shareholders
- **Fiduciary duties**: directors under the business-judgment rule
  (Oregon recognizes the BJR); see ORS 60.357
- **Piercing the corporate veil**: Oregon courts apply the *Amfac
  Foods, Inc. v. International Systems and Controls Corp.* factors —
  requires unity of interest + unjust enrichment

## Mandatory arbitration (ORAM)

Cases at or below the jurisdictional cap in the Circuit Court are
subject to **Oregon Mandatory Arbitration (ORAM)** under ORS 36.400
et seq. ORAM replaces the trial for smaller cases with binding
arbitration before a neutral arbitrator (trial de novo on appeal
available but with costs-shifting if the appealing party does not
improve their position by 10% or more).

**Jurisdictional cap**: set by the Oregon Supreme Court by rule. As
of recent years: $50,000. Verify the current cap at the OJD website.

## Composition

- `or-statewide-format` — UTCR 2.010 formatting
- `or-discovery` — commercial discovery (trade secrets protective
  orders, ORCP 44 business-records subpoenas, electronically stored
  information under ORCP 43)
- `or-deadlines` — SOL tracking (1 yr UTPA; 4 yr UCC; 6 yr contract)
- `or-multcc` / `or-wccc` / `or-county-courts` — venue
