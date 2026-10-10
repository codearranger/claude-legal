# ga-first-30-days — 30-day answer + State Court forum + § 9-11-13 counterclaim

## Prompt

I just got served with a debt-collection lawsuit in Georgia. The papers
say "State Court of Fulton County." I think the collector also violated
the law harassing me. What are my options in the first month — how long
do I have to answer, where is this case, and can I sue them back in the
same case?

## Expected triggers

- `ga-first-30-days`
- `ga-deadlines`
- `ga-statewide-format`

## Acceptance criteria

### Forum (the Georgia State / Superior / Magistrate split)

- [ ] Confirms that routine debt-collection suits are properly filed in
      **State Court** — a court of limited jurisdiction with **no dollar
      ceiling** that hears civil actions of any amount except the
      superior-court-exclusive subjects (divorce, equity, title to land,
      felonies) — so a State Court of Fulton County debt case is in the
      right forum; explains the split is by **subject matter, not dollar
      amount**
- [ ] Notes the alternative venues: **Magistrate Court** for claims within
      its statutory civil cap (read the **O.C.G.A. § 15-10-2(5)** cap from
      the corpus rather than asserting the dollar figure) and **Superior
      Court** for the exclusive subjects

### Answer deadline and triage

- [ ] States the **30-day answer window** under **O.C.G.A. § 9-11-12(a)**
      (reading the count and service variants from the corpus via
      `ga-deadlines`) and the **15-day open-default** window under
      **O.C.G.A. § 9-11-55(a)**
- [ ] Identifies the **§ 9-11-12(b)(6)** motion to dismiss for failure to
      state a claim as a pre-answer option and its effect on the deadline
- [ ] States that **affirmative defenses** (statute of limitations,
      payment, lack of standing) must be raised in the answer or risk
      waiver

### Counterclaims (O.C.G.A. § 9-11-13)

- [ ] Explains that a claim arising out of the same transaction (e.g., an
      FDCPA / FBPA collection-abuse claim) is a **compulsory counterclaim**
      under **O.C.G.A. § 9-11-13(a)** and must be pleaded in the answer or
      it is lost; permissive counterclaims fall under § 9-11-13(b) — reads
      the rule from the corpus

## Common failure modes

- Says the case is "in the wrong court" because State Court is not
  Superior Court (misses the subject-matter, not-dollar split)
- Asserts a magistrate civil cap dollar figure from memory instead of the
  § 15-10-2(5) corpus value
- States a 20-day answer window instead of Georgia's 30 days
- Misses that the collection-abuse claim is a compulsory counterclaim
  under § 9-11-13(a)
