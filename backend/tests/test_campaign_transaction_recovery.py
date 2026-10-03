from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.database import Base
from app.models.core import Campaign,CampaignLocation,CampaignStatus,Country,District,EntityType,LocationStatus,State
from app.orchestrator.full_campaign import run_next_full_district
def test_pipeline_failure_rolls_back_and_marks_campaign_failed(monkeypatch):
    engine=create_engine("sqlite:///:memory:");Base.metadata.create_all(engine)
    with Session(engine) as db:
        c=Country(name="India",iso_code="IN");t=EntityType(name="School",slug="school");db.add_all([c,t]);db.flush();s=State(country_id=c.id,name="Bihar");db.add(s);db.flush();d=District(state_id=s.id,name="Siwan",normalized_name="siwan");db.add(d);db.flush();camp=Campaign(name="x",entity_type_id=t.id,country_id=c.id,status=CampaignStatus.QUEUED);db.add(camp);db.flush();loc=CampaignLocation(campaign_id=camp.id,state_id=s.id,district_id=d.id,status=LocationStatus.PENDING);db.add(loc);db.commit()
        monkeypatch.setattr("app.orchestrator.full_campaign.cleanup_invalid_source_entities",lambda *a,**k:{"invalid_entities_removed":0,"search_websites_removed":0})
        monkeypatch.setattr("app.orchestrator.full_campaign.merge_exact_duplicates",lambda db:{"duplicates_merged":0})
        monkeypatch.setattr("app.orchestrator.full_campaign.run_simple_source_pipeline",lambda *a,**k:(_ for _ in ()).throw(RuntimeError("source boom")))
        result=run_next_full_district(db,camp.id)
        db.refresh(camp);db.refresh(loc)
        assert result["status"]=="failed" and camp.status==CampaignStatus.FAILED and loc.status==LocationStatus.FAILED
        assert "source boom" in loc.last_error
