from app.sources.registered_school_sources import for_state
from app.source_discovery.service import discover_sources
from app.sources.search_settings import SearchSettings,SearchMode
def test_bihar_has_multiple_registered_sources():
    rows=for_state("Bihar")
    assert len(rows)>=3 and any("education.gov.in" in x.url for x in rows)
def test_registered_sources_survive_when_search_empty(monkeypatch):
    monkeypatch.setattr("app.source_discovery.service.search_web_diagnostic",lambda q,s,d:[])
    x=discover_sources(entity_type="school",district="Siwan",state="Bihar",country="India",settings=SearchSettings(mode=SearchMode.ALL))
    registry=[s for s in x["sources"] if s["engine"]=="registry"]
    assert len(registry)>=3
