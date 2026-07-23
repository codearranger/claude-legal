# Integration — Georgia divorce intake: Superior Court, parenting plan, child support

## Prompt

My spouse and I have decided to divorce. We've lived in Cobb County,
Georgia for several years. We have two kids (ages 9 and 12), a house we
both own, two cars, and retirement accounts. Walk me through the full
process from filing to decree — where I file, what's mandatory, how the
kids and property are handled, and the key deadlines.

## Expected triggers

- `ga-family-law`
- `ga-family-court`
- `ga-deadlines`
- `ga-file-packet`
- `ga-statewide-format`

## Acceptance criteria

### Forum, residency, grounds (ga-family-law)

- [ ] Confirms divorce is **Superior-Court-exclusive** — files in the
      **Superior Court of Cobb County, State of Georgia** with
      **Petitioner / Respondent** designations and **"Civil Action File
      No."**
- [ ] Confirms the **O.C.G.A. § 19-5-2** bona fide residency requirement
      is satisfied and identifies the no-fault ground ("irretrievably
      broken," § 19-5-3(13)) plus the **30-day-from-service** minimum
      before a no-fault decree — reads the periods from the corpus

### Cobb domestic standing order (ga-family-court / ga-cobb)

- [ ] Flags that Cobb auto-attaches a **Domestic Relations Standing Order
      / Rule Nisi** via PeachCourt at filing (restraining asset
      dissipation, child removal, insurance changes, etc.) and a
      **Co-Parenting / Divorcing Parents seminar** requirement (USCR 24.8)
      — reads the current Cobb standing-order terms from the references
      rather than asserting them from memory
- [ ] Notes the **USCR 24.2 Domestic Relations Financial Affidavit (DRFA)**
      and child-support worksheet must be filed on the rule's schedule
      (read the lead-time from the corpus)

### Property + children

- [ ] States Georgia is an **equitable-distribution** state (*Stokes v.
      Stokes*, verified against `key-cases.md`); house and retirement are
      likely marital; flags the **QDRO** for retirement accounts
- [ ] Requires a **mandatory parenting plan** (O.C.G.A. § 19-9-1) under the
      § 19-9-3 best-interest standard, noting the child-election ages
      (read § 19-9-3(a)(5)/(6) from the corpus)
- [ ] Computes child support via the **income-shares O.C.G.A. § 19-6-15**
      worksheet / Commission calculator — reading the **current
      post-January-1-2026 text** from the corpus, not a remembered version

### Deadlines + filing (ga-deadlines / ga-file-packet / ga-statewide-format)

- [ ] Applies **§ 9-11-6(a) / § 1-3-1(d)(3)** time computation with the
      § 1-4-1 holiday list for any response/hearing dates — reads counts
      from the corpus
- [ ] E-files through **PeachCourt** (Cobb) with each document (petition,
      DRFA, proposed parenting plan, child-support worksheet) as a separate
      attachment; routes an indigent filer to the § 9-15-2 / § 9-11-3
      poverty affidavit

## Common failure modes

- Files the divorce in State or Magistrate Court instead of
  Superior-Court-exclusive
- Describes Georgia as a community-property state
- Omits the Cobb auto-attached domestic standing order and parenting
  seminar
- Relies on a pre-2026 version of § 19-6-15 for child support
- Routes the Cobb filing to Odyssey eFileGA instead of PeachCourt
- Uses "custody/visitation" loosely without the mandatory parenting plan
