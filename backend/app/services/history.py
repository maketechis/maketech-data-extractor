from datetime import datetime, timezone
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.core import CampaignLocation, LocationStatus
from app.models.history import CampaignRun, CampaignRunDistrict

def start_campaign_run(db:Session,campaign_id:int):
    total=db.scalar(select(func.count(CampaignLocation.id)).where(CampaignLocation.campaign_id==campaign_id)) or 0
    run=CampaignRun(campaign_id=campaign_id,status="running",districts_total=total)
    db.add(run); db.commit(); db.refresh(run); return run

def snapshot_campaign_run(db:Session,run:CampaignRun):
    locations=db.scalars(select(CampaignLocation).where(CampaignLocation.campaign_id==run.campaign_id)).all()
    db.query(CampaignRunDistrict).filter(CampaignRunDistrict.campaign_run_id==run.id).delete()
    for x in locations:
        db.add(CampaignRunDistrict(campaign_run_id=run.id,district_id=x.district_id,status=x.status.value,attempts=x.attempts,records_found=x.records_found,records_saved=x.records_saved,started_at=x.started_at,completed_at=x.completed_at,last_error=x.last_error))
    run.districts_total=len(locations); run.districts_completed=sum(x.status==LocationStatus.COMPLETED for x in locations); run.districts_failed=sum(x.status==LocationStatus.FAILED for x in locations)
    run.records_found=sum(x.records_found for x in locations); run.records_saved=sum(x.records_saved for x in locations)
    db.commit(); return run

def finish_campaign_run(db:Session,run:CampaignRun,status:str):
    snapshot_campaign_run(db,run); run.status=status; run.completed_at=datetime.now(timezone.utc); db.commit(); return run
