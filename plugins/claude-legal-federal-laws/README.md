# claude-legal-federal-laws

Shared reference corpus for the `claude-legal` marketplace, plus a nationwide consumer
credit-report-rights skills layer.

## What's in here

- `references/federal-debt-laws/` — verbatim text of U.S. consumer-finance and debt-collection statutes (FDCPA, FCRA, TILA, ECOA) and the CFPB regulations that implement them (Reg B, Reg F, Reg V, Reg Z). Pulled from `uscode.house.gov` USLM XML and the eCFR Versioner API by [`scripts/pull_federal_debt_laws.py`](../../scripts/pull_federal_debt_laws.py).
- `references/ucc-model/` — model Uniform Commercial Code, Articles 1 (General Provisions), 2 (Sales), 3 (Negotiable Instruments), and 9 (Secured Transactions). The *model* text as drafted by ALI/ULC; pulled from Cornell Legal Information Institute (`law.cornell.edu/ucc`) by [`scripts/pull_ucc.py`](../../scripts/pull_ucc.py). State-court matters should cite the enacting state code (e.g., RCW Title 62A for Washington), not the model text — the model is included here for interpreting uniform language across states.
- `references/ada-laws/` — the **Americans with Disabilities Act** (42 U.S.C. ch. 126, §§ 12101–12213) and its three core implementing regulations: EEOC Title I (29 C.F.R. Part 1630), DOJ Title II (28 C.F.R. Part 35), and DOJ Title III (28 C.F.R. Part 36, whose appendices carry the 2010 ADA Standards for Accessible Design). Verbatim from `uscode.house.gov` USLM XML and the eCFR Versioner API; pulled by [`scripts/pull_ada.py`](../../scripts/pull_ada.py). Mirrors the corpus at [ada.gov/law-and-regs](https://www.ada.gov/law-and-regs/). See [`references/ada-laws/README.md`](references/ada-laws/README.md).
- `skills/` — a **consumer credit-report-rights skills layer** built on the FCRA (15 U.S.C. §§ 1681 et seq.). These are state-independent, matter-neutral self-help skills that produce documents (request/dispute letters, identity-theft block requests, communication logs, damages ledgers, harm declarations, re-notification demands, review checklists), not legal advice. They cite the FCRA text in `references/federal-debt-laws/FCRA.md` and compose with the per-state `*-consumer-debt` and `*-pro-se` skills.

  | Skill | Role |
  |---|---|
  | `consumer-report-ordering` | Order all Big-3 + specialty CRA reports; free-report entitlements; private right of action for non-delivery |
  | `consumer-credit-disputes` | Lawful direct-to-CRA disputes (§ 1681i); 4-business-day identity-theft block (§ 1681c-2); post-dispute regulator escalation |
  | `consumer-report-accuracy` | PII hygiene; Date of First Delinquency + re-aging; the "disputed by consumer" flag |
  | `consumer-harm-documentation` | Communication logs, damages ledgers, and harm declarations |
  | `consumer-credit-monitoring` | Adverse-action proof; § 1681i(d) re-notification; ongoing review |
  | `ada-rights` | Nationwide ADA self-help: reasonable-accommodation / reasonable-modification requests, ADA grievances, DOJ ADA complaints, and EEOC charge intake — routed across Title I (employment / 29 CFR 1630), Title II (state & local government / 28 CFR 35), and Title III (public accommodations / 28 CFR 36 + 2010 Standards) |
  | `case-law-research` | Live legal research via the bundled MCP servers (below): U.S. case law / RECAP dockets / judges via CourtListener, multi-jurisdictional + foreign law via Legal Data Hunter; never-cite-from-memory + quote-check discipline |

## Why it's a plugin

The federal and model-UCC corpora live in one canonical place rather than being copy-pasted into every state plugin (`wa-court-docs`, `or-court-docs`, `ca-court-docs`, `co-court-docs`, `in-court-docs`, `ny-court-docs`, `oh-court-docs`). Because every state plugin depends on this one, the consumer credit-report-rights skills also ride along — they are available anywhere any state plugin is installed.

State plugins declare this plugin in their `plugin.json` `dependencies` array. When a user runs `/plugin install <state>-court-docs@claude-legal`, the Claude Code marketplace runtime auto-installs this plugin alongside, dereferences the symlinks each state plugin uses to point into this directory (per the Claude Code plugin spec, symlinks within a marketplace are followed and the target content is copied into the install cache), and the federal/UCC files end up locally available under each state plugin's `references/` tree at runtime.

## Bundled MCP servers

The plugin's [`.mcp.json`](.mcp.json) declares two free remote MCP servers, which connect automatically when the plugin is enabled (run `/mcp` in Claude Code to complete the one-time sign-in for each):

- **CourtListener** (`https://mcp.courtlistener.com/`) — Free Law Project's legal-research database: millions of federal and state opinions, the RECAP archive of PACER dockets, oral arguments, and a judges database. Free CourtListener account; OAuth sign-in — no API token needed.
- **Legal Data Hunter** (`https://legaldatahunter.com/mcp`) — multi-jurisdictional legal research (court decisions, statutes/regulations, doctrine across 100+ countries) with hybrid semantic + keyword search. Free; GitHub/Google sign-in.

Because every state plugin depends on this plugin, these servers are available anywhere any state plugin is installed. They serve the on-demand case-law layer described in each state plugin's `legal-data-apis.md` — reference corpora (statutes, court rules) stay snapshotted in-repo, while case law is fetched live. The `case-law-research` skill drives them: it routes each research question to the right server, enforces never-cite-a-case-from-memory and quote-check discipline, and hands confidence-flagged results to the per-state `*-fact-check` skills.

## Refresh

The quarterly `refresh-references` GitHub Action runs `pull_federal_debt_laws.py`, `pull_ucc.py`, and `pull_ada.py` against the paths in this plugin, then opens a PR. Federal/UCC/ADA content is now updated once per quarter instead of once per state.

## Not legal advice

The reference text is verbatim from official sources and is provided as a drafting aid. The skills produce drafting aids and checklists, not legal advice, and do not create an attorney-client relationship. Verify against the current statutes and regulations before relying on any citation in a filing.
