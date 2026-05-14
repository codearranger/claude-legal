#!/usr/bin/env python3
"""Pull selected debt-relevant California statutory chapters from
leginfo.legislature.ca.gov and convert to MD.

Output: plugins/ca-court-docs/skills/ca-law-references/references/ca-statutes-debt/
One MD file per topic, each section as its own heading inside.

Modeled on scripts/pull_wa_rcw.py. The CA target is the
California Legislative Information bulk codes view at
leginfo.legislature.ca.gov.

URL patterns used:

  - Expanded branch (chapter / article TOC):
    https://leginfo.legislature.ca.gov/faces/codes_displayexpandedbranch.xhtml?tocCode=<CODE>&division=...&title=...&part=...&chapter=...&article=...

  - Single section:
    https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=<CODE>&sectionNum=<NUM>.

Codes referenced here:

  - CCP  — Code of Civil Procedure
  - CIV  — Civil Code
  - BPC  — Business and Professions Code
  - FIN  — Financial Code
  - COM  — Commercial Code

NOTE: leginfo's HTML is JSF (JavaServer Faces) with view-state
tokens. This puller uses the public displaySection endpoint which
serves a stable HTML body for each section. If the site changes
its URL or HTML scheme, update the SECTION_URL / parser below.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path

USER_AGENT = (
    "claude-legal/1.0 (+https://github.com/codearranger/claude-legal) "
    "ca-statutes-puller"
)
BASE = "https://leginfo.legislature.ca.gov"
SECTION_URL = (
    BASE
    + "/faces/codes_displaySection.xhtml?lawCode={code}&sectionNum={section}."
)
RANGE_URL = (
    BASE
    + "/faces/codes_displayText.xhtml?lawCode={code}&division=&title="
    "&part=&chapter=&article=&sectionNum={section}."
)


# ---- Configuration: which sections to pull, grouped by output file ------------
#
# Each entry maps an OUTPUT FILE in ca-statutes-debt/ to a list of sections
# to fetch. Sections are tuples of (code, section_number, label).
#
# Section numbers must exactly match the lookup format on leginfo. For
# California, many codes have section numbers with embedded dots (e.g.,
# "1788.30" for Cal. Civ. Code § 1788.30); preserve them as strings.
#
# To add coverage:
#   1. Append a new (code, section, label) tuple to the relevant FILE entry,
#      OR add a new FILE entry mapping output filename → section list
#   2. Re-run the puller
#
# These groupings mirror the topic-organized files already authored in
# ca-statutes-debt/, so the puller will incrementally enrich them with
# verbatim text from leginfo.

CCP_SOL = [
    ("CCP", "312",   "General SOL rule"),
    ("CCP", "313",   "Acquired rights"),
    ("CCP", "318",   "Real property — 5 years"),
    ("CCP", "335.1", "Personal injury — 2 years"),
    ("CCP", "337",   "Written contract / book account — 4 years"),
    ("CCP", "338",   "3-year actions; fraud/mistake discovery rule"),
    ("CCP", "339",   "Oral contract — 2 years"),
    ("CCP", "340",   "1-year actions"),
    ("CCP", "343",   "Catch-all — 4 years"),
    ("CCP", "360",   "Revival by acknowledgment / partial payment"),
    ("CCP", "361",   "Borrowing statute"),
    ("CCP", "366.2", "Action against decedent"),
]

CCP_TIME = [
    ("CCP", "12",    "Time computation — general rule"),
    ("CCP", "12a",   "Holidays — extension of period"),
    ("CCP", "12b",   "Half-holidays"),
    ("CCP", "12c",   "Court day defined"),
    ("CCP", "13",    "Single-day computation"),
    ("CCP", "135",   "Judicial holidays"),
]

CCP_SERVICE = [
    ("CCP", "412.10",  "Manner of service"),
    ("CCP", "412.20",  "Form of summons; 30-day answer"),
    ("CCP", "415.10",  "Personal service"),
    ("CCP", "415.20",  "Substituted service"),
    ("CCP", "415.30",  "Service by mail with NORF"),
    ("CCP", "415.40",  "Out-of-state service"),
    ("CCP", "415.50",  "Service by publication"),
    ("CCP", "416.10",  "Service on corporation"),
    ("CCP", "416.20",  "Service on partnership"),
    ("CCP", "417.10",  "Proof of service"),
    ("CCP", "417.20",  "Proof — service on entity"),
]

CCP_PLEADINGS = [
    ("CCP", "425.10",  "Required contents of complaint"),
    ("CCP", "425.11",  "Personal-injury statement of damages"),
    ("CCP", "425.16",  "Anti-SLAPP"),
    ("CCP", "426.10",  "Cross-complaints — definitions"),
    ("CCP", "426.30",  "Compulsory cross-complaint"),
    ("CCP", "428.10",  "Permissive cross-complaint"),
    ("CCP", "430.10",  "Grounds for demurrer"),
    ("CCP", "430.20",  "Grounds for demurrer to answer"),
    ("CCP", "430.30",  "Face-of-pleading rule"),
    ("CCP", "430.40",  "Time for demurrer"),
    ("CCP", "430.41",  "Meet-and-confer for demurrer"),
    ("CCP", "430.50",  "Demurrer to part of cause of action"),
    ("CCP", "431.30",  "Form of answer; verification"),
    ("CCP", "431.40",  "Verification by entity attorney"),
    ("CCP", "431.70",  "Setoff"),
    ("CCP", "435",     "Notice of motion to strike"),
    ("CCP", "435.5",   "Meet-and-confer for motion to strike"),
    ("CCP", "436",     "Authority of court to strike"),
    ("CCP", "437",     "Court rules and orders"),
    ("CCP", "437c",    "Summary judgment"),
    ("CCP", "438",     "Motion for judgment on pleadings"),
]

CCP_MOTIONS = [
    ("CCP", "1005",    "Motion notice / service / time"),
    ("CCP", "1010",    "Notice of motion — contents"),
    ("CCP", "1010.6",  "Electronic service"),
    ("CCP", "1011",    "Personal service of papers"),
    ("CCP", "1012",    "Service by mail"),
    ("CCP", "1013",    "Mail service extension"),
    ("CCP", "1013a",   "Proof of service by mail"),
    ("CCP", "1014",    "Appearance defined"),
    ("CCP", "1015",    "Other notices"),
    ("CCP", "1019",    "Filing of papers"),
    ("CCP", "1020",    "Service / filing acknowledgments"),
]

CCP_DISCOVERY = [
    ("CCP", "2017.010", "Scope of discovery"),
    ("CCP", "2023.030", "Sanctions"),
    ("CCP", "2024.020", "Trial-date cutoffs"),
    ("CCP", "2025.270", "Deposition notice — time"),
    ("CCP", "2025.450", "Motion to compel attendance"),
    ("CCP", "2030.010", "Right to propound interrogatories"),
    ("CCP", "2030.030", "35-special-interrogatory cap"),
    ("CCP", "2030.040", "Declaration of necessity for additional"),
    ("CCP", "2030.050", "Required declaration of necessity"),
    ("CCP", "2030.060", "Form of interrogatories"),
    ("CCP", "2030.260", "Time to respond"),
    ("CCP", "2030.300", "Motion to compel further (rogs)"),
    ("CCP", "2031.010", "Right to demand inspection"),
    ("CCP", "2031.260", "Time to respond to RFP"),
    ("CCP", "2031.310", "Motion to compel further (RFPs)"),
    ("CCP", "2031.320", "Failure to comply with compel order"),
    ("CCP", "2033.010", "Right to request admission"),
    ("CCP", "2033.030", "35-RFA cap (non-genuineness)"),
    ("CCP", "2033.250", "Time to respond to RFA"),
    ("CCP", "2033.280", "Failure to respond — deemed admitted"),
    ("CCP", "2033.290", "Motion to compel further (RFAs)"),
]

CCP_RELIEF = [
    ("CCP", "473",   "Relief from default — discretionary + mandatory"),
    ("CCP", "473.5", "Set aside default when no actual notice"),
]

CCP_ENFORCEMENT = [
    ("CCP", "683.020",  "10-year judgment life"),
    ("CCP", "683.110",  "Renewal of judgment"),
    ("CCP", "683.130",  "Renewal procedure"),
    ("CCP", "683.140",  "Effect of renewal"),
    ("CCP", "685.010",  "Post-judgment costs"),
    ("CCP", "685.030",  "Post-judgment costs added to judgment"),
    ("CCP", "697.310",  "Judgment lien on real property"),
    ("CCP", "697.510",  "Judgment lien on personal property"),
    ("CCP", "697.060",  "Duration of lien"),
    ("CCP", "699.510",  "Writ of execution"),
    ("CCP", "700.010",  "Levying officer"),
    ("CCP", "700.140",  "Levy on deposit accounts"),
    ("CCP", "706.010",  "Wage garnishment — application"),
    ("CCP", "706.022",  "Earnings withholding order"),
    ("CCP", "706.029",  "Priority"),
    ("CCP", "706.050",  "Withholding amount"),
    ("CCP", "706.105",  "Claim of exemption procedure"),
    ("CCP", "708.110",  "Judgment debtor exam"),
    ("CCP", "708.120",  "Third-party exam"),
    ("CCP", "708.170",  "Failure to appear"),
    ("CCP", "708.205",  "Turnover order"),
    ("CCP", "708.510",  "Assignment of rights to payment"),
    ("CCP", "708.610",  "Appointment of receiver"),
    ("CCP", "724.010",  "Acknowledgment of satisfaction"),
    ("CCP", "724.030",  "Filing acknowledgment"),
    ("CCP", "724.050",  "Demand for acknowledgment"),
    ("CCP", "724.080",  "Penalty for failure"),
    ("CCP", "724.110",  "Demand for acknowledgment with payment"),
    ("CCP", "918",      "Stay pending appeal"),
]

CCP_EXEMPTIONS = [
    ("CCP", "703.140", "Bankruptcy-style exemptions"),
    ("CCP", "703.520", "Claim of exemption — notice"),
    ("CCP", "703.530", "Levying officer's response"),
    ("CCP", "703.550", "Judgment creditor's response"),
    ("CCP", "703.580", "Hearing"),
    ("CCP", "704.010", "Motor vehicle"),
    ("CCP", "704.020", "Household goods"),
    ("CCP", "704.030", "Jewelry, heirlooms, art"),
    ("CCP", "704.040", "Health and safety items"),
    ("CCP", "704.060", "Tools of trade"),
    ("CCP", "704.070", "Paid earnings"),
    ("CCP", "704.080", "Deposit account"),
    ("CCP", "704.090", "Public benefits"),
    ("CCP", "704.100", "Life insurance"),
    ("CCP", "704.110", "Retirement"),
    ("CCP", "704.115", "Self-settled IRAs"),
    ("CCP", "704.140", "Personal injury recoveries"),
    ("CCP", "704.170", "Cemetery property"),
    ("CCP", "704.180", "Crime-victim compensation"),
    ("CCP", "704.710", "Homestead — definitions"),
    ("CCP", "704.720", "Automatic homestead exemption"),
    ("CCP", "704.730", "Homestead amount (AB 1885)"),
    ("CCP", "704.780", "Declaration of homestead"),
]

CIV_ROSENTHAL = [
    ("CIV", "1788",      "Title"),
    ("CIV", "1788.1",    "Findings"),
    ("CIV", "1788.2",    "Definitions"),
    ("CIV", "1788.10",   "Threats and use of force"),
    ("CIV", "1788.11",   "Communication frequency / pretense"),
    ("CIV", "1788.12",   "Communication with workplace / others"),
    ("CIV", "1788.13",   "False or misleading representations"),
    ("CIV", "1788.14",   "Specific abusive practices"),
    ("CIV", "1788.15",   "Litigation against debtor"),
    ("CIV", "1788.16",   "Postdated checks"),
    ("CIV", "1788.17",   "FDCPA incorporation"),
    ("CIV", "1788.18",   "Identity theft"),
    ("CIV", "1788.30",   "Remedies and damages"),
    ("CIV", "1788.32",   "Cumulative remedies"),
    ("CIV", "1788.33",   "Severability"),
]

CIV_FDBPA = [
    ("CIV", "1788.50",  "Definitions"),
    ("CIV", "1788.52",  "Pre-collection requirements"),
    ("CIV", "1788.58",  "Complaint requirements"),
    ("CIV", "1788.59",  "Requests for documentation"),
    ("CIV", "1788.60",  "Default judgment requirements"),
    ("CIV", "1788.61",  "Notice of sale of debt"),
    ("CIV", "1788.62",  "Remedies and damages"),
    ("CIV", "1788.63",  "Cumulative remedies"),
    ("CIV", "1788.65",  "Severability"),
    ("CIV", "1788.66",  "Effective date"),
]

CIV_CLRA = [
    ("CIV", "1750",   "Title and purpose"),
    ("CIV", "1761",   "Definitions"),
    ("CIV", "1770",   "Prohibited practices (24 enumerated)"),
    ("CIV", "1780",   "Remedies"),
    ("CIV", "1781",   "Class actions"),
    ("CIV", "1782",   "Pre-suit notice"),
    ("CIV", "1783",   "Statute of limitations"),
    ("CIV", "1784",   "Effect on existing rights"),
]

CIV_ATTY_FEES = [
    ("CIV", "1717",   "Reciprocal attorney's fees"),
    ("CIV", "1717.5", "Pleading requirements"),
]

BPC_UCL = [
    ("BPC", "17200",   "Unfair competition defined"),
    ("BPC", "17201",   "Person defined"),
    ("BPC", "17203",   "Remedies"),
    ("BPC", "17204",   "Standing"),
    ("BPC", "17205",   "Cumulative remedies"),
    ("BPC", "17206",   "Civil penalties (AG)"),
    ("BPC", "17208",   "Statute of limitations"),
    ("BPC", "17500",   "False advertising — prohibition"),
]

FIN_CDCLA = [
    ("FIN", "100000",  "Title"),
    ("FIN", "100001",  "Definitions"),
    ("FIN", "100002",  "License requirement"),
    ("FIN", "100003",  "Exemptions"),
    ("FIN", "100005",  "License application"),
    ("FIN", "100007",  "Surety bond"),
    ("FIN", "100008",  "Denial / suspension / revocation"),
    ("FIN", "100010",  "Renewal"),
    ("FIN", "100012",  "Continuing education"),
    ("FIN", "100015",  "Examination and supervision"),
    ("FIN", "100018",  "Rosenthal Act incorporation"),
    ("FIN", "100020",  "Enforcement"),
    ("FIN", "100027",  "Effective date"),
]

COM_ART2 = [
    ("COM", "2102",   "Scope"),
    ("COM", "2105",   "Definitions — goods"),
    ("COM", "2201",   "Statute of frauds"),
    ("COM", "2204",   "Formation in general"),
    ("COM", "2207",   "Battle of the forms"),
    ("COM", "2313",   "Express warranties"),
    ("COM", "2314",   "Implied warranty: merchantability"),
    ("COM", "2315",   "Implied warranty: fitness for purpose"),
    ("COM", "2316",   "Exclusion / modification of warranties"),
    ("COM", "2503",   "Tender of delivery"),
    ("COM", "2601",   "Buyer's rights upon nonconforming tender"),
    ("COM", "2607",   "Notice of breach"),
    ("COM", "2703",   "Seller's remedies"),
    ("COM", "2711",   "Buyer's remedies"),
    ("COM", "2715",   "Incidental and consequential damages"),
    ("COM", "2719",   "Contractual modification / limitation"),
    ("COM", "2725",   "Statute of limitations — 4 years"),
]

COM_ART3 = [
    ("COM", "3102",   "Scope"),
    ("COM", "3104",   "Negotiable instrument defined"),
    ("COM", "3301",   "Person entitled to enforce"),
    ("COM", "3302",   "Holder in due course"),
    ("COM", "3305",   "Defenses against person entitled to enforce"),
    ("COM", "3308",   "Proof of signatures / status"),
    ("COM", "3309",   "Lost / destroyed / stolen instrument"),
    ("COM", "3118",   "Statute of limitations"),
]

COM_ART9 = [
    ("COM", "9101",   "Short title"),
    ("COM", "9102",   "Definitions"),
    ("COM", "9203",   "Attachment"),
    ("COM", "9310",   "Perfection by filing"),
    ("COM", "9404",   "Rights acquired by assignee"),
    ("COM", "9406",   "Discharge of account debtor"),
    ("COM", "9601",   "Rights after default"),
    ("COM", "9610",   "Disposition of collateral"),
    ("COM", "9611",   "Notification before disposition"),
    ("COM", "9615",   "Application of proceeds"),
    ("COM", "9626",   "Burden of proof — commercial reasonableness"),
]

# ---- Civil-practice expansion (Phase 5) -------------------------------
# New groups covering civil-practice topics beyond the original
# debt-collection scope: contract formation/damages, consumer warranties,
# trial-conduct motions, writs, unlawful detainer, family law, probate,
# and labor-wages enforcement.

CCP_TRIAL_NEW = [
    # New trial / JNOV / vacate-after-judgment
    ("CCP", "657",    "Grounds for new trial"),
    ("CCP", "658",    "Time to move for new trial"),
    ("CCP", "659",    "Notice of intention to move"),
    ("CCP", "659a",   "Time to file affidavits"),
    ("CCP", "660",    "Hearing on motion; time to rule"),
    ("CCP", "660.5",  "Effect of failure to rule"),
    ("CCP", "662",    "Trial-court alternatives in lieu of new trial"),
    ("CCP", "662.5",  "Conditional new-trial order"),
    ("CCP", "663",    "Motion to vacate judgment"),
    ("CCP", "663a",   "Time to move to vacate"),
]

CCP_WRITS = [
    ("CCP", "1085",   "Writ of mandate — issuance"),
    ("CCP", "1086",   "Mandamus by interested party"),
    ("CCP", "1087",   "Form / contents of writ"),
    ("CCP", "1088",   "Alternative writ vs. peremptory"),
    ("CCP", "1089",   "Answer and reply"),
    ("CCP", "1090",   "Trial on issues of fact"),
    ("CCP", "1094",   "Costs"),
    ("CCP", "1094.5", "Administrative mandamus — review of agency decisions"),
    ("CCP", "1094.6", "90-day SOL for admin mandamus"),
    ("CCP", "1095",   "Prohibition writ"),
    ("CCP", "1097",   "Contempt for disobedience"),
]

CCP_UNLAWFUL_DETAINER = [
    ("CCP", "1159",   "Forcible entry defined"),
    ("CCP", "1161",   "Unlawful detainer — grounds and notice periods"),
    ("CCP", "1161.1", "Pre-judgment notice — commercial"),
    ("CCP", "1161.2", "Sealed records pending judgment"),
    ("CCP", "1162",   "Service of notice to quit"),
    ("CCP", "1166",   "Complaint — required allegations"),
    ("CCP", "1167",   "Summons — 5-day response"),
    ("CCP", "1170",   "Answer and verification"),
    ("CCP", "1170.5", "Trial setting — 20-day rule"),
    ("CCP", "1170.7", "Summary judgment in UD actions"),
    ("CCP", "1171",   "Set-off / counterclaim limits"),
    ("CCP", "1174",   "Judgment for plaintiff"),
    ("CCP", "1179",   "Relief from forfeiture"),
]

CCP_ARBITRATION = [
    # California Arbitration Act
    ("CCP", "1280",   "Definitions"),
    ("CCP", "1281",   "Validity of agreement"),
    ("CCP", "1281.2", "Petition to compel arbitration; defenses"),
    ("CCP", "1281.4", "Stay of court action pending arbitration"),
    ("CCP", "1281.6", "Selection of arbitrator"),
    ("CCP", "1281.91", "Arbitrator disqualification — disclosures"),
    ("CCP", "1281.97", "Forfeiture for non-payment of fees (consumer/employment)"),
    ("CCP", "1281.98", "Employer fee-payment timing"),
    ("CCP", "1282.2", "Conduct of hearing"),
    ("CCP", "1283.05", "Discovery in arbitration"),
    ("CCP", "1284.2", "Allocation of arbitration costs"),
    ("CCP", "1285",   "Petition to confirm award"),
    ("CCP", "1286.2", "Grounds to vacate award"),
    ("CCP", "1286.6", "Grounds to correct award"),
    ("CCP", "1294",   "Appealable orders"),
    ("CCP", "1294.2", "Stay pending appeal"),
]

CIV_CONTRACTS = [
    # General contract formation and interpretation
    ("CIV", "1549",   "Definition of contract"),
    ("CIV", "1550",   "Essential elements"),
    ("CIV", "1556",   "Who may contract"),
    ("CIV", "1565",   "Mutual consent essentials"),
    ("CIV", "1568",   "Apparent consent"),
    ("CIV", "1571",   "Fraud — types"),
    ("CIV", "1572",   "Actual fraud"),
    ("CIV", "1573",   "Constructive fraud"),
    ("CIV", "1605",   "Consideration defined"),
    ("CIV", "1622",   "Oral contracts valid except as noted"),
    ("CIV", "1624",   "Statute of frauds — writings required"),
    ("CIV", "1636",   "Interpretation goal"),
    ("CIV", "1638",   "Plain meaning"),
    ("CIV", "1639",   "Reduced to writing"),
    ("CIV", "1641",   "Whole-contract reading"),
    ("CIV", "1644",   "Ordinary meaning"),
    ("CIV", "1647",   "Circumstances considered"),
    ("CIV", "1654",   "Ambiguity construed against drafter"),
    ("CIV", "1668",   "Contracts exempting fraud / willful injury are void"),
    ("CIV", "1670.5", "Unconscionability"),
    ("CIV", "1689",   "Rescission grounds"),
    ("CIV", "1691",   "Rescission procedure"),
    ("CIV", "1692",   "Restoration on rescission"),
]

CIV_DAMAGES = [
    # Damages framework — Civ Code §§ 3274-3361
    ("CIV", "3274",   "Damages — general"),
    ("CIV", "3281",   "Damages defined"),
    ("CIV", "3282",   "Detriment defined"),
    ("CIV", "3283",   "Detriment includes future losses"),
    ("CIV", "3287",   "Prejudgment interest on liquidated damages"),
    ("CIV", "3288",   "Discretionary interest in tort"),
    ("CIV", "3289",   "Interest on contract obligations"),
    ("CIV", "3294",   "Punitive damages — fraud / malice / oppression"),
    ("CIV", "3300",   "Contract damages — general"),
    ("CIV", "3301",   "Contract damages — certainty"),
    ("CIV", "3302",   "Money paid as damages"),
    ("CIV", "3306",   "Real-property contract damages"),
    ("CIV", "3333",   "Tort damages — proximate cause"),
    ("CIV", "3333.2", "Cap on noneconomic medmal damages"),
    ("CIV", "3334",   "Wrongful occupation damages"),
    ("CIV", "3343",   "Fraud damages — out of pocket"),
    ("CIV", "3358",   "Mitigation"),
    ("CIV", "3359",   "Reasonable damages"),
]

CIV_SONG_BEVERLY = [
    # Song-Beverly Consumer Warranty Act
    ("CIV", "1790",     "Findings and policy"),
    ("CIV", "1791",     "Consumer goods defined"),
    ("CIV", "1791.1",   "Implied warranty defined"),
    ("CIV", "1791.2",   "Express warranty defined"),
    ("CIV", "1792",     "Implied warranty of merchantability"),
    ("CIV", "1792.1",   "Implied warranty of fitness"),
    ("CIV", "1792.2",   "Used goods"),
    ("CIV", "1792.4",   "Disclaimer of implied warranty"),
    ("CIV", "1793",     "Duration of implied warranty"),
    ("CIV", "1793.2",   "Manufacturer service / repair obligations"),
    ("CIV", "1793.22",  "Lemon law presumption (Tanner Consumer Protection Act)"),
    ("CIV", "1793.25",  "Reimbursement to manufacturer"),
    ("CIV", "1793.3",   "Repair facilities"),
    ("CIV", "1794",     "Remedies for breach"),
    ("CIV", "1794.4",   "Service contract requirements"),
    ("CIV", "1795",     "Implied warranties for new and used goods"),
    ("CIV", "1795.5",   "Used goods — implied warranty 30 days"),
    ("CIV", "1795.6",   "Toll of warranty period during repair"),
    ("CIV", "1795.7",   "Buyer's right to demand replacement"),
    ("CIV", "1795.8",   "Mobile homes excluded"),
]

EVID_KEY = [
    # Core Evidence Code provisions for civil practice
    ("EVID", "350",   "Relevance — only relevant evidence admissible"),
    ("EVID", "351",   "All relevant evidence admissible"),
    ("EVID", "352",   "Discretionary exclusion (prejudice)"),
    ("EVID", "353",   "Erroneous admission"),
    ("EVID", "354",   "Erroneous exclusion"),
    ("EVID", "400",   "Proof of preliminary fact"),
    ("EVID", "402",   "Procedure for determining preliminary fact"),
    ("EVID", "403",   "Conditional relevance"),
    ("EVID", "452",   "Permissive judicial notice"),
    ("EVID", "452.5", "Certified record judicial notice"),
    ("EVID", "453",   "Mandatory judicial notice"),
    ("EVID", "459",   "Reviewing court — judicial notice"),
    ("EVID", "702",   "Personal knowledge required"),
    ("EVID", "720",   "Expert qualification"),
    ("EVID", "1200",  "Hearsay defined"),
    ("EVID", "1220",  "Party admission"),
    ("EVID", "1222",  "Authorized admission"),
    ("EVID", "1224",  "Statement of co-conspirator"),
    ("EVID", "1271",  "Business records exception"),
    ("EVID", "1280",  "Public records exception"),
    ("EVID", "1400",  "Authentication required"),
    ("EVID", "1401",  "Authentication generally"),
    ("EVID", "1410",  "Methods of authentication"),
    ("EVID", "1411",  "Other methods not excluded"),
    ("EVID", "1500",  "Best evidence — content of writing"),
    ("EVID", "1521",  "Secondary evidence — original required if dispute"),
]

# ---- Family Code -------------------------------------------------------

FAM_DISSOLUTION = [
    # Dissolution / nullity / legal separation
    ("FAM", "2310",   "Grounds for dissolution"),
    ("FAM", "2311",   "Irreconcilable differences"),
    ("FAM", "2320",   "6-month + 3-month residency"),
    ("FAM", "2330",   "Petition — contents"),
    ("FAM", "2335",   "Misnomer not a defense"),
    ("FAM", "2336",   "Default — judgment requirements"),
    ("FAM", "2337",   "Termination of marital status; reserving jurisdiction"),
    ("FAM", "2339",   "6-month waiting period; effective date"),
    ("FAM", "2340",   "Effect on insurance, beneficiary"),
    ("FAM", "2400",   "Summary dissolution — eligibility"),
    ("FAM", "2401",   "Joint petition"),
    ("FAM", "2403",   "Effect of judgment"),
]

FAM_PROPERTY = [
    # Community property characterization and division
    ("FAM", "760",    "Community property defined"),
    ("FAM", "770",    "Separate property of married person"),
    ("FAM", "771",    "Earnings after separation"),
    ("FAM", "780",    "Joint-tenancy presumption"),
    ("FAM", "850",    "Transmutation — general rule"),
    ("FAM", "851",    "Transmutation in writing"),
    ("FAM", "852",    "Transmutation requirements"),
    ("FAM", "2550",   "Equal division — mandate"),
    ("FAM", "2552",   "Valuation date"),
    ("FAM", "2581",   "Joint-form-title presumption"),
    ("FAM", "2622",   "Liabilities at dissolution"),
    ("FAM", "2640",   "Reimbursement for separate-property contributions"),
    ("FAM", "2641",   "Educational reimbursement"),
]

FAM_CUSTODY = [
    # Custody and visitation
    ("FAM", "3010",   "Equal status of parents"),
    ("FAM", "3011",   "Best interest factors"),
    ("FAM", "3020",   "Public policy"),
    ("FAM", "3040",   "Custody preferences and presumptions"),
    ("FAM", "3041",   "Award to non-parent"),
    ("FAM", "3042",   "Child's preference"),
    ("FAM", "3044",   "Domestic-violence presumption"),
    ("FAM", "3046",   "Absence not a factor against"),
    ("FAM", "3080",   "Joint-custody presumption when stipulated"),
    ("FAM", "3082",   "Findings required if denied"),
    ("FAM", "3083",   "Joint legal custody"),
    ("FAM", "3084",   "Joint physical custody"),
    ("FAM", "3088",   "Modification with child's consent"),
    ("FAM", "3100",   "Visitation — non-custodial parent"),
    ("FAM", "3110",   "Court-appointed counsel for child"),
    ("FAM", "3200",   "UCCJEA — citation"),
]

FAM_SUPPORT = [
    # Child support
    ("FAM", "4050",   "Statewide uniform guideline"),
    ("FAM", "4053",   "Principles of guideline"),
    ("FAM", "4055",   "Statewide formula"),
    ("FAM", "4057",   "Rebuttal of guideline"),
    ("FAM", "4058",   "Annual gross income"),
    ("FAM", "4059",   "Net disposable income"),
    ("FAM", "4060",   "Net disposable income — adjustments"),
    ("FAM", "4061",   "Adjustments for prior support"),
    ("FAM", "4062",   "Add-ons — mandatory and discretionary"),
    ("FAM", "4063",   "Documentation"),
    ("FAM", "4064",   "Seasonal or fluctuating income"),
    ("FAM", "4065",   "Stipulated support — child waiver limited"),
    ("FAM", "4068",   "Order for hardship"),
    ("FAM", "4070",   "Imputation of income"),
    ("FAM", "4071",   "Hardship deductions"),
    ("FAM", "4076",   "Form orders"),
]

# ---- Probate Code ------------------------------------------------------

PROB_BASICS = [
    # Intestate succession + general probate procedure
    ("PROB", "6400",  "Property subject to intestate distribution"),
    ("PROB", "6401",  "Surviving spouse share"),
    ("PROB", "6402",  "Other heirs — order"),
    ("PROB", "6402.5", "Predeceased spouse property"),
    ("PROB", "6403",  "Survivorship requirement"),
    ("PROB", "6404",  "Escheat to state"),
    ("PROB", "8000",  "Petition for probate"),
    ("PROB", "8002",  "Contents of petition"),
    ("PROB", "8003",  "Hearing date"),
    ("PROB", "8004",  "Filing fee"),
    ("PROB", "8005",  "Bond"),
    ("PROB", "8120",  "Notice of hearing"),
    ("PROB", "8121",  "Manner of service"),
    ("PROB", "8200",  "Will — proof"),
    ("PROB", "8222",  "Will — petition to admit"),
    ("PROB", "8250",  "Self-proving will"),
    ("PROB", "8270",  "Lost or destroyed will"),
    ("PROB", "8400",  "Issuance of letters"),
    ("PROB", "8540",  "Removal of personal representative"),
    ("PROB", "13100", "Small-estate affidavit — under $184,500"),
    ("PROB", "13150", "Real-property small-estate procedure"),
]

# ---- Labor Code (wage payment / collection) ----------------------------

LAB_WAGES = [
    # Wage payment and collection
    ("LAB", "200",    "Wages defined"),
    ("LAB", "201",    "Wages due immediately on discharge"),
    ("LAB", "202",    "Wages due on quit"),
    ("LAB", "203",    "Waiting-time penalty"),
    ("LAB", "204",    "Pay periods"),
    ("LAB", "205.5",  "Tip pooling"),
    ("LAB", "206",    "Undisputed portion of wages"),
    ("LAB", "206.5",  "No release as condition of payment"),
    ("LAB", "210",    "Civil penalties for late payment"),
    ("LAB", "212",    "Payment by check / direct deposit"),
    ("LAB", "218",    "Right to sue without labor commissioner"),
    ("LAB", "218.5",  "Attorney fees in wage actions"),
    ("LAB", "218.6",  "Prejudgment interest"),
    ("LAB", "221",    "Kickback on wages prohibited"),
    ("LAB", "224",    "Wage deductions"),
    ("LAB", "226",    "Itemized wage statement"),
    ("LAB", "226.7",  "Meal/rest premium"),
    ("LAB", "227.3",  "Vacation as wages"),
    ("LAB", "230",    "Anti-retaliation — protected absences"),
    ("LAB", "232",    "Wage disclosure protection"),
    ("LAB", "244",    "Exhaustion of administrative remedy"),
]


# (output_file_stem, description, sections) — drives main() iteration
FILES: list[tuple[str, str, list[tuple[str, str, str]]]] = [
    ("CCP-Time-Computation",       "Time computation (CCP §§ 12-13)",                  CCP_TIME),
    ("CCP-SOL",                    "Statutes of limitation (CCP §§ 312-366)",          CCP_SOL),
    ("CCP-Service",                "Service of summons (CCP §§ 412.10-417.40)",        CCP_SERVICE),
    ("CCP-Pleadings",              "Pleadings, demurrer, MSJ (CCP §§ 425.10-440)",     CCP_PLEADINGS),
    ("CCP-Motions-1005-to-1020",   "Motion practice (CCP §§ 1005-1020)",               CCP_MOTIONS),
    ("CCP-Discovery",              "Civil Discovery Act (CCP §§ 2016.010-2036.050)",   CCP_DISCOVERY),
    ("CCP-Relief-473",             "Relief from default (CCP §§ 473-473.5)",           CCP_RELIEF),
    ("CCP-Enforcement",            "Enforcement of judgments (CCP §§ 683-708)",        CCP_ENFORCEMENT),
    ("CCP-Exemptions",             "Exemptions (CCP §§ 703.140 + 704.010-995)",        CCP_EXEMPTIONS),
    ("CivCode-Rosenthal",          "Rosenthal Act (Civ. Code §§ 1788-1788.33)",        CIV_ROSENTHAL),
    ("CivCode-FDBPA",              "FDBPA (Civ. Code §§ 1788.50-1788.66)",             CIV_FDBPA),
    ("CivCode-CLRA",               "CLRA (Civ. Code §§ 1750-1784)",                    CIV_CLRA),
    ("CivCode-Atty-Fees",          "Reciprocal fees (Civ. Code § 1717)",               CIV_ATTY_FEES),
    ("BPC-UCL",                    "UCL + FAL (B&P §§ 17200-17210, § 17500)",          BPC_UCL),
    ("FinCode-CDCLA",              "CDCLA (Fin. Code §§ 100000-100027)",               FIN_CDCLA),
    ("CommCode-Art-2-Sales",       "UCC Art. 2 (Cal. Comm. Code §§ 2101-2725)",        COM_ART2),
    ("CommCode-Art-3-Negotiable",  "UCC Art. 3 (Cal. Comm. Code §§ 3101-3605)",        COM_ART3),
    ("CommCode-Art-9-Secured",     "UCC Art. 9 (Cal. Comm. Code §§ 9101-9809)",        COM_ART9),
    # Phase 5 civil-practice expansion
    ("CCP-Trial-New-JNOV",         "New trial / JNOV / vacate (CCP §§ 657-663a)",      CCP_TRIAL_NEW),
    ("CCP-Writs",                  "Mandamus and writs (CCP §§ 1085-1097)",            CCP_WRITS),
    ("CCP-Unlawful-Detainer",      "Unlawful detainer (CCP §§ 1159-1179)",             CCP_UNLAWFUL_DETAINER),
    ("CCP-Arbitration",            "California Arbitration Act (CCP §§ 1280-1294.2)",  CCP_ARBITRATION),
    ("CivCode-Contracts",          "Contract formation (Civ. Code §§ 1549-1692)",      CIV_CONTRACTS),
    ("CivCode-Damages",            "Damages framework (Civ. Code §§ 3274-3359)",       CIV_DAMAGES),
    ("CivCode-Song-Beverly",       "Song-Beverly Warranty Act (Civ. Code §§ 1790-1795.8)", CIV_SONG_BEVERLY),
    ("EvidCode-Key",               "Evidence Code — relevance / hearsay / authentication / best evidence", EVID_KEY),
    ("FamCode-Dissolution",        "Dissolution / nullity / legal separation (Fam. Code §§ 2310-2403)", FAM_DISSOLUTION),
    ("FamCode-Property",           "Community property (Fam. Code §§ 760-2641)",       FAM_PROPERTY),
    ("FamCode-Custody",            "Custody and visitation (Fam. Code §§ 3010-3200)",  FAM_CUSTODY),
    ("FamCode-Support",            "Child support guidelines (Fam. Code §§ 4050-4076)", FAM_SUPPORT),
    ("ProbCode-Basics",            "Intestate succession + probate procedure (Prob. Code §§ 6400-13150)", PROB_BASICS),
    ("LabCode-Wages",              "Wage payment and collection (Lab. Code §§ 200-244)", LAB_WAGES),
]


# ---- Networking ---------------------------------------------------------------

def http_get(url: str, *, retries: int = 3, sleep: float = 1.5) -> bytes:
    parsed = urllib.parse.urlsplit(url)
    safe_path = urllib.parse.quote(parsed.path, safe="/%")
    safe_url = urllib.parse.urlunsplit(
        (parsed.scheme, parsed.netloc, safe_path, parsed.query, parsed.fragment)
    )
    req = urllib.request.Request(safe_url, headers={"User-Agent": USER_AGENT})
    last_exc: Exception | None = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:
            last_exc = e
            time.sleep(sleep * (2**attempt))
    assert last_exc is not None
    raise last_exc


# ---- HTML → text --------------------------------------------------------------

def html_to_text(s: str) -> str:
    """Convert HTML fragment to plain text with paragraph breaks at
    div/p/br boundaries. Mirrors the WA puller's approach."""
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", s, flags=re.IGNORECASE | re.DOTALL)
    s = re.sub(r"<(em|i)[^>]*>(.*?)</\1>", lambda m: f"*{m.group(2)}*", s, flags=re.IGNORECASE | re.DOTALL)
    s = re.sub(r"<(strong|b)[^>]*>(.*?)</\1>", lambda m: f"**{m.group(2)}**", s, flags=re.IGNORECASE | re.DOTALL)
    s = re.sub(
        r"<span[^>]*style=\"[^\"]*font-weight:\s*bold[^\"]*\"[^>]*>(.*?)</span>",
        lambda m: f"**{m.group(1)}**",
        s,
        flags=re.IGNORECASE | re.DOTALL,
    )
    s = re.sub(r"<br\s*/?>", "\x1e", s, flags=re.IGNORECASE)
    s = re.sub(r"</(p|div|li|h\d|tr|td|th|blockquote|article|section)\s*>", "\x1e", s, flags=re.IGNORECASE)
    s = re.sub(r"<(p|div|li|h\d|tr|td|th|blockquote|article|section)[^>]*>", "\x1e", s, flags=re.IGNORECASE)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    blocks: list[str] = []
    for raw in s.split("\x1e"):
        cleaned = re.sub(r"\s+", " ", raw).strip()
        if cleaned:
            blocks.append(cleaned)
    return "\n\n".join(blocks).strip()


# ---- Section parsing ----------------------------------------------------------

def parse_section(html_text: str, code: str, section: str) -> tuple[str, str]:
    """Returns (caption, body_md). Leginfo's section page wraps the
    text in <div id="manylawsections"> with the section number and
    body inline. The fallback path captures whatever main content
    block is present.
    """
    caption = ""
    body = ""

    # Caption: typically appears as "<h6>1788.30.</h6>" or similar
    cap_m = re.search(
        r"<h\d[^>]*>\s*" + re.escape(section) + r"\.?\s*</h\d>",
        html_text,
        re.IGNORECASE,
    )

    # Heuristic: find a div with id starting with manylawsections, otherwise
    # fall back to the section's surrounding content.
    body_re = re.compile(
        r"<div\s+id=['\"]manylawsections['\"][^>]*>(.*?)</div>\s*<div\s+id=['\"]hist['\"]",
        re.IGNORECASE | re.DOTALL,
    )
    body_m = body_re.search(html_text)
    if not body_m:
        # Fallback: content area without explicit history div
        body_re2 = re.compile(
            r"<div\s+id=['\"]manylawsections['\"][^>]*>(.*?)(?:</div>\s*<div\s+id=|<footer)",
            re.IGNORECASE | re.DOTALL,
        )
        body_m = body_re2.search(html_text)

    if body_m:
        body = html_to_text(body_m.group(1))

    # Use the body's first line as the caption if no heading found
    if cap_m and not caption:
        caption = section
    elif not caption and body:
        first = body.split("\n", 1)[0]
        if len(first) <= 200:
            caption = first

    return caption, body


def fetch_section(code: str, section: str) -> tuple[str, str, str, str, str | None]:
    """Returns (code, section, caption, body, error|None)."""
    url = SECTION_URL.format(code=code, section=section)
    try:
        html_bytes = http_get(url)
        caption, body = parse_section(html_bytes.decode("utf-8", errors="replace"), code, section)
        return code, section, caption, body, None
    except Exception as e:
        return code, section, "", "", f"{type(e).__name__}: {e}"


# ---- Render -------------------------------------------------------------------

CODE_DISPLAY = {
    "CCP": "Cal. Code Civ. Proc.",
    "CIV": "Cal. Civ. Code",
    "BPC": "Cal. Bus. & Prof. Code",
    "FIN": "Cal. Fin. Code",
    "COM": "Cal. Comm. Code",
    "EVID": "Cal. Evid. Code",
}


def render_file_md(
    stem: str,
    description: str,
    sections: list[tuple[str, str, str]],
    fetched: dict[tuple[str, str], tuple[str, str, str | None]],
) -> str:
    today = date.today().isoformat()
    out: list[str] = []
    out.append(f"# {description}")
    out.append("")
    out.append(f"- Description: {description}")
    out.append(f"- Source: {BASE}/faces/codes.xhtml")
    out.append(f"- Pulled: {today}")
    out.append(f"- Sections: {len(sections)}")
    out.append("")
    out.append("> Verbatim text from the California Legislative Information website.")
    out.append("> Citation history and notes are preserved as published.")
    out.append("")

    out.append("## Contents")
    out.append("")
    for code, section, label in sections:
        cite_disp = f"{CODE_DISPLAY.get(code, code)} § {section}"
        anchor = f"sec-{code.lower()}-{section.replace('.', '-')}"
        out.append(f"- [{cite_disp} — {label}](#{anchor})")
    out.append("")

    for code, section, label in sections:
        key = (code, section)
        caption, body, err = fetched.get(key, ("", "", "missing"))
        cite_disp = f"{CODE_DISPLAY.get(code, code)} § {section}"
        anchor = f"sec-{code.lower()}-{section.replace('.', '-')}"
        out.append(f'<a id="{anchor}"></a>')
        out.append(f"## {cite_disp} — {label}")
        out.append("")
        out.append(f"Source: {SECTION_URL.format(code=code, section=section)}")
        out.append("")
        if err:
            out.append(f"> **Fetch failed:** {err}")
            out.append("")
        elif not body:
            out.append("> _(empty extraction)_")
            out.append("")
        else:
            out.append(body)
            out.append("")
    text = "\n".join(out).rstrip() + "\n"
    return re.sub(r"\n{3,}", "\n\n", text)


# ---- Main --------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out",
        default="plugins/ca-court-docs/skills/ca-law-references/references/ca-statutes-debt",
    )
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument(
        "--only",
        nargs="*",
        help="Optional list of output-file stems to limit to (e.g. CCP-SOL CivCode-Rosenthal).",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Print URLs without fetching.",
    )
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    only = set(args.only) if args.only else None

    if args.dry_run:
        for stem, desc, sections in FILES:
            if only and stem not in only:
                continue
            print(f"\n=== {stem} — {desc} ({len(sections)} sections) ===")
            for code, section, label in sections:
                print(f"  {SECTION_URL.format(code=code, section=section)}")
        return 0

    grand_total = 0
    grand_failed = 0

    for stem, description, sections in FILES:
        if only and stem not in only:
            continue
        print(f"\n=== {stem} — {description} ===", flush=True)
        print(f"  {len(sections)} sections", flush=True)

        fetched: dict[tuple[str, str], tuple[str, str, str | None]] = {}
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = {
                ex.submit(fetch_section, code, section): (code, section)
                for code, section, _label in sections
            }
            done = 0
            for fut in as_completed(futs):
                done += 1
                code, section, caption, body, err = fut.result()
                fetched[(code, section)] = (caption, body, err)
                if err:
                    print(
                        f"    [{done}/{len(sections)}] {code} § {section} FAIL: {err}",
                        flush=True,
                    )
                    grand_failed += 1

        md = render_file_md(stem, description, sections, fetched)
        out_path = out_dir / f"{stem}.md"
        out_path.write_text(md, encoding="utf-8")
        print(f"  wrote {out_path} ({len(md):,} bytes)", flush=True)
        grand_total += len(sections)

    print(
        f"\nDone. {grand_total} sections; {grand_failed} fetch errors.",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
