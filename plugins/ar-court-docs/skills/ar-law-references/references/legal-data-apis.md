# Arkansas Legal Data — Programmatic Access Index

> **NOT LEGAL ADVICE.** Agent-facing index of structured / programmatic
> sources for Arkansas legal data. Endpoints and identifiers change;
> confirm before relying on them.

## Case law — CourtListener

CourtListener (Free Law Project) exposes Arkansas appellate opinions
via REST API and full-text search.

| Court | CourtListener court id |
|---|---|
| Arkansas Supreme Court | `ark` |
| Arkansas Court of Appeals | `arkctapp` |

- **Search / opinions API**: `https://www.courtlistener.com/api/rest/`
  (filter by `court=ark` or `court=arkctapp`).
- Use the medium-neutral citation (`YYYY Ark. NNN` / `YYYY Ark. App.
  NNN`) where available; CourtListener also carries the `S.W.3d`
  parallel.
- Good for: confirming a cite, pulling opinion text, checking later
  history before relying on a case in `key-cases.md`.

## Statutes — Arkansas Code Annotated

- **Official lookup (human-facing, not a clean API)**:
  `https://arkleg.state.ar.us` — the Arkansas General Assembly Code
  search and act/bill history.
- **Justia structured mirror** (used by the puller): base
  `https://law.justia.com/codes/arkansas/` then drill by
  Title → Subtitle/Chapter → Subchapter → Section. The bare section
  text is **public domain**. Justia sits behind Cloudflare, so a pull
  script typically needs **curl_cffi Chrome impersonation** (the same
  approach the other statute pullers use when the mirror is gated).
- **FindLaw mirror**: `https://codes.findlaw.com/ar/` (alternate
  structured source).

## Court rules — ARCP / Ark. R. Evid. / District Court / Admin Orders

- **Official**: `https://arcourts.gov` (Rules of the Supreme Court and
  Court of Appeals; the rule sets and Administrative Orders). The bare
  rule text is a **public-domain edict**.
- **opinions.arcourts.gov/ark/cr/en/** — the official Arkansas Judiciary
  Court Rules database (Lexum); each rule set is one PDF document at
  `/ark/cr/en/<docid>/1/document.do`. The verbatim rule-text source.

## Pull-script targets (for `pull_arkansas_rules.py` /
## `pull_arkansas_statutes.py`)

- **Rules** → `court-rules/`: ARCP, Ark. R. Evid., Arkansas District
  Court Rules, Ark. Sup. Ct. & Ct. App. Rules, Administrative Orders
  (esp. **No. 10**, **No. 19**, **No. 21**). Source: the official
  opinions.arcourts.gov Court Rules PDFs (pdftotext).
- **Statutes** → `ar-statutes-debt/`: the civil + family + consumer
  surface of the **Arkansas Code Annotated** — see
  `ar-statutes-debt/README.md` for the full target table. Source:
  Justia mirror (public-domain text), spot-checked against
  arkleg.state.ar.us.

## Other forums (non-circuit, for completeness)

- **Arkansas Workers' Compensation Commission** —
  `https://www.awcc.state.ar.us` (opinions / forms; the exclusive
  workers'-comp forum).
- **Arkansas State Claims Commission** — the forum for claims against
  the State (see `key-cases.md`, *Andrews*).

## Verification discipline

1. Pull bulk text from the **free mirror**, then **spot-check against
   the official publisher** before citing.
2. For any case you rely on, confirm **current validity** via
   CourtListener (later history) — especially the actively litigated
   tort-reform and State-immunity lines.
