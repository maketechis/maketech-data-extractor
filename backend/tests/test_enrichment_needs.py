from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.database import Base
from app.enrichment.needs import detect_missing_fields
from app.models.core import Country, District, Entity, EntityContact, EntityType, EntityWebsite, State

def test_detects_only_missing_fields():
    engine=create_engine("sqlite:///:memory:"); Base.metadata.create_all(engine)
    with Session(engine) as db:
        c=Country(name="India",iso_code="IN"); t=EntityType(name="Bookseller",slug="bookseller"); db.add_all([c,t]); db.flush()
        s=State(country_id=c.id,name="Bihar"); db.add(s); db.flush()
        d=District(state_id=s.id,name="Siwan",normalized_name="siwan"); db.add(d); db.flush()
        e=Entity(entity_type_id=t.id,name="ABC Books",normalized_name="abc books",country_id=c.id,state_id=s.id,district_id=d.id,address="Main Road",pin=None)
        db.add(e); db.flush()
        db.add(EntityContact(entity_id=e.id,contact_type="phone",value="9876543210"))
        db.add(EntityWebsite(entity_id=e.id,url="https://example.com",domain="example.com"))
        db.commit()
        fields={x.field for x in detect_missing_fields(db,e)}
        assert fields=={"email","pin"}
