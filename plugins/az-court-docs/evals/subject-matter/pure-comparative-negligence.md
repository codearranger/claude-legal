# az-personal-injury — Pure comparative negligence, no-damages-cap rule, nonparty at fault

## Prompt

I was hurt in a car crash in Arizona. The other driver was mostly
at fault, but the insurance company says I was partly to blame too,
and they're also pointing at a third driver who wasn't named in my
lawsuit. Does my own fault wipe out my claim, is there a cap on
what I can recover, and what about the third driver?

## Expected triggers

- `az-personal-injury`

## Acceptance criteria

### Comparative fault (pure)

- [ ] Identifies Arizona as a **pure comparative negligence** state
      under **A.R.S. § 12-2505** — the plaintiff's recovery is reduced
      by the plaintiff's percentage of fault but is **not barred** even
      if the plaintiff is more than 50% at fault — and reads the
      current statutory text/standard from `az-statutes-debt/` rather
      than asserting it
- [ ] Notes the limited intentional/wilful-or-wanton exception to
      recovery (read from the corpus) rather than asserting it

### No damages cap (constitutional rule)

- [ ] Notes the **Arizona constitutional anti-abrogation / no-damages-
      cap rule** — Ariz. Const. art. 2, § 31 prohibits the legislature
      from capping damages for personal injury / death — and reads the
      current statement of the rule from the corpus / `key-cases.md`
      rather than asserting it from memory

### Nonparty at fault

- [ ] Explains the **nonparty-at-fault** mechanism under
      **A.R.S. § 12-2506** — Arizona's abolition of joint liability
      and adoption of **several-only** liability, under which a
      defendant may name a **nonparty at fault** so the jury can
      allocate fault to a person not a party — and the procedural
      requirement/deadline to designate a nonparty (read the timing
      from the corpus / the governing rule)
- [ ] Notes the consequence: each defendant pays only its own
      allocated share (several liability), read from the corpus

## Common failure modes

- Treats Arizona as a modified-comparative (50%-bar) state
- Asserts a damages cap exists, or misses the constitutional
  no-cap rule
- Misses the nonparty-at-fault designation or asserts the
  designation deadline from memory
- Asserts joint-and-several liability instead of several-only
