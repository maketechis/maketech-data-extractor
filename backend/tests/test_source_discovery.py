from app.source_discovery.service import classify,discover_sources
from app.sources.search_settings import SearchSettings,SearchMode
def test_classify_government_pdf():
    kind,score=classify("https://x.gov.in/schools.pdf","Siwan school list")
    assert kind=="government_pdf" and score>=80
def test_discovery_collects_sources(monkeypatch):
    class Hit: engine="google";title="Siwan school directory";url="https://x.gov.in/list"
    monkeypatch.setattr("app.source_discovery.service.search_web",lambda q,s:[Hit()])
    x=discover_sources(entity_type="school",district="Siwan",state="Bihar",country="India",settings=SearchSettings(mode=SearchMode.ALL))
    assert x["queries"]==6 and x["sources"] and x["sources"][0]["kind"].startswith("government")
