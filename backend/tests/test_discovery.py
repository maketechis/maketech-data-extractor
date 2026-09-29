from app.collector.discovery import build_discovery_queries
from app.collector.adapters.manual_search import FixtureSearchAdapter
from app.collector.types import RawEntity

def test_bookseller_queries_are_district_scoped():
    queries=build_discovery_queries(entity_type="bookseller",district="Siwan",state="Bihar",country="India")
    assert len(queries)==4
    assert all("Siwan Bihar India" in item.query for item in queries)
    assert {x.entity_term for x in queries}=={"bookseller","book shop","book store","book dealer"}

def test_search_adapter_contract():
    q="bookseller in Siwan Bihar India"
    expected=RawEntity(name="Example Books",source_name="test",source_url="https://example.test")
    adapter=FixtureSearchAdapter({q:[expected]})
    results=list(adapter.collect(entity_type="bookseller",district="Siwan",state="Bihar",country="India"))
    assert expected in results
