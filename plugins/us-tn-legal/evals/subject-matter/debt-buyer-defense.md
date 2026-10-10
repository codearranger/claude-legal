# tn-consumer-debt — Defending a debt-buyer suit in General Sessions

## Prompt

A company I've never heard of (a debt buyer) sued me in
General Sessions Court in Tennessee on an old credit-card
account they say they bought. They didn't attach the account
agreement or any bill of sale. How do I defend this?

## Expected triggers

- `tn-consumer-debt`
- `tn-general-sessions`

## Acceptance criteria

### Chain-of-title challenge

- [ ] Frames the central defense as a **chain-of-title /
      standing** challenge: the debt buyer must prove the
      unbroken assignment from the original creditor through
      each intermediate assignee to the plaintiff
- [ ] Targets the missing proof: original signed account
      agreement, each bill of sale / pool transfer document,
      and the data showing **this specific account** in the
      purchased pool

### Statute of limitations

- [ ] Identifies the **6-year statute of limitations on
      written contracts / open accounts** under **T.C.A.
      § 28-3-109** (note that the clock for an open/revolving
      account is fact-dependent — commonly tied to the date of
      last payment/activity; verify per case)
- [ ] Notes the **4-year UCC sale-of-goods SOL (T.C.A.
      § 47-2-725)** may displace the 6-year period where the
      underlying transaction is a sale of goods

### 2024 debt-buyer documentation rule

- [ ] Cites **T.C.A. § 20-6-104** (2024) — before any
      **default judgment**, a subsequent-creditor / debt-buyer
      plaintiff must present documentation showing **authority
      to collect** the debt AND **at least one document showing
      the debt's existence**, irrespective of any affidavit
- [ ] Notes this rule does **not** apply to original creditors
      / lienholders

### Collection Service Act licensing

- [ ] Raises the **Tennessee Collection Service Act (T.C.A.
      Title 62, ch. 20)** licensing requirement (§ 62-20-105),
      administered by the Tennessee Collection Service Board
- [ ] Correctly notes the statutory **limit**: a debt
      collected by voluntary payment or final judgment may not
      be set aside solely for the collector's lack of license —
      so a categorical "unlicensed = void" theory is limited

### TCPA caveat (Pursell)

- [ ] Flags that the **Tennessee Consumer Protection Act
      (T.C.A. § 47-18-101 et seq.)** generally does **not reach
      the act of collecting a debt**, per ***Pursell v. First
      American National Bank*, 937 S.W.2d 838 (Tenn. 1996)** —
      framed as fact-specific, not a categorical bar
- [ ] Points to the **FDCPA** + Collection Service Act as the
      primary debt-collection regimes

## Common failure modes

- Treats the suit as automatically valid because a debt buyer
  filed it (misses the chain-of-title burden)
- Asserts the TCPA covers debt collection without the Pursell
  caveat
- Claims an unlicensed collector's judgment is automatically
  void (ignores the § 62-20-105 limit)
- Omits the 2024 § 20-6-104 default-judgment documentation rule
- Hard-codes SOL trigger dates instead of flagging the
  open-account accrual question as fact-dependent
