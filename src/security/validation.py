"""Hard document limits and upload format checks for the offline prototype."""
from pathlib import PurePath

MAX_BYTES = 6 * 1024 * 1024
MAX_CHARS = 150_000
MAX_PAGES = 50


class UploadError(ValueError):
    pass


def safe_filename(filename: str) -> str:
    """Remove paths and invisible controls before reflecting an uploaded filename."""
    name = PurePath(filename.replace("\\", "/")).name
    # Also replace bidi controls to avoid misleading or forged file extensions in UI.
    return "".join(c if c.isprintable() and c not in "\u202a\u202b\u202c\u202d\u202e\u2066\u2067\u2068\u2069" else "_" for c in name)[:120]


def validate_upload(filename: str, data: bytes) -> None:
    name = safe_filename(filename)
    if not name or not name.lower().endswith((".pdf", ".txt")):
        raise UploadError("Only .pdf and .txt documents are accepted.")
    if not data:
        raise UploadError("Document is empty.")
    if len(data) > MAX_BYTES:
        raise UploadError("Document exceeds the 6 MiB size limit.")
    if name.lower().endswith(".pdf") and not data.startswith(b"%PDF-"):
        raise UploadError("Invalid PDF signature.")
