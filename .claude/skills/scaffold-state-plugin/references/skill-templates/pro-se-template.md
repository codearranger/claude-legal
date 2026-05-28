---
name: {{ABBR}}-pro-se
description: >
  This skill should be used when drafting {{STATE_NAME}} court
  documents for a self-represented (pro se) litigant.
  Triggers include "pro se", "self-represented",
  "I'm representing myself", "pro-se drafting framework", "draft
  without an attorney". Covers the pro-se drafting framework
  adapted to {{STATE_NAME}} procedural
  conventions and the practical service and filing protocols
  pro se filers need. Layer on top of
  {{ABBR}}-statewide-format and (if applicable) the relevant
  court skill.
version: 0.1.0
---

# Pro Se Drafting for {{STATE_NAME}} Courts

Use this skill when drafting court documents for a pro se
litigant in a {{STATE_NAME}} court. It encodes the pro-se
drafting framework adapted to {{STATE_NAME}} procedural
conventions.

> **NOT LEGAL ADVICE.** This skill is a drafting aid for
> self-represented litigants, not legal advice and not a
> substitute for counsel. For complex matters, or matters
> with substantial sums at stake, consider consulting a
> licensed {{STATE_NAME}} attorney. Verify every rule,
> deadline, and citation against current law before filing.

## The pro-se drafting framework

Every motion and declaration follows four principles:

1. **Front-load the strongest facts.** The judge should know
   the best fact in the case within the first paragraph.
2. **Keep motions concise.** Target 4–6 pages for a motion +
   memorandum. Use bold lead-ins.
3. **Write to the judge, not to opposing counsel.** Avoid
   ad hominem.
4. **Let the record speak.** Attach the documents that prove
   the point and cite them.

## Signature block for pro se ({{STATE_NAME}})

```
____________________________________
[Full Name]
{{PRO_SE_DESIGNATION}}
[Street Address]
[City, {{STATE_NAME}} ZIP]
[Phone]
[Email]
```

> **TODO**: Identify the state's pro se signature-block
> conventions:
> - State's term: "pro se" / "in pro per" (CA) / etc.
> - Bar number convention: most states omit for pro se
> - Required fields: address, phone, email

## Service protocol — {{STATE_NAME}}

### Initial summons and complaint

> **TODO**: Document the state's initial-process service
> rule (state's FRCP 4 analog).

### Subsequent filings

> **TODO**: Document the state's analog to FRCP 5 / ORCP 9
> for serving filings after the complaint.

### Service best practices for pro se

- Photograph postmarked envelopes
- Memorialize phone calls in writing immediately
- Keep a complete filing log
- Use certified mail for disputed-receipt situations
- Include a Certificate of Service with every filing

## Common pro se pitfalls — {{STATE_NAME}}-specific

| Pitfall | Fix |
|---------|-----|
| Overlong motions | Cap at 6 pages; move narrative to declarations |
| Emotional tone | Rewrite as neutral fact statements |
| Missing relief clause | Every motion ends with "RELIEF REQUESTED" |
| Citing exhibits without attaching | Always attach and index |
| Forgetting perjury clause | Every declaration needs one |
| Colored / highlighted text | Violates {{FORMAT_RULE}} typically |
| Missing scheduling document | Most {{STATE_NAME}} courts require one |
| Ambiguous signature block | Name, role, address, phone, email |

> **TODO**: Identify state-specific pitfalls:
> - State terminology (e.g., "notice of motion" vs. "notice
>   of hearing" vs. "note for motion docket")
> - State exhibit convention (numbered vs. lettered)
> - State citation conventions (periods vs. no periods)
> - State-specific procedural quirks (no interrogatories
>   in OR; "in pro per" in CA; etc.)

## Drafting checklist (run before filing)

- [ ] Caption is complete and matches the case number
- [ ] Court header is correct ({{STATE_NAME}}-specific)
- [ ] Parties separator is correct (state convention)
- [ ] First paragraph states the strongest fact
- [ ] Every factual assertion supported by exhibit or
      sworn statement
- [ ] Motion ≤ 6 pages
- [ ] Relief requested spelled out at the end
- [ ] Perjury clause on all declarations (state form)
- [ ] Signature block correct (pro se conventions)
- [ ] Footer pagination correct
- [ ] {{FORMAT_RULE}} compliant
- [ ] Certificate of Service attached
- [ ] All exhibits listed, cover-paged, referenced

## {{STATE_NAME}}-specific pro se resources

### Statewide

> **TODO**: Identify the state's pro-se resources:
> - State judicial branch self-help page
> - Statewide forms repository
> - State legal-aid organizations

### Legal aid

> **TODO**: List income-eligible legal-aid organizations,
> hotline numbers, modest-means panels.

## Companion skills

- Use `{{ABBR}}-statewide-format` for templates and
  formatting
- If in {{PRIMARY_COURT_NAME}}, use
  `{{ABBR}}-{{PRIMARY_COURT_SLUG}}`
- If in {{SECONDARY_COURT_NAME}}, use
  `{{ABBR}}-{{SECONDARY_COURT_SLUG}}`
- Otherwise use `{{ABBR}}-county-courts`

## References

- `references/pro-se-drafting-framework.md` — full drafting guide
- `references/service-protocol.md` — service templates
- `references/pro-se-toolkit.md` — common motion types
