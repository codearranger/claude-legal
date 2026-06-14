# in-consumer-debt — FDCPA + Indiana DCSA dual-track liability + no state licensing

## Prompt

A debt collector has been calling me multiple times a day,
told me they'd have me arrested if I didn't pay, and sued
me in a Marion County small-claims court that's not in my
township. I'm in Indianapolis. Do I have any claims against
them, and does Indiana have its own debt-collection law
on top of the federal law?

## Expected triggers

- `in-consumer-debt`
- `in-first-30-days`

## Acceptance criteria

### Indiana-specific posture — no state licensing regime

- [ ] States clearly that Indiana has **NO state
      collection-agency licensing regime** — unlike
      California (CDCLA), Oregon (ORS 697), and
      Washington (RCW 19.16); Indiana defense therefore
      rests primarily on the federal FDCPA + state DCSA
- [ ] Does NOT suggest filing a complaint with an
      "Indiana Department of Financial Institutions
      license" check (there is no such regime for debt
      collectors under current Indiana law)

### FDCPA violations identified

- [ ] Identifies the **"7 in 7" call frequency issue**
      as a potential Reg F § 1006.6 violation (telephone
      calls exceeding 7 times in 7 days to the same
      consumer about a particular debt)
- [ ] Identifies the **false threat of arrest** as a
      potential FDCPA § 1692e(4) violation (threat to
      take action that cannot legally be taken — arrest
      for civil debt)
- [ ] Identifies the **wrong venue** as a potential
      FDCPA § 1692i violation — debt collectors must
      sue in the county/district where the consumer
      resides or signed the contract; filing in the
      wrong township small-claims court creates FDCPA
      § 1692i liability
- [ ] Notes FDCPA statutory damages: up to $1,000 per
      action + actual damages + attorney's fees (15
      U.S.C. § 1692k(a))

### Indiana DCSA — IC 24-5-0.5

- [ ] Identifies the **Indiana Deceptive Consumer Sales
      Act (DCSA), IC 24-5-0.5**, as Indiana's UDAP /
      state consumer-protection overlay
- [ ] States the **30-day pre-suit cure demand letter
      requirement** under IC 24-5-0.5-5(a) before
      filing a DCSA cause of action (except for
      "incurable deception" under IC 24-5-0.5-3(b)(40))
- [ ] States DCSA damages: actual damages or $500
      statutory minimum, **treble damages** for uncured /
      incurable deception, and **mandatory attorney's
      fees** under IC 24-5-0.5-4(a)

### Compulsory counterclaim strategy

- [ ] Notes that FDCPA / DCSA claims in response to a
      pending collection lawsuit may be raised as
      **compulsory counterclaims** under T.R. 13(A),
      giving significant settlement leverage

## Common failure modes

- States Indiana requires debt collectors to be licensed
  at the state level (Indiana has no such requirement)
- Omits the pre-suit DCSA cure demand letter requirement
- Asserts arrest is possible for civil debt (it is not,
  making the collector's threat an FDCPA violation)
- Fails to identify § 1692i as the wrong-venue violation
- Asserts FDCPA statutory damage amounts from memory
  without cross-referencing the corpus
