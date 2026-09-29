from dataclasses import dataclass
from difflib import SequenceMatcher
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.collector.normalizer import normalize_name, normalize_phone
from app.collector.types import RawEntity
from app.models.core import Entity, EntityContact, EntityWebsite

@dataclass(frozen=True, slots=True)
class EntityMatch:
    entity_id: int | None
    score: int
    decision: str
    evidence: list[str]

def _name_similarity(a:str,b:str)->float:
    return SequenceMatcher(None,normalize_name(a),normalize_name(b)).ratio()

def find_existing_entity(db:Session,*,record:RawEntity,entity_type_id:int,district_id:int)->EntityMatch:
    candidates=db.scalars(select(Entity).where(Entity.entity_type_id==entity_type_id,Entity.district_id==district_id)).all()
    best=EntityMatch(None,0,"new",[])
    raw_phone=normalize_phone(record.phone)
    raw_domain=None
    if record.website:
        from urllib.parse import urlparse
        value=record.website if "://" in record.website else "https://"+record.website
        raw_domain=urlparse(value).netloc.lower().removeprefix("www.")
    for entity in candidates:
        score=0; evidence=[]; sim=_name_similarity(record.name,entity.name)
        if sim>=0.95: score+=45; evidence.append("name_exact")
        elif sim>=0.82: score+=30; evidence.append("name_similar")
        if record.pin and entity.pin and record.pin==entity.pin: score+=20; evidence.append("pin")
        if raw_phone:
            phones=db.scalars(select(EntityContact.value).where(EntityContact.entity_id==entity.id,EntityContact.contact_type=="phone")).all()
            if raw_phone in {normalize_phone(x) for x in phones}: score+=40; evidence.append("phone")
        if raw_domain:
            domains=db.scalars(select(EntityWebsite.domain).where(EntityWebsite.entity_id==entity.id)).all()
            if raw_domain in {x.lower().removeprefix("www.") for x in domains}: score+=40; evidence.append("domain")
        score=min(score,100)
        decision="merge" if score>=70 else "review" if score>=50 else "new"
        if score>best.score: best=EntityMatch(entity.id,score,decision,evidence)
    return best
