from fastapi import APIRouter,Depends,HTTPException,Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.core import Entity,EntityContact,EntitySource,EntityType,EntityWebsite,District,State
router=APIRouter(prefix="/ui",tags=["ui"])
def get_db():
    db=SessionLocal()
    try:yield db
    finally:db.close()
def entity_row(db,e):
    et=db.get(EntityType,e.entity_type_id);d=db.get(District,e.district_id) if e.district_id else None;s=db.get(State,e.state_id) if e.state_id else None
    contacts=db.scalars(select(EntityContact).where(EntityContact.entity_id==e.id)).all();sites=db.scalars(select(EntityWebsite).where(EntityWebsite.entity_id==e.id)).all();sources=db.scalars(select(EntitySource).where(EntitySource.entity_id==e.id)).all()
    return {"id":e.id,"name":e.name,"type":et.name if et else None,"status":e.status,"state":s.name if s else None,"district":d.name if d else None,"address":e.address,"pin":e.pin,"phones":[x.value for x in contacts if x.contact_type=="phone"],"emails":[x.value for x in contacts if x.contact_type=="email"],"websites":[{"url":x.url,"status":x.verification_status} for x in sites],"source_count":len(sources)}
@router.get("/entities")
def entities(status:str|None=None,limit:int=Query(200,ge=1,le=500),db:Session=Depends(get_db)):
    q=select(Entity).order_by(Entity.id.desc()).limit(limit)
    if status:q=q.where(Entity.status==status)
    return [entity_row(db,e) for e in db.scalars(q).all()]
@router.get("/entities/{entity_id}")
def entity(entity_id:int,db:Session=Depends(get_db)):
    e=db.get(Entity,entity_id)
    if not e:raise HTTPException(404,"Entity not found")
    return entity_row(db,e)
