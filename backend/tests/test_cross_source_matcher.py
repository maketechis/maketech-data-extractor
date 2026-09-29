from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.collector.matcher import find_existing_entity
from app.collector.types import RawEntity
from app.database import Base
from app.models.core import Country,District,Entity,EntityContact,EntityType,State

def test_phone_and_similar_name_merge():
    engine=create_engine("sqlite:///:memory:"); Base.metadata.create_all(engine)
    with Session(engine) as db:
        c=Country(name="India",iso_code="IN"); t=EntityType(name="Bookseller",slug="bookseller"); db.add_all([c,t]); db.flush()
        s=State(country_id=c.id,name="Bihar"); db.add(s); db.flush(); d=District(state_id=s.id,name="Siwan",normalized_name="siwan"); db.add(d); db.flush()
        e=Entity(entity_type_id=t.id,name="ABC Book House",normalized_name="abc book house",country_id=c.id,state_id=s.id,district_id=d.id,pin="841226"); db.add(e); db.flush()
        db.add(EntityContact(entity_id=e.id,contact_type="phone",value="9876543210")); db.commit()
        raw=RawEntity(name="A.B.C. Book House",pin="841226",phone="+91 98765 43210",source_name="second",source_url="https://source.example/2")
        match=find_existing_entity(db,record=raw,entity_type_id=t.id,district_id=d.id)
        assert match.entity_id==e.id
        assert match.decision=="merge"
        assert "phone" in match.evidence
