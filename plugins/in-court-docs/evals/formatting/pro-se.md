# in-pro-se — Pro se appearance, fee waiver, and Self-Help Center

## Prompt

I cannot afford a lawyer. I want to fight a debt-collection
lawsuit against me in Marion Superior Court. What do I have
to do to appear as my own attorney, how do I request a fee
waiver if I can't pay the filing fee, and where can I get
help?

## Expected triggers

- `in-pro-se`
- `in-statewide-format`
- `in-marion`

## Acceptance criteria

### Pro se appearance mechanics

- [ ] States that any Indiana litigant may appear **pro se**
      (self-represented) in a civil action
- [ ] Notes the Indiana Supreme Court's doctrine that pro se
      litigants are held to **the same procedural standards
      as licensed attorneys** (*Goossens v. Goossens*, 829
      N.E.2d 36, 43 (Ind. Ct. App. 2005)) — reads or
      cross-references the case from the corpus rather than
      asserting the holding from memory
- [ ] Notes the **Appearance form under T.R. 3.1** — the
      self-represented party must file a formal Appearance
      with the court so the clerk knows who to serve
- [ ] Explains the pro se signature block: name + "Pro Se"
      designation, address, telephone, email — no Attorney
      Number

### Fee waiver — IC 33-37-3-2

- [ ] Identifies **IC 33-37-3-2** as the fee-waiver
      statute (or reads the current provision from the
      references corpus); describes the financial hardship
      standard
- [ ] Notes the **CIV-0600 / CCIV-0600 fee-waiver form**
      (Indiana state form) or equivalent Marion County
      form; states it must be filed with or before the
      initial pleading when fees cannot be paid

### E-filing / Odyssey

- [ ] States that self-represented litigants may
      **optionally e-file** through Odyssey
      (https://efile.courts.in.gov); not mandatory for pro
      se parties but strongly recommended
- [ ] Notes that if the pro se party does NOT e-file,
      service on opposing counsel can still be
      accomplished by paper / mail under T.R. 5(B)

### Self-Help Center

- [ ] Directs the user to the **Marion County Self-Help
      Center** (City-County Building) for non-legal
      procedural assistance — or reads the current
      directory from `in-pro-se`
- [ ] Flags Indiana Legal Services as the legal-aid
      resource for income-qualifying defendants

## Common failure modes

- Implies the court will give leniency on deadlines or
  format rules because the filer is pro se (Indiana
  courts do not — *Goossens* standard)
- Asserts the *Goossens* holding without citing or
  verifying against the corpus
- Omits the Appearance form (T.R. 3.1) step
- Fails to mention the fee waiver option
- Suggests mandatory e-filing for pro se parties
  (Odyssey is optional for self-represented litigants)
