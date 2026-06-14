# co-denver — Denver District Court caption + CCEFS filing + chambers practice

## Prompt

I have a civil case in Denver District Court (2nd Judicial
District). I need to know: what goes in the caption, how do
I e-file it through CCEFS, and are there any Denver-specific
practices for motions that I should know about?

## Expected triggers

- `co-denver`
- `co-statewide-format`
- `co-file-packet`

## Acceptance criteria

### Caption (Denver 2nd JD specifics)

- [ ] Confirms the caption follows the statewide C.R.C.P. 10
      + CJD 11-01 two-block layout (left case block + COURT
      USE ONLY right block) and identifies the correct court
      line: **District Court, City and County of Denver,
      State of Colorado** (Lindsey-Flanigan Courthouse)
- [ ] Notes the **Division and Courtroom** lines in the left
      block must be filled in once assigned; reads the
      current division-assignment practice from the skill
      references rather than asserting a specific division
      number

### CCEFS e-filing

- [ ] Identifies **CCEFS** (Colorado Courts E-Filing System)
      as the mandatory e-filing platform for represented
      parties and describes the document-code selection step
- [ ] Notes that self-represented parties may use the **Pro
      Se** CCEFS track (cross-reference `co-pro-se`) and
      describes the JDF 205/206 fee-waiver path for
      indigent filers — reading current eligibility
      thresholds from the references corpus rather than
      asserting dollar figures from memory

### Denver motion-practice specifics

- [ ] Notes any **Denver 2nd JD chambers-practice** or
      judicial-practice-standard conventions for motions
      (working copies, cover sheets, or direct email
      channels) — reads the current practice from the
      `co-denver` skill references rather than inventing
      local rules
- [ ] Confirms the statewide **C.R.C.P. 121 § 1-15** page
      limits and conferral requirements apply in Denver
      district court

## Common failure modes

- Writes the court name as "Denver County District Court"
  instead of the correct "District Court, City and County
  of Denver"
- Asserts a specific division number from memory instead of
  directing the filer to confirm assignment
- Skips the CCEFS filing step or treats paper filing as the
  default for represented parties
- Invents chambers email addresses instead of reading
  per-JD contact practice from the references
