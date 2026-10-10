# id-file-packet — assemble + preflight an iCourt filing

## Prompt

I have a motion ready to file in Idaho. Help me assemble the complete
packet and tell me how to e-file it.

## Expected triggers

- `id-file-packet`
- `id-statewide-format`

## Acceptance criteria

- [ ] Enumerates the packet components: the motion, the supporting
      **Memorandum**, any supporting **Affidavit/Declaration**, a
      **Notice of Hearing**, a **proposed order**, and the
      **certificate of service** (I.R.C.P. 5)
- [ ] Describes filing through **iCourt** / Odyssey *File & Serve*
      under the I.R.E.F.S., including the PDF/format requirements
      (I.R.E.F.S. 6) and that e-filing constitutes consent to
      electronic service (I.R.E.F.S. 17)
- [ ] Notes e-filing is mandatory for attorneys and optional for
      self-represented individuals
- [ ] Runs a cross-document consistency check (caption, case number,
      hearing date) and recommends `id-quality-check` /
      `scripts/format-check.py`

## Common failure modes

- Omits the Notice of Hearing or certificate of service
- Misses the e-filing-equals-e-service-consent point
