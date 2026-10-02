from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.core import Country, District, EntityType, State

def ensure_development_seed(db: Session):
    india=db.scalar(select(Country).where(Country.iso_code=="IN"))
    if not india:
        india=Country(name="India",iso_code="IN"); db.add(india); db.flush()
    bihar=db.scalar(select(State).where(State.country_id==india.id, State.name=="Bihar"))
    if not bihar:
        bihar=State(country_id=india.id,name="Bihar",code="BR"); db.add(bihar); db.flush()
    siwan=db.scalar(select(District).where(District.state_id==bihar.id, District.name=="Siwan"))
    if not siwan:
        siwan=District(state_id=bihar.id,name="Siwan",normalized_name="siwan"); db.add(siwan); db.flush()
    bookseller=db.scalar(select(EntityType).where(EntityType.slug=="bookseller"))
    if not bookseller:
        bookseller=EntityType(name="Bookseller",slug="bookseller"); db.add(bookseller); db.flush()
    school=db.scalar(select(EntityType).where(EntityType.slug=="school"))
    if not school:
        school=EntityType(name="School",slug="school"); db.add(school); db.flush()
    db.commit()
    return {"country_id":india.id,"state_id":bihar.id,"district_id":siwan.id,"bookseller_type_id":bookseller.id,"school_type_id":school.id}

def bootstrap_core(db: Session):
    before_countries = 1 if db.scalar(select(Country).where(Country.iso_code=="IN")) else 0
    before_types = sum(1 for slug in ("school","bookseller") if db.scalar(select(EntityType).where(EntityType.slug==slug)))
    ensure_development_seed(db)
    return {"countries": 1-before_countries, "entity_types": 2-before_types}
