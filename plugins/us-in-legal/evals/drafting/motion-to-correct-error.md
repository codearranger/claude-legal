# in-draft-motion — T.R. 59 Motion to Correct Error (Indiana's pre-appeal device)

## Prompt

I lost a bench trial in an Indiana Superior Court three weeks
ago and I think the judge got the damages badly wrong — the
number is way higher than the evidence supports. I also just
found a document that didn't come up at trial. Someone told me
there's a special Indiana motion I have to file before I can
appeal. What is it and how do I draft it?

## Expected triggers

- `in-draft-motion`
- `in-post-judgment`
- `in-deadlines`
- `in-statewide-format`

## Acceptance criteria

### Identifying the device

- [ ] Identifies the **Motion to Correct Error under Trial Rule
      59** as the Indiana-specific post-trial device — it has no
      direct federal analog and is a **required preliminary step
      for preserving certain issues for appeal**
- [ ] Maps the prompt's facts to the T.R. 59 grounds: **newly
      discovered evidence** and **excessive or inadequate
      damages** are among the issues that must be raised by a
      T.R. 59 motion to be preserved (read the current ground
      enumeration from the skill / Trial Rules corpus rather than
      asserting subsection letters from memory)
- [ ] Distinguishes T.R. 59 (errors at trial / in the judgment,
      30-day window) from **T.R. 60(B)** relief from judgment
      (equitable grounds, longer windows) — see `in-post-judgment`

### The jurisdictional clock

- [ ] States the **30-day filing deadline from entry of final
      judgment** and flags it as **jurisdictional** — late
      filings are dismissed
- [ ] Flags that the deadline **cannot be extended under T.R.
      6(B)** (*Cavinder Elevators, Inc. v. Hall*, 726 N.E.2d 285
      (Ind. 2000)) — verify the cite via `in-fact-check` rather
      than asserting from memory
- [ ] Notes the **deemed-denied** mechanism: if the trial court
      does not rule within the rule's window (45 days per the
      skill — read the current count from the corpus), the motion
      is deemed denied and the **appeal clock starts**
- [ ] Connects to the Notice of Appeal under **Ind. App. R. 9**:
      30 days from final judgment OR from the ruling (or deemed
      denial) on the T.R. 59 motion; computes dates via
      `case-calendar.py`

### Drafting mechanics

- [ ] States each alleged error **with specificity** and the
      relief sought (T.R. 59 requires specificity; a general
      "the judgment is wrong" motion fails)
- [ ] Caption + numbered paragraphs + signature per
      `in-statewide-format`; proposed order included

## Common failure modes

- Treats T.R. 59 as optional for newly-discovered-evidence or
  damages issues (those must be raised by T.R. 59 to be
  preserved)
- Suggests asking for an extension of the 30-day deadline under
  T.R. 6(B)
- Confuses T.R. 59 with T.R. 60(B) or with a federal Rule 59
  new-trial motion
- Misses the deemed-denied rule and blows the appeal window
  waiting for a ruling
- States the errors generally instead of with specificity
