# Integration — End-to-end debt defense in Arizona Justice Court

## Prompt

I just got served with a lawsuit in an Arizona Justice Court. It's
a debt buyer claiming I owe about $4,000 on an old credit card that
I stopped paying years ago. Walk me through the whole thing — how
that court works, what I file and when, how to answer and raise my
defenses including that it might be too old, how to get their
paperwork, and how to format everything so it's accepted.

## Expected triggers

- `az-justice-courts`
- `az-consumer-debt`
- `az-first-30-days`
- `az-draft-motion`
- `az-statewide-format`
- `az-fact-check`

## Acceptance criteria

### Forum identification (az-justice-courts)

- [ ] Identifies the **Justice Court** as the limited-jurisdiction
      forum for the claim amount and that it proceeds under the
      **Justice Court Rules of Civil Procedure (JCRCP)**, NOT the
      ARCP — cite the controlling jurisdictional authority and **read
      the current civil jurisdictional cap from the references
      corpus** rather than asserting a number
- [ ] Notes Justice-Court-specific filing/answer mechanics (read
      current specifics from the corpus)

### Answer + affirmative defenses (az-first-30-days)

- [ ] States the time to answer comes from the applicable rule keyed
      to the manner of service (read current day counts from the
      corpus; note Justice-Court specifics) and applies the
      weekend/holiday roll-forward
- [ ] Answers each allegation and pleads affirmative defenses
      **affirmatively** (warning of waiver), including statute of
      limitations and lack of standing

### Substantive defense (az-consumer-debt)

- [ ] Raises **chain of title / standing** — the debt buyer must
      prove ownership via an admissible assignment chain (Ariz. R.
      Evid. 803(6) foundation)
- [ ] Raises the **statute of limitations** — cites **A.R.S. § 12-548
      / § 12-543** and reads the limitations period from
      `az-statutes-debt/` rather than asserting a number — and applies
      the **_Mertola_** acceleration accrual rule (read/verified from
      `key-cases.md`) to fix the accrual date
- [ ] Identifies the Arizona collection-agency / Consumer Fraud Act
      overlay (sections read from the corpus) paired with the federal
      **FDCPA**

### Discovery + dispositive motion (az-draft-motion)

- [ ] Uses the available Justice Court discovery to force production
      of the assignment chain and account records (read the scope and
      timing from the corpus)
- [ ] Triages a dispositive motion — frames a summary-judgment-style
      motion (read the Justice Court vehicle/timing from the corpus)
      for the SOL bar and/or the standing / no-admissible-ownership-
      evidence gap

### Formatting + verification (az-statewide-format / az-fact-check)

- [ ] All filings carry the proper caption + line numbering +
      self-represented signature (no bar number)
- [ ] Verifies every A.R.S. / rule / case citation against the corpus
      / a structured source before filing (does not assert cites from
      memory), and confirms the **JCRCP** rule set for the forum

## Common failure modes

- Treats the Justice Court matter like a Superior Court ARCP case or
  invents the jurisdictional cap
- Buries affirmative defenses instead of pleading them
  affirmatively
- Asserts the limitations period, jurisdictional cap, or *Mertola*
  holding from memory instead of the corpus
- Uses ARCP citations in a JCRCP forum
