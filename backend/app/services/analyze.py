"""Document analysis orchestration with zero raw-document persistence."""
from time import perf_counter
from pathlib import PurePath
from src.ingestion.pdf import extract_pages, DocumentError
from src.preprocessing.text import normalize, count_words
from src.security.validation import validate_upload, MAX_CHARS, MAX_PAGES
from src.classification.model import classify
from src.summarization.extractive import summarize

class AnalysisError(ValueError):
    pass

def analyze(filename: str, payload: bytes) -> dict:
    started = perf_counter()
    validate_upload(filename, payload)
    pages = extract_pages(filename, payload, max_pages=MAX_PAGES)
    cleaned = [{"page": p["page"], "text": normalize(p["text"])} for p in pages]
    text = "\n".join(page["text"] for page in cleaned)
    if not text.strip():
        raise AnalysisError("No selectable text found; scanned PDFs require OCR, which is not enabled.")
    if len(text) > MAX_CHARS:
        raise AnalysisError("Extracted text exceeds the 150,000-character limit.")
    if count_words(text) < 8:
        raise AnalysisError("Not enough text to classify and summarize.")
    pred = classify(text)
    evidence = summarize(cleaned)
    return {
        "filename": PurePath(filename.replace("\\", "/")).name[:120],
        "category": pred["label"], "confidence": pred["confidence"],
        "alternatives": pred["alternatives"],
        "page_count": len(cleaned), "word_count": count_words(text),
        "summary": evidence, "note": pred["model_note"],
        "latency_ms": round((perf_counter() - started) * 1000, 2),
    }
