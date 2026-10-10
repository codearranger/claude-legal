# tx-draft-note — Notice of Hearing (oral hearing vs. submission)

## Prompt

I filed a motion in my Texas district court case. How do I set it for
a hearing, and draft the Notice of Hearing? I'd rather have it decided
on the papers if I can.

## Expected triggers

- `tx-draft-note`
- `tx-schedule-hearing`

## Acceptance criteria

### Right document and posture

- [ ] Produces a document titled **Notice of Hearing** (the Texas
      scheduling document) — not a "note for trial setting" or other
      non-Texas label
- [ ] Distinguishes an **oral hearing** from a **submission** (decided
      on the papers) setting, and frames the notice for **submission**
      given the user's preference, while noting that whether submission
      is available depends on the court's local rules / coordinator
- [ ] Explains the setting is obtained from the **court coordinator**
      (district / county court) and routes the mechanics to
      `tx-schedule-hearing`

### Timing

- [ ] States the notice must give the opposing party adequate notice of
      the setting (TRCP 21/21a service) and, if the motion is a summary
      judgment, accounts for the **21-day** pre-hearing service window
      — reading day-counts from the corpus / `tx-deadlines`
- [ ] Accounts for the **+3 days** added for service by mail / fax /
      email under TRCP 21a where applicable (point to the corpus for
      the exact triggers)

### Form

- [ ] Applies the `tx-statewide-format` caption/footer and includes a
      **certificate of service**

## Common failure modes

- Mislabels the document or invents a non-Texas scheduling instrument
- Conflates oral hearing and submission settings
- Omits the certificate of service or the service/notice window
