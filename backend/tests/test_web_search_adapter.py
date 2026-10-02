from app.collector.adapters.web_search import WebSearchAdapter
from app.sources.search_settings import SearchSettings
def test_web_search_adapter_maps_provenance(monkeypatch):
    class Hit:
        engine="google";title="Example School";url="https://example.edu"
    monkeypatch.setattr("app.collector.adapters.web_search.search_web",lambda q,s:[Hit()])
    rows=WebSearchAdapter(SearchSettings()).collect(entity_type="school",district="Siwan",state="Bihar",country="India")
    assert rows
    assert rows[0].source_name=="google"
    assert rows[0].source_url=="https://example.edu"
    assert rows[0].attributes["engine"]=="google"
