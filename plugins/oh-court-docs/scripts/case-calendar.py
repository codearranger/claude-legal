#!/usr/bin/env python3
"""
case-calendar.py — Compute Ohio court deadlines.

**TODO**: This is a placeholder stub. The substantive
deadline-arithmetic engine needs to be written for Ohio:

- FIXED_HOLIDAYS per **R.C. 1.14** (Ohio legal holidays):
  - January 1 (New Year's Day)
  - January 3rd Monday (MLK Day)
  - February 3rd Monday (Washington's Birthday)
  - May last Monday (Memorial Day)
  - June 19 (Juneteenth — added 2024)
  - July 4 (Independence Day)
  - September 1st Monday (Labor Day)
  - October 2nd Monday (Columbus Day — Ohio still observes)
  - November 11 (Veterans Day)
  - November 4th Thursday (Thanksgiving Day)
  - December 25 (Christmas Day)
- Ohio Civ. R. 6 time computation: exclude day of the
  triggering event; include the last day unless it's a
  Saturday / Sunday / legal holiday in which case roll
  forward to the next business day
- Named-rule catalog (Civ. R. and key R.C. SOLs):
  - Answer due 28 days from service (Civ. R. 12(A)(1))
  - Reply due 28 days from service (Civ. R. 12(A)(2))
  - Motion response 14 days (Civ. R. 6(C)(1)) under
    most local rules; verify per-court
  - Civ. R. 56 summary-judgment notice 14 days minimum
  - R.C. 2305.06 SOL: 6 years on written contract
  - R.C. 2305.07 SOL: 4 years on oral / implied contract
  - R.C. 2305.09 SOL: 4 years on conversion / fraud
  - R.C. 2305.10 SOL: 2 years on personal injury
  - R.C. 2305.11 SOL: 1 year on libel / slander
  - R.C. 1345.10 SOL: 2 years on CSPA claims
  - R.C. 2329.07 SOL: 5 years on judgment-enforcement

Until the substantive arithmetic is authored, this stub
exits with an informational message.
"""

import sys


def main() -> int:
    print("Ohio case-calendar is not yet implemented.")
    print("Authoring is in progress; see SKILL.md "
          "oh-deadlines for the named deadlines this "
          "script will eventually compute.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
