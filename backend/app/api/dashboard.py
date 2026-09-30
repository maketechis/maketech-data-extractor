from fastapi import APIRouter,Depends
from sqlalchemy import func,select
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.core import Campaign,CampaignStatus,Entity
router=APIRouter(prefix="/dashboard",tags=["dashboard"])
def get_db():
    db=SessionLocal()
    try:yield db
    finally:db.close()
@router.get("/summary")
def summary(db:Session=Depends(get_db)):
    campaigns=db.scalar(select(func.count(Campaign.id))) or 0
    entities=db.scalar(select(func.count(Entity.id))) or 0
    review=db.scalar(select(func.count(Entity.id)).where(Entity.status=="needs_review")) or 0
    completed=db.scalar(select(func.count(Campaign.id)).where(Campaign.status==CampaignStatus.COMPLETED)) or 0
    return {"campaigns":campaigns,"entities":entities,"needs_review":review,"completed":completed}
