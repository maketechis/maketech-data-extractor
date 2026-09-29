from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.database import Base
from app.models.core import Campaign, Country, District, EntityType, State
from app.orchestrator.service import build_district_queue

def test_builds_district_queue():
    engine=create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        india=Country(name="India",iso_code="IN"); school=EntityType(name="School",slug="school")
        db.add_all([india,school]); db.flush()
        bihar=State(country_id=india.id,name="Bihar",code="BR"); db.add(bihar); db.flush()
        db.add_all([District(state_id=bihar.id,name="Siwan",normalized_name="siwan"),District(state_id=bihar.id,name="Patna",normalized_name="patna")])
        campaign=Campaign(name="India Schools",entity_type_id=school.id,country_id=india.id)
        db.add(campaign); db.commit(); db.refresh(campaign)
        assert build_district_queue(db,campaign)==2
        assert build_district_queue(db,campaign)==0
