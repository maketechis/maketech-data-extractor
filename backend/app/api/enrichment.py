from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.enrichment.planner import plan_district_enrichment
from app.models.core import Entity
from app.enrichment.needs import detect_missing_fields

router=APIRouter(prefix="/enrichment",tags=["enrichment"])

def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/entities/{entity_id}/needs")
def entity_needs(entity_id:int,db:Session=Depends(get_db)):
    entity=db.get(Entity,entity_id)
    if not entity: return {"entity_id":entity_id,"found":False,"needs":[]}
    return {"entity_id":entity.id,"found":True,"needs":[{"field":x.field,"reason":x.reason} for x in detect_missing_fields(db,entity)]}

@router.get("/districts/{district_id}/plan")
def district_plan(district_id:int,limit:int=Query(100,ge=1,le=500),db:Session=Depends(get_db)):
    items=plan_district_enrichment(db,district_id,limit)
    return {"district_id":district_id,"entities_needing_enrichment":len(items),"items":items}
