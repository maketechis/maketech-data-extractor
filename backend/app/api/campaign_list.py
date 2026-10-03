import json
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.core import Campaign,CampaignLocation,District
from app.orchestrator.campaign_loop import campaign_stats
router=APIRouter(prefix="/campaign-runs",tags=["campaign-runs"])
def get_db():
    db=SessionLocal()
    try:yield db
    finally:db.close()
@router.get("")
def campaigns(db:Session=Depends(get_db)):
    rows=db.scalars(select(Campaign).order_by(Campaign.id.desc()).limit(50)).all()
    return [{"id":c.id,"name":c.name,"status":c.status.value,"stats":campaign_stats(db,c.id),"search":{"google":c.search_google,"bing":c.search_bing,"yahoo":c.search_yahoo,"mode":c.search_mode},"quality":{"status":c.quality_status,**(json.loads(c.quality_json) if c.quality_json else {})},"quality":{"status":c.quality_status,**(json.loads(c.quality_json) if c.quality_json else {})}} for c in rows]
@router.get("/{campaign_id}")
def detail(campaign_id:int,db:Session=Depends(get_db)):
    c=db.get(Campaign,campaign_id)
    if not c: raise HTTPException(404,"Campaign not found")
    locations=db.execute(select(CampaignLocation,District.name).join(District,District.id==CampaignLocation.district_id).where(CampaignLocation.campaign_id==campaign_id).order_by(CampaignLocation.id)).all()
    return {"id":c.id,"name":c.name,"status":c.status.value,"stats":campaign_stats(db,c.id),"districts":[{"name":name,"status":loc.status.value,"found":loc.records_found,"saved":loc.records_saved,"error":loc.last_error} for loc,name in locations]}
