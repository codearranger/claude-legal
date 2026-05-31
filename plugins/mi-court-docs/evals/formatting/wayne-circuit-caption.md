# mi-wayne — Wayne County Circuit Court (3rd Circuit) caption

## Prompt

I'm filing a civil complaint in the Wayne County Circuit Court
in Detroit. Can you build me the caption block exactly the way
it should read for that court?

## Expected triggers

- `mi-wayne`
- `mi-statewide-format`

## Acceptance criteria

### Court identification

- [ ] Identifies the court as the **Third Judicial Circuit of
      Michigan (Wayne County Circuit Court)** and labels it
      correctly in the caption (e.g., "STATE OF MICHIGAN / IN
      THE CIRCUIT COURT FOR THE COUNTY OF WAYNE / THIRD JUDICIAL
      CIRCUIT")
- [ ] Notes the Coleman A. Young Municipal Center / civil
      division as the filing location and any Wayne-specific
      practice (read current local-rule / e-filing specifics
      from the references corpus rather than asserting them)

### Caption mechanics (MCR 1.109 / MCR 2.113)

- [ ] Caption built per **MCR 1.109** and **MCR 2.113**:
      plaintiff v. defendant with designations, a **case number**
      slot (Wayne uses the NN-NNNNNN-XX format with a case-type
      code — read the current case-type-code convention from the
      corpus rather than inventing one), and the assigned-judge
      line
- [ ] Includes the document title and the attorney/self-
      represented signature-line expectations

### Self-represented note

- [ ] If pro se, signature block omits the P-number (defers to
      `mi-pro-se`)

## Common failure modes

- Calls it "Wayne District Court" or omits the "Third Judicial
  Circuit" designation
- Invents a case-number or case-type-code format instead of
  reading the convention from the corpus
- Uses a generic caption that ignores Wayne-specific elements
- Hard-codes a courtroom/judge assignment as fact
