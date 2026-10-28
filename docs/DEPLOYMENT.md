# Deployment

From the repository root run: docker compose up --build

Then open http://localhost:8080 . Nginx serves React and reverse-proxies /api to FastAPI. Operational metadata is stored in the Docker named volume docsight-data. The command docker compose down -v permanently removes that volume.

For development, install Python dependencies and start uvicorn backend.app.main:app --reload; use cd frontend && npm install && npm run dev for the UI.

GitHub Actions builds and tests source but does **not** provision a hosted application. For public full-stack hosting, authentication, HTTPS, rate limiting, parser sandboxing, real-world ML evaluation, monitoring and operational approvals remain external tasks. GitHub Pages alone cannot serve FastAPI.
