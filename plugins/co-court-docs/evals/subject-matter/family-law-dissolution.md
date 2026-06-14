# co-family-law — UDMA dissolution + 91-day waiting period + equitable distribution

## Prompt

My spouse and I want to divorce in Colorado. We've been
residents for a while, we have two kids (ages 8 and 11),
and we have a house and some retirement accounts. How does
a Colorado divorce work, and how are the kids and property
handled?

## Expected triggers

- `co-family-law`
- `co-deadlines`

## Acceptance criteria

### Grounds and residency

- [ ] States Colorado is a **no-fault, pure irreconcilable-
      differences** state under the **Uniform Dissolution
      of Marriage Act (UDMA)** at **C.R.S. art. 10 of
      title 14** — no fault-based grounds
- [ ] States the **91-day residency requirement** before
      filing under **C.R.S. § 14-10-106** and the
      **91-day waiting period** before a decree can
      enter — reads the current time requirements from
      the references corpus rather than asserting days
      from memory

### Property division (equitable distribution)

- [ ] States Colorado is an **equitable-distribution
      state** (NOT community property): marital property
      is divided equitably (not necessarily 50/50) under
      **C.R.S. § 14-10-113** factors — reads the
      current factors from the corpus
- [ ] Notes that **retirement accounts** require a
      **Qualified Domestic Relations Order (QDRO)** to
      divide without triggering tax penalties — flags
      this as requiring specialized assistance

### Parental responsibilities (C.R.S. § 14-10-124)

- [ ] Uses the correct Colorado terminology —
      **"allocation of parental responsibilities"**
      (decision-making + parenting time), NOT "custody"
      / "visitation"
- [ ] States the **best-interest factors** at
      **C.R.S. § 14-10-124** — reads the factor list
      from the corpus rather than asserting from memory
- [ ] Notes that a **permanent parenting plan** or
      agreed allocation order is required

### Financial disclosures (C.R.C.P. 16.2)

- [ ] Flags the mandatory **C.R.C.P. 16.2 Sworn
      Financial Statement (JDF 1111)** — both parties
      must exchange it within **42 days** of initial
      filing (reads the current deadline from the
      corpus); it is **not optional**

## Common failure modes

- Describes Colorado as a community-property state
- Asserts the waiting period as 60 days (not 91)
- Uses "custody" and "visitation" instead of the
  UDMA's "parental responsibilities" and
  "parenting time"
- Omits the C.R.C.P. 16.2 financial-disclosure
  requirement
- Fails to flag the QDRO requirement for retirement
  accounts
