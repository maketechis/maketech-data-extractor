from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.core import Campaign, CampaignLocation, CampaignStatus, LocationStatus
from app.orchestrator.runner import run_next_district

def campaign_stats(db: Session, campaign_id: int) -> dict:
    rows=db.execute(
        select(CampaignLocation.status,func.count(CampaignLocation.id))
        .where(CampaignLocation.campaign_id==campaign_id)
        .group_by(CampaignLocation.status)
    ).all()
    counts={status.value:count for status,count in rows}
    return {
        "pending":counts.get("pending",0),"running":counts.get("running",0),
        "completed":counts.get("completed",0),"failed":counts.get("failed",0),
        "total":sum(counts.values()),
    }

def retry_failed(db: Session, campaign_id: int, max_attempts: int=2) -> int:
    rows=db.scalars(select(CampaignLocation).where(
        CampaignLocation.campaign_id==campaign_id,
        CampaignLocation.status==LocationStatus.FAILED,
        CampaignLocation.attempts < max_attempts,
    )).all()
    for row in rows:
        row.status=LocationStatus.PENDING
        row.last_error=None
        row.completed_at=None
    db.commit()
    return len(rows)

def run_campaign(db: Session, campaign_id: int, *, adapters=None, max_districts: int=1, max_attempts: int=2):
    campaign=db.get(Campaign,campaign_id)
    if not campaign: raise ValueError("Campaign not found")
    if campaign.status==CampaignStatus.PAUSED:
        return {"campaign_id":campaign_id,"status":"paused","stats":campaign_stats(db,campaign_id)}
    campaign.status=CampaignStatus.RUNNING; db.commit()
    processed=[]; limit=max(1,max_districts)
    for _ in range(limit):
        result=run_next_district(db,campaign_id,adapters)
        if result["status"]=="no_pending_districts":
            if retry_failed(db,campaign_id,max_attempts):
                continue
            break
        processed.append(result)
    stats=campaign_stats(db,campaign_id)
    if stats["pending"]==0 and stats["running"]==0:
        campaign.status=CampaignStatus.COMPLETED if stats["failed"]==0 else CampaignStatus.FAILED
    db.commit()
    return {"campaign_id":campaign_id,"status":campaign.status.value,"processed":processed,"stats":stats}
