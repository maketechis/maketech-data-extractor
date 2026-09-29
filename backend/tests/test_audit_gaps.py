from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.database import Base
from app.enrichment.district_job import run_district_enrichment
from app.models.core import Country,District,Entity,EntityType,State

def test_district_enrichment_filters_entity_type():
    engine=create_engine("sqlite:///:memory:"); Base.metadata.create_all(engine)
    with Session(engine) as db:
        c=Country(name="India",iso_code="IN"); a=EntityType(name="Bookseller",slug="bookseller"); b=EntityType(name="School",slug="school"); db.add_all([c,a,b]); db.flush()
        s=State(country_id=c.id,name="Bihar"); db.add(s); db.flush(); d=District(state_id=s.id,name="Siwan",normalized_name="siwan"); db.add(d); db.flush()
        db.add_all([Entity(entity_type_id=a.id,name="Books",normalized_name="books",country_id=c.id,state_id=s.id,district_id=d.id),Entity(entity_type_id=b.id,name="School",normalized_name="school",country_id=c.id,state_id=s.id,district_id=d.id)]); db.commit()
        result=run_district_enrichment(db,d.id,entity_type_id=a.id)
        assert result["processed"]==1
