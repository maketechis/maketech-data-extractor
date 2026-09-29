from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.collector.types import RawEntity
from app.database import Base
from app.models.core import Campaign, Country, District, EntityType, State
from app.orchestrator.service import build_district_queue
from app.orchestrator.runner import run_next_district

class FakeAdapter:
    name="fake"
    def collect(self,**kwargs):
        yield RawEntity(name="Test Book House",phone="9876543210",source_name="fixture",source_url="https://example.test/1")

def test_run_next_district_completes_and_persists():
    engine=create_engine("sqlite:///:memory:"); Base.metadata.create_all(engine)
    with Session(engine) as db:
        c=Country(name="India",iso_code="IN"); t=EntityType(name="Bookseller",slug="bookseller"); db.add_all([c,t]); db.flush()
        s=State(country_id=c.id,name="Bihar",code="BR"); db.add(s); db.flush()
        d=District(state_id=s.id,name="Siwan",normalized_name="siwan"); db.add(d); db.flush()
        campaign=Campaign(name="Test",entity_type_id=t.id,country_id=c.id); db.add(campaign); db.commit(); db.refresh(campaign)
        build_district_queue(db,campaign)
        result=run_next_district(db,campaign.id,[FakeAdapter()])
        assert result["status"]=="completed"
        assert result["saved"]==1
        assert run_next_district(db,campaign.id,[FakeAdapter()])["status"]=="no_pending_districts"
