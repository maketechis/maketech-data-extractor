from fastapi import APIRouter,Depends,Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.history import ExtractionEvent,ExtractionRun

router=APIRouter(prefix="/history",tags=["history"])

def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/runs")
def runs(campaign_id:int|None=None,district_id:int|None=None,limit:int=Query(100,ge=1,le=500),db:Session=Depends(get_db)):
    stmt=select(ExtractionRun).order_by(ExtractionRun.id.desc()).limit(limit)
    if campaign_id: stmt=stmt.where(ExtractionRun.campaign_id==campaign_id)
    if district_id: stmt=stmt.where(ExtractionRun.district_id==district_id)
    return [{"id":x.id,"campaign_id":x.campaign_id,"district_id":x.district_id,"type":x.run_type,"status":x.status,"started_at":x.started_at,"completed_at":x.completed_at,"raw_count":x.raw_count,"saved_count":x.saved_count,"error":x.error} for x in db.scalars(stmt).all()]

@router.get("/entities/{entity_id}")
def entity_history(entity_id:int,limit:int=Query(200,ge=1,le=1000),db:Session=Depends(get_db)):
    rows=db.scalars(select(ExtractionEvent).where(ExtractionEvent.entity_id==entity_id).order_by(ExtractionEvent.id.desc()).limit(limit)).all()
    return [{"id":x.id,"run_id":x.run_id,"event_type":x.event_type,"field":x.field_name,"old":x.old_value,"new":x.new_value,"source_url":x.source_url,"confidence":x.confidence,"created_at":x.created_at} for x in rows]
