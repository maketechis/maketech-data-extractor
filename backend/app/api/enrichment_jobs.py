from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.enrichment.district_job import run_district_enrichment
from app.enrichment.job import run_entity_enrichment

router=APIRouter(prefix="/enrichment-jobs",tags=["enrichment-jobs"])

def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/entities/{entity_id}/run")
def run_entity(entity_id:int,max_pages:int=Query(5,ge=1,le=10),db:Session=Depends(get_db)):
    try: result=run_entity_enrichment(db,entity_id,max_pages=max_pages)
    except ValueError as exc: raise HTTPException(404,str(exc)) from exc
    return result.__dict__

@router.post("/districts/{district_id}/run")
def run_district(district_id:int,limit:int=Query(25,ge=1,le=100),max_pages:int=Query(5,ge=1,le=10),db:Session=Depends(get_db)):
    return run_district_enrichment(db,district_id,limit=limit,max_pages=max_pages)
