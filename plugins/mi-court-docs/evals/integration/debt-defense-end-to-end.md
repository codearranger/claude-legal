# Integration — End-to-end debt defense in the 36th District Court

## Prompt

I just got served with a lawsuit in the 36th District Court in
Detroit. It's a debt buyer claiming I owe about $4,000 on an
old credit card. Walk me through the whole thing — how that
court works, what I file and when, how to answer and raise my
defenses, how to get their paperwork in discovery, and how to
format everything so it's accepted.

## Expected triggers

- `mi-first-30-days`
- `mi-consumer-debt`
- `mi-36th-district`
- `mi-district-courts`
- `mi-draft-motion`
- `mi-statewide-format`
- `mi-fact-check`

## Acceptance criteria

### Forum identification (mi-36th-district / mi-district-courts)

- [ ] Identifies the **36th District Court (Detroit)** as the
      forum and the **District Court** as the limited-
      jurisdiction trial court for the claim amount — cite the
      controlling jurisdictional statute (MCL 600.8301) and
      **read the current civil jurisdictional cap from the
      references corpus** rather than asserting a number
- [ ] Notes 36th-District-specific filing/e-filing and docket
      practice (read current specifics from the corpus)

### Answer + affirmative defenses (mi-first-30-days)

- [ ] States the time to answer comes from **MCR 2.108** keyed
      to the manner of service (read current day counts from the
      corpus; note District-Court specifics)
- [ ] Answers each allegation per **MCR 2.111** and pleads
      affirmative defenses **separately under MCR 2.111(F)**
      (warning of waiver), including statute of limitations and
      lack of standing

### Substantive defense (mi-consumer-debt)

- [ ] Raises **chain of title / standing** — the debt buyer must
      prove ownership via an admissible assignment chain
- [ ] Raises the **statute of limitations** by citing
      **MCL 600.5807** and reading the limitations period from
      `mi-statutes-debt/` rather than asserting a number
- [ ] Identifies the Michigan **RCPA / MCPA** overlay (section
      numbers and prohibited conduct read from the corpus) and
      pairs it with the federal **FDCPA**

### Discovery + dispositive motion (mi-draft-motion)

- [ ] Uses discovery (interrogatories / production under the
      MCR 2.300-series; read response timing from the corpus) to
      force production of the assignment chain and account
      records
- [ ] Triages a **summary-disposition** motion: **MCR 2.116(C)(7)**
      for the SOL bar and/or **(C)(10)** for the standing/no-
      admissible-ownership-evidence gap

### Formatting + verification (mi-statewide-format / mi-fact-check)

- [ ] All filings carry the **MCR 1.109 / MCR 2.113** caption +
      signature; self-represented signature block (no P-number)
- [ ] Verifies every MCL / MCR / case citation against the
      corpus / CourtListener before filing (does not assert
      cites from memory)

## Common failure modes

- Treats the 36th District matter like a Circuit Court case or
  invents the jurisdictional cap
- Buries affirmative defenses instead of pleading them
  separately under MCR 2.111(F)
- Picks the wrong summary-disposition subrule for the SOL bar
- Asserts the limitations period, jurisdictional cap, or RCPA/
  MCPA sections from memory instead of the corpus
