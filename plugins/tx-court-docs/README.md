# tx-court-docs — Texas

Draft and format pleadings, motions, affidavits and unsworn declarations, notices of hearing, and proposed orders for Texas courts.

> **NOT LEGAL ADVICE.** Output is a drafting aid; verify every rule, deadline, and citation against current law before filing.

## What it covers

Texas has **no single statewide pleading-paper rule** for the trial courts — the form of a filing flows from the **Texas Rules of Civil Procedure** (TRCP **45** form of pleadings, **47** claims for relief incl. the **Rule 47(c)** statement of the range of relief sought, **57** signing with the State Bar of Texas number, **78a** civil case information sheet) and the Supreme Court's e-filing technology standards (Tex. R. Jud. Admin. 10). Documents file through **eFileTexas.gov** (Tyler Odyssey *File & Serve*) under **TRCP 21(f)** — mandatory for attorneys, available to self-represented filers. The plugin ships the marketplace's clean, court-safe formatting baseline (Letter paper, ≥ 1″ margins, ≥ 12-pt font, 1.5×+ spacing, line-numbered pleading paper **on by default**, and a continuous *Page X of Y* footer).

Texas trial courts: **District Courts** (general jurisdiction — civil, family/SAPCR, title to land), **County Courts at Law** and **Constitutional County Courts** (mid-tier civil, probate, de novo appeals from JP courts), and **Justice of the Peace (Justice) Courts** (small-claims/debt-claim and eviction under **TRCP Part V, Rules 500–510**). The civil court of last resort is the **Supreme Court of Texas**; criminal appeals run to the **Court of Criminal Appeals** (Texas has *two* courts of last resort). Venue skills:

- **`tx-hcdc`** — Harris County District Courts (Houston) — the state's largest trial-court system.
- **`tx-dcdc`** — Dallas County District Courts.
- **`tx-county-courts`** — a statewide roll-up of other counties' District Courts and County Courts at Law.
- **`tx-justice-courts`** — the statewide Justice of the Peace layer (TRCP 500–510): debt-claim cases, eviction/forcible detainer, the simplified procedure (TRCP 500.3(e): the regular rules of civil procedure and evidence largely do not apply), and de novo appeal to county court.
- **`tx-smith-county-jp`** — **Smith County (Tyler) Justice Court**, layering the precinct-specific mechanics on `tx-justice-courts` and `tx-statewide-format`.
- **`tx-family-court`** — the family docket (Texas has no separate family court; divorce and SAPCR are heard in District Courts, with designated family district courts and associate judges in some counties).

Architected as matter-neutral civil-procedure skills — statewide format, discovery (Texas **allows interrogatories**, capped at 25 excluding identify-persons rogs; discovery-control-plan **Levels 1/2/3** under TRCP 190 + **expedited actions** under TRCP 169), hearings (oral hearing vs. **submission docket**), first-30-days, post-judgment, deadlines, fact-check, filing, and drafting scaffolders (motion, declaration, notice of hearing, proposed order) — plus two subject-matter bundles:

- **`tx-consumer-debt`** — FDCPA / Regulation F / FCRA overlay, the **Texas Debt Collection Act** (Tex. Fin. Code Ch. 392 — incl. the **§ 392.101 $10,000 Secretary-of-State surety-bond** requirement and the **§ 392.404 DTPA tie-in**), the **DTPA** (Tex. Bus. & Com. Code Ch. 17), the **4-year** debt limitations defense (Tex. Civ. Prac. & Rem. Code § 16.004) with the no-revival-by-payment rule (Fin. Code § 392.307), the **sworn-account** (TRCP 185) verified-denial trap, chain of title, and the **TRE 803(6) / 902(10)** debt-buyer evidence foundation.
- **`tx-family-law`** + **`tx-family-court`** — **community-property** "just and right" division (Tex. Fam. Code Ch. 7), the percentage-of-obligor-net-resources **child-support guidelines** (Ch. 154), conservatorship and the Standard Possession Order (Ch. 153), spousal maintenance (Ch. 8), **informal/common-law marriage** (§ 2.401), SAPCR, UCCJEA (Ch. 152) / UIFSA (Ch. 159), and Title 4 protective orders.

**25 skills total** (the 21-skill civil-practice core + family court/law + the Justice-Court and Smith County JP venue skills).

### Procedural quirks worth flagging

- **The "Monday rule" answer deadline** — a district/county-court answer is due "by 10:00 a.m. on the Monday next after the expiration of twenty days after the date of service" (TRCP 99(b)); `case-calendar.py --rule answer-due` computes it. A **justice-court** answer is due by the **end of the 14th day** after service (TRCP 502.5).
- **No-evidence summary judgment** (TRCP 166a(i)) alongside the traditional motion (166a(c)).
- **Sworn account** (TRCP 185) is prima facie proof unless met by a **verified denial** (TRCP 93(10)) — a common pro-se trap in collection suits.
- **Special exceptions** (TRCP 91) and **Rule 91a** dismissal — there is **no general demurrer** in Texas.
- **Rule 47(c)** requires the petition to plead a range-of-relief statement.
- Discovery is governed by a **control plan** (Level 1 / 2 / 3, TRCP 190) and the **expedited-actions** track for claims at or below the statutory ceiling (TRCP 169).
- **Justice Court** procedure is simplified — the rules of civil procedure and evidence largely **do not apply** (TRCP 500.3(e)); appeals go **de novo** to county court.
- **Wages are generally exempt from garnishment** for ordinary consumer debt (Tex. Const. art. XVI § 28); enforcement runs through bank-account garnishment and **turnover** (CPRC § 31.002). Texas's **homestead** and personal-property **exemptions** (Tex. Prop. Code Ch. 41 / 42) are among the most generous in the country.
- **Tex. Gov't Code § 662.003 holidays** — Juneteenth and the Friday after Thanksgiving are court-closed days; the state-only "partial-staffing" holidays (Confederate Heroes Day, Texas Independence Day, San Jacinto Day, LBJ Day) are not.
- **Community-property** state; family matters are heard in the District Courts under the TRCP (no separate family-procedure rule set).

## Reference corpora

Under `skills/tx-law-references/references/` (each corpus dir has its own README):

- `court-rules/` — Texas Rules of Civil Procedure (incl. the Part V justice-court rules), Tex. R. Evid., and Tex. R. App. P. targets, fetched by `scripts/pull_texas_rules.py` from txcourts.gov.
- `tx-statutes-debt/` — Texas statute text for the codes most relevant to civil + family practice (Civil Practice & Remedies Code limitations/fees/judgments/proportionate-responsibility, Finance Code Ch. 392 debt collection, Business & Commerce Code DTPA + UCC Article 9, Property Code exemptions/eviction, Family Code, and the Government Code holiday/jurisdiction sections), fetched by `scripts/pull_texas_statutes.py` from statutes.capitol.texas.gov.
- `federal-debt-laws/`, `federal-bankruptcy/`, `ucc-model/` — **symlinks** into the shared `claude-legal-federal-laws` plugin (declared as a dependency; dereferenced at install time).

## Scripts

- `scripts/format-check.py` — validates a generated `.docx` against the marketplace formatting baseline (Letter paper, ≥ 1″ margins, ≥ 12-pt font, 1.5×+ spacing, black ink, footer pagination).
- `scripts/case-calendar.py` — Tex. R. Civ. P. 4 deadline arithmetic with Tex. Gov't Code § 662.003 holidays and named rules, including the special **Monday-rule** answer computation. Run `case-calendar.py --rules` to list them.

## Dependencies

- `claude-legal-federal-laws` — shared federal / UCC / Bankruptcy corpora (symlinked into `references/`).
- `document-skills` (from the `anthropic-agent-skills` marketplace) — DOCX / PDF / PPTX / XLSX output.

---
Part of the [claude-legal](../../README.md) marketplace. Skills are indexed in [CLAUDE.md](../../CLAUDE.md).
