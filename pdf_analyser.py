"""
PDF metadata extractor.

PyPDF2's PdfReader exposes the document info dictionary as
reader.metadata - that's where author, producer, creation date etc.
live. Page count comes from len(reader.pages).
"""

from pathlib import Path

from PyPDF2 import PdfReader


def analyse(filepath) -> dict:
    """Extract metadata from a PDF file and return it as a label -> value dict."""
    path = Path(filepath)
    result = {
        "File name": path.name,
        "File size": f"{path.stat().st_size / 1024:.1f} KB",
    }

    reader = PdfReader(str(path))
    result["Number of pages"] = len(reader.pages)

    if reader.is_encrypted:
        result["Encryption"] = "Yes - this PDF is password protected"

    meta = reader.metadata
    if not meta:
        result["Document metadata"] = "None found"
        return result

    fields = {
        "Author": meta.author,
        "Title": meta.title,
        "Subject": meta.subject,
        "Creator (originating application)": meta.creator,
        "Producer (software that wrote the PDF)": meta.producer,
        "Creation date": meta.creation_date,
        "Modification date": meta.modification_date,
    }

    for label, value in fields.items():
        result[label] = value if value else "Not present"

    return result
