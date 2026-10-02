from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.database import Base
from app.models.core import Country,District,Entity,EntityType,State
from app.models.school import SchoolProfile
from app.api.school_data import coverage
def test_school_coverage_counts_udise():
    e=create_engine("sqlite:///:memory:");Base.metadata.create_all(e)
    with Session(e) as db:
        c=Country(name="India",iso_code="IN");t=EntityType(name="School",slug="school");db.add_all([c,t]);db.flush();s=State(country_id=c.id,name="Bihar");db.add(s);db.flush();d=District(state_id=s.id,name="Siwan",normalized_name="siwan");db.add(d);db.flush();a=Entity(entity_type_id=t.id,name="A",normalized_name="a",country_id=c.id,state_id=s.id,district_id=d.id);b=Entity(entity_type_id=t.id,name="B",normalized_name="b",country_id=c.id,state_id=s.id,district_id=d.id);db.add_all([a,b]);db.flush();db.add(SchoolProfile(entity_id=a.id,udise_code="123"));db.commit();x=coverage(db=db);assert x["schools"]==2 and x["with_udise"]==1
