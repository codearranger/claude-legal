# id-quality-check — pre-filing format + content QC

## Prompt

I've drafted a motion for an Idaho District Court. Can you run a
quality check before I file it?

## Expected triggers

- `id-quality-check`
- `id-statewide-format`

## Acceptance criteria

- [ ] Runs a two-pass review: a **format** pass (I.R.C.P. 2 baseline)
      and a **content/consistency** pass
- [ ] Invokes / references `scripts/format-check.py` for the `.docx`
      format validation (paper, margins, spacing, font, black ink,
      footer pagination)
- [ ] Checks the caption matches the venue and case number, the
      Notice of Hearing date math is consistent, and the certificate
      of service is present
- [ ] Verifies citations are in Idaho form (defers substantive
      citation verification to `id-fact-check`)
- [ ] Reports issues without asserting that a clean format means the
      legal position is sound (surface-only disclaimer)

## Common failure modes

- Treats a passing format check as legal sufficiency
- Skips the certificate-of-service / Notice-of-Hearing consistency check
