from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.core import Campaign
from app.orchestrator.full_campaign import run_next_full_district

router=APIRouter(prefix="/pipeline",tags=["pipeline"])

def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/campaigns/{campaign_id}/next-district")
def next_district(campaign_id:int,enrichment_limit:int=Query(25,ge=1,le=100),max_pages:int=Query(5,ge=1,le=10),db:Session=Depends(get_db)):
    if not db.get(Campaign,campaign_id): raise HTTPException(404,"Campaign not found")
    return run_next_full_district(db,campaign_id,enrichment_limit=enrichment_limit,max_pages=max_pages)
