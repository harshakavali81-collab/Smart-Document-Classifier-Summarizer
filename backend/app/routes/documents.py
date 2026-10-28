from fastapi import APIRouter, File, UploadFile, HTTPException
from starlette.concurrency import run_in_threadpool
from backend.app.schemas.models import AnalysisResponse
from backend.app.services.analyze import analyze
from backend.app.db.store import record, dashboard
from src.ingestion.pdf import DocumentError
from src.security.validation import UploadError, MAX_BYTES

router = APIRouter(prefix="/api/v1", tags=["document-analysis"])

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Provide a file name.")
    if not file.filename.lower().endswith((".pdf", ".txt")):
        raise HTTPException(status_code=415, detail="Only PDF and UTF-8 TXT files are accepted.")
    payload = await file.read(MAX_BYTES + 1)
    await file.close()
    if len(payload) > MAX_BYTES:
        raise HTTPException(status_code=413, detail="The upload exceeds 6 MiB.")
    try:
        result = await run_in_threadpool(analyze, file.filename, payload)
    except (UploadError, DocumentError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    try:
        await run_in_threadpool(record, result)
    except Exception:
        # Analytics is nonessential; do not log document bytes or raw text.
        pass
    return result

@router.get("/analytics")
def analytics():
    return dashboard()
