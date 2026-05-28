# tn-personal-injury — Negligence claim end-to-end intake

## Prompt

A friend was injured 11 months ago in Tennessee — rear-ended at
a stoplight in Memphis by a delivery driver for a private
shipping company. She has medical bills around $35,000 and lost
3 weeks of work. What's the timeline to file, and what should
she think about before suing?

## Expected triggers

- `tn-personal-injury`
- `tn-deadlines`

## Acceptance criteria

### Statute of limitations

- [ ] Identifies the **1-year personal-injury SOL** under
      **Tenn. Code Ann. § 28-3-104(a)(1)** — running out in
      approximately 1 month from the inquiry
- [ ] Flags the **3-year property-damage SOL** at § 28-3-105
      as separate — the vehicle-damage claim runs on a different
      clock from the personal-injury claim
- [ ] Recommends **filing within 30 days** to preserve the
      personal-injury claim with margin

### Comparative-fault framework

- [ ] Cites ***McIntyre v. Balentine*, 833 S.W.2d 52 (Tenn.
      1992)** — modified comparative fault with the **49% bar**
- [ ] Notes the **several-liability** default for non-
      intentional torts post-*McIntyre*
- [ ] Identifies the need to assess fault attribution among all
      drivers + non-parties + possibly the friend herself

### Damages framework

- [ ] Identifies the **non-economic cap** under Tenn. Code
      Ann. § 29-39-102 — **$750,000** standard; the case as
      stated does not appear to be catastrophic
- [ ] Recognizes that **economic damages are uncapped** —
      medical bills + wage loss + future medicals
- [ ] (Bonus) Notes the **collateral-source rule** still
      applies; health-insurance payments do not reduce the
      tortfeasor's liability

### UM/UIM analysis

- [ ] Flags the **uninsured / underinsured motorist (UM/UIM)**
      analysis under **Tenn. Code Ann. §§ 56-7-1201** et seq.
- [ ] Recommends serving any UM/UIM carrier under § 56-7-1206
      contemporaneously with serving the defendant

### Forum considerations

- [ ] Identifies **Shelby County Circuit Court** (30th JD) as
      the likely forum
- [ ] Notes that **General Sessions** has a $25,000 cap and
      would NOT be appropriate for a case with $35,000 in
      medical bills alone (over the cap)
- [ ] (Bonus) Notes the **delivery-company defendant**
      analysis: if the driver was an employee, respondeat
      superior pulls in the employer; if an independent
      contractor with a national franchisor, the analysis
      becomes more complex

### Insurance posture

- [ ] Recommends **pre-suit demand on the defendant's auto
      liability insurer** before filing — Tennessee does not
      have a pre-suit-notice requirement for ordinary auto-
      negligence claims, but a demand sets up bad-faith
      exposure under Tennessee's bad-faith statute at § 56-7-105

### Things NOT in play

- [ ] Does NOT incorrectly invoke the HCLA (no health-care
      defendant)
- [ ] Does NOT incorrectly invoke the GTLA (private defendant)
- [ ] Does NOT incorrectly invoke the TPLA (no defective
      product)

## Common failure modes

- Misstates the SOL as 2 or 3 years
- Treats medical bills + wage loss as capped by § 29-39-102
  (they're not — that's non-economic only)
- Tries to file in General Sessions despite the case value
- Misses the UM/UIM service requirement
- Confuses the GTLA $300k/$700k caps with the general non-
  economic cap
- Suggests pre-suit notice (only HCLA / GTLA have those gates)
- Cites the *Rye* summary-judgment standard as if it changes
  the SOL framework
