from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.collector.adapters.osm_overpass import OSMOverpassAdapter
from app.collector.engine import CollectorEngine
from app.database import SessionLocal
from app.models.core import Country, District, Entity, EntityType, State

router=APIRouter(prefix="/collector",tags=["collector"])

def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/run")
def run_collection(entity_type:str,country_id:int,state_id:int,district_id:int,db:Session=Depends(get_db)):
    et=db.get(EntityType,entity_type) if entity_type.isdigit() else db.scalar(select(EntityType).where(EntityType.slug==entity_type))
    country=db.get(Country,country_id); state=db.get(State,state_id); district=db.get(District,district_id)
    if not all([et,country,state,district]): raise HTTPException(404,"Entity type or geography not found")
    if state.country_id!=country.id or district.state_id!=state.id: raise HTTPException(400,"Geography hierarchy mismatch")
    try:
        return CollectorEngine([OSMOverpassAdapter()]).collect(db=db,entity_type=et,country=country,state=state,district=district)
    except Exception as exc:
        raise HTTPException(502,f"Live source failed: {type(exc).__name__}") from exc

@router.get("/entities")
def list_entities(entity_type:str|None=None,district_id:int|None=None,limit:int=100,db:Session=Depends(get_db)):
    stmt=select(Entity).order_by(Entity.name).limit(min(limit,500))
    if district_id: stmt=stmt.where(Entity.district_id==district_id)
    if entity_type:
        et=db.scalar(select(EntityType).where(EntityType.slug==entity_type))
        if not et: return []
        stmt=stmt.where(Entity.entity_type_id==et.id)
    return [{"id":x.id,"name":x.name,"address":x.address,"pin":x.pin,"district_id":x.district_id} for x in db.scalars(stmt).all()]
