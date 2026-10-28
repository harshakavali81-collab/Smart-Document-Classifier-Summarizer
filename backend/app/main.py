import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routes.documents import router

app = FastAPI(
    title="Smart Document Classifier & Summarizer",
    description="Offline extractive page-evidence summarization with a synthetic-trained classifier.",
    version="1.0.0",
)
origins = [x.strip() for x in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",") if x.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=False,
                   allow_methods=["GET", "POST"], allow_headers=["Content-Type"])
app.include_router(router)

@app.get("/api/v1/health")
def health():
    return {"status": "ok", "classifier": "synthetic-example model", "ocr": False, "generation": "extractive"}
