from sqlalchemy import func,select
from sqlalchemy.orm import Session
from app.enrichment.needs import detect_missing_fields
from app.models.core import District,Entity,EntityContact,EntitySource,EntityType,EntityWebsite,State
from app.models.school import SchoolProfile

def school_benchmark(db:Session,*,state_name:str="Bihar",district_name:str="Siwan")->dict:
    school_type=db.scalar(select(EntityType).where(EntityType.slug=="school"))
    state=db.scalar(select(State).where(State.name==state_name))
    district=db.scalar(select(District).where(District.state_id==state.id,District.name==district_name)) if state else None
    if not school_type or not district: raise ValueError("School entity type or geography not found")
    entities=db.scalars(select(Entity).where(Entity.entity_type_id==school_type.id,Entity.district_id==district.id)).all()
    ids=[e.id for e in entities]; total=len(ids)
    if not total:
        return {"state":state_name,"district":district_name,"unique_schools":0,"coverage":{},"sources":[],"unresolved":0}
    profiles=db.scalars(select(SchoolProfile).where(SchoolProfile.entity_id.in_(ids))).all()
    profile_by_entity={x.entity_id:x for x in profiles}
    phones=set(db.scalars(select(EntityContact.entity_id).where(EntityContact.entity_id.in_(ids),EntityContact.contact_type=="phone")).all())
    emails=set(db.scalars(select(EntityContact.entity_id).where(EntityContact.entity_id.in_(ids),EntityContact.contact_type=="email")).all())
    websites=set(db.scalars(select(EntityWebsite.entity_id).where(EntityWebsite.entity_id.in_(ids))).all())
    verified=set(db.scalars(select(EntityWebsite.entity_id).where(EntityWebsite.entity_id.in_(ids),EntityWebsite.verification_status=="verified")).all())
    unresolved=sum(bool(detect_missing_fields(db,e)) for e in entities)
    source_rows=db.execute(select(EntitySource.source_type,func.count(func.distinct(EntitySource.entity_id))).where(EntitySource.entity_id.in_(ids)).group_by(EntitySource.source_type)).all()
    def metric(count): return {"count":count,"percent":round(count*100/total,2)}
    udise=sum(bool(profile_by_entity.get(i) and profile_by_entity[i].udise_code) for i in ids)
    return {"state":state_name,"district":district_name,"unique_schools":total,
        "coverage":{"udise":metric(udise),"phone":metric(len(phones)),"email":metric(len(emails)),"website":metric(len(websites)),"verified_website":metric(len(verified))},
        "sources":[{"source":name,"entities":count} for name,count in source_rows],"unresolved":unresolved}
