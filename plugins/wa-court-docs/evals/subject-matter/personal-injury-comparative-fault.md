# wa-personal-injury — Pure comparative fault

## Prompt

I was rear-ended in Tacoma by a driver who ran a red light.
The other driver argues I was 25% at fault because my brake
lights weren't working (I didn't know). My medical bills are
$50,000. What can I recover under Washington law?

## Expected triggers

- `wa-personal-injury`
- `wa-pierce`

## Acceptance criteria

- [ ] Identifies Washington as a **pure comparative fault**
      state under RCW 4.22
- [ ] Notes that plaintiff's fault reduces recovery
      proportionally but does **not** bar recovery — even at
      99% at fault, plaintiff recovers 1%
- [ ] Distinguishes from modified-comparative-fault states
      (50% / 51% bar) and pure-contributory-negligence states
- [ ] Applies the framework: if jury accepts 25% plaintiff
      fault, plaintiff recovers 75% of damages (= $37,500 on
      $50k bills; treats the prompt's hypothetical numbers as
      the math input)
- [ ] References the 1986 Reform Act's general several-
      liability rule (with statutory carve-outs in RCW 4.22.070
      — see chapter file for current carve-out enumeration)
- [ ] Notes the SOL framework at RCW 4.16 (current day counts
      in `wa-law-references/references/wa-rcw-debt/RCW-4_16.md`)
- [ ] Notes empty-chair-defense considerations

## Common failure modes

- Treating Washington as modified-comparative-fault (51% bar)
- Stating the plaintiff is barred from recovery
- Hard-coding specific SOL day counts
- Missing the 1986 Reform Act several-liability framework
