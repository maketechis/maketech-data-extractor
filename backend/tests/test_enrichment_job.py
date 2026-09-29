from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.database import Base
from app.enrichment.job import run_entity_enrichment
from app.models.core import Country, District, Entity, EntityType, State

def test_job_requests_discovery_when_no_website():
    engine=create_engine("sqlite:///:memory:"); Base.metadata.create_all(engine)
    with Session(engine) as db:
        c=Country(name="India",iso_code="IN"); t=EntityType(name="Bookseller",slug="bookseller"); db.add_all([c,t]); db.flush()
        s=State(country_id=c.id,name="Bihar"); db.add(s); db.flush()
        d=District(state_id=s.id,name="Siwan",normalized_name="siwan"); db.add(d); db.flush()
        e=Entity(entity_type_id=t.id,name="ABC Books",normalized_name="abc books",country_id=c.id,state_id=s.id,district_id=d.id)
        db.add(e); db.commit(); db.refresh(e)
        result=run_entity_enrichment(db,e.id)
        assert result.status=="needs_discovery"
        assert {"phone","email","website","address","pin"}.issubset(set(result.before))
