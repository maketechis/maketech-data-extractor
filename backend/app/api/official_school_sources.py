from dataclasses import asdict
from fastapi import APIRouter,HTTPException
from app.services.bihar_school_sources import fetch_bssb
router=APIRouter(prefix="/official-school-sources",tags=["official-school-sources"])
@router.get("/bihar-sanskrit")
def bihar_sanskrit(district:str="Siwan"):
    try:rows=fetch_bssb(district)
    except Exception as exc:raise HTTPException(502,f"Official Bihar source unavailable: {type(exc).__name__}") from exc
    return {"source":"Bihar Sanskrit Shiksha Board","district":district,"count":len(rows),"schools":[asdict(x) for x in rows]}
