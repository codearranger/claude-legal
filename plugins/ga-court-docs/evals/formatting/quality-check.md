# ga-quality-check — Pre-filing format + content QC

## Prompt

I've drafted a motion for summary judgment in a Georgia consumer-debt
case and I want to make sure it's ready before I file it. Walk me through
the pre-filing checklist — formatting, citations, and anything else that
could get it bounced or embarrass me.

## Expected triggers

- `ga-quality-check`
- `ga-statewide-format`
- `ga-fact-check`

## Acceptance criteria

### Format pass

- [ ] Checks the Georgia caption per **O.C.G.A. § 9-11-10** — correct
      court and county line, **"Civil Action File No."** label, party
      designations, document title below the caption — and the marketplace
      format baseline (US Letter, 1-inch margins, 12-point, double-spaced,
      footer) — reads current standards from the references corpus rather
      than asserting fixed numbers from memory
- [ ] Confirms a **certificate of service** under O.C.G.A. § 9-11-5 is
      present and the signature block matches the filer's status (no
      Georgia Bar No. for pro se)

### Content pass

- [ ] Verifies the motion states the relief requested up front, cites the
      controlling rule/statute with the standard (e.g., the
      **O.C.G.A. § 9-11-56** summary-judgment standard and *Lau's Corp. v.
      Haskins*), ties facts to a supporting affidavit, and restates the
      relief in the conclusion
- [ ] Confirms the supporting affidavit is on **personal knowledge**
      (O.C.G.A. § 9-11-56(e)) and does not contain legal argument

### Citation pass

- [ ] Verifies every **O.C.G.A. / USCR / case citation** against the
      references corpus or `key-cases.md` — never asserted from memory —
      and confirms case cites use the official Georgia reporters
      (Ga. / Ga. App. with S.E.2d parallels per Ga. Sup. Ct. Rule 22)

### Proposed order

- [ ] Confirms a **separate proposed order** is prepared
      (cross-reference `ga-draft-order`), not embedded in the motion body

## Common failure modes

- Uses "Case No." instead of "Civil Action File No."
- Lets an unverified case citation pass (asserts from memory instead of
  checking `key-cases.md`)
- Misses the § 9-11-56(e) personal-knowledge requirement for the
  supporting affidavit
- Misses a missing proposed order
