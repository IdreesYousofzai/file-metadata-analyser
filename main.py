
"""
File Metadata Analyser
=======================
A digital-forensics style CLI tool. Point it at a file and it will
detect the type (image / PDF / Word document) and extract whatever
metadata is embedded in it: GPS coordinates, camera model, EXIF
dates, document authorship, revision history, creation/modification
timestamps, software used and more.

Usage:
    python main.py                # interactive menu
    python main.py path/to/file   # analyse one file directly
"""

import sys
from pathlib import Path

from analysers import image_analyser, pdf_analyser, docx_analyser
from analysers.utils import print_header, print_fields, print_error

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp", ".heic"}
PDF_EXTENSIONS = {".pdf"}
DOCX_EXTENSIONS = {".docx"}

BANNER = r"""
 ______ _ _          __  __      _            _       _
|  ____(_) |        |  \/  |    | |          | |     | |
| |__   _| | ___    | \  / | ___| |_ __ _  __| | __ _| |_ __ _
|  __| | | |/ _ \   | |\/| |/ _ \ __/ _` |/ _` |/ _` | __/ _` |
| |    | | |  __/   | |  | |  __/ || (_| | (_| | (_| | |_ (_| |
|_|    |_|_|\___|   |_|  |_|\___|\__\__,_|\__,_|\__,_|\__\__,_|

            Analyser  -  Digital Forensics Toolkit
"""


def detect_and_analyse(filepath: str) -> None:
    cleaned = str(filepath).strip().strip('"').strip("'")
    path = Path(cleaned).expanduser()

    if not path.exists():
        print_error(f"File not found: {path}")
        return
    if not path.is_file():
        print_error(f"Not a file: {path}")
        return

    ext = path.suffix.lower()

    try:
        if ext in IMAGE_EXTENSIONS:
            print_header(f"Image metadata - {path.name}")
            print_fields(image_analyser.analyse(path))

        elif ext in PDF_EXTENSIONS:
            print_header(f"PDF metadata - {path.name}")
            print_fields(pdf_analyser.analyse(path))

        elif ext in DOCX_EXTENSIONS:
            print_header(f"Word document metadata - {path.name}")
            print_fields(docx_analyser.analyse(path))

        else:
            print_error(
                f"Unsupported file type '{ext}'. "
                f"Supported: images (jpg/png/tiff/bmp/heic), .pdf, .docx"
            )

    except Exception as exc:
        print_error(f"Could not read metadata - {exc}")


def browse_directory(directory: str = ".") -> None:
    """List supported files in a directory so the user can pick one by number."""
    supported = IMAGE_EXTENSIONS | PDF_EXTENSIONS | DOCX_EXTENSIONS
    folder = Path(directory).expanduser()

    if not folder.is_dir():
        print_error(f"Not a directory: {folder}")
        return

    files = sorted(
        p for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in supported
    )

    if not files:
        print_error(f"No supported files found in {folder.resolve()}")
        return

    print_header(f"Supported files in {folder.resolve()}")
    for i, f in enumerate(files, start=1):
        print(f"  [{i}] {f.name}")
    print("-" * 60)

    choice = input("  Select a file number (Enter to cancel): ").strip()
    if not choice:
        return
    try:
        index = int(choice) - 1
        if 0 <= index < len(files):
            detect_and_analyse(str(files[index]))
        else:
            print_error("Invalid selection.")
    except ValueError:
        print_error("Please enter a valid number.")


def main_menu() -> None:
    print(BANNER)
    while True:
        print("""
  MAIN MENU
  ---------
  [1] Analyse a file (enter a path)
  [2] Browse a folder for supported files
  [3] Exit
""")
        choice = input("  Choose an option: ").strip()

        if choice == "1":
            filepath = input("  Enter the path to a file: ").strip()
            detect_and_analyse(filepath)

        elif choice == "2":
            directory = input("  Enter folder path (Enter for current folder): ").strip() or "."
            browse_directory(directory)

        elif choice == "3":
            print("\n  Goodbye.\n")
            sys.exit(0)

        else:
            print_error("Invalid option - choose 1, 2 or 3.")


if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        detect_and_analyse(sys.argv[1])
    else:
        main_menu()
