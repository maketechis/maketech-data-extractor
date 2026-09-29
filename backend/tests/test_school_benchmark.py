from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.benchmarks.school import school_benchmark
from app.database import Base
from app.models.core import Country,District,Entity,EntityContact,EntitySource,EntityType,EntityWebsite,State
from app.models.school import SchoolProfile

def test_siwan_school_benchmark():
    engine=create_engine("sqlite:///:memory:"); Base.metadata.create_all(engine)
    with Session(engine) as db:
        c=Country(name="India",iso_code="IN"); et=EntityType(name="School",slug="school"); db.add_all([c,et]); db.flush()
        s=State(country_id=c.id,name="Bihar"); db.add(s); db.flush(); d=District(state_id=s.id,name="Siwan",normalized_name="siwan"); db.add(d); db.flush()
        e=Entity(entity_type_id=et.id,name="ABC School",normalized_name="abc school",country_id=c.id,state_id=s.id,district_id=d.id,address="Main Road",pin="841226"); db.add(e); db.flush()
        db.add_all([SchoolProfile(entity_id=e.id,udise_code="10160000001"),EntityContact(entity_id=e.id,contact_type="phone",value="9876543210"),EntityWebsite(entity_id=e.id,url="https://abc.example",domain="abc.example",verification_status="verified"),EntitySource(entity_id=e.id,source_type="fixture",source_url="https://source.example")]); db.commit()
        result=school_benchmark(db)
        assert result["unique_schools"]==1
        assert result["coverage"]["udise"]["percent"]==100.0
        assert result["coverage"]["phone"]["percent"]==100.0
        assert result["coverage"]["email"]["percent"]==0.0
        assert result["sources"][0]["entities"]==1
