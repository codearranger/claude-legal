# ga-law-references — Corpus navigation: O.C.G.A., USCR, federal symlinks, key cases

## Prompt

I'm researching a Georgia consumer-debt case. Where do the Georgia
statutes, court rules, and federal debt laws live in this plugin, and how
do I make sure I'm citing the current text rather than something out of
date?

## Expected triggers

- `ga-law-references`

## Acceptance criteria

### Corpus map

- [ ] Identifies the Georgia-specific corpora under the
      `ga-law-references` references tree — **`court-rules/`** (USCR and
      the parallel State/Magistrate court rules) and
      **`ga-statutes-debt/`** (the O.C.G.A. chapters relevant to debt,
      garnishment, exemptions, the FBPA, and evidence) — and reads from
      them rather than from memory
- [ ] Identifies the **shared federal corpora** reached by symlink —
      `federal-debt-laws/` (FDCPA, FCRA, TILA, etc.), `federal-bankruptcy/`,
      and `ucc-model/` — and notes these are the canonical federal sources
      to pair with the Georgia statutes

### Citation discipline

- [ ] Confirms O.C.G.A. section numbers and titles against
      `ga-statutes-debt/`, USCR rule numbers against `court-rules/`, and
      **case citations** against `key-cases.md` (or CourtListener) — never
      asserted from memory
- [ ] Notes that O.C.G.A. official text is the copyrighted LexisNexis
      edition; the corpus is drawn from open mirrors (FindLaw / CourtListener
      corroboration) and section text should be verified before filing

### Reporter conventions

- [ ] Notes that Georgia case cites use the **official reporters**
      (Ga. for the Supreme Court, Ga. App. for the Court of Appeals) with
      S.E.2d parallels, per **Ga. Sup. Ct. Rule 22** — Georgia has not
      adopted a public-domain neutral citation

## Common failure modes

- Looks for federal debt-law text inside the Georgia corpus instead of
  the shared `federal-debt-laws/` symlink
- Asserts an O.C.G.A. section number from memory without checking
  `ga-statutes-debt/`
- Invents a neutral-citation format for Georgia opinions instead of the
  Ga. / Ga. App. + S.E.2d reporters
