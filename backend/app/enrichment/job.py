from dataclasses import dataclass
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.enrichment.needs import detect_missing_fields
from app.enrichment.verified_site import enrich_from_website
from app.models.core import Entity, EntityWebsite

ACCEPTED_WEBSITE_STATUSES=("verified","likely")

@dataclass(slots=True)
class EnrichmentJobResult:
    entity_id: int
    status: str
    before: list[str]
    after: list[str]
    website_id: int | None = None
    pages_crawled: int = 0
    values_found: int = 0
    added: int = 0

def _fields(db: Session, entity: Entity) -> list[str]:
    return [x.field for x in detect_missing_fields(db,entity)]

def best_accepted_website(db: Session, entity_id: int):
    return db.scalar(
        select(EntityWebsite)
        .where(EntityWebsite.entity_id==entity_id,EntityWebsite.verification_status.in_(ACCEPTED_WEBSITE_STATUSES))
        .order_by(EntityWebsite.confidence.desc(),EntityWebsite.id)
        .limit(1)
    )

def run_entity_enrichment(db: Session, entity_id: int, *, max_pages: int=5) -> EnrichmentJobResult:
    entity=db.get(Entity,entity_id)
    if not entity: raise ValueError("Entity not found")
    before=_fields(db,entity)
    if not before:
        return EnrichmentJobResult(entity_id,"complete",[],[])
    website=best_accepted_website(db,entity.id)
    if not website:
        candidates=db.scalars(select(EntityWebsite).where(EntityWebsite.entity_id==entity.id,EntityWebsite.verification_status=="candidate")).all()
        status="needs_review" if candidates else "needs_discovery"
        return EnrichmentJobResult(entity.id,status,before,before)
    crawl=enrich_from_website(db,website,max_pages=max_pages)
    db.refresh(entity)
    after=_fields(db,entity)
    if not after: status="complete"
    elif set(after)==set(before): status="partial"
    else: status="partial"
    return EnrichmentJobResult(entity.id,status,before,after,website.id,crawl["pages_crawled"],crawl["values_found"],crawl["added"])
