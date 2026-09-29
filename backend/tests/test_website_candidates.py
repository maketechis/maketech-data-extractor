from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.database import Base
from app.enrichment.candidates import WebsiteCandidate, candidate_query
from app.enrichment.website_discovery import FixtureWebsiteDiscovery, discover_candidates
from app.models.core import Country, District, Entity, EntityType, State

def test_candidate_is_stored_not_verified():
    engine=create_engine("sqlite:///:memory:"); Base.metadata.create_all(engine)
    with Session(engine) as db:
        c=Country(name="India",iso_code="IN"); t=EntityType(name="Bookseller",slug="bookseller"); db.add_all([c,t]); db.flush()
        s=State(country_id=c.id,name="Bihar"); db.add(s); db.flush()
        d=District(state_id=s.id,name="Siwan",normalized_name="siwan"); db.add(d); db.flush()
        e=Entity(entity_type_id=t.id,name="ABC Book House",normalized_name="abc book house",country_id=c.id,state_id=s.id,district_id=d.id,pin="841226")
        db.add(e); db.commit(); db.refresh(e)
        q=candidate_query(db,e)
        provider=FixtureWebsiteDiscovery({q:[WebsiteCandidate(url="https://abcbooks.example/contact",source_url="https://search.example",source_name="fixture")]})
        result=discover_candidates(db,e,provider)
        assert result["candidates"][0]["status"]=="candidate"
        assert result["candidates"][0]["domain"]=="abcbooks.example"
