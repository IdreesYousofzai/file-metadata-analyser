# File Metadata Analyser

A digital-forensics style CLI tool that detects a file's type (image, PDF, or
Word document) and extracts the metadata hidden inside it: GPS coordinates,
camera model, EXIF dates, document authorship, revision history, edit time,
and creation/modification timestamps.

---

## Why metadata matters for forensic investigators

**Metadata is data *about* data**: information a file carries about itself,
separate from its visible content. A photo's pixels show a scene; its
metadata can show exactly *when*, *where*, and *on what device* it was taken.
A Word document's text shows what was written; its metadata can show *who*
wrote it, *who* last touched it, and *how long* they spent editing.

This makes metadata extremely valuable as digital evidence:

- **EXIF data in photos**: Most cameras and smartphones embed an EXIF
  block in every JPEG: camera make/model, the exact timestamp the shot was
  taken, exposure settings, and if location services were on GPS
  coordinates accurate to a few metres. This can place a specific device at a
  specific place and time, which is exactly the kind of fact an investigator
  (or a journalist verifying a source image) needs.

- **Author/revision info in PDFs and Word docs**: Office documents quietly
  record who created and who last edited a file, how many times it's been
  revised, and how many minutes were spent editing it (`TotalTime` in a
  `.docx`). In a fraud or plagiarism investigation, this can reveal that a
  document was created by someone other than its claimed author, or that it
  was edited *after* a date it was supposed to be finalised.

- **Creation/modified timestamps**: File system and document timestamps
  build a timeline. Investigators cross-reference these against other
  evidence (CCTV, phone logs, alibi statements) to spot inconsistencies.

- **The absence of metadata is itself a clue.** Platforms like Facebook,
  WhatsApp, and Instagram strip EXIF data on upload. So if an image *has* no
  metadata, that can tell an investigator it was likely shared through one
  of those platforms rather than sent as a raw camera file.

https://github.com/IdreesYousofzai/file-metadata-analyser.git
