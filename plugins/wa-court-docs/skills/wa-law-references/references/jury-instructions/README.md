# Washington Pattern Jury Instructions (WPI / WPIC)

- Canonical entry point (AOC): https://www.courts.wa.gov/index.cfm?fa=home.contentDisplay&location=PatternJuryInstructions
- Free public access site (Thomson/West, civil): https://govt.westlaw.com/wciji/Index
- Coverage: index + canonical pointers only — **NOT verbatim**.
- Verified: 2026-06-05

## What this corpus is — and is not

This is a **pointer-stub corpus**, not a verbatim snapshot. It indexes the
Washington Pattern Jury Instructions so an agent knows *which* instruction
exists, *where* it sits in the numbering, and *how to reach the authoritative
text* — but it does **not** reproduce the instruction text, Notes on Use, or
Comments.

This is deliberate. Every other Washington corpus in this plugin
(`court-rules/`, `wa-rcw-debt/`) is snapshotted **verbatim** because the
underlying content is a **public-domain government edict** — statutes and
court rules are not copyrightable. The Pattern Jury Instructions are
**different**:

- The **WPI** (Civil) and **WPIC** (Criminal) are drafted by the Washington
  Supreme Court Committee on Jury Instructions but are **published and
  copyrighted by Thomson Reuters/West** (Washington Practice series, vols. 6 /
  6A civil; 11 / 11A criminal).
- They are made available to the public for free **by agreement** between the
  WPI Committee and Thomson/West — a *public-access* arrangement, **not** a
  public-domain dedication. The terms permit use "in the practice of law and
  legal research" and prohibit other use, **including commercial re-use** and
  redistribution.
- The host (`govt.westlaw.com`) is bot-gated specifically to prevent bulk
  extraction.

Mirroring the instruction text verbatim into this repo would therefore be a
copyright infringement and a terms-of-use violation. So this corpus follows
the same "publish what we can lawfully verify + honest pointer stubs for the
rest" discipline the plugin already uses for paywalled/copyrighted sources
(the Colorado annotated rule sets, the New York Tanbook, the EOIR practice
manuals).

> **NOT LEGAL ADVICE.** This index is a drafting/navigation aid. Pattern
> instructions are starting points, not law — they must be tailored to the
> evidence and the current statute/case law, and a proposed instruction is
> only as good as the authority behind it. Always open the live instruction
> (with its Notes on Use and Comment) and verify it is current before
> proposing it to a court.

## Files

| File | Set | Scope |
|---|---|---|
| [WPI-civil.md](WPI-civil.md) | WPI | Washington Pattern Jury Instructions — **Civil** (Wash. Prac. vols. 6 / 6A). Topic-number index + canonical pointers. |
| [WPIC-criminal.md](WPIC-criminal.md) | WPIC | Washington Pattern Jury Instructions — **Criminal** (Wash. Prac. vols. 11 / 11A). Part I–XVI index + canonical pointers. |
| `_manifest.json` | — | Machine-readable index (sets, access posture, canonical URLs). |

The plugin is civil-focused, so **WPI (Civil) is the primary deliverable**;
WPIC (Criminal) is indexed as a companion pointer.

## How to access the authoritative text

1. Start at the **AOC landing page** (the stable, rot-resistant entry point):
   https://www.courts.wa.gov/index.cfm?fa=home.contentDisplay&location=PatternJuryInstructions
2. Follow its link to the Thomson/West free-access site. The civil set is at
   `govt.westlaw.com/wciji`; the criminal set has its own database — reach it
   from the AOC landing page rather than guessing the slug (the Westlaw
   database paths change; the AOC page is the authoritative jumping-off point).
3. Navigate the site's table of contents to the instruction number. The free
   site has **no search** — browse by chapter/part.
4. Questions on the instructions themselves go to `JuryInstructions@courts.wa.gov`.

## Citation

Cite a pattern instruction by set, number, and edition, e.g.:

> 6 Wash. Prac., Washington Pattern Jury Instructions: Civil [WPI] 10.01 (7th ed.)

In a filing, an instruction is usually proposed as "Plaintiff's Proposed
Instruction No. __ (WPI 10.01)". See `../citation-format.md` for general
Washington citation form and GR 14 compliance.

## Refreshing

There is **no `pull_*.py` script** for this corpus, by design — the content is
copyrighted and the host bars scraping, so there is nothing to mirror
verbatim. "Refreshing" means:

1. Re-verify the AOC landing page and the civil free-access URL still resolve.
2. Re-check the part/chapter structure below against the live table of contents
   (the Committee revises and renumbers instructions periodically).
3. Update the `Verified:` date here and in `_manifest.json`, and note any
   structural change.

When the structure changes materially, bump the `wa-law-references` SKILL.md
`version:` (PATCH for a date/verify refresh; MINOR if part/chapter coverage
changes).
