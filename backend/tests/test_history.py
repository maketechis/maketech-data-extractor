from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.database import Base
from app.models.core import Campaign,CampaignLocation,Country,District,EntityType,LocationStatus,State
from app.services.history import finish_campaign_run,start_campaign_run

def test_campaign_history_snapshot():
    engine=create_engine("sqlite:///:memory:"); Base.metadata.create_all(engine)
    with Session(engine) as db:
        c=Country(name="India",iso_code="IN"); et=EntityType(name="Bookseller",slug="bookseller"); db.add_all([c,et]); db.flush()
        s=State(country_id=c.id,name="Bihar"); db.add(s); db.flush(); d=District(state_id=s.id,name="Siwan",normalized_name="siwan"); db.add(d); db.flush()
        campaign=Campaign(name="India Books",entity_type_id=et.id,country_id=c.id); db.add(campaign); db.flush()
        db.add(CampaignLocation(campaign_id=campaign.id,state_id=s.id,district_id=d.id,status=LocationStatus.COMPLETED,records_found=20,records_saved=15)); db.commit()
        run=start_campaign_run(db,campaign.id); finish_campaign_run(db,run,"completed")
        assert run.districts_completed==1 and run.records_found==20 and run.records_saved==15
