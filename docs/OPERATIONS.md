# Operations runbook — local prototype

## Start

From repo root: \`docker compose up --build -d\`; visit http://localhost:8080. To run without Docker use Python 3.11+ and Node 20+, following README. Test \`curl http://localhost:8080/api/v1/health\`.

## Verify

- \`pytest -q\` for Python unit/integration tests.
- \`python -m scripts.evaluate\` then \`python -m scripts.make_eval_charts\` for synthetic metrics and charts.
- \`python -m scripts.smoke_api http://localhost:8080\` for the live Docker Compose API through Nginx.
- \`cd frontend && npm install && npm run build\` for React compile.
- \`docker compose config -q\` to check service definition.

## Troubleshoot

- **No selectable text:** this tool deliberately does not OCR scanned PDFs.
- **422 upload rejected:** inspect file extension, 6 MiB limit, 50-page limit, encryption, text length and UTF-8.
- **Backend unavailable:** check \`docker compose ps\` and \`docker compose logs backend\`.
- **Analytics empty:** only completed API requests increment counts; local SQLite begins empty. A failed write leaves analysis working but telemetry absent.
- **Frontend blank/404:** confirm both containers are healthy and try http://localhost:8080 rather than assuming GitHub Pages hosts the Python service.

## Backups and deletion

SQLite operational metadata lives in a persistent Docker named volume. Back up it only when the service is stopped and handle as potentially sensitive metadata. To deliberately erase the local database, run \`docker compose down -v\` (this is destructive). There is no per-user deletion endpoint because the prototype lacks user accounts.

## Public release gate

Do **not** expose this prototype publicly for sensitive documents until identity, authorization, rate limiting, isolated PDF parsing, malware detection, encryption, retention compliance, observability, load testing and independent real-world model evaluation are complete. GitHub Actions success confirms tests/build only, not production readiness.
