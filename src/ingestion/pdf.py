"""Page-preserving ingestion with bounded work and no OCR or external services."""
import fitz

from src.security.validation import MAX_CHARS


class DocumentError(ValueError):
    """Input cannot be safely interpreted as a supported document."""


def extract_pages(filename: str, raw: bytes, max_pages: int = 50) -> list[dict]:
    if filename.lower().endswith(".txt"):
        try:
            value = raw.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise DocumentError("Text documents must use UTF-8 encoding.") from exc
        if len(value) > MAX_CHARS:
            raise DocumentError(f"Extracted text exceeds the {MAX_CHARS:,}-character limit.")
        return [{"page": 1, "text": value.strip()}]
    if not filename.lower().endswith(".pdf") or not raw.startswith(b"%PDF-"):
        raise DocumentError("Upload a valid PDF or UTF-8 .txt file.")
    try:
        with fitz.open(stream=raw, filetype="pdf") as doc:
            if doc.is_encrypted:
                raise DocumentError("Password-protected PDFs are not supported.")
            if doc.page_count > max_pages:
                raise DocumentError(f"PDF exceeds the {max_pages}-page limit.")
            pages = []
            total_chars = 0
            for number, page in enumerate(doc, 1):
                page_text = page.get_text("text").strip()
                total_chars += len(page_text)
                if total_chars > MAX_CHARS:
                    raise DocumentError(f"Extracted text exceeds the {MAX_CHARS:,}-character limit.")
                pages.append({"page": number, "text": page_text})
            return pages
    except DocumentError:
        raise
    except Exception as exc:
        raise DocumentError("PDF could not be safely read.") from exc
