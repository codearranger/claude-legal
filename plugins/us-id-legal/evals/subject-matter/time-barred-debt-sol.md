# id-consumer-debt — statute-of-limitations defense

## Prompt

I'm being sued in Idaho over a credit-card debt where the last
payment I made was more than five years ago. Is it too late for them
to sue?

## Expected triggers

- `id-consumer-debt`
- `id-deadlines`

## Acceptance criteria

- [ ] Identifies the **statute of limitations as an affirmative
      defense** that must be pleaded (I.R.C.P. 8(c))
- [ ] States the relevant Idaho limitations periods, reading them from
      the corpus: **written contract, 5 years (I.C. § 5-216)**;
      **oral / open account, 4 years (I.C. § 5-217)** with accrual on
      an open account governed by **I.C. § 5-222**
- [ ] Flags that whether a credit-card account is a "written contract"
      or an "open account" is **litigable / fact-dependent** and
      routes the case-law question to case-law research rather than
      asserting a settled Idaho rule from memory
- [ ] Distinguishes the underlying-debt SOL from the **11-year action-
      on-a-judgment period (I.C. § 5-215)** if a judgment already exists
- [ ] Computes the accrual date / cutoff using `id-deadlines`
      (I.R.C.P. 2.2)

## Common failure modes

- Asserts a single settled SOL for credit cards without flagging the
  written-vs-open-account dispute
- Confuses the debt SOL with the judgment SOL
- Treats the SOL as self-executing rather than a pleaded defense
