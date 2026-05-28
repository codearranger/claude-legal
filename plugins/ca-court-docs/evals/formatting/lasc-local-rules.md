# ca-lasc — LASC local rules and protocols

## Prompt

I have a motion ready to file in Los Angeles Superior Court. How
do I reserve a hearing date and what local rules apply?

## Expected triggers

- `ca-lasc`
- `ca-schedule-hearing`
- `ca-statewide-format`

## Acceptance criteria

### Court identification

- [ ] Names "Los Angeles Superior Court" / LASC
- [ ] Identifies primary courthouse (Stanley Mosk Courthouse,
      111 N. Hill St.)
- [ ] Notes district courthouses (Spring St., Norwalk, Pomona,
      Van Nuys, Pasadena, Long Beach, Compton, etc.)

### Reservation

- [ ] LASC Court Reservation System (CRS) at lacourt.org
- [ ] Reserve the date BEFORE serving the notice
- [ ] Department-specific reservation rules

### Tentative-ruling regime

- [ ] CRC 3.1308 and LASC Local Rule 3.31 — tentative posted
      day before hearing
- [ ] Party that contests must call by 4:30 p.m. day before
- [ ] Failure to contest = tentative becomes order

### E-filing

- [ ] Mandatory for represented parties via Odyssey eFileCA
      (Tyler-based)
- [ ] efilingsupport.lacourt.org

### Case management

- [ ] CMC typically scheduled ~120 days after filing
- [ ] CMC Statement (Judicial Council Form CM-110) due 15
      calendar days before CMC (CRC 3.725)

## Common failure modes

- Telling user to file the motion before reserving the date
- Confusing LASC with SFSC reservation system
- Citing a single LASC courthouse when the user might be in
  Van Nuys or Long Beach
- Importing King County or Multnomah reservation procedures
