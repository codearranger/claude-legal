# tn-personal-injury — HCLA 60-day pre-suit notice + certificate of good faith

## Prompt

I want to sue a hospital and two doctors in Tennessee for
medical malpractice. A friend told me I have to "send some
kind of notice" before filing. What exactly is required, when
does the clock run, and what happens if I get a piece wrong?

## Expected triggers

- `tn-personal-injury`
- `tn-deadlines`

## Acceptance criteria

### Terminology

- [ ] Uses the Tennessee statutory term **"health care
      liability action"** (HCLA), not "medical malpractice"
- [ ] Cites the governing chapter as **Tenn. Code Ann. § 29-26-
      101 et seq.**

### Pre-suit notice (§ 29-26-121)

- [ ] Identifies the **60-day pre-suit notice** requirement —
      written notice to **each defendant** health-care
      provider at least 60 days before filing the complaint
- [ ] Lists the required content: (1) identity of claimant +
      relationship; (2) plaintiff DOB + last 4 of SSN; (3) full
      name + address of each notified provider; (4) full name +
      address of each other provider being notified; (5) **HIPAA-
      compliant medical authorization**; (6) list of all
      providers notified
- [ ] Cites the effect of compliant notice: **extends the
      applicable SOL by 120 days** (1-year + 120-day = ~16
      months from accrual)
- [ ] States that the **3-year statute of repose under
      § 29-26-116 is NOT extended** by the pre-suit notice
      extension — a sharp trap for older claims

### Certificate of good faith (§ 29-26-122)

- [ ] Identifies the **certificate of good faith** required
      with the complaint where expert testimony is required
- [ ] Lists the certificate's required averments: (1)
      consultation with one or more experts; (2) experts
      qualified under § 29-26-115; (3) experts have provided
      signed written statements of good-faith basis; (4)
      certificate signed by counsel (or pro-se plaintiff)
- [ ] States that **failure to file the certificate generally
      results in dismissal with prejudice** under § 29-26-122(c)
      and the dismissal is **not curable by amendment**

### Expert qualifications (§ 29-26-115) — the contiguous-state rule

- [ ] Identifies the **contiguous-state rule**: an expert must
      have practiced in Tennessee or in a state bordering
      Tennessee in the year preceding the alleged negligence
- [ ] Lists Tennessee's 8 contiguous states: Kentucky,
      Virginia, North Carolina, Georgia, Alabama, Mississippi,
      Arkansas, Missouri (correct count of 8 is acceptable
      without listing all)

### Common-pitfall awareness

- [ ] Flags **defective pre-suit notice** as the most common
      HCLA case-killer, especially missing or non-compliant
      HIPAA authorization
- [ ] Cites *Stevens ex rel. Stevens v. Hickman Community
      Health Care Services, Inc.*, 418 S.W.3d 547 (Tenn. 2013),
      for the substantial-compliance standard

## Common failure modes

- Uses "medical malpractice" instead of "health care liability
  action"
- Says pre-suit notice is 30 days (it's 60)
- Says the SOL extension is 60 or 90 days (it's 120)
- Asserts the 3-year statute of repose is extended by pre-suit
  notice (it's not — separate trap)
- Treats missing certificate of good faith as curable
- Misses the contiguous-state rule entirely
- Sends notice to the hospital but not to each individual
  physician defendant
