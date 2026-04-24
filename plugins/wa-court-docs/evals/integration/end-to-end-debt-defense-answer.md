# Integration — End-to-end debt-defense Answer packet

## Prompt
I was just served by a debt buyer in KCDC on [date]. The complaint is
bare-bones: it says "Defendant owes $X under account number XXXXX."
Draft my Answer with affirmative defenses and counterclaims for FDCPA
and CPA violations, plus a first set of discovery (interrogatories,
RFPs, RFAs).

## Expected triggers
- `wa-first-30-days`
- `wa-consumer-debt` (fdcpa.md, wa-consumer-protection.md,
  fact-pattern.md)
- `wa-discovery`
- `wa-draft-motion` (or analogous drafting helper)
- `wa-statewide-format`
- `wa-kcdc`

## Acceptance criteria

Produces:

### Answer
- 20-day deadline awareness
- CRLJ 8 admission/denial format — short paragraphs responding to
  each allegation in the complaint
- CRLJ 12(b) enumerated defenses preserved (SMJ, PJ, venue, process,
  service, failure to state a claim)
- Affirmative defenses (CRLJ 8(c)):
  - Statute of limitations
  - Payment / accord and satisfaction
  - Failure of consideration
  - Lack of standing (chain-of-title)
  - Unclean hands (where applicable)
  - Failure to mitigate
- Counterclaims:
  - **FDCPA** — 15 U.S.C. § 1692e, § 1692g, § 1692f; statutory
    damages, actual damages, fees and costs
  - **CPA** — RCW 19.86, Hangman Ridge 5-element framework; treble
    damages up to $25,000 + fees
  - **Collection Agency Act** — RCW 19.16.440 per se CPA violation
    where applicable
- Prayer for relief with multi-ground fee request

### First Discovery
- **Interrogatories** (CRLJ 33) targeting:
  - Chain of title / assignments
  - Original creditor records and custodians
  - Calculation of balance
  - Communications and validation history
- **Requests for Production** (CRLJ 34):
  - Signed cardholder agreement
  - Complete bill of sale with schedules
  - Account statements from default backwards
  - Call logs, validation correspondence
- **Requests for Admission** (CRLJ 36) targeting key evidentiary
  weaknesses

### Format
- GR 14 compliant
- Proper captions, party designations, signature blocks
- Certificate of Service

## Common failure modes
- Missing affirmative-defense pleading (waiver by inaction)
- Missing chain-of-title defense
- Counterclaim prayer missing one of the four fee grounds
- Discovery requests that are overbroad (plaintiff will object and
  court will not compel)
- Using FDCPA without addressing Henson debt-buyer coverage issue
- Missing 20-day deadline compliance
