# ca-draft-declaration — Declaration scaffold

## Prompt

I need to draft a declaration in opposition to a motion for
summary judgment in my LASC case. I'm the defendant. I want to
attach my credit card statements as exhibits to show the last
payment was in 2019 and the lawsuit is time-barred. Help me
scaffold this.

## Expected triggers

- `ca-draft-declaration`
- `ca-statewide-format`
- `ca-consumer-debt` (for SOL analysis)
- `ca-pro-se`

## Acceptance criteria

### Caption

- [ ] Correct CRC 2.111 caption format
- [ ] Title: "DECLARATION OF [NAME] IN OPPOSITION TO PLAINTIFF'S
      MOTION FOR SUMMARY JUDGMENT"

### Body

- [ ] Numbered paragraphs
- [ ] First paragraph states declarant's identity and capacity
- [ ] Each paragraph states facts within personal knowledge
- [ ] Exhibits referenced as "attached as Exhibit A is a true
      and correct copy of..."
- [ ] No legal argument disguised as fact

### Penalty-of-perjury attestation (CCP § 2015.5)

- [ ] Includes the exact statutory language: "I declare under
      penalty of perjury under the laws of the State of
      California that the foregoing is true and correct."
- [ ] Date of execution
- [ ] **Place of execution** (California-specific — CCP § 2015.5
      requires both date AND place)
- [ ] Signature block

### SOL substance

- [ ] References CCP § 337 (4-year SOL on written contract)
- [ ] Last-payment date stated as fact
- [ ] Computation of running time

## Common failure modes

- Missing the "place of execution" — CCP § 2015.5 distinguishes
  California from many other states
- Using "affidavit" instead of "declaration" (CA uses declaration
  for most purposes)
- Conclusory paragraphs ("plaintiff lacks standing")
- Failing to authenticate exhibits in the declaration
- Importing the Oregon "I declare under penalty of perjury" form
  (which omits the place requirement) — California requires
  state-of-California language and place
