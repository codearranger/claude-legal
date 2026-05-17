# wa-commercial-disputes — Shareholder derivative + judicial dissolution

## Prompt

I own 30% of a Washington close corporation. The 70% majority
shareholder has been paying himself excessive compensation,
declined to declare dividends for 5 years, and just fired me
from my employment with the company. What are my remedies?

## Expected triggers

- `wa-commercial-disputes`

## Acceptance criteria

- [ ] Identifies **WBCA at RCW 23B** as governing
- [ ] Walks fiduciary-duty framework — directors' duty of
      care + loyalty + good faith
- [ ] Identifies **derivative claim** under RCW 23B.07.400
      for excessive compensation (breach of fiduciary duty)
      — demand on board generally required unless excused
- [ ] Identifies **judicial dissolution** under RCW
      23B.14.300 — court can dissolve on shareholder
      showing of director illegality / oppressive / fraud
      conduct + waste of corporate assets
- [ ] Applies *Scott v. Trans-System, Inc.*, 148 Wn.2d 701
      (2003) **reasonable-expectations test** for
      oppression in closely-held corporations:
      employment-as-shareholder-benefit + freeze-out
      pattern + excessive compensation diverting earnings
- [ ] Walks **dissenters' rights** under RCW 23B.13 if a
      qualifying corporate action triggers appraisal
- [ ] Notes oppression remedy can be tailored — buy-out
      (most common); appointment of receiver; injunctive
      relief; less commonly outright dissolution
- [ ] Considers buyout valuation methodology — fair value
      vs. fair market value

## Common failure modes

- Treating compensation claim as direct (it's usually
  derivative)
- Missing demand-on-board prerequisite
- Confusing dissenters' rights with dissolution
- Wrong test (don't apply Delaware reasonable-expectations
  case law unmodified)
