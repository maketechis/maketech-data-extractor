from fastapi import APIRouter,HTTPException
from pydantic import BaseModel,HttpUrl
from app.source_extraction.service import extract_source
router=APIRouter(prefix="/source-extraction",tags=["source-extraction"])
class ExtractRequest(BaseModel):url:HttpUrl
@router.post("")
def extract(payload:ExtractRequest):
    try:return extract_source(str(payload.url))
    except Exception as exc:raise HTTPException(502,f"Source extraction failed: {type(exc).__name__}") from exc
