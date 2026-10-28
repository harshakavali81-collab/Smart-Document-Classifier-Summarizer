# API

Local Python: http://localhost:8000/docs ; Docker: http://localhost:8080

**POST /api/v1/analyze** takes multipart field file, PDF with selectable text or UTF-8 TXT. Successful result fields: filename, category, confidence, alternatives, page_count, word_count, summary (array with text and page), note and latency_ms. Page numbers start at 1. The score is uncalibrated and the summary is extractive.

Error responses: 400 missing filename; 413 oversized upload; 415 unsupported extension; 422 invalid, empty, textless, encrypted or too-large extracted document.

**GET /api/v1/analytics** returns total_analyses, average_latency_ms, pages_processed, categories, days, data_note. This measures operational usage, not model quality.

**GET /api/v1/health** describes runtime status and offline processing mode. OpenAPI specification is at /openapi.json.

No API authentication is included; do not deploy publicly without additional security.
