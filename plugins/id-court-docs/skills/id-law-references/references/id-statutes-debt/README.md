# id-statutes-debt Corpus — Idaho

> **NOT LEGAL ADVICE.** Curated digest corpus. Confirm every section and
> **especially every dollar amount** against the current Idaho Code on
> legislature.idaho.gov before relying on it.

This corpus holds **curated, topic-grouped digests** of the Idaho Code
sections most relevant to civil practice, consumer-debt defense, exemptions,
family law, and deadline arithmetic. Each file gives **citations plus a short
scope summary per section** — it is **not** a full verbatim enumeration of the
Idaho Code. **Dollar amounts are flagged "verify current figure"** because they
are revised periodically.

## Mode

- **Mode:** `curated-digest` (citation + scope summary per section; not
  verbatim).
- **Source:** Idaho Legislature — https://legislature.idaho.gov/statutesrules/idstat/
- **Puller:** a future `scripts/pull_idaho_statutes.py` will fetch verbatim
  section text from legislature.idaho.gov and may expand these digests.

## Topic files

- `Title5-limitations.md` — statutes of limitation (Title 5)
- `Title11-exemptions-garnishment.md` — exemptions and wage garnishment (Title 11)
- `homestead-Title55.md` — homestead exemption (Title 55)
- `consumer-protection-collection.md` — Idaho Consumer Protection Act, Collection Agency Act, Idaho Credit Code
- `attorney-fees-costs-Title12.md` — attorney fees and costs (Title 12)
- `family-Title32.md` — domestic relations / community property (Title 32)
- `holidays-Title73.md` — legal holidays for deadline arithmetic (Title 73)
- `ucc-article9-Title28.md` — Idaho UCC Article 9 secured transactions (Title 28)

## How it will be populated

`scripts/pull_idaho_statutes.py` will fetch the per-section pages from
`https://legislature.idaho.gov/statutesrules/idstat/title<t>/t<t>ch<c>/sect<s>/`,
extract the section body, and may replace or augment these curated digests with
verbatim text. Verify dollar figures against the live source on each refresh.
