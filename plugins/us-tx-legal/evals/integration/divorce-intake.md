# Integration — Texas divorce intake (residency, waiting period, SAPCR)

## Prompt

I want to file for divorce in Texas. We've lived in Texas for two
years and in this county for the last 8 months. We have two kids and a
house we bought during the marriage. I make $4,000 a month. Walk me
through what I need to file and what to expect on the children and
support, and start the petition.

## Expected triggers

- `tx-family-law`
- `tx-family-court`
- `tx-statewide-format`

## Acceptance criteria

### Residency + grounds + venue

- [ ] Confirms **residency under Fam. Code § 6.301** — a party must
      have been a domiciliary of Texas for the preceding **6 months**
      and a resident of the county for the preceding **90 days**; the
      user's 2 years in state / 8 months in county **satisfies** both
- [ ] Notes the no-fault ground of **insupportability (§ 6.001)** and
      that divorce is heard in **District Court** (Petitioner /
      Respondent), routing venue specifics to `tx-family-court`

### Waiting period

- [ ] States the **60-day waiting period (Fam. Code § 6.702)** — the
      court may not grant the divorce before the 60th day after the
      petition is filed (limited exceptions) — and frames it as a
      framework anchor, confirming against
      `../tx-law-references/references/family-rules.md`

### Community property

- [ ] Identifies the **house bought during marriage** as presumptively
      **community property (§ 3.003)** subject to a **"just and right"
      division (Ch. 7)**, and recommends a community-property
      **inventory**

### SAPCR / child support

- [ ] Frames the children's issues as a **SAPCR** with a rebuttable
      presumption of **joint managing conservators (§ 153.131)** and a
      **Standard Possession Order (§ 153.252)**, best interest under the
      **Holley** factors
- [ ] Explains child support uses the **percentage-of-obligor-net-
      resources model (Fam. Code Ch. 154)** — guideline percentages
      step up by number of children — applies the **two-children**
      guideline percentage to the user's stated $4,000/month as a
      framework illustration, while reading the **current net-resources
      cap** and the guideline percentages from
      `../tx-law-references/references/family-rules.md` /
      `tx-statutes-debt/` rather than hard-coding them

### Form

- [ ] Starts an **Original Petition for Divorce** with the
      `tx-statewide-format` caption (Petitioner v. Respondent), the
      TRCP 47(c) relief statement, line numbering, and footer
- [ ] Notes the **TRCP 145 Statement of Inability** option for costs

## Common failure modes

- Gets the § 6.301 6-month/90-day residency test wrong, or says the
  user doesn't qualify
- Omits the 60-day § 6.702 waiting period
- Recites the net-resources cap or guideline percentages from memory
- Treats the marital house as separate property
- Uses Plaintiff/Defendant instead of Petitioner/Respondent
