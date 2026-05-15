#!/usr/bin/env python3
"""
format-check.py — Ohio Civ. R. 10 + per-court local-rule
format compliance checker.

**TODO**: This is a placeholder stub. The substantive checks
need to be written for Ohio:

- Paper size: Letter (8.5 x 11)
- Margins per Ohio Civ. R. 10(A): top 1 1/2 inches on the
  first page (for caption); 1 inch sides + bottom; 1 inch
  top on subsequent pages
- Font: 12-point minimum (Sup. R. 26 + most local rules)
- Line spacing: double-spaced body (most local rules)
- Caption format per Ohio Civ. R. 10(A): court name +
  case number + plaintiff v. defendant + title of the
  document
- Signature block per Ohio Civ. R. 11: name + address +
  phone + email + Ohio Supreme Court attorney registration
  number (or "Pro Se" for self-represented filer)
- Per-court overlay: each Common Pleas court publishes its
  own local rules adding page limits, certificate-of-
  service requirements, and filing-format specifics.

Until the substantive checks are authored, this stub exits
with an informational message.
"""

import sys


def main() -> int:
    print("Ohio format-check is not yet implemented.")
    print("Authoring is in progress; see SKILL.md "
          "oh-quality-check for the format requirements "
          "this script will eventually enforce.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
