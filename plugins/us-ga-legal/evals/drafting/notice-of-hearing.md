# ga-draft-note — Georgia Rule Nisi / Notice of Hearing (the court sets the date)

## Prompt

My motion in the State Court of Gwinnett County has been fully briefed
for weeks and nothing is happening. How do I get a hearing date in
Georgia, and what document do I file to tell everyone the date?

## Expected triggers

- `ga-draft-note`
- `ga-schedule-hearing`
- `ga-statewide-format`

## Acceptance criteria

### The Georgia scheduling model

- [ ] Explains that in Georgia civil practice oral argument is obtained by
      a **Rule Nisi** under **USCR 6.3 / 6.4** — the movant submits a
      proposed Rule Nisi and the judge (or judicial assistant) sets the
      date; the party does **not** self-calendar a motion docket
- [ ] Routes the user to the correct party-side action — a chambers /
      judicial-assistant request for a setting per the assigned judge's
      practice — reading the per-court scheduling-contact practice from
      the skill references (cross-reference `ga-schedule-hearing`)

### The notice a party files

- [ ] Identifies the party-filed variants this skill drafts — a **Notice
      of Hearing** (echoing a court-set date to the parties), Notice of
      Filing, Notice of Leave of Absence (USCR 16) — and drafts the one
      that fits
- [ ] The drafted notice carries the case caption, the motion being set,
      the date/time/courtroom as set by the court, and a certificate of
      service under O.C.G.A. § 9-11-5

### Composition

- [ ] Caption per the Georgia caption naming the **State Court of
      Gwinnett County** with "Civil Action File No." (`ga-statewide-format`)
- [ ] Reads per-court scheduling-contact practice (and Gwinnett's
      Odyssey eFileGA channel) from the references rather than inventing
      chambers emails or local-rule numbers

## Common failure modes

- Imports a self-scheduling "note for motion docket" model into Georgia
  instead of the Rule Nisi practice
- Drafts a notice as if the party, rather than the court, sets the
  hearing date
- Invents a chambers email address or local-rule citation instead of
  reading per-court practice from the references
