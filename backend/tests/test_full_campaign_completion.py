from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.database import Base
from app.models.core import Campaign,CampaignLocation,CampaignStatus,Country,District,EntityType,LocationStatus,State
from app.orchestrator.full_campaign import run_next_full_district
def test_last_district_finalizes_campaign(monkeypatch):
    engine=create_engine("sqlite:///:memory:");Base.metadata.create_all(engine)
    with Session(engine) as db:
        c=Country(name="India",iso_code="IN");t=EntityType(name="School",slug="school");db.add_all([c,t]);db.flush();s=State(country_id=c.id,name="Bihar");db.add(s);db.flush();d=District(state_id=s.id,name="Siwan",normalized_name="siwan");db.add(d);db.flush();camp=Campaign(name="x",entity_type_id=t.id,country_id=c.id,status=CampaignStatus.QUEUED);db.add(camp);db.flush();loc=CampaignLocation(campaign_id=camp.id,state_id=s.id,district_id=d.id,status=LocationStatus.PENDING);db.add(loc);db.commit()
        monkeypatch.setattr("app.orchestrator.full_campaign.run_simple_source_pipeline",lambda *a,**k:{"discovery":{"query":"school list","pages":5,"results":0,"sources_saved":0},"extraction":{"sources":0,"raw":0,"accepted":0,"saved":0,"failed_sources":0}})
        monkeypatch.setattr("app.orchestrator.full_campaign.merge_exact_duplicates",lambda db:{"duplicates_merged":0})
        monkeypatch.setattr("app.orchestrator.full_campaign.process_district",lambda db,campaign,location,**kw:(setattr(location,"status",LocationStatus.COMPLETED),db.commit(),{"status":"completed","collection":{"raw":0},"enrichment":{}})[-1])
        result=run_next_full_district(db,camp.id)
        db.refresh(camp)
        assert camp.status==CampaignStatus.COMPLETED
        assert result["campaign_status"]=="completed"
