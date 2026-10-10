# ny-fact-check — Tanbook citation conventions

## Prompt

Check this citation for me: *Smith v. Jones*, 100 NY2d 543
(2003). Is the format right for a NY Supreme Court filing?

## Expected triggers

- `ny-fact-check`
- `ny-law-references`

## Acceptance criteria

- [ ] Identifies the **NY Law Reports Style Manual
      ("Tanbook")** as the authoritative source for NY
      citation format in court papers
- [ ] Correct format: *Smith v Jones*, 100 NY2d 543 (2003)
      — note the **lack of period after `v`** (Tanbook
      convention; differs from Bluebook)
- [ ] Correct format: **`NY2d`** for Court of Appeals
      reports; **`AD3d`** for Appellate Division reports;
      **`Misc 3d`** for unofficial reports
- [ ] Period and spacing follow Tanbook
- [ ] Notes the alternative format for NY County / Sup Ct
      cases (e.g., "Sup Ct, NY County")
- [ ] References the Tanbook PDF at the Reporter of
      Decisions' site

## Common failure modes

- Cites Bluebook format with periods after "v." and "N.Y.2d"
- Misses the Tanbook's no-period convention
- Adds incorrect parenthetical
