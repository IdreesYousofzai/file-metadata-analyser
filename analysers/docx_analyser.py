"""
Word document (.docx) metadata extractor.

python-docx exposes the standard "core" properties (author, last
modified by, revision number, created/modified dates...) through
Document.core_properties - those live in docProps/core.xml.

It does NOT expose the "app" properties stored in docProps/app.xml,
such as TotalTime (total editing time, in minutes) or the
Application that created the file. A .docx is just a zip archive
under the hood, so to get those extra forensically-useful fields we
open the zip directly and parse app.xml ourselves.
"""

import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from docx import Document

APP_XML_PATH = "docProps/app.xml"
APP_NS = {"ep": "http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"}


def _extract_app_properties(path: Path) -> dict:
    """Pull extra metadata out of docProps/app.xml (not exposed by python-docx)."""
    extras = {}
    try:
        with zipfile.ZipFile(path) as docx_zip:
            if APP_XML_PATH not in docx_zip.namelist():
                return extras
            with docx_zip.open(APP_XML_PATH) as f:
                root = ET.parse(f).getroot()

        def get(tag):
            el = root.find(f"ep:{tag}", APP_NS)
            return el.text if el is not None else None

        total_time = get("TotalTime")
        if total_time:
            extras["Total edit time"] = f"{total_time} minutes"

        application = get("Application")
        if application:
            extras["Created with"] = application

        company = get("Company")
        if company:
            extras["Company"] = company

        pages = get("Pages")
        if pages:
            extras["Pages (at last save)"] = pages

        words = get("Words")
        if words:
            extras["Word count"] = words

    except (zipfile.BadZipFile, ET.ParseError):
        pass

    return extras


def analyse(filepath) -> dict:
    """Extract metadata from a .docx file and return it as a label -> value dict."""
    path = Path(filepath)
    result = {
        "File name": path.name,
        "File size": f"{path.stat().st_size / 1024:.1f} KB",
    }

    doc = Document(str(path))
    props = doc.core_properties

    core_fields = {
        "Author": props.author,
        "Last modified by": props.last_modified_by,
        "Revision number": props.revision,
        "Created": props.created,
        "Last modified": props.modified,
        "Title": props.title,
        "Subject": props.subject,
        "Category": props.category,
        "Comments": props.comments,
    }

    for label, value in core_fields.items():
        result[label] = value if value not in (None, "") else "Not present"

    result.update(_extract_app_properties(path))

    return result
