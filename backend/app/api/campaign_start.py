from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.core import Campaign
from app.orchestrator.full_campaign import run_next_full_district
router=APIRouter(prefix="/campaign-start",tags=["campaign-start"])
def get_db():
    db=SessionLocal()
    try:yield db
    finally:db.close()
@router.post("/{campaign_id}")
def start(campaign_id:int,db:Session=Depends(get_db)):
    if not db.get(Campaign,campaign_id):raise HTTPException(404,"Campaign not found")
    return run_next_full_district(db,campaign_id)
