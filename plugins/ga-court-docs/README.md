# ga-court-docs — Georgia

Draft and format pleadings, declarations, motions, notices, and proposed orders for Georgia courts.

> **NOT LEGAL ADVICE.** Output is a drafting aid; verify every rule, deadline, and citation against current law before filing.

## What it covers

Georgia has **no single statewide pleading-paper rule** — document form flows from **O.C.G.A. § 9-11-10** (caption, numbered paragraphs, separate counts), the **Uniform Superior Court Rules** / **Uniform State Court Rules** / **Uniform Magistrate Court Rules**, **§ 9-11-11** (signing) and **§ 9-11-5** (service + certificate of service), and the statewide e-filing standards (USCR 36). The plugin applies the `claude-legal` marketplace format baseline (US Letter, 1-inch margins, 12-pt serif, line-numbered pleading paper, "Page X of Y" footer) by default so every filing is clean and universally acceptable.

The plugin is architected as **matter-neutral civil-procedure skills** plus **subject-matter bundles**, all auto-invoked from natural-language triggers (no slash commands).

### Court coverage (26 skills)

**Venue skills**

- **`ga-fulton`** — Superior Court of Fulton County (Atlanta Judicial Circuit), State Court of Fulton County, and Magistrate Court; the Metro Atlanta Business Case Division; eFileGA/PeachCourt; the dedicated Family Division + per-judge standing case-management orders.
- **`ga-cobb`** — Superior Court of Cobb County (Cobb Judicial Circuit, Marietta), State Court, and Magistrate Court; **PeachCourt** e-filing; the **two** Cobb domestic standing orders (the Rule Nisi/restraint order + the USCR 24.8 co-parenting seminar order) and the traps they set for non-Cobb filers.
- **`ga-gwinnett`** — Superior Court of Gwinnett County (Gwinnett Judicial Circuit, Lawrenceville), State Court, and Magistrate Court; **Odyssey eFileGA**; the MABCD opt-in (the only county with both its State and Superior courts enrolled); mandatory ADR.
- **`ga-state-court`** — the Georgia State Court layer: civil actions of **any amount** (no dollar ceiling) + misdemeanors, but no equity/divorce/title/felony. The principal forum for consumer-debt and tort suits. Quirk: the State/Superior split is by **subject, not dollar amount**, and not every county has a State Court.
- **`ga-magistrate`** — Magistrate Court small claims (jurisdiction capped by O.C.G.A. § 15-10-2(5)), dispossessory, garnishment; informal procedure; de novo appeal to State/Superior Court.
- **`ga-county-courts`** — the rest-of-state roll-up: a per-county workflow (judicial circuit, State Court status, Magistrate, e-filing platform, local rules) for any county without a dedicated venue skill.
- **`ga-family-court`** — where Georgia hears family matters (Superior Court exclusively; per-circuit Family Divisions), intake, financial affidavit, and the parenting-plan requirement.

**Procedural skills** — `ga-statewide-format`, `ga-pro-se`, `ga-first-30-days`, `ga-discovery`, `ga-hearings`, `ga-schedule-hearing`, `ga-submit-order`, `ga-post-judgment`, `ga-deadlines`, `ga-fact-check`, `ga-quality-check`, `ga-file-packet`, `ga-draft-motion`, `ga-draft-declaration`, `ga-draft-note`, `ga-draft-order`, and the reference hub `ga-law-references`.

**Subject-matter bundles**

- **`ga-consumer-debt`** — debt-buyer / collection defense. Federal FDCPA-forward (Georgia has **no mini-FDCPA and does not license most collectors**); the **Fair Business Practices Act** overlay (O.C.G.A. § 10-1-390 et seq.) with its **mandatory 30-day pre-suit written demand** (§ 10-1-399(b)) and **treble damages** (§ 10-1-399(c)); chain-of-title / standing (*Nyankojo*); business-records foundation (§§ 24-8-803(6), 24-9-902(11)); and the **6-year written-contract SOL on credit-card debt** (§ 9-3-24; *Hill v. American Express*).
- **`ga-family-law`** — divorce (13 grounds, § 19-5-3), **equitable distribution** (*Stokes v. Stokes*), **income-shares child support** (§ 19-6-15), best-interests custody with the age-14 child election (§ 19-9-3), alimony (§ 19-6-1 et seq.), the Family Violence Act/TPO (§ 19-13), UCCJEA/UIFSA, and the abolition of common-law marriage (§ 19-3-1.1).

### Procedural quirks flagged in the skills

- **State Court vs. Superior Court is a subject split, not a dollar split** — most debt/tort suits land in State Court, which has no amount ceiling.
- **30-day answer + a 15-day open-default-as-of-right window** (O.C.G.A. §§ 9-11-12, 9-11-55; *Bowen v. Savoy*).
- **Credit-card debt runs on the 6-year written-contract SOL**, not the 4-year open-account SOL (*Hill v. American Express*; *Phoenix Recovery v. Mehta*).
- **No state licensing of most debt collectors / debt buyers**; the FBPA is the state-law vehicle, gated by a 30-day pre-suit demand.
- **Post-2016 garnishment overhaul** (Title 18, ch. 4; *Strickland v. Alexander*) with the § 18-4-15 defendant's-claim mechanism and § 18-4-5 wage / § 18-4-6 funds exemptions; Georgia is a § 44-13-100 **opt-out** exemption state.
- **E-filing platform differs by county** — PeachCourt (Fulton, Cobb) vs. Odyssey eFileGA (Gwinnett).
- **Lau's Corp. v. Haskins** summary-judgment standard (movant may point to an absence of evidence).

## Reference corpora

Under `skills/ga-law-references/references/` (each corpus dir has its own README): `ga-statutes-debt/` (the O.C.G.A. chapters — Title 9 CPA + limitations, Title 24 Evidence, Title 10 FBPA, Title 7 Installment Loan Act, Title 18 garnishment, Title 44 landlord-tenant + exemptions, Title 19 domestic relations, Title 15 courts, Title 11 UCC), `court-rules/` (USCR / Uniform State / Uniform Magistrate / appellate rules), plus the shared `federal-debt-laws/` / `federal-bankruptcy/` / `ucc-model/` symlinks into `claude-legal-federal-laws`.

Citation/verification note: the official O.C.G.A. (LexisNexis) is paywalled; open mirrors used for refresh are codes.findlaw.com/ga (current) and law.justia.com/codes/georgia. Court rules come from georgiacourts.gov. The bundled CourtListener + Legal Data Hunter MCP servers (from the federal dependency) drive on-demand case-law lookup (Georgia court IDs `ga` / `gactapp`).

## Refresh

Plugin scripts: `scripts/format-check.py` (marketplace format baseline) · `scripts/case-calendar.py` (O.C.G.A. § 1-3-1(d)(3) / § 9-11-6(a) time computation with § 1-4-1 holidays and Georgia named deadline rules).

Corpus pullers (repo root `scripts/`): `pull_georgia_statutes.py` (O.C.G.A. → `ga-statutes-debt/`) and `pull_georgia_rules.py` (Uniform Rules → `court-rules/`).

---
Part of the [claude-legal](../../README.md) marketplace. Skills are indexed in [CLAUDE.md](../../CLAUDE.md).
