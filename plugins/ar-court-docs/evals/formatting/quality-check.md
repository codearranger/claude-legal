# ar-quality-check — Pre-filing QC with local-rule WARN posture

## Prompt

Can you QC my Arkansas motion before I file it?

## Expected triggers

- `ar-quality-check`

## Acceptance criteria

- [ ] Runs a format + content pass against the **Ark. R. Civ. P. 10/11** caption
      and signature and **Administrative Order No. 19** redaction
- [ ] **WARNs** (rather than fails) on typography items, because Arkansas has no
      statewide format rule — those are local-rule matters
- [ ] References `scripts/format-check.py`

## Common failure modes

- Reports a typography "failure" as if a statewide rule were violated
