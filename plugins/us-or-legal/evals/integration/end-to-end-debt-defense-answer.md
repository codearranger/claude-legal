# Integration — End-to-end debt defense (answer + counterclaims)

## Prompt

I'm Jane Doe in Multnomah Co, OR (Case 25CV01234). I was
served on April 1, 2025 by personal delivery with a complaint
from Velocity Investments, LLC, alleging I owe $7,432 on a
Bank of America credit card I don't recognize. Velocity isn't
registered with Oregon DCBS as far as I can tell from the
public database. Last activity on the account (per their
complaint) was 2017. Help me prepare a complete first-30-days
response.

## Expected triggers

- `or-first-30-days`
- `or-consumer-debt`
- `or-deadlines`
- `or-draft-motion` or `or-draft-declaration` (for the answer
  components)
- `or-pro-se`
- `or-statewide-format`
- `or-multcc`

## Acceptance criteria

### Deadline computation

- [ ] Answer due 30 days from April 1 = May 1, 2025 (no
      adjustment needed; weekday)
- [ ] References ORCP 7 C(2)
- [ ] Recommends buffer (file by April 24 or so)

### Fact-pattern triage

- [ ] Identifies Pattern 1 (debt-buyer) + Pattern 3 (time-
      barred) + Pattern 5 (unregistered) — the combination
- [ ] Recommends SOL defense as LEAD (8 years > 6-year SOL
      under ORS 12.080)

### Answer + counterclaims

- [ ] Drafts answer with paragraph-by-paragraph denials
- [ ] Includes affirmative defenses:
  - SOL (ORS 12.080)
  - Lack of capacity (ORS 697.105)
  - Lack of standing
  - ORCP 21 A(8) (failure to state)
  - OEC 803(6) foundation
- [ ] Includes counterclaims (in alternative pleading):
  - FDCPA + Reg F (15 USC § 1692; 12 CFR pt 1006)
  - Oregon UTPA (ORS 646.605 et seq.)
  - ORS 697.085 (Collection Agency)

### Discovery

- [ ] Drafts first RFPs targeting chain of title and DCBS
      registration
- [ ] Drafts RFAs targeting basic facts and registration
      status

### Procedural

- [ ] Format per UTCR 2.010
- [ ] Multnomah caption header
- [ ] Pro se signature (no OSB#)
- [ ] Certificate of Service per UTCR 1.090

### Filing instructions

- [ ] eFile via File and Serve
- [ ] Serve under ORCP 9 / UTCR 21.100
- [ ] Calendar key deadlines (response to discovery, motion
      cutoffs, etc.)

### Strategic priorities

- [ ] **SOL first** (dispositive if proven)
- [ ] ORS 697.105 capacity (also dispositive)
- [ ] Chain of title (develops through discovery)
- [ ] Counterclaims (leverage and recovery)

## Common failure modes

- Generic "answer the complaint" without specific Oregon
  defenses
- Missing the ORS 697 capacity defense
- Treating partial payment as SOL revival (wrong in Oregon)
- Forgetting to plead UTPA alongside FDCPA
- Cite-checking errors (Bluebook periods, "vs.", etc.)
- Suggesting interrogatories (not in ORCP)
- Wrong court header or "Note for Motion Docket" instead of
  Oregon "Notice of Hearing"
