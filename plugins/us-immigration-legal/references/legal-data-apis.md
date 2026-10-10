# Immigration Legal Data APIs — Machine-Readable Sources

Companion to `online-sources.md` (which lists canonical URLs for human reading).
This file lists **structured, on-demand sources** an agent should hit when
looking up or fact-checking immigration law and case law — official/free and
stable enough to script against.

Immigration practice has two distinct source layers, handled differently:

- **Statutes + regulations (INA, 8 CFR, 22 CFR)** — *snapshotted verbatim* into
  this plugin's `references/immigration-statutes/` and
  `references/immigration-regulations/` corpora by `scripts/pull_ina.py` and
  `scripts/pull_immigration_cfr.py`. Read those first; hit the live APIs below
  only to confirm a post-snapshot amendment.
- **Case law (federal circuits, BIA, AAO)** — *not snapshotted.* Immigration
  case law is too large and fast-moving to mirror, so it is fetched **on
  demand** via the APIs / MCP tools below. This is the same discipline the
  state plugins use for case law (CourtListener over a local snapshot).

## When to use what

| Need | Best source | Why |
|---|---|---|
| Verbatim INA / U.S.C. text | local `immigration-statutes/` corpus → uscode.house.gov USLM XML | Official; already snapshotted |
| Verbatim 8 CFR / 22 CFR text | local `immigration-regulations/` corpus → eCFR Versioner API | Official; already snapshotted |
| FAM guidance text | local `foreign-affairs-manual/` corpus → fam.state.gov | Verbatim; puller AIA-chases the server's omitted TLS intermediate + crawls the JSON TOC API |
| Federal **circuit court** immigration opinion | CourtListener (MCP `search` / REST v4) | Full text + citations; covers all 13 circuits |
| **Board of Immigration Appeals** precedent (I&N Dec.) | EOIR Virtual Law Library + CourtListener | EOIR is the publisher of record; CL indexes many |
| **AAO** (USCIS Administrative Appeals Office) decisions | USCIS AAO decisions site | The only authoritative source for AAO non-precedent + precedent |
| "Is this cite real / what does it say?" | CourtListener Citation Lookup | Returns the case given any citation format |

## 1. CourtListener — federal circuit immigration case law

CourtListener (Free Law Project) is the primary programmatic source for
federal appellate immigration decisions. **A CourtListener MCP server is wired
into this environment** — prefer its tools when available; fall back to the
REST API otherwise.

### MCP tools (preferred when present)

- `search` — hybrid search over Opinions / RECAP / Judges / Oral arguments.
  Restrict to the circuits with the `court` filter and use the `fields`
  argument aggressively (opinion text fields are huge — request
  `html_with_citations` only when you need the body).
- `get_endpoint_schema` + `call_endpoint` — richer detail on a specific
  opinion / cluster / docket than the search index exposes.
- `analyze_citations` / `extract_citations` — pull and validate the citations
  out of a brief or opinion.

### REST API (no key required for search; free tier)

```
GET https://www.courtlistener.com/api/rest/v4/search/?q={query}&type=o&court={court_ids}
GET https://www.courtlistener.com/api/rest/v4/opinions/{id}/
POST https://www.courtlistener.com/api/rest/v4/citation-lookup/   (body: {"text": "..."} )
```

### Court IDs for the federal circuits (use in `court=`)

The circuits that hear the most petitions for review of removal orders:

| Circuit | CourtListener `court` id |
|---|---|
| First | `ca1` |
| Second | `ca2` |
| Third | `ca3` |
| Fourth | `ca4` |
| Fifth | `ca5` |
| Sixth | `ca6` |
| Seventh | `ca7` |
| Eighth | `ca8` |
| **Ninth** (largest immigration docket) | `ca9` |
| Tenth | `ca10` |
| Eleventh | `ca11` |
| D.C. | `cadc` |
| Federal | `cafc` |
| U.S. Supreme Court | `scotus` |

> Most immigration appeals reach an Article III court as a **petition for
> review of a BIA final order** under INA § 242 (8 U.S.C. § 1252), filed
> directly in the circuit where the immigration judge completed proceedings —
> there is no district-court layer for the merits. District courts do appear
> for **habeas** (detention), **naturalization** (INA § 336(b) / § 310(c)),
> and **mandamus/APA** delay suits — searchable the same way with the relevant
> district `court` id.

## 2. Board of Immigration Appeals (BIA) — precedent decisions

The BIA's **precedent** decisions are published as *Administrative Decisions
Under Immigration and Nationality Laws of the United States* — cited **"I&N
Dec."** (e.g., *Matter of A-B-*, 28 I&N Dec. 199 (BIA 2021)). The Board issues
thousands of unpublished decisions; only the bound-volume precedents bind.

- **EOIR Virtual Law Library / BIA precedent index** — the publisher of record.
  Browse by volume; each decision is a PDF. See `online-sources.md` for the URL.
- **CourtListener** indexes many BIA precedents — search with `type=o` and the
  citation, or use `citation-lookup` on an "I&N Dec." cite.
- **DOJ EOIR** also posts the current AG- and BIA-certified decisions list.

There is **no clean public JSON API** for the full I&N Dec. set; retrieval is
URL/PDF-based (EOIR) or via CourtListener's index. Confirm a precedent is still
good law — the Attorney General can **certify and overrule** BIA decisions
(*Matter of* A-G referrals), and circuits split on deference.

## 3. AAO — USCIS Administrative Appeals Office decisions

The AAO adjudicates appeals of most USCIS benefit denials (I-140, I-129, waiver
applications, etc.) that do **not** go to the BIA. Two tiers:

- **Non-precedent decisions** — the large majority; persuasive only. Published
  on the USCIS AAO decisions site, organized by benefit type and month, as PDFs.
- **Precedent decisions** — designated and binding agency-wide; also collected
  in the I&N Dec. volumes alongside BIA/AG precedents.

Retrieval is **website/PDF-based** (USCIS AAO decisions browser); there is no
official JSON API. See `online-sources.md` for the entry URL. CourtListener does
**not** comprehensively index AAO non-precedent decisions — go to the USCIS site.

## 4. Statute / regulation refresh APIs (for verifying the snapshots)

| Source | Endpoint | Used by |
|---|---|---|
| U.S. Code (INA) USLM XML | `https://uscode.house.gov/download/releasepoints/us/pl/<congress>/<law>/xml_usc08@<release>.zip` (note the **zero-padded** `usc08`) | `scripts/pull_ina.py` |
| eCFR Versioner (8/22 CFR) | `https://www.ecfr.gov/api/versioner/v1/full/{date}/title-{8|22}.xml?part={part}` | `scripts/pull_immigration_cfr.py` |
| Citation lookup | `POST https://www.courtlistener.com/api/rest/v4/citation-lookup/` | ad hoc |

> **NOT LEGAL ADVICE.** These sources support drafting and research; verify
> currency and good-law status before relying on any result.
