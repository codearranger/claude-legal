# Integration — End-to-end General Sessions debt-defense

## Prompt

I just got served with a civil warrant from a debt buyer in
General Sessions Court in Tennessee. They want about $4,000 on
a credit card I haven't paid in years. Walk me through the
whole thing — what to file, how the court works, what
deadlines I'm on, and how to format what I file.

## Expected triggers

- `tn-general-sessions`
- `tn-consumer-debt`
- `tn-deadlines`
- `tn-statewide-format`
- `tn-pro-se`

## Acceptance criteria

### Forum identification (tn-general-sessions)

- [ ] Identifies the matter as a **General Sessions** civil
      case commenced by a **civil warrant** (informal practice;
      Tenn. R. Civ. P. generally do not apply except as made
      applicable)
- [ ] States the **$25,000 civil jurisdictional cap** (cite
      T.C.A. § 16-15-501; read the current figure from the
      references corpus) and that there is **no formal
      discovery as of right**
- [ ] Explains the **10-day de novo appeal to Circuit Court**
      (T.C.A. § 27-5-108) if the litigant loses

### Substantive defense (tn-consumer-debt)

- [ ] Raises **chain-of-title / standing** — the debt buyer
      must prove the assignment from the original creditor
- [ ] Identifies the **6-year SOL on written contracts / open
      accounts (T.C.A. § 28-3-109)** as a potential defense
      (accrual fact-dependent for revolving accounts)
- [ ] Cites the **2024 § 20-6-104** pre-default-judgment
      documentation rule for debt buyers
- [ ] Notes the **Collection Service Act** licensing point
      (T.C.A. § 62-20-105) with its § 62-20-105 set-aside limit
      and the **Pursell** TCPA caveat as fact-specific

### Deadlines (tn-deadlines)

- [ ] Identifies the General Sessions **appearance/return
      date on the civil warrant** as the operative date (NOT
      the 30-day Circuit Court answer clock) — cite the
      controlling authority and read current timing from the
      references corpus
- [ ] Applies **Tenn. R. Civ. P. 6.01** weekend/holiday
      roll-forward and the **§ 15-1-101** holiday list (Good
      Friday + Columbus Day observed) where a deadline is
      computed under the rules; notes the **Rule 6.05 3-day
      mail add-on** where applicable

### Formatting (tn-statewide-format)

- [ ] States Tennessee has **no statewide page/margin/font
      rule** — typography/page limits defer to **per-county
      local rules**; gives common-practice defaults (Letter,
      1-inch margins, 12-pt) as defaults, not mandates
- [ ] Anything filed carries a Tenn. R. Civ. P. **10.01**-style
      caption + **Rule 11** signature; self-represented
      signature block (no bar number)

## Common failure modes

- Treats the General Sessions matter like a Circuit Court
  summons-and-complaint with a 30-day answer clock
- Promises formal discovery in General Sessions
- Misses the 2024 § 20-6-104 documentation rule
- Invents a statewide format mandate with hard margin/font
  numbers
- States a 30-day appeal instead of the 10-day de novo appeal
