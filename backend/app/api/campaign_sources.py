from fastapi import APIRouter,Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.core import CampaignSource
router=APIRouter(prefix="/campaign-sources",tags=["campaign-sources"])
def get_db():
    db=SessionLocal()
    try:yield db
    finally:db.close()
@router.get("/{campaign_id}")
def sources(campaign_id:int,db:Session=Depends(get_db)):
    rows=db.scalars(select(CampaignSource).where(CampaignSource.campaign_id==campaign_id).order_by(CampaignSource.page_number,CampaignSource.rank)).all()
    return [{"id":x.id,"engine":x.engine,"query":x.query,"page":x.page_number,"rank":x.rank,"title":x.title,"url":x.url,"status":x.status,"raw":x.records_raw,"accepted":x.records_accepted,"saved":x.records_saved,"error":x.last_error} for x in rows]
