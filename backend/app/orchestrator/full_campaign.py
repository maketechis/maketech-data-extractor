from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.core import Campaign, CampaignLocation, CampaignStatus, LocationStatus
from app.orchestrator.campaign_loop import campaign_stats
from app.orchestrator.district_pipeline import process_district

def run_next_full_district(db: Session, campaign_id: int, *, adapters=None, enrichment_limit=25, max_pages=5):
    campaign=db.get(Campaign,campaign_id)
    if not campaign: raise ValueError("Campaign not found")
    if campaign.status==CampaignStatus.PAUSED: return {"campaign_id":campaign_id,"status":"paused"}
    location=db.scalar(select(CampaignLocation).where(CampaignLocation.campaign_id==campaign_id,CampaignLocation.status==LocationStatus.PENDING).order_by(CampaignLocation.id).limit(1).with_for_update(skip_locked=True))
    if not location:
        stats=campaign_stats(db,campaign_id)
        if stats["pending"]==0 and stats["running"]==0:
            campaign.status=CampaignStatus.COMPLETED if stats["failed"]==0 else CampaignStatus.FAILED; db.commit()
        return {"campaign_id":campaign_id,"status":"no_pending_districts","stats":stats}
    campaign.status=CampaignStatus.RUNNING; db.commit()
    result=process_district(db,campaign,location,adapters=adapters,enrichment_limit=enrichment_limit,max_pages=max_pages)
    return {"campaign_id":campaign_id,**result,"campaign_stats":campaign_stats(db,campaign_id)}
