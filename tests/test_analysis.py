import fitz
import pytest
from src.summarization.extractive import summarize
from src.ingestion.pdf import extract_pages, DocumentError
from backend.app.services.analyze import analyze

TEXT = ("Quarterly business report outlines company performance and key operational indicators. "
        "The operations team tracked milestones and reviewed delivery risks during the quarter. "
        "Management recommends a weekly project review to reduce recurring service delays.")

def test_evidence_is_substring_of_cited_page():
    pages = [{"page": 1, "text": TEXT}, {"page": 2, "text": "The report concludes that delivery planning needs stronger oversight. " * 2}]
    for evidence in summarize(pages):
        original = next(p["text"] for p in pages if p["page"] == evidence["page"])
        assert evidence["text"] in original

def test_txt_analysis():
    result = analyze("sample.txt", TEXT.encode())
    assert result["page_count"] == 1
    assert result["summary"] and all(x["page"] == 1 for x in result["summary"])
    assert result["category"] in {"Report", "Uncertain"}

def test_pdf_page_links():
    pdf = fitz.open()
    for text in [TEXT, "Legal contract defines the parties, confidentiality and contractual obligations. " * 2]:
        p = pdf.new_page()
        p.insert_text((50, 75), text[:125])
    raw = pdf.tobytes()
    pdf.close()
    pages = extract_pages("document.pdf", raw)
    assert len(pages) == 2
    for item in summarize(pages):
        assert item["text"] in pages[item["page"]-1]["text"]

def test_scan_only_rejected():
    blank = fitz.open()
    blank.new_page()
    raw = blank.tobytes()
    blank.close()
    with pytest.raises(ValueError, match="No selectable text"):
        analyze("scan.pdf", raw)

def test_corrupt_file_rejected():
    with pytest.raises(ValueError):
        analyze("x.pdf", b"%PDF-broken")

def test_bad_extension():
    with pytest.raises(ValueError):
        analyze("x.exe", b"pretend executable file")

def test_too_many_bytes():
    with pytest.raises(ValueError):
        analyze("x.txt", b"hello " * 1_100_000)
