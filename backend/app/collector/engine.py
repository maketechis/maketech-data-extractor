from sqlalchemy.orm import Session
from app.collector.deduplicator import deduplicate
from app.collector.matcher import find_existing_entity
from app.collector.merge import merge_record
from app.collector.normalizer import normalize_email, normalize_name, normalize_phone, normalize_website
from app.models.core import Entity, EntityContact, EntitySource, EntityWebsite

class CollectorEngine:
    def __init__(self, adapters):
        self.adapters=adapters

    def collect(self, *, db: Session, entity_type, country, state, district):
        raw=[]
        for adapter in self.adapters:
            raw.extend(adapter.collect(entity_type=entity_type.slug,district=district.name,state=state.name,country=country.name))
        records=deduplicate(raw)
        saved=merged=review=0
        for record in records:
            match=find_existing_entity(db,record=record,entity_type_id=entity_type.id,district_id=district.id)
            if match.decision=="merge" and match.entity_id:
                merge_record(db,db.get(Entity,match.entity_id),record); merged+=1; continue
            if match.decision=="review":
                review+=1
            entity=Entity(entity_type_id=entity_type.id,name=record.name,normalized_name=normalize_name(record.name),country_id=country.id,state_id=state.id,district_id=district.id,address=record.address,pin=record.pin,status="needs_review" if match.decision=="review" else "active")
            db.add(entity); db.flush()
            merge_record(db,entity,record); saved+=1
        db.commit()
        return {"raw":len(raw),"unique":len(records),"saved":saved,"merged":merged,"needs_review":review}
