from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.collector.adapters.osm_overpass import OSMOverpassAdapter
from app.collector.engine import CollectorEngine
from app.enrichment.district_job import run_district_enrichment
from app.models.core import Campaign, CampaignLocation, Country, District, EntityType, LocationStatus, State

def utcnow(): return datetime.now(timezone.utc)

def process_district(db: Session, campaign: Campaign, location: CampaignLocation, *, adapters=None, enrichment_limit=25, max_pages=5):
    district=db.get(District,location.district_id); state=db.get(State,location.state_id)
    country=db.get(Country,campaign.country_id); entity_type=db.get(EntityType,campaign.entity_type_id)
    location.status=LocationStatus.COLLECTING; location.started_at=location.started_at or utcnow(); location.attempts+=1; db.commit()
    try:
        collected=CollectorEngine(adapters or [OSMOverpassAdapter()]).collect(db=db,entity_type=entity_type,country=country,state=state,district=district)
        location.records_found=collected["raw"]; location.records_saved=collected["saved"]
        location.status=LocationStatus.ENRICHING; db.commit()
        enriched=run_district_enrichment(db,district.id,limit=enrichment_limit,max_pages=max_pages)
        location.status=LocationStatus.COMPLETED; location.completed_at=utcnow(); location.last_error=None; db.commit()
        unresolved=enriched["counts"].get("needs_discovery",0)+enriched["counts"].get("needs_review",0)+enriched["counts"].get("partial",0)
        return {"district_id":district.id,"district":district.name,"status":"completed","collection":collected,"enrichment":enriched["counts"],"unresolved_entities":unresolved}
    except Exception as exc:
        location.status=LocationStatus.FAILED; location.completed_at=utcnow(); location.last_error=f"{type(exc).__name__}: {str(exc)[:500]}"; db.commit()
        return {"district_id":district.id,"district":district.name,"status":"failed","error_type":type(exc).__name__}
