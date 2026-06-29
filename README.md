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

- **EXIF data in photos** — Most cameras and smartphones embed an EXIF
  block in every JPEG: camera make/model, the exact timestamp the shot was
  taken, exposure settings, and if location services were on — GPS
  coordinates accurate to a few metres. This can place a specific device at a
  specific place and time, which is exactly the kind of fact an investigator
  (or a journalist verifying a source image) needs. It's also why privacy
  advocates warn people to strip EXIF data before posting photos online —
  plenty of real stalking and doxxing cases have started with someone
  finding the GPS tag buried in a "harmless" photo.

https://github.com/IdreesYousofzai/file-metadata-analyser.git
