from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.collector.types import RawEntity
from app.database import Base
from app.models.core import Campaign, Country, District, EntityType, State
from app.orchestrator.campaign_loop import run_campaign
from app.orchestrator.service import build_district_queue

class FakeAdapter:
    name="fake"
    def collect(self,**kwargs):
        yield RawEntity(name=f"Books {kwargs['district']}",source_name="fixture",source_url="https://example.test")

def test_campaign_processes_multiple_districts():
    engine=create_engine("sqlite:///:memory:"); Base.metadata.create_all(engine)
    with Session(engine) as db:
        country=Country(name="India",iso_code="IN"); et=EntityType(name="Bookseller",slug="bookseller"); db.add_all([country,et]); db.flush()
        state=State(country_id=country.id,name="Bihar"); db.add(state); db.flush()
        db.add_all([District(state_id=state.id,name="Siwan",normalized_name="siwan"),District(state_id=state.id,name="Patna",normalized_name="patna")]); db.flush()
        campaign=Campaign(name="Bihar Books",entity_type_id=et.id,country_id=country.id); db.add(campaign); db.commit(); db.refresh(campaign)
        build_district_queue(db,campaign)
        result=run_campaign(db,campaign.id,adapters=[FakeAdapter()],max_districts=10)
        assert result["status"]=="completed"
        assert result["stats"]["completed"]==2
        assert len(result["processed"])==2
