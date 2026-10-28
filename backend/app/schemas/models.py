from pydantic import BaseModel, Field

class Evidence(BaseModel):
    text: str
    page: int = Field(ge=1)

class Alternative(BaseModel):
    label: str
    confidence: float

class AnalysisResponse(BaseModel):
    filename: str
    category: str
    confidence: float
    alternatives: list[Alternative]
    page_count: int
    word_count: int
    summary: list[Evidence]
    note: str
    latency_ms: float
