"""Manual end-to-end smoke test of a locally running FastAPI server."""
import json
import sys
from pathlib import Path

import httpx


def main(base_url: str = "http://127.0.0.1:8000") -> None:
    base_url = base_url.rstrip("/")
    sample = Path("data/samples/example_report.txt")
    with httpx.Client(timeout=25) as client:
        health = client.get(base_url + "/api/v1/health")
        health.raise_for_status()
        with sample.open("rb") as stream:
            response = client.post(base_url + "/api/v1/analyze",
                                   files={"file": ("example_report.txt", stream, "text/plain")})
        response.raise_for_status()
        result = response.json()
        if not result.get("summary") or result.get("page_count") != 1:
            raise AssertionError("Unexpected page evidence for sample report")
        metrics = client.get(base_url + "/api/v1/analytics")
        metrics.raise_for_status()
        print(json.dumps({"health": health.json()["status"], "category": result["category"],
                          "summary_excerpts": len(result["summary"]),
                          "analytics_count": metrics.json()["total_analyses"]}, indent=2))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000")
