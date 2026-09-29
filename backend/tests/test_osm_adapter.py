import pytest
from app.collector.adapters.osm_overpass import OSMOverpassAdapter

def test_bookseller_overpass_query_is_area_scoped():
    adapter=OSMOverpassAdapter()
    query=adapter._query(123,"bookseller")
    assert 'area(123)' in query
    assert '"shop"="books"' in query

def test_school_overpass_query():
    query=OSMOverpassAdapter()._query(123,"school")
    assert '"amenity"="school"' in query

def test_unsupported_entity_rejected():
    with pytest.raises(ValueError):
        OSMOverpassAdapter()._query(123,"unknown")
