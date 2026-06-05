---
name: ar-law-references
description: >
  Matter-neutral reference catalog for Arkansas civil practice and the
  canonical host of the plugin's reference corpora. Contains the Arkansas
  Rules of Civil Procedure (ARCP) summary, the Arkansas Rules of Evidence
  (Ark. R. Evid.) summary with emphasis on the 803(6) business-records
  exception and 902(11) self-authentication, the fees-and-costs framework
  (Ark. Code Ann. § 16-22-308 contract/civil-action fee-shifting), Arkansas
  medium-neutral citation format under Ark. Sup. Ct. R. 5-2, an index of
  where circuit/district local rules live, and the canonical online-sources
  catalog. Triggers include "Arkansas civil rule", "Ark. R. Civ. P.", "ARCP",
  "Arkansas rule of civil procedure", "Ark. R. Evid.", "Arkansas evidence
  rule", "Ark. Code Ann. § ...", "Arkansas Code", "Arkansas citation format",
  "medium-neutral citation", "2015 Ark. 100", "Ark. App.", "what's the
  Arkansas rule on X", "look up Arkansas law on X", "Circuit Court",
  "District Court", "Amendment 80", "Administrative Order No. 19",
  "Administrative Order No. 21", "arcourts.gov", "S.W.3d Ark". Other ar-
  skills cite this one for specific rule numbers and case authorities;
  the heavy reference corpora (court-rules, ar-statutes-debt,
  federal-debt-laws, federal-bankruptcy, ucc-model) live in this skill's
  `references/` subdirectory.
version: 0.1.0
---

# Arkansas Law References

> **NOT LEGAL ADVICE.** Reference catalog only. Read the cited rule,
> statute, or case in full — and confirm it is current — before
> relying on it.

This is the **matter-neutral** reference index for Arkansas civil
practice. Other skills in the `ar-court-docs` plugin point here for
rule numbers, statute citations, and case authorities. This skill is
also the physical **host** of the plugin's reference corpora.

## What's here

```
references/
├── court-rules/            # Verbatim rule text — ARCP, Ark. R. Evid.,
│                           #   Arkansas District Court Rules, Supreme
│                           #   Court / Court of Appeals Rules, and the
│                           #   Administrative Orders — corpus
├── ar-statutes-debt/       # Arkansas Code Annotated titles/chapters most
│                           #   relevant to civil practice — corpus
│                           #   (legacy slug; scope is the whole civil
│                           #   + family + consumer surface, not debt-only)
├── federal-debt-laws/      # FDCPA, FCRA, TILA, etc. (symlink into the
│                           #   shared claude-legal-federal-laws plugin)
├── federal-bankruptcy/     # Title 11 U.S.C. (symlink into shared plugin)
└── ucc-model/              # Model UCC Articles 1/2/3/9 (symlink into
                            #   shared plugin)
```

The three symlinked corpora (`federal-debt-laws/`,
`federal-bankruptcy/`, `ucc-model/`) point into the shared
`claude-legal-federal-laws` plugin so the federal text is stored once,
not copied per state. The Arkansas-specific corpora (`court-rules/`,
`ar-statutes-debt/`) live physically under this skill.

The companion reference files in `references/` carry the volatile
specifics — day counts, dollar thresholds, the interrogatory cap, exact
subsection lettering — so the skill bodies in this plugin can stay
thin and point here:

- `references/civil-rules.md` — ARCP rule-by-rule summary
- `references/evidence-rules.md` — Ark. R. Evid. summary
- `references/citation-format.md` — Arkansas medium-neutral citation
- `references/fees-and-costs.md` — fee-shifting + costs framework
- `references/key-cases.md` — general-civil + procedural precedents
- `references/online-sources.md` — canonical URLs
- `references/legal-data-apis.md` — programmatic-access index

## Court structure — terminology

Arkansas **unified its trial courts** under **Amendment 80** to the
Arkansas Constitution (adopted November 2000, effective July 1, 2001).
Amendment 80 merged the former separate **Chancery Courts** (equity),
**Probate Courts**, and **Circuit Courts** (law) into a single
**Circuit Court** of general jurisdiction. There is no longer a
separate chancery or equity court — law and equity are unified.

| Court | Jurisdiction |
|---|---|
| **Circuit Court** | General-jurisdiction trial court. Organized by Supreme Court administrative plan into **five subject-matter divisions** — criminal, civil, probate, domestic relations, and juvenile — which are administrative divisions of **one court**, not separate courts; a circuit judge may sit in any division. **28 judicial circuits** across **75 counties**. |
| **District Court** | **Limited**-jurisdiction trial court (renamed from "Municipal Court" by Amendment 80). Civil jurisdiction up to a statutory cap, with a **small claims division** for smaller claims (see `references/civil-rules.md` for the current dollar amounts under Ark. Code Ann. § 16-17-704). Handles civil, small claims, misdemeanors, traffic, and **unlawful detainer / eviction**. The high-volume consumer-debt + eviction forum. |
| **City Courts** | In some small cities lacking a district court. |

Appeals from **District Court** go to **Circuit Court for de novo
review** (verify the current appeal period and mechanics in
`references/civil-rules.md`). The appellate courts are the **Arkansas
Court of Appeals** (intermediate) and the **Arkansas Supreme Court**.

Divorce, custody, and support are heard in the **Domestic Relations
Division** of Circuit Court; paternity, dependency-neglect, FINS, and
termination of parental rights are in the **Juvenile Division** of
Circuit Court (Arkansas Juvenile Code, Ark. Code Ann. Title 9, ch. 27).
There is no separate family court.

## Ark. R. Civ. P. — Arkansas Rules of Civil Procedure

The ARCP were adopted in 1979, modeled on the Federal Rules but with
Arkansas variations. The rules every Arkansas civil practitioner uses:

| Rule | Subject |
|---|---|
| Ark. R. Civ. P. 4 | Summons and service of process (service period — verify the current day count in `references/civil-rules.md`) |
| Ark. R. Civ. P. 5 | Service and filing of subsequent papers; e-filing under Administrative Order No. 21 |
| Ark. R. Civ. P. 6 | Time computation (6(a)); the 3-day mail add-on (6(d)) |
| Ark. R. Civ. P. 8 | General rules of pleading; **fact pleading** (8(a) requires a statement of *facts*); affirmative defenses (8(c)) |
| Ark. R. Civ. P. 9 | Pleading special matters — fraud/mistake with particularity (9(b)) |
| Ark. R. Civ. P. 10 | Form of pleadings — caption (10(a)), numbered paragraphs (10(b)), attaching written instruments (10(c)) |
| Ark. R. Civ. P. 11 | Signing of pleadings and motions; the Rule 11 certification |
| Ark. R. Civ. P. 12 | Defenses and objections; answer deadline; Rule 12(b) motions, incl. **12(b)(6) failure to state facts upon which relief can be granted** |
| Ark. R. Civ. P. 13 | Counterclaim and cross-claim (compulsory vs. permissive) |
| Ark. R. Civ. P. 15 | Amended and supplemental pleadings |
| Ark. R. Civ. P. 26–37 | Discovery — scope, interrogatories (Rule 33, presumptive cap), production (34), admissions (36), depositions (30/31), motion to compel (37) |
| Ark. R. Civ. P. 55 | Default judgment |
| Ark. R. Civ. P. 56 | Summary judgment — the "meet proof with proof" standard |
| Ark. R. Civ. P. 59 | New trial |
| Ark. R. Civ. P. 60 | Relief from judgment or order — the **90-day Rule 60(a)** modify/vacate window; narrower Rule 60(c) grounds after 90 days |

> **Arkansas is a fact-pleading jurisdiction.** Ark. R. Civ. P. 8(a)
> requires "a statement in ordinary and concise language of facts" — a
> complaint must plead **facts**, not mere conclusions. This is
> stricter than federal notice pleading and drives Rule 12(b)(6)
> practice. See `ar-first-30-days`.

Confirm current day counts and subsection lettering against the
verbatim text in `references/court-rules/` before relying on them.

## Ark. R. Evid. — Arkansas Rules of Evidence

The Arkansas Rules of Evidence track the federal model closely. The
two most load-bearing rules for documentary civil practice (especially
debt-buyer and business-records matters):

- **Ark. R. Evid. 803(6)** — the **business-records** hearsay
  exception. A record of a regularly conducted activity is admissible
  if a **custodian or other qualified witness** lays the foundation
  (made at or near the time by someone with knowledge, kept in the
  regular course, regular practice to keep it) — unless the source or
  circumstances indicate a lack of trustworthiness.
- **Ark. R. Evid. 902(11)** — **self-authentication** of certified
  domestic business records. A qualifying written certification can
  substitute for live foundation testimony — the standard pathway by
  which a debt buyer tries to get account records in without a witness.
- **Ark. R. Evid. 901** — authentication generally.

Other commonly cited rules: 401–403 (relevance / unfair prejudice),
404(b) (other acts), 408 (compromise offers), 602 (personal
knowledge), 702–703 (experts), 801–807 (hearsay), 1001–1008 (best
evidence). See `references/evidence-rules.md`.

## Fees and costs

Arkansas follows the **American rule** — each party bears its own
attorney's fees unless a statute, rule, or contract shifts them. The
authority invoked most often in civil practice:

- **Ark. Code Ann. § 16-22-308** — in any civil action to recover on a
  **contract** (and in certain other civil actions), the court **may**
  award reasonable attorney's fees to the **prevailing party**. The
  award is **discretionary**, not automatic. This is the principal
  Arkansas fee-shifting statute and cuts both ways in a contract /
  consumer-debt case — the prevailing **defendant** can recover too.
- **15 U.S.C. § 1692k(a)(3)** — FDCPA attorney's fees to a prevailing
  consumer.
- **Contractual fee provisions** — enforceable per their terms,
  subject to reasonableness review.

Filing-fee schedules are set by statute and by the clerk of each
court; confirm the current amount with the clerk of the filing court.
See `references/fees-and-costs.md`.

## Citation format

Arkansas uses a **medium-neutral / public-domain citation** for
opinions issued on or after **July 1, 2009**, governed by **Ark. Sup.
Ct. R. 5-2**:

- **Arkansas Supreme Court (post-7/1/2009)**: `Smith v. Jones, 2015 Ark. 100`
- **Arkansas Court of Appeals (post-7/1/2009)**: `Smith v. Jones, 2015 Ark. App. 200`
- Parallel `S.W.3d` cites are commonly added but the medium-neutral
  cite is the required form.
- **Pre-7/1/2009 cases**: cite to the **Arkansas Reports** plus the
  South Western Reporter — e.g., `Sterling Drug, Inc. v. Oxford, 294 Ark. 239, 743 S.W.2d 380 (1988)`.
- **Statutes**: `Ark. Code Ann. § 16-56-111`.
- **Rules**: `Ark. R. Civ. P. 12`; `Ark. R. Evid. 803(6)`;
  `Ark. Sup. Ct. R. 5-2`.
- **Federal**: `15 U.S.C. § 1692g(b)`; `12 C.F.R. § 1006.34`.

There is **no formal Arkansas state style manual** — Rule 5-2 modifies
an otherwise Bluebook-based practice. See `references/citation-format.md`.

## Local rules and filing — where they live

Arkansas has **no single statewide page-limit / margin / font rule**
for trial-court pleadings. Document form is governed by **Ark. R. Civ.
P. 10** (caption, numbered paragraphs, exhibits) and **Rule 11**
(signature), plus:

- **Administrative Order No. 19** — Access to Court Records; requires
  **redaction** of confidential / identifying information (SSNs,
  account numbers, minors' identifiers) and a certificate of
  compliance. See `ar-pro-se` for the self-redaction workflow.
- **Administrative Order No. 21** — Electronic Filing; statewide
  e-filing via **eFlex** (Contexte case-management system). Registered
  e-filers consent to e-service.
- **Administrative Order No. 10** — the child-support guidelines (the
  income-shares Family Support Chart, effective July 1, 2020).
- **Circuit / district administrative plans and local rules** — set
  margins, page limits, chambers-copy conventions, and motion-day
  mechanics per venue. Confirm with the clerk.

Appellate briefs have a strict format under **Ark. Sup. Ct. R. 4-1 /
4-2**, with mandatory appellate e-filing — but that is appellate, not
trial-court, practice.

## Online sources

- **Arkansas Judiciary / Administrative Office of the Courts**:
  https://arcourts.gov (court rules, Administrative Orders, forms,
  opinions, self-help)
- **Arkansas Code Annotated**: via the Arkansas General Assembly at
  https://arkleg.state.ar.us (plus public / commercial mirrors such as
  law.justia.com/codes/arkansas)
- **Arkansas appellate opinions**: arcourts.gov opinions and
  **CourtListener** (Arkansas Supreme Court, Court of Appeals)

See `references/online-sources.md` and `references/legal-data-apis.md`
for the full catalog, and the `references/` corpora for verbatim rule
and statute text.

## Composition

- Every other Arkansas skill cites this one for rule numbers, statute
  numbers, and case authorities.
- For the filing court's mechanics: `ar-pulaski`, `ar-benton`,
  `ar-washington`, `ar-district-courts`, `ar-county-courts`.
- For self-represented conventions: `ar-pro-se`.
- For the defendant's response window: `ar-first-30-days`.
- For discovery: `ar-discovery`.
- For matter-specific bundles: the `ar-consumer-debt`, `ar-family-law`,
  `ar-landlord-tenant`, `ar-personal-injury`, `ar-employment`, and
  `ar-commercial-disputes` skills.

## References

- `references/civil-rules.md` — ARCP rule-by-rule summary
- `references/evidence-rules.md` — Ark. R. Evid. summary
- `references/citation-format.md` — Arkansas medium-neutral citation
- `references/fees-and-costs.md` — fee-shifting + costs
- `references/key-cases.md` — general-civil + procedural precedents
- `references/online-sources.md` — canonical URLs
- `references/legal-data-apis.md` — programmatic-access index
- `references/court-rules/` — verbatim ARCP / Ark. R. Evid. / District
  Court Rules / Supreme Court & Court of Appeals Rules / Administrative
  Orders corpus
- `references/ar-statutes-debt/` — Arkansas Code Annotated chapters
  most relevant to civil practice
- `references/federal-debt-laws/` — federal-law corpus (symlink)
- `references/federal-bankruptcy/` — Title 11 U.S.C. corpus (symlink)
- `references/ucc-model/` — Model UCC text (symlink)
