from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.database import Base
from app.models.core import Campaign,CampaignSource,CampaignStatus,Country,District,EntityType,State
from app.orchestrator.simple_source_pipeline import discover_and_store
def test_discovery_saves_serp_sources(monkeypatch):
    engine=create_engine("sqlite:///:memory:");Base.metadata.create_all(engine)
    class Hit:
        title="School directory";url="https://example.org/siwan-schools";page=3;rank=2
    monkeypatch.setattr("app.orchestrator.simple_source_pipeline.search_google_pages",lambda q,pages,delay_seconds=20:([Hit()],[{"page":1,"status":"success","results":1,"error":None}]))
    with Session(engine) as db:
        c=Country(name="India",iso_code="IN");t=EntityType(name="School",slug="school");db.add_all([c,t]);db.flush();s=State(country_id=c.id,name="Bihar");db.add(s);db.flush();d=District(state_id=s.id,name="Siwan",normalized_name="siwan");db.add(d);db.flush();camp=Campaign(name="x",entity_type_id=t.id,country_id=c.id,status=CampaignStatus.QUEUED);db.add(camp);db.commit()
        x=discover_and_store(db,camp,d,5);row=db.query(CampaignSource).one()
        assert x["sources_saved"]==1 and row.page_number==3 and row.rank==2 and row.url==Hit.url
