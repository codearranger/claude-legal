# claude-legal-federal-laws

Shared reference corpus for the `claude-legal` marketplace, plus a nationwide consumer
credit-report-rights skills layer.

## What's in here

- `references/federal-debt-laws/` — verbatim text of U.S. consumer-finance and debt-collection statutes (FDCPA, FCRA, TILA, ECOA) and the CFPB regulations that implement them (Reg B, Reg F, Reg V, Reg Z). Pulled from `uscode.house.gov` USLM XML and the eCFR Versioner API by [`scripts/pull_federal_debt_laws.py`](../../scripts/pull_federal_debt_laws.py).
- `references/ucc-model/` — model Uniform Commercial Code, Articles 1 (General Provisions), 2 (Sales), 3 (Negotiable Instruments), and 9 (Secured Transactions). The *model* text as drafted by ALI/ULC; pulled from Cornell Legal Information Institute (`law.cornell.edu/ucc`) by [`scripts/pull_ucc.py`](../../scripts/pull_ucc.py). State-court matters should cite the enacting state code (e.g., RCW Title 62A for Washington), not the model text — the model is included here for interpreting uniform language across states.
- `skills/` — a **consumer credit-report-rights skills layer** built on the FCRA (15 U.S.C. §§ 1681 et seq.). These are state-independent, matter-neutral self-help skills that produce documents (request/dispute letters, identity-theft block requests, communication logs, damages ledgers, harm declarations, re-notification demands, review checklists), not legal advice. They cite the FCRA text in `references/federal-debt-laws/FCRA.md` and compose with the per-state `*-consumer-debt` and `*-pro-se` skills.

  | Skill | Role |
  |---|---|
  | `consumer-report-ordering` | Order all Big-3 + specialty CRA reports; free-report entitlements; private right of action for non-delivery |
  | `consumer-credit-disputes` | Lawful direct-to-CRA disputes (§ 1681i); 4-business-day identity-theft block (§ 1681c-2); post-dispute regulator escalation |
  | `consumer-report-accuracy` | PII hygiene; Date of First Delinquency + re-aging; the "disputed by consumer" flag |
  | `consumer-harm-documentation` | Communication logs, damages ledgers, and harm declarations |
  | `consumer-credit-monitoring` | Adverse-action proof; § 1681i(d) re-notification; ongoing review |

## Why it's a plugin

The federal and model-UCC corpora live in one canonical place rather than being copy-pasted into every state plugin (`wa-court-docs`, `or-court-docs`, `ca-court-docs`, `co-court-docs`, `in-court-docs`, `ny-court-docs`, `oh-court-docs`). Because every state plugin depends on this one, the consumer credit-report-rights skills also ride along — they are available anywhere any state plugin is installed.

State plugins declare this plugin in their `plugin.json` `dependencies` array. When a user runs `/plugin install <state>-court-docs@claude-legal`, the Claude Code marketplace runtime auto-installs this plugin alongside, dereferences the symlinks each state plugin uses to point into this directory (per the Claude Code plugin spec, symlinks within a marketplace are followed and the target content is copied into the install cache), and the federal/UCC files end up locally available under each state plugin's `references/` tree at runtime.

## Refresh

The quarterly `refresh-references` GitHub Action runs `pull_federal_debt_laws.py` and `pull_ucc.py` against the paths in this plugin, then opens a PR. Federal/UCC content is now updated once per quarter instead of once per state.

## Not legal advice

The reference text is verbatim from official sources and is provided as a drafting aid. The skills produce drafting aids and checklists, not legal advice, and do not create an attorney-client relationship. Verify against the current statutes and regulations before relying on any citation in a filing.
