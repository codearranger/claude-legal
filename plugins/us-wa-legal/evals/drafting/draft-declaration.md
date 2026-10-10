# wa-draft-declaration — Declaration in support

## Prompt
Draft a declaration in support of my motion to compel. I need to
establish that I served the discovery on [date], received deficient
responses on [date], and that we met and conferred on [date].

## Expected triggers
- `wa-draft-declaration`
- `wa-statewide-format`
- `wa-law-references` (civil-rules.md — CR 56(e) declaration
  requirements)

## Acceptance criteria
- Caption matches the motion exactly
- Title: "DECLARATION OF [NAME] IN SUPPORT OF [MOTION]"
- Opening sentence: "I, [name], declare as follows:"
- Numbered paragraphs, each a single factual assertion
- First paragraph establishes **personal knowledge** and competency
- Facts only — no argument, no legal conclusions (CR 12(f) strike
  risk)
- Each exhibit referenced with: "A true and correct copy of [document]
  is attached hereto as Exhibit [A]"
- Closing language: "I declare under penalty of perjury under the
  laws of the State of Washington that the foregoing is true and
  correct."
- Signature block: location signed, date, signature line, printed
  name, party designation (pro se)
- Complies with **RCW 9A.72.085** unsworn declaration statute

## Common failure modes
- Including argument or legal conclusions ("plaintiff's conduct is
  sanctionable")
- Missing personal-knowledge foundation
- Missing "under penalty of perjury under the laws of the State of
  Washington" exact language (RCW 9A.72.085 requires it)
- Missing the "true and correct" attestation
- Missing location where declaration was signed
