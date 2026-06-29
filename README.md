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

https://github.com/IdreesYousofzai/file-metadata-analyser.git
