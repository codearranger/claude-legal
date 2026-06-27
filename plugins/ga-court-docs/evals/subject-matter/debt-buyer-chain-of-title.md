# ga-consumer-debt — Debt-buyer standing / chain of title + § 24-8-803(6) records

## Prompt

A company I've never dealt with sued me in the State Court of Gwinnett
County claiming they bought my old credit card account from a bank. They
attached only a spreadsheet and a generic affidavit saying they bought a
"pool" of accounts. Do they actually own my debt, and how do I raise that
defense?

## Expected triggers

- `ga-consumer-debt`
- `ga-first-30-days`
- `ga-draft-motion`

## Acceptance criteria

### Standing / chain of title

- [ ] Frames the core defense: a **debt buyer must prove it owns the
      specific account** through an **unbroken, admissible chain of
      assignments** from the original creditor through each intermediate
      purchaser to the plaintiff — anchored to **Nyankojo v. North Star
      Capital Acquisition, 298 Ga. App. 6 (2009)** (reversed summary
      judgment for failure to prove the assignment chain) — verified
      against `key-cases.md` rather than asserted from memory
- [ ] Notes that a generic "pool" affidavit without an account-specific
      exhibit may be **insufficient**, citing **Wirth v. CACH, LLC,
      300 Ga. App. 488 (2009)** and **Rutledge v. Gemini Capital Group,
      LLC, 327 Ga. App. 454 (2014)** on the account-stated /
      business-records foundation — verified against `key-cases.md`

### Business-records foundation (O.C.G.A. § 24-8-803(6))

- [ ] Ties admissibility of the account records to the **business-records
      exception, O.C.G.A. § 24-8-803(6)** — records made at/near the time
      by a person with knowledge and a business duty, kept in the regular
      course — and the **§ 24-9-902(11)** self-authentication-by-certificate
      route — reads the foundation elements from the corpus rather than
      asserting them from memory
- [ ] Flags the debt-buyer battleground: the original creditor's records
      are **incorporated third-party records**, so the plaintiff must
      establish the original creditor's business duty and trustworthiness,
      not just its own

### Pleading and discovery

- [ ] Routes the standing challenge into the **answer as an affirmative
      defense** and a later **summary-judgment** motion
      (O.C.G.A. § 9-11-56), and uses discovery (RFPs under § 9-11-34) to
      force production of the full assignment chain and the original
      cardmember agreement (cross-reference `ga-discovery`)

## Common failure modes

- Treats the generic "pool" affidavit as conclusive proof of ownership
- Asserts the § 24-8-803(6) foundation elements from memory without the
  corpus
- Cites *Nyankojo* / *Wirth* / *Rutledge* without verifying them against
  `key-cases.md`
- Misses that the original creditor's records are incorporated
  third-party records requiring their own foundation
