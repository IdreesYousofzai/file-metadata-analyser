"""
Image metadata extractor.

Pillow gives us the basics (format, dimensions, colour mode) easily,
but decoding EXIF tags - especially GPS coordinates - through Pillow's
raw API is fiddly (everything comes back as numeric tag IDs). exifread
does that decoding for us and hands back human-readable tag names, so
we use it for anything EXIF-related.
"""

from pathlib import Path

from PIL import Image
import exifread


def _convert_to_degrees(value) -> float:
    """Convert an exifread GPS ratio triplet (deg, min, sec) to decimal degrees."""
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)
    return d + (m / 60.0) + (s / 3600.0)


def _extract_gps(tags) -> tuple[float, float] | None:
    """Pull a (latitude, longitude) pair out of exifread tags, or None if absent."""
    required = (
        "GPS GPSLatitude", "GPS GPSLatitudeRef",
        "GPS GPSLongitude", "GPS GPSLongitudeRef",
    )
    if not all(key in tags for key in required):
        return None

    lat = _convert_to_degrees(tags["GPS GPSLatitude"])
    if tags["GPS GPSLatitudeRef"].values[0] != "N":
        lat = -lat

    lon = _convert_to_degrees(tags["GPS GPSLongitude"])
    if tags["GPS GPSLongitudeRef"].values[0] != "E":
        lon = -lon

    return round(lat, 6), round(lon, 6)


def analyse(filepath) -> dict:
    """Extract metadata from an image file and return it as a label -> value dict."""
    path = Path(filepath)
    result = {
        "File name": path.name,
        "File size": f"{path.stat().st_size / 1024:.1f} KB",
    }

    # --- Basic info via Pillow ---
    with Image.open(path) as img:
        result["Format"] = img.format
        result["Dimensions"] = f"{img.width} x {img.height} px"
        result["Colour mode"] = img.mode

    # --- Detailed EXIF via exifread ---
    with open(path, "rb") as f:
        tags = exifread.process_file(f, details=False)

    if not tags:
        result["EXIF data"] = "None found (metadata likely stripped or never present)"
        return result

    make = tags.get("Image Make")
    model = tags.get("Image Model")
    if make or model:
        result["Camera"] = f"{make or ''} {model or ''}".strip()

    date_taken = tags.get("EXIF DateTimeOriginal") or tags.get("Image DateTime")
    if date_taken:
        result["Date taken"] = str(date_taken)

    software = tags.get("Image Software")
    if software:
        result["Software"] = str(software)

    gps = _extract_gps(tags)
    if gps:
        lat, lon = gps
        result["GPS coordinates"] = f"{lat}, {lon}"
        result["Map link"] = f"https://maps.google.com/?q={lat},{lon}"
    else:
        result["GPS coordinates"] = "Not present"

    return result
