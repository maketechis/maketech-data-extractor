import csv
from io import StringIO
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.core import District, Entity, EntityContact, EntityWebsite, State

def build_csv(db: Session, *, district_id: int|None=None) -> str:
    stmt=select(Entity).order_by(Entity.id)
    if district_id: stmt=stmt.where(Entity.district_id==district_id)
    out=StringIO(); writer=csv.writer(out)
    writer.writerow(["id","name","state","district","address","pin","phone","email","website","verification_status"])
    for e in db.scalars(stmt).all():
        state=db.get(State,e.state_id) if e.state_id else None; district=db.get(District,e.district_id) if e.district_id else None
        cs=db.scalars(select(EntityContact).where(EntityContact.entity_id==e.id)).all(); sites=db.scalars(select(EntityWebsite).where(EntityWebsite.entity_id==e.id).order_by(EntityWebsite.confidence.desc())).all()
        best=sites[0] if sites else None
        writer.writerow([e.id,e.name,state.name if state else "",district.name if district else "",e.address or "",e.pin or "","; ".join(x.value for x in cs if x.contact_type=="phone"),"; ".join(x.value for x in cs if x.contact_type=="email"),best.url if best else "",best.verification_status if best else ""])
    return out.getvalue()
