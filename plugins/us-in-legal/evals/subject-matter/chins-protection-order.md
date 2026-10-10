# in-family-law — CHINS IC 31-34 + protection orders IC 34-26-5

## Prompt

My neighbor's children look like they are being neglected
— they're left alone for long periods and appear
malnourished. Separately, my ex-partner is threatening
me and I'm scared. What Indiana law applies to each
situation, and what courts handle these matters?

## Expected triggers

- `in-family-law`
- `in-family-court`

## Acceptance criteria

### CHINS — IC 31-34

- [ ] Identifies **Children In Need of Services (CHINS)**
      under **IC 31-34** as the controlling statute for
      child neglect or abuse proceedings in Indiana
- [ ] States the proper intake channel: a report to the
      **Department of Child Services (DCS)** or law
      enforcement triggers DCS investigation; DCS
      (not the private neighbor) initiates the CHINS
      petition in **Juvenile Court**
- [ ] Identifies the Juvenile Court (or Juvenile Division
      of Circuit / Superior Court in larger counties) as
      the forum — reads the venue topology from
      `in-family-court` rather than asserting specific
      county configurations from memory
- [ ] Notes that DCS involvement, CHINS adjudication,
      and dispositional orders (services to the family)
      are the statutory path — not a direct private
      filing by the neighbor

### Protection orders — IC 34-26-5

- [ ] Identifies **IC 34-26-5** as the Indiana civil
      protection-order statute for the threatening
      ex-partner scenario
- [ ] Notes the petition must be **verified** under T.R.
      11(B) / IC 34-26-5 (the notarized / affirmed
      petition — not simply an unsworn filing)
- [ ] States the forum: Circuit Court or Superior Court
      in the petitioner's or respondent's county; some
      counties have a dedicated family/domestic division
- [ ] Notes the **ex parte temporary protective order
      (TPO)** available if the petitioner shows immediate
      and present danger; the full hearing follows within
      the statutory window (reads current day count from
      the corpus rather than asserting a number)
- [ ] Flags that violation of a protection order is a
      crime under IC 35-46-2-2

### Corpus-first discipline

- [ ] Reads current statutory thresholds, hearing
      deadlines, and specific factor enumerations from
      the references corpus (`IC-31-34.md`, `IC-34-26.md`)
      rather than asserting them from memory

## Common failure modes

- Suggests the concerned neighbor can file a CHINS
  petition directly (DCS initiates CHINS in Indiana;
  the neighbor's role is to report)
- Applies a federal or other-state protection-order
  framework (IC 34-26-5 is Indiana-specific)
- Asserts the TPO hearing window day count from memory
  without verifying from the corpus
- Omits the verification / affirmation requirement for
  the protection-order petition
