# State Research Protocol

Before scaffolding a new state plugin, research the state's
procedural rules using WebFetch against authoritative sources.
The substantive content of every skill depends on this.

> **WebFetch only**. Per the marketplace's safety policy, no
> curl, wget, requests, or other network mechanisms. All
> sources below are public-facing HTML or PDF reachable via
> WebFetch.

## What to research

### 1. State pleading-format rule

Find the state's rule governing the physical format of court
filings (paper size, margins, fonts, color, footer).

Common patterns:

| State | Rule |
|-------|------|
| Washington | GR 14 |
| Oregon | UTCR 2.010 |
| California | CRC 2.100–2.119 |
| Texas | TRCP 21a |
| Florida | Fla. R. Gen. Prac. Jud. Admin. 2.520 |
| New York | CPLR 2101 |
| Arizona | Ariz. R. Civ. P. 5.4 |
| Colorado | C.R.C.P. 121 |

```
WebFetch:
  url: https://www.courts.[state-domain]/[rule-path]
  prompt: Locate the rule governing the format of court
          filings (paper size, margins, font, color). Quote
          the verbatim text. Identify the current effective
          date.
```

### 2. State civil rules

| State | Civil rules code |
|-------|------------------|
| Washington | CR (superior) + CRLJ (district) |
| Oregon | ORCP |
| California | CCP — Code of Civil Procedure |
| Texas | TRCP — Texas Rules of Civil Procedure |
| Florida | Fla. R. Civ. P. |
| New York | CPLR — Civil Practice Law & Rules |
| Arizona | Ariz. R. Civ. P. |
| Colorado | C.R.C.P. |
| Illinois | 735 ILCS 5/2- (and Ill. S. Ct. Rule series) |
| Pennsylvania | Pa. R. Civ. P. |

Identify the analog rules for:

- Service of process
- Initial responsive-pleading deadline
- Motion to dismiss (failure to state)
- Discovery scope and tools (RFPs, RFAs, depositions,
  interrogatories — and which are available)
- Motion to compel + fee-shifting
- Summary judgment
- Default judgment
- Vacation of judgment (state's FRCP 60 analog)
- Time computation
- Pleading amendments

### 3. State evidence rules

| State | Evidence code |
|-------|--------------|
| Washington | ER (court rule) |
| Oregon | OEC (codified at ORS Ch. 40) |
| California | CEC — Cal. Evid. Code |
| Texas | Tex. R. Evid. |
| Florida | Fla. Stat. § 90 |
| New York | (mostly common-law; CPLR Art. 45) |
| Federal | FRE |

Identify the analog rules for:

- Relevance
- Hearsay definition and exceptions (especially business
  records)
- Authentication and self-authentication
- Best evidence rule
- Privileges

### 4. State citation style

Most states publish a style manual:

| State | Style |
|-------|-------|
| Washington | Reporter of Decisions (GR 14(d) cites Wn.2d / Wn. App.) |
| Oregon | Oregon Appellate Courts Style Manual (no periods) |
| California | California Style Manual / Cal Reports |
| Texas | Texas Rules of Form (Green Book) |
| Federal | The Bluebook |

```
WebFetch:
  url: <state style manual URL>
  prompt: Identify the case-citation conventions for this
          state. Quote the citation form for the state
          supreme court and intermediate appellate court.
          Identify any state-specific conventions (periods,
          spacing, italicization).
```

### 5. State consumer-protection statute

| State | Statute | Notes |
|-------|---------|-------|
| Washington | RCW 19.86 (CPA) | Hangman Ridge factors |
| Oregon | ORS 646.605 (UTPA) | Mandatory fees ORS 646.638(3) |
| California | Bus. & Prof. Code §§ 17200 (UCL), 17500 (FAL); Civ. Code §§ 1750 (CLRA), 1788 (Rosenthal Act) | Multiple overlapping statutes |
| Texas | Tex. Bus. & Com. Code § 17 (DTPA) | Treble damages |
| Florida | Fla. Stat. § 501.201 (FDUTPA) | |
| New York | GBL §§ 349, 350 | Limited remedies |
| Illinois | 815 ILCS 505 (ICFA) | Strong private right |

### 6. State debt-collection / collection-agency law

Important state-level wrinkle for the consumer-debt bundle:

| State | Statute | Registration? |
|-------|---------|---------------|
| Washington | RCW 19.16 | License required |
| Oregon | ORS 697 | Registration required |
| California | Civ. Code § 1788 (Rosenthal) + Fin. Code § 100001 (CDCLA, 2022+) | License required |
| Texas | Tex. Fin. Code Ch. 392 | Bond required |
| Florida | Fla. Stat. § 559.55 | License required |
| New York | NY Gen. Bus. Law § 600 | License required |

Always check whether the state has a public-facing
registration database (most do — California has DFPI; Texas
has OCCC; etc.).

### 7. Statutes of limitations on debt

| State | Written contract | Open account | Authority |
|-------|------------------|--------------|-----------|
| Washington | 6 years | 6 years | RCW 4.16.040 |
| Oregon | 6 years | 6 years | ORS 12.080 |
| California | 4 years | 4 years | CCP § 337 |
| Texas | 4 years | 4 years | Tex. Civ. Prac. & Rem. Code § 16.004 |
| Florida | 5 years | 5 years | Fla. Stat. § 95.11 |
| New York | 6 years (CC); 3 years for revolving credit | NY CPLR § 213; § 214-i (2022 reform) | |
| Illinois | 10 years | 5 years | 735 ILCS 5/13-205 |

Also research the state's **revival** rule (does partial
payment restart the clock?):

- Oregon: NO, only written promise (ORS 12.230)
- Washington: YES, partial payment can revive (RCW 4.16.270)
- California: YES, partial payment revives (CCP § 360)
- Many states differ

### 8. State legal holidays

For the case-calendar script. Federal holidays apply across
all states; state-specific holidays vary:

- Washington: federal + Native American Heritage Day (Friday
  after Thanksgiving)
- Oregon: federal only (no day after Thanksgiving)
- California: federal + César Chávez Day (March 31) +
  Lincoln's Birthday (Feb. 12, observed)
- Texas: federal + Confederate Heroes Day (Jan 19, no longer
  observed as a state holiday in courts) + Texas Independence
  Day (Mar 2)
- Florida: federal + Susan B. Anthony Day
- Hawaii: federal + Prince Kūhiō Day, King Kamehameha I Day,
  Statehood Day

Pull from the state's official sources:

```
WebFetch:
  url: <state secretary of state or judicial branch holiday list>
  prompt: List the state's legal holidays for the current
          year, including any observed-day shift rules
          (Saturday → Friday, Sunday → Monday, etc.).
```

### 9. High-volume courts

Identify the two highest-civil-filing courts in the state for
flagship-court skills:

| State | Primary | Secondary |
|-------|---------|-----------|
| Washington | King Co Superior | King Co District |
| Oregon | Multnomah Circuit | Washington Co Circuit |
| California | LA Superior | SF Superior (or Orange Co) |
| Texas | Harris Co District | Dallas Co District |
| Florida | Miami-Dade Circuit | Broward Co Circuit |
| New York | NY Supreme NY County | NY Supreme Kings County |

Research:

- Address
- Civil Division contact (phone, email)
- Local rules (slug typically `slr` or `local rules`)
- Scheduling model (JA / Civil Division / centralized motion
  docket)
- Working-copy practice (required? threshold?)
- eFiling system

### 10. eFiling system

Most states use one of:

- Tyler Tech (File and Serve / Odyssey)
- Pro Doc / Texas-specific
- State-specific portal (NY NYSCEF, FL Portal)
- Self-built (older states)

Identify the portal and the state's eFiling rule.

## State research output

After research, the agent should have a compact summary like:

```
State: California
Abbreviation: ca

Format rule: California Rules of Court 2.100–2.111
Civil rules: California Code of Civil Procedure (CCP)
Evidence rules: California Evidence Code (CEC, Cal. Evid. Code)
Statute code: Cal. Civ. Code, CCP, Cal. Bus. & Prof. Code

Style manual: California Style Manual (4th ed.)
URL: https://www.courts.ca.gov/style-manual

Primary court: Los Angeles Superior Court
  Slug: lasc
  Address: 111 N Hill St, Los Angeles CA 90012
  Local rules: Los Angeles SC Local Rules
  Scheduling: Individual department / clerk
  eFiling: One Legal / File & ServeXpress (state-approved)

Secondary court: San Francisco Superior Court
  Slug: sfsc
  Address: 400 McAllister St, San Francisco CA 94102
  Local rules: SF Local Rules
  Scheduling: Mostly tentative-ruling system

Roll-up counties: Orange, San Diego, San Bernardino, Sacramento,
  Alameda, Santa Clara, Contra Costa, Riverside, Fresno

State debt SOL: 4 years (CCP § 337)
Partial-payment revival: Yes (CCP § 360)

Consumer-protection statute: California Rosenthal Fair Debt
  Collection Practices Act (Cal. Civ. Code §§ 1788–1788.32)
  + CA UCL (Bus. & Prof. Code § 17200)
  + CLRA (Civ. Code § 1750)

Collection-agency licensing: Cal. Fin. Code § 100001 et seq.
  (Debt Collection Licensing Act, 2022)
  DFPI registry: https://docqnet.dfpi.ca.gov/

State holidays (state-specific beyond federal):
  - César Chávez Day (March 31)
  - Lincoln's Birthday (Feb 12, observed)
```

This block is what the scaffolder script consumes (or what
the agent uses to author the skills manually).

## Sanity-check the research

Before authoring 21 skills based on the research:

- Run a different WebFetch on the same source to verify
- Cross-check against state-bar publications
- Check that any cited statute is **currently in effect**
  (legislatures amend; do not rely on caches)
- Note the "as of" date in the research summary

## When research conflicts with a generated skill

If, after authoring, the agent realizes a cited rule has been
amended or doesn't exist: **fix the SKILL.md immediately**.
A wrong cited rule is worse than no skill — it would mislead
a pro se filer.

## Pull-script targets

Many states have legislative websites that publish statutes
in XML or structured HTML. A future `pull_<state>.py` script
can extract from:

- California: leginfo.legislature.ca.gov
- Texas: statutes.capitol.texas.gov
- New York: nysenate.gov/legislation
- Florida: leg.state.fl.us

Add the URL pattern to the new plugin's `legal-data-apis.md`
even before the pull script exists, so future maintainers
know where to look.
