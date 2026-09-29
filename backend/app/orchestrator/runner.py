from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.collector.adapters.osm_overpass import OSMOverpassAdapter
from app.collector.engine import CollectorEngine
from app.models.core import Campaign, CampaignLocation, Country, District, EntityType, LocationStatus, State
from app.orchestrator.service import next_pending_location

def utcnow():
    return datetime.now(timezone.utc)

def run_next_district(db: Session, campaign_id: int, adapters=None):
    campaign=db.get(Campaign,campaign_id)
    if not campaign: raise ValueError("Campaign not found")
    location=next_pending_location(db,campaign_id)
    if not location: return {"campaign_id":campaign_id,"status":"no_pending_districts"}
    location.status=LocationStatus.RUNNING; location.started_at=utcnow(); location.attempts+=1; db.commit()
    district=db.get(District,location.district_id); state=db.get(State,location.state_id)
    country=db.get(Country,campaign.country_id); entity_type=db.get(EntityType,campaign.entity_type_id)
    try:
        location.status=LocationStatus.COLLECTING; db.commit()
        result=CollectorEngine(adapters or [OSMOverpassAdapter()]).collect(db=db,entity_type=entity_type,country=country,state=state,district=district)
        location.records_found=result["raw"]; location.records_saved=result["saved"]
        location.status=LocationStatus.COMPLETED; location.completed_at=utcnow(); location.last_error=None
        db.commit()
        return {"campaign_id":campaign_id,"district_id":district.id,"district":district.name,"status":"completed",**result}
    except Exception as exc:
        location.status=LocationStatus.FAILED; location.last_error=f"{type(exc).__name__}: {str(exc)[:500]}"; location.completed_at=utcnow(); db.commit()
        return {"campaign_id":campaign_id,"district_id":district.id,"district":district.name,"status":"failed","error_type":type(exc).__name__}
