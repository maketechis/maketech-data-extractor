from fastapi import APIRouter,Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.core import EntityType
router=APIRouter(prefix="/entity-types",tags=["entity-types"])
def get_db():
    db=SessionLocal()
    try:yield db
    finally:db.close()
@router.get("")
def list_types(db:Session=Depends(get_db)):
    return [{"id":x.id,"name":x.name,"slug":x.slug} for x in db.scalars(select(EntityType).order_by(EntityType.name)).all()]
