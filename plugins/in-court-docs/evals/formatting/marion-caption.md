# in-marion — Marion Superior Court caption, case assignment, and Odyssey filing

## Prompt

I'm filing a civil complaint in Indianapolis. The other party
owes me about $25,000 on a contract. Which court do I file
in, what does my cause number look like, and is there anything
specific about Marion County format that's different from the
rest of Indiana?

## Expected triggers

- `in-marion`
- `in-statewide-format`
- `in-file-packet`

## Acceptance criteria

### Venue and court selection

- [ ] Identifies Marion County as the filing county;
      states that for a civil monetary claim over the
      small-claims cap, the appropriate court is the
      **Marion Superior Court Civil Division** (14
      courtrooms numbered D01–D14)
- [ ] Reads the current small-claims monetary cap for
      Marion County from `in-statewide-format` /
      `in-marion` references rather than asserting a
      fixed number from memory
- [ ] Notes that Marion Superior Court assigns cases by
      **random rotation** through Odyssey — the filer
      does not choose the courtroom division

### Cause number format

- [ ] Explains the Marion cause-number encoding:
      `49D01-YYMM-CT-NNNNNN`
      - `49` = Marion County code
      - `D01` = Superior Court, Division 1
      - `YYMM` = filing month
      - `CT` = case-type code (`PL`, `CC`, `CT`, `MF`, etc.)
      - `NNNNNN` = Odyssey-assigned sequence
- [ ] Notes that Odyssey generates the cause number
      automatically; the filer does not assign it

### Marion-specific local rules

- [ ] Notes at least one Marion-distinctive local rule —
      e.g., the requirement to include a **proposed order
      with every motion** (reads the rule from `in-marion`
      rather than asserting the specific rule citation
      from memory)
- [ ] Notes the **CPC (Civil Pretrial Practice and
      Procedure)** case-management framework for Marion
      Civil Division cases: scheduling orders, discovery
      deadlines, pretrial conference timing

### Odyssey e-filing

- [ ] States that Odyssey (https://efile.courts.in.gov)
      is the statewide e-filing portal; mandatory for
      represented parties; optional for pro se
- [ ] Notes PDF-only accepted format and that document
      codes must be selected from the Odyssey dropdown
      matching the document title

## Common failure modes

- Directs the filer to the Circuit Court as the only
  Marion court (Marion Superior Court is the primary civil
  court; Marion Circuit Court also exists but is far less
  commonly used for civil plenary actions)
- Asserts a specific small-claims cap dollar amount from
  memory instead of the corpus
- Invents the courtroom assignment instead of noting
  random rotation
- Omits the proposed-order-with-every-motion requirement
