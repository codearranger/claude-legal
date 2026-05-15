# ny-nassau-dc / ny-suffolk-dc — District Court format compliance

## Prompt

I have a $12,000 consumer-debt case filed against me in
Nassau District Court at 99 Main Street, Hempstead. What
court is this and what format rules apply?

## Expected triggers

- `ny-nassau-dc`
- `ny-statewide-format`
- `ny-county-courts` (delegating)

## Acceptance criteria

- [ ] Identifies **Nassau County District Court** as a
      separate trial court established under the **Uniform
      District Court Act (UDCA)** — not Supreme Court, not
      Civil Court of the City of New York
- [ ] Civil jurisdiction up to **$15,000**
- [ ] Format rules at **22 NYCRR Part 212** (not Part 202)
- [ ] Notes that the **CCFA** (2022) and **22 NYCRR
      § 202.27-a** default-judgment scrutiny apply
- [ ] Notes that Nassau District Court has expanded
      **NYSCEF** for many civil case types
- [ ] Identifies the **First District** (countywide civil)
      vs. the geographic Districts 2-6
- [ ] Cross-references `ny-consumer-debt` for the debt-
      defense substance

## Common failure modes

- Confuses Nassau District Court with Nassau County Supreme
  Court (`ny-nassau`) — they are different courts at different
  courthouses
- Cites 22 NYCRR Part 202 instead of Part 212
- Suggests filing in Supreme Court because of the dollar
  amount (the $15,000 UDCA ceiling is more restrictive than
  Supreme Court's general jurisdiction)
