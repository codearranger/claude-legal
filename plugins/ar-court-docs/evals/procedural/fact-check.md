# ar-fact-check — Citation verification

## Prompt

Check the citations in my Arkansas brief.

## Expected triggers

- `ar-fact-check`

## Acceptance criteria

- [ ] Verifies medium-neutral citations in the **`YEAR Ark. NNN` /
      `YEAR Ark. App. NNN`** form under Ark. Sup. Ct. R. 5-2
- [ ] Checks statute cites in **Ark. Code Ann.** form and rule cites
      (Ark. R. Civ. P. / Ark. R. Evid.)
- [ ] Runs internal/packet/sworn-vs-argued consistency passes

## Common failure modes

- Treats only S.W.3d reporter cites as valid and rejects the medium-neutral form
