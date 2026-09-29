from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.core import Campaign, CampaignLocation
from app.orchestrator.runner import run_next_district

router=APIRouter(prefix="/jobs",tags=["jobs"])

def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/campaigns/{campaign_id}/run-next")
def run_next(campaign_id:int,db:Session=Depends(get_db)):
    if not db.get(Campaign,campaign_id): raise HTTPException(404,"Campaign not found")
    return run_next_district(db,campaign_id)

@router.get("/campaigns/{campaign_id}/locations")
def locations(campaign_id:int,db:Session=Depends(get_db)):
    rows=db.scalars(select(CampaignLocation).where(CampaignLocation.campaign_id==campaign_id).order_by(CampaignLocation.id)).all()
    return [{"district_id":x.district_id,"status":x.status.value,"attempts":x.attempts,"records_found":x.records_found,"records_saved":x.records_saved,"last_error":x.last_error} for x in rows]
