from dataclasses import dataclass
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.core import Entity, EntityContact, EntityWebsite

@dataclass(frozen=True, slots=True)
class EnrichmentNeed:
    field: str
    reason: str

def detect_missing_fields(db: Session, entity: Entity) -> list[EnrichmentNeed]:
    contacts=db.execute(select(EntityContact.contact_type).where(EntityContact.entity_id==entity.id)).scalars().all()
    websites=db.execute(select(EntityWebsite.id).where(EntityWebsite.entity_id==entity.id)).scalars().all()
    present=set(contacts); needs=[]
    if "phone" not in present: needs.append(EnrichmentNeed("phone","No phone contact stored"))
    if "email" not in present: needs.append(EnrichmentNeed("email","No email contact stored"))
    if not websites: needs.append(EnrichmentNeed("website","No website stored"))
    if not entity.address: needs.append(EnrichmentNeed("address","No address stored"))
    if not entity.pin: needs.append(EnrichmentNeed("pin","No PIN/postal code stored"))
    return needs
