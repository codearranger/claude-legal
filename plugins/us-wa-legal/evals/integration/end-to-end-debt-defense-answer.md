# Integration — End-to-end debt-defense answer

## Prompt

I just got served with a complaint in King County District
Court. Plaintiff is "LVNV Funding, LLC." The complaint
alleges $6,200 owed on a Discover credit-card account, last
payment about 4 years ago. The complaint attaches monthly
statements and a "Certificate of Indebtedness" but no
cardholder agreement. Help me draft my answer with
affirmative defenses and counterclaims.

## Expected triggers

- `wa-consumer-debt`
- `wa-first-30-days`
- `wa-discovery`
- `wa-statewide-format`
- `wa-kcdc`
- `wa-pro-se`
- `wa-draft-motion` or `wa-draft-declaration` for supporting
  papers

## Acceptance criteria

### Caption + format

- [ ] Correct King County District Court caption
- [ ] Cause number format
- [ ] GR 14 formatting (margins, font, line spacing)
- [ ] Pro se signature block

### Answer

- [ ] Computes the response deadline using `wa-deadlines`
      (does NOT hard-code a specific day count)
- [ ] Paragraph-by-paragraph denial / admission consistent
      with CR 8 / CRLJ 8
- [ ] Pleads affirmative defenses in a numbered list:
      - Statute of limitations (RCW 4.16 — applicability turns
        on whether plaintiff has the cardholder agreement)
      - Lack of standing (CR 17(a); chain of title gap)
      - Lack of capacity to sue (RCW 19.16 licensing — *Gray
        v. Suttell*)
      - Failure to state a claim
      - Failure of consideration / Article 9 attachment
        deficiency
      - Unclean hands / FDCPA violations
      - Reservation of additional defenses pending discovery

### Counterclaims

- [ ] Pleads FDCPA counterclaim (15 U.S.C. § 1692) with
      relevant prohibition cite (false representations on
      time-barred debt + lack of standing claim, threat to
      sue without owning the account, etc.)
- [ ] Pleads WA CPA counterclaim (RCW 19.86) — invokes the
      per-se pathway via RCW 19.16
- [ ] Prayer for relief includes: actual damages; FDCPA
      statutory damages; treble CPA damages (subject to the
      statutory cap); mandatory attorney's fees; costs

### References corpus integration

- [ ] Cites RCW chapters at chapter level (e.g., "RCW 4.16"
      not "RCW 4.16.040(2) — 6 years") — current SOL day
      counts and current treble caps live in the references
      corpus

## Common failure modes

- Hard-coding the SOL period in the affirmative defense
- Hard-coding the treble cap or FDCPA statutory damages amount
- Missing the per-se CPA pathway via RCW 19.16
- Filing a general denial instead of paragraph-by-paragraph
- Forgetting to plead fees in the prayer
