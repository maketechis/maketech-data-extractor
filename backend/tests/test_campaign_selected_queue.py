from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.database import Base
from app.models.core import Campaign,Country,District,EntityType,State
from app.orchestrator.service import build_district_queue
def test_queue_can_target_one_district():
    e=create_engine("sqlite:///:memory:");Base.metadata.create_all(e)
    with Session(e) as db:
        c=Country(name="India",iso_code="IN");t=EntityType(name="School",slug="school");db.add_all([c,t]);db.flush();s=State(country_id=c.id,name="Bihar");db.add(s);db.flush();a=District(state_id=s.id,name="Siwan",normalized_name="siwan");b=District(state_id=s.id,name="Patna",normalized_name="patna");db.add_all([a,b]);db.flush();campaign=Campaign(name="test",entity_type_id=t.id,country_id=c.id);db.add(campaign);db.commit();assert build_district_queue(db,campaign,[a.id])==1
