from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.core import Country, District, State

router = APIRouter(prefix="/geography", tags=["geography"])

def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/countries")
def countries(db: Session=Depends(get_db)):
    return [{"id":x.id,"name":x.name,"iso_code":x.iso_code} for x in db.scalars(select(Country).order_by(Country.name)).all()]

@router.get("/countries/{country_id}/states")
def states(country_id:int, db:Session=Depends(get_db)):
    return [{"id":x.id,"name":x.name,"code":x.code} for x in db.scalars(select(State).where(State.country_id==country_id).order_by(State.name)).all()]

@router.get("/states/{state_id}/districts")
def districts(state_id:int, db:Session=Depends(get_db)):
    return [{"id":x.id,"name":x.name} for x in db.scalars(select(District).where(District.state_id==state_id).order_by(District.name)).all()]
