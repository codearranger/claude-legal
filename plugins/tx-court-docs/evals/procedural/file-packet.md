# tx-file-packet — assembling an eFileTexas packet

## Prompt

I'm ready to file my original petition in a Texas district court. What
goes in the packet and how do I e-file it?

## Expected triggers

- `tx-file-packet`

## Acceptance criteria

### Packet contents

- [ ] Assembles the core packet: the **Original Petition** (with the
      **TRCP 47(c) statement of relief**), a **Civil Case Information
      Sheet (TRCP 78a)**, and a **certificate of service** (TRCP
      21/21a)
- [ ] Includes a request for issuance of **citation** for service on
      the defendant, and (if fees can't be paid) a **TRCP 145 Statement
      of Inability to Afford Payment**

### E-filing mechanics

- [ ] Identifies mandatory statewide e-filing via **eFileTexas.gov**
      (Tyler Odyssey File & Serve) under **TRCP 21(f)**, and that
      e-service accompanies e-filing
- [ ] Notes self-represented filers may e-file and points to
      **TexasLawHelp.org** for guided forms

### Preflight

- [ ] Runs a format/QC preflight (line numbering, `Page X of Y` footer,
      caption) via `tx-quality-check` / `scripts/format-check.py` and
      reads any drift-prone figure (the 47(c) tiers) from the corpus

## Common failure modes

- Omits the Civil Case Information Sheet (TRCP 78a)
- Omits the Rule 47(c) relief statement from the petition
- Forgets the certificate of service or the citation request
