from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.core import CampaignStatus
from app.models.history import CampaignRun
from app.services.history import finish_campaign_run, snapshot_campaign_run, start_campaign_run

def get_or_start_active_run(db:Session,campaign_id:int):
    run=db.scalar(select(CampaignRun).where(CampaignRun.campaign_id==campaign_id,CampaignRun.status=="running").order_by(CampaignRun.id.desc()).limit(1))
    return run or start_campaign_run(db,campaign_id)

def sync_run(db:Session,run:CampaignRun,campaign_status:CampaignStatus):
    if campaign_status in (CampaignStatus.COMPLETED,CampaignStatus.FAILED,CampaignStatus.CANCELLED):
        return finish_campaign_run(db,run,campaign_status.value)
    return snapshot_campaign_run(db,run)
