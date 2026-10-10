# co-draft-declaration — Unsworn declaration under C.R.S. § 13-27-104

## Prompt

I'm self-represented in a Colorado civil case and I need to put my
own sworn facts in front of the judge to support my motion — when I
was served, what the collector said on the phone. Do I have to find
a notary, or is there a Colorado way to sign it myself? Draft it for
me.

## Expected triggers

- `co-draft-declaration`
- `co-statewide-format`
- `co-pro-se`

## Acceptance criteria

### Declaration vs. affidavit

- [ ] Explains that Colorado permits an **unsworn declaration under
      penalty of perjury** in lieu of a notarized affidavit under
      **C.R.S. § 13-27-104** (Colorado's analog to 28 U.S.C.
      § 1746) — no notary needed for most filings
- [ ] Uses the Colorado **verification language** — declared "under
      penalty of perjury pursuant to the laws of the State of
      Colorado" — reading the current attestation wording from the
      skill references / `co-statutes-debt` corpus rather than
      quoting a fixed sentence from memory
- [ ] Notes the narrow cases where a **notarized affidavit** is
      still required (where a specific statute or rule demands an
      affidavit) and offers that form as the alternative

### Content discipline

- [ ] Establishes a **personal-knowledge** foundation in the opening
      paragraph and confines the body to facts the declarant
      personally knows (no argument, no legal conclusions)
- [ ] Uses **numbered paragraphs**, exhibit references ("a true and
      correct copy ... attached as Exhibit A"), and an exhibit list
- [ ] Includes the **date and place of execution** ("Executed on
      [date] at [city], Colorado") and a signature block

### Composition

- [ ] Caption identical to the motion it supports, per the Colorado
      flexible caption (`co-statewide-format`)
- [ ] Self-represented signature block — no Atty. Reg. # and no
      notary jurat on the declaration form

## Common failure modes

- Tells the filer a notary is always required (misses
  C.R.S. § 13-27-104)
- Uses the federal 28 U.S.C. § 1746 language instead of the
  Colorado penalty-of-perjury formulation
- Lets the declaration drift into legal argument instead of
  personal-knowledge facts
- Omits the date/place-of-execution line
