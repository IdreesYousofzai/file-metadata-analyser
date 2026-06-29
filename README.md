<img width="596" height="299" alt="image" src="https://github.com/user-attachments/assets/290b7a29-49c0-4541-a4b9-3d6c618b5367" />

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

  ---

## Features

- **Images** (`.jpg`, `.jpeg`, `.png`, `.tiff`, `.bmp`, `.heic`) — via
  Pillow + exifread: format, dimensions, camera make/model, date taken,
  software used, and GPS coordinates (converted from EXIF's degrees/minutes/
  seconds format into a clickable Google Maps link).
- **PDFs** (`.pdf`) — via PyPDF2: author, title, creator application,
  producer (software that generated the file), creation/modification dates,
  page count, and encryption status.
- **Word documents** (`.docx`) — via python-docx (plus direct parsing of
  `docProps/app.xml`, which python-docx doesn't expose): author, last
  modified by, revision number, created/modified dates, and total edit time
  in minutes.
- **Clean CLI menu** — auto-detects the file type from its extension and
  routes it to the right extractor. Supports an interactive menu, a
  "browse this folder" picker, or a direct command-line argument for
  drag-and-drop use.
- **Graceful handling** of missing files, unsupported formats, and files
  with no metadata at all (clearly reported rather than crashing).

---

## Installation

```bash
git clone https://github.com/IdreesYousofzai/file-metadata-analyser.git
cd file-metadata-analyser
pip install -r requirements.txt
```

## Usage

Interactive menu:

```bash
python main.py
```

Or analyse a file directly:

```bash
python main.py path/to/photo.jpg
python main.py path/to/report.pdf
python main.py path/to/essay.docx
```

### Example output

```
============================================================
 IMAGE METADATA - HOLIDAY_PHOTO.JPG
============================================================
  File name       : holiday_photo.jpg
  File size       : 3421.6 KB
  Format          : JPEG
  Dimensions      : 4032 x 3024 px
  Colour mode     : RGB
  Camera          : Apple iPhone 14 Pro
  Date taken      : 2026:03:14 10:22:01
  Software        : iOS 17.4
  GPS coordinates : 53.763197, -2.7031
  Map link        : https://maps.google.com/?q=53.763197,-2.7031
------------------------------------------------------------
```

---

## Project structure

```
file-metadata-analyser/
├── main.py                   # CLI entry point: detects file type, dispatches
├── requirements.txt
├── README.md
└── analysers/
    ├── __init__.py
    ├── image_analyser.py     # Pillow + exifread -> EXIF / GPS extraction
    ├── pdf_analyser.py        # PyPDF2 -> author/producer/dates/page count
    ├── docx_analyser.py       # python-docx + raw app.xml -> author/edit time
    └── utils.py               # shared CLI output formatting
```

---

## Notes & limitations

- **PyPDF2** is the library specified for this project; note that upstream
  development has moved to its successor, `pypdf` (same API, actively
  maintained). `PyPDF2` still works fine here and is kept since it's what
  was requested.
- **HEIC images** need the optional `pillow-heif` plugin installed for
  Pillow to open them — not included by default since it's a less common
  format.
- Many social platforms strip EXIF/GPS data on upload, so a lack of
  metadata on a downloaded image doesn't necessarily mean none ever existed.
- This is a learning/portfolio project, not a tool for handling real
  chain-of-custody evidence — production forensic work should use
  validated, court-admissible tooling (e.g. Autopsy, EnCase, ExifTool with
  hash verification).
