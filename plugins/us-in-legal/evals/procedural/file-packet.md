# in-file-packet — Odyssey e-filing assembly and document codes

## Prompt

I'm ready to file my motion and supporting documents in
Hamilton County Superior Court through the Indiana e-filing
system. I have the motion, a memorandum, a declaration, and
a proposed order. How do I upload everything, what document
codes do I use, and how do I make sure opposing counsel gets
served automatically?

## Expected triggers

- `in-file-packet`
- `in-statewide-format`

## Acceptance criteria

### Odyssey portal and access

- [ ] Identifies the filing portal as
      **https://efile.courts.in.gov** (the Indiana
      statewide Odyssey system) — the **only** state
      besides Illinois to run unified statewide e-filing
      through Tyler Odyssey
- [ ] Notes it is **mandatory for represented parties**
      in every Indiana county since 2018; **optional
      for pro se** filers
- [ ] States the accepted file format is **PDF only**
      (not Word); notes the 25 MB per-document limit
      and 100 MB total multi-document limit

### Document codes and packet assembly

- [ ] States that each document must be assigned a
      **document code** from the Odyssey dropdown that
      matches the document title (the dropdown labels
      mirror T.R. 7 motion types)
- [ ] Identifies the correct code for each of the four
      documents in the packet: motion, memorandum /
      brief in support, declaration / affidavit, and
      proposed order (reads code labels from
      `in-file-packet` / `in-statewide-format` rather
      than asserting specific code strings from memory)
- [ ] Notes that Marion County LR49-TR5-203 prefers
      exhibits as a single combined PDF with bookmarks
      (or as separate sub-documents per Odyssey upload
      method) — reads from `in-marion` / `in-statewide-
      format`

### Service through Odyssey

- [ ] States that Odyssey **auto-serves all registered
      Service Contacts** on a case when the filing is
      submitted; explains that the party configures
      Service Contacts at the first filing
- [ ] Notes that for non-Odyssey-registered parties
      (some pro se opponents), paper service under
      T.R. 5(B) must still be accomplished
- [ ] States the Certificate of Service should still
      appear in the document body even when Odyssey
      auto-serves registered counsel

### PII redaction

- [ ] Notes the redaction obligation for sensitive
      identifiers (Social Security numbers, financial
      account numbers) before PDF upload — reads the
      controlling rule from the corpus

## Common failure modes

- States Odyssey is mandatory for pro se filers
  (it is optional)
- Suggests uploading Word (.docx) directly (Odyssey
  requires PDF)
- States Odyssey auto-serves all parties regardless
  of registration (unregistered parties still need
  paper service)
- Omits the Certificate of Service from the document
  body because Odyssey "handles it"
