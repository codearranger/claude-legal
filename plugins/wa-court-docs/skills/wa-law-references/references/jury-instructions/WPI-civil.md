# WPI — Washington Pattern Jury Instructions: Civil

- Set: **WPI** (Civil)
- Published as: 6 & 6A Wash. Prac., Washington Pattern Jury Instructions: Civil (7th ed.)
- Drafted by: Washington Supreme Court Committee on Jury Instructions
- Copyright: Thomson Reuters/West (free public access by agreement — see README)
- Canonical entry point: https://www.courts.wa.gov/index.cfm?fa=home.contentDisplay&location=PatternJuryInstructions
- Free public access (civil): https://govt.westlaw.com/wciji/Index
- Verified: 2026-06-05

> **POINTER STUB — NOT VERBATIM.** This file indexes the WPI numbering and
> topical structure so an agent can locate the right instruction. It does
> **not** reproduce instruction text, Notes on Use, or Comments (those are
> copyrighted). Open the live instruction via the entry point above and
> verify it is current before proposing it. **NOT LEGAL ADVICE.**

## How WPI is organized

WPI uses a **topic-number** scheme: each instruction is `WPI <chapter>.<n>`
(e.g., `WPI 10.01`). Instructions are grouped into topical chapters that run
roughly from general/introductory matters, through liability and specific
causes of action, to damages and concluding instructions and verdict forms.
The numbering below is the **stable topical backbone**; the Committee adds,
renumbers, and reserves individual instruction numbers between editions, so
treat any specific `WPI x.yy` as a lead to verify on the live TOC, not as a
guaranteed-current citation.

## Topical chapter index

The chapters fall into these functional groups. Browse the live TOC for the
exact instruction numbers within each.

### Preliminary, general, and trial-conduct instructions
- Introductory / preliminary instructions to the jury; province of judge and
  jury; conduct of the trial; cautionary instructions.
- General definitions and concepts used across civil cases.
- Burden of proof and the meaning of "proof" / "preponderance of the
  evidence" (the `WPI 21.xx` burden-of-proof family).
- Evidence: direct/circumstantial, credibility of witnesses, expert testimony,
  number of witnesses.

### Negligence — duty, breach, causation (the core liability chapters)
- General negligence: the duty of ordinary care, the reasonably careful
  person, negligence and the standard of care (the `WPI 10.xx` family).
- Proximate cause (the `WPI 15.xx` family); concurring cause; intervening
  cause.
- Specific negligence contexts: negligence per se / violation of statute;
  res ipsa loquitur.

### Defenses and apportionment
- Contributory/comparative fault and its effect (Washington is a **pure
  comparative fault** state, RCW 4.22.005); apportionment among entities;
  the special-verdict apportionment framework.
- Assumption of risk; failure to mitigate; the empty-chair / nonparty-at-fault
  framework under RCW 4.22.

### Specific causes of action and contexts
- Motor-vehicle / "rules of the road" instructions.
- Premises liability (invitee / licensee / trespasser duties).
- Employer/employee, agency, vicarious liability, scope of employment.
- Medical negligence / informed consent (coordinate with RCW 7.70).
- Product liability under the WPLA (coordinate with RCW 7.72) — the higher
  topic-number families.
- Professional negligence; common carriers; landowner/occupier duties.

### Contract, business, and other civil-cause instructions
- Contract formation, breach, and contract damages.
- Business-tort and statutory-claim instructions (e.g., Consumer Protection
  Act elements under RCW 19.86 — coordinate with `wa-cpa`).
- Fraud / misrepresentation.

### Damages
- Personal-injury and wrongful-death/survival damages (the `WPI 30.xx`
  damages family); measure of economic and noneconomic damages; life
  expectancy; present cash value.
- Property damage; the no-speculation and no-double-recovery cautions.
- Wrongful death / survival actions (coordinate with RCW 4.20 / 4.24).

### Concluding instructions and verdict forms
- Concluding/deliberation instructions; selection of presiding juror;
  unanimity; use of verdict forms.
- General-verdict and special-verdict forms; interrogatories to the jury.

## Cross-references inside this plugin

When proposing a civil instruction, anchor it to the substantive law the
plugin already carries verbatim:

- Comparative fault / apportionment → `../wa-rcw-debt/` (RCW 4.22) and
  `wa-personal-injury`.
- Medical negligence / informed consent → RCW 7.70; product liability →
  RCW 7.72 (`wa-personal-injury`).
- Consumer Protection Act elements → `wa-cpa` / `wa-consumer-debt`
  (the *Hangman Ridge* five elements).
- Evidence foundations referenced in instructions → `../evidence-rules.md`.

## Verification

A pattern instruction is a starting point, not authority. Before it goes in a
packet: (1) open the live WPI instruction and read its **Notes on Use** and
**Comment**; (2) confirm the supporting statute/case it rests on is current
(run `wa-fact-check`); (3) tailor the bracketed material to the actual
evidence. Cite the controlling RCW or case — not the pattern instruction —
as the legal authority.
