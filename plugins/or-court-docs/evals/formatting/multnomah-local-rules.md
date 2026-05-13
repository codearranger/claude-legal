# or-multcc — Multnomah Circuit Court motion practice

## Prompt

I need to reserve a hearing date for a motion in Multnomah
County Circuit Court. My case is assigned to Judge [Name].
What do I do?

## Expected triggers

- `or-multcc`
- `or-schedule-hearing`

## Acceptance criteria

### Multnomah-specific procedure

- [ ] Identifies the assigned-judge / Judicial Assistant
      (JA) email contact (NOT Civil Division for Multnomah)
- [ ] References the Multnomah judges page
      (courts.oregon.gov/courts/multnomah/judges)
- [ ] Notes that Multnomah uses individual-calendar
      scheduling (not centralized motion docket)
- [ ] References Multnomah SLR 5.025 (setting motions by
      request to JA)
- [ ] References the 3-business-day window for filing the
      Notice of Hearing under Multnomah SLR 5.015

### Email template

- [ ] Subject line includes "Hearing Date Request" and case
      identifier
- [ ] Email identifies assigned judge by name
- [ ] Proposes 2–3 dates
- [ ] Estimates argument time
- [ ] Asks about WebEx vs. in-person preference
- [ ] Has appropriate professional tone

### What NOT to do

- [ ] Does NOT direct user to a Civil Division clerk (that's
      Washington Co)
- [ ] Does NOT direct user to a centralized motion docket
      (Multnomah doesn't have one)
- [ ] Does NOT suggest emailing KCDC.CivilMGT (that's
      Washington State)

## Common failure modes

- Conflating Multnomah with Washington Co (Oregon) — the
  scheduling routing is different
- Suggesting Civil Division contact when Multnomah uses JA
  contact
- Using the WA plugin's KCDC pattern verbatim
- Forgetting the working-copy threshold (25 pages for
  Multnomah)
