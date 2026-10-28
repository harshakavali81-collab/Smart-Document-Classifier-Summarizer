"""Adversarial boundary and privacy checks for supported document formats."""
import fitz
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.services.analyze import analyze
from src.ingestion.pdf import extract_pages, DocumentError
from src.security.validation import MAX_CHARS, MAX_PAGES, safe_filename
from src.summarization.extractive import summarize


def _pdf(pages, text="A short report describes a research experiment using measurements."):
    document = fitz.open()
    for _ in range(pages):
        page = document.new_page()
        if text:
            page.insert_text((24, 65), text)
    data = document.tobytes()
    document.close()
    return data


def test_page_limit_fails_before_text_extraction():
    with pytest.raises(DocumentError, match="50-page"):
        extract_pages("oversized.pdf", _pdf(MAX_PAGES + 1))


def test_exact_maximum_pages_allowed():
    assert len(extract_pages("valid.pdf", _pdf(MAX_PAGES))) == MAX_PAGES


def test_large_text_rejected_early():
    with pytest.raises(DocumentError, match="character limit"):
        extract_pages("many.txt", ("a" * (MAX_CHARS + 1)).encode())


def test_invalid_utf8_is_rejected():
    with pytest.raises(DocumentError, match="UTF-8"):
        extract_pages("bad.txt", bytes([255, 254, 250]))


def test_filename_path_and_controls_removed():
    name = safe_filename("../secret" + chr(13) + chr(10) + "file.txt")
    assert "/" not in name and chr(13) not in name and chr(10) not in name
    assert chr(0x202e) not in safe_filename("docs/" + chr(0x202e) + "report.pdf")
    assert safe_filename("C:\\\\fake\\\\folder\\\\report.pdf") == "report.pdf"


def test_content_not_persisted_in_usage_db(tmp_path, monkeypatch):
    monkeypatch.setenv("ANALYTICS_DB", str(tmp_path / "usage.db"))
    unique = "PRIVATE_SAMPLE_TOKEN_9a2b7c5d"
    sample = ("Quarterly business report covers operations and project risks. "
              "The management team confirmed an internal financial review. "
              "The report includes " + unique + " as a harmless local test marker.")
    response = TestClient(app).post(
        "/api/v1/analyze",
        files={"file": ("private.txt", sample.encode(), "text/plain")}
    )
    assert response.status_code == 200, response.text
    blob = (tmp_path / "usage.db").read_bytes()
    assert unique.encode() not in blob and b"private.txt" not in blob


def test_cited_text_is_exact_substring_on_multipage_input():
    pages = [
        {"page": 1, "text": "A document review team summarized operational milestones and future work. " * 3},
        {"page": 2, "text": "Research methods describe measurements with repeatable experimental conditions. " * 3},
    ]
    for item in summarize(pages, limit=8):
        assert item["text"] in pages[item["page"] - 1]["text"]


def test_no_qualifying_sentences_never_makes_up_content():
    assert summarize([{"page": 1, "text": "Yes. No."}]) == []
