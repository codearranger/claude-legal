# tx-quality-check — pre-filing QC catches defects

## Prompt

Here's my draft Original Answer in a Texas sworn-account collection
case (district court). Before I file it, can you check it for
problems? It's a general denial, it has my caption and signature, and
that's it.

## Expected triggers

- `tx-quality-check`

## Acceptance criteria

### Catches the missing verified denial

- [ ] Flags that a plaintiff's claim pleaded as a **sworn account (TRCP
      185)** is prima facie proof **unless the defendant files a sworn
      / verified denial** — a bare general denial under TRCP 92 does
      **not** put a sworn account in issue (TRCP 93(10) / 185)
- [ ] Recommends adding a **verified denial** (denial under oath, or by
      a CPRC § 132.001 unsworn declaration) and lists the other matters
      that must be verified under **TRCP 93** (reading the list from
      the corpus)

### Catches the missing Rule 47(c) statement

- [ ] Notes that if the user is also asserting affirmative claims /
      counterclaims, the pleading needs the **TRCP 47(c)** statement of
      the range of relief (and that on the petition side its absence
      can bar default)

### Catches the missing certificate of service

- [ ] Flags the absence of a **certificate of service** (TRCP 21/21a)
      and that e-filed documents must be e-served

### Format

- [ ] Confirms or repairs line numbering, the `Page X of Y` footer, and
      the caption via `tx-statewide-format` / `scripts/format-check.py`

## Common failure modes

- Treats a bare general denial as sufficient against a sworn account
- Misses the missing certificate of service
- Recites the TRCP 93 verified-denial list from memory instead of the
  corpus
