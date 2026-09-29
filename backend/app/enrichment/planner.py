from sqlalchemy import select
from sqlalchemy.orm import Session
from app.enrichment.needs import detect_missing_fields
from app.models.core import Entity

def plan_district_enrichment(db: Session, district_id: int, limit: int=100):
    entities=db.scalars(select(Entity).where(Entity.district_id==district_id).order_by(Entity.id).limit(limit)).all()
    output=[]
    for entity in entities:
        needs=detect_missing_fields(db,entity)
        if needs:
            output.append({"entity_id":entity.id,"name":entity.name,"needs":[{"field":x.field,"reason":x.reason} for x in needs]})
    return output
