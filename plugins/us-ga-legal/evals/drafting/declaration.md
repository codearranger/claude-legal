# ga-draft-declaration — Georgia affidavit / sworn statement for motion support

## Prompt

I'm self-represented in a Georgia civil case and I need to put my own
facts in front of the judge to support my motion — when I was served and
what the collector said on the phone. How do I sign it in Georgia, and
does it need to be notarized? Draft it for me.

## Expected triggers

- `ga-draft-declaration`
- `ga-statewide-format`
- `ga-pro-se`

## Acceptance criteria

### Sworn-statement form

- [ ] Explains that Georgia practice generally relies on a **notarized
      affidavit** (sworn before a notary or officer authorized to
      administer oaths) for evidentiary support, and reads the current
      attestation/jurat wording from the skill references rather than
      quoting a fixed sentence from memory
- [ ] Notes that O.C.G.A. § 9-11-11 imposes **no general verification
      requirement** on ordinary pleadings, but a factual affidavit
      supporting a motion (or a summary-judgment affidavit under
      **O.C.G.A. § 9-11-56(e)**) must be made on **personal knowledge**,
      set out admissible facts, and show the affiant is competent to
      testify — reads § 9-11-56(e) from the corpus

### Content discipline

- [ ] Establishes a **personal-knowledge** foundation in the opening
      paragraph and confines the body to facts the affiant personally
      knows (no argument, no legal conclusions)
- [ ] Uses **numbered paragraphs** per O.C.G.A. § 9-11-10(b), exhibit
      references ("a true and correct copy ... attached as Exhibit A"),
      and an exhibit list
- [ ] Includes the **execution / jurat** block (date, county, notary
      signature line)

### Composition

- [ ] Caption identical to the motion it supports, per the Georgia
      caption (`ga-statewide-format`)
- [ ] Self-represented signature block — no Georgia Bar No.

## Common failure modes

- Imports a federal "unsworn declaration under penalty of perjury"
  (28 U.S.C. § 1746) form as if it were the default Georgia vehicle
  without flagging the notarization expectation
- Lets the affidavit drift into legal argument instead of
  personal-knowledge facts
- Omits the § 9-11-56(e) personal-knowledge / admissibility standard for
  a summary-judgment affidavit
- Omits the jurat / notary block
