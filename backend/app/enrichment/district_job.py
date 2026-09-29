from sqlalchemy import select
from sqlalchemy.orm import Session
from app.enrichment.job import run_entity_enrichment
from app.models.core import Entity

def run_district_enrichment(db: Session, district_id: int, *, limit: int=100, max_pages: int=5):
    entities=db.scalars(select(Entity).where(Entity.district_id==district_id).order_by(Entity.id).limit(limit)).all()
    results=[]; counts={"complete":0,"partial":0,"needs_discovery":0,"needs_review":0}
    for entity in entities:
        result=run_entity_enrichment(db,entity.id,max_pages=max_pages)
        counts[result.status]=counts.get(result.status,0)+1
        results.append(result)
    return {"district_id":district_id,"processed":len(results),"counts":counts,"results":[r.__dict__ for r in results]}
