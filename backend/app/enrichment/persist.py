from sqlalchemy import select
from sqlalchemy.orm import Session
from app.enrichment.contact_extractor import ExtractedValue
from app.models.core import Entity, EntityContact

def persist_extracted_values(db: Session, entity: Entity, values: list[ExtractedValue]) -> dict:
    added=0
    for item in values:
        if item.field in ("phone","email"):
            exists=db.scalar(select(EntityContact.id).where(EntityContact.entity_id==entity.id,EntityContact.contact_type==item.field,EntityContact.value==item.value))
            if not exists:
                db.add(EntityContact(entity_id=entity.id,contact_type=item.field,value=item.value,source_url=item.source_url,confidence=item.confidence,verified=item.confidence>=0.95)); added+=1
        elif item.field=="address" and not entity.address:
            entity.address=item.value; added+=1
        elif item.field=="pin" and not entity.pin:
            entity.pin=item.value; added+=1
    db.commit()
    return {"added":added}
