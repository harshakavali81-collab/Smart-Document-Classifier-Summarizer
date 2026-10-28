# Quick local startup instructions for Windows PowerShell (Python 3.11+, Node 20+).
$ErrorActionPreference = "Stop"
Write-Host "DocSight AI - local development setup" -ForegroundColor Cyan
if (!(Test-Path ".venv")) { python -m venv .venv }
$py = Join-Path (Get-Location) ".venv\Scripts\python.exe"
& $py -m pip install -r requirements-dev.txt
Write-Host "Python environment ready. Install frontend packages next..." -ForegroundColor Green
Push-Location frontend
try { npm install --no-audit --no-fund } finally { Pop-Location }
Write-Host "Open two PowerShell terminals in the repository root:" -ForegroundColor Yellow
Write-Host '  Terminal 1: .venv\Scripts\python.exe -m uvicorn backend.app.main:app --port 8000'
Write-Host '  Terminal 2: cd frontend; npm run dev'
Write-Host "Then open http://localhost:5173 (API docs: http://localhost:8000/docs)"
Write-Host "Or use Docker Compose instead: docker compose up --build"
