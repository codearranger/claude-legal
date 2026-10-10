# oh-draft-motion — Motion to compel scaffold

## Prompt

I need to file a motion to compel discovery in my Ohio
Common Pleas case. The defendant (a debt buyer) hasn't
answered my Requests for Production after 28 days plus the
meet-and-confer I sent two weeks ago. Case is Midland
Funding LLC v. Jane Doe in Cuyahoga County, case
CV-25-987654. I'm pro se.

## Expected triggers

- `oh-draft-motion`
- `oh-discovery`
- `oh-statewide-format`
- `oh-cuya`
- `oh-pro-se`

## Acceptance criteria

### Structure

- [ ] Caption per Civ. R. 10(A) with court name
      "IN THE COURT OF COMMON PLEAS OF CUYAHOGA COUNTY,
      OHIO" and case number `CV-25-987654`
- [ ] Title: `DEFENDANT'S MOTION TO COMPEL DISCOVERY`
- [ ] Introduction paragraph
- [ ] Statement of facts (discovery served / date;
      response deadline / passed; meet-and-confer / date)
- [ ] Legal authority section citing **Civ. R. 37(A)** and
      **Civ. R. 37(E)** (meet-and-confer)
- [ ] Argument applying authority to facts
- [ ] Prayer for relief: order compelling responses + fees
      under Civ. R. 37(A)(5)(a)
- [ ] Certificate of service
- [ ] Signature block with pro se designation (no Atty.
      Reg. #)

### Content

- [ ] Cites Civ. R. 26(B) scope
- [ ] Cites Civ. R. 37(A)(1) good-faith conferral
      requirement
- [ ] References the meet-and-confer letter as an exhibit
- [ ] Does NOT cite FRCP 37 (federal); Ohio uses Civ. R. 37

## Common failure modes

- Citing FRCP 37 instead of Ohio Civ. R. 37
- Missing certificate of service
- Forgetting Civ. R. 37(E) good-faith conferral
- Using `vs` (no period) or `v.` — Ohio uses `vs.`
- Listing a fake Ohio attorney registration number on a
  pro-se filing
