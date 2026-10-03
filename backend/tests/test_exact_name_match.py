from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.database import Base
from app.collector.matcher import find_existing_entity
from app.collector.types import RawEntity
from app.models.core import Country,District,Entity,EntityType,State
def test_exact_normalized_name_same_district_merges():
    eng=create_engine("sqlite:///:memory:");Base.metadata.create_all(eng)
    with Session(eng) as db:
        c=Country(name="India",iso_code="IN");t=EntityType(name="School",slug="school");db.add_all([c,t]);db.flush();s=State(country_id=c.id,name="Bihar");db.add(s);db.flush();d=District(state_id=s.id,name="Siwan",normalized_name="siwan");db.add(d);db.flush();e=Entity(entity_type_id=t.id,name="Orbit Public School",normalized_name="orbit public school",country_id=c.id,state_id=s.id,district_id=d.id);db.add(e);db.commit()
        r=RawEntity(name="ORBIT PUBLIC SCHOOL",source_name="x",source_url="https://x")
        x=find_existing_entity(db,record=r,entity_type_id=t.id,district_id=d.id)
        assert x.decision=="merge" and x.entity_id==e.id
