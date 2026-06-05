# Integration — Motion-to-compel packet

## Prompt

The debt buyer ignored my discovery in my Arkansas case. Put together a complete
motion-to-compel packet.

## Expected triggers

- `ar-discovery`
- `ar-draft-motion`
- `ar-draft-note`
- `ar-draft-order`
- `ar-file-packet`

## Acceptance criteria

- [ ] Assembles a motion to compel under **Ark. R. Civ. P. 37** with a supporting
      brief documenting good-faith conferral
- [ ] Includes a **Notice of Hearing** (ar-draft-note) and a **proposed order**
      (ar-draft-order, judge-signed)
- [ ] Applies the statewide format (caption, numbered paragraphs, signature,
      Rule 5 certificate of service, line numbering, footer)
- [ ] Addresses eFlex assembly and Administrative Order No. 19 redaction

## Common failure modes

- Omits the proposed order or the certificate of service; mislabels the Notice
  of Hearing
