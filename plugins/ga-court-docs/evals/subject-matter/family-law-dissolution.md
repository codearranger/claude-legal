# ga-family-law — Divorce: Superior Court, equitable distribution, 30-day wait

## Prompt

My spouse and I want to divorce in Georgia. We've lived here for years, we
have two kids (ages 8 and 11), a house, and some retirement accounts. How
does a Georgia divorce work, where do I file, and how are the kids and
property handled?

## Expected triggers

- `ga-family-law`
- `ga-family-court`

## Acceptance criteria

### Forum, grounds, and residency

- [ ] States that divorce is heard **exclusively in Superior Court**
      (Ga. Const. art. VI) — never State or Magistrate Court — and uses
      **Petitioner / Respondent** designations
- [ ] States the **bona fide residency** requirement under **O.C.G.A.
      § 19-5-2** (resident six months before filing; venue is the
      defendant/respondent's county) — reads the period from the corpus
- [ ] Identifies the **no-fault ground** ("irretrievably broken,"
      O.C.G.A. § 19-5-3(13)) among the 13 statutory grounds, and notes the
      **30-day-from-service** minimum before a no-fault decree — reads the
      waiting period from the corpus rather than asserting days from memory

### Property division (equitable distribution)

- [ ] States Georgia is an **equitable-distribution** state (NOT community
      property) — marital property is divided equitably, not necessarily
      50/50 — anchored to **Stokes v. Stokes, 246 Ga. 765 (1980)** —
      verified against `key-cases.md`
- [ ] Notes that **separate property** (gift / inheritance / pre-marital)
      is generally not divided unless commingled (O.C.G.A. § 19-3-9), and
      that dividing **retirement accounts** requires a **QDRO** — flags
      this as needing specialized assistance

### Children (custody + parenting plan)

- [ ] Uses **O.C.G.A. § 19-9-3** best-interest standard (judge, not jury;
      no presumption for either parent) and notes a **parenting plan is
      mandatory** under O.C.G.A. § 19-9-1 — reads the factors from the
      corpus
- [ ] Notes the **child-election** rule: at age **14+** a child may select
      the custodial parent (controlling unless not in the best interest);
      ages **11-13** the preference is considered but not controlling —
      reads § 19-9-3(a)(5)/(6) from the corpus rather than asserting the
      ages from memory
- [ ] Routes child support to the income-shares analysis
      (`child-support-income-shares.md`)

## Common failure modes

- Says divorce can be filed in State Court (it is Superior-Court-exclusive)
- Describes Georgia as a community-property state
- Asserts the child-election ages from memory instead of reading
  § 19-9-3 from the corpus
- Cites *Stokes v. Stokes* without verifying it against `key-cases.md`
- Omits the QDRO requirement for retirement accounts
