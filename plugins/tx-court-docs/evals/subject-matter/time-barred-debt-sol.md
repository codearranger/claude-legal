# tx-consumer-debt — time-barred debt SOL + no-revival rule

## Prompt

A debt buyer is suing me in Texas on an old credit-card account. My
last payment was more than five years ago, and they're saying that a
small payment I made last year "restarted the clock." Is the suit too
late, and is that revival argument right?

## Expected triggers

- `tx-consumer-debt`
- `tx-deadlines`

## Acceptance criteria

### SOL as a pleaded defense

- [ ] Identifies the statute of limitations as an **affirmative defense
      that must be pleaded** in the answer or it is waived
- [ ] States the **4-year** limitations period for a debt/contract
      claim under **CPRC § 16.004** (residual § 16.051), confirming the
      period against
      `../tx-law-references/references/tx-statutes-debt/`

### No revival by partial payment (Texas-specific)

- [ ] Explains that under **Tex. Fin. Code § 392.307** a payment on, or
      acknowledgment of, **time-barred consumer debt does NOT revive**
      the limitations period, and that the collector owes a statutory
      notice when collecting out-of-statute consumer debt — reading the
      current § 392.307 text/notice requirement from the corpus rather
      than reciting it
- [ ] Distinguishes the general written-acknowledgment revival rule
      (**CPRC § 16.065**) and explains § 392.307 controls for
      time-barred **consumer** debt — so the "small payment restarted
      the clock" argument is contestable, not conceded

### Computation

- [ ] Frames the accrual/cutoff analysis (accrual on default / last
      payment is fact-dependent) and computes via `tx-deadlines`,
      routing the case-law question to case-law research

## Common failure modes

- Treats the SOL as self-executing rather than a pleaded defense
- Concedes that the recent payment revived the debt
- Recites the § 392.307 / § 16.004 text or day-counts from memory
