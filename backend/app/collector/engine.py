from sqlalchemy.orm import Session
from app.collector.deduplicator import deduplicate
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
        saved=0
        for record in records:
            entity=Entity(entity_type_id=entity_type.id,name=record.name,normalized_name=normalize_name(record.name),country_id=country.id,state_id=state.id,district_id=district.id,address=record.address,pin=record.pin)
            db.add(entity); db.flush()
            db.add(EntitySource(entity_id=entity.id,source_type=record.source_name,source_url=record.source_url,source_record_id=record.source_record_id))
            for kind,value in (("phone",normalize_phone(record.phone)),("email",normalize_email(record.email))):
                if value: db.add(EntityContact(entity_id=entity.id,contact_type=kind,value=value,source_url=record.source_url,verified=False))
            website=normalize_website(record.website)
            if website:
                from urllib.parse import urlparse
                db.add(EntityWebsite(entity_id=entity.id,url=website,domain=urlparse(website).netloc.lower(),verification_status="unverified"))
            saved+=1
        db.commit()
        return {"raw":len(raw),"unique":len(records),"saved":saved}
