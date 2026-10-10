# ca-draft-order — Proposed Order scaffold

## Prompt

The judge granted my motion to compel further responses at today's
hearing. I'm the prevailing party. Help me draft the proposed
order.

## Expected triggers

- `ca-draft-order`
- `ca-statewide-format`
- `ca-submit-order`

## Acceptance criteria

### Caption

- [ ] CRC 2.111 caption
- [ ] Title: "[PROPOSED] ORDER GRANTING DEFENDANT'S MOTION TO
      COMPEL FURTHER RESPONSES TO REQUESTS FOR PRODUCTION
      (SET ONE)" — with "[PROPOSED]" prefix common in CA
      practice

### Recitals

- [ ] "On [date], the Court heard Defendant's Motion to Compel
      Further Responses..."
- [ ] Identifies appearing parties / counsel
- [ ] Notes the papers considered (motion, opposition, reply,
      separate statement, declaration)

### Order body

- [ ] Specific operative language ("IT IS HEREBY ORDERED")
- [ ] Specific relief: which RFPs, by when
- [ ] Sanctions if awarded — amount + recipient
- [ ] Discovery deadline reference where applicable

### Signature

- [ ] "DATED: _________"
- [ ] "_________, JUDGE OF THE SUPERIOR COURT"

### CRC 3.1312 compliance

- [ ] Reminder note that proposed order must be served on other
      parties within 5 court days of ruling
- [ ] Reminder that other party has 5 court days to object to
      form

## Common failure modes

- Missing the "[PROPOSED]" prefix
- Putting argumentative language in the recitals
- Failing to specify which RFPs must be supplemented
- Omitting CRC 3.1312 5-court-day reminder
- Putting "IT IS SO ORDERED" without a separate "ORDERED" body
  describing specific relief
- Mis-spelled "Honorable" or wrong judge title format
