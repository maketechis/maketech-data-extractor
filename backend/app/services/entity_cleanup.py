from sqlalchemy import select
from sqlalchemy.orm import Session
from app.collector.merge import merge_record
from app.collector.normalizer import normalize_name
from app.models.core import Entity,EntityContact,EntitySource,EntityWebsite
def merge_exact_duplicates(db:Session)->dict:
    rows=db.scalars(select(Entity).order_by(Entity.id)).all();keepers={};merged=0
    for e in rows:
        key=(e.entity_type_id,e.district_id,normalize_name(e.name))
        if key not in keepers:keepers[key]=e;continue
        keep=keepers[key]
        for x in db.scalars(select(EntityContact).where(EntityContact.entity_id==e.id)).all():
            if not db.scalar(select(EntityContact.id).where(EntityContact.entity_id==keep.id,EntityContact.contact_type==x.contact_type,EntityContact.value==x.value)):x.entity_id=keep.id
            else:db.delete(x)
        for x in db.scalars(select(EntityWebsite).where(EntityWebsite.entity_id==e.id)).all():
            if not db.scalar(select(EntityWebsite.id).where(EntityWebsite.entity_id==keep.id,EntityWebsite.domain==x.domain)):x.entity_id=keep.id
            else:db.delete(x)
        for x in db.scalars(select(EntitySource).where(EntitySource.entity_id==e.id)).all():x.entity_id=keep.id
        if not keep.address and e.address:keep.address=e.address
        if not keep.pin and e.pin:keep.pin=e.pin
        db.delete(e);merged+=1
    db.flush();return {"duplicates_merged":merged}
