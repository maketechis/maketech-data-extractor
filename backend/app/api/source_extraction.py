from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel,HttpUrl
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.core import Country,District,EntityType,State
from app.source_extraction.service import extract_source
from app.source_extraction.persist import persist_extracted
router=APIRouter(prefix="/source-extraction",tags=["source-extraction"])
def get_db():
    db=SessionLocal()
    try:yield db
    finally:db.close()
class ExtractRequest(BaseModel):url:HttpUrl
class PersistRequest(BaseModel):
    url:HttpUrl;entity_type:str="school";country:str="India";state:str="Bihar";district:str="Siwan"
@router.post("")
def extract(payload:ExtractRequest):
    try:return extract_source(str(payload.url))
    except Exception as exc:raise HTTPException(502,f"Source extraction failed: {type(exc).__name__}") from exc
@router.post("/persist")
def persist(payload:PersistRequest,db:Session=Depends(get_db)):
    try:data=extract_source(str(payload.url))
    except Exception as exc:raise HTTPException(502,f"Source extraction failed: {type(exc).__name__}") from exc
    et=db.scalar(select(EntityType).where(EntityType.slug==payload.entity_type));country=db.scalar(select(Country).where(Country.name==payload.country));state=db.scalar(select(State).where(State.country_id==country.id,State.name==payload.state)) if country else None;district=db.scalar(select(District).where(District.state_id==state.id,District.name==payload.district)) if state else None
    if not all((et,country,state,district)):raise HTTPException(404,"Entity type or geography not found")
    result=persist_extracted(db,data["records"],entity_type=et,country=country,state=state,district=district)
    return {"source":data["url"],"kind":data["kind"],"extracted":data["count"],"persistence":result}
