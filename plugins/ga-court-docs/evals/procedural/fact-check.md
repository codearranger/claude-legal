# ga-fact-check — Citation verification + internal consistency + corpus sourcing

## Prompt

I've drafted a motion for summary judgment in a Georgia consumer-debt
case. Before I file it, I want to verify that all my citations are
accurate, the facts in my affidavit match the motion, and there are no
internal inconsistencies. How do I do that?

## Expected triggers

- `ga-fact-check`
- `ga-quality-check`

## Acceptance criteria

### Citation verification

- [ ] Checks every **O.C.G.A. / USCR / case citation** against a
      structured source:
      - O.C.G.A. section numbers and titles verified against
        `ga-statutes-debt/` or the references corpus
      - USCR rule numbers verified against `court-rules/`
      - Case citations (e.g., *Lau's Corp. v. Haskins*, *Hill v. American
        Express*, *Nyankojo v. North Star Capital Acquisition*) verified
        against `key-cases.md` or CourtListener — never asserted from
        memory
- [ ] Confirms case cites use the **official Georgia reporters**
      (Ga. / Ga. App. + S.E.2d) per Ga. Sup. Ct. Rule 22 — flags that
      some secondary sources conflate the S.E.2d pin-cites for *Hill v.
      American Express*, so the reporter cite must be verified

### Internal consistency

- [ ] Verifies the **motion body and supporting affidavit** tell the same
      factual story — no date conflicts, amount discrepancies, or
      conflicting party descriptions
- [ ] Confirms **exhibit references** in the motion correspond to actual
      attached exhibits

### Packet consistency

- [ ] Confirms the **caption is identical** across motion, affidavit, and
      proposed order (same court/county, Civil Action File No., parties,
      title)
- [ ] Confirms the **proposed order** grants exactly the relief requested

### Sworn-vs-argued discipline

- [ ] Verifies legal conclusions in the motion are **not** repeated as
      sworn facts in the affidavit (§ 9-11-56(e) personal knowledge)

## Common failure modes

- Accepts a case citation without verifying it in `key-cases.md`
- Uses an unverified S.E.2d pin-cite for *Hill v. American Express*
- Misses a date discrepancy between the motion and the affidavit
- Lets legal argument creep into the affidavit as a sworn fact
