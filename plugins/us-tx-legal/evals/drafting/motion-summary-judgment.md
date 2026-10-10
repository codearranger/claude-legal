# tx-draft-motion — motion for summary judgment (166a(c) / 166a(i))

## Prompt

A debt buyer sued me in a Texas district court and they have no
records connecting me to the account. Draft a motion for summary
judgment, with a notice of hearing and a proposed order. The hearing
I want to set is on June 1.

## Expected triggers

- `tx-draft-motion`
- `tx-statewide-format`

## Acceptance criteria

### Right summary-judgment vehicle

- [ ] Recognizes Texas has **two** summary-judgment paths — a
      **traditional motion under TRCP 166a(c)** and a **no-evidence
      motion under TRCP 166a(i)** — and, given "they have no records,"
      frames a no-evidence motion (or explains the choice) rather than
      treating Texas summary judgment as a single federal-style Rule 56
- [ ] For a no-evidence motion, states it must identify the **specific
      elements** on which there is no evidence and that the burden then
      shifts to the non-movant to produce more than a scintilla
- [ ] Cites **Tex. R. Civ. P. 166a** (not "Rule 56")

### Service / hearing timing

- [ ] States the motion must be served at least **21 days before the
      hearing** and the response is due **7 days before the hearing**
      (TRCP 166a(c)), and computes the latest service date / response
      date backward from the user's June 1 hearing via `tx-deadlines`
- [ ] Produces a separate **Notice of Hearing** (oral hearing or
      submission) — does not bury the setting in the motion

### Form

- [ ] Produces a **separate proposed order** that only the judge signs
- [ ] Applies the `tx-statewide-format` caption/format (line numbering,
      `Page X of Y` footer) and includes a **certificate of service**
- [ ] Supports the motion with summary-judgment evidence (affidavit or
      a CPRC § 132.001 unsworn declaration), not unsworn argument

## Common failure modes

- Treats Texas summary judgment as one federal-style motion and omits
  the no-evidence option
- Uses a federal 28-day / Rule 56 service window instead of 21/7
- Drafts an order the movant signs, or merges the order into the motion
