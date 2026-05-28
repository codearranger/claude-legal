# Thin-Skill Architecture — Keep the Law in References

> **Rule**: SKILL.md bodies and eval acceptance criteria
> describe **procedural frameworks + chapter pointers**.
> Current statutory text, dollar thresholds, day counts,
> exact subsection numbers, damages multipliers, and other
> values that drift live **only in the references corpus**.
> The quarterly puller refreshes the corpus without
> requiring any SKILL.md edits.

This is the dominant lesson from the `expand-wa-civil-
practice` work: every embedded statutory specific is a
maintenance debt that a future amendment will silently
break. The skill author who embeds `"$25,000 CPA treble
cap"` in 2024 produces a SKILL.md that will be wrong if
the Legislature amends the cap in 2026 — and there's no
mechanism to surface the drift until a user or reviewer
catches it.

The fix: make the references corpus the single canonical
source of truth for everything that can drift. Skills name
the chapter, describe the framework, and point at the
chapter file. Quarterly refreshes update the chapter file;
the skill doesn't change.

## What to keep in a skill body

- **Chapter-level pointers** — "WPLA at RCW 7.72 governs
  product liability; see `references/wa-rcw-debt/RCW-7_72.md`
  for current text"
- **Qualitative framework descriptions** — "Washington is a
  pure-comparative-fault state" / "Washington is a community-
  property state" / "WBCA uses the reasonable-expectations
  test for oppression in close corporations"
- **Decision trees and procedural workflows** — "Step 1:
  identify triggering event. Step 2: identify the rule.
  Step 3: compute the deadline via the helper script.
  Step 4: report clearly."
- **Stable historical reform attributions** — "the 1986
  Reform Act", "2019 SB 5600 reformed the pay-or-vacate
  notice", "2022 consolidated civil-protection-order
  regime in RCW 7.105". The reform names + dates don't
  drift; the day counts they set DO.
- **Composition pointers** — "delegate the date arithmetic
  to `<state>-deadlines`"; "subject-matter specifics live
  in `<state>-consumer-debt`"
- **Stable case-law citations** — case names and reporters
  don't drift the way statutory text does. *Hangman Ridge*,
  *Putnam*, *Walston* are stable references; you can quote
  the framework they articulate without staleness risk.
  (Cases can be overruled; flag that as a separate
  *Shepardize before relying* discipline.)

## What to REMOVE from a skill body

If any of these appears in the SKILL.md you're authoring,
extract it to the references corpus and replace with a
chapter pointer:

- **Specific dollar thresholds** — "$116,594.96 / 2024
  salary threshold", "$25,000 treble cap", "$1,000 FDCPA
  statutory damages"
- **Specific year tags on a threshold** — "as of 2024",
  "the 2025 minimum wage of $X"
- **Specific SOL day counts** — "6 years on written
  contract", "30-day response window", "the 8-year statute
  of repose"
- **Specific employer-coverage / income thresholds** —
  "WLAD covers employers with 8+ employees" — instead, say
  "WLAD covers smaller employers than federal Title VII;
  read the current employee-count threshold from
  `RCW-49_60.md`"
- **Specific damages multipliers in body text** — "2x as
  damages for willful withholding" → reference the
  multiplier chapter file
- **Specific subsection-level cite of a cause-of-action
  element** — "RCW 7.72.060(3) provides a 3-year SOL
  from discovery" → "WPLA SOL combines a discovery rule
  with a useful-safe-life presumption; see `RCW-7_72.md`"
- **Specific notice period day counts** — "14-day
  pay-or-vacate notice", "60-day pre-suit notice"
- **Specific hearing-window day counts** — "ex parte
  followed by full hearing within 14 days"

## The same principle applies to evals

Eval acceptance criteria are not exempt. A criterion that
says `[ ] $80k is **below** the $116,594.96 threshold`
will go stale exactly when the salary threshold does.

### Eval acceptance criterion patterns

**Good** — requires the agent to read current values:

```markdown
- [ ] Identifies the **salary-threshold rule**: non-compete
      VOID below a COL-adjusted statutory threshold; the
      threshold is reset annually under RCW 49.62.020
- [ ] **Reads the current threshold from
      `wa-law-references/references/wa-rcw-debt/RCW-49_62.md`**
      (or notes the L&I-published current figure)
- [ ] Compares the $80k salary in the prompt against the
      **current** threshold and reaches the correct
      conclusion
```

**Bad** — hard-codes the law into the acceptance criterion:

```markdown
- [ ] Identifies the salary-threshold rule: non-compete
      VOID below $116,594.96/year for 2024
- [ ] $80k is below the threshold — non-compete VOID
```

The second form fails next year when the threshold is
$120k. The first form keeps working because the agent
is required to look up the live number.

### What's OK to hard-code in evals

- **The user's hypothetical prompt facts** — "I make $80,000
  a year" or "I have $50,000 in medical bills" or "My net
  monthly income is $4,200". These are scenario context for
  the framework to apply to, not law claims that drift.
- **Math that derives deterministically from prompt inputs**
  — if the prompt says income $4,200 / $7,800, the
  acceptance criterion can require "computes pro-rata shares
  of 35% / 65%" because that's deterministic math, not law.
- **Stable case-law citations** — *Hangman Ridge* 5-element
  test enumeration is fine; the case is stable.

## How to refactor an existing thick skill

The `expand-wa-civil-practice` PR refactored 9 thick WA
skills + 14 evals. The pattern that worked:

1. **Inventory the embedded specifics**. Grep for `\$[0-9]+`,
   `[0-9]+ days`, `[0-9]+ years`, `[0-9]+%`, and specific
   subsection cites like `RCW X\.Y\.Z\(`. Each hit is a
   candidate for extraction.

2. **Verify against the references corpus**. For each hit,
   confirm the value lives in the references corpus already
   (e.g., the RCW chapter file). If it does, replace with
   a pointer. If it doesn't, the corpus has a gap — add the
   chapter to the puller catalog before removing from the
   skill.

3. **Rewrite the surrounding context to a framework
   description**. Instead of `"6-year SOL on written
   contracts under RCW 4.16.040(1)"`, write `"the SOL
   framework lives in RCW 4.16; see RCW-4_16.md for
   current day counts by cause of action"`.

4. **Preserve qualitative framework descriptions**. Keep
   structural facts like "WLAD has no statutory damages
   cap" (that's a structural feature, not a number) and
   "Washington applies pure comparative fault" (that's a
   doctrinal classification, not a day count).

5. **Update the description frontmatter** to drop embedded
   specifics. The description still lists trigger phrases
   ("RCW 49.62", "WLAD", "non-compete reform") — those are
   how users phrase queries. But don't make claims like
   "no damages cap under WLAD with mandatory fees" if those
   features are statutorily set; the description should
   name the framework, not claim its current parameters.

6. **Bump the skill's `version:`** — a thin-skill refactor
   is a MINOR change (architecture shift in the body) even
   when the skill's surface contract is unchanged.

7. **Apply the same pass to the skill's evals**. Acceptance
   criteria with hard-coded values must be rewritten to
   require reading from the references corpus.

## Skill descriptions and trigger phrases

The frontmatter `description:` field needs substantive
content for the skill-invocation matcher to fire on the
right user queries. But the description can name a topic
without claiming a specific value:

**Good** — names the topic, lists trigger phrases:

```yaml
description: >
  Use when handling a Washington employment matter — the
  Minimum Wage Act + WLAD at RCW 49.60 + PFML under RCW
  Title 50A + non-compete reform at RCW 49.62 + L&I-
  exclusive workers' comp at RCW 51. Substantive framework
  lives in RCW Title 49 + Title 50A + Title 51; current
  minimum wage, damages multipliers, threshold dollar
  amounts, and SOL day counts live in the references
  corpus, not embedded here. Triggers include "Washington
  employment", "WA wage theft", "RCW 49.48", "WLAD", "RCW
  49.60", "WA Paid Sick Leave", "WA PFML", "RCW 50A",
  "WA non-compete", "RCW 49.62"...
```

**Bad** — embeds current values that drift:

```yaml
description: >
  Wage-and-hour claims under the Minimum Wage Act (RCW
  49.46) — $16.66/hour state minimum for 2025; WLAD with
  no damages cap and 8+ employee coverage; non-compete
  reform invalidating non-competes below $116,594.96/year
  for 2024 ...
```

Both invoke on the same triggers. The first survives the
2026 minimum-wage adjustment; the second goes stale.

## Citation-drift hazards by category

Common drift hazards observed in marketplace SKILL.md
authoring:

| Category | Hazard examples |
|---|---|
| Wage / employment | minimum wage figure, non-compete salary threshold, WLAD employer-count threshold, PFML premium rate, paid-sick-leave accrual rate |
| Family-law | child-support combined-income cap, modification-threshold percentage, mandatory-waiting-period days |
| L&T | pay-or-vacate notice period, deposit-return window, repair-and-deduct cap, retaliation-presumption window, just-cause grounds enumeration |
| Personal injury | SOL day counts, statute-of-repose period, notice-of-claim period, damages caps, useful-safe-life presumption |
| Consumer protection | treble-damages cap, statutory-damages amount, fee-shifting threshold |
| Procedural | answer-deadline days, motion-day timing, MAR jurisdictional cap, revision-motion window, mail-service add-on, response-to-RFA-deemed-admitted timing |
| Corporate | dissenters'-rights deadlines, derivative-action demand timing |
| UCC | statute-of-frauds dollar threshold, perfect-tender exceptions |

If your skill mentions a category, audit it for embedded
specifics from that row before committing.

## When the law genuinely can't be deferred

Some content is fundamentally definitional and won't
sensibly point at a corpus file:

- **Doctrinal classifications** — "pure comparative fault"
  vs. "modified" vs. "contributory negligence". Naming the
  classification is structural, not drift-prone.
- **Number-of-elements counts** — "Hangman Ridge 5-element
  test" or "GTE Automatic Electric three-part test". The
  count is part of the doctrine's name.
- **Major reform names + dates** — "1986 Reform Act",
  "2019 SB 5600", "2021 SB 5160", "2022 RCW 7.105
  consolidation". These are stable historical attributions.
- **Court-system shape** — "Washington has no separate
  Family Court trial court; family matters sit inside
  the general-jurisdiction Superior Court". Structural fact.

Use judgment. The test: would amending the chapter the
skill cites make the embedded statement wrong? If yes, it
goes in the references corpus. If no, it can stay in the
skill body.

## Workflow integration with the puller

The references corpus is refreshed quarterly via
`refresh-references.yml`. The state's `pull_<state>_*.py`
scripts pull verbatim text from the state's authoritative
publisher (legislature, judicial branch).

The whole point of the thin-skill architecture is that the
quarterly refresh **just works**: the puller updates the
chapter file; skills that point at the chapter file remain
correct without any SKILL.md edit.

If a skill embeds a value that the corpus also has, the two
can drift independently — which is the failure mode we're
preventing.

## Cross-state portability

The thin-skill principle also makes cross-state porting
easier. When the WA `wa-family-law` SKILL.md describes a
chapter-pointer framework ("RCW 26.09 dissolution; see
the chapter file for residency requirement and waiting
period"), porting to another state is a structured copy:

- Rename WA to NEW STATE
- Swap `RCW 26.09` for the NEW STATE's analog (e.g.,
  `Cal. Fam. Code §§ 2300-2580` for California)
- Swap `RCW-26_09.md` for `CA-Fam-Code-2300.md`
- Update the framework description for state-specific
  doctrine (e.g., California is also community-property,
  so the property-distribution framework largely carries
  over; New York is equitable-distribution, so the
  framework differs)

A thick skill with embedded specifics (`$300,000 combined-
income cap`, `93-overnight rule`) can't be ported the same
way — every embedded number requires research into the
target state's analog.
