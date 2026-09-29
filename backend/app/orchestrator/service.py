from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.core import Campaign, CampaignLocation, CampaignStatus, District, LocationStatus, State

def build_district_queue(db: Session, campaign: Campaign) -> int:
    if campaign.collection_level != "district":
        raise ValueError("Only district collection is supported in V1")
    rows = db.execute(
        select(District.id, District.state_id)
        .join(State, District.state_id == State.id)
        .where(State.country_id == campaign.country_id)
        .order_by(State.name, District.name)
    ).all()
    existing = set(db.scalars(select(CampaignLocation.district_id).where(CampaignLocation.campaign_id == campaign.id)).all())
    created = 0
    for district_id, state_id in rows:
        if district_id in existing:
            continue
        db.add(CampaignLocation(campaign_id=campaign.id,state_id=state_id,district_id=district_id,status=LocationStatus.PENDING))
        created += 1
    campaign.status = CampaignStatus.QUEUED
    db.commit()
    return created

def next_pending_location(db: Session, campaign_id: int):
    return db.scalar(
        select(CampaignLocation)
        .where(CampaignLocation.campaign_id == campaign_id, CampaignLocation.status == LocationStatus.PENDING)
        .order_by(CampaignLocation.id)
        .limit(1)
        .with_for_update(skip_locked=True)
    )
