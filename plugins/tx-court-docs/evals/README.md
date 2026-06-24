# Evals — Skill Regression Tests (Texas)

Prompt-based regression tests for the `tx-court-docs` plugin, across
five categories.

> **NOT LEGAL ADVICE.** These evals exercise drafting and procedural
> scaffolding, not legal advice.

## Folder layout

- `drafting/` — drafting-skill evals (motion / summary judgment, unsworn declaration, notice of hearing, proposed order)
- `formatting/` — format and venue-caption evals (statewide format, Smith County JP caption, pro se, quality check)
- `procedural/` — matter-neutral civil-procedure evals (law-references, deadlines, discovery, first-30-days, fact-check, file-packet)
- `subject-matter/` — subject-bundle evals (time-barred debt SOL, debt-buyer chain of title, TDCA/DTPA tie-in, community-property division)
- `integration/` — end-to-end multi-skill evals (debt-defense answer, divorce intake)

## Thin-skill acceptance criteria

User-stated hypothetical facts in eval prompts are fine (e.g. "served
on April 15", "I make $4,000/month"), and deterministic math derived
from them is fine. Acceptance criteria must NOT hard-code drift-prone
current-law values (justice-court jurisdictional ceiling, homestead
acreage, personal-property exemption cap, net-resources cap, expedited-
action ceiling, the $10,000 bond figure). Where a figure matters, the
criterion requires the agent to **read the current value from the
references corpus** (`../tx-law-references/references/`), not recite it
from memory.

## Texas-specific things these evals guard

- **The "Monday rule"** district/county-court answer deadline — answer
  due by 10:00 a.m. on the Monday next after the expiration of 20 days
  from service (TRCP 99), NOT a flat 20-day count.
- **Justice-court 14-day answer** (TRCP 502.5) and the rule that the
  rules of civil procedure and of evidence largely do **not** apply in
  Justice Court except where TRCP Part V (500–510) incorporates them
  (TRCP 500.3(e)).
- **No-evidence summary judgment** (TRCP 166a(i)) alongside traditional
  166a(c); 21-day notice / 7-day response window.
- **Discovery Levels 1/2/3** (TRCP 190) + expedited actions (TRCP 169);
  25-interrogatory cap (TRCP 190.3); 30-day response window.
- **Sworn account** (TRCP 185) and the mandatory **verified denial**
  (TRCP 93) needed to put a sworn account in issue.
- **Rule 47(c)** mandatory statement of the range of relief.
- **CPRC § 132.001 unsworn declaration** as a substitute for an
  affidavit, with the statutory penalty-of-perjury jurat.
- **4-year debt SOL** (CPRC § 16.004) and the no-revival-by-payment
  rule for time-barred consumer debt (Fin. Code § 392.307).
- **TDCA → DTPA tie-in** (Fin. Code § 392.404) and the **60-day
  pre-suit notice** (Bus. & Com. Code § 17.505).
- **§ 392.101 surety-bond** requirement (a bond, not a license — Texas
  has no debt-collector licensing regime).
- **Community property** "just and right" division (Fam. Code Ch. 7),
  residency (§ 6.301) and the 60-day waiting period (§ 6.702).
- **Two courts of last resort** (Supreme Court of Texas + Court of
  Criminal Appeals); S.W.3d citation with the court-of-appeals district
  and the petition-history parenthetical.
- **Tex. Gov't Code § 662.003** holidays (Juneteenth + Friday after
  Thanksgiving close the courts; Confederate Heroes Day / Texas
  Independence Day / San Jacinto Day / LBJ Day are partial-staffing
  only and do NOT close the courts).
