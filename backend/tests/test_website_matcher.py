from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.database import Base
from app.models.core import Country, District, Entity, EntityContact, EntityType, State
from app.verification.website_matcher import score_candidate

def build(db):
    c=Country(name="India",iso_code="IN"); t=EntityType(name="School",slug="school"); db.add_all([c,t]); db.flush()
    s=State(country_id=c.id,name="Bihar"); db.add(s); db.flush()
    d=District(state_id=s.id,name="Siwan",normalized_name="siwan"); db.add(d); db.flush()
    e=Entity(entity_type_id=t.id,name="St Joseph School",normalized_name="st joseph school",country_id=c.id,state_id=s.id,district_id=d.id,pin="841238")
    db.add(e); db.flush(); db.add(EntityContact(entity_id=e.id,contact_type="phone",value="8002977006")); db.commit(); return e

def test_strong_candidate_verifies():
    engine=create_engine("sqlite:///:memory:"); Base.metadata.create_all(engine)
    with Session(engine) as db:
        e=build(db)
        r=score_candidate(db,e,"Welcome to St Joseph School, Siwan, Bihar 841238. Contact 8002977006.")
        assert r.status=="verified"
        assert r.score>=75

def test_unrelated_candidate_rejected():
    engine=create_engine("sqlite:///:memory:"); Base.metadata.create_all(engine)
    with Session(engine) as db:
        e=build(db)
        r=score_candidate(db,e,"Completely unrelated business in Delhi.")
        assert r.status=="rejected"
