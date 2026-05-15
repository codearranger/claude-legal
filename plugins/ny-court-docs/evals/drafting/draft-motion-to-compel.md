# ny-draft-motion — Motion to Compel scaffold (CPLR 3124)

## Prompt

Draft a motion to compel for my New York case. The plaintiff
(Midland Credit Management, Inc.) served boilerplate
objections to my CPLR 3120 document requests asking for the
chain of title on the assigned debt. The case is in NY County
Supreme Court, Index No. 654321/2025, IAS Part 38. I am pro
se.

## Expected triggers

- `ny-draft-motion`
- `ny-statewide-format`
- `ny-nyco`
- `ny-discovery`
- `ny-pro-se`
- `ny-consumer-debt`

## Acceptance criteria

### Caption

- [ ] "SUPREME COURT OF THE STATE OF NEW YORK" at top
- [ ] "COUNTY OF NEW YORK" below
- [ ] Two-block caption with `-against-` party separator
      (not `v.` or `versus`)
- [ ] Index No. 654321/2025 in the upper-right block
- [ ] IAS Part 38 referenced
- [ ] Title in ALL CAPS: "NOTICE OF MOTION TO COMPEL
      DISCOVERY" + "AFFIRMATION IN SUPPORT"

### Notice of Motion (CPLR 2214)

- [ ] Returnable date specified
- [ ] Relief sought: order compelling responses + costs
- [ ] Statutory grounds: CPLR 3124 (motion to compel) +
      CPLR 3126 (sanctions for nondisclosure)
- [ ] Time of service complies with CPLR 2214(b) — 8 days
      minimum (16 if served by mail, per CPLR 2103(b)(2)'s
      5-day mail rule plus the rest)

### Good-faith certification

- [ ] 22 NYCRR § 202.20-f conferral affirmation present
- [ ] Recites specific dates of meet-and-confer
      correspondence
- [ ] States affirmative effort to resolve before motion

### Affirmation in Support

- [ ] CPLR 2106 affirmation form (the 2023 universal
      affirmation, available to non-attorneys after the
      2023 amendments — NOT the old attorney-only rule)
- [ ] Numbered paragraphs
- [ ] "Material and necessary" disclosure scope cited
      (CPLR 3101(a) + *Allen v. Crowell-Collier Pub. Co.*,
      21 N.Y.2d 403 (1968))

### Composition

- [ ] References pro se status without overclaiming /
      lawyer-speak

## Common failure modes

- Defaults to FRCP (Rule 37) instead of CPLR 3124
- Uses `v.` instead of `-against-`
- Wrong return-date math (forgets the 5-day mail rule)
- Cites the pre-2023 CPLR 2106 (which limited affirmations to
  attorneys) instead of the post-2023 universal version
- Forgets the 22 NYCRR § 202.20-f conferral requirement
