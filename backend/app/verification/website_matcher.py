import re
from dataclasses import dataclass
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.collector.normalizer import normalize_name, normalize_phone
from app.models.core import District, Entity, EntityContact, EntityWebsite, State

@dataclass(frozen=True, slots=True)
class MatchResult:
    score: int
    status: str
    evidence: list[str]

def _tokens(value: str) -> set[str]:
    return {x for x in normalize_name(value).split() if len(x)>2}

def score_candidate(db: Session, entity: Entity, page_text: str) -> MatchResult:
    text=page_text.lower()
    score=0; evidence=[]
    name_tokens=_tokens(entity.name)
    matched=sum(1 for t in name_tokens if t in text)
    if name_tokens and matched/len(name_tokens)>=0.8:
        score+=35; evidence.append("name")
    elif name_tokens and matched/len(name_tokens)>=0.5:
        score+=20; evidence.append("partial_name")
    district=db.get(District,entity.district_id) if entity.district_id else None
    state=db.get(State,entity.state_id) if entity.state_id else None
    if district and district.name.lower() in text: score+=15; evidence.append("district")
    if state and state.name.lower() in text: score+=10; evidence.append("state")
    if entity.pin and entity.pin in text: score+=20; evidence.append("pin")
    contacts=db.scalars(select(EntityContact).where(EntityContact.entity_id==entity.id)).all()
    for contact in contacts:
        if contact.contact_type=="phone":
            phone=normalize_phone(contact.value)
            compact=re.sub(r"\D","",page_text)
            if phone and phone in compact: score+=15; evidence.append("phone"); break
        if contact.contact_type=="email" and contact.value.lower() in text:
            score+=15; evidence.append("email"); break
    score=min(score,100)
    if score>=75: status="verified"
    elif score>=55: status="likely"
    elif score>=30: status="needs_review"
    else: status="rejected"
    return MatchResult(score,status,evidence)

def apply_match(db: Session, website: EntityWebsite, result: MatchResult):
    website.confidence=float(result.score)
    website.verification_status=result.status
    db.commit()
    return website
