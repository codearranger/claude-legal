# Integration — Dissolution intake in Arizona Family Court

## Prompt

I want to file for divorce in Arizona. I'm representing myself. We
were married eight years, own a house and two cars, both have
retirement accounts, there's a credit card in my name, and we have
two young kids. Walk me through how to start the case — which court
and rules, how property and the kids get handled, what I file, and
the deadlines I need to watch.

## Expected triggers

- `az-family-court`
- `az-family-law`
- `az-pro-se`
- `az-statewide-format`
- `az-deadlines`

## Acceptance criteria

### Forum + rule set (az-family-court)

- [ ] Identifies the **Superior Court of Arizona** (Family /
      Domestic-Relations division) as the dissolution forum and that
      the matter proceeds under the **Arizona Rules of Family Law
      Procedure (ARFLP)**, NOT the ARCP — reads the current filing
      mechanics from the references corpus
- [ ] Notes the **petition for dissolution** as the initiating
      document and any **residency** prerequisite and **statutory
      waiting period** before a decree may enter — reads the current
      day counts from the corpus rather than asserting them

### Property + debt (az-family-law)

- [ ] Frames Arizona as a **community-property** state — division of
      community property and debts under **A.R.S. § 25-211 / § 25-318**
      (the house, cars, retirement, and the credit card incurred
      during marriage) — reading the standard from `az-statutes-debt/`
      rather than asserting it
- [ ] Distinguishes separate property (read the governing section
      from the corpus)

### Legal decision-making + children (az-family-law)

- [ ] Uses **legal decision-making** terminology (not "custody") and
      frames the **best-interests** analysis under **A.R.S. § 25-403**,
      reading the factors from the corpus; notes parenting time and
      child support under the Arizona Child Support Guidelines (read
      governing sections from the corpus)

### Format + deadlines (az-pro-se / az-statewide-format / az-deadlines)

- [ ] All filings carry the **Ariz. R. Civ. P. 10** caption (as
      applied in family matters), line numbering, and a
      **self-represented** signature (no State Bar of Arizona number)
- [ ] Applies time computation and any service-related deadlines
      (response to the petition, service of process) reading the
      current method and day counts — including the weekend/holiday
      roll-forward — from the corpus via `az-deadlines`

## Common failure modes

- Applies the ARCP instead of the ARFLP to the dissolution
- Treats Arizona as an equitable-distribution (non-community-
  property) state
- Uses "custody" instead of legal decision-making, or lists § 25-403
  factors from memory
- Asserts the residency requirement, waiting period, or any day
  count from memory instead of the corpus
- Adds a bar number to the self-represented signature block
