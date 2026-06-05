# ar-personal-injury — Comparative fault and no damages caps

## Prompt

I was hurt in an Arkansas car accident and may be partly at fault. Can I still
recover, and are damages capped?

## Expected triggers

- `ar-personal-injury`

## Acceptance criteria

- [ ] States Arkansas **modified comparative fault** under § 16-64-122 — recovery
      is barred if the plaintiff's fault is **equal to or greater** than the
      defendant's (the **"less than" / 49% bar**)
- [ ] Notes **no damages caps** under **Ark. Const. art. 5, § 32**, and that the
      tort-reform punitive cap was struck (*Bayer CropScience v. Schafer*)
- [ ] Flags the 3-year general tort SOL (read the count from references) and, for
      claims against the State, the near-absolute sovereign immunity routing to
      the **Arkansas State Claims Commission**

## Common failure modes

- Applies a 50%-or-pure comparative rule, or asserts a non-economic/punitive cap
