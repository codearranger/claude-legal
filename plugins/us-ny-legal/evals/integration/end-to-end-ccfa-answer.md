# Integration — End-to-end CCFA answer packet

## Prompt

I was served with a Summons and Complaint by Velocity
Investments LLC in NYC Civil Court last Tuesday (April 15,
2026). The complaint alleges I owe $4,800 on an account
"purchased from Capital One" in 2022 with no other detail.
The case is 2026-CV-002345. I am pro se. Draft me an Answer
packet including affirmative defenses, a counterclaim, and a
verification.

## Expected triggers

- `ny-first-30-days`
- `ny-statewide-format`
- `ny-county-courts`
- `ny-consumer-debt`
- `ny-draft-declaration`
- `ny-deadlines`
- `ny-pro-se`

## Acceptance criteria

### Caption

- [ ] "CIVIL COURT OF THE CITY OF NEW YORK" + "COUNTY OF
      [borough]"
- [ ] Two-block caption with `-against-`
- [ ] Case number 2026-CV-002345
- [ ] Title in ALL CAPS: "ANSWER WITH AFFIRMATIVE DEFENSES
      AND COUNTERCLAIMS"

### Substantive Answer

- [ ] Numbered admissions / denials matching plaintiff's
      paragraphs (CPLR 3018(a))
- [ ] Pleads affirmative defenses with specificity, including:
      - failure to comply with **CPLR 3015(e) heightened
        pleading** (no chain of title, no itemization, no
        original-creditor identification, no last-activity
        date)
      - **statute of limitations** under **CPLR 214-i** (3
        years on consumer credit, post-CCFA)
      - lack of standing (no chain of title)
      - violation of **GBL § 601** (mini-FDCPA — false
        representation of right to collect)
      - violation of **FDCPA 15 U.S.C. §§ 1692e / 1692f** as
        counterclaim
- [ ] Counterclaims under FDCPA + GBL § 349 (deceptive acts)

### Verification

- [ ] **CPLR 3020-3021 verification** by the answering party
      (consumer-credit answers are routinely verified)
- [ ] Uses the **post-2023 CPLR 2106 universal affirmation**
      or CPLR 2309 affidavit verification

### Deadline math

- [ ] Answer must be served within 20 days of personal
      service per CPLR 320(a); served April 15, 2026 → due
      **May 5, 2026** (counting forward 20 calendar days
      including weekends per CPLR 2103, with weekend roll-
      over under General Construction Law § 25-a)

### Service

- [ ] Service by mail on plaintiff (CPLR 2103(b)(2)) — note
      the **5-day mail rule** if any responsive deadlines
      are downstream
- [ ] File Answer with NYC Civil Court Clerk (UCMS or
      paper); fee waived for pro se Answer

## Common failure modes

- Defaults to FRCP 8/12 framing
- Forgets the 3-year CCFA SOL and pleads the 6-year contract
  SOL
- Verifies under CPLR 2309 with notary when CPLR 2106
  affirmation suffices
- Uses `v.` party separator
- Misses the GBL § 601 mini-FDCPA defense
- Treats this as a Supreme Court case (wrong court for a
  $4,800 claim — NYC Civil Court is correct)
