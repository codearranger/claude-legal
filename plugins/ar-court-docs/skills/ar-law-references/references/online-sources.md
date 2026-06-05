# Arkansas Online Sources — Canonical URLs

> **NOT LEGAL ADVICE.** Source catalog for verification. URLs change;
> confirm each source is current and authoritative when you use it.

## Rules of court / Administrative Orders / forms

- **Arkansas Judiciary (Administrative Office of the Courts)** —
  https://arcourts.gov
  - Rules of the Supreme Court and Court of Appeals; the **Arkansas
    Rules of Civil Procedure (ARCP)**; **Arkansas Rules of Evidence**;
    the **Arkansas District Court Rules**; and the **Administrative
    Orders** (incl. **No. 10** child support, **No. 19** access to
    court records / redaction, **No. 21** electronic filing).
  - **Court forms** (domestic relations, protection orders, etc.) and
    **self-help** materials.
  - The **bare rule text is a public-domain edict**; commercial
    annotated compilations (LexisNexis) are copyrighted only as to the
    annotations.
- **opinions.arcourts.gov/ark/cr/en/** — the official Arkansas Judiciary
  Court Rules database (Lexum); each rule set is published as a PDF at
  `/ark/cr/en/<docid>/1/document.do`. This is the verbatim source the
  rules puller uses.

## Statutes — Arkansas Code Annotated

- **Arkansas General Assembly** — https://arkleg.state.ar.us
  (the official Arkansas Code Annotated lookup; bill / act history).
- **Justia** — https://law.justia.com/codes/arkansas/ (free structured
  mirror of the **public-domain** Arkansas Code section text; useful for
  programmatic pulls; may require Cloudflare-compatible fetching).
- **FindLaw** — https://codes.findlaw.com/ar/ (another free mirror).

## Opinions / case law

- **Arkansas appellate opinions** — arcourts.gov opinions search
  (Arkansas Supreme Court + Court of Appeals).
- **CourtListener** — https://www.courtlistener.com (Arkansas Supreme
  Court and Court of Appeals opinions; full-text search; see
  `legal-data-apis.md` for the court ids and API).

## Specialized agencies / forums (not circuit court)

- **Arkansas Workers' Compensation Commission** —
  https://www.awcc.state.ar.us (exclusive forum for workers'-comp).
- **Arkansas State Claims Commission** — the forum for claims against
  the **State** (Ark. Code Ann. § 19-10-201 et seq.; see *Andrews* in
  `key-cases.md`).
- **Arkansas State Board of Collection Agencies** — collection-agency
  licensing (Ark. Code Ann. § 17-24-101 et seq.); useful to confirm a
  collector's license status in a debt-buyer matter.
- **Arkansas Attorney General — Consumer Protection** — ADTPA
  enforcement and consumer complaint intake.

## Legal aid / self-help

- **Legal Aid of Arkansas** — https://arlegalaid.org
- **Center for Arkansas Legal Services** — https://www.arlegalservices.org
- **Arkansas Legal Services Partnership / ArLawHelp** —
  https://www.arlegalservices.org / https://www.arlawhelp.org
  (self-help guides + forms for eligible litigants).
- **Arkansas Bar Association** — lawyer-referral service.

## Notes on access posture

- Prefer the **official** publisher (arcourts.gov / arkleg.state.ar.us)
  for anything you will cite.
- Use the **public-domain text sources** (the official
  opinions.arcourts.gov Court Rules PDFs for rules; the Justia mirror for
  Code sections) for bulk pulls, then **spot-check against the official
  source**.
