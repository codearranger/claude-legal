# tx-first-30-days — responding to an original petition

## Prompt

I just got served with an original petition in a Texas district court.
I have about three weeks to respond. What are my options for the first
filing, and what could I lose if I pick the wrong one?

## Expected triggers

- `tx-first-30-days`
- `tx-deadlines`

## Acceptance criteria

### Deadline

- [ ] States the **TRCP 99 Monday-rule** answer deadline (10:00 a.m. on
      the Monday next after 20 days from service) and computes it via
      `tx-deadlines` — not a flat 20 days

### Response menu

- [ ] Explains a **general denial (TRCP 92)** as the baseline answer
      that puts the plaintiff to its proof
- [ ] Flags that certain matters must be raised by a **verified denial
      under TRCP 93** (e.g., lack of capacity, defect of parties,
      denial of a **sworn account under TRCP 185**) — and that a bare
      general denial waives them; reads the TRCP 93 list from the
      corpus
- [ ] Identifies **special exceptions (TRCP 91)** as the vehicle to
      challenge a vague/defective pleading, and notes there is **no
      general demurrer** in Texas
- [ ] Identifies a **TRCP 91a motion to dismiss** (no basis in law or
      fact) filed within **60 days** of the challenged pleading, and
      routes the current fee-shifting rule to the corpus (made
      discretionary by 2019 legislation)

### Affirmative defenses preserved

- [ ] Reminds that affirmative defenses (e.g., limitations) must be
      pleaded in the answer or risk waiver

## Common failure modes

- Uses a flat 20-day deadline
- Treats a general denial as sufficient against a sworn account
- Calls the special exceptions a "demurrer" or a federal 12(b)(6)
- Hard-codes the 91a fee rule instead of deferring to the corpus
