# Supreme Court of Georgia Rules (GSC)

<!-- ga-court-rules: pointer-stub -->

> **NOT LEGAL ADVICE.** Pointer stub — not verbatim. The verbatim text of the Supreme Court of Georgia Rules is published by the relevant Georgia court (uniform rules on georgiacourts.gov; appellate rules on the Supreme Court / Court of Appeals sites). This file is populated by `scripts/pull_georgia_rules.py` (which needs the optional `pypdf` dependency and network access). Until a verbatim pull lands, consult the canonical source.

_Stub reason: --stubs-only requested._

## Canonical source

- Source (HTML mirror): https://www.courtrules.net/georgia/ga-supreme-court-rules/
- Rules index: https://www.gasupreme.us/rules/

## Rules targeted for this set

22, 34, 40, 43

## How to retrieve verbatim text

```
pip3 install --break-system-packages pypdf
python3 scripts/pull_georgia_rules.py --only supreme-court-rules.md --force
```
