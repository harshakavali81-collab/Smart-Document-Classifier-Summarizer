"""Exercise neglected validation branches without adding sensitive sample data."""
import asyncio
import io

import fitz
import pytest
from fastapi import HTTPException, UploadFile
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.routes.documents import analyze_document
from backend.app.services.analyze import analyze
from src.ingestion.pdf import DocumentError, extract_pages
from src.security.validation import MAX_CHARS, UploadError, validate_upload


def test_parser_rejects_unrecognized_pdf_signature():
    with pytest.raises(DocumentError, match="valid PDF"):
        extract_pages("invalid.pdf", b"wrong document header")


def test_validation_rejects_invalid_pdf_signature():
    with pytest.raises(UploadError, match="Invalid PDF signature"):
        validate_upload("fake.pdf", b"not a pdf")


def test_parser_rejects_password_protected_pdf():
    document = fitz.open()
    document.new_page().insert_text((50, 80), "Protected financial document")
    raw = document.tobytes(
        encryption=fitz.PDF_ENCRYPT_AES_256, owner_pw="local-test-owner", user_pw="local-test-user"
    )
    document.close()
    with pytest.raises(DocumentError, match="Password-protected"):
        extract_pages("encrypted.pdf", raw)


def test_parser_enforces_text_limit_while_extracting(monkeypatch):
    class FakePage:
        def get_text(self, mode):
            assert mode == "text"
            return "A" * (MAX_CHARS + 1)

    class FakePdf:
        is_encrypted = False
        page_count = 1

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def __iter__(self):
            yield FakePage()

    monkeypatch.setattr("src.ingestion.pdf.fitz.open", lambda **kwargs: FakePdf())
    with pytest.raises(DocumentError, match="character limit"):
        extract_pages("large.pdf", b"%PDF-1.7\n")


def test_second_character_limit_blocks_untrusted_parser_result(monkeypatch):
    monkeypatch.setattr(
        "backend.app.services.analyze.extract_pages",
        lambda *args, **kwargs: [{"page": 1, "text": "X" * (MAX_CHARS + 1)}],
    )
    with pytest.raises(ValueError, match="150,000-character limit"):
        analyze("short.txt", b"Document input has enough words to be validated for processing.")


def test_too_short_text_is_rejected():
    with pytest.raises(ValueError, match="Not enough text"):
        analyze("short.txt", b"Two or three words.")


def test_api_requires_filename_for_upload():
    payload = UploadFile(filename="", file=io.BytesIO(b"example data"))
    with pytest.raises(HTTPException) as raised:
        asyncio.run(analyze_document(payload))
    assert raised.value.status_code == 400


def test_analytics_write_failure_does_not_discard_user_result(monkeypatch):
    def broken_analytics(_result):
        raise RuntimeError("Local metadata database unavailable")

    monkeypatch.setattr("backend.app.routes.documents.record", broken_analytics)
    sentence = ("This business report describes quarterly operations and performance. "
                "The management team recorded delivery milestones and risks. "
                "The summary recommends routine status meetings and better coordination.")
    response = TestClient(app).post(
        "/api/v1/analyze", files={"file": ("synthetic.txt", sentence.encode(), "text/plain")}
    )
    assert response.status_code == 200, response.text
    assert response.json()["summary"]

