---
name: wa-deadlines
description: >
  Use this skill whenever the user asks about timing or deadlines in
  a Washington civil case. Triggers include "when is my answer due",
  "when is the response brief due", "compute the deadline", "how many
  court days", "what's the reply deadline", "I was served — when do I
  have to answer", "when does my discovery response have to go out",
  "how long do I have to file a motion to vacate", "exemption claim
  deadline", "FDCPA statute of limitations", "is this deadline past".
  Computes court-day and calendar-day deadlines under CR 6 / CRLJ 6
  using RCW 1.16.050 holidays (with Saturday→Friday / Sunday→Monday
  observed-day rule), and covers FDCPA SOL, garnishment timing (RCW
  6.27), post-judgment (CR 59, CR 60, RAP 5.2), and WA debt SOL.
  Deterministic date arithmetic is delegated to
  `scripts/case-calendar.py`.
version: 0.1.0
---

# Washington Case Deadlines

Compute and track deadlines for Washington civil cases. The agent
should invoke this skill automatically when the user asks a timing
question, without requiring an explicit command.

## How to answer a deadline question

1. **Identify the triggering event.** What happened? (e.g., "I was
   served on April 1", "the judge signed the order on March 15", "the
   garnishment writ was mailed yesterday").

2. **Identify the rule.** Match the event to the deadline reference
   chart below. Name the rule (CR 12(a), CRLJ 6(d), RCW 6.27, etc.)
   so the user knows what governs.

3. **Compute the date** using the Python helper — it handles WA state
   holidays (RCW 1.16.050) and the Saturday→Friday / Sunday→Monday
   observed-day shift:

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/case-calendar.py" \
     --from 2026-06-03 \
     --days -3 \
     --mode court
   ```

   Flags:
   - `--from YYYY-MM-DD` — triggering date
   - `--days N` — offset (negative = before; positive = after)
   - `--mode court|calendar` — court-day counting (skips weekends +
     WA state holidays) or calendar-day counting

4. **Report clearly.** Give the date, the day of the week, whether
   any intervening holiday pushed the count, and the rule citation.

## Optional — maintain a per-case calendar

If the user wants a tracked calendar for the case, store it at
`[case-folder]/CASE_CALENDAR.md` with this shape:

```markdown
# Case Calendar — [Case Name], Cause No. [number]

Court: [court]
Judge: [if known]
Defendant: [pro se]

## Events
- 2025-01-15: Summons served on Defendant
- 2025-02-14: Answer due (CR 12(a) — 20 days from service)
- 2025-03-01: First Discovery Request served
- 2025-03-31: Discovery responses due (CR 33/34 — 30 days)

## Completed
- [x] 2025-02-14: Answer filed

## Notes
[running notes]
```

When the user adds a new event, append to `## Events`, compute any
derived deadlines, and add those too.

## Court-day vs. calendar-day counting (CR 6(a))

- **Calendar days** — every day, including weekends and holidays
- **Court days** — excludes Saturdays, Sundays, and WA state legal
  holidays
- CR 6(a): periods of fewer than 7 days typically count court days;
  longer periods typically count calendar days (but always verify
  the specific rule — there are exceptions)

## Deadline reference chart

### Pleadings and service

| Event | Deadline | Authority |
|-------|----------|-----------|
| Summons served | — | — |
| Answer due (pro se defendant, WA resident) | 20 calendar days from service | CR 12(a)(1) |
| Answer due (non-resident defendant) | 60 calendar days from service | CR 12(a)(1) |
| Reply to counterclaim | 20 calendar days from service | CR 12(a)(3) |
| Response to amended complaint | 14 calendar days from service | CR 15(a) |

### Discovery

| Event | Deadline | Authority |
|-------|----------|-----------|
| Response to RFPs / IROGs / RFAs | 30 calendar days from service | CR 33, 34, 36 |
| + 3 days if served by mail | 33 calendar days | CR 6(e) |
| RFA objection deadline | 30 calendar days — silence = admission | CR 36(a) |
| Motion to compel | After CR 26(i) conference | CR 37(a) |

### Motion practice — superior court (CR 56 / CR 6)

| Event | Deadline | Authority |
|-------|----------|-----------|
| Note for motion docket | Set at least 9 court days out | CR 6(d) |
| Response to motion | 11 court days before hearing | CR 6(d) |
| Reply | 5 court days before hearing | CR 6(d) |
| Summary judgment motion | Filed 28 calendar days before hearing | CR 56(c) |
| SJ response | Filed 11 court days before hearing | CR 56(c) |
| SJ reply | Filed 5 court days before hearing | CR 56(c) |

### Motion practice — district court (CRLJ 6)

| Event | Deadline | Authority |
|-------|----------|-----------|
| Response to motion | 3 court days before hearing | CRLJ 6(d) |

### Post-trial / post-judgment

| Event | Deadline | Authority |
|-------|----------|-----------|
| Motion for reconsideration | 10 calendar days from entry | CR 59(b) |
| Motion to vacate — CR 60(b)(1)-(3) | 1 year from entry | CR 60(b) |
| Motion to vacate — CR 60(b)(5) | Reasonable time | CR 60(b) |
| Notice of Appeal (superior → Court of Appeals) | 30 calendar days from final order | RAP 5.2 |
| Notice of Appeal (district → superior, RALJ) | 30 calendar days | RALJ 2.5 |

### Garnishment / execution

| Event | Deadline | Authority |
|-------|----------|-----------|
| Exemption Claim Form | 21 days from mailing OR 28 days from service — whichever is later | RCW 6.27 |
| Garnishee's answer | 20 calendar days from service | RCW 6.27.190 |
| Writ of continuing wage lien — duration | 60 calendar days | RCW 6.27 |

### FDCPA

| Event | Deadline | Authority |
|-------|----------|-----------|
| Consumer dispute of debt | 30 calendar days from validation notice | 15 U.S.C. § 1692g |
| FDCPA civil claim — statute of limitations | 1 year from violation | 15 U.S.C. § 1692k(d); *Rotkiske* |

### Satisfaction of judgment

| Event | Deadline | Authority |
|-------|----------|-----------|
| Creditor files satisfaction | 60 calendar days from payment | RCW 4.56.100 |
| Demand letter to non-filing creditor | Recommended 14 days | — |

### Washington state statutes of limitations (consumer debt)

| Type | Period | Authority |
|------|--------|-----------|
| Written contract (most credit card) | 6 years | RCW 4.16.040; *Discover Bank v. Bridges* |
| Oral contract | 3 years | RCW 4.16.080(3) |
| Account stated | 3 years | RCW 4.16.080(3) |

## Common triggering events — auto-derive deadlines

When the user reports one of these, compute the derived deadlines
proactively:

- **"I was served with a summons"** → Answer due (20 days), research
  deadline (14 days recommended)
- **"I got a writ of garnishment"** → Exemption Claim deadline (21/28
  days)
- **"The judge ruled against me"** → CR 59 (10 days) and RAP 5.2 (30
  days) deadlines
- **"Plaintiff served discovery"** → response due (30 + 3 if by mail)
- **"I filed a motion to compel"** → opposing response (3 court days
  before hearing in district court; 11 in superior), reply (5 court
  days before, superior only)
- **"The creditor sent me a validation notice"** → 30-day dispute
  deadline

## Washington state legal holidays (RCW 1.16.050)

The helper script observes these. Saturday holidays shift to the
preceding Friday; Sunday holidays shift to the following Monday.

| Holiday | Date |
|---------|------|
| New Year's Day | January 1 |
| Martin Luther King Jr. Day | 3rd Monday of January |
| Presidents' Day | 3rd Monday of February |
| Memorial Day | Last Monday of May |
| Juneteenth | June 19 |
| Independence Day | July 4 |
| Labor Day | 1st Monday of September |
| Veterans Day | November 11 |
| Thanksgiving Day | 4th Thursday of November |
| Native American Heritage Day | Friday after Thanksgiving |
| Christmas Day | December 25 |

**Federal court divergence**: Federal courts do **not** treat Native
American Heritage Day (the day after Thanksgiving) as a holiday. If
the matter is in federal court, check the local federal court
calendar rather than this WA state list.

**Court closures not on this list** — each division / chambers may
declare additional closures (inclement weather, administrative
days). The helper script does not know about these; check the
court's website for anything near a declared closure.

## Output format (example)

```
Case: Velocity Investments LLC v. Doe
Today: 2026-04-23

UPCOMING DEADLINES:

🔴 Overdue:
   (none)

🟡 Within 7 days:
   - 2026-04-28 (5 days): Response to Motion to Compel — CRLJ 6(d)

🟢 Later:
   - 2026-05-29 (36 days): Reply brief — 3 court days before hearing
   - 2026-06-03 (41 days): Hearing on Motion to Compel
```

## Notes

- **Extensions** — CR 6(b) allows extensions for cause; stipulations
  of counsel are common. Update the calendar when granted.
- **Mail service adds 3 days** per CR 6(e) — apply when the method of
  service is by mail
- **Do not rely solely on this skill** — verify each deadline against
  the current rule text and the court's calendar for holidays and
  adjustments. For KCDC motion days, pull the rolling motions
  calendar from:
  https://kingcounty.gov/en/court/district-court/courts-jails-legal-system/civil-filings
