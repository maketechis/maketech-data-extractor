from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.core import Campaign, CampaignStatus
from app.orchestrator.service import build_district_queue
from app.schemas.campaign import CampaignCreate, CampaignRead

router = APIRouter(prefix="/campaigns", tags=["campaigns"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=CampaignRead, status_code=201)
def create_campaign(payload: CampaignCreate, db: Session = Depends(get_db)):
    campaign = Campaign(**payload.model_dump(), status=CampaignStatus.DRAFT)
    db.add(campaign); db.commit(); db.refresh(campaign)
    return campaign

@router.post("/{campaign_id}/queue")
def queue_campaign(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.get(Campaign, campaign_id)
    if not campaign:
        raise HTTPException(404, "Campaign not found")
    created = build_district_queue(db, campaign)
    return {"campaign_id": campaign.id, "status": campaign.status.value, "district_jobs_created": created}
