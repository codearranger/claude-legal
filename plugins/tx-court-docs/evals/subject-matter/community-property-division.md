# tx-family-law — "just and right" community-property division

## Prompt

My spouse and I are divorcing in Texas. I owned a house before we
married, we bought a car together during the marriage, and I have a
401(k) I started before the wedding. How does Texas split all this?

## Expected triggers

- `tx-family-law`

## Acceptance criteria

### Community vs. separate characterization

- [ ] States Texas is a **community-property** state with a
      **community-property presumption (Fam. Code § 3.003)** —
      property possessed during or on dissolution of marriage is
      presumed community unless proven separate by **clear and
      convincing evidence**
- [ ] Characterizes the user's facts correctly as a framework: property
      owned **before marriage** (the house, the pre-marital portion of
      the 401(k)) is **separate**; property acquired **during marriage**
      (the car) is **community**; and flags that a mixed/commingled
      asset like the 401(k) requires **tracing** and that the community
      may have a reimbursement / characterization claim — routing the
      growth-vs-contribution question to the corpus / case-law

### Division standard

- [ ] States the court divides the **community estate** in a manner the
      court deems **"just and right"** under **Fam. Code Ch. 7
      (§ 7.001)** — and that "just and right" is **not necessarily
      50/50** — while the court **cannot divest a spouse of separate
      property**
- [ ] Reads any drift-prone figure (e.g., reimbursement statutory
      detail) from
      `../tx-law-references/references/family-rules.md` /
      `tx-statutes-debt/` rather than asserting it from memory

### Terminology

- [ ] Uses **Petitioner / Respondent** (family-law parties), not
      Plaintiff/Defendant

## Common failure modes

- Says Texas divides community property 50/50 as a rule
- Treats the pre-marital house or pre-marital 401(k) portion as
  community
- Suggests the court can award one spouse's separate property to the
  other
