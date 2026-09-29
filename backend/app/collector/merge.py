from sqlalchemy import select
from sqlalchemy.orm import Session
from app.collector.normalizer import normalize_email, normalize_phone, normalize_website
from app.collector.types import RawEntity
from app.models.core import Entity, EntityContact, EntitySource, EntityWebsite

def merge_record(db:Session,entity:Entity,record:RawEntity):
    if not entity.address and record.address: entity.address=record.address
    if not entity.pin and record.pin: entity.pin=record.pin
    for kind,value in (("phone",normalize_phone(record.phone)),("email",normalize_email(record.email))):
        if value and not db.scalar(select(EntityContact.id).where(EntityContact.entity_id==entity.id,EntityContact.contact_type==kind,EntityContact.value==value)):
            db.add(EntityContact(entity_id=entity.id,contact_type=kind,value=value,source_url=record.source_url,verified=False))
    website=normalize_website(record.website)
    if website:
        from urllib.parse import urlparse
        domain=urlparse(website).netloc.lower().removeprefix("www.")
        if not db.scalar(select(EntityWebsite.id).where(EntityWebsite.entity_id==entity.id,EntityWebsite.domain==domain)):
            db.add(EntityWebsite(entity_id=entity.id,url=website,domain=domain,verification_status="unverified"))
    if not db.scalar(select(EntitySource.id).where(EntitySource.entity_id==entity.id,EntitySource.source_url==record.source_url,EntitySource.source_record_id==record.source_record_id)):
        db.add(EntitySource(entity_id=entity.id,source_type=record.source_name,source_url=record.source_url,source_record_id=record.source_record_id))
    db.flush()
    return entity
