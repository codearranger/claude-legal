# or-statewide-format — UTCR 2.010 baseline format

## Prompt

Draft me a motion to compel in Oregon — Multnomah Circuit
Court. The case number is 25CV01234, I'm Jane Doe and
plaintiff is Velocity Investments, LLC. I'm pro se. Make sure
it's formatted to comply with the Oregon court rules.

## Expected triggers

- `or-statewide-format` (always)
- `or-multcc`
- `or-pro-se`
- `or-draft-motion`

## Acceptance criteria

### Caption

- [ ] Court header: "IN THE CIRCUIT COURT OF THE STATE OF
      OREGON" + "FOR THE COUNTY OF MULTNOMAH"
- [ ] Case number `25CV01234`
- [ ] Parties: VELOCITY INVESTMENTS, LLC (Plaintiff) v. JANE
      DOE (Defendant)
- [ ] **"v." (with period)** between parties, NOT "vs."
- [ ] Vertical rule between left and right columns
- [ ] Horizontal rule below caption

### UTCR 2.010 format

- [ ] References 3" top margin on page 1, 1" elsewhere
- [ ] References Times New Roman 12 pt or Arial 12 pt
- [ ] References 1.5 or double spacing
- [ ] References "black or blue-black ink only" (no color)
- [ ] References "Page X of Y" footer with PAGE / NUMPAGES
      fields

### Parker framework (motion structure)

- [ ] Cites ORCP 46 A as the procedural authority at the top
      of the MOTION section
- [ ] Has sections I (Relief), II (Facts), III (Issues),
      IV (Evidence), V (Authorities), VI (Argument), VII
      (Conclusion)
- [ ] Meet-and-confer certification (Multnomah SLR 5.045)

### Pro se conventions

- [ ] Signature block uses "Defendant, pro se"
- [ ] NO OSB# in the signature block
- [ ] Includes address, phone, email

### Citation format

- [ ] ORCP cited as `ORCP 46 A` (capital letter, space)
- [ ] Any case citations use `Or` / `Or App` / `P3d` (no
      periods)
- [ ] ORS cited as `ORS [chapter].[section]`
- [ ] UTCR cited as `UTCR 2.010(N)` (decimal format)

## Common failure modes

- Using "vs." instead of "v."
- Using Bluebook periods in citations (`Or.`, `P.3d`)
- Citing Washington analogs (RCW, CR/CRLJ, KCDC, etc.)
- Lettered exhibits instead of numbered
- Including a fake OSB# for pro se filer
- Missing the meet-and-confer certification
- Wrong court header line
