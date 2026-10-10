# az-draft-motion — Ariz. R. Civ. P. 56 motion for summary judgment in a debt case

## Prompt

I'm representing myself in Arizona Superior Court. A debt buyer
sued me on an old credit-card account for about $9,000. Through
discovery they couldn't produce any assignment paperwork or
account statements — just a one-page "affidavit of debt." I want
to file a motion to get the case thrown out because there's no
admissible evidence they actually own this debt. How do I draft
it?

## Expected triggers

- `az-draft-motion`
- `az-statewide-format`
- `az-consumer-debt`
- `az-pro-se`

## Acceptance criteria

### Caption and title

- [ ] Caption follows the Arizona format per **Ariz. R. Civ. P. 10**
      (court, parties, case number, document title) with line
      numbering on the left margin — read current layout from
      `az-statewide-format`
- [ ] Title identifies the filing as a **Motion for Summary
      Judgment under Ariz. R. Civ. P. 56**
- [ ] Distinguishes Rule 56 (no genuine dispute of material fact
      on the evidentiary record) from a Rule 12(b)(6) motion
      (failure to state a claim on the pleadings alone) and
      explains why Rule 56 is the right vehicle when the litigant
      relies on the discovery record / evidentiary gaps

### Standard

- [ ] States the Rule 56(a) standard: summary judgment is proper
      when there is **no genuine dispute as to any material fact**
      and the movant is entitled to judgment as a matter of law;
      evidence viewed in the light most favorable to the
      non-movant
- [ ] References Arizona's articulation of the standard
      (*Orme School v. Reeves*) by citation, read/verified from
      `key-cases.md` rather than asserted from memory
- [ ] Notes the supporting/opposing-evidence and statement-of-facts
      requirements and the response/reply timing under
      **Rule 56** (cite the rule; read the current day counts from
      the references corpus rather than asserting them from memory)

### Substantive theory (az-consumer-debt)

- [ ] Frames the standing / chain-of-title defect — the plaintiff
      must prove it owns the debt through an admissible assignment
      chain from the original creditor
- [ ] Notes that a bare "affidavit of debt" may not be admissible
      business-record evidence (Ariz. R. Evid. 803(6) foundation)
      and does not by itself establish ownership; points to the
      framework in `az-statutes-debt/` rather than asserting
      elements from memory

### Composition

- [ ] References self-represented status without lawyer-speak
- [ ] Signature block per Arizona format (self-represented; no
      State Bar of Arizona number — see `az-pro-se`)

## Common failure modes

- Defaults to FRCP 56 framing instead of Ariz. R. Civ. P. 56
- Confuses Rule 56 with a Rule 12(b)(6) motion
- Asserts hard response/reply day counts as fixed facts instead
  of reading current timing from the corpus
- Invents a bar number or attorney signature block for a pro-se
  filer
