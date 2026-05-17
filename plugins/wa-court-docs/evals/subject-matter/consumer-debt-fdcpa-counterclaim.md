# wa-consumer-debt — FDCPA counterclaim

## Prompt

The debt collector sent me dunning letters that misrepresented
the legal status of my debt (claimed they would file suit
immediately if I didn't pay, even though I later learned the
SOL had run). Can I counterclaim under the FDCPA?

## Expected triggers

- `wa-consumer-debt`
- `wa-first-30-days`

## Acceptance criteria

- [ ] Identifies the FDCPA at 15 U.S.C. § 1692 et seq. (see
      `wa-law-references/references/federal-debt-laws/FDCPA.md`)
- [ ] Identifies the relevant prohibition (likely § 1692e
      false/misleading representations, especially threatening
      legal action that cannot legally be taken on a time-barred
      debt)
- [ ] References Regulation F at 12 C.F.R. § 1006 — specifically
      the prohibition on threatening or filing suit on time-
      barred debt (current rule subsection in
      `federal-debt-laws/Reg-F.md`)
- [ ] Notes FDCPA remedies: actual damages + statutory damages
      (current cap per § 1692k — see federal-debt-laws corpus) +
      mandatory attorney's fees + costs
- [ ] Notes short FDCPA SOL — runs from violation per
      *Rotkiske v. Klemm* (current day count in federal-debt-
      laws corpus)
- [ ] Notes that FDCPA can be pleaded as a counterclaim in the
      state collection action (federal claim cognizable in state
      court)
- [ ] Pair with WA CPA per-se pathway via RCW 19.16 (see
      `wa-consumer-debt/references/wa-consumer-protection.md`)

## Common failure modes

- Hard-coding a specific FDCPA statutory damages figure
- Missing the Reg F time-barred-debt prohibition
- Citing FDCPA SOL as accruing on discovery (it's violation-
  date per *Rotkiske*)
- Failing to pair with the WA CPA per-se pathway
