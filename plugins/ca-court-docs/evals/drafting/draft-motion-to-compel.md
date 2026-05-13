# ca-draft-motion — Motion to Compel scaffold

## Prompt

Draft a motion to compel further responses to my RFPs for my
California case. Plaintiff (Velocity Investments, LLC) served
boilerplate objections to RFPs targeting the chain of title. The
case is in LASC, Stanley Mosk Courthouse, 25STCV01234. I'm pro
per. Hearing is set for July 15, 2026.

## Expected triggers

- `ca-draft-motion`
- `ca-statewide-format`
- `ca-lasc`
- `ca-discovery`
- `ca-pro-se`

## Acceptance criteria

### Caption

- [ ] Correct LASC caption — "Superior Court of California, County
      of Los Angeles" + Stanley Mosk Courthouse, 111 N. Hill St.
- [ ] Case number `25STCV01234`
- [ ] Title in ALL CAPS: "DEFENDANT'S NOTICE OF MOTION AND MOTION
      TO COMPEL FURTHER RESPONSES TO REQUESTS FOR PRODUCTION
      (SET ONE); MEMORANDUM OF POINTS AND AUTHORITIES"
- [ ] Hearing date / time / department in the caption block

### Notice of Motion section

- [ ] States date, time, place (department) of hearing
- [ ] States nature of motion ("Defendant will move ...")
- [ ] States grounds with CCP §§ 2031.310 citation
- [ ] States that motion is based on the notice, the memorandum,
      the separate statement, and the meet-and-confer declaration

### Separate Statement (CRC 3.1345)

- [ ] Explicit reference to the separate statement requirement
- [ ] Each RFP / response / reason-for-compelling laid out

### Memorandum of P&A

- [ ] I. Introduction
- [ ] II. Statement of Facts
- [ ] III. Argument
- [ ] IV. Conclusion
- [ ] Cites CCP §§ 2017.010, 2031.210, 2031.310
- [ ] Cites CRC 3.1345 (separate statement)
- [ ] Identifies the 45-day deadline (CCP § 2031.310(c)) and
      establishes timeliness

### Meet-and-confer declaration

- [ ] References CCP § 2031.310(b)(2)
- [ ] Recites the specific dates of M&C correspondence

### Pro se conventions

- [ ] "Defendant, In Pro Per" (or "Self-Represented") in
      signature block
- [ ] No bar number

### Notice timing

- [ ] Recognizes 16 court-day notice under CCP § 1005(b)
- [ ] Backs into a service deadline given the hearing date

## Common failure modes

- Forgetting the separate-statement requirement (CRC 3.1345)
- Citing FRCP 26/37 instead of CCP § 2031.310
- Citing Oregon ORCP 46 A or Washington CR 37 instead of California
- Missing the 45-day jurisdictional deadline check
- Combining Notice of Motion and Memorandum into a single doc
  (California uses separate documents)
- Using "Esq." or a bar number for a pro per filer
