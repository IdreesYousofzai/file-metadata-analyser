"""
analysers package
-----------------
Each module in here knows how to pull metadata out of one file type:

    image_analyser.py  -> JPG / PNG / TIFF / BMP / HEIC  (Pillow + exifread)
    pdf_analyser.py     -> PDF                            (PyPDF2)
    docx_analyser.py    -> Word .docx                     (python-docx + raw XML)

Every module exposes a single function, analyse(filepath) -> dict,
so main.py can treat them interchangeably once it has detected the
file type.
"""
