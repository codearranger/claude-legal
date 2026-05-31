# az-file-packet — AZTurboCourt assembly + sensitive-data redaction

## Prompt

I've finished drafting my answer and a couple of supporting
documents for my Arizona Superior Court case. How do I actually
file them? I think Arizona uses an online system, and I'm worried
because my documents have my full Social Security number and bank
account numbers in a couple of places.

## Expected triggers

- `az-file-packet`
- `az-statewide-format`

## Acceptance criteria

### E-filing assembly (AZTurboCourt)

- [ ] Identifies **AZTurboCourt** as Arizona's e-filing system and
      walks the packet assembly (document-type selection, lead
      document vs. attachments, proposed orders lodged separately) —
      reads the current mechanics from the references corpus rather
      than asserting screens/steps from memory
- [ ] Notes which courts/case types are e-filing vs. paper and that
      the litigant should confirm the forum's current requirement
      from the corpus

### Sensitive-data redaction

- [ ] Flags that **sensitive personal data** (full SSN, full
      financial-account numbers, etc.) must be **redacted or
      restricted** per the Arizona rule governing privacy/redaction
      in court filings — cite the governing Ariz. R. Civ. P. /
      Supreme Court rule by number and read the current
      redaction requirements (what to truncate, sealed/restricted
      filing) from the corpus rather than asserting them
- [ ] Recommends a preflight redaction pass before submission

### Composition / format

- [ ] Confirms each document carries the **Ariz. R. Civ. P. 10**
      caption + line numbering + signature via `az-statewide-format`
      before assembly

## Common failure modes

- Asserts AZTurboCourt screens/steps from memory instead of reading
  current mechanics from the corpus
- Misses the sensitive-data redaction requirement or asserts the
  redaction rule from memory
- Lodges a proposed order as a merged attachment instead of
  separately
