"""Page-preserving PDF and UTF-8 text ingestion. No OCR or external API calls."""
import fitz

class DocumentError(ValueError):
    pass

def extract_pages(filename: str, raw: bytes, max_pages: int = 50) -> list[dict]:
    if filename.lower().endswith(".txt"):
        try:
            value = raw.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise DocumentError("Text documents must use UTF-8 encoding.") from exc
        return [{"page": 1, "text": value.strip()}]
    if not filename.lower().endswith(".pdf") or not raw.startswith(b"%PDF-"):
        raise DocumentError("Upload a valid PDF or UTF-8 .txt file.")
    try:
        with fitz.open(stream=raw, filetype="pdf") as doc:
            if doc.is_encrypted:
                raise DocumentError("Password-protected PDFs are not supported.")
            if doc.page_count > max_pages:
                raise DocumentError(f"PDF exceeds the {max_pages}-page limit.")
            pages = [{"page": n + 1, "text": page.get_text("text").strip()}
                     for n, page in enumerate(doc)]
    except DocumentError:
        raise
    except Exception as exc:
        raise DocumentError("PDF could not be safely read.") from exc
    return pages
