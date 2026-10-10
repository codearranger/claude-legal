# tn-discovery — Propounding discovery in Circuit Court

## Prompt

I'm the defendant in a Tennessee Circuit Court case and I
want to send the plaintiff interrogatories and document
requests. How many interrogatories can I serve, and how long
do they have to respond? Would this be different if my case
were in General Sessions?

## Expected triggers

- `tn-discovery`

## Acceptance criteria

### Interrogatory cap

- [ ] States there is **no statewide numeric cap** on
      interrogatories under Tenn. R. Civ. P. 33
- [ ] **Tells the litigant to verify the venue's local rules**,
      which may impose a numeric limit (verify-venue point)

### Response timing

- [ ] States responses are due **30 days** after service
      (cite the controlling rule; note the longer period where
      a defendant is served before answering — read the
      current figure from the references corpus)
- [ ] Identifies the discovery devices: Rule 33
      interrogatories, Rule 34 requests for production, Rule 36
      requests for admission, Rules 30/31 depositions, and Rule
      37 motion to compel / sanctions

### General Sessions contrast

- [ ] States that **General Sessions has no formal discovery
      as of right** — the discovery rules described apply in
      Circuit/Chancery, not General Sessions

## Common failure modes

- Asserts a fixed interrogatory cap (e.g., "25") as statewide
  law instead of flagging that it is local-rule-dependent
- Cites FRCP 33's 25-interrogatory presumptive limit as
  Tennessee law
- Misstates the response period
- Tells the litigant they can propound formal discovery in
  General Sessions
