from fastapi import APIRouter,Depends,HTTPException,Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.history import CampaignRun,CampaignRunDistrict

router=APIRouter(prefix="/campaign-history",tags=["campaign-history"])

def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()

@router.get("")
def history(limit:int=Query(100,ge=1,le=500),db:Session=Depends(get_db)):
    rows=db.scalars(select(CampaignRun).order_by(CampaignRun.id.desc()).limit(limit)).all()
    return [{"run_id":x.id,"campaign_id":x.campaign_id,"status":x.status,"started_at":x.started_at,"completed_at":x.completed_at,"districts_total":x.districts_total,"districts_completed":x.districts_completed,"districts_failed":x.districts_failed,"records_found":x.records_found,"records_saved":x.records_saved} for x in rows]

@router.get("/{run_id}")
def run_detail(run_id:int,db:Session=Depends(get_db)):
    run=db.get(CampaignRun,run_id)
    if not run: raise HTTPException(404,"Campaign run not found")
    districts=db.scalars(select(CampaignRunDistrict).where(CampaignRunDistrict.campaign_run_id==run.id).order_by(CampaignRunDistrict.id)).all()
    return {"run":{"id":run.id,"campaign_id":run.campaign_id,"status":run.status,"started_at":run.started_at,"completed_at":run.completed_at,"records_found":run.records_found,"records_saved":run.records_saved},"districts":[{"district_id":x.district_id,"status":x.status,"attempts":x.attempts,"records_found":x.records_found,"records_saved":x.records_saved,"last_error":x.last_error} for x in districts]}
