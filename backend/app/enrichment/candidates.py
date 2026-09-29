from dataclasses import dataclass
from urllib.parse import urlparse
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.core import District, Entity, EntityWebsite, State

@dataclass(frozen=True, slots=True)
class WebsiteCandidate:
    url: str
    source_url: str
    source_name: str
    title: str | None = None
    snippet: str | None = None

def normalize_candidate_url(url: str) -> tuple[str,str]:
    value=url.strip()
    if not value.startswith(("http://","https://")): value="https://"+value
    parsed=urlparse(value)
    if not parsed.netloc: raise ValueError("Invalid candidate URL")
    domain=parsed.netloc.lower().removeprefix("www.")
    return parsed.geturl(),domain

def candidate_query(db: Session, entity: Entity) -> str:
    district=db.get(District,entity.district_id) if entity.district_id else None
    state=db.get(State,entity.state_id) if entity.state_id else None
    parts=[f'"{entity.name}"']
    if district: parts.append(district.name)
    if state: parts.append(state.name)
    if entity.pin: parts.append(entity.pin)
    return " ".join(parts)

def store_candidate(db: Session, entity: Entity, candidate: WebsiteCandidate) -> EntityWebsite:
    url,domain=normalize_candidate_url(candidate.url)
    existing=db.scalar(select(EntityWebsite).where(EntityWebsite.entity_id==entity.id,EntityWebsite.domain==domain))
    if existing: return existing
    row=EntityWebsite(entity_id=entity.id,url=url,domain=domain,confidence=0.0,verification_status="candidate")
    db.add(row); db.commit(); db.refresh(row)
    return row
