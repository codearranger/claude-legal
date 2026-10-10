# oh-quality-check — Pre-filing QC

## Prompt

I'm about to file a motion in my Ohio Common Pleas case.
Can you run a pre-filing quality check?

## Expected triggers

- `oh-quality-check`
- `oh-statewide-format`
- `oh-fact-check`

## Acceptance criteria

### Format

- [ ] Verifies Civ. R. 10 caption form
- [ ] Verifies signature block (pro se: no Atty. Reg. #;
      counsel: Atty. Reg. # present)
- [ ] Verifies certificate of service
- [ ] Verifies margins / font / spacing per common Common
      Pleas local-rule baseline

### Content

- [ ] Verifies citation format (Ohio public-domain
      `YYYY-Ohio-NNNN` for appellate cases)
- [ ] Verifies R.C. / Civ. R. / Evid. R. cites resolve to
      real statutes / rules
- [ ] Flags discrepancies between sworn statements and
      argument

### Logistics

- [ ] Verifies filing fee / fee waiver attached if needed
- [ ] Verifies courtesy copy / chambers copy plan
- [ ] Flags any missing exhibits referenced in body

## Common failure modes

- Skipping the citation check
- Skipping the certificate of service
- Missing fee verification
