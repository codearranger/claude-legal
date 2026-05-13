# KCSC — e-filing, working copies, the case schedule, and motion practice

> All of this is governed by the **King County LCR** (amended roughly
> annually) plus the statewide CR / ER. Pull the current LCR and the
> Clerk's instructions before filing; treat the specifics below as
> pointers.

## E-filing through the Clerk

- File through the **King County Superior Court Clerk's E-Filing
  application**, reached from the Department of Judicial Administration
  (DJA) filing page:
  `https://kingcounty.gov/en/dept/dja/courts-jails-legal-system/court-forms-document-filing/filing`.
- On an **initial pleading** filed electronically, the Clerk returns an
  electronic **conformed copy** to the filer; the **CICS / Case
  Assignment Designation** is filed with it (see
  `case-assignment-and-locations.md`).
- View filed documents through **eRecords**.
- Fees: see the Clerk's current fee schedule on the DJA site (the
  `wa-law-references` "fees and costs" material has the statewide filing
  fee baseline; King County adds local fees).
- **Service**: serve under **CR 5** the same day by an authorized
  method; attach a **Declaration/Certificate of Service** to anything
  served.

## Working copies — required (LCR 7)

KCSC requires **working copies** of motion materials for the assigned
judge's department (or for Ex Parte). Key points — confirm against the
current LCR 7 and the Clerk's "working copies" instructions:

- Working copies are delivered **separately** from the e-filed
  documents, by the LCR 7 deadline (working copies are generally due a
  set number of court days before the hearing).
- The Clerk provides an electronic **"Submit Working Copies"** tool;
  many departments accept that, some also accept/prefer paper —
  check the assigned department's posted procedures.
- Each set carries the **working-copy designation / coversheet**
  (identifying the judge/department, hearing date, and the moving
  party).
- Working copies include the motion, memorandum, declarations, exhibits,
  and proposed order — i.e., everything the judge needs to rule.

## Case schedule — LCR 4

For most civil cases the Clerk issues an **Order Setting Civil Case
Schedule** at filing. It fixes deadlines keyed to the filing date:
confirmation of joinder of parties / claims / defenses, disclosure of
possible primary and additional witnesses, discovery cutoff, deadline
for dispositive motions, status conference (if any), and the **trial
date**. Some case types are exempt or follow a different track (check the
case-type list in LCR 4). Treat the Case Schedule as binding alongside CR
6 time computation — use the `wa-deadlines` skill and
`plugins/wa-court-docs/scripts/case-calendar.py`, applying RCW 1.16.050
holidays. Missing a Case Schedule deadline can mean sanctions or
exclusion of witnesses/evidence under LCR 4.

## Civil motions — noting, notice, confirmation (LCR 7)

- **Where it's heard**: a motion in a case with an assigned judge is
  noted to that **department** (scheduled with the bailiff per the
  department's procedures); some matters go to **Chief Civil**; agreed
  and many procedural orders go through **Ex Parte / Ex Parte via the
  Clerk**.
- **Notice period**: note the motion the number of court days ahead that
  LCR 7 / CR 6 require for the type of motion and method of service
  (commonly **≥ 9 court days** for an in-person-served noted civil
  motion; response and reply deadlines and any e-service adjustment are
  in LCR 7 — read the current version).
- **Confirmation**: the moving party generally must **confirm** the
  motion by the LCR 7 deadline (and state whether oral argument is
  wanted); an **unconfirmed motion is struck**.
- **Continuances / strikes**: follow the LCR 7 / department procedure
  (often an agreed order via Ex Parte, or a notice of strike), and
  notify the other parties.

## Document set for a noted civil motion

1. **Motion** (+ **Memorandum** if not self-contained)
2. **Declaration(s)** with authenticated exhibits
3. **Proposed Order**
4. **Note for Civil Motion Calendar** (assigned department) **or** Ex
   Parte presentation materials
5. **Working copies** of items 1–3 (and the note), with the working-copy
   coversheet, delivered per LCR 7
6. **Declaration/Certificate of Service**

E-file each as a separate PDF through the Clerk's E-Filing application;
deliver working copies through the Submit Working Copies tool or as the
department directs. Run `plugins/wa-court-docs/scripts/format-check.py`
and the `wa-quality-check` skill before filing.
