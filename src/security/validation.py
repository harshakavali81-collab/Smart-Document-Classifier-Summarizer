"""Upload validation and predictable resource limits."""
MAX_BYTES = 6 * 1024 * 1024
MAX_CHARS = 150_000
MAX_PAGES = 50

class UploadError(ValueError):
    pass

def validate_upload(filename: str, data: bytes) -> None:
    if not filename or not filename.lower().endswith((".pdf", ".txt")):
        raise UploadError("Only .pdf and .txt documents are accepted.")
    if not data:
        raise UploadError("Document is empty.")
    if len(data) > MAX_BYTES:
        raise UploadError("Document exceeds the 6 MiB size limit.")
    if filename.lower().endswith(".pdf") and not data.startswith(b"%PDF-"):
        raise UploadError("Invalid PDF signature.")
