from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.core import Campaign, CampaignStatus
from app.orchestrator.campaign_loop import campaign_stats, run_campaign

router=APIRouter(prefix="/campaign-control",tags=["campaign-control"])

def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/{campaign_id}/run")
def run(campaign_id:int,max_districts:int=Query(1,ge=1,le=10),db:Session=Depends(get_db)):
    if not db.get(Campaign,campaign_id): raise HTTPException(404,"Campaign not found")
    return run_campaign(db,campaign_id,max_districts=max_districts)

@router.post("/{campaign_id}/pause")
def pause(campaign_id:int,db:Session=Depends(get_db)):
    c=db.get(Campaign,campaign_id)
    if not c: raise HTTPException(404,"Campaign not found")
    c.status=CampaignStatus.PAUSED; db.commit()
    return {"campaign_id":c.id,"status":"paused"}

@router.post("/{campaign_id}/resume")
def resume(campaign_id:int,db:Session=Depends(get_db)):
    c=db.get(Campaign,campaign_id)
    if not c: raise HTTPException(404,"Campaign not found")
    c.status=CampaignStatus.QUEUED; db.commit()
    return {"campaign_id":c.id,"status":"queued"}

@router.get("/{campaign_id}/stats")
def stats(campaign_id:int,db:Session=Depends(get_db)):
    if not db.get(Campaign,campaign_id): raise HTTPException(404,"Campaign not found")
    return campaign_stats(db,campaign_id)
