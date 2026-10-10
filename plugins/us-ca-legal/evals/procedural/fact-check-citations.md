# ca-fact-check — Citation verification

## Prompt

Fact-check this paragraph from a motion I'm about to file in
LASC: "Under Cal. Civ. Code § 1788.13, the Rosenthal Act
prohibits debt collectors from communicating with consumers in
ways that simulate legal process. *People v. Smith* (2010) 50
Cal.3d 100 supports this position."

## Expected triggers

- `ca-fact-check`
- `ca-law-references`
- `ca-consumer-debt`

## Acceptance criteria

### Citation verification

- [ ] Verifies Cal. Civ. Code § 1788.13 against the Rosenthal
      Act text (correct: addresses simulated legal process)
- [ ] Flags *People v. Smith* (2010) 50 Cal.3d 100 as needing
      verification — generic case name + reporter may not exist
      or may not address the claimed point
- [ ] Citation format: "(2010) 50 Cal.3d 100" — per California
      Style Manual; if Cal.3d series ended in 1991 this would
      be flagged as anachronistic

### Quote-to-source

- [ ] Cross-checks against the canonical Rosenthal Act
      provisions (Cal. Civ. Code §§ 1788-1788.33)

### Citation format

- [ ] California Style Manual: "Code Civ. Proc., § X" with
      comma + § (not "CCP § X" in formal cite)
- [ ] California Style Manual: "Cal. Rules of Court, rule X"
- [ ] Reporter abbreviations: Cal.4th / Cal.App.5th /
      Cal.Rptr.3d

### Unpublished opinions

- [ ] Notes CRC 8.1115 — unpublished opinions generally not
      citable

## Common failure modes

- Accepting *People v. Smith* without verifying its existence
- Failing to flag anachronistic reporter series (Cal.3d ended
  1991)
- Importing Oregon citation conventions ("Or, Or App, P3d
  without periods")
- Importing Bluebook conventions (CA uses CSM, not Bluebook)
- Failing to verify the cited Civ. Code section actually
  addresses simulated legal process
