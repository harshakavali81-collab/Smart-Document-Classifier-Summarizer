from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)
SAMPLE = ("Monthly business report summarizes company revenue and operational performance. "
          "The management team reviewed milestones, risks and outstanding delivery tasks. "
          "The report recommends a weekly status meeting to improve project coordination.")

def test_health():
    assert client.get("/api/v1/health").json()["status"] == "ok"

def test_upload_txt(tmp_path, monkeypatch):
    monkeypatch.setenv("ANALYTICS_DB", str(tmp_path / "usage.db"))
    res = client.post("/api/v1/analyze", files={"file": ("demo.txt", SAMPLE.encode(), "text/plain")})
    assert res.status_code == 200, res.text
    data = res.json()
    assert data["page_count"] == 1 and data["summary"][0]["page"] == 1
    assert client.get("/api/v1/analytics").json()["total_analyses"] == 1

def test_reject_unsupported():
    res = client.post("/api/v1/analyze", files={"file": ("virus.exe", b"data", "application/octet-stream")})
    assert res.status_code == 415

def test_reject_empty():
    res = client.post("/api/v1/analyze", files={"file": ("empty.txt", b"", "text/plain")})
    assert res.status_code == 422

def test_reject_large():
    res = client.post("/api/v1/analyze", files={"file": ("large.txt", b"x" * (6*1024*1024+1), "text/plain")})
    assert res.status_code == 413
